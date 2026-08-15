from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"


def read_one(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def pct(part: float, whole: float) -> float:
    return 100.0 * part / whole


def main() -> None:
    fraud = read_one("cross_border_sca_fraud_2024.csv")[0]
    total = float(fraud["total_fraud_eur_bn"])
    ct = float(fraud["credit_transfer_fraud_eur_bn"])
    card = float(fraud["card_fraud_eur_bn"])
    print("FRAUD DECOMPOSITION")
    print(f"credit transfer share: {pct(ct, total):.1f}%")
    print(f"card share: {pct(card, total):.1f}%")
    print(f"other instruments: {pct(total-ct-card, total):.1f}%")

    structure = {r["metric"]: r for r in read_one("eu_payment_structure_h2_2025.csv")}
    card_count = float(structure["card_count"]["value"])
    card_value = float(structure["card_value"]["value"])
    remote_count_share = float(structure["remote_share_count"]["value"]) / 100
    remote_value_share = float(structure["remote_share_value"]["value"]) / 100
    remote_count = card_count * remote_count_share
    nonremote_count = card_count * (1 - remote_count_share)
    remote_value = card_value * remote_value_share
    nonremote_value = card_value * (1 - remote_value_share)
    remote_ticket = remote_value * 1e12 / (remote_count * 1e9)
    nonremote_ticket = nonremote_value * 1e12 / (nonremote_count * 1e9)
    print("\nPAYMENT STRUCTURE")
    print(f"remote card count: {remote_count:.2f}bn")
    print(f"non-remote card count: {nonremote_count:.2f}bn")
    print(f"implied remote avg ticket: EUR {remote_ticket:.2f}")
    print(f"implied non-remote avg ticket: EUR {nonremote_ticket:.2f}")
    print(f"ticket ratio: {remote_ticket/nonremote_ticket:.2f}x")

    adyen = read_one("adyen_processor_economics.csv")
    print("\nPROCESSOR ECONOMICS")
    for row in adyen:
        print(
            f"{row['period']}: {row['derived_net_revenue_to_volume_bps']} bps proxy"
            + (f", POS share {row['derived_pos_share_pct']}%" if row['derived_pos_share_pct'] else "")
        )

    readiness = read_one("instant_vop_readiness_2026.csv")
    print("\nINSTANT / VOP READINESS")
    for row in readiness:
        print(f"{row['requirement']}: {row['status_as_of_2026_08_15']} ({row['deadline']})")

    architecture = read_one("zalando_checkout_architecture.csv")
    print("\nPUBLIC CHECKOUT ARCHITECTURE")
    for row in architecture:
        print(f"{row['evidence_item']}: {row['value']} {row['unit']} -> {row['implication']}")


if __name__ == "__main__":
    main()
