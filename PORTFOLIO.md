# Checkout — Payments Evidence Portfolio

This portfolio is designed for one buyer question:

> **Can you show me, with evidence, what you can actually diagnose and execute in a checkout stack?**

The answer is organized as a chain of proof rather than a list of skills.

**Market evidence → merchant-level diagnosis → causal testing → provider execution → lifecycle integrity → reconciliation.**

Every material claim is labeled. Synthetic data is not presented as client data. Provider test execution is not presented as production processing. Official market statistics are kept separate from merchant-level inference.

---

## Proof map

| Proof object | What exists | Evidence class | What it demonstrates |
| --- | --- | --- | --- |
| Euro-area payments benchmark | H2 2025 ECB dataset, source URLs, limitations | `OFFICIAL SOURCE` | market research, provenance, data extraction |
| EEA fraud benchmark | 2024 EBA/ECB fraud dataset | `OFFICIAL SOURCE` | fraud/SCA context and risk framing |
| Public-market analysis | reproducible calculations from the two datasets | `REAL PUBLIC DATA` + derived | turning official data into decision-relevant diagnostics |
| Merchant acceptance environment | 300,000 payment attempts across 10 countries, 3 PSPs, 4 methods, 2 devices | `SYNTHETIC` | segmentation, decline analytics, SQL, funnel diagnostics |
| Germany route diagnostic | PSP_A 93.03% vs PSP_B 89.31%, raw 372 bp gap | `SYNTHETIC` | identifying an investigation target without overstating causality |
| Routing experiment | N=40,000 randomized treatment-control design, ~248 bp difference, ~191–305 bp 95% CI | `RANDOMIZED SYNTHETIC` | experiment design, uncertainty, causal discipline |
| Stripe success / decline / 3DS | retained test executions | `PROVIDER TEST` | real API-state handling in Stripe test mode |
| Auth → capture → refund | retained execution | `PROVIDER TEST` | payment lifecycle operations |
| Signed webhook verification | retained execution | `PROVIDER TEST` | signature verification and event integrity |
| Persistent event ledger | SQLite duplicate-event claiming and replay controls | `CONTRACT TESTED` | idempotency and operational safety |
| Reconciliation engine | seeded settlement matches and explicit exceptions | `SYNTHETIC` / executable | post-checkout financial operations |
| Production merchant uplift | none claimed | `PENDING VALIDATION` | claim discipline |

---

# Case file 01 — The European payments surface

## Question

What does the current European payments environment imply about the checkout problems worth measuring?

## Data

Two machine-readable public datasets are retained in the repository:

- `data/public/eu_payments_market_benchmark_h2_2025.csv`
- `data/public/eu_payments_fraud_benchmark_2024.csv`

The market table records H2 2025 euro-area payments statistics published by the ECB. The fraud table records 2024 EEA aggregates published jointly by the EBA and ECB.

## Selected official observations

**ECB H2 2025**

- 83.5 billion euro-area non-cash payment transactions.
- €117.8 trillion total non-cash payment value.
- Cards represented 57% of non-cash payment count.
- 47.8 billion card transactions worth about €1.8 trillion.
- Remote payments represented 19% of card count but 30% of card value.
- 32.9 billion contactless card payments.
- 25.7 million POS terminals, 93% contactless-enabled.

**EBA/ECB 2024 fraud context**

- payment fraud remained around 0.002% of transaction value across the EEA;
- reported fraud value rose from €3.5bn in 2023 to €4.2bn in 2024;
- card fraud was reported as 17x higher when the recipient was outside the EEA;
- SCA-authenticated transactions were generally less susceptible to fraud, particularly for card payments.

## What I calculate

`public_market_analysis.py` derives several deliberately modest indicators from the rounded official aggregates:

- approximately **9.08bn remote** and **38.72bn non-remote** card transactions in H2 2025;
- an approximate **€59.46 remote average ticket** versus **€32.54 non-remote**, based on rounded aggregate count/value shares;
- a remote/non-remote average-ticket ratio of about **1.83×**;
- contactless transactions representing about **68.8% of total card count**;
- reported aggregate fraud value increasing about **20%** from 2023 to 2024.

These are market-level calculations. They do **not** identify a merchant's authorization problem. Their purpose is to establish what deserves attention: remote checkout economics, authentication, fraud guardrails, routing, device/payment-method mix, and lifecycle integrity.

## Buyer relevance

The work product is not “I read an ECB press release.” It is a provenance-controlled benchmark that can sit beside a merchant's own metrics. In a client engagement I would map the merchant's authorization, 3DS, decline, retry, route and lifecycle metrics against the relevant market context while keeping external aggregates out of merchant causal claims.

