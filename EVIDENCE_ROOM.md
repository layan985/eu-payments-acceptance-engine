# Checkout Evidence Room

## WHERE IS CHECKOUT LOSING MONEY?

This room is a forensic demonstration, not a claim of production merchant access.

### Evidence snapshot

| Object | Number / status | Badge | Boundary |
| --- | ---: | --- | --- |
| Merchant transaction environment | 300,000 transactions | `SYNTHETIC` | Generated with fixed seed; not client data |
| Overall authorization | 93.10% | `SYNTHETIC` | Seeded environment |
| Germany PSP gap | 372 bps | `SYNTHETIC` | Observed diagnostic gap; **not causal** |
| Randomized routing effect | ~248 bps | `RANDOMIZED SYNTHETIC` | Separate experiment; not realized merchant uplift |
| Randomized 95% CI | ~191–305 bps | `RANDOMIZED SYNTHETIC` | Applies only to seeded experiment |
| Stripe authorization success | executed | `PROVIDER TEST` | Stripe test mode |
| Stripe declines | executed | `PROVIDER TEST` | Test-card behavior |
| Stripe 3DS `requires_action` | executed | `PROVIDER TEST` | Test authentication flow |
| Authorization → capture → refund | executed | `PROVIDER TEST` | Test lifecycle |
| Signed webhook verification | executed | `PROVIDER TEST` | Test delivery + local verifier |
| Production merchant case | 0 | `PENDING VALIDATION` | No production merchant claim |

Full claim-level detail: [PROOF_LEDGER.md](PROOF_LEDGER.md).

## Visual evidence contract

The buyer-facing Checkout surface should contain these objects, each with a forensic footer:

1. Authorization funnel
2. Decline taxonomy
3. 3DS drop-off view
4. Country × payment-method heatmap
5. Retry-sequence Sankey
6. Refund / payout timeline
7. Money-at-risk waterfall
8. PSP experiment confidence interval
9. Action-priority matrix

Under every chart:

**SOURCE / N / WINDOW / FILTER / STATUS / LIMITATION / DOWNLOAD DATA**

No chart may visually blur `SYNTHETIC`, `RANDOMIZED SYNTHETIC`, and `PROVIDER TEST` evidence.

## Sample client-report structure

A six-page pre-purchase sample should show:

1. **Executive loss map** — where authorization is leaking and what is known vs unknown.
2. **Failure anatomy** — decline categories, 3DS friction, device / method / geography cuts.
3. **Money at risk** — a transparent scenario model, explicitly marked synthetic unless client data exists.
4. **Experiment design** — observational signals separated from randomized evidence.
5. **Payment operations** — retry, customer action, capture/refund and webhook controls.
6. **Action register** — prioritized changes, expected evidence standard, guardrails, and next measurement.

Any sample merchant must be labeled **SYNTHETIC DEMO** on every page where its data appear.

## First real case standard

The first production case should only become public as:

**CASE 001 — REAL MERCHANT DATA / ANONYMIZED / CLIENT-APPROVED**

Required before publication:

- explicit client approval;
- anonymization review;
- exact measurement window;
- documented filters and exclusions;
- before/after or experimental design stated precisely;
- no causal language without causal identification;
- limitations visible next to the headline number;
- reproducible analysis package where confidentiality permits.
