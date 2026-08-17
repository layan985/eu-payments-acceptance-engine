# Case File 001 — Zalando Checkout Investigation

<div class="meta-line"><span>INDEPENDENT PUBLIC-SOURCE INVESTIGATION</span><span>NOT A CLIENT</span><span>OFFICIAL / FIRST-PARTY SOURCES</span><span>SYNTHETIC RECONSTRUCTION</span></div>

<div class="callout danger"><b>INDEPENDENT PUBLIC-SOURCE INVESTIGATION · NOT A CLIENT.</b><p>Zalando has not commissioned, reviewed or endorsed this work. No production data, internal routing, fraud rules, conversion rates or commercial contracts were accessed.</p></div>

## Executive finding

The public record exposes enough operational structure to define a serious payment investigation without inventing inside access. The first diligence problem is upstream of “which PSP wins?”: order-dependent method eligibility, country-local payment paths, invoice allocation, financial approval, payout currency and post-payment state can all change the denominator before route performance is interpreted.

## Public facts inspected · 16 August 2026

| Surface | First-party observation | Source | Boundary |
|---|---|---|---|
| Payments scale | Zalando Payments describes infrastructure serving 60m+ active customers and thousands of partners | [Zalando Payments](https://jobs.zalando.com/en/blog/future-of-embedded-payments) | scale context, not performance |
| Dynamic eligibility | payment methods are reviewed for each order and a preferred method may not be offered | [Zalando Germany FAQ](https://www.zalando.de/faq/Payments/why-is-my-preferred-payment-method-not-available.html) | scoring/rules remain private |
| Cash on Delivery | ZSS documentation describes CoD in CZ, IT, PL and ES; Poland onboarding requires CoD | [Zalando Partner](https://partner.zalando.com/university/article/cash-on-delivery-with-zss) | operational availability, not conversion |
| Invoice reference | invoice payment requires the Zalando order number as payment reference | [Zalando Partner](https://partner.zalando.com/university/article/order-quality-assurance-requirements-explained) | payment-allocation control surface |
| Financial approval | zDirect order documentation exposes an initial financial-approval state before approved | [Zalando Partner](https://partner.zalando.com/university/article/manage-orders-tool-on-zdirect) | no failure/latency rate disclosed |
| Payout currency | partner setup distinguishes local-currency and euro payout modes | [Zalando Partner](https://partner.zalando.com/university/article/zdirect-onboarding-account-setup) | settlement control, not fee claim |

## Forensic priority map

<div class="bar-chart" data-title="Public evidence → testable failure surfaces · analyst priority, not Zalando data">
<div><b>Dynamic method eligibility</b><i style="--v:100%"></i><strong>5/5</strong></div>
<div><b>Invoice reference integrity</b><i style="--v:100%"></i><strong>5/5</strong></div>
<div><b>Country-local CoD</b><i style="--v:80%"></i><strong>4/5</strong></div>
<div><b>Financial approval state</b><i style="--v:80%"></i><strong>4/5</strong></div>
<div><b>Multi-currency payout</b><i style="--v:60%"></i><strong>3/5</strong></div>
<div><b>Invoice / BNPL state</b><i style="--v:80%"></i><strong>4/5</strong></div>
</div>

The scores only order the investigation. They are not Zalando performance measurements.

## Checkout observation

A payment-method page is not the denominator. If method availability is evaluated per order, a production audit must preserve the sequence:

<div class="state-line"><span>ELIGIBLE</span><b>→</b><span>DISPLAYED</span><b>→</b><span>SELECTED</span><b>→</b><span>ATTEMPTED</span><b>→</b><span>AUTHORIZED</span><b>→</b><span>CAPTURED</span></div>

Beginning at `attempted` and assuming every method or route was equally available can create a false performance story before any processor is compared.

## Hypotheses designed to be killed

### H1 · Eligibility

**Hypothesis:** part of apparent method-level checkout loss occurs before authorization because eligibility changes what can be shown.

**Production test:** intent-level eligible → displayed → selected → attempted → authorized waterfall by market and method.

**Falsifier:** availability is stable and has no material relationship with abandonment or downstream mix.

### H2 · Invoice allocation

**Hypothesis:** reference integrity creates payment exceptions invisible to card-authorization dashboards.

**Production test:** join expected reference, received transfer reference, allocation state, reminder/contact outcomes.

**Falsifier:** misallocation is negligible and produces no meaningful downstream exception load.

### H3 · Country-local methods

**Hypothesis:** CoD creates a different operational/economic state path and should not be collapsed into one checkout-failure metric.

**Production test:** map order/payment/fulfilment/return states and exception distributions by method and market.

**Falsifier:** state/error distributions are effectively identical across methods.

### H4 · Financial approval

**Hypothesis:** financial approval is a distinct latency/failure gate.

**Production test:** measure initial → approved latency, failure, cancellation and downstream fulfilment impact.

**Falsifier:** no meaningful failure or latency is attributable to the gate.

### H5 · Payout currency

**Hypothesis:** local-vs-euro payout mode creates an FX/reconciliation control surface.

**Production test:** reconcile transaction currency, payout currency, bank account, conversion and payout IDs.

**Falsifier:** no meaningful reconciliation/FX exception is associated with payout mode.

## Synthetic reconstruction — without fake Zalando numbers

Public documentation does not expose production transaction performance. The reconstruction therefore refuses to estimate it. It specifies the production table contract instead:

| Object | Minimum fields |
|---|---|
| payment_intent | intent_id · order_id · market · customer pseudonym · basket value · created_at |
| eligibility | intent_id · method · eligible_flag · display_flag · rule_version |
| attempt | attempt_id · intent_id · method · route · 3DS state · issuer response · authorized |
| order / financial state | order_id · financial_approval_state · fulfilment_state · cancellation |
| invoice / settlement | expected reference · received reference · allocation · transaction currency · payout currency · payout_id · fee · FX |
| event ledger | event_id · provider object · payment object · state · sequence · idempotency result |

## Decision memo

**FIX:** payment-object identity, method-eligibility denominator and state reconciliation if unstable.

**INVESTIGATE:** country/method surfaces, invoice allocation, financial approval and payout-currency exceptions.

**TEST:** only a narrow route/authentication intervention after eligibility and state identity are stable, with fraud/dispute/latency/cost guardrails.

**DO NOT CLAIM:** no Zalando authorization rate, conversion rate, uplift, revenue recovery, fraud result or internal routing architecture is asserted from public evidence.

## What would falsify the overall thesis?

If production data showed stable method eligibility, negligible invoice/CoD/state exceptions, no meaningful financial-approval failure or latency, and no payout/reconciliation differences, the case for prioritizing these surfaces ahead of processor routing would weaken materially.

## Sources + technical record

[Public forensics portfolio](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/forensics/README.md) · [one-command reproduction](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/reproduce.py)

## Limitations

First-party documentation is not live checkout instrumentation. Public ecosystem figures can refer to different business scopes. No internal PSP list, issuer mix, risk score, authorization rate, fraud rate, abandonment rate, route rule, fee schedule or commercial contract is inferred.