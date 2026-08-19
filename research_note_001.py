from __future__ import annotations

import math
import numpy as np
import pandas as pd

SEED = 20260819
OBS_N = 250_000
DISCOVERY_N = 100_000
VALIDATION_N = 100_000
MIN_CELL_N = 1_500
MIN_DISCOVERY_UPLIFT_BPS = 100


def make_features(rng: np.random.Generator, n: int) -> pd.DataFrame:
    country = rng.choice(["DE", "FR", "NL"], n, p=[0.45, 0.35, 0.20])
    scheme = rng.choice(["visa", "mastercard"], n, p=[0.55, 0.45])
    device = rng.choice(["mobile", "desktop"], n, p=[0.66, 0.34])
    issuer = rng.choice(["prime", "standard", "challenged"], n, p=[0.40, 0.45, 0.15])
    cross_border = rng.binomial(1, np.where(country == "DE", 0.12, 0.16))
    three_ds = rng.binomial(1, np.where(device == "mobile", 0.70, 0.55))
    card_on_file = rng.binomial(1, 0.37, n)
    amount_eur = np.clip(np.exp(rng.normal(3.7, 0.7, n)), 5, 1_000)

    p_a = np.full(n, 0.965)
    p_a += np.where(issuer == "standard", -0.025, 0)
    p_a += np.where(issuer == "challenged", -0.120, 0)
    p_a += np.where(device == "mobile", -0.010, 0)
    p_a += np.where(three_ds == 1, 0.005, 0)
    p_a += np.where(cross_border == 1, -0.025, 0)
    p_a += np.where(amount_eur > 150, -0.015, 0)
    p_a += np.where(card_on_file == 1, 0.004, 0)
    p_a = np.clip(p_a, 0.72, 0.99)

    delta = np.full(n, -0.010)
    delta += np.where((issuer == "challenged") & (three_ds == 1), 0.045, 0)
    delta += np.where((cross_border == 1) & (scheme == "mastercard"), 0.020, 0)
    delta += np.where((device == "mobile") & (three_ds == 0), -0.012, 0)
    delta += np.where(amount_eur > 250, -0.008, 0)

    p_b = np.clip(p_a + delta, 0.70, 0.995)

    return pd.DataFrame({
        "country": country,
        "scheme": scheme,
        "device": device,
        "issuer_cohort": issuer,
        "cross_border": cross_border,
        "three_ds": three_ds,
        "card_on_file": card_on_file,
        "amount_eur": amount_eur,
        "p_a": p_a,
        "p_b": p_b,
        "true_delta": p_b - p_a,
    })


def diff_stats(df: pd.DataFrame, arm_col: str, outcome_col: str = "authorized") -> dict[str, float | int]:
    g = df.groupby(arm_col)[outcome_col].agg(["mean", "count"])
    p0, n0 = float(g.loc[0, "mean"]), int(g.loc[0, "count"])
    p1, n1 = float(g.loc[1, "mean"]), int(g.loc[1, "count"])
    diff = p1 - p0
    se = math.sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)
    z = diff / se
    p_value = math.erfc(abs(z) / math.sqrt(2))
    return {
        "control_rate": p0,
        "treatment_rate": p1,
        "control_n": n0,
        "treatment_n": n1,
        "effect": diff,
        "ci_low": diff - 1.96 * se,
        "ci_high": diff + 1.96 * se,
        "p_value": p_value,
    }


