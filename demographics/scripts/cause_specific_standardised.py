#!/usr/bin/env python3
"""
Cause-specific age-standardised mortality for Cuba, 2021-2023.

Numerators: Cuba's own ICD-10 submission to WHO (data/who/cuba_morticd10_*.csv),
deaths by 4-digit cause x 5-year age group x sex, Frmat 0.
Denominators: ONEI 3.3 mid-year population by age (observed 2021-2022).

Why this exists
---------------
Cuba's published cause-specific rates are CRUDE, and are routinely set against
regional AGE-STANDARDISED rates -- producing claims like "three times the
subregional average" for cardiovascular disease, or "27 times" for stroke.
Cuba has the oldest population in Latin America, so a large part of any such gap
is demography. This script computes both, so the comparison can be made on the
same footing, and reports the inflation factor (crude / standardised) that a
crude comparison silently smuggles in.

2023 is excluded from standardisation: ONEI 3.3 stops at 2022, so there is no
observed denominator, and a projected one would put modelling error inside a
number whose whole purpose is to be directly measured.

Outputs ``artifacts/cause_specific_standardised.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import ARTIFACTS, DATA  # noqa: E402
from mortality_data import _xls  # noqa: E402

OUT = ARTIFACTS / "cause_specific_standardised.json"
WHO_CSV = DATA / "who" / "cuba_morticd10_2021_2023.csv"

# WHO World Standard Population 2000-2025 (Ahmad et al. 2001), percent.
AGE_GROUPS = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34",
              "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69",
              "70-74", "75-79", "80-84", "85+"]
WHO_STANDARD = [8.86, 8.69, 8.60, 8.47, 8.22, 7.93, 7.61, 7.15, 6.59, 6.04,
                5.37, 4.55, 3.72, 2.96, 2.21, 1.52, 0.91, 0.63]

# Frmat 0 death columns -> the 18 standard groups.
DEATH_COLS = {
    "0-4": ["Deaths2", "Deaths3", "Deaths4", "Deaths5", "Deaths6"],
    "5-9": ["Deaths7"], "10-14": ["Deaths8"], "15-19": ["Deaths9"],
    "20-24": ["Deaths10"], "25-29": ["Deaths11"], "30-34": ["Deaths12"],
    "35-39": ["Deaths13"], "40-44": ["Deaths14"], "45-49": ["Deaths15"],
    "50-54": ["Deaths16"], "55-59": ["Deaths17"], "60-64": ["Deaths18"],
    "65-69": ["Deaths19"], "70-74": ["Deaths20"], "75-79": ["Deaths21"],
    "80-84": ["Deaths22"], "85+": ["Deaths23", "Deaths24", "Deaths25"],
}
UNKNOWN_COL = "Deaths26"

# ICD-10 letter + numeric ranges. Chosen to match the groupings the public
# debate actually uses.
CAUSES = {
    "all_causes": None,
    "circulatory_I00_I99": ("I", 0, 99),
    "ischaemic_heart_I20_I25": ("I", 20, 25),
    "cerebrovascular_I60_I69": ("I", 60, 69),
    "malignant_neoplasms_C00_C97": ("C", 0, 97),
    "diabetes_E10_E14": ("E", 10, 14),
    "respiratory_J00_J99": ("J", 0, 99),
}


def _in_range(code: str, letter: str, lo: int, hi: int) -> bool:
    code = str(code)
    if not code.startswith(letter):
        return False
    digits = code[1:3]
    if not digits[:2].isdigit():
        return False
    return lo <= int(digits[:2]) <= hi


def _population_18(year: int) -> dict[str, float]:
    """ONEI 3.3 mid-year population on the 18 standard groups."""
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
    out = {
        "0-4": sum(vals[str(a)] for a in range(0, 5)),
        "5-9": sum(vals[str(a)] for a in range(5, 10)),
        "10-14": sum(vals[str(a)] for a in range(10, 15)),
        "15-19": sum(vals[str(a)] for a in range(15, 20)),
    }
    for g in ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
              "55-59", "60-64", "65-69", "70-74", "75-79", "80-84"]:
        out[g] = vals[g]
    out["85+"] = vals["85 y más"]
    return out


def _deaths_18(df: pd.DataFrame) -> dict[str, float]:
    d = {g: float(df[cols].sum().sum()) for g, cols in DEATH_COLS.items()}
    unknown = float(df[UNKNOWN_COL].sum()) if UNKNOWN_COL in df else 0.0
    known = sum(d.values())
    if unknown and known:
        shares = {g: v / known for g, v in d.items()}
        d = {g: v + unknown * shares[g] for g, v in d.items()}
    return d


def analyse(year: int, who: pd.DataFrame) -> dict:
    pops = _population_18(year)
    total_pop = sum(pops.values())
    wsum = sum(WHO_STANDARD)
    yr = who[who.Year == year]
    results = {}
    for name, rng in CAUSES.items():
        sub = yr[yr.Cause == "AAA"] if rng is None else yr[
            yr.Cause.map(lambda c: _in_range(c, *rng))]
        deaths = _deaths_18(sub)
        total = sum(deaths.values())
        crude = total / total_pop * 100_000
        asmr = sum(
            (w / wsum) * (deaths[g] / pops[g]) * 100_000
            for g, w in zip(AGE_GROUPS, WHO_STANDARD)
        )
        results[name] = {
            "deaths": int(round(total)),
            "crude_per_100k": round(crude, 1),
            "age_standardised_per_100k": round(asmr, 1),
            "crude_over_standardised": round(crude / asmr, 2) if asmr else None,
            "pct_of_crude_from_age_structure": round(100 * (crude - asmr) / crude, 1)
            if crude else None,
        }
    return {"year": year, "mid_year_population": int(round(total_pop)),
            "causes": results}


def main() -> None:
    if not WHO_CSV.exists():
        raise SystemExit(
            f"missing {WHO_CSV}\nSee data/EXTERNAL_DATA.md for the WHO download URLs.")
    who = pd.read_csv(WHO_CSV, low_memory=False)
    # Sexes 1 and 2 only; 9 (unspecified) would double-count if present.
    who = who[who.Sex.isin([1, 2])]

    years = [2021, 2022]  # ONEI 3.3 denominators stop at 2022
    rows = [analyse(y, who) for y in years]

    out = {
        "standard": "WHO World Standard Population 2000-2025 (Ahmad et al. 2001)",
        "method": "direct standardisation, 18 five-year groups to 85+",
        "numerator": "Cuba ICD-10 submission to WHO (Frmat 0), data/who/",
        "denominator": "ONEI 3.3 mid-year population by age (observed)",
        "years": rows,
        "excluded": {
            "2023": "Cuba submitted 2023 deaths to WHO, but ONEI 3.3 population "
                    "stops at 2022, so there is no observed denominator. "
                    "Standardising it would require a projected population.",
        },
        "how_to_read": (
            "crude_over_standardised is the factor by which a CRUDE comparison "
            "overstates Cuba's position against an age-standardised comparator. "
            "For the diseases of old age it is large, which is why crude "
            "cause-specific comparisons against regional standardised rates are "
            "not evidence of anything."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    for r in rows:
        print(f"\nCuba {r['year']} — mid-year population {r['mid_year_population']:,}")
        print(f"{'cause':<32}{'deaths':>9}{'crude':>10}{'ASMR':>10}{'crude/ASMR':>12}")
        print("-" * 73)
        for name, c in r["causes"].items():
            print(f"{name:<32}{c['deaths']:>9,}{c['crude_per_100k']:>10.1f}"
                  f"{c['age_standardised_per_100k']:>10.1f}"
                  f"{c['crude_over_standardised']:>12.2f}")
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
