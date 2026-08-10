# External review packet

This repository is open for review by payments analysts, engineers, product managers and researchers.

A useful review does **not** need to endorse the project. The highest-value feedback is a concrete correction, edge case, missing guardrail or production assumption that should change.

## Five review questions

1. Is the authorization/routing experiment framed correctly for a merchant acceptance team?
2. Which production confounders are missing from the synthetic transaction model?
3. Which PSP/acquirer metrics would you require before reallocating traffic?
4. Are the 3DS/SCA and decline categories operationally realistic enough for an interview case?
5. What one additional failure mode would make this closer to real payment operations?

## How to review

Open a GitHub issue with the file or assumption you reviewed, the concrete problem or missing case, why it matters in production, and a suggested correction or test if possible.

External feedback will be acknowledged in the repository changelog when incorporated.
