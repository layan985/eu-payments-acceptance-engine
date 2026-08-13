# Checkout Leak Audit — Sample Client Report

**Status:** SYNTHETIC DEMO. This sample uses generated merchant transactions plus separate provider-test evidence. It is not a production client case and does not claim realized revenue uplift.

## Page 1 — Executive finding

The synthetic environment contains 300,000 payment attempts with a seeded overall authorization rate of 93.10%. The largest raw market-route diagnostic is Germany, where PSP_A authorizes at 93.03% and PSP_B at 89.31%, a 372 bp observational gap. That gap is not treated as causal.

A separate randomized synthetic experiment estimates a 247.9 bp treatment-control difference, with a 95% confidence interval of 190.9–304.9 bps. The randomized result is a demonstration of evaluation design, not evidence of merchant revenue uplift.

**Decision:** a real merchant should not reroute traffic because of the 372 bp diagnostic alone. The next step would be a pre-specified experiment with fraud, disputes, latency, fees and customer-experience guardrails.

## Page 2 — Authorization and decline diagnostics

Across all generated attempts, 93.10% authorize and 6.90% decline.

Synthetic decline mix:

- insufficient funds: 31.3% of declines;
- do not honor: 27.6%;
- authentication failed: 21.4%;
- invalid account: 11.8%;
- lost or stolen: 8.0%.

These shares are generator inputs. They demonstrate how a decline taxonomy should be presented and prioritized, but they are not estimates of a real merchant's decline population.

## Page 3 — Authentication and payment-method view

Attempts tagged for 3DS authorize at 92.15% versus 93.75% among attempts without the tag. This is a synthetic association, not a causal 3DS penalty. The dataset does not record shopper abandonment during authentication, so a true 3DS drop-off funnel cannot be calculated.

The strongest payment-method rates in the seeded environment tend to appear for PayPal and SEPA debit, while card rates are lower in several cells. These differences reflect encoded generator behavior and sample composition.

**Required client fields:** authentication start, challenge presented, challenge completed, abandonment state, exemption state, payment method, device, issuer/market and final authorization outcome.

## Page 4 — Money at risk

Generated attempted value totals approximately €13.86 million. Approximately €12.90 million is attached to authorized attempts and €958 thousand to failed attempts.

The €958 thousand figure is **failed attempted value, not lost revenue**. Without retry linkage, subsequent conversion, duplicate-attempt resolution and order-level outcomes, failed attempted value cannot be converted into a revenue-loss claim.

A production audit would reconcile payment attempts to order IDs and customer/session IDs before estimating recoverable value.

## Page 5 — Provider operations evidence

Separate Stripe test-environment evidence demonstrates:

- successful PaymentIntent authorization;
- deliberate generic and insufficient-funds declines;
- a 3DS path reaching `requires_action`;
- manual authorization followed by capture and refund;
- a signed webhook accepted after `Stripe-Signature` verification.

This evidence proves test-environment execution and operational handling. It does not prove production reliability, live-money processing, certification or merchant uplift.

## Page 6 — Action queue and evidence boundary

| Finding | Current evidence | Next real-world action | Guardrail |
| --- | --- | --- | --- |
| Germany PSP dispersion | synthetic observational | randomized routing test | fraud, disputes, latency, fees |
| Mobile/3DS performance | synthetic diagnostic | instrument authentication funnel | SCA compliance, fraud, abandonment |
| Insufficient-funds declines | seeded decline mix | measure retry success by reason and delay | customer fatigue, duplicate attempts |
| Refund/payout exceptions | not modeled | request lifecycle + payout fields | reconciliation accuracy |

### Claim boundary

No production merchant data is present. No live-money processing is claimed. No merchant revenue uplift is claimed. The first qualifying production object should be labeled:

**CASE 001 — REAL MERCHANT DATA / ANONYMIZED / CLIENT-APPROVED**

Every public number should remain linked to the repository Proof Ledger and retain its evidence class, source, date, reproducibility status and limitation.