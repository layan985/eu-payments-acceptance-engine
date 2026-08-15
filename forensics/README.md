# Checkout Forensic Portfolio — Real-Data Expansion

This room contains five additional public-evidence projects built to answer the buyer question that matters most:

> **Can you move from external payments evidence to a defensible merchant investigation without inventing causality, client data or recovered revenue?**

Every project below separates `OFFICIAL SOURCE`, `REAL PUBLIC DATA`, `DERIVED PUBLIC DATA`, `PROVIDER TEST`, `SYNTHETIC`, and `PENDING VALIDATION`.

---

## Project 01 — Cross-border fraud × SCA exposure

**Question.** If a merchant improves authorization, where can fraud or authentication risk erase the gain?

**Public evidence.** The joint EBA/ECB 2025 payment-fraud report records €4.2bn of EEA payment fraud in 2024, up from €3.5bn in 2023. Credit-transfer fraud losses were €2.200bn (+16% YoY); card-payment fraud losses on EU/EEA-issued cards were €1.329bn (+29% YoY). For credit transfers, payment-service users bore about 85% of losses. Card fraud was reported as 17 times higher when the recipient was outside the EEA, where SCA is not legally required and is often not used. The EBA's December 2025 risk assessment reports fraudulent card payments at 0.015% of volume and 0.033% of value in 2024.

**Derived diagnostics.** From those published aggregates:

- total fraud value increased **20.0%** from 2023 to 2024;
- credit-transfer fraud represented about **52.4%** of the reported €4.2bn total;
- card fraud represented about **31.6%**;
- the remainder across other reported instruments was about **16.0%**.

These shares are descriptive decomposition, not causal attribution.

**What I would execute for a merchant.** Build a matrix by EEA/non-EEA counterparty, SCA/non-SCA, exemption, issuer country, merchant country, route, method and device; calculate fraud rate and authorization rate on identical denominators; estimate gross authorization lift and then apply fraud/dispute/cost guardrails; isolate one-leg/cross-border surfaces; audit exemptions; design a pre-specified test where a routing or authentication change is actually testable.

**The finding I would not make.** “Turn off 3DS to increase conversion.” The public evidence supports the opposite discipline: any friction intervention has to be evaluated jointly with fraud exposure and regulatory constraints.

Dataset: `forensics/data/cross_border_sca_fraud_2024.csv`

---

## Project 02 — European payment-method structure and localization

**Question.** Why is one European checkout configuration unlikely to be optimal across markets?

**Public evidence.** ECB H2 2025 statistics report 83.5bn euro-area non-cash payments. Cards represented 57% of count, credit transfers 21%, direct debits 14% and e-money 6%. At national level, Cyprus had the highest card share at about 75%, Latvia the highest credit-transfer share at about 36%, and Germany the highest direct-debit share at about 31%. Card payments totaled 47.8bn transactions; remote payments were 19% of card count but 30% of card value. Contactless accounted for 85% of non-remote card count.

**Derived diagnostic.** Using the rounded ECB aggregates, remote card payments imply roughly **9.08bn** transactions and €0.54tn of value, versus **38.72bn** non-remote transactions and €1.26tn. The implied average ticket is about **€59.46 remote vs €32.54 non-remote**, a ratio of roughly **1.83×**. These are approximate because the ECB source shares and totals are rounded.

**What I would execute for a merchant.** Build country × method × device × authentication × ticket-size matrices; rank exposed value rather than just failure counts; test whether “weak markets” are really payment-method mix problems; quantify local-method coverage; separate remote from physical behavior; and recommend market-specific experiments rather than a global checkout rewrite.

**Commercial output.** A Payment-Method Coverage Map, localization gap register, remote-ticket exposure table, country-specific acceptance scorecard and experiment queue.

Dataset: `forensics/data/eu_payment_structure_h2_2025.csv`

---

## Project 03 — Instant Payments + Verification of Payee readiness

**Question.** Can a European payment product translate regulation into an executable implementation and control map?

**Regulatory evidence.** Regulation (EU) 2024/886 requires euro-area PSPs in scope to receive instant euro credit transfers by 9 January 2025 and send them by 9 October 2025. Charges for instant transfers cannot exceed corresponding regular credit-transfer charges; euro-area PSPs had to comply with the charging rule by 9 January 2025. Verification of Payee (VoP) must be offered before authorization of the transfer; euro-area PSPs had to comply by 9 October 2025. Non-euro-area deadlines extend into 2027. Payment institutions and electronic-money institutions have specific later reachability deadlines. The EPC's VoP Scheme Rulebook v1.1 was published 16 March 2026 and becomes effective **20 September 2026**.

**Current-state inference as of 15 August 2026.** The primary euro-area bank reachability, sending and VoP dates are already in force. EPC VoP v1.1 is **36 days from effective date**, making change-readiness—not first-time regulatory discovery—the relevant operational question for an already-live euro-area bank.

**What I would execute.** Build a requirements-to-controls matrix covering reachability, sending, fees, VoP invocation, `match / close_match / no_match / verification_not_possible`, customer messaging, liability, sanctions-screening cadence, API/state handling, duplicate submission and exception monitoring. Then map each control to owner, evidence, test case and failure severity.

