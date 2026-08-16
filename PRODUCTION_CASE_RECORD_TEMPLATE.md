# Production Case Record Template

Use this for every real Checkout engagement. A public case record is created only to the extent permitted by the client agreement. Private working evidence, raw transaction data, processor credentials, personal data and restricted commercial terms never belong in this repository.

## 1. Engagement identity

- Audit ID:
- Client disclosure: named / anonymized / fully confidential
- Sector:
- Region / markets:
- Engagement dates:
- Payment perimeter: PSPs, acquirers, methods, currencies, channels
- Approximate transaction-volume band permitted for publication:
- Public permission status:

## 2. Decision question

State the operational question in one sentence. Examples: whether a checkout loss is concentrated in a specific authentication flow, whether a raw PSP approval gap survives mix adjustment, or whether a retry policy should be changed.

## 3. Baseline

| Field | Record |
| --- | --- |
| Baseline window | |
| Metric | |
| Numerator | |
| Denominator | |
| Baseline value | |
| Data completeness | |
| Known exclusions | |
| Evidence class | PRODUCTION CLIENT DATA |

## 4. Issue observed

Document the exact failure pattern and the segments in which it appears. Distinguish measured facts from hypotheses. Do not translate an observed gap into recoverable revenue without an explicit economic-value method and uncertainty range.

## 5. Evidence

For every material finding record:

`CLAIM → NUMBER → EVIDENCE TYPE → SOURCE/QUERY → DATE/WINDOW → CODE → REPRODUCIBLE? → LIMITATION → STATUS`

Permitted status language includes:

- LOSS OBSERVED
- OPPORTUNITY ESTIMATED
- EXPERIMENT VALIDATED
- IMPLEMENTED
- FINANCIALLY REALIZED

## 6. Intervention

- Recommended action:
- Decision class: FIX / INVESTIGATE / TEST / DO NOT TOUCH
- Identification status before change:
- Implementation owner:
- Implementation date:
- Fraud / cost / customer-friction guardrails:
- Rollback condition:

## 7. Experiment or validation design

- Design: randomized / phased / matched / interrupted time series / observational follow-up / not testable
- Primary metric:
- Guardrail metrics:
- Comparator:
- Measurement window:
- Pre-specified exclusions:
- Minimum detectable effect or decision threshold, where relevant:
- Confounding risks:

## 8. Outcome

| Field | Record |
| --- | --- |
| Observed value | |
| Absolute change | |
| Relative change | |
| Causal estimate, if justified | |
| Uncertainty interval | |
| Economic-value method | |
| Realized financial value | Only if traceable to settlement/accounting evidence |
| Client acceptance | |
| Outcome state | |

## 9. Limitations

Record missing data, denominator instability, processor taxonomy limitations, selection, seasonality, concurrent changes, low power, external-validity limits, or any reason the finding should not be generalized.

## 10. Permission-safe public record

Only publish fields explicitly covered by the agreed publication permission. The public record should normally contain, where permitted:

- anonymized sector and region;
- bounded problem statement;
- evidence architecture;
- selected permission-safe figures or ranges;
- intervention class;
- validation design;
- outcome state;
- limitations;
- evidence class;
- date and version.

It should not contain client identity, raw data, secrets, restricted processor terms, exact commercial pricing, or unpublished performance metrics unless separately authorized.

## Suggested contract language for case-record permission

> The Client permits the Provider to retain an internal engagement record for quality assurance and, only where the Client separately approves the proposed disclosure, to publish an anonymized case record describing the problem class, method, evidence type, intervention class, validation design, outcome state and limitations. No client name, raw data, confidential metric, transaction-level record, commercial term or identifying detail will be published without explicit written approval. Client review of the proposed public record is required before publication.

This clause is a working commercial template, not legal advice. Adapt it to the governing contract and jurisdiction.
