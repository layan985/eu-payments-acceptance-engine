# PP-AUD-011 — First Production Merchant Audit Intake

Status: `PENDING VALIDATION`
Purpose: canonical intake for the first production merchant audit.

## Minimum data contract

Preferred grain: one row per payment attempt, plus event tables where available.

### Attempt table

Required where available:

- merchant payment/order ID
- payment attempt ID
- provider payment ID
- timestamp and timezone
- amount and currency
- merchant country / customer country
- payment method
- card scheme and non-sensitive card attributes where lawful
- issuer country / BIN-derived grouping where lawful
- PSP / acquirer / MID / route
- 3DS/authentication status and exemption path
- authorization status
- raw provider decline code and message
- capture state
- refund state
- recurring/stored-credential indicator
- device/channel
- retry sequence identifier

### Risk and economics tables

Where available:

- fraud decision and reason family
- chargeback/dispute state
- fraud loss
- processor fees
- scheme/network fees
- FX/cross-border fees
- refund/chargeback fees
- settlement/payout records

### Event table

- event ID
- event type
- provider object ID
- event-created timestamp
- received timestamp
- processed timestamp
- signature-valid flag
- idempotency/duplicate flag
- resulting internal state

## Day 0 QA gates

Analysis does not begin until these are measured:

1. row-count reconciliation;
2. duplicate attempt IDs;
3. missing-state rates;
4. amount/currency validity;
5. timestamp ordering;
6. payment/order/provider ID join coverage;
7. terminal-state consistency;
8. provider-code coverage;
9. route/PSP/method/country coverage;
10. capture/refund/settlement join coverage where supplied.

## Standard audit outputs

1. Executive Decision Memo
2. Payment Data QA
3. Metric Dictionary
4. Authorization Map
5. Failed-Value Waterfall
6. Decline Forensics
7. 3DS Funnel
8. Routing Analysis
9. Retry Analysis
10. Fraud Guardrails
11. Cost Economics
12. Reconciliation Exceptions
13. Experiment Designs
14. 30-Day Action Register
15. Technical Appendix
16. SQL/Python analysis package
17. Claim Ledger
18. Limitations Register
19. Final Outcome Register

## Finding classification

Every recommendation is exactly one of:

- `FIX`
- `INVESTIGATE`
- `TEST`
- `DO NOT TOUCH`

Every effect is exactly one strongest state from:

- observed
- mix-adjusted
- experimentally estimated
- implemented
- financially realized

## Publication boundary

This file is a production-audit specification, not evidence that PP-AUD-011 has occurred. The case becomes `PRODUCTION CLIENT DATA` only after an actual merchant dataset has been received and analyzed under an engagement record.