**Proof already connected to Checkout.** The companion `sepa-instant-vop-simulator` implements IBAN validation, VoP-style outcomes, state transitions and idempotency as an educational simulator. It is not presented as scheme-certified connectivity.

Dataset: `forensics/data/instant_vop_readiness_2026.csv`

---

## Project 04 — Processor economics: Adyen public benchmark

**Question.** Can I reason about payment economics without confusing processor financials, merchant price and interchange?

**Public evidence.** Adyen reported Q1 2026 net revenue of €620.8m on €382.0bn processed volume. For H2 2025 it reported €1,270.7m net revenue on €745.3bn processed volume, including €173.1bn point-of-sale volume, and €702.1m EBITDA at a 55% margin. Full-year 2025 net revenue was €2,364.2m on €1,394.3bn processed volume, with €311bn POS volume and a 53% EBITDA margin.

**Derived diagnostics.** A simple net-revenue / processed-volume ratio is approximately:

- **16.25 bps** in Q1 2026;
- **17.05 bps** in H2 2025;
- **16.96 bps** in FY2025.

POS volume represented roughly **23.2%** of H2 2025 processed volume and **22.3%** of FY2025 processed volume.

**Critical boundary.** This ratio is **not merchant MDR, interchange, scheme fee or a quoted Adyen price**. It is an analytical proxy from company-level disclosed aggregates. Presenting it as “Adyen charges ~17 bps” would be wrong.

**What I would execute for a merchant.** Reconstruct effective processing cost from actual PSP invoices and settlement files: interchange, scheme/network fees, processor markup, gateway fees, FX, cross-border, 3DS, refund/chargeback and other line items; then join cost to approval and fraud outcomes so routing is optimized for net contribution rather than authorization alone.

Dataset: `forensics/data/adyen_processor_economics.csv`

---

## Project 05 — Zalando checkout architecture teardown

**Question.** What can be inferred about a real multi-market European checkout and its operational failure surface from public first-party evidence?

**Public evidence.** Zalando Payments describes infrastructure supporting **60m+ active customers** and local payment methods across **25 markets**. A Zalando payments role describes **20+ payment options** across 25 European markets. Zalando's partner documentation states that Cash on Delivery through Zalando Shipping Solutions is available in Czech Republic, Italy, Poland and Spain and is mandatory for Poland in its country onboarding requirements. Its order-quality documentation shows payment by invoice requires the Zalando order number as the payment reference and is not enabled in every country. Partner payout documentation supports local-currency mode or euro mode, creating explicit bank-account and FX handling choices.

**Architecture inference.** The payment problem is not “which PSP?” It is a localization-and-ledger system spanning method eligibility, country rules, customer risk, order reference integrity, invoice allocation, CoD, settlement currency, partner payout, refunds and reconciliation.

**What I would execute.** Build a market-method eligibility matrix; payment-state and ledger map; order-reference reconciliation test; CoD/invoice exposure report; local-currency/FX settlement map; failure taxonomy; and a country-by-country checkout QA plan. On production data, I would then connect those controls to authorization, abandonment, fraud, refund and payout exceptions.

**What this teardown does not claim.** It does not claim access to Zalando production data, internal payment-provider routing, hidden fraud rules, conversion rates or commercial contracts. It shows how to construct a testable diligence map from public first-party evidence.

Dataset: `forensics/data/zalando_checkout_architecture.csv`

---

# The portfolio now proves a complete chain

1. **Market structure** — official ECB payments data.
2. **Risk** — official EBA/ECB fraud and SCA evidence.
3. **Regulation** — Instant Payments / VoP requirements translated into controls.
4. **Economics** — processor financials interpreted with disciplined boundaries.
5. **Real merchant architecture** — a public first-party checkout teardown.
6. **Transaction analytics** — the existing 300,000-attempt merchant environment.
7. **Causal testing** — the existing randomized routing experiment.
8. **Provider execution** — retained Stripe test-mode evidence.
9. **Post-payment operations** — webhook integrity and reconciliation.

That is the object to send when a buyer asks, “What have you actually done?”

## Reproduce

```bash
python forensics/analyze_forensics.py
```

The script uses Python's standard library only and reads the public CSVs in `forensics/data/`.

## Source register

- ECB, *Payments statistics: second half of 2025*, 22 July 2026.
- EBA/ECB, *Joint report on payment fraud*, 15 December 2025.
- EBA, *Risk Assessment Report*, December 2025.
- EUR-Lex, Regulation (EU) 2024/886.
- European Payments Council, Verification of Payee Scheme Rulebook v1.1, 16 March 2026; effective 20 September 2026.
- Adyen, H2 2025 financial results, 12 February 2026; Q1 2026 Business Update, 6 May 2026.
- Zalando first-party Partner/Payments documentation, accessed 15 August 2026.

## Claim rule

No derived public-market number is a merchant result. No provider sandbox execution is production processing. No public-company teardown is inside access. No observed route difference is called causal uplift without an identification strategy.