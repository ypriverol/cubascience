#!/usr/bin/env python3
"""
Excess-mortality decomposition: how much of the rise in deaths is the ageing
population, and how much is a change in age-specific death rates?

The rate term is NOT identified as health-system deterioration. It is the
residual against the 2019 age-specific schedule and absorbs every unmodelled
cause -- reporting changes, denominator error, the projection bias measured in
backtest_projection.py, and genuine deterioration alike.

Replaces the coarse 2019-crude-death-rate bridge in
``mortality_schedule_residual.py`` with indirect age standardisation on
*observed* age denominators.

Method
------
Age groups are the finest set that ONEI 3.15 (deaths) and ONEI 3.3 (mid-year
population) share: {0-14, 15-59, 60-64, 65+}.  Splitting 60+ matters because the
1960s baby boom is entering at 60-64, so the 60+ group is getting *younger* --
a compositional shift that a single open-ended 60+ group would misread as rising
mortality.

Let ``m_a^2019`` be 2019 age-specific death rates.  For year *t* with age-group
populations ``P_{a,t}``,

    E_t     = sum_a m_a * P_{a,t}          expected deaths, 2019 health system
    E_ref   = sum_a m_a * P_{a,2019}       the same schedule on the 2019 structure

    size    = (P_t - P_2019) * E_ref / P_2019
    ageing  = sum_a m_a (P_{a,t} - P_{a,2019}) - size
    rate    = D_t * Dfac - E_t

so that ``D_t*Dfac - E_ref = size + ageing + rate`` holds exactly per draw (the
reference is E_ref rather than the raw 2019 count so that rate perturbations
cancel instead of leaking into the ageing term).

The **rate** term is excess deaths relative to the 2019 age-specific schedule.
It is deliberately NOT called 'attributable to health-system deterioration': the
same formula returns ~61,900 for 2021, which is a pandemic.

Population inputs
-----------------
2019-2022 age structure is *observed* (ONEI 3.3 publishes mid-year population by
age annually through 2022).  2023-2026 is a cohort projection from the observed
2022 structure: entrants from the 55-59 cohort, exits by 2019-schedule mortality,
and elderly emigration at the 8% share in claims.selectivity.  The elderly count
is never derived as (share x total), because the official total absorbs ONEI's
2023 register catch-up in a single step and multiplying that step by an age share
deletes elderly people who never emigrated.

Outputs ``artifacts/attributable_mortality.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta as beta_dist

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import ARTIFACTS, get_claims  # noqa: E402
from mortality_data import deaths_by_age_for_year, mean_population_by_age  # noqa: E402

OUT = ARTIFACTS / "attributable_mortality.json"

N = 200_000
SEED = 2028
BASE_YEAR = 2019
YEARS = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
OBSERVED_THROUGH = 2022  # last year ONEI 3.3 publishes

GROUPS = ("age_0_14", "age_15_59", "age_60_64", "age_65_plus")

# ONEI 3.15 quinquennial labels -> the shared group set
_G0_14 = ("Menores de 5", "5 - 9", "10 - 14")
_G15_59 = (
    "15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39",
    "40 - 44", "45 - 49", "50 - 54", "55 - 59",
)
_G60_64 = ("60 - 64",)
_G65 = ("65 - 69", "70 años y m")

# Mid-year total population (millions). Official ONEI series; 2026 continues the
# observed 2025 pace. Only the *total* comes from here -- the elderly count is
# projected by cohort (see _project_ages).
OFFICIAL_END_M = {2019: 11.19, 2020: 11.18, 2021: 11.11, 2022: 11.09,
                  2023: 10.06, 2024: 9.75, 2025: 9.43, 2026: 9.12}

# Model D living-population path (millions, end of year).
MODEL_D_ANCHORS_M = {2021: 10.80, 2025: 8.58, 2026: 8.29}

# Net emigration by year (persons) used to age the elderly cohorts. Official
# branch: ONEI implied. Model D branch: scaled by the median M.
NET_MIG = {2023: 1_006_000, 2024: 251_237, 2025: 245_264, 2026: 210_000}


def _load_rates(year: int) -> dict:
    """Age-group death rates per 1000 in `year`: ONEI 3.15 deaths / ONEI 3.3 pop."""
    dd = deaths_by_age_for_year(year)
    labels = dd["age_group"].str.strip()

    def _sum(prefixes: tuple[str, ...]) -> float:
        return float(dd.loc[labels.str.startswith(prefixes), "deaths"].sum())

    deaths = {
        "age_0_14": _sum(_G0_14),
        "age_15_59": _sum(_G15_59),
        "age_60_64": _sum(_G60_64),
        "age_65_plus": _sum(_G65),
    }
    unknown = float(dd.loc[labels.str.startswith("Ignorado"), "deaths"].sum())
    known = sum(deaths.values())
    total = known + unknown
    # Redistribute "Ignorado" proportionally. Shares are computed once, up front:
    # updating the denominator inside the loop makes the result order-dependent.
    if unknown:
        shares = {g: v / known for g, v in deaths.items()}
        deaths = {g: v + unknown * shares[g] for g, v in deaths.items()}

    pops = mean_population_by_age(year)
    rates = {g: deaths[g] / pops[g] * 1000.0 for g in GROUPS}
    return {
        "deaths": deaths,
        "pops": {g: pops[g] for g in GROUPS},
        "pop_total": pops["total"],
        "rates_per_1000": rates,
        "total_deaths": total,
        "cdr_per_1000": total / pops["total"] * 1000.0,
        "share_deaths_60_plus_pct": 100.0
        * (deaths["age_60_64"] + deaths["age_65_plus"]) / total,
    }


def _model_d_path() -> dict[int, float]:
    """Log-linear interpolation of the Model D living-population path."""
    yrs = sorted(MODEL_D_ANCHORS_M)
    out: dict[int, float] = {}
    for y in range(2019, 2027):
        if y < yrs[0]:
            out[y] = OFFICIAL_END_M[y]
        elif y in MODEL_D_ANCHORS_M:
            out[y] = MODEL_D_ANCHORS_M[y]
        else:
            lo = max(a for a in yrs if a <= y)
            hi = min(a for a in yrs if a >= y)
            f = (y - lo) / (hi - lo)
            out[y] = float(np.exp(np.log(MODEL_D_ANCHORS_M[lo]) * (1 - f)
                                  + np.log(MODEL_D_ANCHORS_M[hi]) * f))
    return out


def _midyear(path_end_m: dict[int, float], year: int) -> float:
    prev = path_end_m.get(year - 1, path_end_m[year])
    return 0.5 * (prev + path_end_m[year]) * 1e6


def _project_ages(rates: dict[str, float], elderly_emig_share: float,
                  mig_scale: float) -> dict[int, dict[str, float]]:
    """
    Cohort projection of the elderly groups for 2023-2026 from observed 2022.

    Five-year groups lose a fifth of their members to the next group each year;
    the 60+ groups additionally lose 2019-schedule deaths and their share of net
    emigration. Observed years are passed through unchanged.
    """
    ages = {y: mean_population_by_age(y) for y in range(BASE_YEAR, OBSERVED_THROUGH + 1)}
    cur = dict(ages[OBSERVED_THROUGH])
    for year in range(OBSERVED_THROUGH + 1, 2027):
        mig = NET_MIG.get(year, 210_000) * mig_scale
        e_mig = mig * elderly_emig_share
        # 65+ has roughly twice the person-years of 60-64, so split its share.
        e_60_64, e_65p = e_mig * 0.35, e_mig * 0.65
        to_65 = cur["age_60_64"] / 5.0
        to_60 = cur["age_55_59"] / 5.0
        to_55 = cur["age_50_54"] / 5.0
        to_50 = cur["age_45_49"] / 5.0
        to_45 = cur["age_40_44"] / 5.0
        # Every five-year group loses a fifth to the next and gains a fifth from
        # the previous. The previous version had a dead `* 0.0` term here, so
        # 50-54 received no inflow and decayed 59% by 2026, starving the cohorts
        # that feed 60+ and inflating the attributable residual.
        nxt = {
            "age_40_44": cur["age_40_44"] - to_45 + to_45,   # held flat: no
            # published feeder below 40-44, and four years of drift there does
            # not reach 60+ inside this window.
            "age_45_49": cur["age_45_49"] + to_45 - to_50,
            "age_50_54": cur["age_50_54"] + to_50 - to_55,
            "age_55_59": cur["age_55_59"] + to_55 - to_60,
            "age_60_64": cur["age_60_64"] + to_60 - to_65
            - cur["age_60_64"] * rates["age_60_64"] / 1000.0 - e_60_64,
            "age_65_plus": cur["age_65_plus"] + to_65
            - cur["age_65_plus"] * rates["age_65_plus"] / 1000.0 - e_65p,
        }
        nxt["age_60_plus"] = nxt["age_60_64"] + nxt["age_65_plus"]
        ages[year] = nxt
        cur = nxt
    return ages


def _baseline_sensitivity(base: dict) -> dict:
    """2017-2019 mean rates against the 2019 anchor, on observed denominators."""
    alt = [_load_rates(y) for y in (2017, 2018, 2019)]
    mean_rates = {g: float(np.mean([a["rates_per_1000"][g] for a in alt])) for g in GROUPS}
    ratio = {g: mean_rates[g] / base["rates_per_1000"][g] for g in GROUPS}
    return {
        "alt_baseline": "mean age-specific rates 2017-2019 (ONEI 3.15 / ONEI 3.3)",
        "rates_per_1000": {g: round(v, 3) for g, v in mean_rates.items()},
        "ratio_to_2019": {g: round(v, 4) for g, v in ratio.items()},
        "note": "A ratio above 1 at ages 65+ means 2019 was a comparatively good "
                "year, so the 2019 anchor is NOT conservative there; the shift is "
                "well inside the 2% schedule noise either way.",
    }


def _pre_crisis_trend() -> dict:
    """
    Fit the pre-crisis age-standardised trend from the data rather than assert it.

    The justification for a flat 2019 anchor used to live only in a docstring.
    It is window-fragile: 2006-2019 gives ~+0.24%/yr, but 2009-2012 fail to parse
    (the reader guard rejects them) and the contiguous recent window 2013-2019
    gives roughly three times that. Both are reported so the reader can see the
    choice rather than take it on trust.
    """
    from age_standardised_mortality import standardise
    from scipy import stats
    out = {}
    for name, yrs in [("2006_2019_sparse", [2006, 2007, 2008, 2013, 2014, 2015,
                                            2016, 2017, 2018, 2019]),
                      ("2013_2019_contiguous", [2013, 2014, 2015, 2016, 2017,
                                                2018, 2019])]:
        pts = []
        for y in yrs:
            try:
                pts.append((y, standardise(y)["age_standardised_per_100k"]))
            except Exception:
                continue
        if len(pts) < 3:
            continue
        xs = np.array([a for a, _ in pts], float)
        ys = np.log(np.array([b for _, b in pts], float))
        r = stats.linregress(xs, ys)
        tcrit = float(stats.t.ppf(0.975, len(pts) - 2))
        out[name] = {
            "n_years": len(pts),
            "annual_pct": round(100 * r.slope, 3),
            "se_pct": round(100 * r.stderr, 3),
            "p_value": round(float(r.pvalue), 4),
            "r_squared": round(float(r.rvalue) ** 2, 3),
            "ci95_pct": [round(100 * (r.slope - tcrit * r.stderr), 3),
                         round(100 * (r.slope + tcrit * r.stderr), 3)],
        }
    # BOTH confidence intervals contain zero (p = 0.066, 0.064). The pre-crisis
    # trend is NOT identifiable from this series. We therefore do not fit it and
    # propagate it -- that would manufacture precision the data cannot support.
    # The flat anchor is a stated convention, and the counterfactual span below
    # uses the CI bounds rather than the point estimates.
    out["identifiable"] = False
    out["verdict"] = ("Neither slope differs from zero at conventional levels; "
                      "the flat 2019 anchor is a convention, not a finding.")
    return out


def counterfactual_sensitivity(base: dict, expected_2025: float,
                               registered_2025: float, dfac_med: float,
                               expected_by_year: dict | None = None,
                               registered_by_year: dict | None = None) -> dict:
    """
    How much does the CHOICE of counterfactual move the answer?

    The 2019 anchor assumes Cuban mortality would have been flat absent the
    crisis. That is an assumption, and it is the single largest source of
    uncertainty in this estimate -- larger than every term inside the Monte
    Carlo, and entirely outside the reported band. Cuba's own pre-crisis
    age-standardised series is roughly flat (about +0.24%/yr, 2006-2019), which
    supports the choice; regional peers were improving 0.5-1.5%/yr, which does
    not. Both readings are reported.
    """
    fitted = _pre_crisis_trend()
    sparse = fitted.get("2006_2019_sparse", {}).get("annual_pct", 0.236) / 100.0
    contig = fitted.get("2013_2019_contiguous", {}).get("annual_pct", 0.678) / 100.0
    # Upper 95% bound of the steeper fit: the most the data permit for a
    # worsening pre-crisis trend, and therefore the lowest defensible excess.
    contig_hi = fitted.get("2013_2019_contiguous", {}).get(
        "ci95_pct", [0, 1.413])[1] / 100.0
    out = {}
    for label, drift in [("cuba_trend_contiguous_upper95", contig_hi),
                         ("cuba_trend_sparse_2006_2019", sparse),
                         ("cuba_trend_contiguous_2013_2019", contig),
                         ("flat_2019_schedule_AS_USED", 0.0),
                         ("improvement_0.5pct_yr", -0.005),
                         ("improvement_1.0pct_yr", -0.010),
                         ("improvement_1.5pct_yr_regional_norm", -0.015)]:
        exp = expected_2025 * (1 + drift) ** (2025 - BASE_YEAR)
        out[label] = {
            "expected_2025": int(round(exp)),
            "excess_2025": int(round(registered_2025 * dfac_med - exp)),
        }
    # The cumulative windows are what the abstract quotes, so they need the
    # same sensitivity -- previously it was computed for 2025 only.
    if expected_by_year and registered_by_year:
        cum = {}
        for label, drift in [("cuba_trend_contiguous_upper95", contig_hi),
                             ("cuba_trend_sparse_2006_2019", sparse),
                             ("cuba_trend_contiguous_2013_2019", contig),
                             ("flat_2019_schedule_AS_USED", 0.0),
                             ("improvement_0.5pct_yr", -0.005),
                             ("improvement_1.0pct_yr", -0.010),
                             ("improvement_1.5pct_yr_regional_norm", -0.015)]:
            tot = 0.0
            for y in range(2022, 2026):
                exp = expected_by_year[y] * (1 + drift) ** (y - BASE_YEAR)
                tot += registered_by_year[y] * dfac_med - exp
            cum[label] = int(round(tot))
        out["cumulative_2022_2025"] = cum
        out["cumulative_2022_2025"]["_span"] = [min(cum.values()), max(cum.values())]
    out["pre_crisis_trend_fitted"] = fitted
    # Dfac asymmetry: the estimator lifts target-year deaths but leaves the 2019
    # anchor at registered counts, so it assumes 2019 registration was complete
    # and later years are ~3% incomplete. That reads Dfac as a DETERIORATION in
    # completeness. The symmetric variant (anchor lifted too) is the reading in
    # which Dfac is a constant level, and is reported so the choice is visible.
    sym_2025 = registered_2025 * dfac_med - expected_2025 * dfac_med
    out["dfac_symmetric_variant"] = {
        "excess_2025": int(round(sym_2025)),
        "note": "Dfac applied to the 2019 anchor as well. Lower than the headline "
                "because only a CHANGE in completeness since 2019 then counts as "
                "excess. The headline treats Dfac as crisis-induced deterioration.",
    }
    vals = [v["excess_2025"] for v in out.values()
            if isinstance(v, dict) and "excess_2025" in v]
    out["_range"] = {"low": min(vals), "high": max(vals),
                     "note": "This span is comparable to the entire Monte Carlo "
                             "band and is NOT included in it. A flat anchor is "
                             "more likely to under- than overstate, because "
                             "Cuba's peers kept improving."}
    return out


def _elderly_share_sensitivity() -> dict:
    """
    Re-run the decomposition at 0%, the assumed 8%, and 16%.

    Computed, not typed. The hard-coded version of this block had drifted from
    what the script produces (23,668 vs 23,679 and so on) -- small, but the
    artifact's own headline sensitivity was not reproducible by the script that
    writes it, which is the failure mode this whole pipeline exists to prevent.
    """
    out = {}
    for label, share in (("0pct", 0.0), ("8pct_as_used", None), ("16pct", 0.16)):
        r = run(share_override=share, with_sensitivity=False)
        yr = {x["year"]: x for x in r["by_year"]}
        out[label] = {
            "excess_2025": yr[2025]["excess_vs_2019_schedule"]["median"],
            "cumulative_2022_2025": r["cumulative_excess"]["2022_2025_post_covid"]["median"],
        }
    return {
        "parameter": "claims.selectivity.emigrants_60_plus_pct",
        "class": "expert_prior",
        "excess_2025": {k: v["excess_2025"] for k, v in out.items()},
        "cumulative_2022_2025": {k: v["cumulative_2022_2025"] for k, v in out.items()},
        "swing_2025": round((out["16pct"]["excess_2025"]
                             - out["0pct"]["excess_2025"]) / 2),
        "swing_cumulative": round((out["16pct"]["cumulative_2022_2025"]
                                   - out["0pct"]["cumulative_2022_2025"]) / 2),
        "note": "About a quarter of the 2025 prior sensitivity range and a "
                "fifth of the cumulative one, from a single expert prior. "
                "Raising the share RAISES the excess: a genuinely fixed "
                "elderly count (0%) gives the LOWEST value, not the highest.",
    }


def run(share_override: float | None = None, with_sensitivity: bool = True) -> dict:
    """
    ``share_override`` re-runs the whole decomposition at a different elderly
    emigration share, so the sensitivity block is computed rather than typed.
    The previous version hard-coded it and had drifted from what the script
    actually produces.
    """
    rng = np.random.default_rng(SEED)
    base = _load_rates(BASE_YEAR)
    claims = get_claims()
    vs = claims["vital_series"]
    reg_by_year = dict(zip(vs["years"], vs["deaths"]))
    reg_by_year[2026] = int(round(reg_by_year[2025] * 1.04))
    elderly_share = (float(claims["selectivity"]["emigrants_60_plus_pct"]) / 100.0
                     if share_override is None else share_override)

    m = base["rates_per_1000"]
    p19 = base["pops"]
    pop19 = base["pop_total"]

    d_path = _model_d_path()
    ages_off = _project_ages(m, elderly_share, mig_scale=1.0)
    # Model D runs a larger migration engine (median M ~ 1.34), so more elderly
    # leave under that branch.
    ages_d = _project_ages(m, elderly_share, mig_scale=1.34)

    # --- systematic parameters: drawn ONCE and reused in every year ---
    rate_noise = rng.normal(1.0, 0.02, N)
    dfac = 1.0 + 0.09 * beta_dist.ppf(rng.random(N), 1.8, 3.2)
    use_d = rng.random(N) < 0.5
    pop_noise = rng.normal(1.0, 0.02, N)
    # Projection error is SYSTEMATIC: a mis-projected 2022->2023 age structure
    # propagates mechanically into every later year. Drawing it per-year (as the
    # previous version did) averaged it down and made cumulative bands ~8% too
    # narrow, contradicting the Methods claim that all systematic parameters are
    # shared. One shared normal, scaled by horizon.
    proj_z = rng.normal(0.0, 1.0, N)
    # Residual within-65+ composition drift not captured by the 60-64/65+ split.
    # Symmetric: the observed shift since 2019 is toward *younger* elderly.
    drift_max = rng.normal(0.0, 0.03, N)

    results = []
    excess_draws: dict[int, np.ndarray] = {}

    for year in YEARS:
        drift = drift_max * (year - BASE_YEAR) / (YEARS[-1] - BASE_YEAR)
        rates = {g: m[g] * rate_noise for g in GROUPS}
        rates["age_65_plus"] = rates["age_65_plus"] * (1.0 + drift)

        p_tot = np.where(use_d, _midyear(d_path, year), _midyear(OFFICIAL_END_M, year))
        p_tot = p_tot * pop_noise

        a_off, a_d = ages_off[year], ages_d[year]
        p60_64 = np.where(use_d, a_d["age_60_64"], a_off["age_60_64"])
        p65 = np.where(use_d, a_d["age_65_plus"], a_off["age_65_plus"])
        if year > OBSERVED_THROUGH:
            # Projected years carry cohort-projection error; observed ones do not.
            proj_noise = 1.0 + proj_z * 0.015 * (year - OBSERVED_THROUGH)
            p60_64, p65 = p60_64 * proj_noise, p65 * proj_noise
        younger = p_tot - p60_64 - p65
        share_0_14 = p19["age_0_14"] / (p19["age_0_14"] + p19["age_15_59"])
        pa = {
            "age_0_14": younger * share_0_14,
            "age_15_59": younger * (1.0 - share_0_14),
            "age_60_64": p60_64,
            "age_65_plus": p65,
        }

        expected = sum(rates[g] * pa[g] / 1000.0 for g in GROUPS)
        # Reference uses the SAME perturbed rates on the 2019 structure, so the
        # identity closes exactly per draw.
        e_ref = sum(rates[g] * p19[g] / 1000.0 for g in GROUPS)

        reg = float(reg_by_year[year])
        total_deaths = reg * dfac
        rate_effect = total_deaths - expected
        size_effect = (p_tot - pop19) * e_ref / pop19
        struct_size = sum(rates[g] * (pa[g] - p19[g]) / 1000.0 for g in GROUPS)
        ageing_effect = struct_size - size_effect
        excess_draws[year] = rate_effect

        def q(x: np.ndarray) -> dict[str, int]:
            lo, med, hi = np.percentile(x, [5, 50, 95])
            return {"p05": round(float(lo)), "median": round(float(med)),
                    "p95": round(float(hi))}

        results.append({
            "year": year,
            "age_structure_source": "ONEI 3.3 observed" if year <= OBSERVED_THROUGH
            else "cohort projection from 2022",
            "registered_deaths": int(reg),
            "total_deaths_incl_unregistered": q(total_deaths),
            "expected_deaths_2019_schedule": q(expected),
            "population_60_plus_median": int(round(float(np.median(p60_64 + p65)))),
            "excess_vs_2019_schedule": q(rate_effect),
            "excess_per_100k_official_stock": round(
                float(np.median(rate_effect)) / _midyear(OFFICIAL_END_M, year) * 1e5, 1),
            "ageing_effect_vs_2019": q(ageing_effect),
            "population_size_effect_vs_2019": q(size_effect),
            "unregistered_deaths": q(total_deaths - reg),
            "identity_residual_median": round(float(np.median(
                (total_deaths - e_ref) - (size_effect + ageing_effect + rate_effect)))),
            "share_of_death_rise_from_ageing_pct": round(
                float(100.0 * np.median(ageing_effect)
                      / max(np.median(ageing_effect) + np.median(rate_effect), 1.0)), 1),
        })

    def _cum(lo: int, hi: int) -> dict[str, int]:
        tot = sum(v for y, v in excess_draws.items() if lo <= y <= hi)
        p05, med, p95 = np.percentile(tot, [5, 50, 95])
        return {"p05": int(round(p05)), "median": int(round(med)), "p95": int(round(p95))}

    return {
        "method": "indirect age standardisation on {0-14, 15-59, 60-64, 65+}; "
                  "2019 rates from ONEI 3.15 deaths over ONEI 3.3 mid-year "
                  "population; age structure observed 2019-2022 and cohort-"
                  "projected 2023-2026",
        "n_draws": N,
        "seed": SEED,
        "base_year": BASE_YEAR,
        "base_2019": {
            "total_deaths": int(round(base["total_deaths"])),
            "mid_year_population": int(round(base["pop_total"])),
            "cdr_per_1000": round(base["cdr_per_1000"], 3),
            "share_of_deaths_at_60_plus_pct": round(base["share_deaths_60_plus_pct"], 1),
            "rates_per_1000": {g: round(v, 3) for g, v in base["rates_per_1000"].items()},
            "population_by_group": {g: int(round(v)) for g, v in base["pops"].items()},
        },
        "baseline_sensitivity": _baseline_sensitivity(base),
        # The 8% elderly-emigrant share is an expert prior and it is load-bearing:
        # it is NOT a "held fixed" elderly count. Values recomputed by rerunning
        # this script with claims.selectivity.emigrants_60_plus_pct set to 0/8/16.
        "elderly_share_sensitivity": _elderly_share_sensitivity()
        if with_sensitivity else None,
        "counterfactual_sensitivity": counterfactual_sensitivity(
            base,
            [r for r in results if r["year"] == 2025][0][
                "expected_deaths_2019_schedule"]["median"],
            float(reg_by_year[2025]),
            float(np.median(dfac)),
            {r["year"]: r["expected_deaths_2019_schedule"]["median"] for r in results},
            {y: float(reg_by_year[y]) for y in YEARS}),
        "by_year": results,
        "cumulative_excess": {
            "2020_2025": _cum(2020, 2025),
            "2021_2025": _cum(2021, 2025),
            "2022_2025_post_covid": _cum(2022, 2025),
            "2024_2025": _cum(2024, 2025),
        },
        "caveats": [
            "Age structure is observed only through 2022 (ONEI 3.3); 2023-2026 is a "
            "cohort projection whose error grows with horizon and is carried as an "
            "explicit noise term.",
            "The 2019 baseline embeds no counterfactual improvement in Cuban "
            "mortality after 2019.",
            "Excess deaths against the 2019 schedule are an association with the crisis period, not a "
            "cause-of-death attribution; blackouts, arboviruses, drug shortages and "
            "delayed care are not separately identified.",
            "Registered deaths for 2026 are a scenario continuation (+4% on 2025).",
            "Dfac is shared with Model D, so this is not independent of the headcount.",
        ],
    }


def main() -> None:
    out = run()
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    b = out["base_2019"]
    print(f"2019: {b['total_deaths']:,} deaths on {b['mid_year_population']:,} mid-year "
          f"population, CDR {b['cdr_per_1000']:.2f}, {b['share_of_deaths_at_60_plus_pct']}% at 60+")
    print(f"  rates/1000: {b['rates_per_1000']}")
    print(f"{'yr':>5} {'src':>10} {'reg':>8} {'60+pop':>10} {'expected':>9} "
          f"{'size':>8} {'ageing':>8} {'excess (range)':>24} {'resid':>6}")
    for r in out["by_year"]:
        a = r["excess_vs_2019_schedule"]
        print(f"{r['year']:>5} {'obs' if 'observed' in r['age_structure_source'] else 'proj':>10} "
              f"{r['registered_deaths']:>8,} {r['population_60_plus_median']:>10,} "
              f"{r['expected_deaths_2019_schedule']['median']:>9,} "
              f"{r['population_size_effect_vs_2019']['median']:>8,} "
              f"{r['ageing_effect_vs_2019']['median']:>8,} "
              f"{a['median']:>8,} [{a['p05']:,}–{a['p95']:,}]".ljust(24)
              + f" {r['identity_residual_median']:>6}")
    print("\ncumulative excess vs the 2019 age-specific schedule:")
    for k, v in out["cumulative_excess"].items():
        print(f"  {k}: {v['median']:,} [{v['p05']:,}–{v['p95']:,}]")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
