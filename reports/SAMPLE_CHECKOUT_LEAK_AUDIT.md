# Checkout Leak Audit — Flagship Sample Report

**Edition:** Founding sample 001  
**Evidence status:** SYNTHETIC + PROVIDER TEST  
**Production merchant data:** NONE  

## Executive decision

The seeded 300,000-transaction merchant environment shows a 93.10% overall authorization rate. Within the Germany slice, PSP_A authorizes 93.03% and PSP_B 89.31%, a raw difference of 372 basis points.

That 372 bp difference is a diagnostic signal, not a revenue-uplift estimate. The data-generating process for that slice does not justify a causal routing claim. A separate randomized synthetic experiment produces an approximately 248 bp treatment-control difference with a 95% confidence interval of roughly 191–305 bps. The two findings are intentionally kept separate.

**Decision:** investigate the observed route gap; do not forecast recovered revenue from it. If a production merchant shows a similar pattern, test the routing change prospectively with fraud, dispute, latency and cost guardrails.

## 1. Acceptance map

| Measure | Result | Evidence class | Decision use |
| --- | ---: | --- | --- |
| Eligible attempts | 300,000 | SYNTHETIC | reproducible test population |
| Overall authorization | 93.10% | SYNTHETIC | baseline |
| Germany / PSP_A | 93.03% | SYNTHETIC | route diagnostic |
| Germany / PSP_B | 89.31% | SYNTHETIC | route diagnostic |
| Raw route difference | 372 bps | OBSERVATIONAL SYNTHETIC | investigate; not causal |
| Randomized treatment-control difference | ~248 bps | RANDOMIZED SYNTHETIC | experiment demonstration |
| Randomized 95% CI | ~191–305 bps | RANDOMIZED SYNTHETIC | uncertainty interval |

The most common seeded decline is `insufficient_funds`, accounting for roughly 31% of declines. That matters operationally because a high-volume decline class is not automatically a recoverable class: retry policy should depend on the reason, timing, customer action required and provider/network guidance.

## 2. Failure anatomy

A production audit would rank failure states by both count and attempted value, then segment them by market, currency, payment method, device, issuer/route where available, authentication path and retry position.

The required analytical distinction is:

- **where failure concentrates**;
- **which failures can be acted on safely**;
- **which apparent differences survive mix adjustment**;
- **which interventions require randomized or otherwise credible causal evaluation**.

## 3. 3DS and payment-state operations

Stripe test-environment execution retained in the repository covers:

- successful PaymentIntent authorization;
- deliberate generic and insufficient-funds declines;
- a 3DS path reaching `requires_action`;
- manual authorization followed by capture and refund;
- signed webhook delivery accepted after signature verification.

This is provider-test evidence, not production evidence. Its purpose is to show that the audit logic can connect analytical findings to real payment states and operational controls.

## 4. Money-at-risk logic

A real merchant report should calculate:

1. attempted value;
2. failed value;
3. value associated with 3DS abandonment or authentication failure;
4. retry-exposed value;
5. capture/refund/payout exception value where in scope;
6. a narrower **actionable scenario value** that never assumes every failed payment is recoverable.

No money-at-risk number should be presented without the measurement window, currency treatment, eligibility denominator, exclusions and evidence class.

## 5. Recommended action queue

| Priority | Finding | Current evidence | Next action | Guardrail |
| --- | --- | --- | --- | --- |
| P0 | route-level acceptance difference | observational synthetic | reproduce on merchant data; adjust for mix | no uplift claim |
| P0 | high-volume insufficient-funds declines | synthetic | analyze retry timing and sequence | no blind retrying |
| P1 | 3DS friction path | provider test + merchant data required | build challenge/completion funnel | preserve SCA requirements |
| P1 | lifecycle integrity | provider test | reconcile authorization, capture, refund and webhook states | idempotency / duplicate controls |
| P2 | candidate routing intervention | randomized synthetic methodology | pre-specify production experiment | fraud, dispute, latency, cost |

## 6. What a paid production audit adds

A production engagement replaces every synthetic table with merchant-specific evidence and returns:

- authorization and failure maps;
- money-at-risk table;
- decline taxonomy;
- 3DS funnel;
- market × method and device × authentication cuts;
- retry-sequence analysis;
- lifecycle and payout exceptions where available;
- experiment recommendations;
- a ranked action register;
- metric dictionary, QA notes and reproducible appendix.

## Evidence boundary

This sample does **not** claim live-money processing, production merchant access, PCI certification or real merchant revenue uplift. The public proof is a combination of reproducible synthetic analytics and executed Stripe test-environment flows. A real case becomes public only with explicit client approval and visible labeling as production evidence.