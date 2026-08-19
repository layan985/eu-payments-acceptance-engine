# Checkout Research Note 001 — The PSP Leaderboard Was the Wrong Decision Rule

## Headline

A synthetic PSP appeared **271.5 bps worse** in historical routed traffic.

Because the data-generating process is known, the true average PSP effect in that historical cohort is **-66.9 bps**. The historical leaderboard therefore overstated the global disadvantage by **204.6 bps**.

A separate 50/50 randomized experiment estimated **-63.8 bps** (95% CI **-96.0 to -31.6**). The known average treatment effect in that randomized cohort was **-67.3 bps**, so the experiment recovered the generator truth to within **3.5 bps**.

The discovery stage examined 24 mechanically defined issuer × 3DS × cross-border × scheme cells. A cell entered the routing policy only when its discovery uplift exceeded **100 bps** and total cell size was at least **1,500**.

The frozen policy routed **10.38%** of validation traffic to PSP_B. In an independent randomized holdout, the policy beat an all-PSP_A strategy by **+46.0 bps** (95% CI **+14.8 to +77.2**, two-sided p = **0.0038**).

That is approximately **460 incremental authorizations per 100,000 attempts** in this synthetic validation.

## Why the result matters

The historical question was: **Which PSP has the higher observed authorization rate?**

The experimental question was: **What happens if comparable traffic is randomly sent to A or B?**

The policy question was: **Can we identify traffic for which B is worth keeping, freeze the rule, and beat an all-A routing strategy on untouched data?**

Those are three different estimands.

## Study design

- Historical cohort: **250,000** synthetic attempts with deliberately non-random routing.
- Randomized discovery cohort: **100,000** synthetic attempts, 50/50 A/B assignment.
- Independent validation cohort: **100,000** synthetic attempts, randomized between all-A and the frozen segment policy.
- Fixed seed: **20260819**.
- Outcome: authorization.
- Confidence intervals: normal-approximation 95% intervals for differences in proportions.
- Evidence boundary: **SYNTHETIC methodological demonstration. No production merchant data.**

## Selected routing cells

| issuer_cohort | three_ds | cross_border | scheme | uplift_bps | n |
|---|---:|---:|---|---:|---:|
| challenged | 1 | 0 | mastercard | 264.579 | 3704 |
| challenged | 1 | 0 | visa | 305.117 | 4612 |
| standard | 1 | 1 | mastercard | 153.596 | 1803 |

## Deliberate guardrail

The largest discovery estimates were **not automatically promoted**. Cells below the 1,500-attempt floor were excluded regardless of apparent uplift. The final policy was then evaluated on a separate randomized validation sample.

## What this study does not establish

- It does not benchmark any real PSP.
- PSP_A and PSP_B are synthetic labels.
- It does not establish production revenue uplift.
- It does not imply authorization should be optimized without fraud, dispute, cost, latency, and refund guardrails.
