# Checkout Audit Intake Contract

Version: 1.0
Effective: 2026-08-17

The public Request Audit form collects **commercial scoping metadata only**. It is not a production-data upload channel.

## Public intake fields

Required:

- company;
- work email;
- role / function;
- approximate monthly payment attempts;
- markets;
- PSPs / acquirers / payment methods in scope;
- decision or problem the buyer needs resolved;
- current data availability.

Optional:

- website;
- preferred contact name;
- security / confidentiality note;
- timing constraint.

## Never submit through the public form

Do not submit or paste:

- PAN / card numbers;
- CVV / CVC;
- card-track data;
- authentication secrets;
- API keys, passwords or private keys;
- raw payment exports;
- customer PII;
- confidential production datasets;
- files or database extracts.

Production data transfer is agreed separately after the engagement perimeter and security expectations are confirmed.

## Intake processing

The public website may use a form-delivery processor to forward scoping submissions to the audit inbox. That processor is a transport layer only and does not change Checkout's production-data perimeter. The website does not present the intake form as a secure production-data exchange.

## Qualification output

A qualified request should resolve to:

`buyer → decision question → data grain → payment perimeter → feasibility → security needs → scope → next action`

No audit is accepted merely because the form was submitted. Scope and data feasibility are confirmed before production data is requested.