def run() -> dict[str, object]:
    rng = np.random.default_rng(SEED)

    obs = make_features(rng, OBS_N)
    route_b_probability = np.full(OBS_N, 0.28)
    route_b_probability += np.where(obs["issuer_cohort"] == "standard", 0.12, 0)
    route_b_probability += np.where(obs["issuer_cohort"] == "challenged", 0.42, 0)
    route_b_probability += np.where(obs["cross_border"] == 1, 0.10, 0)
    route_b_probability += np.where(obs["amount_eur"] > 150, 0.05, 0)
    route_b_probability += np.where(obs["device"] == "mobile", 0.03, 0)
    route_b_probability = np.clip(route_b_probability, 0.05, 0.90)
    obs["psp_b"] = rng.binomial(1, route_b_probability)
    obs["authorized"] = rng.binomial(1, np.where(obs["psp_b"] == 1, obs["p_b"], obs["p_a"]))
    observed = diff_stats(obs, "psp_b")
    known_true_ate = float(obs["true_delta"].mean())

    disc = make_features(rng, DISCOVERY_N)
    disc["psp_b"] = rng.binomial(1, 0.50, DISCOVERY_N)
    disc["authorized"] = rng.binomial(1, np.where(disc["psp_b"] == 1, disc["p_b"], disc["p_a"]))
    randomized = diff_stats(disc, "psp_b")
    randomized_true_ate = float(disc["true_delta"].mean())

    segment_keys = ["issuer_cohort", "three_ds", "cross_border", "scheme"]
    cell = disc.groupby(segment_keys + ["psp_b"])["authorized"].agg(["mean", "count"]).reset_index()
    pivot = cell.pivot(index=segment_keys, columns="psp_b", values=["mean", "count"])
    pivot.columns = ["_".join(map(str, c)) for c in pivot.columns]
    pivot = pivot.reset_index()
    pivot["uplift_bps"] = (pivot["mean_1"] - pivot["mean_0"]) * 10_000
    pivot["n"] = pivot["count_0"] + pivot["count_1"]
    selected = pivot[(pivot["uplift_bps"] > MIN_DISCOVERY_UPLIFT_BPS) & (pivot["n"] >= MIN_CELL_N)].copy()

    val = make_features(rng, VALIDATION_N)
    selected_tuples = set(selected[segment_keys].itertuples(index=False, name=None))
    val["policy_routes_b"] = [tuple(row) in selected_tuples for row in val[segment_keys].itertuples(index=False, name=None)]
    policy_route_share = float(val["policy_routes_b"].mean())
    val["policy_arm"] = rng.binomial(1, 0.50, VALIDATION_N)
    actual_route_b = (val["policy_arm"] == 1) & val["policy_routes_b"]
    val["authorized"] = rng.binomial(1, np.where(actual_route_b, val["p_b"], val["p_a"]))
    policy = diff_stats(val, "policy_arm")
    known_true_policy_gain = float(np.where(val["policy_routes_b"], val["true_delta"], 0).mean())

    assert round(observed["effect"] * 10_000, 1) == -271.5
    assert round(known_true_ate * 10_000, 1) == -66.9
    assert round(randomized["effect"] * 10_000, 1) == -63.8
    assert round(randomized_true_ate * 10_000, 1) == -67.3
    assert round(policy_route_share * 100, 2) == 10.38
    assert round(policy["effect"] * 10_000, 1) == 46.0
    assert policy["ci_low"] > 0
    assert len(selected) == 3

    return {
        "observed": observed,
        "known_true_ate": known_true_ate,
        "randomized": randomized,
        "randomized_true_ate": randomized_true_ate,
        "selected": selected[segment_keys + ["uplift_bps", "n"]],
        "policy_route_share": policy_route_share,
        "policy": policy,
        "known_true_policy_gain": known_true_policy_gain,
    }


if __name__ == "__main__":
    r = run()
    print(f"Observed historical gap: {r['observed']['effect']*10000:+.1f} bps")
    print(f"Known historical ATE: {r['known_true_ate']*10000:+.1f} bps")
    print(f"Randomized ATE: {r['randomized']['effect']*10000:+.1f} bps [{r['randomized']['ci_low']*10000:+.1f}, {r['randomized']['ci_high']*10000:+.1f}]")
    print(f"Known randomized ATE: {r['randomized_true_ate']*10000:+.1f} bps")
    print(f"Selected cells: {len(r['selected'])} / 24")
    print(f"Policy routes PSP_B: {r['policy_route_share']*100:.2f}%")
    print(f"Validated policy effect: {r['policy']['effect']*10000:+.1f} bps [{r['policy']['ci_low']*10000:+.1f}, {r['policy']['ci_high']*10000:+.1f}], p={r['policy']['p_value']:.4f}")
    print(f"Known generator policy gain: {r['known_true_policy_gain']*10000:+.1f} bps")
    print(r["selected"].to_string(index=False))
