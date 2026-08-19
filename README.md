# EU Payments Acceptance Engine

[![tests](https://github.com/layan985/eu-payments-acceptance-engine/actions/workflows/tests.yml/badge.svg)](https://github.com/layan985/eu-payments-acceptance-engine/actions/workflows/tests.yml)

A public technical record for diagnosing payment-acceptance loss without turning descriptive differences into invented uplift.

> **Question:** when authorization differs across markets, devices, authentication paths and routes, what is actually established, what is merely observed, and what intervention is safe to test?

## Research Note 001 — The PSP leaderboard was the wrong decision rule

A separate deterministic synthetic routing study now tests a harder question: whether a PSP that is worse on average can still belong in a better conditional routing policy.

| Stage | Result | Evidence class |
|---|---:|---|
| Historical PSP_B − PSP_A | -271.5 bps | `SYNTHETIC · OBSERVATIONAL · NOT CAUSAL` |
| Randomized all-B − all-A | -63.8 bps | `RANDOMIZED SYNTHETIC` |
| Randomized 95% CI | -96.0 to -31.6 bps | `RANDOMIZED SYNTHETIC` |
| Frozen policy share sent to PSP_B | 10.38% | `DISCOVERY RULE · FROZEN BEFORE HOLDOUT` |
| Independent holdout policy effect | +46.0 bps | `RANDOMIZED SYNTHETIC · HOLDOUT` |
| Holdout 95% CI | +14.8 to +77.2 bps | `RANDOMIZED SYNTHETIC · HOLDOUT` |
| Holdout two-sided p-value | 0.0038 | `RANDOMIZED SYNTHETIC · HOLDOUT` |

The design uses **250,000 historical attempts**, **100,000 randomized discovery attempts**, and **100,000 independent randomized validation attempts**. The discovery stage evaluates 24 pre-defined issuer × 3DS × cross-border × scheme cells, applies a minimum sample threshold, freezes the rule, and only then evaluates the policy on untouched holdout data.

**Interpretation:** PSP_B is worse globally under randomization, but the frozen policy still routes 10.38% of traffic to PSP_B and outperforms an all-PSP_A strategy on the independent holdout. Provider rankings and transaction-routing policies answer different questions.

- [`RESEARCH_NOTE_001.md`](RESEARCH_NOTE_001.md) — methodology, results, selected cells, limitations and evidence boundary.
- [`research_note_001.py`](research_note_001.py) — fixed-seed executable experiment with drift assertions on the published headline metrics.

This is a **synthetic methodological demonstration**, not a benchmark of any real PSP and not a production revenue claim.

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

`research_note_001.py` is a separate policy-learning study and is intentionally not conflated with the canonical 300,000-attempt diagnostic or the legacy 40,000-attempt experiment above.

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
- `research_note_001.py` — randomized discovery → frozen conditional routing policy → independent holdout validation.
- `research_artifacts.py` — retry-denominator and payment-state research datasets.
- `reproduce.py` — canonical one-command verification gate.
- `provider_sandboxes/stripe_sandbox.py` — PaymentIntent test scenarios.
- `provider_sandboxes/stripe_lifecycle.py` — manual authorization, capture and refund.
- `provider_sandboxes/stripe_webhook_server.py` — raw-body signature verification and event-id ledger.
- `provider_sandboxes/stripe_failure_ops.py` — decline classification / recovery operations.
- `sql/acceptance_diagnostics.sql` — SQL acceptance analysis.

## Production-security standard

`institution/SECURITY_CONFIDENTIALITY.md` states the public operating standard for client data. Default analytical intake excludes full PAN, CVV/CVC, card-track data, authentication secrets, private keys, passwords and unnecessary directly identifying customer data. The document does not claim PCI DSS, processor, scheme or provider certification.

## External and commercial validation

The aggregate validation/commercial registry currently records:

- **3 completed external reviews**;
- **1 completed independent reproduction**;
- **1 paid Checkout audit**;
- **1 measured production case**;
- **1 retained client testimonial**; and
- **1 referral / repeat engagement**.

See [`VALIDATION_AND_COMMERCIAL_PROOF.md`](VALIDATION_AND_COMMERCIAL_PROOF.md), [`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) and [`ADOPTION.md`](ADOPTION.md).

Aggregate counts are public. Reviewer/client identities, production metrics, testimonial wording, contract details and referral counterparties remain permission-controlled unless separately cleared.

Stars, forks and self-run CI are not counted as external validation.

## Claim boundary

The public merchant transaction environment and added research cohorts are synthetic. Official ECB/EBA material is real public market context. The retained Stripe records are provider-test evidence. Separately retained production and external-validation records do **not** retroactively convert synthetic/provider-test results into production results. Observational route differences remain non-causal unless identified as such by a defensible design.
