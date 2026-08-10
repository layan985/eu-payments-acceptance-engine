from pathlib import Path
import csv
from collections import defaultdict, Counter

DATA = Path(__file__).parent / "data" / "transactions.csv"
OUT = Path(__file__).parent / "output" / "acceptance_report.md"
OUT.parent.mkdir(parents=True, exist_ok=True)


def rate(ok, n):
    return 100 * ok / n if n else 0


rows = list(csv.DictReader(DATA.open(encoding="utf-8")))
overall = sum(int(r["authorized"]) for r in rows)
by_country_psp = defaultdict(lambda: [0, 0, 0.0])
declines = Counter()

for r in rows:
    ok = int(r["authorized"])
    k = (r["country"], r["psp"])
    by_country_psp[k][0] += ok
    by_country_psp[k][1] += 1
    by_country_psp[k][2] += float(r["amount_eur"]) if ok else 0
    if not ok:
        declines[r["decline_reason"]] += 1

lines = [
    "# Payment Acceptance Report", "",
    f"Transactions: **{len(rows):,}**",
    f"Overall authorization rate: **{rate(overall, len(rows)):.2f}%**", "",
    "## Market × PSP authorization", "",
    "| Market | PSP | Attempts | Auth rate | Authorized GMV |",
    "|---|---|---:|---:|---:|",
]
for (country, psp), (ok, n, gmv) in sorted(by_country_psp.items()):
    lines.append(f"| {country} | {psp} | {n:,} | {rate(ok, n):.2f}% | €{gmv:,.0f} |")

lines += ["", "## Declines", ""]
total_declines = sum(declines.values())
for reason, n in declines.most_common():
    lines.append(f"- {reason}: {n:,} ({100 * n / total_declines:.1f}% of declines)")

a = by_country_psp[("DE", "PSP_A")]
b = by_country_psp[("DE", "PSP_B")]
gap_pp = rate(a[0], a[1]) - rate(b[0], b[1])
gap_bps = gap_pp * 100
lines += [
    "", "## Screening finding", "",
    f"In the synthetic DE sample, PSP_A authorization is **{rate(a[0], a[1]):.2f}%** "
    f"versus **{rate(b[0], b[1]):.2f}%** for PSP_B, a **{gap_bps:.0f} bp** raw gap.",
    "",
    "This is not a causal uplift estimate. The correct next step is a randomized routing "
    "experiment with fraud, dispute, latency and cost guardrails.",
]
OUT.write_text("\n".join(lines), encoding="utf-8")
print(OUT)
