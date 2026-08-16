"""Generate the public research artifacts used by Checkout reports 002 and 003.

Everything generated here is synthetic. The script exists so published retry and
payment-state results are inspectable and reproducible without provider keys.
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "output" / "research_artifacts"


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def retry_artifact(seed: int = 20260816, n: int = 30_000) -> dict:
    rng = random.Random(seed)
    attempts: list[dict] = []
    intents: list[dict] = []
    reasons = ["insufficient_funds", "do_not_honor", "authentication_failed", "invalid_account", "lost_or_stolen"]
    weights = [0.31, 0.27, 0.22, 0.12, 0.08]

    for i in range(n):
        payment_id = f"pi_{i:07d}"
        customer_id = f"cust_{i:07d}"
        amount = round(min(rng.lognormvariate(3.55, 0.75), 1200), 2)
        record = {"payment_intent_id": payment_id, "amount_eur": amount, "resolved": False, "attempts": 0}

        def add(attempt_no: int, ok: bool, reason: str = "") -> None:
            attempts.append({
                "payment_intent_id": payment_id,
                "customer_id": customer_id,
                "attempt_no": attempt_no,
                "amount_eur": amount,
                "authorized": int(ok),
                "decline_reason": reason,
                "event_time_min": i * 5 + attempt_no - 1,
            })
            record["attempts"] += 1

        initial_ok = rng.random() < 0.90
        if initial_ok:
            add(1, True)
            record["resolved"] = True
        else:
            reason = rng.choices(reasons, weights=weights)[0]
            add(1, False, reason)
            soft = reason in {"insufficient_funds", "do_not_honor", "authentication_failed"}
            if rng.random() < (0.62 if soft else 0.08):
                second_ok = rng.random() < (0.38 if soft else 0.04)
                add(2, second_ok, "" if second_ok else reason)
                if second_ok:
                    record["resolved"] = True
                elif soft and rng.random() < 0.22:
                    third_ok = rng.random() < 0.27
                    add(3, third_ok, "" if third_ok else reason)
                    record["resolved"] = third_ok
        intents.append(record)

    attempted = len(attempts)
    metrics = {
        "seed": seed,
        "payment_intents": n,
        "attempts": attempted,
        "attempt_authorization_rate": sum(row["authorized"] for row in attempts) / attempted,
        "intent_resolution_rate": sum(bool(row["resolved"]) for row in intents) / n,
        "economic_value_resolution_rate": sum(row["amount_eur"] for row in intents if row["resolved"]) / sum(row["amount_eur"] for row in intents),
        "retry_share_of_attempts": (attempted - n) / attempted,
        "multi_attempt_intents": sum(row["attempts"] > 1 for row in intents),
    }
    write_csv(OUT / "retry_attempts.csv", attempts)
    (OUT / "retry_metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


def state_artifact(seed: int = 31082026, n: int = 20_000) -> dict:
    rng = random.Random(seed)
    events: list[dict] = []
    ledger: list[dict] = []
    counter = 0

    for i in range(n):
        payment_id = f"pay_{i:07d}"
        amount = round(min(rng.lognormvariate(3.6, 0.7), 1000), 2)
        sequence = [("created", amount)]
        authorized = rng.random() < 0.925
        if authorized:
            sequence.append(("authorized", amount))
            captured = rng.random() < 0.974
            if captured:
                captured_amount = amount if rng.random() > 0.012 else round(amount * rng.uniform(0.35, 0.85), 2)
                sequence.append(("captured", captured_amount))
                if rng.random() < 0.082:
                    sequence.append(("refunded", round(captured_amount * (1 if rng.random() < 0.78 else rng.uniform(0.2, 0.8)), 2)))
                if rng.random() < 0.004:
                    sequence.append(("disputed", captured_amount))
            else:
                sequence.append(("authorization_reversed", amount))
        else:
            sequence.append(("declined", amount))

        for seq_no, (state, value) in enumerate(sequence, start=1):
            counter += 1
            event_id = f"evt_{counter:09d}"
            events.append({"event_id": event_id, "payment_intent_id": payment_id, "sequence": seq_no, "state": state, "amount_eur": value, "duplicate_of": "", "delivery_order_anomaly": 0})
            if rng.random() < 0.018:
                counter += 1
                events.append({"event_id": f"evt_{counter:09d}", "payment_intent_id": payment_id, "sequence": seq_no, "state": state, "amount_eur": value, "duplicate_of": event_id, "delivery_order_anomaly": 0})

        ledger.append({
            "payment_intent_id": payment_id,
            "amount_eur": amount,
            "captured_amount_eur": next((value for state, value in sequence if state == "captured"), 0),
            "refunded_amount_eur": next((value for state, value in sequence if state == "refunded"), 0),
        })

    shuffled_indices = list(range(len(events)))
    rng.shuffle(shuffled_indices)
    for index in shuffled_indices[: int(len(events) * 0.008)]:
        events[index]["delivery_order_anomaly"] = 1

    naive_captures = sum(row["state"] == "captured" for row in events)
    unique_captures = sum(row["captured_amount_eur"] > 0 for row in ledger)
    naive_refunds = sum(row["state"] == "refunded" for row in events)
    unique_refunds = sum(row["refunded_amount_eur"] > 0 for row in ledger)
    duplicate_events = sum(bool(row["duplicate_of"]) for row in events)
    metrics = {
        "seed": seed,
        "payment_intents": n,
        "delivered_events": len(events),
        "duplicate_events": duplicate_events,
        "duplicate_event_rate": duplicate_events / len(events),
        "naive_captured_event_count": naive_captures,
        "state_aware_unique_captures": unique_captures,
        "capture_count_overstatement_pct": naive_captures / unique_captures - 1,
        "naive_refund_event_count": naive_refunds,
        "state_aware_unique_refunds": unique_refunds,
        "refund_count_overstatement_pct": naive_refunds / unique_refunds - 1,
        "out_of_order_flagged_events": sum(row["delivery_order_anomaly"] for row in events),
    }
    write_csv(OUT / "payment_state_events.csv", events)
    (OUT / "payment_state_metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


def generate_all() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    result = {"retry": retry_artifact(), "payment_state": state_artifact()}
    (OUT / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(generate_all(), indent=2))
