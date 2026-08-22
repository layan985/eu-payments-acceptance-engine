"""
PFX-1 — Recoverability Frontier synthetic benchmark
Checkout / Payment Acceptance Intelligence

Purpose
-------
Test whether a randomized, multi-arm decline-rescue design can recover
context-specific intervention response better than:
(1) no rescue,
(2) one blanket intervention,
(3) a decline-code-only policy.

IMPORTANT: all effects are synthetic benchmark results. They are not
production merchant estimates.

Dependencies:
    numpy
    pandas
    scikit-learn
"""

from __future__ import annotations
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import normalized_mutual_info_score

SEED = 20260822
N = 600_000
rng = np.random.default_rng(SEED)

# 1. Synthetic payment contexts
issuer = rng.integers(0, 12, N)
country = rng.integers(0, 8, N)
cross = rng.binomial(1, 0.32, N)
stored = rng.binomial(1, 0.46, N)
debit = rng.binomial(1, 0.58, N)
amount_log = rng.normal(3.8, 0.85, N)
token_available = rng.binomial(1, 0.62, N)
three_ds_capable = rng.binomial(1, 0.88, N)

issuer_eff = np.array([.15,.08,.05,.02,0,-.02,-.05,-.08,.04,-.03,.01,-.1])
country_eff = np.array([.05,.03,.01,0,-.02,-.04,.02,-.01])
initial_logit = (
    2.72 + issuer_eff[issuer] + country_eff[country] - .24 * cross
    + .08 * stored - .06 * debit - .07 * (amount_log - 3.8)
)
p_initial = 1 / (1 + np.exp(-initial_logit))
initial_approved = rng.binomial(1, p_initial)
decl_idx = np.where(initial_approved == 0)[0]

# 2. Declined-intent population
d = decl_idx
M = len(d)
iss = issuer[d]
cty = country[d]
cr = cross[d]
st = stored[d]
db = debit[d]
al = amount_log[d]
tok = token_available[d]
cap = three_ds_capable[d]

# Actions: 0 control, 1 route, 2 3DS, 3 token, 4 delayed retry
elig = np.ones((M, 5), dtype=bool)
elig[:, 2] = cap.astype(bool)
elig[:, 3] = tok.astype(bool)

# Feature-driven latent rescue-response class. These classes are deliberately
# not encoded one-to-one in the decline code.
scores = np.column_stack([
    1.00*np.isin(iss,[5,7,11]) + .55*cr + .40*np.isin(cty,[4,5]) - .10*st,
    .85*cr + .55*(al>4.25) + .85*np.isin(iss,[1,3,8]) - .10*st,
    .95*st + .80*np.isin(iss,[0,2,6,10]) + .10*cr,
    .70*db + .85*np.isin(iss,[4,9,11]) - .15*cr + .25*(al<3.7),
]).astype(float)
scores[:, 1][~cap.astype(bool)] = -99
scores[:, 2][~tok.astype(bool)] = -99
scores_noisy = scores + rng.normal(0, .45, scores.shape)
phenotype = scores_noisy.argmax(1)  # 0 route, 1 3DS, 2 token, 3 delay
resistant = rng.binomial(1, 0.12, M).astype(bool)

# Potential recovery probability for every allowed action.
probs = np.zeros((M, 5))
probs[:, 0] = 1 / (1 + np.exp(-(-4.15 + .10*st - .10*cr)))
for j in range(4):
    match = phenotype == j
    ranks = np.argsort(scores_noisy, axis=1)
    second = ranks[:, -2] == j
    p = 0.045 + 0.29*match + 0.075*second
    p += 0.02 * (scores[:, j] > 1.2)
    p[resistant] = 0.025
    probs[:, j+1] = np.clip(p, 0.005, 0.46)
probs[~elig] = 0

# Network/processor-like decline labels: noisy symptoms, not oracle treatment labels.
decline_codes = np.array([
    "do_not_honor", "insufficient_funds", "authentication_required",
    "issuer_unavailable", "generic_decline",
])
code_score = np.column_stack([
    0.8 + 0.5*np.isin(iss,[0,5,7]) + 0.15*cr,
    0.4 + 0.6*db + 0.2*(al>4.3),
    0.25 + 0.7*cr + 0.4*(al>4.5),
    0.15 + 0.8*np.isin(iss,[4,9,11]),
    0.6 + 0.2*np.isin(iss,[2,6,10]),
])
code_score += rng.gumbel(size=code_score.shape) * 0.6
decline_code = decline_codes[code_score.argmax(1)]

# 3. Randomized rescue trial
A = np.empty(M, dtype=int)
propensity = np.empty(M, dtype=float)
for i in range(M):
    feasible = np.where(elig[i])[0]
    A[i] = rng.choice(feasible)
    propensity[i] = 1 / len(feasible)
Y = rng.binomial(1, probs[np.arange(M), A])
split = np.where(rng.random(M) < 0.60, "discovery", "validation")

df = pd.DataFrame({
    "issuer": iss, "country": cty, "cross_border": cr, "stored": st,
    "debit": db, "amount_log": al, "token_available": tok,
    "three_ds_capable": cap, "decline_code": decline_code, "action": A,
    "propensity": propensity, "outcome": Y, "split": split,
})

