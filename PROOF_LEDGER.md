# Proof Ledger

Every material claim in this repository should resolve to a source, a date, code where applicable, a reproducibility statement, a limitation, and a validation status. A number without that trail is not a public claim.

## Evidence badges

`REAL PUBLIC DATA` — published by an external public institution.  
`CLIENT DATA` — real client data, only when disclosure is explicitly approved.  
`PROVIDER TEST` — executed against a provider-controlled test environment.  
`SYNTHETIC` — generated merchant or transaction data.  
`RANDOMIZED SYNTHETIC` — a deliberately randomized synthetic experiment.  
`EXTERNALLY VERIFIED` — independently verifiable external record or rerun.  
`FOUNDER PRODUCED` — implementation, analysis, test, or artifact produced inside this project.  
`PENDING VALIDATION` — not yet independently verified or not yet available.

## Ledger

| Claim | Number | Evidence type | Source | Date | Code | Reproducible? | Limitation | Status |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Synthetic merchant environment size | 300,000 transactions | `SYNTHETIC` `FOUNDER PRODUCED` | `generate_data.py`; `RESULTS.md` | 2026-08-13 ledger check | `generate_data.py` | Yes, fixed seed 42 | Not production merchant behavior | Reproduced |
| Seeded overall authorization rate | 93.10% | `SYNTHETIC` | `RESULTS.md` | 2026-08-13 ledger check | `generate_data.py`; `analyze.py` | Yes | Generated from encoded approval probabilities | Reproduced |
| Germany / PSP_A authorization | 93.03% | `SYNTHETIC` | `RESULTS.md` | 2026-08-13 ledger check | `generate_data.py`; `analyze.py` | Yes | Observational within a synthetic environment | Reproduced |
| Germany / PSP_B authorization | 89.31% | `SYNTHETIC` | `RESULTS.md` | 2026-08-13 ledger check | `generate_data.py`; `analyze.py` | Yes | Observational within a synthetic environment | Reproduced |
| Raw Germany PSP gap | 372 bps | `SYNTHETIC` | `RESULTS.md` | 2026-08-13 ledger check | `analyze.py` | Yes | **Not causal uplift**; use only as a diagnostic gap | Reproduced |
| Randomized routing treatment-control difference | ~248 bps | `RANDOMIZED SYNTHETIC` | `experiment.py`; `RESULTS.md` | 2026-08-13 ledger check | `experiment.py` | Yes, fixed seed 7; N=40,000 | Synthetic treatment probabilities; not merchant revenue uplift | Reproduced |
| 95% CI for randomized difference | ~191–305 bps | `RANDOMIZED SYNTHETIC` | `experiment.py`; `RESULTS.md` | 2026-08-13 ledger check | `experiment.py` | Yes | Confidence interval applies to the seeded synthetic experiment only | Reproduced |
| Largest decline category | ~31% insufficient funds | `SYNTHETIC` | `RESULTS.md`; generator decline weights | 2026-08-13 ledger check | `generate_data.py` | Yes | Decline mix is designed, not learned from a merchant | Reproduced |
| Stripe PaymentIntent success path executed | 1 retained execution record | `PROVIDER TEST` `FOUNDER PRODUCED` | `provider_sandboxes/evidence/stripe_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_sandbox.py` | Partly; requires developer test credentials | Stripe test mode, not live money | Executed provider evidence |
| Stripe deliberate generic + insufficient-funds declines executed | 2 retained decline paths | `PROVIDER TEST` `FOUNDER PRODUCED` | `provider_sandboxes/evidence/stripe_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_sandbox.py` | Partly; requires developer test credentials | Test cards and test-mode semantics | Executed provider evidence |
| Stripe 3DS path reached `requires_action` | 1 retained 3DS path | `PROVIDER TEST` `FOUNDER PRODUCED` | `provider_sandboxes/evidence/stripe_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_sandbox.py` | Partly; requires developer test credentials | Test authentication flow only | Executed provider evidence |
| Manual authorization → capture → refund executed | 1 retained lifecycle | `PROVIDER TEST` `FOUNDER PRODUCED` | `provider_sandboxes/evidence/stripe_lifecycle_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_lifecycle.py` | Partly; requires developer test credentials | Test-mode lifecycle, not settlement economics | Executed provider evidence |
| Signed Stripe webhook accepted after signature verification | 1 retained signed delivery | `PROVIDER TEST` `FOUNDER PRODUCED` | `provider_sandboxes/evidence/stripe_webhook_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_webhook_server.py` | Partly; requires local webhook secret + Stripe CLI | Does not prove production delivery reliability | Executed provider evidence |
| Persistent duplicate-event ledger exists and is tested | implemented; CI-tested | `FOUNDER PRODUCED` | `README.md`; tests | 2026-08-13 ledger check | `provider_sandboxes/stripe_webhook_server.py`; tests | Yes in local/CI environment | Contract-tested; do not label as live provider evidence until a retained run exists | Contract-tested |
| European payments baseline comes from official ECB/EBA material | H2 2025 + 2024 context | `REAL PUBLIC DATA` | `ECB_MARKET_CONTEXT.md`; `ecb_market_snapshot.py` | source periods H2 2025 / 2024 | `ecb_market_snapshot.py` | Yes subject to source availability | Aggregate market context, not transaction-level merchant evidence | Public-source evidence |
| Real production merchant dataset | 0 disclosed | `PENDING VALIDATION` | repository claim boundary | 2026-08-13 | N/A | N/A | No production merchant access is claimed | Open zero |
| Real merchant revenue uplift | 0 validated claims | `PENDING VALIDATION` | repository claim boundary | 2026-08-13 | N/A | N/A | Synthetic effects must never be sold as realized revenue | Open zero |
| Independent merchant case study | 0 | `PENDING VALIDATION` | `ADOPTION.md`; `EXTERNAL_REVIEW.md` | 2026-08-13 | N/A | N/A | First case should be anonymized and client-approved | Open zero |

## Display rule

Any public chart or KPI derived from this repository should show, directly beneath the visual:

**SOURCE / N / WINDOW / FILTER / STATUS / LIMITATION / DOWNLOAD DATA**

The badge must describe the evidence behind the number, not the aesthetic of the chart.
