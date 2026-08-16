# CASE FILE 002 — Booking.com travel-payment architecture

<div class="meta-line"><span>INDEPENDENT PUBLIC-SOURCE ANALYSIS</span><span>NOT A CLIENT</span><span>PUBLIC SOURCES + SYNTHETIC RECONSTRUCTION</span><span>TRAVEL / MULTI-EVENT PAYMENT ARCHITECTURE</span></div>

This case file asks a narrower question than “is Booking.com checkout good?”:

> **Where would I instrument a travel-booking payment system so that payment failures, schedule mismatches, cancellations, refunds and payout exceptions can be distinguished from each other before somebody calls all of them conversion loss?**

Booking.com has not commissioned, reviewed or endorsed this analysis. No production Booking.com transaction data, private provider contracts, internal fraud logic, conversion rates or payment-routing data are used.

## 01 — Why this is structurally different from Case File 001

The Zalando investigation is primarily a multi-market commerce / method-eligibility / returns / reconciliation problem. Booking.com’s public Demand API exposes a different structure: a booking can move through **preview → create → post-booking management → cancellation/refund → property payout/reconciliation**, while payment behaviour depends on supplier policy, timing, schedule and collection model.

That changes the object being measured. One booking may have more than one payment event, a guarantee can exist without an immediate charge, a later cancellation can change the economic state, and a property payout can be separated from traveller collection.

## 02 — Public-source register

| # | Public fact used in the investigation | Source | Evidence class |
|---|---|---|---|
| 01 | `/orders/preview` validates the booking, final price, payment options and creates an order token. | Booking.com Demand API — Create orders | OFFICIAL SOURCE |
| 02 | The order token expires after 15 minutes. | Booking.com Demand API — Create orders / FAQ | OFFICIAL SOURCE |
| 03 | `/orders/create` must use the selected payment configuration and the preview token. | Booking.com Demand API — Create orders | OFFICIAL SOURCE |
| 04 | `/orders/preview` is described as the authoritative source for checkout payment behaviour. | Booking.com Payments — Get started | OFFICIAL SOURCE |
| 05 | Payment behaviour is dynamic and should not be hardcoded. | Booking.com Payments — Get started | OFFICIAL SOURCE |
| 06 | A booking may contain multiple charges, split payments, deposits or guarantees. | Booking.com Payments — Get started | OFFICIAL SOURCE |
| 07 | Payment timing includes pay online now, pay online later and pay at service/property models. | Booking.com Demand API payment documentation | OFFICIAL SOURCE |
| 08 | Payment methods can include cards, VCCs and pay-at-service flows depending on context. | Booking.com — Payment methods | OFFICIAL SOURCE |
| 09 | Available payment methods depend on supplier policy, timing, partner configuration and regulatory requirements. | Booking.com — Payment methods | OFFICIAL SOURCE |
| 10 | Booking.com-collects flow charges the traveller and then pays the property. | Booking.com — Booking.com collects payment | OFFICIAL SOURCE |
| 11 | Partner-collects can use VCC funding and must still follow preview timing/method requirements. | Booking.com — Partner collects / VCC flow | OFFICIAL SOURCE |
| 12 | Payments by Booking supports bank-transfer, VCC and Stripe payout methods for partners. | Booking.com Connectivity — Understanding payouts | OFFICIAL SOURCE |
| 13 | `/orders/details` supports reporting and reconciliation workflows across order data. | Booking.com — Orders management | OFFICIAL SOURCE |
| 14 | Pay-at-property can require a card guarantee even though the property collects payment later. | Booking.com — Regular travellers / pay at property | OFFICIAL SOURCE |
| 15 | Preview/create mismatches can produce errors such as missing method, unexpected timing or unsupported card ID. | Booking.com accommodation payments guide | OFFICIAL SOURCE |

### Source links

1. https://developers.booking.com/demand/docs/orders-api/order-preview-create
2. https://developers.booking.com/demand/docs/orders-api/orders-faqs
3. https://developers.booking.com/demand/docs/orders-api/overview
4. https://developers.booking.com/demand/docs/payments/how-to
5. https://developers.booking.com/demand/docs/payments/payments-methods
6. https://developers.booking.com/demand/docs/payments/models/booking-collects
7. https://developers.booking.com/demand/docs/payments/models/partner-collects
8. https://developers.booking.com/connectivity/docs/payments-by-booking-onboarding-api/understanding-payouts
9. https://developers.booking.com/demand/docs/payments/models/pay-at-property
10. https://developers.booking.com/demand/docs/payments/how-to-accommodation-payments

