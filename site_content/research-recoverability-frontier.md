# Decline codes are not failure types

<div class="meta-line"><span>REPORT 004</span><span>RANDOMIZED SYNTHETIC</span><span>PFX-1</span><span>FROZEN HOLDOUT</span></div>

A processor can tell you why an authorization was declined. That does not tell you which intervention would have caused the payment to succeed.

PFX-1 tests a different object: the **recoverability frontier**. For each eligible failed payment, the experiment asks which feasible intervention — route, authentication, credential/token treatment, delayed retry, or no immediate rescue — produces the highest probability of successful payment resolution. The goal is not to maximize retry volume. It is to estimate how much failed demand is actually controllable under a merchant's available action set.

<div class="metric-grid"><div><b>600k</b><span>synthetic attempts</span></div><div><b>39,670</b><span>initial declines</span></div><div><b>20.93%</b><span>holdout recovery · context policy</span></div><div><b>+45.5 bps</b><span>vs best blanket rescue · synthetic</span></div></div>

## The problem

Modern payment stacks already optimize routing, authorization messages, tokenization, authentication and retries. Stripe documents Adaptive Acceptance, which experiments with issuer-specific treatments and selective reattempts. Adyen Uplift combines routing, messaging, authentication, tokenization and automated rescue. Network retry guidance such as Mastercard Merchant Advice Codes and Visa decline categories also constrains whether and when a transaction should be reattempted.

Those systems are valuable. They also leave a measurement question that is useful independently of any one processor:

> **What fraction of failed customer demand is causally recoverable by the interventions the merchant can actually use?**

That is different from a decline rate, a soft-decline rate, or a retry success rate.

## The proposed object: Recoverability Frontier

For a failed payment with context `x`, let `A(x)` be the set of interventions that are legally, contractually and operationally feasible for that payment. Let `V(pi)` be the probability of resolved payment under policy `pi`.

For a pre-specified policy class Π:

`Recoverability Frontier = max V(pi), pi in Π`

and:

`Controllable Failure Gap = Frontier value - current-policy value`

The frontier is always conditional on the tested action set. It does **not** mean every remaining decline is preventable.

## Causal decline phenotype

Traditional decline labels describe a response message. PFX-1 asks whether failure populations can instead be separated by **differential response to intervention**.

A population may be predominantly:

- route-sensitive;
- authentication-sensitive;
- credential/token-sensitive;
- time-sensitive;
- multi-sensitive;
- effectively unrecoverable under the tested action set.

This is a population-level causal classification problem. It is not a claim that every unobserved potential outcome for an individual transaction can be known.

## Why borrow from adaptive-treatment research?

Sequential Multiple Assignment Randomized Trials (SMARTs) were developed to learn adaptive treatment regimes: randomized decisions are made at multiple stages, later interventions can depend on earlier response, and the resulting data support causal comparison of treatment pathways. Payment recovery has the same formal structure: an initial attempt is made; non-response creates a new decision point; the next action should depend on state, prior treatment and eligibility.

PFX-1 is not claiming to invent SMARTs or dynamic treatment regimes. The contribution is applying that logic to **payment authorization and recovery as an experimentally measurable policy problem**.

Background:

- [SMART designs for adaptive interventions — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4167891/)
- [Dynamic Treatment Regimes — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4231831/)
- [Estimation of Optimal Dynamic Treatment Regimes — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4247353/)

Payment-system context:

