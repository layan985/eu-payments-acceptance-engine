# Payment Performance Audit Methodology

## 1. Decision question

Every engagement starts with a bounded decision question, not a generic dashboard request. Examples include: where authorization is being lost; whether a retry policy recovers soft declines economically; whether a routing difference survives traffic-mix adjustment; whether 3DS friction is creating avoidable abandonment; or whether payment-state and reconciliation defects are distorting operational metrics.

## 2. Evidence perimeter

Before analysis, record the merchant, geography, currency, PSP/acquirer, payment methods, channels, period, event grain, production/test status, exclusions and known instrumentation gaps. Provider-test records, synthetic records, official market statistics and production client records remain separate evidence classes.

## 3. Data contract

Minimum event-level fields are requested only when required by the question. Typical domains include payment/attempt identifiers, timestamps, amount/currency, country, issuer/BIN attributes where lawfully available, route/processor, payment method, authentication state, raw and normalized decline reason, retry sequence, capture/refund state, fraud decision, fees, settlement/payout and reconciliation identifiers.

Raw PAN, CVV and unnecessary sensitive personal data are outside the analytical perimeter.

## 4. Metric contract

Each metric is defined before comparison. The denominator, event grain, eligibility rule, exclusion logic, time zone, treatment of retries and duplicate attempts, and treatment of partial capture/refund must be explicit. A percentage without a denominator contract is not an audit result.

## 5. Diagnostic sequence

1. Reconcile event counts and states.
2. Establish baseline funnel and failure taxonomy.
3. Segment by the variables that can plausibly change the mechanism.
4. Separate descriptive gaps from intervention hypotheses.
5. Quantify economic exposure without calling modeled exposure realized value.
6. Classify each finding as `FIX`, `INVESTIGATE`, `TEST`, or `DO_NOT_TOUCH`.
7. Where testable, define a controlled experiment or staged rollout with guardrails.
8. Record implementation separately from the recommendation.
9. Measure outcomes on a declared post-intervention window.

## 6. Causal language

Observed route, country, PSP or method gaps are descriptive until a credible identification strategy supports a causal statement. Randomized tests, phased rollouts, strong quasi-experiments or another defensible counterfactual are required before an intervention is described as causing uplift.

## 7. Finding record

Every material finding must resolve to:

`finding_id → evidence → metric → slice → magnitude → mechanism hypothesis → decision → confidence → validation plan → limitation → owner/status`

## 8. Outcome validation

Baseline and measurement windows are fixed and disclosed. Guardrails are checked. Realized value is calculated from measured incremental outcomes under a documented economic model, not from the initial opportunity estimate.

## 9. Publication boundary

Client identity, production metrics, case-study details and acceptance evidence are published only with permission. Confidentiality does not permit invented anonymized outcomes. If a production outcome cannot be published, the public register records that the evidence is withheld rather than manufacturing a proxy claim.
