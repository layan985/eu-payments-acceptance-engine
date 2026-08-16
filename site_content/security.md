# Security & Confidentiality

<div class="meta-line"><span>PUBLIC OPERATING STANDARD</span><span>DATA MINIMIZATION</span><span>NO UNCLAIMED CERTIFICATIONS</span></div>

Checkout is designed so a payment-acceptance audit can usually be performed without receiving raw card credentials or unnecessary customer identity data.

## Data accepted

Typical analytical inputs are limited to the fields required by the agreed decision question:

- merchant-generated payment, order, attempt and event identifiers;
- provider object IDs;
- timestamps, amount and currency;
- market, channel and payment method;
- route / PSP / acquirer labels where relevant;
- authorization result and normalized decline class;
- 3DS / authentication state without authentication secrets;
- retry sequence;
- capture, refund, reversal, dispute, settlement and payout state where in scope;
- provider fees and reconciliation identifiers where necessary;
- pseudonymized customer references or BIN/IIN-derived attributes only where lawful and analytically necessary.

## Data never requested by default

Checkout's default analytical perimeter excludes:

**full PAN · CVV/CVC · card-track data · authentication secrets · private keys · passwords · unnecessary direct customer identifiers.**

If a decision can be answered without a sensitive field, the field should not be transferred.

## Storage

Production client material is handled under a written scope and permitted-use definition. The operating standard requires encrypted storage, client separation where practical and no copying of raw client data into public repositories.

## Access

Access is limited to the minimum required for the engagement. Systems containing production client material are expected to use MFA and least-privilege access. Access logging is required for production datasets where applicable.

## Transfer

The public Request Audit form is for commercial scoping metadata only. **Do not upload or paste payment records into the public form.** Production-data transfer is agreed separately after scope and security expectations are confirmed, using an encrypted transfer path appropriate to the engagement.

## Retention

The retention period is agreed before analysis. Data should not be kept indefinitely merely because an audit has finished.

## Deletion

Where required by the engagement, deletion is performed at close and confirmed. Any retained derived artifact must remain within the agreed permitted-use boundary.

## Confidentiality

NDA/DPA terms are used where applicable. Client material is not turned into public examples by default. Confidentiality does not permit fabricated anonymized outcomes: if an engagement cannot be disclosed, the public record stays aggregate or withheld.

## Public-case permission

A paid engagement is **not automatically a publishable case study**. Permission is treated separately for client identity, alias, market, volume, attempted value, findings, outcome metrics, testimonial wording and implementation status.

Anonymization is not treated as a substitute for permission where the underlying facts could reasonably identify the client.

## Incident contact

Use the [Request Audit / Contact page](/contact) and select **Security / confidentiality**. A material confidentiality, integrity or availability incident is recorded with detection time, affected perimeter, containment action, notification status, corrective action and closure evidence.

## Certification boundary

Checkout does **not** claim PCI DSS certification, processor certification, scheme certification or provider partnership unless a current verifiable basis exists. Stripe sandbox execution remains labelled `PROVIDER TEST`, not production certification.

[Canonical security standard](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/institution/SECURITY_CONFIDENTIALITY.md)