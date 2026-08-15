# Payment Performance Lab — Data Security & Client Confidentiality

Version: 1.0
Status: Public operating standard
Effective: 2026-08-16

This document states the controls the practice is prepared to operate. It does not claim certification that has not been obtained.

## Data perimeter

Default intake excludes full PAN, CVV/CVC, card-track data, authentication secrets, private keys, passwords, and unnecessary directly identifying customer data.

Preferred analytical identifiers are merchant-generated non-sensitive IDs, provider object IDs, tokenized/pseudonymized customer references, BIN/IIN-derived attributes where lawful and necessary, and normalized order/payment/attempt/event identifiers.

## Minimum controls for production engagements

- data minimization before transfer;
- written scope and permitted-use definition;
- least-privilege access;
- MFA on systems containing client material;
- encrypted transfer and encrypted storage;
- separate client workspaces where practical;
- access logging for production datasets;
- no public raw client data;
- retention period agreed before analysis;
- deletion confirmation at engagement close where required;
- NDA/DPA where applicable;
- subprocessor disclosure when relevant;
- incident escalation and client-notification procedure;
- reproducible analysis without copying sensitive data into public repositories.

## Public case studies

A production engagement is not automatically publishable. Public disclosure requires explicit permission for each category that will be surfaced, including client identity, alias, volume, value, market, findings, outcome metrics, testimonial, and implementation status.

Anonymization is not a substitute for permission when facts could reasonably re-identify the client.

## Provider and certification boundary

The practice does not claim PCI DSS certification, processor certification, scheme certification, or provider partnership unless a current verifiable basis exists. Sandbox execution is labeled `PROVIDER TEST`, never production capability certification.

## Incident register

Any material confidentiality, integrity, or availability incident affecting client evidence must be recorded with detection time, affected perimeter, containment action, client notification status, corrective action, and closure evidence.
