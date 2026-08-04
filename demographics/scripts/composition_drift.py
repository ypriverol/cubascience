#!/usr/bin/env python3
"""
Within-65+ composition drift in the standardised series used for the trend fits.

Why this exists
---------------
The pre-crisis trend fits set the LOW end of the counterfactual span. They run on
an age-standardised series whose top group is open-ended 65+, so ageing WITHIN
65+ enters the slope as if it were rising mortality. This measures that
contamination.

Round 7 caught the numbers being quoted in the manuscript with no script behind
them -- exactly the failure this pipeline exists to prevent. The rates below are
now derived from Cuba's own WHO submission rather than typed.

Method: hold within-65+ age-specific rates FIXED at their 2022 values (Cuba's
WHO ICD-10 submission, deaths by 5-year band over ONEI 3.3 denominators), then
let only the 65-74 / 75-84 / 85+ composition move. Any resulting trend in the
aggregate 65+ rate is pure composition, not mortality.

Writes artifacts/composition_drift.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import linregress

_S = Path(__file__).resolve().parent
sys.path.insert(0, str(_S))
from constants import ARTIFACTS, DATA  # noqa: E402
from mortality_data import mean_population_by_age  # noqa: E402

OUT = ARTIFACTS / "composition_drift.json"
# WHO Frmat 0 bands: Deaths19=65-69, 20=70-74, 21=75-79, 22=80-84,
# 23=85-89, 24=90-94, 25=95+. The 85+ group spans THREE columns; taking only
# Deaths23 halves its rate and understates the composition effect.
BANDS = {"age_65_74": ["Deaths19", "Deaths20"],
         "age_75_84": ["Deaths21", "Deaths22"],
         "age_85_plus": ["Deaths23", "Deaths24", "Deaths25"]}


def _rates_2022() -> dict[str, float]:
    """Within-65+ death rates per 1,000, 2022, from Cuba's WHO submission."""
    df = pd.read_csv(DATA / "who" / "cuba_morticd10_2021_2023.csv")
    # All-cause, both sexes: List code for the all-cause total varies, so sum the
    # detailed causes for Sex=9 (both) if present, else Sex 1+2.
    d = df[(df["Year"] == 2022) & (df["Cause"].astype(str).str.upper() == "AAA")]
    if d.empty:
        raise SystemExit("no all-cause (AAA) rows for 2022 in the WHO file")
    d = d[d["Sex"].isin([1, 2])] if 9 not in set(d["Sex"]) else d[d["Sex"] == 9]
    pops = mean_population_by_age(2022)
    return {g: float(d[cols].sum().sum()) / pops[g] * 1000.0
            for g, cols in BANDS.items()}


def run() -> dict:
    rates = _rates_2022()
    out = {}
    for lo, hi, label in ((2013, 2019, "contiguous_2013_2019"),
                          (2006, 2019, "sparse_2006_2019"),
                          (2014, 2019, "post_break_2014_2019")):
        yrs = list(range(lo, hi + 1))
        agg = []
        for y in yrs:
            p = mean_population_by_age(y)
            n = sum(p[g] for g in BANDS)
            agg.append(sum(rates[g] * p[g] for g in BANDS) / n)
        r = linregress(yrs, np.log(agg))
        out[label] = {"years": [lo, hi], "drift_pct_per_yr": round(100 * r.slope, 3)}

    # The 2012/2013 denominator break that makes the two windows incomparable.
    b = {}
    for y in (2012, 2013):
        p = mean_population_by_age(y)
        tot = sum(p[g] for g in BANDS)
        b[str(y)] = {"share_85_plus_pct": round(100 * p["age_85_plus"] / tot, 3),
                "count_85_plus": round(p["age_85_plus"]),
                "count_65_74": round(p["age_65_74"]),
                "count_75_84": round(p["age_75_84"])}
    b["drop_85_plus"] = b["2012"]["count_85_plus"] - b["2013"]["count_85_plus"]
    return {
        "within_65_rates_2022_per_1000": {k: round(v, 2) for k, v in rates.items()},
        "rates_source": "Cuba WHO ICD-10 submission (data/who), deaths by 5-year "
                        "band over ONEI 3.3 mid-year denominators",
        "composition_only_drift": out,
        "denominator_break_2012_2013": b,
        "reading": "The drift CHANGES SIGN between the contiguous and sparse "
                   "windows. ONEI 3.3's 85+ count FALLS between 2012 and 2013 "
                   "while 65-74 and 75-84 both rise, which is not a demographic "
                   "path; the contiguous window begins on that break and the "
                   "sparse window straddles it, so they are not measuring the "
                   "same object.",
    }


def main() -> None:
    o = run()
    OUT.write_text(json.dumps(o, indent=2), encoding="utf-8")
    print("within-65+ rates 2022 (per 1,000):", o["within_65_rates_2022_per_1000"])
    for k, v in o["composition_only_drift"].items():
        print(f"  {k:24} {v['drift_pct_per_yr']:+.3f}%/yr")
    b = o["denominator_break_2012_2013"]
    print(f"85+ share {b['2012']['share_85_plus_pct']}% (2012) -> "
          f"{b['2013']['share_85_plus_pct']}% (2013); 85+ count falls {b['drop_85_plus']:,}")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
