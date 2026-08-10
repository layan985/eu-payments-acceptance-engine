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

`adyen_sandbox.py` calls the Adyen Checkout test `/payments` endpoint using Adyen test-environment encrypted-card placeholders and documented `RequestedTestAcquirerResponseCode` values.

The CLI exposes four scenarios:

- `success` -> test response code `1` / expected `Authorised`
- `generic_decline` -> code `2` / expected `Refused`
- `insufficient_funds` -> code `12` / expected `Refused` with not-enough-balance semantics
- `authentication_required` -> code `38` / expected `Refused` with authentication-required semantics

Set locally:

```text
ADYEN_TEST_API_KEY=...
ADYEN_TEST_MERCHANT_ACCOUNT=...
```

Then run:

```bash
python provider_sandboxes/adyen_sandbox.py success
python provider_sandboxes/adyen_sandbox.py generic_decline
python provider_sandboxes/adyen_sandbox.py insufficient_funds
python provider_sandboxes/adyen_sandbox.py authentication_required
```

The script prints only an evidence-safe summary: scenario, result/refusal fields, PSP reference, merchant reference, amount/currency and action type. Raw action payloads and credentials are not printed.

## Evidence to retain

After running each provider, save a redacted record under `evidence/` containing only the PSP reference, sandbox marker, result/status, amount/currency, scenario name and timestamp. Never commit API keys, webhook secrets, client secrets, cardholder data or unredacted account identifiers.

## Official documentation

- Stripe testing: https://docs.stripe.com/testing
- Stripe PaymentIntents: https://docs.stripe.com/api/payment_intents/create
- Stripe webhooks: https://docs.stripe.com/webhooks
- Adyen testing result codes: https://docs.adyen.com/development-resources/testing/result-codes/
- Adyen API authentication: https://docs.adyen.com/development-resources/api-authentication/
- Adyen Checkout API v72: https://docs.adyen.com/api-explorer/Checkout/72/post/payments
