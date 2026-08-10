# PSP sandbox verification

This folder upgrades the portfolio from an offline simulator to credential-gated calls against real PSP test environments.

## Stripe

`stripe_sandbox.py` creates and confirms PaymentIntents with official Stripe test PaymentMethods for successful Visa authorization, generic issuer decline, insufficient-funds decline, and a 3DS-required flow.

Set `STRIPE_TEST_SECRET_KEY` locally. Never commit it.

```bash
python provider_sandboxes/stripe_sandbox.py success
python provider_sandboxes/stripe_sandbox.py generic_decline
python provider_sandboxes/stripe_sandbox.py insufficient_funds
python provider_sandboxes/stripe_sandbox.py 3ds_required
```

The 3DS-required scenario is expected to demonstrate an authentication state rather than a frictionless final success.

### Executed evidence

The Stripe path was executed against Stripe's test API on 2026-08-10 using a developer-owned test secret key. A deliberately insufficient-funds payment produced a card-error response, and the 3DS-required flow reached `requires_action` with a Visa 3DS2 fingerprint path.

See `evidence/stripe_2026-08-10.md` for the redacted record. No secret key, client secret, account identifier, customer data or raw certificate material is stored.

## Adyen

`adyen_sandbox.py` calls the Adyen Checkout test `/payments` endpoint using the documented `test_`-prefixed encrypted test-card fields.

Set locally:

```text
ADYEN_TEST_API_KEY=...
ADYEN_TEST_MERCHANT_ACCOUNT=...
```

Then run:

```bash
python provider_sandboxes/adyen_sandbox.py
```

## Evidence to retain

After running each provider, save a redacted JSON response under `evidence/` containing only the PSP reference, sandbox marker, result/status, amount/currency, scenario name and timestamp. Never commit API keys, webhook secrets, client secrets, cardholder data or unredacted account identifiers.

## Official documentation

- Stripe testing: https://docs.stripe.com/testing
- Stripe PaymentIntents: https://docs.stripe.com/api/payment_intents/create
- Stripe webhooks: https://docs.stripe.com/webhooks
- Adyen testing: https://docs.adyen.com/development-resources/testing
- Adyen Checkout API: https://docs.adyen.com/api-explorer/Checkout/latest/overview
- Adyen test cards: https://docs.adyen.com/development-resources/testing/test-card-numbers/
