#!/usr/bin/env python3
"""
Directly age-standardised all-cause mortality for Cuba (WHO World Standard).

Why this exists
---------------
Cuba's crude death rate rose from 9.7 to ~14.2 per 1,000 between 2019 and 2025,
and that number is routinely compared against Latin American averages of 6-9.
Most of that gap is age structure, not health: Cuba has the oldest population in
the region. Comparing Cuba's *crude* rate to anyone else's rate -- or, worse,
comparing a Cuban 75+ cause-specific rate to an all-ages regional rate -- is not
evidence of anything.

Direct standardisation removes the age structure:

    ASMR = sum_x w_x * (D_x / P_x) * 100,000

with w_x the WHO World Standard Population (Ahmad et al. 2001) weights. The
difference between the crude rate and the ASMR *is* the ageing contribution.

Data
----
Deaths by age: ONEI 3.15 (all-cause, 1985-2022).
Population by age: ONEI 3.3 (mid-year, 2006-2022).
Both stop at 2022, so 2023-2025 are shown only as a crude-rate series and are
explicitly NOT standardised -- a cause-and-age table would be needed.

The open-ended top group is 65+ because ONEI 3.15 publishes 65-69 and 70+ while
3.3 publishes "65 y mas". Within-65+ composition is therefore not controlled;
this understates the correction for a population ageing inside that group.

Outputs ``artifacts/age_standardised_mortality.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import ARTIFACTS, get_claims  # noqa: E402
from mortality_data import deaths_by_age_for_year, mean_population_by_age  # noqa: E402

OUT = ARTIFACTS / "age_standardised_mortality.json"

# WHO World Standard Population 2000-2025 (Ahmad et al. 2001), percent.
# Collapsed to the groups ONEI 3.15 and 3.3 share; 65+ absorbs 65-69 .. 85+.
WHO_STANDARD = {
    "0-4": 8.86, "5-9": 8.69, "10-14": 8.60, "15-19": 8.47, "20-24": 8.22,
    "25-29": 7.93, "30-34": 7.61, "35-39": 7.15, "40-44": 6.59, "45-49": 6.04,
    "50-54": 5.37, "55-59": 4.55, "60-64": 3.72,
    "65+": 2.96 + 2.21 + 1.52 + 0.91 + 0.63,
}

# ONEI 3.15 death-row label prefixes -> group
DEATH_ROWS = {
    "0-4": ("Menores de 5",), "5-9": ("5 - 9",), "10-14": ("10 - 14",),
    "15-19": ("15 - 19",), "20-24": ("20 - 24",), "25-29": ("25 - 29",),
    "30-34": ("30 - 34",), "35-39": ("35 - 39",), "40-44": ("40 - 44",),
    "45-49": ("45 - 49",), "50-54": ("50 - 54",), "55-59": ("55 - 59",),
    "60-64": ("60 - 64",), "65+": ("65 - 69", "70 años y m"),
}

# ONEI 3.3 population keys. Single years 0-19 are summed; 65+ uses "65 y más".
POP_SINGLE = {
    "0-4": range(0, 5), "5-9": range(5, 10), "10-14": range(10, 15),
    "15-19": range(15, 20),
}
POP_GROUP = {g: g for g in ("20-24", "25-29", "30-34", "35-39", "40-44",
                            "45-49", "50-54", "55-59", "60-64")}


def _population_by_group(year: int) -> dict[str, float]:
    """Re-read ONEI 3.3 at the granularity this standardisation needs."""
    import pandas as pd
    from mortality_data import _xls

    df = pd.read_excel(_xls("3.3*"), header=None)
    col = next(j for j in range(df.shape[1])
               if isinstance(df.iloc[0, j], str)
               and df.iloc[0, j].startswith("3.3") and f"año {year}" in df.iloc[0, j])
    vals: dict[str, float] = {}
    for i in range(8, df.shape[0]):
        lab = df.iloc[i, col]
        if isinstance(lab, str):
            try:
                vals[lab.strip()] = float(df.iloc[i, col + 1])
            except (TypeError, ValueError):
                pass
    out = {g: sum(vals[str(a)] for a in rng) for g, rng in POP_SINGLE.items()}
    out.update({g: vals[k] for g, k in POP_GROUP.items()})
    out["65+"] = vals["65 y más"]
    return out


def standardise(year: int) -> dict:
    dd = deaths_by_age_for_year(year)
    labels = dd["age_group"].str.strip()
    deaths = {
        g: float(dd.loc[labels.str.startswith(pref), "deaths"].sum())
        for g, pref in DEATH_ROWS.items()
    }
    unknown = float(dd.loc[labels.str.startswith("Ignorado"), "deaths"].sum())
    known = sum(deaths.values())
    if unknown:
        shares = {g: v / known for g, v in deaths.items()}
        deaths = {g: v + unknown * shares[g] for g, v in deaths.items()}

    pops = _population_by_group(year)
    wsum = sum(WHO_STANDARD.values())
    asmr = sum(
        (WHO_STANDARD[g] / wsum) * (deaths[g] / pops[g]) * 100_000
        for g in WHO_STANDARD
    )
    total_pop = mean_population_by_age(year)["total"]
    total_deaths = known + unknown
    crude = total_deaths / total_pop * 100_000
    return {
        "year": year,
        "total_deaths": int(round(total_deaths)),
        "mid_year_population": int(round(total_pop)),
        "crude_per_100k": round(crude, 1),
        "age_standardised_per_100k": round(asmr, 1),
        "ageing_gap_per_100k": round(crude - asmr, 1),
        "pct_of_crude_explained_by_age_structure": round(100 * (crude - asmr) / crude, 1),
        "age_specific_per_1000": {g: round(deaths[g] / pops[g] * 1000, 3)
                                  for g in WHO_STANDARD},
    }


def main() -> None:
    years = list(range(2017, 2023))  # ONEI 3.15 and 3.3 both end at 2022
    rows = [standardise(y) for y in years]
    base = rows[years.index(2019)]

    claims = get_claims()
    vs = claims["vital_series"]
    pop = dict(zip(claims["population_official_m"]["years"],
                   claims["population_official_m"]["values"]))
    reg = dict(zip(vs["years"], vs["deaths"]))
    # Direct standardisation needs deaths BY AGE, which stop at 2022. Indirect
    # standardisation only needs expected deaths under a reference schedule,
    # which attributable_mortality.py already computes on the projected age
    # structure -- so the age-controlled comparison can still be made as an SMR.
    am = json.loads((ARTIFACTS / "attributable_mortality.json").read_text(encoding="utf-8"))
    expected = {r["year"]: r["expected_deaths_2019_schedule"]["median"]
                for r in am["by_year"]}
    crude_only = []
    for y in (2023, 2024, 2025):
        mid = (pop[y - 1] + pop[y]) / 2 * 1e6
        smr = reg[y] / expected[y]
        crude_only.append({
            "year": y, "total_deaths": reg[y],
            "crude_per_100k": round(reg[y] / mid * 100_000, 1),
            "age_standardised_per_100k": None,
            "expected_deaths_2019_schedule": int(round(expected[y])),
            "smr_vs_2019_schedule": round(smr, 3),
            "implied_asmr_per_100k": round(base["age_standardised_per_100k"] * smr, 1),
            "note": "Direct standardisation impossible (no deaths-by-age after 2022). "
                    "SMR = registered / expected-at-2019-rates on the projected age "
                    "structure; implied ASMR assumes the rate rise is proportional "
                    "across ages, which is an assumption, not a measurement.",
        })

    out = {
        "standard": "WHO World Standard Population 2000-2025 (Ahmad et al. 2001)",
        "method": "direct standardisation, 14 age groups, open-ended 65+",
        "sources": {"deaths": "ONEI 3.15", "population": "ONEI 3.3"},
        "standardised": rows,
        "crude_only_2023_2025": crude_only,
        "change_2019_to_2022": {
            "crude_pct": round(100 * (rows[-1]["crude_per_100k"]
                                      / base["crude_per_100k"] - 1), 1),
            "age_standardised_pct": round(100 * (rows[-1]["age_standardised_per_100k"]
                                                 / base["age_standardised_per_100k"] - 1), 1),
        },
        "caveats": [
            "Open-ended 65+ leaves within-65+ ageing uncontrolled, so the ageing "
            "correction here is a LOWER bound.",
            "All-cause only. Cause-specific standardisation needs a cause x age x "
            "population table (PAHO PLISA / WHO Morticd10), which is not in this repo.",
            "2023-2025 cannot be standardised: no published deaths-by-age after 2022.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"Direct age standardisation, {out['standard']}\n")
    print(f"{'year':>5} {'deaths':>9} {'crude/100k':>11} {'ASMR/100k':>10} "
          f"{'ageing gap':>11} {'% of crude':>11}")
    print("-" * 62)
    for r in rows:
        print(f"{r['year']:>5} {r['total_deaths']:>9,} {r['crude_per_100k']:>11.1f} "
              f"{r['age_standardised_per_100k']:>10.1f} {r['ageing_gap_per_100k']:>11.1f} "
              f"{r['pct_of_crude_explained_by_age_structure']:>10.1f}%")
    for r in crude_only:
        print(f"{r['year']:>5} {r['total_deaths']:>9,} {r['crude_per_100k']:>11.1f} "
              f"{r['implied_asmr_per_100k']:>9.1f}* {'—':>11} {'—':>11}")
    print("\n* indirect: SMR vs the 2019 schedule on the projected age structure")
    print(f"{'year':>5} {'expected':>10} {'observed':>10} {'SMR':>7}")
    for r in crude_only:
        print(f"{r['year']:>5} {r['expected_deaths_2019_schedule']:>10,} "
              f"{r['total_deaths']:>10,} {r['smr_vs_2019_schedule']:>7.3f}")
    c = out["change_2019_to_2022"]
    print(f"\n2019 -> 2022: crude {c['crude_pct']:+.1f}%, "
          f"age-standardised {c['age_standardised_pct']:+.1f}%")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
