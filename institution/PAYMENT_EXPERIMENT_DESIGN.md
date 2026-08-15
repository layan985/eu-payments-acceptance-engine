# Payment Experiment Design Standard

## Experiment header

Record `experiment_id`, audit/finding linkage, owner, start/end rule, population, treatment, control, allocation unit, randomization unit, primary metric, guardrails and stopping rule before launch.

## Hypothesis

State the mechanism and expected direction before inspecting the treatment result. Example: routing eligible transactions through route B increases issuer authorization among the eligible population without increasing fraud loss, processing cost or payment latency beyond the declared guardrails.

## Eligibility and exclusions

Define the exact traffic eligible for assignment. Exclusions must not be changed after results are known without recording the deviation and rerunning the analysis under both specifications where feasible.

## Assignment

Prefer deterministic reproducible randomization keyed to a stable unit. Record seed/hash logic where appropriate. Check balance on pre-treatment dimensions that materially affect authorization or fraud risk.

## Primary estimand

The primary effect is defined on the pre-specified denominator. Retry/recovery experiments must distinguish attempt-level authorization from order/customer recovery to avoid denominator inflation.

## Guardrails

Typical guardrails include fraud/chargeback exposure, payment latency, customer abandonment, cost per successful payment, duplicate capture risk, operational exception rate and settlement/reconciliation integrity.

## Analysis

Report treatment/control N, raw rates, absolute effect, relative effect, uncertainty interval, missingness, exclusions and any noncompliance. Segment results are exploratory unless pre-specified or adjusted for multiplicity.

## Economics

Convert measured incremental successful payments into economic value only with an explicit margin/value assumption and subtract incremental processing, fraud, operational and implementation costs. Do not equate authorization uplift with profit uplift.

## Decision

Conclude with one of: `ROLL_OUT`, `EXTEND TEST`, `ROLL BACK`, `NO MATERIAL EFFECT`, `INCONCLUSIVE`. Preserve negative and inconclusive results.
