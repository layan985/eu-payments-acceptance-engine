import math
import random
import statistics

SEED = 7
N = 40_000
CONTROL_P = 0.895
TREATMENT_P = 0.918


def run_experiment(n=N, control_p=CONTROL_P, treatment_p=TREATMENT_P, seed=SEED):
    random.seed(seed)
    control, treatment = [], []
    for _ in range(n):
        if random.random() < 0.5:
            control.append(1 if random.random() < control_p else 0)
        else:
            treatment.append(1 if random.random() < treatment_p else 0)

    pc = statistics.mean(control)
    pt = statistics.mean(treatment)
    diff = pt - pc
    pooled = (sum(control) + sum(treatment)) / (len(control) + len(treatment))
    se_null = math.sqrt(pooled * (1 - pooled) * (1 / len(control) + 1 / len(treatment)))
    z = diff / se_null
    p_value = math.erfc(abs(z) / math.sqrt(2))
    se_diff = math.sqrt(pc * (1 - pc) / len(control) + pt * (1 - pt) / len(treatment))
    return {
        "control_n": len(control), "treatment_n": len(treatment),
        "control_rate": pc, "treatment_rate": pt, "diff": diff,
        "z": z, "p_value": p_value,
        "ci_low": diff - 1.96 * se_diff, "ci_high": diff + 1.96 * se_diff,
    }


if __name__ == "__main__":
    r = run_experiment()
    print(f"Control auth rate:   {r['control_rate']:.3%} (n={r['control_n']:,})")
    print(f"Treatment auth rate: {r['treatment_rate']:.3%} (n={r['treatment_n']:,})")
    print(f"Uplift:              {r['diff'] * 10_000:.0f} bps")
    print(f"95% CI:              [{r['ci_low'] * 10_000:.0f}, {r['ci_high'] * 10_000:.0f}] bps")
    print(f"z-stat:              {r['z']:.2f}")
    print(f"two-sided p-value:   {r['p_value']:.4g}")
    print(f"Per 100k attempts:   {r['diff'] * 100_000:,.0f} incremental authorizations")
    print("Guardrails: fraud, disputes, latency, processing cost, refund rate.")
