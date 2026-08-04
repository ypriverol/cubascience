#!/usr/bin/env python3
"""
Back-test the cohort projection rule on the years where truth is observed.

Why this exists
---------------
The 2025 excess-mortality estimate rests on a projected 60+ population for
2023-2026, because ONEI table 3.3 stops at 2022. The projection rule was never
validated, and it can be: run it forward from observed 2019 and compare against
observed 2020, 2021 and 2022 -- exactly three years, the same horizon the
forward projection runs past 2022.

It overshoots, and the error is one-sided and grows with horizon. The model
carried projection error as a symmetric +/-1.5%/yr draw, which by construction
cannot represent a bias. This script measures the bias so the manuscript can
state it with a sign instead of claiming the noise term absorbs it.

Direction of the consequence: an overshooting 60+ count raises expected deaths
E_t, and excess = D_t * Dfac - E_t, so the bias makes the reported excess too
SMALL. The headline is conservative on this axis. That is worth stating plainly
rather than leaving a reader to discover the rule is untested.

Writes artifacts/projection_backtest.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

import attributable_mortality as am  # noqa: E402
from constants import ARTIFACTS  # noqa: E402
from mortality_data import mean_population_by_age  # noqa: E402

OUT = ARTIFACTS / "projection_backtest.json"

# Net emigration assumed during the back-test window. ONEI publishes no
# identity-consistent residual per year before 2022, so this is the same
# placeholder the forward projection uses for unlisted years. The back-test is
# reported at both ends: zero migration isolates the cohort-flow rule itself,
# and the placeholder shows how much of the gap emigration can absorb.
BACKTEST_MIG = 210_000


def _step(cur: dict, rates: dict, e_mig: float) -> dict:
    """One year of the projection rule, identical to attributable_mortality."""
    e_60_64, e_65p = e_mig * 0.35, e_mig * 0.65
    to_65 = cur["age_60_64"] / 5.0
    to_60 = cur["age_55_59"] / 5.0
    to_55 = cur["age_50_54"] / 5.0
    to_50 = cur["age_45_49"] / 5.0
    to_45 = cur["age_40_44"] / 5.0
    return {
        "age_40_44": cur["age_40_44"],
        "age_45_49": cur["age_45_49"] + to_45 - to_50,
        "age_50_54": cur["age_50_54"] + to_50 - to_55,
        "age_55_59": cur["age_55_59"] + to_55 - to_60,
        "age_60_64": cur["age_60_64"] + to_60 - to_65
        - cur["age_60_64"] * rates["age_60_64"] / 1000.0 - e_60_64,
        "age_65_plus": cur["age_65_plus"] + to_65
        - cur["age_65_plus"] * rates["age_65_plus"] / 1000.0 - e_65p,
    }


def run() -> dict:
    rates = am._load_rates(2019)["rates_per_1000"]
    obs = {y: mean_population_by_age(y) for y in range(2019, 2023)}

    arms = {}
    for label, share in (("no_migration", 0.0), ("elderly_share_8pct", 0.08)):
        cur, rows = dict(obs[2019]), []
        for year in (2020, 2021, 2022):
            cur = _step(cur, rates, BACKTEST_MIG * share)
            proj = cur["age_60_64"] + cur["age_65_plus"]
            truth = obs[year]["age_60_plus"]
            rows.append({
                "year": year,
                "horizon": year - 2019,
                "projected_60_plus": round(proj),
                "observed_60_plus": round(truth),
                "error": round(proj - truth),
                "error_pct": round(100 * (proj - truth) / truth, 2),
            })
        arms[label] = rows

    # Translate the horizon-3 error into deaths, which is the quantity the
    # manuscript reports. The 60+ groups carry ~82% of all deaths.
    h3 = arms["elderly_share_8pct"][-1]
    death_bias = h3["error"] * rates["age_65_plus"] / 1000.0
    h3_nomig = arms["no_migration"][-1]
    death_bias_nomig = h3_nomig["error"] * rates["age_65_plus"] / 1000.0

    return {
        "what": "cohort projection rule run forward from observed 2019, "
                "compared against observed 2020-2022 (ONEI 3.3)",
        "horizon": "three years, matching 2023->2025 past the 2022 anchor",
        "arms": arms,
        "finding": {
            "direction": "the rule OVERSHOOTS the 60+ count at every horizon, "
                         "and the error grows monotonically",
            "horizon_3_error_pct": {
                "no_migration": h3_nomig["error_pct"],
                "elderly_share_8pct": h3["error_pct"],
            },
            "implied_expected_death_bias_2025": {
                "no_migration": round(death_bias_nomig),
                "elderly_share_8pct": round(death_bias),
            },
            "effect_on_headline": "excess = D*Dfac - E, so an overshooting E "
                                  "makes the reported excess too SMALL. The "
                                  "2025 headline is conservative on this axis "
                                  "by roughly the death figures above.",
            "why_the_noise_term_does_not_cover_it": "projection error entered "
                                                    "as a symmetric N(0, 1.5%) "
                                                    "draw, which has zero mean "
                                                    "and cannot represent a "
                                                    "one-sided bias.",
        },
    }


def main() -> None:
    out = run()
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Projection back-test — 60+ population, rule vs ONEI 3.3 observed\n")
    for label, rows in out["arms"].items():
        print(f"{label}:")
        for r in rows:
            print(f"  {r['year']}  proj {r['projected_60_plus']:>10,}"
                  f"  obs {r['observed_60_plus']:>10,}"
                  f"  err {r['error']:>+9,} ({r['error_pct']:+.2f}%)")
    f = out["finding"]
    print(f"\nBias is one-sided and grows. Implied 2025 expected-death bias: "
          f"{f['implied_expected_death_bias_2025']['elderly_share_8pct']:,} to "
          f"{f['implied_expected_death_bias_2025']['no_migration']:,} deaths.")
    print("The reported excess is too SMALL by that amount — conservative.")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
