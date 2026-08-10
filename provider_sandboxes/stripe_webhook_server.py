import hashlib
import hmac
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from stripe_webhook_store import EventStore

DEFAULT_TOLERANCE_SECONDS = 300
DEFAULT_EVENT_DB = "stripe_webhook_events.db"


def parse_signature_header(header):
    values = {}
    for item in header.split(","):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        values.setdefault(key.strip(), []).append(value.strip())
    return values


def verify_signature(payload, signature_header, endpoint_secret, tolerance=DEFAULT_TOLERANCE_SECONDS, now=None):
    if isinstance(payload, str):
        payload = payload.encode()
    values = parse_signature_header(signature_header)
    timestamps = values.get("t", [])
    signatures = values.get("v1", [])
    if not timestamps or not signatures:
        return False

    try:
        timestamp = int(timestamps[0])
    except ValueError:
        return False

    current_time = int(time.time() if now is None else now)
    if abs(current_time - timestamp) > tolerance:
        return False

    signed_payload = str(timestamp).encode() + b"." + payload
    expected = hmac.new(endpoint_secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    return any(hmac.compare_digest(expected, signature) for signature in signatures)


def summarize_event(event):
    obj = ((event.get("data") or {}).get("object") or {})
    return {
        "event_id": event.get("id"),
        "event_type": event.get("type"),
        "livemode": event.get("livemode"),
        "object_id": obj.get("id"),
        "status": obj.get("status"),
        "amount": obj.get("amount") or obj.get("amount_received"),
        "currency": obj.get("currency"),
    }


def event_store():
    return EventStore(os.getenv("STRIPE_WEBHOOK_DB", DEFAULT_EVENT_DB))


class StripeWebhookHandler(BaseHTTPRequestHandler):
    def _json_response(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        if self.path != "/webhook":
            self._json_response(404, {"error": "not_found"})
            return

        endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if not endpoint_secret:
            self._json_response(500, {"error": "webhook_secret_not_configured"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length)
        signature = self.headers.get("Stripe-Signature", "")

        if not verify_signature(payload, signature, endpoint_secret):
            self._json_response(400, {"error": "invalid_signature"})
            return

        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid_json"})
            return

        summary = summarize_event(event)
        if not summary.get("event_id") or not summary.get("event_type"):
            self._json_response(400, {"error": "invalid_event"})
            return

        store = event_store()
        claimed = store.claim(summary)
        if not claimed:
            duplicate_summary = dict(summary)
            duplicate_summary["duplicate"] = True
            print(json.dumps(duplicate_summary, indent=2))
            self._json_response(200, {"received": True, "duplicate": True})
            return

        try:
            print(json.dumps(summary, indent=2))
            store.mark_processed(summary["event_id"])
        except Exception:
            store.mark_failed(summary["event_id"])
            self._json_response(500, {"received": False})
            return

        self._json_response(200, {"received": True, "duplicate": False})

    def log_message(self, format, *args):
        return


def run(port=4242):
    if not os.getenv("STRIPE_WEBHOOK_SECRET"):
        raise SystemExit("Set STRIPE_WEBHOOK_SECRET to the Stripe test webhook signing secret (whsec_...).")
    print(f"Stripe webhook listener: http://localhost:{port}/webhook")
    print(f"Idempotency ledger: {os.getenv('STRIPE_WEBHOOK_DB', DEFAULT_EVENT_DB)}")
    HTTPServer(("127.0.0.1", port), StripeWebhookHandler).serve_forever()


if __name__ == "__main__":
    run()
