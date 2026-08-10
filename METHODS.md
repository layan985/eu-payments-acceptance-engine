# Methods

## Objective

Diagnose payment acceptance and design an experiment that can distinguish a promising routing hypothesis from a causal improvement.

## Synthetic data design

Transactions are generated from fixed random seeds. Baseline authorization probability is modified by a small number of explicit rules:

- Germany × PSP_B has a negative authorization adjustment.
- Italy/Spain × PSP_C has a smaller negative adjustment.
- mobile card transactions using 3DS have additional friction.
- PayPal and SEPA Direct Debit receive small positive baseline adjustments.

These rules make the dataset useful for testing whether diagnostics recover known structure.

## Why the report does not call the raw PSP gap "uplift"

Routing is not randomized in observational payment data. PSP performance can be confounded by issuer mix, customer mix, retry policy, transaction size, fraud controls, geography, network, card product and traffic allocation. The raw gap is therefore a screening signal only.

## Experiment

`experiment.py` simulates a randomized A/B routing test. It reports control and treatment authorization, basis-point difference, a two-sided z-test approximation, a 95% confidence interval and incremental authorizations per 100,000 attempts.

A real rollout would additionally monitor fraud losses, disputes, latency, processing cost, refund rate and operational failure rates.

## Reproducibility

The generator and experiment use fixed seeds. The data file is intentionally not checked into Git; it can be regenerated exactly.
