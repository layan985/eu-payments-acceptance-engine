# Payment State Integrity

<div class="meta-line"><span>SYNTHETIC</span><span>PROVIDER TEST LINKED</span><span>UPDATED 2026-08-16</span></div>

## Core finding

Authorization is not capture. Capture is not settlement. A webhook delivery is not a unique economic event.

| Object | Seeded result | Evidence class |
|---|---:|---|
| Payment intents | 20,000 | SYNTHETIC |
| Delivered events | 61,134 | SYNTHETIC |
| Duplicate events | 1,036 / 1.69% | SYNTHETIC |
| Unique captures | 18,019 | SYNTHETIC |
| Naive capture events | 18,350 | SYNTHETIC |
| Capture-count overstatement | 1.84% | SYNTHETIC |
| Refund-count overstatement | 1.27% | SYNTHETIC |

<div class="bar-chart" data-title="Naive event counting overstates economic state">
<div><b>Capture-count overstatement</b><i style="--v:84%"></i><strong>1.84%</strong></div>
<div><b>Refund-count overstatement</b><i style="--v:58%"></i><strong>1.27%</strong></div>
</div>

## Inspectable event rows

| event_id | payment_intent_id | sequence | state | duplicate_of |
|---|---|---:|---|---|
| evt_000000050 | pay_0000016 | 1 | created | — |
| evt_000000051 | pay_0000016 | 2 | authorized | — |
| evt_000000052 | pay_0000016 | 3 | captured | — |
| evt_000000053 | pay_0000016 | 3 | captured | evt_000000052 |
| evt_000000063 | pay_0000020 | 1 | created | — |
| evt_000000064 | pay_0000020 | 1 | created | evt_000000063 |

**Inspect:** [research_artifacts.py](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/research_artifacts.py) · [reproduce.py](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/reproduce.py)

## Why event identity matters

The research cohort keys economic state to `payment_intent_id` while each delivery has its own `event_id`. A repeated delivery is retained as delivery evidence but must not become a second capture or refund.

<div class="state-line"><span>CREATED</span><b>→</b><span>AUTHORIZED</span><b>→</b><span>CAPTURED</span><b>→</b><span>REFUNDED</span><i>branches: DECLINED · REVERSED · DISPUTED</i></div>

## Provider-test connection

The public technical record separately retains real Stripe **test-mode** evidence for:

- manual authorization reaching `requires_capture`;
- capture reaching `succeeded`;
- a refund request accepted against the same PaymentIntent;
- a Stripe CLI test webhook whose signature was accepted by the local verifier.

The persistent event-ID ledger is implemented and contract-tested. The retained execution record does **not** claim that a real duplicate Stripe delivery was observed.

**Provider records:** [authorization → capture → refund](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/provider_sandboxes/evidence/stripe_lifecycle_2026-08-10.md) · [signed webhook](https://github.com/layan985/eu-payments-acceptance-engine/blob/main/provider_sandboxes/evidence/stripe_webhook_2026-08-10.md)

## Control architecture

| Control | Requirement |
|---|---|
| Object identity | stable order, payment-intent, attempt, provider-object and event IDs |
| Transition validity | quarantine impossible regressions or unexpected state transitions |
| Idempotency | acknowledge duplicate event ID without reprocessing |
| Economic state | track captured, refunded and disputed amounts as ledger values |
| Reconciliation | compare internal state, provider state and settlement/payout records |

## Decision memo

**FIX** any KPI counting webhook deliveries as economic outcomes. **INVESTIGATE** capture/refund mismatches and delayed/out-of-order events. **TEST** recovery under duplicate and delayed delivery. **DO NOT TOUCH** revenue reporting until object identity and state transitions are trustworthy.

## Reproduce

```bash
python reproduce.py
```

## Limitations

The synthetic state machine omits scheme clearing, settlement batches, full chargeback lifecycle, split tender, FX, marketplace sub-ledgers and many provider-specific states. It demonstrates the accounting/control failure mode rather than a complete payments ledger.