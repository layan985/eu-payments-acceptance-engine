# Checkout Leak Audit · €1,950

<div class="meta-line"><span>FOUNDING PRODUCTION RATE</span><span>50% UPFRONT</span><span>FIXED SCOPE</span><span>LIMITED EARLY CASE CAPACITY</span></div>

<div class="price-card"><b>€1,950</b><span>€975 upfront · €975 on delivery</span><small>founding production rate · limited early-case allocation</small></div>

This is **founding production pricing**, not the intended long-run price for the service. It is deliberately below the eventual specialist-practice rate while the first additional permissioned production cases are being built. The scope is fixed after the decision question and data perimeter are confirmed.

A Head of Payments should be able to decide whether this is relevant without booking a discovery call.

## Inputs

| Input | Minimum useful fields | Default security boundary |
|---|---|---|
| payment attempts / intents | stable IDs, timestamp, amount, market, method, route, result | no PAN/CVV/card-track |
| authentication | 3DS state, exemption/flow where available, result | no authentication secrets |
| declines | normalized reason/code, soft/hard classification | sensitive provider/issuer text minimized |
| lifecycle | authorization, capture, refund, reversal/dispute states + timestamps | non-sensitive provider object IDs |
| economics / reconciliation | provider fees, payout/settlement identifiers where in scope | only fields needed for agreed decision |

Default intake excludes full PAN, CVV/CVC, card-track data, authentication secrets, private keys, passwords and unnecessary directly identifying customer data. Preferred identifiers are merchant-generated non-sensitive IDs, provider object IDs and pseudonymized references.

**Security standard:** [Security & Confidentiality](/security)

## What the engagement actually feels like

| Day | Checkout work | Client provides / confirms | Gate before moving on |
|---|---|---|---|
| **Day 0 · Scope** | lock decision question, objects, markets, denominator, exclusions, permitted-use and data perimeter | decision owner, scope, minimum field inventory, access/transfer expectations | written measurement contract + approved perimeter |
| **Day 1 · QA** | identifier tests, duplicates, missingness, timestamp/state checks, denominator reconstruction | clarifications on field semantics and known data quirks | canonical object/state map is defensible |
| **Day 2–3 · Diagnostics** | failed-value decomposition, decline/3DS/retry cuts, route screens, lifecycle/reconciliation exceptions | rapid clarification only where a field or state is ambiguous | every material finding carries an evidence class and limitation |
| **Day 4 · Decision review** | rank findings, kill weak hypotheses, define FIX / INVESTIGATE / TEST / DO NOT TOUCH | decision-maker review of operational constraints and feasible interventions | recommendations are bounded by evidence and implementation reality |
| **Day 5 · Delivery** | deliver 8–15 page decision pack + reproducible analytical outputs + readout | acceptance / questions / implementation ownership | proof ledger, limitations register and action register closed |

If the Day 1 QA shows the data cannot support the intended decision, that is surfaced immediately rather than hidden behind a polished report.

## Analysis stages

### 01 · Perimeter + measurement contract

Lock the decision question, payment objects, eligibility rule, denominator, time window and exclusions before analysis starts.

### 02 · Data QA + state integrity

Check identifiers, duplicates, missing states, impossible transitions, timestamp/order consistency and reconciliation perimeter. A broken event model is fixed before performance is optimized.

### 03 · Loss decomposition

Authorization and failed-value maps by market, method, device, route, issuer/BIN attributes where lawful, authentication state and decline class.

### 04 · Retry + authentication

Separate attempt, intent and economic denominators; isolate retry contamination and selected authentication populations.

### 05 · Routing + economics

Screen route differences; refuse causal wording until assignment/identification is defensible; join fraud, dispute, latency and processing-cost guardrails where available.

### 06 · Decision memo

Every issue ends in one state: **FIX · INVESTIGATE · TEST · DO NOT TOUCH**, with evidence, limitation and next action.

## Exact deliverables

### Measurement + QA

- Payment Data QA report
- metric dictionary
- object/state map
- provenance/transformation notes
- limitations register

### Payment forensics

- failed-value waterfall
- authorization map
- decline forensics
- 3DS diagnostic
- retry analysis
- routing screen where identifiable
- payment-state / reconciliation exceptions

### Decision layer

- experiment designs
- primary outcome + guardrails
- executive decision memo
- technical appendix
- FIX / INVESTIGATE / TEST / DO NOT TOUCH register

## Sample output preview

<div class="decision-cards">
<div><span>INVESTIGATE</span><b>Observed route gap</b><strong>372 bps</strong><p>Do not annualize. Check mix, eligibility and assignment first.</p></div>
<div><span>TEST</span><b>Identified intervention</b><strong>pre-specified</strong><p>Randomize eligible traffic; monitor authorization + fraud + dispute + latency + cost.</p></div>
<div><span>DO NOT TOUCH</span><b>Hard decline repeat</b><strong>blocked</strong><p>No blind recovery loop for hard/sensitive failure classes.</p></div>
</div>

[See the full sample Day 5 delivery →](/sample-delivery)

## Founding-rate boundary

The €1,950 price is reserved for a limited number of early production engagements while Checkout builds additional permissioned third-party proof. The service is not being positioned as permanent low-cost freelance work. Once the founding allocation is filled, pricing is expected to move upward with the evidence base and delivery history.

No urgency claim is fabricated: the site will not display a fake countdown or fake remaining-slot number.

## What happens during the engagement

**Start:** written scope + permitted-use/data perimeter.  
**Analysis:** work proceeds against the locked measurement contract; missing evidence is marked unresolved rather than guessed.  
**Delivery:** one decision pack plus reproducible analytical outputs.  
**Close:** agreed retention/deletion expectations are followed. Any public case record requires separate explicit permission.

## What Checkout refuses to claim

- an observed processor difference is not called causal uplift;
- gross authorization movement is not called realized revenue;
- sandbox execution is not provider, scheme or PCI certification;
- fraud reduction is not inferred from approval data;
- no client identity, production metric or result is published without explicit permission.

## Suitable

Multi-market ecommerce, travel, subscription and digital businesses with stable payment identifiers and enough history to inspect acceptance and state behavior.

## Not suitable

Generic CRO design, PCI certification, processor procurement without data, fraud-model outsourcing, or anyone buying a guaranteed “X% revenue lift.”

## Request the audit

Use the structured [Request Audit form](/contact). The public form collects commercial scoping metadata only; production payment data is transferred separately after scope and security expectations are agreed.

[Commercial FAQ](/faq) · [Security & Confidentiality](/security)