## 03 — Concrete observations

### Observation 01 — Preview/create consistency is a payment control

The payment object cannot be treated as a static checkout form. Booking.com’s public implementation guidance makes preview authoritative, and the subsequent create request must remain consistent with the preview response.

**Diagnostic implication:** instrument both preview and create and preserve a joinable `order_token` / request lineage so mismatch failures can be separated from issuer declines.

### Observation 02 — Token expiry is a measurable failure surface

The preview token expires after 15 minutes.

**Diagnostic implication:** payment failures need an `elapsed_preview_to_create_seconds` variable. A stale-token failure is not a card-acceptance problem.

### Observation 03 — One booking can have multiple economic events

The documentation explicitly warns integrations not to assume one payment event per order. Deposits, guarantees, later payments and split schedules can coexist.

**Diagnostic implication:** “authorization rate per booking” is insufficient. The event model requires booking, payment obligation, payment attempt, charge, refund and payout identifiers.

### Observation 04 — Payment timing and payment method are jointly constrained

A method that exists for one timing may not exist for another.

**Diagnostic implication:** method performance must be conditional on eligible timing/schedule. Otherwise mix changes can look like method-quality changes.

### Observation 05 — Pay at property is not “no payment state”

A booking may be collected at the property while still requiring a card guarantee.

**Diagnostic implication:** guarantee success, traveller charge success and property collection are different states and should not be collapsed.

### Observation 06 — Traveller collection and property payout can be decoupled

Booking.com-collects charges the traveller and pays the property later. Payments by Booking exposes multiple payout rails.

**Diagnostic implication:** traveller-payment success does not establish partner-settlement completion.

### Observation 07 — VCC introduces a second card lifecycle

A VCC can be created/funded for a booking and later charged by the property.

**Diagnostic implication:** there can be a successful traveller payment and a later VCC activation/charge exception. These belong to different operational owners.

### Observation 08 — Cancellation and refund are economic-state transitions

Post-booking management and cancellation are first-class API operations.

**Diagnostic implication:** gross booked value should not be annualized into realized payment value without cancellation/refund state.

### Observation 09 — Reporting/reconciliation is part of the API model

Booking.com explicitly positions order retrieval for reporting and reconciliation.

**Diagnostic implication:** a mature diagnostic must reconcile order state with payment event state rather than treating payment analytics as a front-end-only problem.

### Observation 10 — Error taxonomies should begin before the PSP

Preview mismatch, invalid token, unsupported method/timing and occupancy/price changes can fail before an issuer authorization exists.

**Diagnostic implication:** the denominator for “issuer decline rate” must exclude integration-state failures.

## 04 — Five testable hypotheses

| Hypothesis | Why it is plausible | Required production evidence | What would falsify it? |
|---|---|---|---|
| H1 — preview/create drift creates avoidable booking failure | Payment configuration is dynamic and preview is authoritative. | preview payload hash, selected timing/method, create payload, elapsed time, response code | mismatch failures are negligible after controlling for expired tokens and product changes |
| H2 — stale order tokens create a long-tail abandonment surface | Tokens expire after 15 minutes. | preview timestamp, create timestamp, token-expiry response, customer retry | expired-token rate is near zero and retries recover almost all affected bookings |
| H3 — pay-at-property guarantee failures are being mixed with payment declines | Guarantee and collection are different economic events. | collection model, guarantee attempt, charge attempt, property collection state | existing metrics already separate guarantee failure from charge failure with stable denominators |
| H4 — cancellation/refund state materially changes apparent approved value | Travel has a long post-booking lifecycle. | cancellation state, refund amount/time, retained value | cancellation/refund-adjusted value is statistically indistinguishable from gross approved value for the decision window |
| H5 — property payout exceptions survive after successful traveller collection | Collection and payout can use separate rails. | traveller charge, payout method, VCC/BT/Stripe payout state, exception code | successful traveller collection almost always reaches completed partner payout within the agreed SLA |

## 05 — Measurement contract

A production diagnostic should not start until these objects are separable:

| Object | Minimum identifier / fields | Why |
|---|---|---|
| booking | order ID, product, supplier/property, market, currency | commercial unit |
| preview | preview/request ID, order token hash, timestamp, eligible timing/method/schedule | eligibility and configuration |
| create | request ID, selected timing/method, create timestamp, response/error | booking completion |
| payment obligation | due date, amount, currency, collection model | scheduled economic obligation |
| payment attempt | attempt ID, amount, method, authentication, processor result | acceptance denominator |
| cancellation/refund | amount, reason, timestamp, final state | retained economic value |
| guarantee / VCC | guarantee status, activation/charge state where applicable | pay-at-property / partner collection control |
| payout | payout rail, amount, currency, state, exception | property settlement |
| reconciliation | expected amount/state, observed amount/state, match status | ledger integrity |

