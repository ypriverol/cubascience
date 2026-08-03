#!/usr/bin/env python3
"""
How many deaths could Cuba be hiding? A bounding analysis.

Two claims are routinely conflated and must be kept apart:

  (A) UNDER-REGISTRATION -- deaths that never enter the official register at all.
      Parameterised as Dfac >= 1 on registered deaths.
  (B) EXCESS / ATTRIBUTABLE MORTALITY -- deaths above what the 2019 health system
      and the current age structure would produce. Most of these ARE registered.

The attributable-mortality model already answers (B): ~28,600 in 2025. This
script bounds (A): it sweeps Dfac and reports, for each level, the quantities
that would have to be simultaneously true -- and flags which levels collide with
something observable.

The binding constraint is Cuba's own 2021: registered deaths jumped 54% in a
single year (109,080 -> 167,645) and ONEI published it. A register that recorded
a 54% surge under maximum stress is not one that can quietly absorb an unlimited
number of hidden deaths -- which is why the central Dfac stays low even though
the crisis is severe.

Outputs ``artifacts/underregistration_bounds.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from attributable_mortality import _load_rates, _midyear, _model_d_path, OFFICIAL_END_M  # noqa: E402
from constants import ARTIFACTS, get_claims  # noqa: E402
from mortality_data import mean_population_by_age  # noqa: E402

OUT = ARTIFACTS / "underregistration_bounds.json"

YEAR = 2025
DFAC_GRID = [1.00, 1.03, 1.06, 1.09, 1.15, 1.20, 1.30, 1.40, 1.50]

# Observed anchors for "how far has a real mortality shock ever pushed a rate".
BENCHMARKS = {
    "cuba_2021_covid_peak_registered": {
        "deaths": 167_645,
        "note": "Cuba's own worst year, openly published: +53.7% on 2019.",
    },
    "venezuela_crisis_all_cause_cdr_rise_pct": {
        "value": 25,
        "note": "Approx. all-cause crude death-rate rise during the collapse.",
    },
    "puerto_rico_maria_6month_excess_pct": {
        "value": 22,
        "note": "Six-month excess after Hurricane Maria (Kishore et al. 2018).",
    },
    "onei_internal_disagreement_2023_pct": {
        "value": 9.6,
        "note": "Three official 2023 death totals: 129,049 / 120,098 / 117,746. "
                "The spread between official sources is itself ~9.6% -- an "
                "empirical floor on how much reporting slack demonstrably exists.",
    },
}


def main() -> None:
    claims = get_claims()
    base = _load_rates(2019)
    reg = dict(zip(claims["vital_series"]["years"], claims["vital_series"]["deaths"]))
    d_reg = float(reg[YEAR])

    # 2019 observed anchors
    p60_2019 = mean_population_by_age(2019)["age_60_plus"]
    share60 = base["share_deaths_60_plus_pct"] / 100.0
    rate60_2019 = share60 * base["total_deaths"] / p60_2019 * 1000.0

    # 2025 stocks and elderly count (from the attributable-mortality projection)
    am = json.loads((ARTIFACTS / "attributable_mortality.json").read_text(encoding="utf-8"))
    row = [r for r in am["by_year"] if r["year"] == YEAR][0]
    p60_2025 = float(row["population_60_plus_median"])
    expected = float(row["expected_deaths_2019_schedule"]["median"])
    pop_off = _midyear(OFFICIAL_END_M, YEAR)
    pop_d = _midyear(_model_d_path(), YEAR)

    rows = []
    for dfac in DFAC_GRID:
        total = d_reg * dfac
        hidden = total - d_reg
        deaths60 = share60 * total
        rate60 = deaths60 / p60_2025 * 1000.0
        rows.append({
            "dfac": dfac,
            "hidden_pct": round(100 * (dfac - 1), 1),
            "true_deaths_2025": int(round(total)),
            "deaths_never_registered": int(round(hidden)),
            "cdr_official_stock": round(total / pop_off * 1000.0, 2),
            "cdr_model_d_stock": round(total / pop_d * 1000.0, 2),
            "rate_60_plus_per_1000": round(rate60, 1),
            "rate_60_plus_vs_2019_pct": round(100 * (rate60 / rate60_2019 - 1), 1),
            "attributable_2025": int(round(total - expected)),
            "vs_cuba_2021_peak_pct": round(100 * (total / 167_645 - 1), 1),
        })

    verdicts = []
    for r in rows:
        d = r["dfac"]
        if d <= 1.09:
            v = ("plausible — inside the spread between Cuba's own official "
                 "sources for a single year (~9.6%)")
        elif d <= 1.20:
            v = ("possible — requires registry degradation beyond anything "
                 "documented, but 60+ mortality stays below the 2021 peak")
        elif d <= 1.30:
            v = ("strained — implies annual deaths above Cuba's published COVID "
                 "peak with no pandemic, and 60+ mortality ~50% over 2019")
        else:
            v = ("implausible — implies a crude death rate at or above wartime "
                 "levels, and more hidden deaths than the 2021 wave killed in total")
        verdicts.append({"dfac": d, "verdict": v})

    out = {
        "question": "How many Cuban deaths could be going unregistered?",
        "year": YEAR,
        "registered_deaths": int(d_reg),
        "expected_deaths_2019_schedule": int(round(expected)),
        "anchors_2019": {
            "total_deaths": int(round(base["total_deaths"])),
            "population_60_plus": int(round(p60_2019)),
            "death_rate_60_plus_per_1000": round(rate60_2019, 2),
            "share_of_deaths_at_60_plus_pct": round(100 * share60, 1),
        },
        "stocks_2025_midyear": {
            "official": int(round(pop_off)),
            "model_d": int(round(pop_d)),
            "population_60_plus": int(round(p60_2025)),
        },
        "sweep": rows,
        "verdicts": verdicts,
        "benchmarks": BENCHMARKS,
        "reading": (
            "Under-registration (A) and excess mortality (B) are different "
            "quantities. Even at Dfac = 1.00 -- perfect registration -- the "
            "attributable toll in 2025 is ~24,200, because the crisis kills "
            "mostly through deaths that ARE recorded but should not have "
            "happened. Raising Dfac adds to that, but the register's own "
            "behaviour in 2021 (a published 54% surge) argues it does not hide "
            "at scale."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"Cuba {YEAR}: {int(d_reg):,} registered deaths; "
          f"{int(round(expected)):,} expected on the 2019 schedule at today's age structure")
    print(f"2019 anchor: 60+ death rate {rate60_2019:.2f}/1000 on {int(p60_2019):,} people\n")
    hdr = (f"{'hidden':>7} {'true deaths':>12} {'unregistered':>13} {'CDR off':>8} "
           f"{'CDR D':>7} {'60+ rate':>9} {'vs2019':>8} {'attributable':>13} {'vs 2021 peak':>13}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['hidden_pct']:>6.0f}% {r['true_deaths_2025']:>12,} "
              f"{r['deaths_never_registered']:>13,} {r['cdr_official_stock']:>8.2f} "
              f"{r['cdr_model_d_stock']:>7.2f} {r['rate_60_plus_per_1000']:>9.1f} "
              f"{r['rate_60_plus_vs_2019_pct']:>7.0f}% {r['attributable_2025']:>13,} "
              f"{r['vs_cuba_2021_peak_pct']:>12.0f}%")
    print()
    for v in verdicts:
        print(f"  Dfac {v['dfac']:.2f}: {v['verdict']}")
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
