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

It overshoots. The model carried projection error as a symmetric +/-1.5%/yr
draw, which by construction cannot represent a bias, so the direction is worth
stating.

WHAT THIS DOES NOT MEASURE. An earlier version of this script read the overshoot
as the cohort-flow rule's bias and quoted it in the manuscript as a death count.
That was wrong. Re-running with each year's ACTUAL age-specific rates instead of
the 2019 schedule collapses the 8%-arm horizon-2 error from +49,399 to -101: the
overshoot is dominated by unmodelled 2020-2022 excess mortality (+48,120 of it
the 2021 COVID peak), which the 2019 schedule does not contain, not by the
cohort flow. A window whose middle year is a pandemic cannot calibrate a
2023-2026 horizon where the paper's own estimates put annual excess at 12k-29k.

The MECHANISM is real for the forward years and survives: depletion at the 2019
schedule under-depletes the elderly stock whenever actual mortality runs above
2019, which raises E_t and so lowers the reported excess. But the paper also
applies the 8% elderly share to the 2023 catch-up figure, which pushes the other
way by a comparable amount. This script therefore reports the SIGN and both
diagnostic arms, and declines to publish a magnitude.

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
    # Two rate regimes. The 2019-schedule arm is what the forward projection
    # actually does; the actual-rates arm isolates the cohort-flow rule from the
    # excess mortality the 2019 schedule cannot see.
    for label, share, actual in (("no_migration", 0.0, False),
                                 ("elderly_share_8pct", 0.08, False),
                                 ("no_migration_actual_rates", 0.0, True),
                                 ("elderly_share_8pct_actual_rates", 0.08, True)):
        cur, rows = dict(obs[2019]), []
        for year in (2020, 2021, 2022):
            yr_rates = am._load_rates(year)["rates_per_1000"] if actual else rates
            cur = _step(cur, yr_rates, BACKTEST_MIG * share)
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

    # Unmodelled 60+ excess in the back-test window, which is what the
    # 2019-schedule arms are mostly picking up.
    unmodelled = {}
    for year in (2020, 2021, 2022):
        b = am._load_rates(year)
        exp = sum(rates[g] / 1000.0 * obs[year][g]
                  for g in ("age_60_64", "age_65_plus"))
        act = b["deaths"]["age_60_64"] + b["deaths"]["age_65_plus"]
        unmodelled[year] = round(act - exp)

    return {
        "what": "cohort projection rule run forward from observed 2019, "
                "compared against observed 2020-2022 (ONEI 3.3)",
        "horizon": "three years, matching 2023->2025 past the 2022 anchor",
        "arms": arms,
        "unmodelled_60_plus_excess_deaths": unmodelled,
        "finding": {
            "direction": "under the 2019 schedule the rule OVERSHOOTS the 60+ "
                         "count at every horizon",
            "what_the_overshoot_mostly_is": "unmodelled 2020-2022 excess "
                                            "mortality, not cohort-flow error: "
                                            "with each year's actual rates the "
                                            "8%-arm horizon-2 error collapses "
                                            "from +49,399 to -101, and 2021 "
                                            "alone contributes +48,120 "
                                            "unmodelled 60+ excess deaths",
            "magnitude_is_NOT_reported": "a window whose middle year is a "
                                         "pandemic cannot calibrate a 2023-2026 "
                                         "horizon. An earlier version published "
                                         "a death count from this exercise; it "
                                         "was withdrawn.",
            "mechanism_that_survives": "depletion at the 2019 schedule "
                                       "under-depletes whenever actual mortality "
                                       "exceeds 2019, raising E_t and so lowering "
                                       "the reported excess. The 8% elderly share "
                                       "applied to the 2023 catch-up pushes the "
                                       "other way by a comparable amount, so we "
                                       "do not claim a net direction for the "
                                       "projection as configured.",
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
    print("\nunmodelled 60+ excess deaths in the window:",
          ", ".join(f"{y} {v:+,}" for y, v in
                    out["unmodelled_60_plus_excess_deaths"].items()))
    print("\nThe 2019-schedule overshoot is mostly that excess, not cohort-flow")
    print("error. No magnitude is published from this exercise; the sign of the")
    print("depletion mechanism is stated in the manuscript and nothing more.")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
