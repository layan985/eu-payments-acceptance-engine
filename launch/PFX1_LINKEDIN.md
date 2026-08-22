# PFX-1 launch post

I think decline codes are the wrong unit for payment-recovery decisions.

They tell you what came back from the issuer or processor. They do not necessarily tell you what would have made the payment succeed.

So I built an experiment around a different question:

**What fraction of failed demand is actually recoverable by the interventions a merchant can use?**

The framework is called the **Recoverability Frontier**.

For each eligible failed payment, the action set can include things like an alternate route, 3DS treatment, token/credential treatment, delayed retry, or control. Discovery traffic is randomized. The policy is learned there, frozen, and evaluated once on untouched holdout traffic.

I ran the first benchmark on 600,000 synthetic attempts.

On the frozen holdout:

- context policy recovery: 20.93%
- best blanket rescue: 14.05%
- decline-code-only policy: 14.42%
- difference vs blanket: +6.88 percentage points of failed intents
- equivalent overall authorization difference in the benchmark: about +45.5 bps

The number is not the important part. It is synthetic and I am not presenting it as merchant uplift.

The interesting question is whether real payment failures contain treatment heterogeneity that ordinary decline labels do not capture.

If they do, then two merchants with the same authorization rate can have completely different problems. One may already be close to its attainable frontier. The other may be leaving a meaningful amount of recoverable demand on the table.

If they do not, the framework should fail in production and I want to know that too.

I published the full research note, code, frozen results and real-merchant protocol here:

https://checkout-polished.vercel.app/research/recoverability-frontier

I am now looking for one merchant or payments platform willing to test it on real randomized traffic under retry, fraud, dispute, cost, latency and customer-friction guardrails.

The public result can remain fully anonymized.

And for teams that are not ready to randomize traffic yet, I launched a €950 Recoverability Scan: one anonymized export, 48 hours, and a decision on whether there is enough structured failure to justify an experiment.

If you work on payment optimization, orchestration, authorization, retries or experimentation and think this is wrong, I would genuinely like you to tell me where it breaks.
