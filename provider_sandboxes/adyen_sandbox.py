import argparse
import json
import os
import urllib.error
import urllib.request
import uuid

API = 'https://checkout-test.adyen.com/v72/payments'

# Adyen documents these RequestedTestAcquirerResponseCode values for test payments.
SCENARIOS = {
    'success': '1',
    'generic_decline': '2',
    'insufficient_funds': '12',
    'authentication_required': '38',
}


def build_payload(
    merchant_account,
    scenario='success',
    amount=1299,
    currency='EUR',
    reference=None,
):
    if scenario not in SCENARIOS:
        raise ValueError(f'unknown scenario: {scenario}')

    return {
        'merchantAccount': merchant_account,
        'amount': {'currency': currency, 'value': amount},
        'reference': reference or f'layan-portfolio-{scenario}-{uuid.uuid4().hex[:8]}',
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
        'additionalData': {
            'RequestedTestAcquirerResponseCode': SCENARIOS[scenario],
        },
    }


def summarize_response(data, scenario):
    """Return only non-secret fields useful for sandbox evidence."""
    amount = data.get('amount') or {}
    action = data.get('action') or {}
    return {
        'provider': 'adyen',
        'environment': 'test',
        'scenario': scenario,
        'result_code': data.get('resultCode'),
        'refusal_reason': data.get('refusalReason'),
        'refusal_reason_code': data.get('refusalReasonCode'),
        'psp_reference': data.get('pspReference'),
        'merchant_reference': data.get('merchantReference'),
        'amount_value': amount.get('value'),
        'amount_currency': amount.get('currency'),
        'action_type': action.get('type'),
    }


def summarize_error(data, http_status, scenario):
    return {
        'provider': 'adyen',
        'environment': 'test',
        'scenario': scenario,
        'http_status': http_status,
        'status': data.get('status'),
        'error_code': data.get('errorCode'),
        'error_type': data.get('errorType'),
        'message': data.get('message'),
    }


def run(scenario='success'):
    key = os.getenv('ADYEN_TEST_API_KEY')
    merchant = os.getenv('ADYEN_TEST_MERCHANT_ACCOUNT')
    if not key or not merchant:
        raise SystemExit('Set ADYEN_TEST_API_KEY and ADYEN_TEST_MERCHANT_ACCOUNT.')

    payload = build_payload(merchant, scenario=scenario)
    req = urllib.request.Request(API, data=json.dumps(payload).encode(), method='POST')
    req.add_header('X-API-Key', key)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Idempotency-Key', f'layan-portfolio-{scenario}-{uuid.uuid4()}')

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            summary = summarize_response(json.load(response), scenario)
            print(json.dumps(summary, indent=2))
            return summary
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {'errorType': 'non_json_error'}
        summary = summarize_error(data, exc.code, scenario)
        print(json.dumps(summary, indent=2))
        return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('scenario', choices=sorted(SCENARIOS), nargs='?', default='success')
    run(parser.parse_args().scenario)
