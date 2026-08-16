"""One-command offline reproduction for Checkout's public evidence.

Runs without provider credentials or network access. It regenerates the canonical
300,000-attempt synthetic environment, recomputes the headline authorization
metrics, reruns the randomized routing experiment, rebuilds the retry/payment-state
research artifacts, and executes the unit tests. The command exits non-zero if a
published seeded result drifts.
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
from research_artifacts import generate_all

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "transactions.csv"

EXPECTED = {
    "transactions": 300_000,
    "overall_authorization_rate": 0.9309766666666667,
    "de_psp_a_authorization_rate": 0.9303012404016539,
    "de_psp_b_authorization_rate": 0.8930619266055045,
    "de_observed_gap_bps": 372.3931379614941,
    "randomized_control_n": 20_044,
    "randomized_treatment_n": 19_956,
    "randomized_control_rate": 0.8940331271203352,
    "randomized_treatment_rate": 0.9188214070956103,
    "randomized_effect_bps": 247.88279975275107,
    "randomized_ci_low_bps": 190.8601012449193,
    "randomized_ci_high_bps": 304.90549826058283,
}

RESEARCH_EXPECTED = {
    "retry.payment_intents": 30_000,
    "retry.attempts": 31_746,
    "retry.attempt_authorization_rate": 0.8712593712593713,
    "retry.intent_resolution_rate": 0.9219666666666667,
    "retry.economic_value_resolution_rate": 0.9217844088926843,
    "retry.retry_share_of_attempts": 0.054999054999055,
    "retry.multi_attempt_intents": 1_531,
    "payment_state.payment_intents": 20_000,
    "payment_state.delivered_events": 61_134,
    "payment_state.duplicate_events": 1_036,
    "payment_state.duplicate_event_rate": 0.01694638008309615,
    "payment_state.naive_captured_event_count": 18_350,
    "payment_state.state_aware_unique_captures": 18_019,
    "payment_state.capture_count_overstatement_pct": 0.018369498862311984,
    "payment_state.naive_refund_event_count": 1_516,
    "payment_state.state_aware_unique_refunds": 1_497,
    "payment_state.refund_count_overstatement_pct": 0.012692050768203123,
    "payment_state.out_of_order_flagged_events": 489,
}


def assert_close(name: str, actual: float, expected: float, tol: float = 1e-10) -> None:
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


def verify_core(metrics: dict[str, float | int]) -> None:
    for key, expected in EXPECTED.items():
        actual = metrics[key]
        if isinstance(expected, int):
            if actual != expected:
                raise SystemExit(f"REPRODUCTION DRIFT: {key}: expected {expected}, got {actual}")
        else:
            assert_close(key, float(actual), expected)


def verify_research(artifacts: dict) -> None:
    for dotted_key, expected in RESEARCH_EXPECTED.items():
        section, key = dotted_key.split(".", 1)
        actual = artifacts[section][key]
        if isinstance(expected, int):
            if actual != expected:
                raise SystemExit(f"REPRODUCTION DRIFT: {dotted_key}: expected {expected}, got {actual}")
        else:
            assert_close(dotted_key, float(actual), expected)


def run_tests() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    core = canonical_metrics()
    verify_core(core)
    research = generate_all()
    verify_research(research)
    run_tests()
    print("\nCHECKOUT REPRODUCTION: PASS")
    print(json.dumps({"core": core, "research": research}, indent=2, sort_keys=True))
    print("\nEvidence boundary: canonical merchant data and research extensions are synthetic.")
    print("Provider-test evidence remains credential-gated and is verified by retained redacted execution records + contract tests.")


if __name__ == "__main__":
    main()
