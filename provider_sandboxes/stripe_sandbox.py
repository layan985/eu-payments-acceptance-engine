import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request

API = 'https://api.stripe.com/v1/payment_intents'
SCENARIOS = {
    'success': 'pm_card_visa',
    'generic_decline': 'pm_card_visa_chargeDeclined',
    'insufficient_funds': 'pm_card_visa_chargeDeclinedInsufficientFunds',
    '3ds_required': 'pm_card_threeDSecure2Required',
}


def build_payload(scenario='success', amount=1299, currency='eur'):
    if scenario not in SCENARIOS:
        raise ValueError(f'unknown scenario: {scenario}')
    return {
        'amount': str(amount),
        'currency': currency,
        'payment_method': SCENARIOS[scenario],
        'payment_method_types[]': 'card',
        'confirm': 'true',
        'metadata[portfolio_scenario]': scenario,
    }


def summarize_payment_intent(data, scenario):
    """Return only fields safe and useful for portfolio evidence."""
    next_action = data.get('next_action') or {}
    return {
        'provider': 'stripe',
        'environment': 'test',
        'scenario': scenario,
        'payment_intent': data.get('id'),
        'status': data.get('status'),
        'amount': data.get('amount'),
        'currency': data.get('currency'),
        'livemode': data.get('livemode'),
        'payment_method_types': data.get('payment_method_types'),
        'next_action_type': next_action.get('type'),
    }


def summarize_error(data, scenario, http_status):
    """Reduce Stripe error JSON to non-secret diagnostic fields."""
    error = data.get('error') or {}
    payment_method = error.get('payment_method') or {}
    card = payment_method.get('card') or {}
    return {
        'provider': 'stripe',
        'environment': 'test',
        'scenario': scenario,
        'http_status': http_status,
        'error_type': error.get('type'),
        'error_code': error.get('code'),
        'decline_code': error.get('decline_code'),
        'payment_intent': (error.get('payment_intent') or {}).get('id'),
        'livemode': payment_method.get('livemode'),
        'card_brand': card.get('brand'),
        'test_card_last4': card.get('last4'),
    }


def run(scenario='success'):
    key = os.getenv('STRIPE_TEST_SECRET_KEY')
    if not key:
        raise SystemExit('Set STRIPE_TEST_SECRET_KEY to a Stripe sandbox/test secret key.')

    body = urllib.parse.urlencode(build_payload(scenario)).encode()
    req = urllib.request.Request(API, data=body, method='POST')
    token = base64.b64encode((key + ':').encode()).decode()
    req.add_header('Authorization', 'Basic ' + token)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Idempotency-Key', f'layan-portfolio-{scenario}')

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            summary = summarize_payment_intent(json.load(response), scenario)
            print(json.dumps(summary, indent=2))
            return summary
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {'error': {'type': 'non_json_error'}}

        summary = summarize_error(data, scenario, exc.code)
        print(json.dumps(summary, indent=2))

        # Stripe uses HTTP 402 for valid requests whose payments are deliberately
        # declined. Those are expected outcomes for the decline scenarios.
        if exc.code == 402 and scenario in {'generic_decline', 'insufficient_funds'}:
            return summary
        raise


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('scenario', choices=sorted(SCENARIOS), nargs='?', default='success')
    run(parser.parse_args().scenario)
