# Recoverability Scan · €950

<div class="meta-line"><span>48-HOUR ENTRY PRODUCT</span><span>100% UPFRONT</span><span>ANONYMIZED EXPORT</span><span>PFX-1 SCREENING</span></div>

<div class="price-card"><b>€950</b><span>one anonymized payment export · fixed scope · 48-hour decision</span><small>credited in full if upgraded to the €1,950 Checkout Leak Audit</small></div>

The first question is not “how do we optimize everything?” It is narrower:

> **Is there enough structured recoverability in your failed demand to justify changing anything?**

The Recoverability Scan is the commercial entry point to Checkout's PFX-1 research. It screens historical payment data for where failed value concentrates, which rescue actions appear operationally testable, and whether a randomized production experiment is economically worth running.

It **does not** turn observational history into a causal uplift claim. If the data cannot support a useful experiment, the answer is allowed to be “do not run one.”

## What to send

One de-identified attempt / intent export covering a useful recent period. Minimum useful fields are:

| Object | Useful fields |
|---|---|
| payment identity | stable attempt and payment-intent/order IDs |
| transaction | timestamp, amount, currency, market, method |
| processing | PSP/acquirer/route, result, normalized decline code/reason |
| authentication | 3DS eligibility/state/result where available |
| retry | retry sequence or parent-intent linkage |
| credential | token / stored-credential state where lawfully available |

No PAN, CVV/CVC, card-track data, authentication secrets, passwords or unnecessary customer-identifying fields.

## What comes back in 48 hours

### 01 · Failed-value map

Where failed economic value actually concentrates by issuer/market, route, payment method, 3DS state, credential state and retry sequence where those fields exist.

### 02 · Recoverability screen

Candidate populations that look potentially route-sensitive, authentication-sensitive, credential-sensitive, time-sensitive or unlikely to justify intervention. These are **hypothesis classes**, not causal labels.

### 03 · Action-set audit

Which interventions the current stack can realistically test: alternate route, 3DS treatment, token/credential treatment, compliant delayed retry, or control.

### 04 · Experiment viability

Whether the merchant has enough eligible failed intents, treatment optionality and observable guardrails to run PFX-1 credibly.

### 05 · Decision

One of four outputs:

**RUN PFX-1 · RUN A NARROWER TEST · FIX MEASUREMENT FIRST · DO NOT TEST YET**

You get the reasoning, the relevant segments, the proposed primary outcome and the guardrails required before any causal claim.

## What this is not

- no guaranteed authorization lift;
- no “AI recovered X revenue” claim from historical correlations;
- no blind retry recommendation;
- no processor migration pitch;
- no requirement to publish the merchant's identity or data.

## If the scan finds something real

The next step can be a bounded randomized PFX-1 replication. Eligible failures are assigned only among merchant-approved, scheme-compliant actions. The policy is learned on discovery traffic, frozen, and evaluated once on untouched validation traffic with fraud, dispute, cost, latency and customer-friction guardrails.

[Read the public PFX-1 experiment →](/research/recoverability-frontier)

## Upgrade path

If broader payment-state, routing, 3DS, retry, reconciliation or lifecycle work is needed, the €950 is credited **in full** against the **€1,950 Checkout Leak Audit**.

The full audit retains the existing five-day production scope and 50% upfront structure.

## Request the scan

Use the [structured intake form](/contact). Select the Checkout Leak Audit inquiry type and put **Recoverability Scan** in the decision field. Do not upload production payment data through the public form; secure transfer is agreed after scope.

[Security & Confidentiality](/security) · [PFX-1 Research](/research/recoverability-frontier) · [Sample Delivery](/sample-delivery)