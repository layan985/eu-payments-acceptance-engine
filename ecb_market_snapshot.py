"""Fetch a small real-market payments snapshot from the ECB Data Portal.

This is market context only. The synthetic transaction experiment remains fully
reproducible without network access.
"""

from __future__ import annotations

import csv
import io
import urllib.parse
import urllib.request

BASE = "https://data-api.ecb.europa.eu/service/data"

SERIES = {
    "card_payments_millions": (
        "PCP",
        "H.U2.W0.W0.CP0.1._T._T.PCS_ALL._Z._X._Z.N.PN",
    ),
    "average_card_payment_eur": (
        "PAY",
        "H.U2.W0.CP0.1._Z.N.EUR_R_PNT",
    ),
    "contactless_card_payments_millions": (
        "PCP",
        "H.U2.W0.W0.CP1.1.2223.NR.PCS_ALL._Z._X._Z.N.PN",
    ),
}


def fetch_latest(dataset: str, key: str, timeout: int = 20) -> dict[str, str]:
    query = urllib.parse.urlencode({"format": "csvdata", "lastNObservations": 1})
    url = f"{BASE}/{dataset}/{key}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "eu-payments-acceptance-engine/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8-sig")

    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise RuntimeError(f"ECB returned no observations for {dataset}/{key}")
    row = rows[-1]
    return {
        "time_period": row.get("TIME_PERIOD", ""),
        "value": row.get("OBS_VALUE", ""),
        "unit": row.get("UNIT_MEASURE", row.get("UNIT", "")),
        "series_key": f"{dataset}/{key}",
    }


def snapshot() -> dict[str, dict[str, str]]:
    return {name: fetch_latest(dataset, key) for name, (dataset, key) in SERIES.items()}


if __name__ == "__main__":
    for name, obs in snapshot().items():
        print(
            f"{name}: {obs['value']} {obs['unit']} "
            f"({obs['time_period']}; {obs['series_key']})"
        )
