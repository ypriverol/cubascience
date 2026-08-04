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
OFFICIAL_2021 = 11_113_215  # official end-2021 stock: the single base the paper uses
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


def run_model_a(n: int | None = None, seed: int | None = None) -> dict[str, np.ndarray]:
    """
    Conservative-scenario spread, delegated to the shipped pipeline.

    This used to be a hand-rolled recreation: a Gaussian copula (rho=0.5) over a
    2019 base with its own priors. It printed a median of 9.05 M -- a figure in
    no scenario -- labelled a "90% CI", which is the one label the paper forbids.
    Recreations drift; the notebook now runs the same code the paper does, so it
    cannot disagree with it.
    """
    import model_population as mp

    rng = np.random.default_rng(mp.SEED if seed is None else seed)
    s = mp.SCENARIOS["conservative"]
    b = mp.band(s, rng)
    draws = rng.random(0)  # kept for signature compatibility; unused
    del draws
    p2025 = np.array([b["pop_end_2025_p05"], b["pop_end_2025_median"],
                      b["pop_end_2025_p95"]])
    decline = mp.P2021 - p2025
    return {
        "decline": decline,
        "pct": 100 * decline / mp.P2021,
        "p2025": p2025,
        "mig": np.array([mp.R * (1 + mp._mean(*s["M"]))]),
        "note": "conservative scenario, prior-predictive spread (NOT a confidence "
                "interval; no coverage property)",
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
