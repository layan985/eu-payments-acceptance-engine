# Checkout Leak Audit — Sample Diagnostic

<div class="meta-line"><span>SYNTHETIC</span><span>RANDOMIZED SYNTHETIC</span><span>UPDATED 2026-08-16</span></div>

## Decision question

Where does acceptance loss concentrate, which differences are descriptive only, and which intervention is sufficiently identified to test?

<div class="callout danger">No production uplift is claimed. No synthetic route difference is annualized as merchant revenue.</div>

## Headline evidence

| Object | Result | Evidence class | Boundary |
|---|---:|---|---|
| Payment attempts | 300,000 | SYNTHETIC | deterministic seed 42 |
| Overall authorization | 93.0977% | SYNTHETIC | not merchant performance |
| Germany PSP_A | 93.030% / n=13,544 | SYNTHETIC | descriptive slice |
| Germany PSP_B | 89.306% / n=10,464 | SYNTHETIC | descriptive slice |
| Raw Germany gap | 372.39 bps | SYNTHETIC · OBSERVED | **not causal** |
| Randomized effect | 247.88 bps | RANDOMIZED SYNTHETIC | separate 40k experiment |
| Randomized 95% CI | 190.86–304.91 bps | RANDOMIZED SYNTHETIC | separate experiment |

## 1. Data-generating process

The canonical generator emits 300,000 payment attempts across ten countries, three route labels, four payment methods and two device classes. Seed `42` makes the environment deterministic. The code exposes every seeded adjustment rather than hiding it behind a model artifact.

<div class="bar-chart" data-title="Seeded authorization rate by market">
<div><b>AT</b><i style="--v:68%"></i><strong>93.22%</strong></div>
<div><b>BE</b><i style="--v:65%"></i><strong>93.09%</strong></div>
<div><b>DE</b><i style="--v:32%"></i><strong>91.79%</strong></div>
<div><b>ES</b><i style="--v:69%"></i><strong>93.27%</strong></div>
<div><b>FR</b><i style="--v:66%"></i><strong>93.13%</strong></div>
<div><b>PT</b><i style="--v:79%"></i><strong>93.65%</strong></div>
</div>

**Inspect:** [generator](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/generate_data.py) · [analysis](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/analyze.py) · [one-command reproduction](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/reproduce.py)

## 2. Germany processor screen

The seeded Germany split is the screening finding. PSP_A authorizes 93.03%; PSP_B authorizes 89.31%; PSP_C authorizes 93.34%. The raw A–B difference is 372.39 bps.

<div class="bar-chart two" data-title="Germany · observed authorization by route">
<div><b>PSP_A</b><i style="--v:94%"></i><strong>93.03%</strong></div>
<div><b>PSP_B</b><i style="--v:36%"></i><strong>89.31%</strong></div>
<div><b>PSP_C</b><i style="--v:99%"></i><strong>93.34%</strong></div>
</div>

The generator itself seeds a Germany + PSP_B penalty. The screen therefore proves the diagnostic can recover a known failure surface. It does **not** prove a processor would create that effect in production.

## 3. Observed comparison versus identified experiment

<div class="compare-chart">
<div class="observed"><span>OBSERVED · NOT CAUSAL</span><b>372.39 bps</b><p>Germany PSP_A − PSP_B in the seeded 300k environment.</p></div>
<div class="randomized"><span>RANDOMIZED SYNTHETIC</span><b>247.88 bps</b><p>Separate randomized 40k treatment-control experiment.</p></div>
</div>

The randomized experiment realizes 89.403% control versus 91.882% treatment, with a 95% interval of 190.86–304.91 bps and a two-sided p-value around 1.73e-17. It answers a different question from the Germany route screen.

**Inspect:** [experiment.py](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/experiment.py)

## 4. Failure taxonomy

| Seeded decline | Count | Share of declines | Operational interpretation |
|---|---:|---:|---|
| insufficient_funds | 6,475 | 31.27% | soft-failure candidate; recovery requires policy |
| do_not_honor | 5,706 | 27.56% | ambiguous soft failure; do not assume retryability |
| authentication_failed | 4,422 | 21.36% | authentication surface |
| invalid_account | 2,446 | 11.81% | hard failure |
| lost_or_stolen | 1,658 | 8.01% | hard/sensitive failure; no blind retry |

## 5. Decision queue

| State | Finding | Action |
|---|---|---|
| INVESTIGATE | Germany PSP_B raw gap | stratify traffic; verify eligibility and route assignment |
| TEST | routing intervention | pre-specify eligible traffic, primary outcome and fraud/dispute/latency/cost guardrails |
| FIX | metric contract | make attempt, intent, customer and economic-value denominators explicit |
| DO NOT TOUCH | hard decline repeat attempts | do not turn hard/sensitive failures into generic retry volume |

## Method

Descriptive authorization is `authorized attempts / eligible attempts` within the declared slice. Observed route differences remain screening signals. A causal statement requires randomized assignment or a separately defended quasi-experimental design. Authorization is not optimized without fraud, dispute, latency, processing-cost, refund and payment-state guardrails.

## Reproduce

```bash
python reproduce.py
```

The command regenerates the canonical 300k environment, checks the published metrics, reruns the randomized experiment, rebuilds the retry/state research artifacts and runs the full test suite. It exits non-zero on drift.

## Limitations

The merchant environment is synthetic and deliberately simplified. It contains no real merchant issuer mix, local acquiring, network-token state, merchant category, real exemption policy, production fraud or fee schedule. The 372.39 bps route difference is seeded by construction and is **not** a merchant uplift estimate.