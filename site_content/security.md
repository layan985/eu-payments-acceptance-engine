# Security & Confidentiality

<div class="meta-line"><span>PUBLIC OPERATING STANDARD</span><span>FOUNDER-LED ACCESS</span><span>DATA MINIMIZATION</span><span>NO UNCLAIMED CERTIFICATIONS</span></div>

Checkout is designed so a payment-acceptance audit can usually be performed without receiving raw card credentials or unnecessary customer identity data.

## Who handles production data

Checkout is operated by **Layan Aloreidi**. By default, Layan Aloreidi is the engagement lead, primary analyst and production-data handler. A buyer is not silently handing data to an undisclosed team.

The written engagement identifies the contracting identity, approved access perimeter, permitted use, transfer path, retention/deletion position and incident contact before any production data is transferred. Additional people do not receive access by default; any additional approved access must be disclosed and bounded inside the engagement.

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

### Public-form processor

The current public request form uses **FormSubmit** as an email-forwarding transport. FormSubmit states that submissions may be retained for **30 days** in its submission archive. For that reason, the form is deliberately restricted to company/contact/scoping information and accepts **no files or production payment records**.

This is a temporary public-intake dependency, not part of the production-data path. Replacing it with a first-party intake endpoint and domain mailbox is an active commercial-infrastructure improvement; until that migration is complete, the processor boundary remains explicitly disclosed rather than hidden.

[FormSubmit documentation](https://formsubmit.co/documentation)

## Retention

The production-data retention period is agreed before analysis. Data should not be kept indefinitely merely because an audit has finished.

Public-form scoping submissions are subject to the form processor's separate retention boundary described above.

## Deletion

Where required by the engagement, production client data is deleted at close and confirmed. Any retained derived artifact must remain within the agreed permitted-use boundary.

## Confidentiality

NDA/DPA terms are used where applicable. Client material is not turned into public examples by default. Confidentiality does not permit fabricated anonymized outcomes: if an engagement cannot be disclosed, the public record stays aggregate or withheld.

## Public-case permission

A paid engagement is **not automatically a publishable case study**. Permission is treated separately for client identity, alias, market, volume, attempted value, findings, outcome metrics, testimonial wording and implementation status.

Anonymization is not treated as a substitute for permission where the underlying facts could reasonably identify the client.

## Incident ownership

A material confidentiality, integrity or availability incident is owned by the engagement lead named in the written scope. The record includes detection time, affected perimeter, containment action, notification status, corrective action and closure evidence.

Use the [Request Audit / Contact page](/contact) and select **Security / confidentiality** for the current public contact route.

## Certification boundary

Checkout does **not** claim PCI DSS certification, processor certification, scheme certification or provider partnership unless a current verifiable basis exists. Stripe sandbox execution remains labelled `PROVIDER TEST`, not production certification.

[Canonical security standard](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/institution/SECURITY_CONFIDENTIALITY.md) · [Public intake contract](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/institution/AUDIT_INTAKE_CONTRACT.md)