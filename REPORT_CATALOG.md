# Checkout Report Catalog

This catalog distinguishes evidence-backed sample reports from reports that require production merchant inputs. No report is represented as a completed client result unless the underlying evidence exists.

| Report | Purpose | Evidence now | Production inputs required | Status |
| --- | --- | --- | --- | --- |
| Checkout Leak Audit Sample Report | Map value loss across the payment lifecycle | generated transaction environment + provider-test lifecycles | merchant transactions, order value, payment states, timestamps, route/method/device/country | Sample available from controlled evidence |
| Authorization Diagnostic Report | Explain where authorization differs and where to investigate | synthetic country/route slices + Stripe success/declines | production auth attempts and processor response data | Sample available; client result `PENDING VALIDATION` |
| Decline Taxonomy Report | Separate retryable, customer-action and terminal decline classes | generated decline taxonomy + retained Stripe decline paths | production decline codes/reasons | Sample available; client distribution `PENDING VALIDATION` |
| 3DS Friction Report | Trace authentication-triggered abandonment and state transitions | Stripe test path reaching `requires_action` | production 3DS/authentication events | Provider-test evidence only |
| Retry Strategy Report | Define safe retry decision rules and test plan | synthetic failure logic | production decline history, retry history, fraud/dispute guardrails | `PENDING VALIDATION` for merchant effect |
| Routing Experiment Memo | Specify and interpret a randomized route test | N=40,000 randomized synthetic experiment; ~248 bps difference; ~191–305 bps 95% CI | production randomization, outcome guardrails, pre-specified decision rule | `RANDOMIZED SYNTHETIC`; client effect `PENDING VALIDATION` |
| Refund & Capture Integrity Report | Audit capture/refund lifecycle consistency | retained Stripe manual auth → capture → refund | production capture/refund/event records | Provider-test evidence only |
| Payout/Reconciliation Report | Reconcile processor events to settlement/payout records | architecture only | production balance transactions, payouts, ledger/orders | `PENDING VALIDATION` |
| Payment Cost Report | Quantify processing/acquiring cost and net route economics | no production fee schedule | merchant pricing/fees, FX, scheme/acquirer costs | `PENDING VALIDATION` |
| 30-Day Action Register | Convert evidence into owners, tests, dependencies and acceptance criteria | decision framework | merchant diagnostics and operating constraints | Framework available; merchant priorities `PENDING VALIDATION` |

## Standard sections in every released report

Executive brief · scope/window/population · claim badges · key evidence cards · charts · methodology · metric dictionary · source/provenance register · QA · limitations · decision memo · action register · reproducibility/downloads · **what would falsify this?**

## Visual catalog

1. Authorization funnel
2. Failed-value waterfall
3. Country × payment-method matrix
4. Decline tree
5. Retry path
6. 3DS funnel
7. Routing confidence interval
8. Payment-lifecycle exception timeline
9. Operational-risk matrix

Every visual displays: **SOURCE / N / WINDOW / FILTER / STATUS / LIMITATION / DOWNLOAD DATA**.
