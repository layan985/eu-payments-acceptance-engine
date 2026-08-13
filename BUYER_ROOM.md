# Checkout Buyer Room

The buyer room answers one question: **where is checkout losing value, what evidence supports that conclusion, and what should be tested next?** It does not claim production merchant access or realized merchant revenue uplift.

## Proof snapshot

| Claim | Number | Badge | Limitation |
| --- | ---: | --- | --- |
| Generated merchant environment | 300,000 attempts | `SYNTHETIC` | Not production behavior |
| Overall seeded authorization | 93.10% | `SYNTHETIC` | Encoded approval probabilities |
| Germany PSP_A vs PSP_B raw gap | 372 bps | `SYNTHETIC` | Diagnostic association; not causal |
| Randomized routing difference | ~248 bps | `RANDOMIZED SYNTHETIC` | Simulation only |
| Randomized 95% CI | ~191–305 bps | `RANDOMIZED SYNTHETIC` | Simulation only |
| Stripe success / decline / 3DS | retained executions | `PROVIDER TEST` | Test mode |
| Manual auth → capture → refund | retained execution | `PROVIDER TEST` | Test mode |
| Signed webhook verification | retained execution | `PROVIDER TEST` | Test mode |
| Production merchant audit | 0 | `PENDING VALIDATION` | No production dataset disclosed |
| Independent case study | 0 | `PENDING VALIDATION` | Outside merchant evidence required |

## Required buyer-room reports

The commercial room is deliberately deep, but depth comes from evidence traceability rather than invented results.

| Report | Current evidence available | Current status |
| --- | --- | --- |
| **Checkout Leak Audit Sample Report** | synthetic funnel/value diagnostics + provider-test lifecycle evidence | evidence-backed sample |
| **Authorization Diagnostic Report** | authorization outcomes, route/country slices, provider-test success/declines | evidence-backed sample |
| **Decline Taxonomy Report** | generated decline taxonomy + retained Stripe decline paths | `SYNTHETIC` + `PROVIDER TEST` |
| **3DS Friction Report** | retained Stripe `requires_action` path | `PROVIDER TEST`; production friction `PENDING VALIDATION` |
| **Retry Strategy Report** | synthetic decline/retry logic only | `SYNTHETIC`; production retry uplift `PENDING VALIDATION` |
| **Routing Experiment Memo** | N=40,000 randomized synthetic experiment, ~248 bps difference, ~191–305 bps 95% CI | `RANDOMIZED SYNTHETIC` |
| **Refund & Capture Integrity Report** | retained manual authorization → capture → refund lifecycle | `PROVIDER TEST` |
| **Payout/Reconciliation Report** | no production payout/settlement file disclosed | `PENDING VALIDATION` |
| **Payment Cost Report** | no merchant fee schedule or production acquiring-cost file disclosed | `PENDING VALIDATION` |
| **30-Day Action Register** | decision framework can be demonstrated; merchant-specific priorities require production data | framework available / client result `PENDING VALIDATION` |

## Visual evidence catalog

Every visual must show **SOURCE / N / WINDOW / FILTER / STATUS / LIMITATION / DOWNLOAD DATA** directly beneath it.

- **Authorization funnel** — attempt → authorized → captured/refunded where states exist.
- **Failed-value waterfall** — attempted value → declined value → potentially recoverable buckets; production recovery claims require client data.
- **Country × payment-method matrix** — authorization/decline rates with denominators and uncertainty.
- **Decline tree** — decline family → retryability/customer action/terminal states.
- **Retry path** — first failure → retry decision → subsequent state; production uplift remains unclaimed.
- **3DS funnel** — authentication-triggered → `requires_action` → completed/failed when observed.
- **Routing confidence interval** — treatment-control difference with the randomized synthetic CI clearly labeled.
- **Lifecycle exception timeline** — authorization → capture → refund/webhook transitions from retained provider tests.
- **Operational-risk matrix** — duplicate events, webhook verification, capture/refund integrity, reconciliation gaps and disclosure status.

The retained Stripe executions should be presented as screenshots/timelines/state diagrams/evidence cards wherever the underlying execution evidence permits. A diagram may summarize a retained test; it must not imply live settlement or merchant economics.

## Institutional buyer-room stack

1. Executive Brief
2. Evidence Room
3. Proof Ledger
4. Methodology
5. Data Dictionary
6. Source / Provenance Register
7. QA Report
8. Limitations Register
9. Results Report
10. Technical Appendix
11. Sample Client / Institutional Report
12. Chart Catalog
13. Metric Dictionary
14. Reproducibility Guide
15. Validation / External Review Pack
16. Commercial Capability Sheet
17. Exact Deliverables + Scope
18. Case Study Library
19. Release Notes / Changelog
20. Downloads
21. FAQ for Buyers
22. Decision Memos
23. One-page Briefs
24. Public Dashboard / Terminal
25. **What would falsify this?**
26. Claim badges on every important number

## Buyer-facing proof objects

- [Evidence Room](EVIDENCE_ROOM.md)
- [Proof Ledger](PROOF_LEDGER.md)
- [Methodology](METHODS.md)
- [Data Dictionary](DATA_DICTIONARY.md)
- [Results](RESULTS.md)
- [Commercial Evidence Pack](COMMERCIAL_EVIDENCE_PACK.md)
- [Decision Memo](decision_memo.md)
- [External Review Status](EXTERNAL_REVIEW.md)
- [Stripe provider-test evidence](provider_sandboxes/evidence/)

## What a real engagement answers

1. Where are first-payment and renewal failures concentrated?
2. Which decline categories can be retried and which require customer action?
3. Which markets, methods, devices, authentication paths and routes carry the most exposed value?
4. Are route differences robust after controlling for mix or, preferably, randomization?
5. Which changes should be tested rather than deployed by intuition?
6. Are captures, refunds, payouts and webhook states operationally consistent?
7. Which interventions remain beneficial after fraud, disputes, latency and processing cost?

## What would falsify or materially weaken the analysis?

A result is weakened when a clean rerun cannot reproduce it; when denominators/state mappings are wrong; when a pre-specified randomized client test fails to reproduce an alleged route/retry effect; when provider lifecycle evidence cannot be reproduced in test mode; or when fraud, disputes, fees or operational exceptions reverse an alleged net benefit.

Every buyer-facing number carries a source, denominator, time window, filter, evidence label and limitation.
