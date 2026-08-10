from pathlib import Path
import csv
import datetime
import random

OUT = Path(__file__).parent / "data" / "transactions.csv"

countries = ["DE", "FR", "NL", "ES", "IT", "AT", "BE", "IE", "FI", "PT"]
psps = ["PSP_A", "PSP_B", "PSP_C"]
methods = ["visa", "mastercard", "paypal", "sepa_debit"]
devices = ["mobile", "desktop"]

declines = [
    ("insufficient_funds", "soft"),
    ("do_not_honor", "soft"),
    ("authentication_failed", "soft"),
    ("invalid_account", "hard"),
    ("lost_or_stolen", "hard"),
]


def approval_probability(country, psp, method, device, three_ds):
    p = 0.935
    if country == "DE" and psp == "PSP_B":
        p -= 0.035
    if country in {"IT", "ES"} and psp == "PSP_C":
        p -= 0.012
    if device == "mobile" and three_ds:
        p -= 0.018
    if method == "paypal":
        p += 0.012
    if method == "sepa_debit":
        p += 0.008
    return max(0.78, min(0.985, p))


def generate(out=OUT, n=300_000, seed=42):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "transaction_id", "timestamp", "country", "psp", "payment_method",
            "device", "three_ds", "amount_eur", "authorized", "decline_reason",
            "decline_type",
        ])
        start = datetime.datetime(2026, 1, 1)
        for i in range(n):
            country = rng.choice(countries)
            psp = rng.choices(psps, weights=[0.45, 0.35, 0.20])[0]
            method = rng.choices(methods, weights=[0.38, 0.32, 0.18, 0.12])[0]
            device = rng.choices(devices, weights=[0.62, 0.38])[0]
            three_ds = method in {"visa", "mastercard"} and rng.random() < 0.58
            amount = round(min(rng.lognormvariate(3.55, 0.75), 1200), 2)
            approved = rng.random() < approval_probability(country, psp, method, device, three_ds)
            reason = dtype = ""
            if not approved:
                reason, dtype = rng.choices(declines, weights=[0.31, 0.27, 0.22, 0.12, 0.08])[0]
            ts = start + datetime.timedelta(minutes=i * 3)
            w.writerow([
                f"tx_{i:08d}", ts.isoformat(), country, psp, method, device,
                int(three_ds), amount, int(approved), reason, dtype,
            ])
    return out


if __name__ == "__main__":
    print(generate())
