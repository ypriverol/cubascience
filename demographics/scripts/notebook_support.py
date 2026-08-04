"""Shared constants and light Monte Carlo helpers for demographics.ipynb."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta as beta_dist
from scipy.stats import norm

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from constants import FIGURES, ROOT, get_claims, model_d_anchors  # noqa: E402

_claims = get_claims()
_v = _claims["vital"]

OFFICIAL_2019 = int(_v["official_pop_2019"])
BIRTHS_2020_25 = int(_v["births_2020_2025"])
DEATHS_2020_25 = int(_v["deaths_2020_2025_registered"])
R_MIG_ONEI = int(_v["onei_net_mig_2020_2025"])

ANCHORS = model_d_anchors(_claims)

TRIANGULATION = [
    (row["source"], row["estimate"], row["role"])
    for row in _claims["triangulation"]["sources"]
]

# `models_summary` was removed from claims.yaml when the A-E model set was
# replaced by the four scenarios. Read the live scenarios instead, so the
# notebook cannot ship a table the paper no longer stands behind.
MODEL_SUMMARY = [
    (
        s["label"],
        s.get("note", "").split(".")[0],
        s["gap_m"],
        s["gap_pct"],
        s["pop_end_2025_m"],
    )
    for key, s in _claims["population_scenarios"]["scenarios"].items()
]


def run_model_a(n: int = 100_000, seed: int = 42) -> dict[str, np.ndarray]:
    """Conservative Monte Carlo (Model A style). Paper uses n=2e5."""
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


__all__ = [
    "ANCHORS",
    "FIGURES",
    "MODEL_SUMMARY",
    "OFFICIAL_2019",
    "ROOT",
    "TRIANGULATION",
    "run_model_a",
    "summarize",
]
