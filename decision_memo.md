# Decision Memo — Germany PSP Routing Experiment

## Observation
The synthetic transaction sample shows a material raw authorization gap between PSP_A and PSP_B for German traffic.

## Decision
Do not reroute all traffic based on observational data. Run a randomized merchant-routing experiment among eligible German card transactions.

## Primary metric
Authorization rate.

## Guardrails
- fraud loss
- dispute / chargeback rate
- payment latency
- processing cost
- refund rate
- issuer / card-network mix stability

## Stakeholders
Payments Product, Payments Engineering, Fraud/Risk, Finance, Customer Support, PSP account managers.

## Rollout rule
Increase traffic only if the treatment improves authorization with no material deterioration in fraud, disputes, latency or unit economics.
