# Where is checkout losing money?

<div class="meta-line"><span>INDEPENDENT PAYMENT ACCEPTANCE INTELLIGENCE</span><span>EVIDENCE BEFORE UPLIFT</span><span>BUYER-INSPECTABLE WORK</span></div>

Checkout diagnoses authorization loss, authentication friction, retry behavior, routing, payment-state integrity and reconciliation for multi-market digital businesses. The current flagship experiment asks a harder question: **does a decline reason actually tell you which intervention would have recovered the payment?** PFX-1 measures the Recoverability Frontier — the amount of failed demand recoverable under the merchant's feasible action set — rather than treating every decline or retry as the same economic object.

<div class="metric-grid"><div><b>600,000</b><span>PFX-1 reproducible synthetic attempts</span></div><div><b>20.93%</b><span>holdout recovery · context policy</span></div><div><b>14.05%</b><span>best blanket rescue · holdout</span></div><div><b>+45.5 bps</b><span>overall authorization vs blanket · randomized synthetic</span></div></div>

## External + production proof

<div class="metric-grid"><div><b>3</b><span>external reviews completed</span></div><div><b>1</b><span>independent reproduction completed</span></div><div><b>1</b><span>paid audit completed</span></div><div><b>1</b><span>measured production case retained</span></div><div><b>1</b><span>client testimonial retained</span></div><div><b>1</b><span>referral / repeat engagement retained</span></div></div>

These are **aggregate proof counts, not substitutes for a public case study**. Reviewer/client identities, production metrics, testimonial wording, contract details and referral counterparties remain permission-controlled unless explicitly cleared for publication. Where a public quote, metric or client identity is unavailable, Checkout says so rather than implying more disclosure than exists.

Third-party evidence is now the priority: additional external reproduction, external review, permissioned production cases and client validation are more valuable than simply publishing another self-authored report.

## What gets interrogated

- **Payment-object identity.** Attempt, intent, order, authorization, capture, refund, dispute and settlement objects are not treated as interchangeable rows.
- **The denominator contract.** Attempt authorization, payment-intent resolution, customer resolution and economic-value resolution are kept separate.
- **Recoverability.** A decline label is not assumed to identify the best rescue. Route, authentication, credential/token and timing interventions are evaluated inside an explicit feasible action set.
- **Method + route eligibility.** A processor or payment-method gap is screened for mix, eligibility and assignment before anyone calls it uplift.
- **3DS / SCA state.** Eligible, challenged, authenticated, attempted, authorized and captured are treated as distinct transitions.
- **Decline mechanism.** Hard, soft, authentication, issuer, technical and policy failures are separated before retry logic is evaluated.
- **Retry chains.** Recovery is measured at the intent and economic-value level, not by celebrating a higher count of attempts.
- **Lifecycle integrity.** Duplicate events, impossible transitions, capture/refund identity and state drift are tested before performance conclusions are trusted.
- **Reconciliation.** Provider events, merchant state and economic settlement are joined only inside an explicit perimeter.

## The work is inspectable

- [Report 004 · PFX-1 — Decline Codes Are Not Failure Types](/research/recoverability-frontier)
- [Report 001 · Checkout Leak Audit — Sample Diagnostic](/research/checkout-leak-audit)
- [Report 002 · The Authorization Rate Is Lying to You](/research/authorization-rate)
- [Report 003 · Payment State Integrity](/research/payment-state-integrity)
- [Evidence Room](/evidence)
- [Case File 001 · Zalando — INDEPENDENT PUBLIC-SOURCE INVESTIGATION · NOT A CLIENT](/case-files/zalando)
- [Case File 002 · Booking.com — INDEPENDENT PUBLIC-SOURCE INVESTIGATION · NOT A CLIENT](/case-files/booking)
- [One-URL Proof Packet](/proof-packet)
- [Production outcomes + disclosure boundary](/client-outcomes)
- [Founding Production Rate · €1,950](/services)

<div class="callout"><b>A decline code is not a treatment policy.</b><p>PFX-1's +45.5 bps result is a randomized synthetic benchmark, not a merchant uplift claim. The frozen context policy beat the best blanket rescue by 6.88 percentage points of declined intents on an untouched holdout (95% CI +5.49 to +8.26 pp). The next claim that matters requires randomized merchant data under retry, fraud, dispute, cost and customer-friction guardrails.</p></div>

## What a buyer actually receives

The production standard is an **8–15 page decision pack plus reproducible analytical outputs**, not a generic strategy deck. The buyer room is expected to contain the Payment Data QA report, metric dictionary, failed-value waterfall, decline taxonomy, 3DS friction view, country × payment-method cuts, route/provider screen with causality warnings, retry/recovery analysis, lifecycle and reconciliation exceptions, intervention register, Proof Ledger, Methodology, Limitations Register and the analysis files needed to interrogate the result.

Every material number carries the strongest evidence label actually available: **OFFICIAL SOURCE, REAL PUBLIC DATA, PROVIDER TEST, SYNTHETIC, RANDOMIZED SYNTHETIC, PRODUCTION CLIENT DATA, EXTERNAL REVIEW, INDEPENDENT REPRODUCTION or PENDING VALIDATION.** Observed differences are not rewritten as causal effects.

## Founding Production Rate

**Checkout Leak Audit · €1,950 · 50% upfront · fixed scope · limited early-case allocation.** This is deliberately a **Founding Production Rate**, not the intended long-run specialist-practice price. The rate exists while additional permissioned production cases and third-party validation are being built; pricing is expected to rise with the evidence base and delivery history.

Exact inputs, Day 0–5 operating timeline, deliverables, refusal boundaries and data-security expectations are public on the [service page](/services). Every engagement closes with a Proof Ledger, a Limitations Register and a decision register: **FIX · INVESTIGATE · TEST · DO NOT TOUCH.**
