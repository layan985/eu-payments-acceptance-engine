# Methods

<div class="meta-line"><span>MEASUREMENT</span><span>IDENTIFICATION</span><span>CLAIM DISCIPLINE</span></div>

## Measurement contract

| Question | Required definition |
|---|---|
| What is an attempt? | one provider authorization attempt, preserving retries |
| What is an intent? | stable payment intent spanning attempts |
| Who is eligible? | traffic that could actually receive the method/route/intervention |
| What is success? | authorization, intent resolution, capture or economic outcome — stated explicitly |
| What is state? | provider event, merchant object state and economic ledger state kept distinct |

## Route comparisons

Raw processor differences are investigation screens. They are not uplift until traffic eligibility, selection and assignment are addressed. The public Germany example intentionally places an observed 372.39 bps gap beside a separate randomized 247.88 bps experiment.

## 3DS

3DS/non-3DS populations are selected by method, market, issuer, risk, exemptions and merchant rules. A raw split is not an A/B test.

## Retries

Attempt authorization can fall while payment-intent resolution rises because successful recovery creates additional attempts. Attempt, intent, customer and economic-value denominators remain explicit.

## Payment state

Authorization, capture, settlement, refund, reversal and dispute are not interchangeable. Event delivery and economic state require stable IDs and idempotent processing.

## Limitations / claim rules

<div class="callout danger"><b>Observed ≠ causal.</b><br/><b>Authorization ≠ realized revenue.</b><br/><b>Provider test ≠ production certification.</b><br/><b>Self-run CI ≠ independent reproduction.</b><br/><b>No production outcome without production evidence.</b></div>

[Audit methodology](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/institution/AUDIT_METHODOLOGY.md) · [Payment experiment design](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/institution/PAYMENT_EXPERIMENT_DESIGN.md) · [Proof Ledger](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/PROOF_LEDGER.md)