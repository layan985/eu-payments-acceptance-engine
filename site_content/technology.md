# Technology

<div class="meta-line"><span>EXECUTED</span><span>TESTED</span><span>REPRODUCIBLE</span></div>

## Analytics

Deterministic 300,000-attempt generator, acceptance segmentation, decline taxonomy, randomized synthetic routing experiment, retry-denominator research and payment-state research.

## Stripe test path

The repository contains executed Stripe test-mode PaymentIntent scenarios, 3DS `requires_action`, a manual authorization → capture → refund lifecycle, and signed-webhook verification. Secrets are not retained.

## State controls

Raw-body signature verification, replay tolerance, persistent event-ID ledger, duplicate-event claiming, lifecycle invariants and idempotency-aware API requests.

## One-command technical gate

```bash
python reproduce.py
```

That command regenerates the core metrics and research artifacts and runs the test suite. It exits non-zero on drift or test failure.

[Technical repository](https://github.com/layan985/eu-payments-acceptance-engine) · [CI](https://github.com/layan985/eu-payments-acceptance-engine/actions/workflows/tests.yml) · [provider evidence](https://github.com/layan985/eu-payments-acceptance-engine/tree/main/provider_sandboxes/evidence)