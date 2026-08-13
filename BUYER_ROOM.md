# Checkout Buyer Room

This repository is packaged as an inspectable proof object for a Checkout Leak Audit. It does not claim production merchant access or realized merchant revenue uplift.

## Proof snapshot

| Evidence | Status |
| --- | --- |
| 300,000-transaction merchant environment | SYNTHETIC |
| 93.10% seeded overall authorization | SYNTHETIC |
| 372 bp Germany PSP difference | OBSERVATIONAL SYNTHETIC; NOT CAUSAL |
| ~248 bp randomized treatment-control difference | RANDOMIZED SYNTHETIC |
| Stripe success / decline / 3DS execution | PROVIDER TEST |
| Authorization → capture → refund | PROVIDER TEST |
| Signed webhook verification | PROVIDER TEST |
| Production merchant audit | 0 / PENDING VALIDATION |

## Buyer-facing objects

- [Evidence room](EVIDENCE_ROOM.md)
- [Proof ledger](PROOF_LEDGER.md)
- [Methods](METHODS.md)
- [Results](RESULTS.md)
- [Commercial evidence pack](COMMERCIAL_EVIDENCE_PACK.md)
- [Report catalog](REPORT_CATALOG.md)
- [Decision memo](decision_memo.md)
- [Stripe test evidence](provider_sandboxes/evidence/)

## What a real engagement answers

1. Where are first-payment and renewal failures concentrated?
2. Which decline categories can be retried and which require customer action?
3. Which markets, devices, methods and authentication paths carry the most exposed value?
4. Are route differences robust after controlling for mix?
5. Which changes should be tested rather than simply deployed?
6. Are captures, refunds, payouts and webhook states operationally consistent?

Every buyer-facing number should carry a source, denominator, time window, filter, evidence class and limitation.