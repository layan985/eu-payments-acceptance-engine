import hashlib
import hmac
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

DEFAULT_TOLERANCE_SECONDS = 300


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


class StripeWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/webhook":
            self.send_response(404)
            self.end_headers()
            return

        endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if not endpoint_secret:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"STRIPE_WEBHOOK_SECRET is not configured")
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length)
        signature = self.headers.get("Stripe-Signature", "")

        if not verify_signature(payload, signature, endpoint_secret):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"invalid signature")
            return

        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"invalid json")
            return

        print(json.dumps(summarize_event(event), indent=2))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"received":true}')

    def log_message(self, format, *args):
        return


def run(port=4242):
    if not os.getenv("STRIPE_WEBHOOK_SECRET"):
        raise SystemExit("Set STRIPE_WEBHOOK_SECRET to the Stripe test webhook signing secret (whsec_...).")
    print(f"Stripe webhook listener: http://localhost:{port}/webhook")
    HTTPServer(("127.0.0.1", port), StripeWebhookHandler).serve_forever()


if __name__ == "__main__":
    run()
