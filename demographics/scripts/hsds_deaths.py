# -*- coding: utf-8 -*-
"""True deaths D*_t from ageing schedule × decadence uplift f(S_t)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from constants import ARTIFACTS, DATA, get_claims
from hsds_features import DEATHS, POP_END
from hsds_score import score_years
from mortality_data import age_structure_shares

OUT = ARTIFACTS / "model_e_deaths.json"
YEARS = list(range(2022, 2026))


def _elderly_share(year: int, age: pd.DataFrame, rem60: float) -> float:
    if year in age.index:
        return float(age.loc[year, "age_60_plus_pct"]) / 100.0
    if year >= 2025:
        return rem60 / 100.0
    # interpolate 2022 → 2025 for 2023–2024
    y0, y1 = 2022, 2025
    s0 = float(age.loc[y0, "age_60_plus_pct"]) / 100.0 if y0 in age.index else 0.223
    s1 = rem60 / 100.0
    return s0 + (s1 - s0) * (year - y0) / (y1 - y0)


def estimate_deaths(n: int = 50_000, seed: int = 2027) -> dict:
    """
    Expected_from_ageing_t ≈ D_2019 × (P_t/P_2019) × (e60_t/e60_2019)
    Decadence_uplift_t = 1 + α × ((S_t − S_2019) / (1 − S_2019)_+)
    D*_t = Expected × uplift × ε
    """
    claims = get_claims()
    rem60 = float(claims["selectivity"]["pct_age_60_plus_remaining"])
    age = age_structure_shares().set_index("year")
    scores = score_years(n_boot=400, seed=seed).set_index("year")
    s2019 = float(scores.loc[2019, "S_median"])
    e2019 = _elderly_share(2019, age, rem60)
    p2019 = POP_END[2019]
    d2019 = DEATHS[2019]

    rng = np.random.default_rng(seed)
    # α: how strongly deterioration lifts mortality beyond ageing (prior)
    alpha = rng.uniform(0.15, 0.55, n)
    eps = rng.normal(1.0, 0.04, n)

    years_out = []
    for year in YEARS:
        s = float(scores.loc[year, "S_median"])
        s_lo = float(scores.loc[year, "S_p05"])
        s_hi = float(scores.loc[year, "S_p95"])
        # sample S within band
        s_draw = rng.uniform(s_lo, s_hi, n)
        e60 = _elderly_share(year, age, rem60)
        pop = 0.5 * (POP_END[year - 1] + POP_END[year])
        expected = d2019 * (pop / p2019) * (e60 / e2019)
        denom = max(1.0 - s2019, 1e-3)
        uplift = 1.0 + alpha * np.clip((s_draw - s2019) / denom, 0.0, None)
        d_star = expected * uplift * eps
        d_reg = float(DEATHS[year])
        # 2023 canonical in claims slightly differs from Anuario footnote
        if year == 2023:
            d_reg = float(claims["meta"].get("deaths_2023_canonical", d_reg))
        hidden = np.maximum(d_star - d_reg, 0.0)

        years_out.append(
            {
                "year": year,
                "D_reg": d_reg,
                "expected_ageing_point": float(expected),
                "D_star": {
                    "p05": float(np.percentile(d_star, 5)),
                    "median": float(np.percentile(d_star, 50)),
                    "p95": float(np.percentile(d_star, 95)),
                },
                "H_hidden": {
                    "p05": float(np.percentile(hidden, 5)),
                    "median": float(np.percentile(hidden, 50)),
                    "p95": float(np.percentile(hidden, 95)),
                },
                "S_median": s,
            }
        )

    payload = {
        "n": n,
        "seed": seed,
        "method": "ageing_scaled_2019_schedule × f(S_t) uplift",
        "years": years_out,
        "sum_D_star_2022_2025_median": float(
            sum(y["D_star"]["median"] for y in years_out)
        ),
        "sum_D_reg_2022_2025": float(sum(y["D_reg"] for y in years_out)),
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    p = estimate_deaths()
    for y in p["years"]:
        print(
            f"{y['year']}: D*={y['D_star']['median']:.0f} "
            f"[{y['D_star']['p05']:.0f},{y['D_star']['p95']:.0f}] "
            f"vs reg {y['D_reg']:.0f}; H_med={y['H_hidden']['median']:.0f}"
        )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
