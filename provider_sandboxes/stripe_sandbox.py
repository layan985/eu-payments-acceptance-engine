import json, os, urllib.parse, urllib.request

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

def run(scenario='success'):
    key = os.getenv('STRIPE_TEST_SECRET_KEY')
    if not key:
        raise SystemExit('Set STRIPE_TEST_SECRET_KEY to a Stripe sandbox/test secret key.')
    body = urllib.parse.urlencode(build_payload(scenario)).encode()
    req = urllib.request.Request(API, data=body, method='POST')
    token = __import__('base64').b64encode((key + ':').encode()).decode()
    req.add_header('Authorization', 'Basic ' + token)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Idempotency-Key', f'layan-portfolio-{scenario}')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(json.dumps(json.load(r), indent=2))
    except urllib.error.HTTPError as e:
        print(e.read().decode())
        raise

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('scenario', choices=sorted(SCENARIOS), nargs='?', default='success')
    run(p.parse_args().scenario)
