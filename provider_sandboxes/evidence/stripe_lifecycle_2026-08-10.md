# Stripe authorize → capture → refund evidence — 2026-08-10

This record documents local execution of `provider_sandboxes/stripe_lifecycle.py` against Stripe's test API using a developer-owned test secret key.

No API key, client secret, customer data, full account identifier, or raw provider payload is retained here.

## Executed flow

The lifecycle command completed successfully on 2026-08-10:

```bash
python provider_sandboxes/stripe_lifecycle.py
```

The script is not a passive request demo. It enforces two provider-state assertions before continuing:

1. the manually captured PaymentIntent must return `requires_capture` after authorization;
2. the PaymentIntent must return `succeeded` after capture.

If either state differs, the script raises a runtime error rather than representing the flow as successful.

After capture, the script submits a refund request against the same PaymentIntent and only reaches its final evidence output if the Stripe API call returns successfully. The exact refund-status field is not reproduced in this record because the redacted console payload was not retained in the review trail.

## What this establishes

- a real Stripe test PaymentIntent was created with `capture_method=manual`;
- the authorization reached Stripe's `requires_capture` state;
- the same PaymentIntent was captured successfully;
- a refund request was accepted by Stripe's test API against that PaymentIntent;
- idempotency keys were supplied separately for authorization, capture and refund.

## Claim boundary

This is sandbox/test-environment execution. It does not imply live-money processing, production merchant ownership, settlement completion, dispute handling, production authorization uplift, or Stripe certification.