- [Stripe payments optimization](https://docs.stripe.com/payments/analytics/optimization)
- [Stripe authorization-rate optimization](https://stripe.com/guides/optimizing-authorization-rates)
- [Adyen Uplift](https://docs.adyen.com/uplift)
- [Adyen Optimize](https://www.adyen.com/uplift/optimize)
- [J.P. Morgan authorization retry logic](https://developer.payments.jpmorgan.com/docs/commerce/online-payments/capabilities/online-payments/payment-methods/cards/authorization)

## Experimental design

The benchmark creates a synthetic payment population and an initial authorization process. Only initially declined payment intents enter the rescue experiment.

Each failed intent receives a feasible action set:

1. no immediate rescue / control;
2. alternate route;
3. 3DS step-up where capable;
4. token / credential intervention where available;
5. delayed retry.

A transaction is randomized uniformly among its eligible actions and the randomization propensity is logged. The declined population is split before analysis into **60% discovery and 40% untouched validation**.

Discovery data train action-specific outcome models. The policy is frozen. Validation data are then used once to compare:

- no rescue;
- best blanket rescue;
- decline-code-only policy;
- full-context learned policy;
- synthetic oracle, shown only because the data-generating process is known.

The primary estimator is doubly robust. Inverse-propensity scoring is retained as a sensitivity estimate.

## Frozen synthetic result

The reproducible run uses seed `20260822`.

<div class="table-shell"><div class="table-bar"><span>PFX-1 validation policy value</span><span>15,913 untouched declined intents</span></div><div class="table-scroll"><table><thead><tr><th>Policy</th><th>Estimated recovery</th><th>Interpretation</th></tr></thead><tbody><tr><td>No rescue</td><td>1.37%</td><td>background resolution</td></tr><tr><td>Best blanket rescue</td><td>14.05%</td><td>same general rescue for everyone</td></tr><tr><td>Decline-code-only</td><td>14.42%</td><td>policy sees the processor-style reason label</td></tr><tr><td>Full context</td><td><strong>20.93%</strong></td><td>policy sees issuer/context/eligibility state</td></tr><tr><td>Synthetic oracle</td><td>29.17%</td><td>upper reference available only in simulation</td></tr></tbody></table></div></div>

The frozen full-context policy beat the best blanket rescue by **6.88 percentage points of declined payments** on the untouched randomized holdout.

95% CI: **+5.49 to +8.26 pp**.

At the benchmark's 6.61% initial decline rate, the contrast corresponds to approximately **+45.5 bps overall authorization**, with a synthetic 95% CI of **+36.3 to +54.6 bps**.

The full-context policy also beat the decline-code-only policy by **6.50 pp of failed payments**, corresponding to about **+43.0 bps overall authorization** in the benchmark.

## The stranger result

The simulator deliberately generated a hidden best-response class for failed payments and separately generated noisy processor-style decline labels.

The normalized mutual information between the two was only:

**0.0097**

That number is synthetic, so it is not evidence that real network decline codes are useless. It demonstrates a falsifiable hypothesis:

> **A decline reason may contain much less information about the best recovery action than merchants assume.**

That is now the real-world test.

## Negative controls and ways this can fail

PFX-1 should be rejected as a useful merchant framework if, in randomized production data:

- context-aware policies do not beat a pre-specified blanket policy out of sample;
- decline-code-only policies capture essentially all useful treatment heterogeneity;
- incremental authorization disappears after intent-level resolution, fraud, dispute, cost or customer-friction guardrails;
- policy value is too unstable to replicate across time;
- treatment effects are too small to justify operational complexity.

A synthetic benchmark cannot answer any of those questions.

## Real-merchant protocol

The production version randomizes only **eligible** interventions. Hard declines, network-prohibited retries and other disallowed actions never enter the treatment set. Mastercard Merchant Advice Codes, Visa categories, processor rules and merchant risk constraints must be encoded before assignment.

Primary outcome: successful payment-intent resolution within the agreed horizon.

Primary comparison: frozen full-context policy vs frozen best blanket policy on an untouched randomized validation sample.

Guardrails include fraud, disputes, latency, processing cost, retry count and authentication friction.

[Open the frozen real-merchant protocol on GitHub →](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/experiments/PFX1_PROTOCOL.md)

## Reproduce it

- [Benchmark code](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/experiments/pfx1_recoverability_frontier.py)
- [Frozen result JSON](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/experiments/pfx1_results.json)
- [Real-merchant protocol](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/experiments/PFX1_PROTOCOL.md)

Run:

`python experiments/pfx1_recoverability_frontier.py`

Expected environment: Python with NumPy, pandas and scikit-learn.

## Claim boundary

Everything numerical on this page is **RANDOMIZED SYNTHETIC** unless explicitly described otherwise. The benchmark establishes that the pipeline can recover seeded treatment heterogeneity under randomization. It does not establish merchant uplift.

The next result that matters is a real randomized replication.

> **A decline code tells you what happened. The experiment asks what would have changed it.**
