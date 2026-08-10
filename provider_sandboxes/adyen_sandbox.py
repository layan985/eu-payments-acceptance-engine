import json
import os
import urllib.error
import urllib.request
import uuid

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


def summarize_response(data):
    """Return only non-secret fields useful for test evidence."""
    amount = data.get('amount') or {}
    action = data.get('action') or {}
    return {
        'provider': 'adyen',
        'environment': 'test',
        'result_code': data.get('resultCode'),
        'psp_reference': data.get('pspReference'),
        'merchant_reference': data.get('merchantReference'),
        'amount_value': amount.get('value'),
        'amount_currency': amount.get('currency'),
        'action_type': action.get('type'),
    }


def summarize_error(data, http_status):
    return {
        'provider': 'adyen',
        'environment': 'test',
        'http_status': http_status,
        'status': data.get('status'),
        'error_code': data.get('errorCode'),
        'error_type': data.get('errorType'),
        'message': data.get('message'),
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
        with urllib.request.urlopen(req, timeout=30) as response:
            summary = summarize_response(json.load(response))
            print(json.dumps(summary, indent=2))
            return summary
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {'errorType': 'non_json_error'}
        summary = summarize_error(data, exc.code)
        print(json.dumps(summary, indent=2))
        raise


if __name__ == '__main__':
    run()
