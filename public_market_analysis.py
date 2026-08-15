from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parent
MARKET = ROOT / "data" / "public" / "eu_payments_market_benchmark_h2_2025.csv"
FRAUD = ROOT / "data" / "public" / "eu_payments_fraud_benchmark_2024.csv"


def load(path: Path) -> dict[str, float]:
    with path.open(encoding="utf-8") as f:
        return {row["metric_id"]: float(row["value"]) for row in csv.DictReader(f)}


def pct(num: float, den: float) -> float:
    return 100.0 * num / den


def main() -> None:
    m = load(MARKET)
    f = load(FRAUD)

    remote_count_bn = m["card_count"] * m["remote_share_count"] / 100
    nonremote_count_bn = m["card_count"] * (100 - m["remote_share_count"]) / 100
    remote_value_trn = m["card_value"] * m["remote_share_value"] / 100
    nonremote_value_trn = m["card_value"] * (100 - m["remote_share_value"]) / 100

    remote_avg = remote_value_trn * 1_000 / remote_count_bn
    nonremote_avg = nonremote_value_trn * 1_000 / nonremote_count_bn
    contactless_share_all_cards = pct(m["contactless_count"], m["card_count"])
    fraud_growth = pct(f["total_fraud_value"] - f["total_fraud_value_2023"], f["total_fraud_value_2023"])

    print("EU PAYMENTS PUBLIC-MARKET ANALYSIS")
    print("Evidence: ECB H2 2025 + EBA/ECB 2024 fraud aggregates")
    print()
    print(f"Card payments: {m['card_count']:.1f}bn transactions / EUR {m['card_value']:.1f}tn")
    print(f"Remote card count (derived): {remote_count_bn:.2f}bn")
    print(f"Non-remote card count (derived): {nonremote_count_bn:.2f}bn")
    print(f"Approx. remote average ticket (derived from rounded aggregates): EUR {remote_avg:.2f}")
    print(f"Approx. non-remote average ticket (derived from rounded aggregates): EUR {nonremote_avg:.2f}")
    print(f"Remote/non-remote average-ticket ratio (derived): {remote_avg / nonremote_avg:.2f}x")
    print(f"Contactless share of all card count (derived): {contactless_share_all_cards:.1f}%")
    print(f"Payment fraud value growth 2023->2024 (derived): {fraud_growth:.1f}%")
    print(f"Outside-EEA card fraud-rate multiple (official aggregate): {f['outside_eea_card_fraud_multiple']:.0f}x")
    print()
    print("Interpretation boundary: these are market-level diagnostics, not merchant-level causal effects.")


if __name__ == "__main__":
    main()
