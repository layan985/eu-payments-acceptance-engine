import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'provider_sandboxes'))

from stripe_sandbox import (
    build_payload as stripe_payload,
    summarize_error as stripe_error_summary,
    summarize_payment_intent as stripe_payment_summary,
)
from adyen_sandbox import (
    build_payload as adyen_payload,
    summarize_response as adyen_response_summary,
)


class ProviderContractTests(unittest.TestCase):
    def test_stripe_success_payload(self):
        payload = stripe_payload('success')
        self.assertEqual(payload['currency'], 'eur')
        self.assertEqual(payload['payment_method'], 'pm_card_visa')
        self.assertEqual(payload['confirm'], 'true')

    def test_stripe_decline_scenario(self):
        payload = stripe_payload('insufficient_funds')
        self.assertIn('InsufficientFunds', payload['payment_method'])

    def test_stripe_payment_summary_excludes_secrets(self):
        data = {
            'id': 'pi_test',
            'status': 'requires_action',
            'amount': 1299,
            'currency': 'eur',
            'livemode': False,
            'payment_method_types': ['card'],
            'client_secret': 'do-not-print',
            'next_action': {
                'type': 'use_stripe_sdk',
                'use_stripe_sdk': {'three_d_secure_2_source': 'secret-ish-payload'},
            },
        }
        summary = stripe_payment_summary(data, '3ds_required')
        self.assertEqual(summary['status'], 'requires_action')
        self.assertEqual(summary['next_action_type'], 'use_stripe_sdk')
        self.assertNotIn('client_secret', summary)
        self.assertNotIn('next_action', summary)

    def test_stripe_error_summary_excludes_account_and_log_url(self):
        data = {
            'error': {
                'type': 'card_error',
                'code': 'card_declined',
                'decline_code': 'insufficient_funds',
                'request_log_url': 'https://example.test/account-id',
                'payment_method': {
                    'livemode': False,
                    'card': {'brand': 'visa', 'last4': '9995'},
                },
            }
        }
        summary = stripe_error_summary(data, 'insufficient_funds', 402)
        self.assertEqual(summary['decline_code'], 'insufficient_funds')
        self.assertNotIn('request_log_url', summary)

    def test_adyen_success_payload(self):
        payload = adyen_payload('TEST_MERCHANT', scenario='success', reference='portfolio-test')
        self.assertEqual(payload['amount']['currency'], 'EUR')
        self.assertEqual(payload['countryCode'], 'DE')
        self.assertTrue(payload['paymentMethod']['encryptedCardNumber'].startswith('test_'))
        self.assertEqual(payload['reference'], 'portfolio-test')
        self.assertEqual(payload['additionalData']['RequestedTestAcquirerResponseCode'], '1')

    def test_adyen_insufficient_funds_payload(self):
        payload = adyen_payload('TEST_MERCHANT', scenario='insufficient_funds')
        self.assertEqual(payload['additionalData']['RequestedTestAcquirerResponseCode'], '12')

    def test_adyen_response_summary_excludes_raw_action(self):
        data = {
            'resultCode': 'RedirectShopper',
            'pspReference': 'test-reference',
            'merchantReference': 'portfolio-test',
            'amount': {'currency': 'EUR', 'value': 1299},
            'action': {'type': 'redirect', 'url': 'https://secret-ish.example'},
        }
        summary = adyen_response_summary(data, 'authentication_required')
        self.assertEqual(summary['scenario'], 'authentication_required')
        self.assertEqual(summary['action_type'], 'redirect')
        self.assertNotIn('action', summary)


if __name__ == '__main__':
    unittest.main()