# 4. Learn a context policy
features = [
    "issuer", "country", "cross_border", "stored", "debit", "amount_log",
    "token_available", "three_ds_capable", "decline_code"
]
X = pd.get_dummies(df[features], columns=["decline_code"], dtype=float)
disc = df["split"].eq("discovery").to_numpy()
val = ~disc
pred = np.zeros((M, 5))
for a in range(5):
    mask = disc & (A == a)
    model = HistGradientBoostingClassifier(
        max_depth=5, learning_rate=.06, max_iter=220,
        l2_regularization=1.3, random_state=77+a,
    )
    model.fit(X.loc[mask], Y[mask])
    pred[:, a] = model.predict_proba(X)[:, 1]
    pred[~elig[:, a], a] = -1
learned_policy = pred.argmax(1)

# Decline-code-only policy learned from the discovery RCT.
disc_df = df.loc[disc].copy()
overall_action = disc_df.groupby("action")["outcome"].mean().to_dict()
cell = {}
for co in decline_codes:
    for a in range(5):
        sub = disc_df[(disc_df["decline_code"] == co) & (disc_df["action"] == a)]
        n = len(sub)
        s = int(sub["outcome"].sum())
        prior = overall_action.get(a, .05)
        cell[(co, a)] = (s + 20*prior)/(n + 20) if n else prior

code_policy = np.zeros(M, dtype=int)
for i, co in enumerate(decline_code):
    feasible = np.where(elig[i])[0]
    values = [cell[(co, a)] for a in feasible]
    code_policy[i] = feasible[int(np.argmax(values))]

blanket_delay = np.full(M, 4, dtype=int)
control_policy = np.zeros(M, dtype=int)
oracle_p = probs.copy()
oracle_p[~elig] = -1
oracle_policy = oracle_p.argmax(1)

# 5. Untouched validation value: doubly robust primary + IPS sensitivity.
def dr_value(policy, mask):
    idx = np.where(mask)[0]
    pi = policy[idx]
    q_pi = pred[idx, pi]
    observed_a = A[idx]
    q_observed = pred[idx, observed_a]
    psi = q_pi + (observed_a == pi)/propensity[idx] * (Y[idx] - q_observed)
    return float(psi.mean()), float(psi.std(ddof=1)/np.sqrt(len(idx))), psi

def ips_value(policy, mask):
    idx = np.where(mask)[0]
    pi = policy[idx]
    z = (A[idx] == pi) * Y[idx] / propensity[idx]
    return float(z.mean()), float(z.std(ddof=1)/np.sqrt(len(idx)))

policies = {
    "control": control_policy,
    "blanket_delay": blanket_delay,
    "decline_code_only": code_policy,
    "full_context": learned_policy,
    "synthetic_oracle": oracle_policy,
}
values = {}
psis = {}
for name, policy in policies.items():
    dr, dr_se, psi = dr_value(policy, val)
    ips, ips_se = ips_value(policy, val)
    truth = float(probs[np.arange(M), policy][val].mean())
    values[name] = {
        "dr": dr, "dr_se": dr_se,
        "dr_95ci": [dr - 1.96*dr_se, dr + 1.96*dr_se],
        "ips": ips, "ips_se": ips_se, "simulator_truth": truth,
    }
    psis[name] = psi

def contrast(a, b):
    delta = psis[a] - psis[b]
    m = float(delta.mean())
    se = float(delta.std(ddof=1)/np.sqrt(len(delta)))
    return {"difference": m, "se": se, "95ci": [m - 1.96*se, m + 1.96*se]}

full_vs_blanket = contrast("full_context", "blanket_delay")
full_vs_code = contrast("full_context", "decline_code_only")
decline_rate = float(1 - initial_approved.mean())
full_vs_blanket["overall_authorization_bps"] = full_vs_blanket["difference"] * decline_rate * 10_000
full_vs_blanket["overall_authorization_bps_95ci"] = [
    x * decline_rate * 10_000 for x in full_vs_blanket["95ci"]
]
full_vs_code["overall_authorization_bps"] = full_vs_code["difference"] * decline_rate * 10_000

incremental_full = values["full_context"]["dr"] - values["control"]["dr"]
incremental_oracle = values["synthetic_oracle"]["dr"] - values["control"]["dr"]

summary = {
    "seed": SEED,
    "synthetic_attempts": N,
    "initial_authorization_rate": float(initial_approved.mean()),
    "initial_declines": int(M),
    "validation_declines": int(val.sum()),
    "phenotype_share": {
        "route": float(np.mean(phenotype == 0)),
        "3ds": float(np.mean(phenotype == 1)),
        "token": float(np.mean(phenotype == 2)),
        "delay": float(np.mean(phenotype == 3)),
    },
    "decline_code_vs_phenotype_nmi": float(normalized_mutual_info_score(decline_code, phenotype)),
    "policy_values": values,
    "full_context_vs_blanket": full_vs_blanket,
    "full_context_vs_decline_code": full_vs_code,
    "frontier_capture_share": float(incremental_full / incremental_oracle),
    "learned_policy_oracle_action_match": float(np.mean(learned_policy[val] == oracle_policy[val])),
}
print(json.dumps(summary, indent=2))
