# Checkout validation and commercial proof registry

**Status date:** 17 August 2026

This is the canonical aggregate registry for completed external, production and commercial proof attached to Checkout.

| Proof layer | Completed | Evidence class | Public disclosure |
|---|---:|---|---|
| External reviews | **3** | EXTERNAL REVIEW | Aggregate count public; identities/review text only where publication permission exists |
| Independent reproductions | **1** | INDEPENDENT REPRODUCTION | Aggregate count public; reproducer detail only where publication permission exists |
| Paid Checkout audits | **1** | PRODUCTION CLIENT DATA / COMMERCIAL RECORD | Aggregate count public; client identity and commercial terms permission-controlled |
| Measured production cases | **1** | PRODUCTION CLIENT DATA | Aggregate count public; metrics, data perimeter and client identity permission-controlled |
| Client testimonials | **1** | CLIENT VALIDATION | Aggregate count public; wording and attribution permission-controlled |
| Referral / repeat engagements | **1** | COMMERCIAL VALIDATION | Aggregate count public; counterparty identity permission-controlled |

## What these counts mean

**External review** means an outside person completed substantive scrutiny of Checkout work. Self-run CI, GitHub stars, invitations to review and friendly comments do not count.

**Independent reproduction** means an outside person completed a rerun/reproduction independently of the author. The project's own `python reproduce.py` gate does not count toward this number.

**Paid audit** means a real Checkout engagement crossed the paid-engagement threshold. A proposal, lead, discovery call or unpaid sample does not count.

**Measured production case** means real production evidence exists with an observed outcome and a retained measurement record. Synthetic demonstrations and provider test-mode executions do not count.

**Testimonial** means client feedback exists as a retained client-validation record. Public quotation or attribution remains permission-controlled.

**Referral / repeat engagement** means commercial trust produced either a repeat engagement or a referral outcome. A warm introduction alone is not silently upgraded beyond the retained record.

## Publication boundary

This registry publishes aggregate proof counts. It does **not** publish private client identity, reviewer identity, testimonial wording, production metrics, payment volume, contract terms or referral counterparties unless the corresponding disclosure permission permits it.

The evidence classes remain distinct:

`SYNTHETIC` · `RANDOMIZED SYNTHETIC` · `PROVIDER TEST` · `PRODUCTION CLIENT DATA` · `EXTERNAL REVIEW` · `INDEPENDENT REPRODUCTION`

No synthetic or provider-test result is relabelled as production evidence because these external/commercial records exist.
