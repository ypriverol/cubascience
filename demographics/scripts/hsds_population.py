# -*- coding: utf-8 -*-
"""Model E: population from reconstructed births, deaths, and Model-D-like migration."""
from __future__ import annotations

import json

import numpy as np
from scipy.stats import beta as beta_dist

from constants import ARTIFACTS, get_claims
from hsds_births import estimate_births
from hsds_deaths import estimate_deaths
from hsds_features import BIRTHS, DEATHS
from hsds_score import score_years

OUT = ARTIFACTS / "model_e_summary.json"

OFFICIAL_2021 = 11_113_215
OFFICIAL_2025 = 9_434_593
# Identity-consistent ONEI net emigration 2022–2025 (same as model_from_2021)
BIRTHS_SUM = 325_233
DEATHS_SUM = 502_149
R_MIG = OFFICIAL_2021 + BIRTHS_SUM - DEATHS_SUM - OFFICIAL_2025  # 1_501_706
YEARS = list(range(2022, 2026))


def run_model_e(n: int = 100_000, seed: int = 2027) -> dict:
    """
    P*_2025 = (P_off_2021 − U0) + Σ (B*_t − D*_t − M*_t)
    M* uses Model D migration bridge (beta uplift on R_MIG) with mild S correlation.
    """
    claims = get_claims()
    rng = np.random.default_rng(seed)

    # Draw yearly B* and D* medians as centers; sample around artifact bands
    deaths = estimate_deaths(n=max(5_000, n // 10), seed=seed)
    births = estimate_births(n=max(5_000, n // 10), seed=seed)
    scores = score_years(n_boot=300, seed=seed).set_index("year")
    s2019 = float(scores.loc[2019, "S_median"])

    # U0 baseline overstatement (Model D scale)
    U0 = 80_000 * beta_dist.rvs(2.0, 5.0, size=n, random_state=rng)

    # Migration multiplier (Model D-like)
    Mfac = 1.0 + 0.55 * beta_dist.rvs(2.0, 3.5, size=n, random_state=rng)
    # Correlate higher late-period S with slightly more exit
    s_late = float(np.mean([scores.loc[y, "S_median"] for y in (2023, 2024, 2025)]))
    Mfac = Mfac * (1.0 + 0.08 * max(s_late - s2019, 0.0) * rng.uniform(0.5, 1.5, n))
    mig_total = R_MIG * Mfac

    # Allocate migration across years proportional to registered natural decrease pressure
    nat_reg = np.array([DEATHS[y] - BIRTHS[y] for y in YEARS], dtype=float)
    nat_reg = np.maximum(nat_reg, 1.0)
    mig_w = nat_reg / nat_reg.sum()

    b_med = {y["year"]: y["B_star"]["median"] for y in births["years"]}
    d_med = {y["year"]: y["D_star"]["median"] for y in deaths["years"]}
    b_p05 = {y["year"]: y["B_star"]["p05"] for y in births["years"]}
    b_p95 = {y["year"]: y["B_star"]["p95"] for y in births["years"]}
    d_p05 = {y["year"]: y["D_star"]["p05"] for y in deaths["years"]}
    d_p95 = {y["year"]: y["D_star"]["p95"] for y in deaths["years"]}

    p = OFFICIAL_2021 - U0
    sum_b = np.zeros(n)
    sum_d = np.zeros(n)
    for i, year in enumerate(YEARS):
        b = rng.uniform(b_p05[year], b_p95[year], n)
        d = rng.uniform(d_p05[year], d_p95[year], n)
        m = mig_total * mig_w[i]
        p = p + b - d - m
        sum_b += b
        sum_d += d

    p2025 = p
    decline = (OFFICIAL_2021 - U0) - p2025
    pct = 100.0 * decline / (OFFICIAL_2021 - U0)
    mig_share = 100.0 * mig_total / np.maximum(decline, 1.0)
    nat_share = 100.0 * (sum_d - sum_b) / np.maximum(decline, 1.0)

    # 2026 nowcast (same spirit as Model D)
    b26 = 65_682 * rng.normal(1.0, 0.03, n)
    d26 = 136_214 * 1.04 * rng.normal(1.0, 0.05, n)
    # mild S uplift on 2026 deaths
    s25 = float(scores.loc[2025, "S_median"])
    d26 = d26 * (1.0 + 0.10 * max(s25 - s2019, 0.0))
    reg = rng.choice([0, 1, 2], size=n, p=[0.35, 0.35, 0.30])
    m26 = np.select(
        [reg == 0, reg == 1, reg == 2],
        [150_000, 210_000, 300_000],
    ).astype(float) * rng.normal(1.0, 0.15, n)
    p2026 = p2025 - (d26 - b26) - m26

    def summ(x: np.ndarray) -> dict:
        q = np.percentile(x, [5, 50, 95])
        return {"p05": float(q[0]), "median": float(q[1]), "p95": float(q[2])}

    payload = {
        "model": "E",
        "label": "vital reconstruction (HSDS)",
        "n": n,
        "seed": seed,
        "anchors": {
            "official_2021": OFFICIAL_2021,
            "R_mig_onei_consistent": R_MIG,
            "B_reg_2022_2025": BIRTHS_SUM,
            "D_reg_2022_2025": DEATHS_SUM,
        },
        "pop_2025": summ(p2025),
        "pop_2026": summ(p2026),
        "decline_2021_2025": summ(decline),
        "pct_corrected_base": summ(pct),
        "mig_share_median": float(np.median(mig_share)),
        "natural_decrease_share_median": float(np.median(nat_share)),
        "u0_median": float(np.median(U0)),
        "sum_B_star_median": float(np.median(sum_b)),
        "sum_D_star_median": float(np.median(sum_d)),
        "mig_median": float(np.median(mig_total)),
        "loss_vs_official_2021_end_2026_pct": float(
            100.0 * (OFFICIAL_2021 - np.median(p2026)) / OFFICIAL_2021
        ),
        "births_artifact": {
            "sum_median": births["sum_B_star_2022_2025_median"],
            "sum_reg": births["sum_B_reg_2022_2025"],
        },
        "deaths_artifact": {
            "sum_median": deaths["sum_D_star_2022_2025_median"],
            "sum_reg": deaths["sum_D_reg_2022_2025"],
        },
        "preferred_public_model_still": claims["meta"]["preferred_model"],
        "note": "Model E is provisional beside A–D until Task 8 adversarial gate.",
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    p = run_model_e()
    print(
        f"E: loss {p['decline_2021_2025']['median']/1e6:.2f}M "
        f"({p['pct_corrected_base']['median']:.1f}%) | "
        f"pop2025 {p['pop_2025']['median']/1e6:.2f}M | "
        f"pop2026 {p['pop_2026']['median']/1e6:.2f}M | "
        f"mig share {p['mig_share_median']:.0f}% | "
        f"nat share {p['natural_decrease_share_median']:.0f}% | "
        f"vs off 2021 by 2026 −{p['loss_vs_official_2021_end_2026_pct']:.1f}%"
    )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
