# Standards, Provenance & Corrections

<div class="meta-line"><span>MAINTAINED RECORD</span><span>VERSIONED</span><span>CORRECTION-AWARE</span></div>

Checkout is maintained as a versioned technical and commercial record rather than a static marketing site.

## Current record

| Field | Current value |
|---|---|
| Last updated | **17 August 2026** |
| Public methodology | **Payment Performance Audit Methodology v1.0** |
| Security standard | **Data Security & Client Confidentiality v1.0** |
| Outcome validation protocol | **v1.0** |
| Canonical repository | `layan985/eu-payments-acceptance-engine` |
| Canonical public commit at this update | `15c0e974e8ab0711400568580d0c3457f42e2506` plus subsequent site-content updates |
| Reproduction command | `python reproduce.py` |
| Publication verification | `python reproduce_publication.py` |

The footer/site may point to a newer commit as maintenance continues. Git history is the authoritative change record.

## Source policy

Every material public claim should resolve to a source and evidence class. The source may be:

- official/public institutional material;
- real public company material;
- reproducible synthetic data;
- randomized synthetic experiments;
- executed provider-test records;
- permission-controlled production client data;
- external review;
- independent reproduction.

Public-source merchant investigations do not imply that the merchant is a client.

## Claim labels

Checkout uses explicit evidence classes so that a reader can distinguish what kind of proof supports a number:

`OFFICIAL SOURCE` · `REAL PUBLIC DATA` · `PROVIDER TEST` · `SYNTHETIC` · `RANDOMIZED SYNTHETIC` · `PRODUCTION CLIENT DATA` · `EXTERNAL REVIEW` · `INDEPENDENT REPRODUCTION` · `FOUNDER PRODUCED` · `PENDING VALIDATION`

A stronger-looking label is never substituted for the actual evidence class.

## Reproduction policy

The canonical public reproduction command regenerates the seeded synthetic merchant environment, recomputes headline metrics, reruns the randomized experiment, rebuilds retry/payment-state artifacts and runs the test suite.

Independent reproduction remains a separate evidence class from self-run CI.

## Correction policy

A material correction should be visible rather than silently rewritten. Corrections should identify:

1. the affected claim/artifact;
2. what was wrong or incomplete;
3. the corrected value/text/method;
4. the reason for the change;
5. whether downstream decisions or reports are affected;
6. the commit/change record containing the correction.

## Versioning policy

Methodology, security, validation and public evidence objects should be versioned when a change materially affects interpretation. Cosmetic edits do not require a methodology version change; denominator definitions, evidence rules, experiment logic, security perimeter or outcome-validation logic do.

## Production confidentiality

Versioning does not override client confidentiality. Private production evidence may be retained in a permission-controlled registry while the public site exposes only allowed aggregate facts.

[Canonical repository](https://github.com/layan985/eu-payments-acceptance-engine) · [Methodology](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/institution/AUDIT_METHODOLOGY.md) · [Security standard](/security)