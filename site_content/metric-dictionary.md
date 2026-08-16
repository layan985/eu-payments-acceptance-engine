# Metric Dictionary

<div class="meta-line"><span>35 DEFINITIONS</span><span>PUBLIC OPERATING STANDARD</span><span>FOUNDER PRODUCED</span></div>

A metric is not accepted into a Checkout decision memo until the object, eligibility rule, denominator, state and identification status are explicit.

| Metric | Canonical operating definition |
|---|---|
| Payment attempt | One provider authorization attempt. Retries remain separate attempts. |
| Payment intent | Stable economic/customer payment object spanning one or more attempts. |
| Customer resolution | Share of customer payment objectives eventually resolved. |
| Attempt authorization rate | Authorized attempts / all authorization attempts. |
| Intent resolution rate | Resolved payment intents / initiated payment intents. |
| Economic-value resolution | Resolved intended value / total intended value. |
| Eligible traffic | Traffic that could actually receive the method, route or treatment. |
| Raw route gap | Observed difference between route groups before identification. |
| Randomized effect | Treatment-control difference under randomized assignment. |
| Basis point | 0.01 percentage point. |
| 3DS eligible | Attempt for which a 3DS flow is available under policy. |
| 3DS challenge rate | Challenged authentication objects / 3DS-eligible objects. |
| Authentication completion | Completed authentication objects / initiated challenges. |
| Issuer authorization | Issuer-approved attempts / eligible authorization attempts. |
| Soft decline | Decline potentially recoverable through changed timing, authentication or customer action. |
| Hard decline | Decline class not automatically retried by default. |
| Retry rate | Additional attempts / initial intents or attempts; denominator must be named. |
| Retry success | Resolved retried intents / retried intents. |
| Duplicate event rate | Duplicate delivered events / delivered events. |
| Capture rate | Captured payment objects / authorized objects. |
| Authorization reversal | Released/reversed authorization before capture. |
| Refund rate | Refunded objects or value / captured objects or value. |
| Dispute rate | Disputed captured objects or value / captured objects or value. |
| Settlement completion | Settled economic objects / captured objects eligible for settlement. |
| Reconciliation match | Expected economic state equals observed provider/ledger state. |
| Amount mismatch | Expected amount differs from reconciled provider/ledger amount. |
| Missing settlement | Captured object has no expected settlement inside the agreed SLA. |
| State mismatch | Provider, merchant and ledger states disagree. |
| Failed value | Eligible economic value not successfully resolved under the stated state definition. |
| Recovered value | Previously failed economic value later resolved under prespecified recovery logic. |
| Incremental approvals | Treatment approvals minus counterfactual approvals under an identified experiment. |
| Incremental approved value | Incremental approvals × prespecified actual/average value, before downstream economics. |
| Net economic effect | Incremental retained value net of fraud, disputes, fees, refunds and implementation effects. |
| Confidence interval | Uncertainty interval around an estimated effect under stated assumptions. |
| Attribution window | Prespecified time window over which intervention and outcome are linked. |

## Metric governance

Definitions can be refined for a merchant's stack, but silent denominator changes are not allowed. If one dashboard says “authorization” and another means “resolved payment intent,” the discrepancy is documented before either number enters an executive memo.

## Four-denominator minimum for recovery work

1. attempt authorization;
2. unique payment-intent resolution;
3. customer resolution where customer identity is lawful and available;
4. economic-value resolution.

## State minimum

At minimum, Checkout distinguishes `CREATED`, `AUTHENTICATION`, `AUTHORIZED`, `CAPTURED`, `SETTLED`, `DECLINED`, `REVERSED`, `REFUNDED`, and `DISPUTED` where the merchant/provider model exposes them.
