# PFX-1 real-merchant protocol

## Research question

Among payment attempts that fail under the merchant's current policy and remain legally, contractually and operationally eligible for rescue, how much incremental successful customer resolution can be produced by choosing rescue interventions conditional on transaction context rather than using one blanket rule or decline-code rule?

## Primary estimand

The primary estimand is the incremental probability of successful payment-intent resolution under a frozen learned rescue policy versus the best pre-specified blanket eligible rescue policy on an untouched randomized validation sample.

This is not the raw retry authorization rate. The primary outcome is resolved intent/customer payment within the specified horizon, so repeated attempts do not manufacture success by changing the denominator.

## Candidate interventions

Only interventions already permitted for a given payment may enter its action set:

1. no immediate rescue / control;
2. alternate eligible route or acquirer;
3. authentication step-up where permitted;
4. eligible credential or network-token intervention;
5. delayed retry where network rules and Merchant Advice Code / equivalent guidance permit it.

The feasible set is payment-specific. Hard declines and prohibited retry states are excluded before randomization.

## Design

Eligible failed payment intents are randomized among their feasible rescue actions with logged propensities. A fixed discovery/validation split is created before outcome analysis.

Discovery data are used to estimate action-specific conditional outcome models and freeze a context-aware policy. Validation data are never used for policy selection.

Comparators are frozen before validation:

- no-rescue control;
- best pre-specified blanket eligible rescue;
- decline-code-only policy;
- full-context learned policy.

## Primary analysis

Policy value is estimated on the randomized validation set using a doubly robust estimator. Inverse-propensity scoring is reported as a sensitivity estimate. The primary contrast is full-context policy minus best blanket policy, with a 95% confidence interval.

Secondary contrasts:

- full-context policy minus decline-code-only policy;
- each intervention versus control;
- subgroup treatment-effect heterogeneity;
- economic-value-weighted resolution;
- latency, fraud, dispute, customer-friction and processing-cost guardrails.

## The Recoverability Frontier

For a pre-specified feasible policy class Π, define the empirical Recoverability Frontier as the estimated value of the best policy in Π under the experiment, subject to all commercial and risk guardrails.

The Controllable Failure Gap is:

`Frontier value - current-policy value`

This quantity is always tied to the action set actually tested. It is not a claim that all remaining failures are preventable.

## Causal decline phenotype

A causal decline phenotype is a population-level description of differential response to feasible interventions. It is not an assertion that the unobserved potential outcomes of an individual transaction have been observed.

The experiment asks whether failure populations are more usefully separated by treatment response than by processor/issuer reason labels alone.

## Minimum data contract

At minimum, de-identified payment-intent and attempt IDs, timestamps, amount/currency, merchant market, payment method, route/acquirer/PSP, issuer/BIN geography or safe grouping, card scheme where applicable, stored-credential state, authentication state, token state where available, decline/reason fields, retry linkage, final intent outcome, and randomized action/propensity.

No PAN, CVV, secrets or unnecessary personal data should be transferred.

## Stop rules and safety

The study must define in advance:

- retry-prohibited states;
- per-intent attempt limits;
- maximum customer-friction budget;
- fraud/dispute guardrails;
- latency and processing-cost guardrails;
- intervention-specific kill switches;
- minimum sample thresholds before subgroup claims.

## Claim boundary

A positive synthetic benchmark is evidence that the analysis pipeline can recover seeded heterogeneity. It is not evidence that a merchant has the same heterogeneity or uplift.

A real-world effect is claimable only from the randomized merchant experiment or another defensible identification design. Historical route differences alone are descriptive.
