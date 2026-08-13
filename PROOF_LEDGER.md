# Checkout Proof Ledger

Every material public claim resolves to a source, date/window, code where applicable, reproducibility statement, limitation and validation status. The only public evidence labels are the canonical taxonomy below.

## Canonical evidence labels

`OFFICIAL SOURCE` · `REAL PUBLIC DATA` · `PROVIDER TEST` · `SYNTHETIC` · `RANDOMIZED SYNTHETIC` · `PRODUCTION CLIENT DATA` · `EXTERNAL REVIEW` · `INDEPENDENT REPRODUCTION` · `PENDING VALIDATION`

No alternative badge vocabulary is used. Internal implementation work is described in the source/code/status fields, not promoted into an evidence class.

## Ledger

| Claim | Number | Evidence label | Source | Date | Code | Reproducible? | Limitation | Status |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Generated merchant environment | 300,000 payment attempts | `SYNTHETIC` | `generate_data.py`; `RESULTS.md` | 2026-08-13 ledger check | `generate_data.py` | Yes, fixed seed 42 | Not production merchant behavior | Reproduced |
| Seeded overall authorization rate | 93.10% | `SYNTHETIC` | `RESULTS.md` | 2026-08-13 | `generate_data.py`; `analyze.py` | Yes | Encoded approval probabilities | Reproduced |
| Germany / PSP_A authorization | 93.03% | `SYNTHETIC` | `RESULTS.md` | 2026-08-13 | `generate_data.py`; `analyze.py` | Yes | Observational inside a synthetic environment | Reproduced |
| Germany / PSP_B authorization | 89.31% | `SYNTHETIC` | `RESULTS.md` | 2026-08-13 | `generate_data.py`; `analyze.py` | Yes | Observational inside a synthetic environment | Reproduced |
| Raw Germany PSP gap | 372 bps | `SYNTHETIC` | `RESULTS.md` | 2026-08-13 | `analyze.py` | Yes | Diagnostic association only; **not causal uplift** | Reproduced |
| Randomized routing treatment-control difference | ~248 bps | `RANDOMIZED SYNTHETIC` | `experiment.py`; `RESULTS.md` | 2026-08-13 | `experiment.py` | Yes, fixed seed 7; N=40,000 | Synthetic treatment probabilities; not merchant revenue uplift | Reproduced |
| Randomized 95% CI | ~191–305 bps | `RANDOMIZED SYNTHETIC` | `experiment.py`; `RESULTS.md` | 2026-08-13 | `experiment.py` | Yes | Interval applies only to the seeded synthetic experiment | Reproduced |
| Largest generated decline category | ~31% insufficient funds | `SYNTHETIC` | `RESULTS.md`; generator decline weights | 2026-08-13 | `generate_data.py` | Yes | Decline mix is designed, not learned from a merchant | Reproduced |
| Stripe PaymentIntent success path | 1 retained execution | `PROVIDER TEST` | `provider_sandboxes/evidence/stripe_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_sandbox.py` | Partly; test credentials required | Stripe test mode, not live money | Executed provider evidence |
| Stripe generic + insufficient-funds declines | 2 retained decline paths | `PROVIDER TEST` | `provider_sandboxes/evidence/stripe_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_sandbox.py` | Partly | Test cards and test-mode semantics | Executed provider evidence |
| Stripe 3DS path reached `requires_action` | 1 retained path | `PROVIDER TEST` | `provider_sandboxes/evidence/stripe_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_sandbox.py` | Partly | Test authentication flow only | Executed provider evidence |
| Manual authorization → capture → refund | 1 retained lifecycle | `PROVIDER TEST` | `provider_sandboxes/evidence/stripe_lifecycle_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_lifecycle.py` | Partly | Test-mode lifecycle, not settlement economics | Executed provider evidence |
| Signed Stripe webhook accepted after signature verification | 1 retained signed delivery | `PROVIDER TEST` | `provider_sandboxes/evidence/stripe_webhook_2026-08-10.md` | 2026-08-10 | `provider_sandboxes/stripe_webhook_server.py` | Partly | Does not prove production delivery reliability | Executed provider evidence |
| Persistent duplicate-event ledger | implemented and CI-tested | `PENDING VALIDATION` | tests; webhook implementation | 2026-08-13 | `provider_sandboxes/stripe_webhook_server.py`; tests | Yes locally/CI | Contract-tested; not a retained production/provider reliability result | Contract-tested |
| European payments context | H2 2025 + 2024 context | `OFFICIAL SOURCE` `REAL PUBLIC DATA` | `ECB_MARKET_CONTEXT.md`; ECB/EBA source material | source periods H2 2025 / 2024 | `ecb_market_snapshot.py` | Yes subject to source availability | Aggregate context, not transaction-level merchant evidence | Public-source evidence |
| Production merchant dataset | 0 disclosed | `PENDING VALIDATION` | repository claim boundary | 2026-08-13 | N/A | N/A | No production merchant access is claimed | Open zero |
| Validated merchant revenue uplift | 0 claims | `PENDING VALIDATION` | repository claim boundary | 2026-08-13 | N/A | N/A | Synthetic effects must never be sold as realized revenue | Open zero |
| Production client case study | 0 recorded | `PENDING VALIDATION` | buyer-room validation registry | 2026-08-13 | N/A | N/A | Requires client-approved real production evidence | Open zero |
| External methodological review | 0 recorded as completed review | `PENDING VALIDATION` | external review register | 2026-08-13 | N/A | N/A | Informal feedback is not a completed review | Open zero |
| Independent reproduction | 0 recorded | `PENDING VALIDATION` | reproduction register | 2026-08-13 | N/A | N/A | Outside rerun required | Open zero |

## Display rule

Every public chart, KPI and evidence card must show directly beneath the visual:

**SOURCE / N / WINDOW / FILTER / STATUS / LIMITATION / DOWNLOAD DATA**

The badge describes the evidence behind the number, not the aesthetics of the chart.

## What would falsify or materially weaken a checkout claim?

- A clean seeded rerun cannot reproduce the documented synthetic result.
- Payment-state mappings or denominators are wrong.
- A pre-specified randomized client test fails to reproduce an alleged routing/retry effect.
- A provider lifecycle path cannot be reproduced in the provider test environment under the documented conditions.
- A production client outcome cannot be traced to the disclosed cohort, window and analysis version.
- Fraud, disputes, processing cost or operational exceptions reverse a claimed net benefit.
- An `EXTERNAL REVIEW` or `INDEPENDENT REPRODUCTION` documents a material implementation or methodology error.
