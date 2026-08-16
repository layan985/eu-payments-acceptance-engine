"""Validate Checkout's public publication layer.

This is deliberately separate from reproduce.py. The core reproduction gate
regenerates the canonical synthetic merchant environment, routing experiment,
retry cohort and payment-state cohort. This publication gate verifies that the
buyer-facing chart library and downloadable sample fixtures have the promised
coverage and schemas.

It does not turn public-company synthetic reconstructions into production data,
and it does not count as independent reproduction.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "site_data"

EXPECTED_FAMILIES = {
    "Authorization": 5,
    "Declines": 4,
    "3DS / Authentication": 4,
    "Retries": 4,
    "Routing": 3,
    "Fraud / Acceptance": 3,
    "Payment State": 3,
    "Reconciliation": 3,
    "Economic Value": 2,
    "Experimental Effects": 2,
}

EXPECTED_SCHEMAS = {
    "retry_attempts_sample.csv": {
        "payment_intent_id", "attempt_number", "amount_eur", "status", "decline_reason", "authorized"
    },
    "payment_state_events_sample.csv": {"payment_id", "event_type", "delivery_number"},
    "reconciliation_exceptions_sample.csv": {"order_id", "amount_eur", "status", "age_days"},
    "booking_travel_reconstruction_sample.csv": {
        "order_id", "timing", "payout", "currency", "amount", "n_events",
        "preview_create_mismatch", "payment_refused", "cancelled", "refund_due",
        "vcc_status", "recon_issue"
    },
    "zalando_reconstruction_sample.csv": {
        "order_id", "market", "method", "amount", "reference_mismatch", "return_flag",
        "refund_delay_days", "payout_mode", "recon_issue", "checkout_completed"
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_chart_manifest() -> None:
    path = DATA / "chart_manifest.csv"
    rows = read_rows(path)
    required = {"chart_id", "category", "title", "label", "value", "unit", "evidence", "note"}
    if not rows or not required.issubset(rows[0]):
        raise SystemExit("PUBLICATION DRIFT: chart_manifest.csv schema mismatch")

    chart_family = {}
    for row in rows:
        chart_id = row["chart_id"].strip()
        category = row["category"].strip()
        if chart_id in chart_family and chart_family[chart_id] != category:
            raise SystemExit(f"PUBLICATION DRIFT: {chart_id} appears in multiple families")
        chart_family[chart_id] = category
        if not row["evidence"].strip():
            raise SystemExit(f"PUBLICATION DRIFT: {chart_id} has an empty evidence label")

    counts = Counter(chart_family.values())
    if dict(counts) != EXPECTED_FAMILIES:
        raise SystemExit(f"PUBLICATION DRIFT: expected {EXPECTED_FAMILIES}, got {dict(counts)}")
    if len(chart_family) != 33:
        raise SystemExit(f"PUBLICATION DRIFT: expected 33 unique charts, got {len(chart_family)}")


def validate_samples() -> None:
    for filename, expected in EXPECTED_SCHEMAS.items():
        path = DATA / filename
        rows = read_rows(path)
        if not rows:
            raise SystemExit(f"PUBLICATION DRIFT: {filename} is empty")
        actual = set(rows[0])
        if actual != expected:
            raise SystemExit(f"PUBLICATION DRIFT: {filename} schema {sorted(actual)} != {sorted(expected)}")
        if len(rows) < 300:
            raise SystemExit(f"PUBLICATION DRIFT: {filename} exposes too small an inspectable slice ({len(rows)} rows)")


def main() -> None:
    validate_chart_manifest()
    validate_samples()
    print("CHECKOUT PUBLICATION VERIFICATION: PASS")
    print("33 chart objects across 10 promised analytical families are present and evidence-labelled.")
    print("Five inspectable synthetic/sample datasets pass schema and minimum-slice checks.")
    print("Boundary: this verifies publication integrity; it is not external review or independent reproduction.")


if __name__ == "__main__":
    main()