### Required denominator set

1. eligible booking previews;
2. create attempts;
3. successfully created bookings;
4. payment obligations due;
5. payment attempts;
6. unique bookings economically resolved;
7. retained booked value after cancellation/refund;
8. partner payouts completed.

## 06 — Synthetic reconstruction

<div class="callout danger"><strong>Important:</strong> the reconstruction below is synthetic. It is designed from public architecture; it is not an estimate of Booking.com performance.</div>

A separate 12,000-order synthetic travel cohort was constructed with:

- pay-online-now / pay-online-later / pay-at-property timing;
- card / wallet / VCC-style collection paths;
- EUR / GBP / USD / PLN currencies;
- multiple payment-event counts;
- preview/create mismatch flags;
- payment refusals;
- cancellation + refund-due states;
- VCC activation/charge state;
- payout/reconciliation exceptions.

Its purpose is not to say “Booking.com has X% failure.” Its purpose is to prove the analysis can represent travel-payment failure surfaces without collapsing them into a single checkout conversion KPI.

## 07 — Visual diagnostic

<div class="decision-cards">
<div><span>CONFIGURATION</span><b>Preview → Create</b><strong>join before blame</strong><p>Expired token, pricing/policy drift and unsupported timing/method belong upstream of issuer acceptance.</p></div>
<div><span>ECONOMIC STATE</span><b>Booking → Refund</b><strong>retain the timeline</strong><p>Booked value, charged value and retained value are different objects.</p></div>
<div><span>SETTLEMENT</span><b>Traveller → Property</b><strong>two-sided control</strong><p>Successful traveller collection does not prove successful partner payout.</p></div>
</div>

## 08 — Experiment plan

### Experiment A — Preview/create consistency intervention

**Treatment:** strict client-side configuration binding to preview response plus forced refresh when token age crosses a prespecified threshold.

**Primary outcome:** booking-create success among eligible previews.

**Secondary outcomes:** stale-token error, payment-method mismatch error, time-to-create, customer retry, downstream payment authorization.

**Guardrail:** do not count price/product availability changes as payment-treatment wins.

### Experiment B — Payment-recovery policy

For retryable payment failures only, randomize recovery treatment at the **booking/payment-obligation** level rather than the raw attempt level.

Primary outcome: economically resolved booking obligation.

Guardrails: duplicate charges, cancellation, refund rate, support contacts and fraud.

## 09 — Management decision memo

### FIX

- Missing join keys between preview, create, payment attempt, refund and payout.
- Any KPI that calls preview/create configuration errors “issuer declines.”
- Any reconciliation process that cannot tie a traveller charge to the eventual economic booking and payout state.

### INVESTIGATE

- Token-age failure distribution.
- Guarantee versus charge failure for pay-at-property bookings.
- Cancellation/refund adjustment to approved value.
- Payout exceptions by rail and market.

### TEST

- Preview/create binding intervention.
- Recovery policy only after retry eligibility is defined at the economic obligation level.

### DO NOT TOUCH

- Do not route more traffic to a processor solely because a raw approval table is higher.
- Do not remove authentication because a selected no-auth group converts better.
- Do not annualize a gross booking-approval delta before refund/cancellation/payout state is reconciled.

## 10 — What would falsify this investigation?

The case becomes materially weaker if production evidence shows:

1. preview/create mismatch and token expiry contribute essentially no failure;
2. guarantee, traveller charge, cancellation/refund and payout are already represented as distinct canonical states;
3. reconciliation exceptions are negligible and quickly resolved;
4. payment timing/method eligibility does not explain any meaningful segment movement;
5. post-booking economics do not change prioritization relative to front-door authorization.

That outcome would be useful. The point of Checkout is not to manufacture a routing recommendation.

## 11 — Claim boundary

**Supported:** Booking.com’s public API documentation exposes dynamic payment configuration, authoritative order preview, multiple payment timings/events, multiple collection models, post-booking operations and payout/reconciliation surfaces.

**Not supported:** Booking.com production authorization, conversion, fraud, refund, payout-exception or revenue-impact figures.

**Synthetic reconstruction:** explicitly separate and used only to demonstrate measurement and diagnostic design.
