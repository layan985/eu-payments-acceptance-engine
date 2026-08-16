"""Validate Checkout's public publication layer.

This check is intentionally separate from reproduce.py. The canonical gate already
regenerates the 300,000-attempt environment, routing experiment, retry cohort and
payment-state cohort. This publication gate verifies that the buyer-facing chart
manifest preserves the promised analytical coverage and that generated research
artifacts exist after reproduction.

Passing this check is not external review or independent reproduction.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "site_data"
GENERATED = ROOT / "output" / "research_artifacts"

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


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_chart_manifest() -> None:
    rows = read_rows(DATA / "chart_manifest.csv")
    required = {"chart_id", "category", "title", "label", "value", "unit", "evidence", "note"}
    if not rows or not required.issubset(rows[0]):
        raise SystemExit("PUBLICATION DRIFT: chart_manifest.csv schema mismatch")

    chart_family: dict[str, str] = {}
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


def validate_generated_research() -> None:
    required = {
        "retry_attempts.csv",
        "retry_metrics.json",
        "payment_state_events.csv",
        "payment_state_metrics.json",
        "manifest.json",
    }
    missing = sorted(name for name in required if not (GENERATED / name).exists())
    if missing:
        raise SystemExit(f"PUBLICATION DRIFT: reproduction did not generate {missing}")


def main() -> None:
    validate_chart_manifest()
    validate_generated_research()
    print("CHECKOUT PUBLICATION VERIFICATION: PASS")
    print("33 chart objects across 10 promised analytical families are present and evidence-labelled.")
    print("Canonical retry and payment-state research artifacts were regenerated before this check.")
    print("Boundary: publication integrity is not external review or independent reproduction.")


if __name__ == "__main__":
    main()
