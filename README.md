# EU Payments Acceptance Engine

[![tests](https://github.com/layan985/eu-payments-acceptance-engine/actions/workflows/tests.yml/badge.svg)](https://github.com/layan985/eu-payments-acceptance-engine/actions/workflows/tests.yml)

A public technical record for diagnosing payment-acceptance loss without turning descriptive differences into invented uplift.

> **Question:** when authorization differs across markets, devices, authentication paths and routes, what is actually established, what is merely observed, and what intervention is safe to test?

## One-command reproduction

```bash
python reproduce.py
```

That single command, with no network access and no provider credentials:

1. regenerates the canonical **300,000-attempt synthetic merchant environment** with seed 42;
2. recomputes the headline authorization metrics and fails if they drift;
3. reruns the separate **40,000-attempt randomized synthetic routing experiment** with seed 7;
4. rebuilds the retry-denominator and payment-state research artifacts;
5. verifies the published seeded metrics for those research artifacts; and
6. runs the full unit-test suite.

The command exits non-zero on metric drift or test failure. Generated research data is written to `output/research_artifacts/`.

## Canonical seeded results

| Metric | Result | Evidence class |
|---|---:|---|
| Payment attempts | 300,000 | `SYNTHETIC` |
| Overall authorization | 93.10% | `SYNTHETIC` |
| Germany / PSP_A | 93.03% | `SYNTHETIC` |
| Germany / PSP_B | 89.31% | `SYNTHETIC` |
| Raw Germany processor gap | 372 bps | `SYNTHETIC · OBSERVATIONAL · NOT CAUSAL` |
| Randomized treatment-control effect | ~248 bps | `RANDOMIZED SYNTHETIC` |
| Randomized 95% CI | ~191–305 bps | `RANDOMIZED SYNTHETIC` |

**The 372 bps number is not an uplift estimate.** It is a descriptive screening signal in a controlled synthetic environment. The ~248 bps result comes from a separate randomized synthetic experiment and answers a different question.

## Research artifacts

`research_artifacts.py` generates two additional transparent synthetic investigations used by the public research notes:

- a payment-intent / retry cohort that makes attempt-level and intent-level denominators inspectably different;
- a payment-state event stream with seeded duplicate delivery and state-aware counting.

These are methodological demonstrations, not merchant benchmarks.

## European market context

Real European market context is kept separate from the synthetic merchant layer. `ECB_MARKET_CONTEXT.md` tracks official ECB / EBA aggregates and `ecb_market_snapshot.py` provides an optional API pull. Network data is deliberately excluded from the default reproduction path so an external API outage cannot invalidate the core reproducibility check.

## Stripe test-environment verification

The repository's Stripe path has been exercised against Stripe's real test API using developer-owned test credentials. Retained redacted evidence covers:

- PaymentIntent success;
- generic and insufficient-funds declines;
- a 3DS flow reaching `requires_action`;
- a separate manual authorization → capture → refund lifecycle;
- an end-to-end Stripe CLI test webhook accepted after `Stripe-Signature` verification.

Evidence records:

- [`provider_sandboxes/evidence/stripe_2026-08-10.md`](provider_sandboxes/evidence/stripe_2026-08-10.md)
- [`provider_sandboxes/evidence/stripe_lifecycle_2026-08-10.md`](provider_sandboxes/evidence/stripe_lifecycle_2026-08-10.md)
- [`provider_sandboxes/evidence/stripe_webhook_2026-08-10.md`](provider_sandboxes/evidence/stripe_webhook_2026-08-10.md)

The persistent duplicate-event ledger and expanded failure-operation paths are implemented and contract-tested. A real duplicate provider delivery is **not** claimed by the retained execution evidence.

## Operational implementation

- `generate_data.py` — deterministic synthetic merchant environment.
- `analyze.py` — market × processor acceptance diagnostics and decline taxonomy.
- `experiment.py` — randomized synthetic routing evaluation with confidence interval.
- `research_artifacts.py` — retry-denominator and payment-state research datasets.
- `reproduce.py` — canonical one-command verification gate.
- `provider_sandboxes/stripe_sandbox.py` — PaymentIntent test scenarios.
- `provider_sandboxes/stripe_lifecycle.py` — manual authorization, capture and refund.
- `provider_sandboxes/stripe_webhook_server.py` — raw-body signature verification and event-id ledger.
- `provider_sandboxes/stripe_failure_ops.py` — decline classification / recovery operations.
- `sql/acceptance_diagnostics.sql` — SQL acceptance analysis.

## Production-security standard

`institution/SECURITY_CONFIDENTIALITY.md` states the public operating standard for client data. Default analytical intake excludes full PAN, CVV/CVC, card-track data, authentication secrets, private keys, passwords and unnecessary directly identifying customer data. The document does not claim PCI DSS, processor, scheme or provider certification.

## External validation

- `EXTERNAL_REVIEW.md` is the adversarial review packet.
- `ADOPTION.md` is the validation register.
- External review: **PENDING**.
- Independent reproduction: **PENDING**.

Stars, forks and self-run CI are not counted as external validation.

## Claim boundary

The merchant transaction environment and added research cohorts are synthetic. Official ECB/EBA material is real public market context. The retained Stripe records are provider-test evidence. This repository does not claim production merchant access, live-money processing, provider certification, real merchant revenue uplift, external review, or independent reproduction unless the relevant evidence register changes.
