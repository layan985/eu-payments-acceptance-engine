import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'provider_sandboxes'))
from stripe_sandbox import build_payload as stripe_payload
from adyen_sandbox import build_payload as adyen_payload

class ProviderContractTests(unittest.TestCase):
    def test_stripe_success_payload(self):
        p = stripe_payload('success')
        self.assertEqual(p['currency'], 'eur')
        self.assertEqual(p['payment_method'], 'pm_card_visa')
        self.assertEqual(p['confirm'], 'true')

    def test_stripe_decline_scenario(self):
        p = stripe_payload('insufficient_funds')
        self.assertIn('InsufficientFunds', p['payment_method'])

    def test_adyen_test_payload(self):
        p = adyen_payload('TEST_MERCHANT', reference='portfolio-test')
        self.assertEqual(p['amount']['currency'], 'EUR')
        self.assertEqual(p['countryCode'], 'DE')
        self.assertTrue(p['paymentMethod']['encryptedCardNumber'].startswith('test_'))
        self.assertEqual(p['reference'], 'portfolio-test')

if __name__ == '__main__':
    unittest.main()