---

# Case file 02 — Authorization leakage without fake uplift claims

## Question

A merchant sees different authorization rates across routes. Is that evidence to reroute traffic?

## Environment

The repository includes a reproducible 300,000-attempt merchant environment spanning:

- 10 European markets;
- PSP_A / PSP_B / PSP_C;
- Visa, Mastercard, PayPal and SEPA debit;
- mobile and desktop;
- 3DS and non-3DS paths;
- soft and hard decline categories.

## Finding

The seeded environment reproduces:

- **93.10%** overall authorization;
- **93.03%** Germany / PSP_A;
- **89.31%** Germany / PSP_B;
- **372 bp** raw Germany route gap.

The important part is not the gap. The important part is the conclusion:

> **A route gap is an investigation signal, not an uplift estimate.**

Traffic mix, issuer mix, authentication, amount, customer mix and selection into routes can all contaminate the comparison.

## What I would do with client data

1. Rebuild authorization at payment-attempt level with stable state definitions.
2. Preserve denominators and eligible populations.
3. Slice by market, BIN/issuer where legally and operationally appropriate, method, device, 3DS, amount, currency, route and retry position.
4. Quantify sampling uncertainty.
5. Adjust observational comparisons for material mix differences.
6. Escalate only robust candidate interventions into a prospective experiment.

## Deliverable

A merchant receives an authorization map with:

`segment → attempts → authorized → auth rate → failed value → evidence strength → suspected mechanism → next test`.

---

# Case file 03 — Routing as an experiment, not a story

## Question

How do you know a routing change actually improves acceptance?

## Executed design

A separate N=40,000 randomized synthetic experiment isolates a routing treatment from the observational environment.

**Seeded result:**

- treatment-control authorization difference: approximately **+248 bp**;
- 95% confidence interval: approximately **+191 to +305 bp**.

## Why this matters

The portfolio intentionally contains both a **372 bp observational gap** and a **248 bp randomized effect**. They are not merged into one persuasive number.

That distinction is the work.

A production experiment would add pre-specified eligibility, sample-size logic, exposure logging and guardrails for:

- fraud;
- disputes;
- processing cost;
- latency;
- retries;
- customer friction;
- provider concentration risk.

The decision metric is not “authorization went up.” It is whether the intervention improves **net payment value under risk and cost constraints**.

---

# Case file 04 — Stripe payment-state execution

## Question

Can the analysis connect to actual provider states, or does it stop at a dashboard?

## Retained provider-test evidence

Executed Stripe test-mode records cover:

- successful PaymentIntent authorization;
- generic decline;
- insufficient-funds decline;
- a 3DS path reaching `requires_action`;
- manual authorization → capture → refund;
- signed webhook delivery accepted only after signature verification.

The code also implements deeper failure scenarios, idempotency-aware requests, raw-body webhook validation, replay tolerance and a persistent event-id ledger.

## What this demonstrates

A checkout diagnosis can be translated into operationally precise states:

`attempt → requires_action / requires_capture / succeeded / failed → capture → refund → webhook → ledger`.

That matters because an “authorization problem” can actually be an authentication, capture, duplicate-event, retry, refund or state-projection problem.

---

# Case file 05 — Decline forensics

## Question

Which failed payments deserve action, and which should be left alone?

## Demonstrated failure classes

The environment and provider-test layer distinguish cases such as:

- insufficient funds;
- generic decline / do-not-honor-style outcomes;
- authentication failure;
- invalid account;
- lost/stolen-card scenarios;
- expired card;
- incorrect CVC;
- processing error;
- velocity-style limits.

## Method

A decline taxonomy is not a chart of reason-code frequencies. Each class should be assigned:

`observed code → normalized family → evidence source → customer action? → retry eligibility → retry timing → terminal? → risk sensitivity → messaging rule`.

Sensitive fraud/lost/stolen-style failures should never be turned into over-specific customer messaging that leaks issuer risk signals.

## Production output

The report ranks decline families by:

- count;
- failed value;
- first-attempt vs retry position;
- market/method/device/authentication path;
- subsequent recovery;
- customer action required;
- operational safety of intervention.

---

# Case file 06 — 3DS friction without blaming 3DS

## Question

Is authentication costing conversion, and if so where?

## Existing proof

A retained Stripe test path reaches `requires_action`. The public merchant environment also contains 3DS state as an analytical dimension.

## Client analysis

I would construct the authentication funnel as distinct states:

