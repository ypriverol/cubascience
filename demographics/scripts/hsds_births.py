# -*- coding: utf-8 -*-
"""True births B*_t under selective exit and crisis fertility × g(S_t)."""
from __future__ import annotations

import json

import numpy as np

from constants import ARTIFACTS, get_claims
from hsds_features import BIRTHS
from hsds_score import score_years

OUT = ARTIFACTS / "model_e_births.json"
YEARS = list(range(2022, 2026))

# Registered births are a strong anchor; allow modest under/over vs register.
TFR_PATH = {
    2022: 1.45,
    2023: 1.40,
    2024: 1.33,
    2025: 1.29,
}
TFR_2019 = 1.60


def estimate_births(n: int = 50_000, seed: int = 2027) -> dict:
    claims = get_claims()
    tfr_floor = float(claims["vital"]["tfr_2025"])
    scores = score_years(n_boot=400, seed=seed).set_index("year")
    s2019 = float(scores.loc[2019, "S_median"])
    rng = np.random.default_rng(seed + 1)

    # Extra TFR depression from deterioration (small; register already shows collapse)
    beta = rng.uniform(0.0, 0.12, n)
    # Registration completeness for births (near 1)
    reg_c = rng.uniform(0.97, 1.03, n)

    years_out = []
    for year in YEARS:
        s = float(scores.loc[year, "S_median"])
        s_lo = float(scores.loc[year, "S_p05"])
        s_hi = float(scores.loc[year, "S_p95"])
        s_draw = rng.uniform(s_lo, s_hi, n)
        denom = max(1.0 - s2019, 1e-3)
        g = 1.0 - beta * np.clip((s_draw - s2019) / denom, 0.0, 1.0)
        tfr_star = np.maximum(TFR_PATH[year] * g, tfr_floor * 0.95)
        # Scale registered births by TFR* / TFR_path and registration factor
        b_reg = float(BIRTHS[year])
        b_star = b_reg * (tfr_star / TFR_PATH[year]) * reg_c
        years_out.append(
            {
                "year": year,
                "B_reg": b_reg,
                "TFR_path": TFR_PATH[year],
                "B_star": {
                    "p05": float(np.percentile(b_star, 5)),
                    "median": float(np.percentile(b_star, 50)),
                    "p95": float(np.percentile(b_star, 95)),
                },
                "TFR_star_median": float(np.median(tfr_star)),
                "S_median": s,
            }
        )

    payload = {
        "n": n,
        "seed": seed,
        "tfr_2019_anchor": TFR_2019,
        "tfr_floor": tfr_floor,
        "years": years_out,
        "sum_B_star_2022_2025_median": float(
            sum(y["B_star"]["median"] for y in years_out)
        ),
        "sum_B_reg_2022_2025": float(sum(y["B_reg"] for y in years_out)),
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    p = estimate_births()
    for y in p["years"]:
        print(
            f"{y['year']}: B*={y['B_star']['median']:.0f} "
            f"[{y['B_star']['p05']:.0f},{y['B_star']['p95']:.0f}] "
            f"vs reg {y['B_reg']:.0f}; TFR*={y['TFR_star_median']:.2f}"
        )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
