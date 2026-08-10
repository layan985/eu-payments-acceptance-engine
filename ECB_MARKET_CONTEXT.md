# ECB market context

The transaction-level dataset in this repository is synthetic. To keep the project anchored to the real European payments market, this file tracks official Eurosystem aggregates separately from the experiment data.

## Latest euro-area snapshot: H2 2025

The ECB's 22 July 2026 payments-statistics release reports for the second half of 2025:

- **83.5 billion** non-cash payments in the euro area;
- card payments representing about **57%** of the number of non-cash payments;
- **32.9 billion** contactless card payments;
- **872.7 million** payment cards in circulation at period end;
- an average card-payment value of around **€39**;
- about **60.1 billion** transactions processed by euro-area retail payment systems.

These are market-context metrics, not inputs to the synthetic authorization model.

## Fraud and SCA context

The joint EBA-ECB 2025 payment-fraud report says the 2024 EEA fraud rate was around **0.002% of total transaction value**, while the total value of fraud rose to **€4.2 billion** from €3.5 billion in 2023. The report also finds that Strong Customer Authentication remains effective against the fraud types it was designed to mitigate, especially for card payments, while payer-manipulation fraud is increasing.

That is why the routing experiment in this repository treats fraud and authentication outcomes as rollout guardrails rather than optimizing authorization rate alone.

## Reproducible series

The companion `ecb_market_snapshot.py` script fetches the latest observation available from the ECB Data Portal API for three official series:

| Metric | ECB dataset / key |
|---|---|
| Card payments, number | `PCP/H.U2.W0.W0.CP0.1._T._T.PCS_ALL._Z._X._Z.N.PN` |
| Average value of card payments | `PAY/H.U2.W0.CP0.1._Z.N.EUR_R_PNT` |
| Contactless card payments, number | `PCP/H.U2.W0.W0.CP1.1.2223.NR.PCS_ALL._Z._X._Z.N.PN` |

The ECB PCP dataset also includes fraud dimensions, including remote/electronic card payments and SCA usage. Fraud-related latest-period values can be provisional and should be interpreted with the ECB's stated caution around revisions and classification quality.

## Sources

- ECB payment statistics, H2 2025: https://www.ecb.europa.eu/press/stats/paysec/html/ecb.pis2025h2~23986fb4a6.en.html
- ECB Data Portal, cards and card payments: https://data.ecb.europa.eu/key-figures/payments-statistics-indicators/cards-and-card-payments
- ECB PCP dataset information, including fraud-data disclaimer: https://data.ecb.europa.eu/data/datasets/PCP/data-information
- Joint EBA-ECB payment fraud report press release: https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr251215~e133d9d683.en.html

The API pull is intentionally kept outside the default CI path so a temporary network/API outage cannot make the core reproducibility tests fail.
