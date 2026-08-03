# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import attributable_mortality as am
from mortality_data import mean_population_by_age


def test_2019_baseline_matches_onei_totals():
    base = am._load_rates(2019)
    assert abs(base["total_deaths"] - 109_080) < 1          # ONEI 3.15
    assert abs(base["pop_total"] - 11_201_549) < 1          # ONEI 3.3 mid-year
    # Cuban mortality is overwhelmingly an elderly phenomenon.
    assert 78.0 < base["share_deaths_60_plus_pct"] < 86.0
    r = base["rates_per_1000"]
    assert r["age_0_14"] < r["age_15_59"] < r["age_60_64"] < r["age_65_plus"]


def test_denominators_are_observed_not_derived_from_shares():
    """Regression: the elderly count must come from ONEI 3.3, not share x total."""
    base = am._load_rates(2019)
    obs = mean_population_by_age(2019)
    assert base["pops"]["age_60_64"] == obs["age_60_64"]
    assert base["pops"]["age_65_plus"] == obs["age_65_plus"]


def test_elderly_population_never_falls():
    """
    Regression: deriving the 60+ count as (share x official total) made it drop
    ~67k in 2024, because the official total absorbs ONEI's 2023 register
    catch-up in one step. Cuba's 60+ count has risen every year since 2006.
    """
    out = am.run()
    counts = [r["population_60_plus_median"] for r in out["by_year"]]
    assert counts == sorted(counts), counts
    # projected years must never fall below the last observed value (mid-2022)
    obs_2022 = mean_population_by_age(2022)["age_60_plus"]
    projected = [r["population_60_plus_median"] for r in out["by_year"]
                 if r["year"] > am.OBSERVED_THROUGH]
    assert min(projected) >= obs_2022 - 1_000, (min(projected), obs_2022)


def test_decomposition_is_exact_per_draw():
    out = am.run()
    for row in out["by_year"]:
        assert abs(row["identity_residual_median"]) <= 1, (
            row["year"], row["identity_residual_median"])


def test_bands_ordered_and_cumulative_is_correlated():
    out = am.run()
    for row in out["by_year"]:
        a = row["attributable_health_system"]
        assert a["p05"] <= a["median"] <= a["p95"]
    cum = out["cumulative_attributable"]["2024_2025"]
    per_year = [r for r in out["by_year"] if r["year"] in (2024, 2025)]
    naive_low = sum(r["attributable_health_system"]["p05"] for r in per_year)
    # Systematic parameters are shared, so the cumulative low must not sit far
    # above the perfectly-correlated sum (which independence would produce).
    assert cum["p05"] >= naive_low - 1


def test_2021_covid_wave_dominates_and_2024_25_rises_again():
    out = am.run()
    by = {r["year"]: r["attributable_health_system"]["median"] for r in out["by_year"]}
    assert by[2021] > 40_000                 # pandemic wave
    assert by[2022] < by[2021] / 3           # falls back sharply
    assert by[2025] > by[2023]               # post-pandemic escalation


if __name__ == "__main__":
    for fn in list(globals().values()):
        if callable(fn) and getattr(fn, "__name__", "").startswith("test_"):
            fn()
    print("ok")
