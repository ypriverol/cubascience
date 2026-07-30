"""Shared constants and light Monte Carlo helpers for demographics.ipynb."""
from __future__ import annotations

import numpy as np
from scipy.stats import beta as beta_dist
from scipy.stats import norm

OFFICIAL_2019 = 11_193_470
BIRTHS_2020_25 = 105_038 + 99_096 + 95_403 + 90_392 + 71_374 + 68_064
DEATHS_2020_25 = 112_439 + 167_645 + 120_098 + 117_739 + 128_098 + 136_214
R_MIG_ONEI = 15_000 + 1_005_006 + 251_221 + 245_264

ANCHORS = {
    "population_end_2025_model_d_m": 8.56,
    "loss_vs_2019_m": 2.31,
    "loss_vs_2019_pct": 21.3,
    "births_2025": 68_064,
    "deaths_2025": 136_214,
    "natural_balance_2025": -68_149,
    "tfr_2025": 1.29,
    "pct_age_60_plus": 26.7,
    "median_age": 45,
    "excess_deaths_2024_25_low": 40_000,
    "excess_deaths_2024_25_high": 60_000,
    "onei_end_2025": 9_434_593,
}

TRIANGULATION = [
    ("UN (stale migration)", 10.90, "ceiling"),
    ("MINSAP denominator", 10.24, "ceiling"),
    ("Electoral roll (level)", 10.00, "ceiling"),
    ("ONEI official", 9.43, "official"),
    ("Housing × occupancy", 8.70, "occupancy"),
    ("Albizu-Campos (2023)", 8.62, "independent"),
    ("This study (Model D)", 8.56, "preferred"),
    ("Albizu-Campos (2024)", 8.03, "independent"),
]

MODEL_SUMMARY = [
    ("A · conservative", "ONEI-anchored", 1.93, 17.6, 9.06),
    ("B · crisis-adjusted", "under-reg. + independent emigration", 2.31, 21.3, 8.54),
    ("C · worst case", "analog-calibrated upper bound", 2.53, 23.5, 8.24),
    ("D · sentinel ★", "IMR sentinel + triangulation", 2.31, 21.3, 8.56),
]


def run_model_a(n: int = 100_000, seed: int = 42) -> dict[str, np.ndarray]:
    """Conservative Monte Carlo (Model A style). Paper uses n=1_000_000."""
    rng = np.random.default_rng(seed)
    z = rng.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], size=n)
    u1, u2 = norm.cdf(z[:, 0]), norm.cdf(z[:, 1])
    b = beta_dist.ppf(u1, 1.5, 3.0)
    b2 = beta_dist.ppf(u2, 1.0, 3.5)
    u0 = 620_000 * b
    m = 1 + 0.55 * b2
    births = BIRTHS_2020_25 * rng.normal(1.0, 0.01, n)
    dmult = np.clip(rng.normal(1.015, 0.012, n), 0.99, 1.06)
    deaths = DEATHS_2020_25 * dmult
    mig = R_MIG_ONEI * m
    decline = (deaths - births) + mig
    base_true = OFFICIAL_2019 - u0
    return {
        "decline": decline,
        "pct": 100 * decline / base_true,
        "p2025": base_true - decline,
        "mig": mig,
    }


def summarize(x: np.ndarray) -> dict[str, float]:
    q = np.percentile(x, [5, 50, 95])
    return {"p05": float(q[0]), "median": float(q[1]), "p95": float(q[2])}
