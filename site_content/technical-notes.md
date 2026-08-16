# Technical Research Notes

<div class="meta-line"><span>12 NOTES</span><span>PAYMENT ACCEPTANCE METHODS</span><span>PUBLIC</span></div>

These are short technical positions used to make the diagnostic logic inspectable before a buyer shares production data.

## Note 01 — Why attempt authorization is usually the wrong executive denominator

Retries mechanically change attempt-weighted rates. A recovery program can add failed attempts and therefore reduce attempt authorization while still improving unique payment-intent resolution. Attempt, intent, customer and economic-value denominators answer different questions.

## Note 02 — A processor gap is a screening statistic, not an uplift estimate

Route assignment is rarely random. Issuer mix, market, method, device, 3DS policy, fraud rules and fallback logic can create a large raw difference. A route table is where investigation starts, not where an annualized uplift claim ends.

## Note 03 — 3DS comparisons are selected populations

3DS status is normally conditional on risk, issuer, market, exemptions, authentication policy and merchant setup. Raw 3DS/no-3DS authorization differences are therefore selected comparisons, not treatment effects.

## Note 04 — Retry success must be keyed to the economic object

A second successful attempt does not create a second successful customer. Retry analysis should aggregate attempts back to the payment intent and preserve the reason, timing and sequence of prior failures.

## Note 05 — Authorization is not capture

Authorization reserves or confirms funds. Capture is a later lifecycle step. A merchant can have strong authorization and still lose value through capture failures, partial capture, reversal or downstream reconciliation errors.

## Note 06 — Webhook delivery is not economic state

Provider events can be duplicated, delayed or arrive out of order. Economic state needs stable object IDs, signature verification, idempotent processing and state-aware transition logic.

## Note 07 — Refund state belongs in acceptance economics

Gross authorization uplift can disappear after cancellation, refunds, fraud, chargebacks or support-driven reversals. “Approved value” is an intermediate metric unless the commercial question explicitly stops at authorization.

## Note 08 — Reconciliation is part of payment performance

A payment that appears successful at checkout but cannot be matched to order, capture, settlement or refund state is an operations problem with economic consequences. Reconciliation cannot be treated as somebody else’s back-office detail.

## Note 09 — Experiment randomization unit matters

Randomizing at attempt level can contaminate customer-level outcomes when one intent generates several attempts. The unit should usually align with the decision object: payment intent, customer session, order or eligible routing opportunity.

## Note 10 — Guardrails belong in the primary decision rule

Fraud, disputes, latency, fees, refunds and support contacts should constrain rollout. A treatment that improves authorization while materially worsening retained value is not a successful payment intervention.

## Note 11 — Public-source merchant analysis can still be falsifiable

A serious external case file should state what production evidence would overturn each hypothesis. The goal is to build a measurement map and experiment queue, not to pretend public documentation reveals private conversion rates.

## Note 12 — A good audit can recommend doing nothing

If a −132 bps raw route gap collapses to −11 bps after adjustment, the correct decision can be **DO NOT SWITCH ROUTING**. Avoiding an unnecessary implementation is a valid result even when there is no dramatic uplift to market.

## Publication rule

These notes are methodological positions. They are not production-client results, independent review or provider certification.
