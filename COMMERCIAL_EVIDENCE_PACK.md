# Checkout Commercial Evidence Pack

## Offer

A fixed-scope payment-operations audit for online businesses using Stripe, Shopify Payments, or another provider with exportable transaction data.

## Deliverables

1. Leak map across available markets, devices, methods, 3DS paths, decline classes and retry sequences.
2. Money map ranking attempted value, failed value, refunds, fees and payout exceptions where fields exist.
3. Action queue assigning each finding an evidence level, owner, next test, guardrail and decision rule.
4. Executive brief with clean charts and tables.
5. Readout focused on decisions rather than dashboards.
6. Reproducible appendix with definitions, filters, QA and limitations where confidentiality permits.

## Evidence classes

- PRODUCTION CLIENT DATA — observed merchant records supplied for an engagement.
- RANDOMIZED CLIENT EVIDENCE — pre-specified client experiment.
- OBSERVATIONAL CLIENT EVIDENCE — diagnostic association, not causal by default.
- PROVIDER TEST — executed provider sandbox/test evidence.
- RANDOMIZED SYNTHETIC — seeded experimental simulation.
- SYNTHETIC — generated merchant environment.

## Current proof

The repository contains a reproducible 300,000-transaction synthetic merchant environment, a seeded 93.10% overall authorization rate, a 372 bp observational Germany PSP difference that is not described as causal uplift, a separate ~248 bp randomized synthetic treatment-control difference, and retained Stripe test evidence for authorization, declines, 3DS, capture/refund and signed webhook verification.

## Client data request

Preferred fields include payment/attempt ID, pseudonymous customer ID, timestamps, amount/currency, market, payment method, device/channel, provider/route, authentication state, authorization outcome, decline category, retry linkage, capture/refund status, fees and payout fields where in scope.

Do not request card numbers, CVCs, API keys or unnecessary secrets.

## QA standard

- unique-key and duplicate checks;
- timestamp/state validation;
- amount/currency validation;
- status normalization with an auditable mapping;
- missingness by segment;
- denominator validation for every rate;
- reconciliation of payment lifecycle populations where in scope;
- clean-run reproduction of headline tables.

## Claim boundary

This repository does not contain production merchant data, live-money processing, certification or verified merchant revenue uplift. Those claims remain unavailable until an actual client engagement supports them.