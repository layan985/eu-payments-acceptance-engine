"""One-command offline reproduction for the core Checkout evidence.

Runs without provider credentials or network access. It regenerates the canonical
300,000-attempt synthetic environment, recomputes the headline authorization
metrics, reruns the randomized routing experiment, and executes the unit tests.
The command exits non-zero if a canonical seeded result drifts.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from generate_data import generate
from experiment import run_experiment

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "transactions.csv"

EXPECTED = {
    "transactions": 300_000,
    "overall_authorization_rate": 0.9309766666666667,
    "de_psp_a_authorization_rate": 0.9303012404016539,
    "de_psp_b_authorization_rate": 0.8930619266055046,
    "de_observed_gap_bps": 372.3931379614931,
    "randomized_control_n": 20_044,
    "randomized_treatment_n": 19_956,
    "randomized_control_rate": 0.8940331271203353,
    "randomized_treatment_rate": 0.9188214070956104,
    "randomized_effect_bps": 247.8827997527516,
    "randomized_ci_low_bps": 190.86010121861268,
    "randomized_ci_high_bps": 304.9054982868905,
}


def assert_close(name: str, actual: float, expected: float, tol: float = 1e-12) -> None:
    if abs(actual - expected) > tol:
        raise SystemExit(f"REPRODUCTION DRIFT: {name}: expected {expected}, got {actual}")


def canonical_metrics() -> dict[str, float | int]:
    generate(out=DATA, n=300_000, seed=42)
    counts = defaultdict(lambda: [0, 0])
    total = authorized = 0

    with DATA.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            ok = int(row["authorized"])
            total += 1
            authorized += ok
            if row["country"] == "DE" and row["psp"] in {"PSP_A", "PSP_B"}:
                counts[row["psp"]][0] += ok
                counts[row["psp"]][1] += 1

    de_a = counts["PSP_A"][0] / counts["PSP_A"][1]
    de_b = counts["PSP_B"][0] / counts["PSP_B"][1]
    exp = run_experiment()

    return {
        "transactions": total,
        "overall_authorization_rate": authorized / total,
        "de_psp_a_authorization_rate": de_a,
        "de_psp_b_authorization_rate": de_b,
        "de_observed_gap_bps": (de_a - de_b) * 10_000,
        "randomized_control_n": exp["control_n"],
        "randomized_treatment_n": exp["treatment_n"],
        "randomized_control_rate": exp["control_rate"],
        "randomized_treatment_rate": exp["treatment_rate"],
        "randomized_effect_bps": exp["diff"] * 10_000,
        "randomized_ci_low_bps": exp["ci_low"] * 10_000,
        "randomized_ci_high_bps": exp["ci_high"] * 10_000,
    }


def verify(metrics: dict[str, float | int]) -> None:
    for key, expected in EXPECTED.items():
        actual = metrics[key]
        if isinstance(expected, int):
            if actual != expected:
                raise SystemExit(f"REPRODUCTION DRIFT: {key}: expected {expected}, got {actual}")
        else:
            assert_close(key, float(actual), expected)


def run_tests() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    metrics = canonical_metrics()
    verify(metrics)
    run_tests()
    print("\nCHECKOUT REPRODUCTION: PASS")
    print(json.dumps(metrics, indent=2, sort_keys=True))
    print("\nEvidence boundary: synthetic merchant environment + randomized synthetic experiment.")
    print("Provider-test evidence remains credential-gated and is verified by retained redacted records + contract tests.")


if __name__ == "__main__":
    main()
