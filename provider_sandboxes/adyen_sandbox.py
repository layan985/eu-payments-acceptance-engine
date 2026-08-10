import json, os, urllib.request, uuid

API = 'https://checkout-test.adyen.com/v72/payments'

def build_payload(merchant_account, amount=1299, currency='EUR', reference=None):
    return {
        'merchantAccount': merchant_account,
        'amount': {'currency': currency, 'value': amount},
        'reference': reference or f'layan-portfolio-{uuid.uuid4().hex[:10]}',
        'returnUrl': 'https://example.com/adyen-return',
        'countryCode': 'DE',
        'shopperInteraction': 'Ecommerce',
        'paymentMethod': {
            'type': 'scheme',
            'encryptedCardNumber': 'test_5555555555554444',
            'encryptedExpiryMonth': 'test_03',
            'encryptedExpiryYear': 'test_2030',
            'encryptedSecurityCode': 'test_737',
        },
    }

def run():
    key = os.getenv('ADYEN_TEST_API_KEY')
    merchant = os.getenv('ADYEN_TEST_MERCHANT_ACCOUNT')
    if not key or not merchant:
        raise SystemExit('Set ADYEN_TEST_API_KEY and ADYEN_TEST_MERCHANT_ACCOUNT.')
    payload = build_payload(merchant)
    req = urllib.request.Request(API, data=json.dumps(payload).encode(), method='POST')
    req.add_header('X-API-Key', key)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Idempotency-Key', f'layan-portfolio-{uuid.uuid4()}')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(json.dumps(json.load(r), indent=2))
    except urllib.error.HTTPError as e:
        print(e.read().decode())
        raise

if __name__ == '__main__':
    run()
