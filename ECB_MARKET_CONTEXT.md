# ECB market context

The transaction-level dataset in this repository is synthetic. To keep the project anchored to the real European payments market, this file tracks official Eurosystem aggregates separately from the experiment data.

## H1 2025 euro-area snapshot

ECB payment statistics for the first half of 2025 report:

- **44.0 billion** card payments in the euro area;
- an average card-payment value of about **€38.40**;
- **29.6 billion** contactless card payments;
- cards representing **56.6%** of the number of non-cash payments, followed by credit transfers at **21.6%** and direct debits at **14.5%**.

These are market-context metrics, not inputs to the synthetic authorization model.

## Reproducible series

The companion `ecb_market_snapshot.py` script fetches the latest observation available from the ECB Data Portal API for three official series:

| Metric | ECB dataset / key |
|---|---|
| Card payments, number | `PCP/H.U2.W0.W0.CP0.1._T._T.PCS_ALL._Z._X._Z.N.PN` |
| Average value of card payments | `PAY/H.U2.W0.CP0.1._Z.N.EUR_R_PNT` |
| Contactless card payments, number | `PCP/H.U2.W0.W0.CP1.1.2223.NR.PCS_ALL._Z._X._Z.N.PN` |

## Sources

- ECB Data Portal, Payments statistics: https://data.ecb.europa.eu/
- ECB press release, payment statistics for the first half of 2025: https://www.ecb.europa.eu/press/stats/paysec/html/ecb.pis2025h1~8bd3a53a8e.en.html

The API pull is intentionally kept outside the default CI path so a temporary network/API outage cannot make the core reproducibility tests fail.