`eligible → exemption/request decision → challenge required → challenge presented → authenticated → authorization submitted → authorized`.

The point is to separate:

- authentication initiation;
- challenge friction;
- authentication failure;
- post-authentication issuer decline.

The fraud benchmark provides the guardrail: SCA cannot be treated as friction to eliminate. The EBA/ECB evidence indicates it remains effective against important fraud classes, while fraud is adapting in other directions.

---

# Case file 07 — Webhook and duplicate-event integrity

## Question

Can a merchant trust its internal payment state?

## Implemented controls

The Stripe webhook path includes:

- raw-body signature verification;
- timestamp/replay tolerance;
- persistent event-id claiming;
- duplicate acknowledgement without duplicate processing.

## Failure modes I would audit

- missing events;
- events accepted without valid signature;
- duplicated financial side effects;
- out-of-order state projection;
- payment state differing from provider state;
- capture/refund events not reflected in internal ledgers.

A conversion dashboard is not useful if its underlying event model cannot be trusted.

---

# Case file 08 — Capture, refund and reconciliation

Checkout success is not the end of the payment.

A companion reconciliation engine demonstrates:

- append-only event history;
- authorization/capture/refund/fee states;
- expected net settlement calculation;
- settlement matching;
- mismatch classification;
- duplicate event handling;
- unknown settlement records routed to investigation.

The seeded demo includes an exact partial-refund reconciliation, an amount mismatch and an unknown settlement row. The objective is to show the operational bridge from acceptance analytics to financial correctness.

---

# What I execute in a Checkout Leak Audit

## Input layer

Depending on scope and availability:

- PSP exports / payment-attempt tables;
- authorization and decline fields;
- 3DS/authentication events;
- capture/refund events;
- payment-method and route fields;
- order/cart value;
- retry chains;
- dispute/fraud signals;
- processor fees;
- payout/settlement reports;
- webhook/event logs.

## Build layer

I produce:

1. payment-state model and metric dictionary;
2. data QA and denominator audit;
3. authorization funnel;
4. failed-value waterfall;
5. decline taxonomy;
6. market × method × device × authentication matrices;
7. retry-sequence analysis;
8. route diagnostics;
9. 3DS funnel;
10. capture/refund integrity checks;
11. reconciliation exception table where data permits;
12. experiment candidates with guardrails;
13. ranked 30-day action register;
14. reproducible SQL/Python appendix;
15. proof ledger recording every material finding.

## Decision layer

Every recommendation lands in one of four buckets:

- **FIX NOW** — state/data/implementation defect with direct evidence;
- **INVESTIGATE** — concentrated loss signal that is not yet causal;
- **TEST** — credible intervention requiring prospective evaluation;
- **DO NOT TOUCH** — apparent opportunity fails risk, evidence or economics checks.

---

# The proof ledger standard

Every important result is recorded as:

`CLAIM → NUMBER → EVIDENCE TYPE → SOURCE → DATE → CODE → REPRODUCIBLE? → LIMITATION → STATUS`

Canonical evidence labels:

- `OFFICIAL SOURCE`
- `REAL PUBLIC DATA`
- `PROVIDER TEST`
- `SYNTHETIC`
- `RANDOMIZED SYNTHETIC`
- `PRODUCTION CLIENT DATA`
- `EXTERNAL REVIEW`
- `INDEPENDENT REPRODUCTION`
- `PENDING VALIDATION`

The evidence class is part of the result, not fine print.

---

# What I will not claim

This portfolio does **not** claim:

- production merchant access that has not been provided;
- live-money processing;
- PCI certification;
- a production authorization uplift;
- recovered merchant revenue;
- scheme/acquirer certification;
- causal inference from an uncontrolled route comparison.

The first real merchant engagement should become the first production case study only with explicit client permission and its own `PRODUCTION CLIENT DATA` badge.

---

# Reproduce the public proof

```bash
python public_market_analysis.py
python generate_data.py
python analyze.py
python experiment.py
python -m unittest discover -s tests -v
```

Provider-test scenarios require developer-owned Stripe test credentials; retained redacted evidence is in `provider_sandboxes/evidence/`.

---

# Buyer challenge

A buyer should be able to ask:

- Where did this number come from?
- What is the denominator?
- Is it public, synthetic, provider-test or production evidence?
- Can I rerun it?
- What assumption would overturn the conclusion?
- Why does this recommendation require a test rather than a rollout?
- What risk or cost could reverse the apparent benefit?

If the portfolio cannot answer those questions, the result is not ready to sell.
