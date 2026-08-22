# MRC Vegas 2027 submission package

## Proposed session title

Decline Codes Are Not Failure Types: Measuring the Recoverability Frontier

## Session abstract

Payment teams usually classify failed transactions by issuer or processor response: do not honor, insufficient funds, authentication required, technical failure, and similar labels. Those codes describe what happened. They do not necessarily identify which merchant-controlled intervention would have caused the payment to succeed.

This session introduces the Recoverability Frontier: a causal framework for measuring the share of failed payment demand that is recoverable under the actions a merchant can actually take. The design borrows from sequential randomized experiments and dynamic treatment regimes. Eligible failed intents can be randomized among actions such as alternate routing, 3DS treatment, token or credential treatment, delayed retry, or control. A policy is learned on discovery traffic, frozen, and evaluated once on untouched validation traffic.

The public PFX-1 benchmark uses 600,000 synthetic attempts and is intentionally framed as a falsifiable demonstration rather than production uplift evidence. On the frozen synthetic holdout, the context policy recovered 20.93% of failed intents versus 14.05% under the best blanket rescue. The more important question is whether real-world decline labels contain enough information about intervention response to make context-aware experimentation unnecessary.

The session will show how to design the experiment without violating scheme retry rules, how to define feasible action sets, how to keep fraud, disputes, processing cost, latency and customer friction in the objective, and what results would cause the framework to be rejected.

## Three attendee takeaways

1. A practical distinction between decline reason, retry success and causal recoverability.
2. A reproducible experimental design for comparing payment-recovery interventions without confusing historical processor gaps with causal uplift.
3. A method for estimating whether a merchant is near its attainable authorization frontier or has a meaningful controllable failure gap.

## Suggested format

20–30 minute technical session or practitioner case-study format. Strongest version would pair Checkout with a merchant, orchestration platform or payment provider that has completed a real PFX-1 replication before the conference.

## Claim boundary

The currently public numerical result is randomized synthetic evidence only. A production result will not be substituted or implied unless a real merchant replication is completed under a frozen protocol before presentation.

## Public research

https://checkout-polished.vercel.app/research/recoverability-frontier
