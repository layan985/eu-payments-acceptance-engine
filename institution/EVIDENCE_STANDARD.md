# Payment Performance Lab — Evidence Standard

Version: 1.0
Status: Public
Effective: 2026-08-16

## Purpose

Every material public or client-facing claim must be traceable to an evidence object. A claim is not strengthened by confident language, visual design, client confidentiality, or internal familiarity. It is strengthened only by source quality, reproducibility, identification, validation, and explicit limitations.

## Canonical evidence classes

Only these public evidence labels are permitted:

- `OFFICIAL SOURCE` — regulator, central bank, law, scheme, standards body, or other authoritative primary source.
- `REAL PUBLIC DATA` — real-world public data from a named first-party or authoritative source.
- `PROVIDER TEST` — retained execution in an identified provider test/sandbox environment.
- `SYNTHETIC` — controlled generated data; never represented as observed merchant behavior.
- `RANDOMIZED SYNTHETIC` — randomized experiment in a controlled synthetic environment.
- `PRODUCTION CLIENT DATA` — analysis of real client production data under an active engagement.
- `EXTERNAL REVIEW` — completed bounded review by an identified qualified external reviewer, with scope and date recorded.
- `INDEPENDENT REPRODUCTION` — completed external rerun from code/data/environment/instructions with outcome recorded.
- `PENDING VALIDATION` — implemented, proposed, simulated, or internally tested work that does not yet satisfy a stronger class.

No alternative badge vocabulary is allowed on public claims.

## Mandatory claim record

Every material number must resolve to:

`CLAIM → NUMBER → EVIDENCE CLASS → SOURCE → WINDOW → N → CODE/QUERY → REPRODUCIBLE? → IDENTIFICATION STATUS → LIMITATION → STATUS`

Every chart or KPI must display or link to:

`SOURCE / N / WINDOW / FILTER / STATUS / LIMITATION / DOWNLOAD DATA`

## Causal language

Observed differences are not called uplift, impact, improvement, or loss caused by a route, PSP, issuer, authentication choice, retry policy, or payment method unless an identification strategy supports the statement.

Permitted language for descriptive evidence:

- observed differential
- association
- concentration
- decomposition
- investigation signal
- estimated opportunity

Causal or intervention language requires a defensible experiment or quasi-experimental design and an explicit guardrail assessment.

## Client outcome ladder

Client value claims are reported at the strongest completed tier only:

1. `LOSS OBSERVED`
2. `OPPORTUNITY ESTIMATED`
3. `EXPERIMENT VALIDATED`
4. `IMPLEMENTED`
5. `FINANCIALLY REALIZED`

A projected annualization never becomes `FINANCIALLY REALIZED` without realized accounting or settlement evidence.

## Required guardrails

Authorization is never optimized in isolation. Depending on the intervention, analysis must consider fraud, disputes, processing cost, authentication, customer experience, latency, operational exceptions, settlement, regulatory constraints, and measurement integrity.

## Corrections

A material methodological, numerical, data, or provenance error must trigger:

1. public correction note;
2. affected claim status change;
3. version increment;
4. rerun of dependent outputs where practical;
5. entry in the corrections register.

## Falsification rule

Every serious report includes a `What would falsify or materially weaken this?` section. Evidence that contradicts a claim is retained, not discarded to preserve a narrative.
