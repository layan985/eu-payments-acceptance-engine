import hashlib
import hmac
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "provider_sandboxes"))

from stripe_lifecycle import build_authorize_payload, summarize_payment_intent, summarize_refund
from stripe_webhook_server import summarize_event, verify_signature


class StripeLifecycleTests(unittest.TestCase):
    def test_manual_capture_payload(self):
        payload = build_authorize_payload()
        self.assertEqual(payload["capture_method"], "manual")
        self.assertEqual(payload["confirm"], "true")
        self.assertEqual(payload["payment_method"], "pm_card_visa")
        self.assertEqual(payload["currency"], "eur")

    def test_payment_intent_summary_excludes_secret(self):
        data = {
            "id": "pi_test",
            "status": "requires_capture",
            "amount": 1299,
            "amount_capturable": 1299,
            "amount_received": 0,
            "currency": "eur",
            "livemode": False,
            "latest_charge": "ch_test",
            "client_secret": "never-print-this",
        }
        summary = summarize_payment_intent(data, "authorization")
        self.assertEqual(summary["status"], "requires_capture")
        self.assertNotIn("client_secret", summary)

    def test_refund_summary_excludes_raw_payment_details(self):
        data = {
            "id": "re_test",
            "status": "succeeded",
            "amount": 1299,
            "currency": "eur",
            "payment_intent": "pi_test",
            "destination_details": {"card": {"reference": "do-not-print"}},
        }
        summary = summarize_refund(data)
        self.assertEqual(summary["status"], "succeeded")
        self.assertNotIn("destination_details", summary)

    def test_webhook_signature_accepts_valid_signature(self):
        payload = b'{"id":"evt_test","type":"payment_intent.succeeded"}'
        secret = "whsec_test"
        timestamp = 1786363200
        signed_payload = str(timestamp).encode() + b"." + payload
        signature = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
        header = f"t={timestamp},v1={signature}"
        self.assertTrue(verify_signature(payload, header, secret, now=timestamp))

    def test_webhook_signature_rejects_tampered_payload(self):
        payload = b'{"id":"evt_test"}'
        secret = "whsec_test"
        timestamp = 1786363200
        signature = hmac.new(
            secret.encode(), str(timestamp).encode() + b"." + payload, hashlib.sha256
        ).hexdigest()
        header = f"t={timestamp},v1={signature}"
        self.assertFalse(verify_signature(b'{"id":"evt_other"}', header, secret, now=timestamp))

    def test_webhook_signature_rejects_replay_outside_tolerance(self):
        payload = b"{}"
        secret = "whsec_test"
        timestamp = 1786363200
        signature = hmac.new(
            secret.encode(), str(timestamp).encode() + b"." + payload, hashlib.sha256
        ).hexdigest()
        header = f"t={timestamp},v1={signature}"
        self.assertFalse(verify_signature(payload, header, secret, now=timestamp + 301))

    def test_event_summary_is_minimal(self):
        event = {
            "id": "evt_test",
            "type": "payment_intent.succeeded",
            "livemode": False,
            "data": {
                "object": {
                    "id": "pi_test",
                    "status": "succeeded",
                    "amount_received": 1299,
                    "currency": "eur",
                    "client_secret": "never-print-this",
                }
            },
        }
        summary = summarize_event(event)
        self.assertEqual(summary["event_type"], "payment_intent.succeeded")
        self.assertNotIn("client_secret", summary)


if __name__ == "__main__":
    unittest.main()
