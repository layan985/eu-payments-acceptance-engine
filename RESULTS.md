# Reproduced results

Using the fixed seed and 300,000 generated transactions:

- overall authorization rate: **93.10%**
- Germany / PSP_A authorization: **93.03%**
- Germany / PSP_B authorization: **89.31%**
- raw Germany PSP gap: **372 bps**
- most common decline: **insufficient_funds** (~31% of declines)

The separate randomized experiment produces a seeded treatment-control difference of about **248 bps**, with a 95% confidence interval of roughly **191–305 bps**.

The observational Germany gap and the randomized experiment are intentionally separate. The first identifies where to investigate; the second demonstrates how a routing change should be evaluated.
