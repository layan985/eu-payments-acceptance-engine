# Sample Delivery

<div class="meta-line"><span>DAY 5 OUTPUT</span><span>CLIENT-FACING DECISION PACK</span><span>NOT ANOTHER RESEARCH REPORT</span></div>

A buyer should know what arrives at the end of the engagement before paying. The production audit is delivered as a compact decision pack plus reproducible analytical outputs.

## 01 · Cover + engagement perimeter

<div class="delivery-card"><span>PP-ENG-###</span><b>Checkout Leak Audit</b><p>Company / business unit · audit window · markets · payment methods · agreed decision question · data perimeter · evidence classification.</p></div>

The first page states what was analyzed, what was excluded and what the audit is allowed to conclude.

## 02 · Executive decision table

| Priority | Finding | Evidence | Decision | Why | Next action |
|---|---|---|---|---|---|
| P1 | Example state-integrity defect | PRODUCTION CLIENT DATA | FIX | Distorts denominator / reconciliation | Repair identity/state mapping |
| P2 | Example route differential | OBSERVATIONAL | INVESTIGATE | Mix/eligibility not yet resolved | Adjust / stratify before test |
| P3 | Example retry policy | TESTABLE | TEST | Recovery mechanism plausible | Randomized eligible cohort |
| P4 | Example hard-decline loop | INSUFFICIENT ECONOMIC CASE | DO NOT TOUCH | Cost/risk exceeds evidence | No implementation |

The real client table contains the actual retained evidence. This page shows the delivery structure only.

## 03 · Failed-value waterfall

The waterfall separates attempted value into economically meaningful failure states rather than presenting one decline total.

<div class="waterfall-demo"><div><b>100%</b><span>attempted value</span></div><div><b>↓</b><span>eligibility / method availability</span></div><div><b>↓</b><span>authentication loss</span></div><div><b>↓</b><span>issuer / authorization loss</span></div><div><b>↓</b><span>post-auth / state loss</span></div><div><b>↓</b><span>refund / reconciliation leakage</span></div></div>

Every production value shown in a real delivery states its denominator, period and evidence class.

## 04 · Authorization matrix

The matrix shows authorization and failed value across the dimensions that can plausibly change mechanism: market, payment method, route/provider, issuer attributes where lawful, device/channel and authentication state.

A raw gap is explicitly marked **descriptive** until selection and eligibility have been handled.

## 05 · 3DS + authentication diagnostic

The delivery separates:

`eligible → challenged → completed authentication → attempted authorization → authorized → captured`

It checks exemptions/flows where available and avoids treating 3DS/non-3DS populations as randomized groups.

## 06 · Retry diagnostic

The retry section distinguishes:

**attempt authorization · payment-intent resolution · customer resolution · economic-value resolution**

Sequence cards show which decline classes are being retried, how quickly, whether recovery is real, and which loops should be blocked.

## 07 · Experiment card

<div class="experiment-card"><small>EXP-###</small><h3>Intervention to test</h3><p><b>Population:</b> explicitly eligible traffic</p><p><b>Assignment:</b> randomized / otherwise justified</p><p><b>Primary outcome:</b> pre-specified</p><p><b>Guardrails:</b> fraud · dispute · latency · cost · operational failure</p><p><b>Decision rule:</b> ship / do not ship / extend test</p><p><b>Contamination checks:</b> route, retry, issuer, market and method mix</p></div>

No experiment card is included merely to make the deliverable look sophisticated. It appears only where an intervention is actually testable.

## 08 · Limitations register

| Limitation | Why it matters | Effect on claim | Resolution |
|---|---|---|---|
| Missing eligibility event | Route/method population uncertain | blocks causal route claim | instrument eligibility |
| Aggregated retry data | sequence contamination hidden | intent recovery uncertain | provide attempt IDs |
| No fraud/dispute join | economic effect incomplete | no net-value claim | join guardrails |
| Short post-window | persistence unknown | annualization blocked | extend measurement window |

## 09 · Technical appendix

The appendix contains metric definitions, transformations, query/code references, QA checks, object/state mapping, evidence provenance and reproducibility instructions needed for the merchant team to interrogate the work.

## 10 · Delivery state

Every recommendation ends in one of four states:

<div class="decision-cards"><div><span>FIX</span><b>Known defect</b><p>Evidence is sufficient to repair the measurement/operational problem.</p></div><div><span>INVESTIGATE</span><b>Signal, not conclusion</b><p>Material pattern exists but mechanism/identification remains unresolved.</p></div><div><span>TEST</span><b>Intervention candidate</b><p>A controlled decision can be run with explicit outcome and guardrails.</p></div><div><span>DO NOT TOUCH</span><b>No defensible change</b><p>The evidence does not support intervention or risk/economics fail.</p></div></div>

[View full scope](/services) · [Commercial FAQ](/faq) · [Request an audit](/contact)