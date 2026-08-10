# Stripe signed-webhook evidence — 2026-08-10

This record documents an end-to-end Stripe test webhook delivery through the repository's local webhook verifier.

## Executed path

On 2026-08-10, a developer-owned Stripe test account and Stripe CLI were used to forward a test event to the local endpoint at `http://localhost:4242/webhook`.

The execution was reported successful after:

1. Stripe CLI generated and forwarded the test webhook;
2. the local server received the raw request body and `Stripe-Signature` header;
3. the repository's HMAC verifier accepted the signature within its replay-tolerance window; and
4. the endpoint acknowledged the event with HTTP 200.

No webhook signing secret, API secret, event payload, customer information, or account identifier is retained in this record.

## What is implemented

`provider_sandboxes/stripe_webhook_server.py` verifies the raw signed payload before parsing JSON. It also keeps a local SQLite event ledger keyed by Stripe `event_id` so a repeated delivery can be acknowledged without processing the event twice.

The duplicate-event ledger was added after the first live webhook verification and is contract-tested in CI. This evidence record does not claim a real duplicate delivery was observed unless a later execution record explicitly documents one.

## Claim boundary

This establishes that the Stripe webhook receiver has been exercised against a real Stripe test-event delivery and successfully verified a Stripe signature. It does not establish production webhook traffic, production reliability, or live-money processing.