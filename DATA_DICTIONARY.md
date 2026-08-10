# Data dictionary

| Field | Type | Meaning |
|---|---|---|
| `transaction_id` | string | synthetic unique transaction identifier |
| `timestamp` | ISO datetime | synthetic transaction timestamp |
| `country` | string | merchant/customer market in the simulation |
| `psp` | string | routed payment service provider |
| `payment_method` | string | Visa, Mastercard, PayPal or SEPA Direct Debit |
| `device` | string | mobile or desktop |
| `three_ds` | 0/1 | whether the simulated card flow used 3DS |
| `amount_eur` | decimal | attempted amount in EUR |
| `authorized` | 0/1 | authorization outcome |
| `decline_reason` | string | synthetic processor/issuer decline category |
| `decline_type` | string | soft or hard decline |
