# Evidence Room

<div class="meta-line"><span>8 PROOF OBJECTS</span><span>CLAIM → ARTIFACT → LIMITATION</span><span>UPDATED 2026-08-16</span></div>

Every object below has something inspectable behind it. Production outcomes, external review and independent reproduction remain empty/pending where the evidence does not yet exist.

## 01 · Authorization forensics

<div class="bar-chart" data-title="Seeded authorization rate by market">
<div><b>DE</b><i style="--v:35%"></i><strong>91.79%</strong></div><div><b>FR</b><i style="--v:72%"></i><strong>93.13%</strong></div><div><b>NL</b><i style="--v:78%"></i><strong>93.32%</strong></div><div><b>PT</b><i style="--v:87%"></i><strong>93.65%</strong></div>
</div>

**Artifact:** 300,000 deterministic attempts, seed 42. Overall authorization 93.0977%.  
**Code:** [generator](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/generate_data.py) · [analysis](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/analyze.py)  
**Boundary:** descriptive synthetic concentration, not production causality.

## 02 · Germany 372 bps investigation

<div class="compare-chart"><div class="observed"><span>OBSERVED · NOT CAUSAL</span><b>372.39 bps</b><p>PSP_A 93.03% vs PSP_B 89.31% in Germany.</p></div><div class="randomized"><span>RANDOMIZED SYNTHETIC</span><b>247.88 bps</b><p>Separate 40,000-attempt experiment; 95% CI 190.86–304.91 bps.</p></div></div>

The first number is a route screen. The second is a separately assigned experiment. They are not interchangeable.

**Artifact:** [Report 001](/research/checkout-leak-audit) · [experiment code](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/experiment.py)

## 03 · 3DS diagnostic

<div class="bar-chart two" data-title="Raw 3DS split · seeded environment"><div><b>No 3DS flag</b><i style="--v:75%"></i><strong>93.75%</strong></div><div><b>3DS flag</b><i style="--v:43%"></i><strong>92.15%</strong></div></div>

Raw 3DS/non-3DS comparison is selected by method and seeded mobile+3DS structure. In production, market, issuer, risk, exemptions and merchant policy add further selection. It is not an A/B test.

**Provider artifact:** [Stripe 3DS requires_action execution record](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/provider_sandboxes/evidence/stripe_2026-08-10.md)

## 04 · Retry pathology

Seed `20260816`: 30,000 payment intents → 31,746 attempts. Attempt authorization 87.13%; intent resolution 92.20%; economic-value resolution 92.18%.

| intent | attempt | auth | decline |
|---|---:|---:|---|
| pi_0000004 | 1 | 0 | authentication_failed |
| pi_0000004 | 2 | 1 | — |
| pi_0000034 | 1 | 0 | insufficient_funds |
| pi_0000034 | 2 | 0 | insufficient_funds |
| pi_0000098 | 1 | 0 | authentication_failed |
| pi_0000098 | 2 | 1 | — |

**Artifact:** [Report 002](/research/authorization-rate) · [artifact generator](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/research_artifacts.py)

## 05 · Stripe execution record

| Executed claim | Retained evidence |
|---|---|
| success / generic decline / insufficient funds / 3DS requires_action | [PaymentIntent record](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/provider_sandboxes/evidence/stripe_2026-08-10.md) |
| manual authorization → capture → refund request | [lifecycle record](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/provider_sandboxes/evidence/stripe_lifecycle_2026-08-10.md) |
| signed Stripe test webhook accepted after signature verification | [webhook record](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/provider_sandboxes/evidence/stripe_webhook_2026-08-10.md) |
| persistent duplicate-event handling | implementation + contract tests; **no claim a real duplicate delivery was observed** |

All are `PROVIDER TEST`, not production certification.

## 06 · Reconciliation integrity

Seeded payment-state cohort: 20,000 intents, 61,134 delivered events, 1,036 duplicate events. Naive delivered-event counting overstates unique captures by 1.84% and refunds by 1.27%.

**Artifact:** [Payment State Integrity](/research/payment-state-integrity)

## 07 · Payment state model

<div class="state-line"><span>CREATED</span><b>→</b><span>AUTHORIZED</span><b>→</b><span>CAPTURED</span><b>→</b><span>SETTLED</span><i>branches: DECLINED · RETRY · REVERSED · REFUNDED · DISPUTED</i></div>

Provider event state, merchant object state and economic state are kept distinct.

## 08 · Proof ledger

| Claim | Evidence class | Status | Limitation |
|---|---|---|---|
| 93.10% seeded overall auth | SYNTHETIC | LIVE | not merchant performance |
| 372.39 bps Germany route difference | SYNTHETIC · OBSERVED | LIVE | not causal / not uplift |
| 247.88 bps randomized effect | RANDOMIZED SYNTHETIC | LIVE | separate synthetic experiment |
| Stripe payment lifecycle | PROVIDER TEST | LIVE | test mode; no production certification |
| Production client outcome | PRODUCTION CLIENT DATA | **NONE PUBLISHED** | no completed public case |
| External review | EXTERNAL REVIEW | **PENDING** | no outside review returned |
| Independent reproduction | INDEPENDENT REPRODUCTION | **PENDING** | no outside rerun returned |

**Canonical:** [Proof Ledger](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/PROOF_LEDGER.md) · [CI](https://github.com/layan985/eu-payments-acceptance-engine/actions/workflows/tests.yml) · [reproduce.py](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/reproduce.py)