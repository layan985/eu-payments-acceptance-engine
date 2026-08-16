# The Authorization Rate Is Lying to You

<div class="meta-line"><span>SYNTHETIC</span><span>FOUNDER PRODUCED</span><span>UPDATED 2026-08-16</span></div>

## Finding

A single payment cohort can produce several valid but materially different “authorization” numbers. The object and denominator are part of the claim.

<div class="bar-chart" data-title="Same cohort · three denominators">
<div><b>Attempt authorization</b><i style="--v:31%"></i><strong>87.13%</strong></div>
<div><b>Intent resolution</b><i style="--v:82%"></i><strong>92.20%</strong></div>
<div><b>Economic value resolution</b><i style="--v:82%"></i><strong>92.18%</strong></div>
</div>

| Metric | Definition | Seeded result | Business question |
|---|---|---:|---|
| Attempt authorization | authorized attempts / all attempts | 87.13% | how efficiently do attempts authorize? |
| Intent resolution | intents with ≥1 approval / intents | 92.20% | how many payment intents eventually resolve? |
| Economic resolution | resolved intended value / total intended value | 92.18% | how much intended value resolves? |
| Retry share | retry attempts / all attempts | 5.50% | how much attempt load is recovery traffic? |

## Attempt-level evidence

Seed `20260816` produces 30,000 payment intents and 31,746 attempts. These are actual rows from the generated research artifact:

| payment_intent_id | attempt | authorized | decline_reason |
|---|---:|---:|---|
| pi_0000004 | 1 | 0 | authentication_failed |
| pi_0000004 | 2 | 1 | — |
| pi_0000034 | 1 | 0 | insufficient_funds |
| pi_0000034 | 2 | 0 | insufficient_funds |
| pi_0000063 | 1 | 0 | do_not_honor |
| pi_0000063 | 2 | 0 | do_not_honor |
| pi_0000098 | 1 | 0 | authentication_failed |
| pi_0000098 | 2 | 1 | — |

**Inspect:** [research_artifacts.py](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/research_artifacts.py) · [reproduce.py](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/reproduce.py)

## Data-generating process

Each intent begins with one attempt at a 90% seeded initial approval probability. Failed attempts receive a seeded decline class. Soft failures have a 62% retry probability and 38% retry-approval probability; hard failures have an 8% retry probability and 4% retry-approval probability. A subset of repeated soft failures receives a third attempt.

Those are transparent design parameters, not merchant benchmarks.

## Retry contamination

Attempt authorization can fall while intent resolution rises because successful recovery requires additional attempts. Conversely, a retry system can raise eventual approval while adding cost, latency, issuer velocity pressure or fraud exposure. A dashboard that shows one rate without the object can reward the wrong behavior.

## 3DS is a selected population

<div class="bar-chart two" data-title="Raw 3DS split · seeded environment">
<div><b>No 3DS flag</b><i style="--v:75%"></i><strong>93.75%</strong></div>
<div><b>3DS flag</b><i style="--v:43%"></i><strong>92.15%</strong></div>
</div>

The raw difference is deliberately **not** called a 3DS penalty. Even in the canonical synthetic generator, method and mobile+3DS structure alter the populations. In production, issuer, market, risk, exemption and merchant policy add further selection.

## What must exist before an acceptance claim is credible

1. Exact denominator and eligibility filter.
2. Stable payment-intent identity across retries.
3. Explicit deduplication rule.
4. Rule for authentication and post-authorization states.
5. Traffic-mix comparison before and after.
6. Fraud, dispute, cost and latency guardrails.
7. Uncertainty statement or confidence interval.
8. Observed association kept separate from identified intervention.

## Reproduce

```bash
python reproduce.py
```

## Limitations

Retry probabilities and success rates are synthetic. The cohort omits real customer abandonment, issuer velocity behavior, network-token changes, asynchronous methods, fraud and actual processing cost. The research demonstrates measurement integrity rather than prescribing a universal retry policy.