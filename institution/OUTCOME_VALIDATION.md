# Payment Performance Lab — Outcome Validation Protocol

Version: 1.0
Effective: 2026-08-16

## Objective

Outcome claims must distinguish diagnosis, estimated opportunity, experimentally validated effect, implementation, and financially realized value.

## Outcome record

Each claimed outcome receives `OUT-###` and records:

- engagement ID and client ID;
- intervention;
- primary metric;
- baseline definition and window;
- treatment definition and window;
- N and population filters;
- effect estimate and uncertainty;
- identification design;
- pre-specified decision rule where applicable;
- fraud guardrail;
- dispute guardrail;
- cost guardrail;
- operational guardrail;
- implementation status;
- annualization method;
- strongest evidence class;
- strongest client-value tier;
- reviewer/reproduction status;
- limitations.

## Authorization effects

Authorization-rate movement is expressed in basis points on a stable denominator. Changes in traffic mix, issuer mix, geography, ticket size, payment method, retry population, 3DS state, fraud screening, and route eligibility are tested before attributing an observed difference to an intervention.

## Annualization

Annualized value must state:

`eligible annual attempts × baseline amount/value distribution × validated incremental success effect × capture/settlement factor − incremental fraud/dispute/cost/operational loss`

If any input is modeled rather than realized, the result remains estimated.

## Experiment standard

Where feasible, routing, retry, authentication, or checkout interventions use randomized assignment with:

- stable eligibility rules;
- assignment logging;
- sample-ratio checks;
- pre-specified primary outcome;
- confidence interval;
- guardrail metrics;
- stopping rule;
- contamination checks;
- post-test implementation check.

## Do-not-claim rules

Do not call:

- a raw PSP difference causal uplift;
- declined value automatically recoverable value;
- projected annual value realized revenue;
- provider sandbox success production reliability;
- sample-report metrics client outcomes.
