import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "provider_sandboxes"))

from stripe_failure_ops import SCENARIOS, build_payload, decide_failure, summarize_error


class StripeFailureOpsTests(unittest.TestCase):
    def test_all_test_scenarios_build_payment_intents(self):
        for scenario, payment_method in SCENARIOS.items():
            payload = build_payload(scenario)
            self.assertEqual(payload["payment_method"], payment_method)
            self.assertEqual(payload["confirm"], "true")
            self.assertEqual(payload["currency"], "eur")

    def test_stolen_card_is_never_exposed_in_customer_message(self):
        decision = decide_failure("card_declined", "stolen_card")
        self.assertEqual(decision["retry_policy"], "do_not_retry")
        self.assertNotIn("stolen", decision["safe_customer_message"].lower())

    def test_insufficient_funds_requires_customer_action(self):
        decision = decide_failure("card_declined", "insufficient_funds")
        self.assertEqual(decision["retry_policy"], "retry_after_customer_action")

    def test_incorrect_cvc_requires_data_correction(self):
        decision = decide_failure("incorrect_cvc", None)
        self.assertEqual(decision["retry_policy"], "retry_after_data_correction")

    def test_advice_code_overrides_decline_fallback(self):
        decision = decide_failure("card_declined", "generic_decline", "try_again_later")
        self.assertEqual(decision["retry_policy"], "retry_later")

    def test_summary_excludes_raw_payment_method(self):
        data = {
            "error": {
                "type": "card_error",
                "code": "card_declined",
                "decline_code": "lost_card",
                "payment_intent": {"id": "pi_test", "client_secret": "never-print"},
                "payment_method": {"card": {"fingerprint": "never-print"}},
            }
        }
        summary = summarize_error(data, "lost_card", 402)
        self.assertEqual(summary["payment_intent"], "pi_test")
        self.assertNotIn("payment_method", summary)
        self.assertNotIn("client_secret", summary)


if __name__ == "__main__":
    unittest.main()
