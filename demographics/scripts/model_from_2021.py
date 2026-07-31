#!/usr/bin/env python3
"""
Monte Carlo from end-2021 → end-2025 (+ 2026 nowcast).

Same Model D sentinel logic as model_d.py, but the accounting window starts at
ONEI end-2021 (11,113,215) and covers registered vital events / net migration
for 2022–2025. This matches the shorter public timeline (five years to end-2026).
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
from scipy.stats import norm, beta as beta_dist

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS  # noqa: E402

ARTIFACTS.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(2027)
N = 1_000_000

# --- anchors (ONEI / Anuario; 2023 deaths = claims canonical 117,739) ---
OFFICIAL_2021 = 11_113_215
OFFICIAL_2025 = 9_434_593
BIRTHS = 95_403 + 90_392 + 71_374 + 68_064  # 2022–2025 = 325,233
DEATHS_REG = 120_098 + 117_739 + 128_098 + 136_214  # 2022–2025 = 502,149
# Identity-consistent ONEI net emigration over 2022–2025
R_MIG = OFFICIAL_2021 + BIRTHS - DEATHS_REG - OFFICIAL_2025  # 1,501,706

assert BIRTHS == 325_233
assert DEATHS_REG == 502_149
assert R_MIG == 1_501_706


def summarize(x: np.ndarray) -> dict[str, float]:
    q = np.percentile(x, [5, 50, 95])
    return {"p05": float(q[0]), "median": float(q[1]), "p95": float(q[2])}


def run_model(
    name: str,
    *,
    u0_scale: float,
    u0_a: float,
    u0_b: float,
    m_span: float,
    m_a: float,
    m_b: float,
    d_span: float,
    d_a: float,
    d_b: float,
    d_floor: float = 1.0,
    pulse_scale: float = 0.0,
    pulse_shape: float = 3.0,
    corr: tuple[float, float, float] = (0.55, 0.30, 0.25),
) -> dict:
    rho01, rho02, rho12 = corr
    cov = np.array(
        [
            [1.0, rho01, rho02],
            [rho01, 1.0, rho12],
            [rho02, rho12, 1.0],
        ]
    )
    z = rng.multivariate_normal([0, 0, 0], cov, N)
    u = norm.cdf(z)
    U0 = u0_scale * beta_dist.ppf(u[:, 0], u0_a, u0_b)
    M = 1.0 + m_span * beta_dist.ppf(u[:, 1], m_a, m_b)
    Dfac = d_floor + d_span * beta_dist.ppf(u[:, 2], d_a, d_b)
    pulse = np.zeros(N) if pulse_scale <= 0 else np.minimum(
        rng.gamma(pulse_shape, pulse_scale, N), 140_000
    )
    births = BIRTHS * rng.normal(1.0, 0.01, N)
    deaths = DEATHS_REG * Dfac + pulse
    mig = R_MIG * M
    decline = (deaths - births) + mig
    base = OFFICIAL_2021 - U0
    p2025 = base - decline
    pct = 100.0 * decline / base
    mig_share = 100.0 * mig / decline

    # 2026 nowcast (same mixture as Model D)
    b26 = 65_682 * rng.normal(1.0, 0.03, N)
    d26 = (136_214 * 1.04 * rng.normal(1.0, 0.03, N)) * Dfac
    reg = rng.choice([0, 1, 2], size=N, p=[0.35, 0.35, 0.30])
    m26 = np.select(
        [reg == 0, reg == 1, reg == 2],
        [150_000, 210_000, 300_000],
    ).astype(float) * rng.normal(1.0, 0.15, N)
    p2026 = p2025 - (d26 - b26) - m26

    out = {
        "name": name,
        "decline": summarize(decline),
        "pct": summarize(pct),
        "pop_2025": summarize(p2025),
        "pop_2026": summarize(p2026),
        "mig_share_median": float(np.median(mig_share)),
        "dfac_median": float(np.median(Dfac)),
        "u0_median": float(np.median(U0)),
        "mig_median": float(np.median(mig)),
        "loss_2026_from_official_2021_pct": float(
            100.0 * (OFFICIAL_2021 - np.median(p2026)) / OFFICIAL_2021
        ),
    }
    print(
        f"{name}: loss {out['decline']['median']/1e6:.2f}M ({out['pct']['median']:.1f}%) | "
        f"pop2025 {out['pop_2025']['median']/1e6:.2f}M | pop2026 {out['pop_2026']['median']/1e6:.2f}M | "
        f"mig share {out['mig_share_median']:.0f}% | "
        f"vs official 2021 by end-2026: −{out['loss_2026_from_official_2021_pct']:.1f}%"
    )
    return out, p2025, p2026, decline


def main() -> None:
    print("=== Monte Carlo end-2021 → end-2025 (N=1e6) ===")
    print(f"OFFICIAL_2021={OFFICIAL_2021:,}  BIRTHS={BIRTHS:,}  DEATHS={DEATHS_REG:,}  R_MIG={R_MIG:,}")

    # A: conservative / ONEI-leaning
    A, *_ = run_model(
        "A",
        u0_scale=450_000,
        u0_a=1.5,
        u0_b=3.0,
        m_span=0.40,
        m_a=1.0,
        m_b=3.5,
        d_span=0.06,
        d_a=2.0,
        d_b=3.0,
        d_floor=1.0,
        corr=(0.50, 0.25, 0.20),
    )
    # B: crisis-adjusted
    B, pB, pB26, dB = run_model(
        "B",
        u0_scale=700_000,
        u0_a=2.2,
        u0_b=2.2,
        m_span=0.72,
        m_a=2.0,
        m_b=2.6,
        d_span=0.14,
        d_a=2.0,
        d_b=2.8,
        pulse_scale=9000,
        pulse_shape=3.0,
        corr=(0.55, 0.35, 0.40),
    )
    # C: worst case
    C, pC, pC26, dC = run_model(
        "C",
        u0_scale=800_000,
        u0_a=2.4,
        u0_b=1.9,
        m_span=0.80,
        m_a=2.4,
        m_b=2.2,
        d_span=0.16,
        d_a=2.2,
        d_b=2.4,
        d_floor=1.02,
        pulse_scale=15000,
        pulse_shape=3.2,
        corr=(0.55, 0.40, 0.45),
    )
    # D: preferred sentinel (tight Dfac)
    D, pD, pD26, dD = run_model(
        "D",
        u0_scale=700_000,
        u0_a=2.0,
        u0_b=2.4,
        m_span=0.72,
        m_a=2.2,
        m_b=2.4,
        d_span=0.09,
        d_a=1.8,
        d_b=3.2,
        corr=(0.55, 0.30, 0.25),
    )

    np.save(ARTIFACTS / "modelD_pop.npy", pD)
    np.save(ARTIFACTS / "modelD_decline.npy", dD)
    np.save(ARTIFACTS / "modelD_pop2026.npy", pD26)
    np.save(ARTIFACTS / "modelB_pop.npy", pB)
    np.save(ARTIFACTS / "modelB_pop2026.npy", pB26)
    np.save(ARTIFACTS / "modelC_pop.npy", pC)
    np.save(ARTIFACTS / "modelC_decline.npy", dC)
    np.save(ARTIFACTS / "modelC_pop2026.npy", pC26)

    def round_m(x: float) -> float:
        return round(x / 1e6, 2)

    def round_pct(x: float) -> float:
        return round(x, 1)

    summary = {
        "window": "end-2021 → end-2025",
        "n": N,
        "seed": 2027,
        "anchors": {
            "official_pop_end_2021": OFFICIAL_2021,
            "official_pop_end_2025": OFFICIAL_2025,
            "births_2022_2025": BIRTHS,
            "deaths_2022_2025_registered": DEATHS_REG,
            "onei_net_mig_2022_2025": R_MIG,
        },
        "models": {
            "A": {
                "loss_m": round_m(A["decline"]["median"]),
                "loss_pct": round_pct(A["pct"]["median"]),
                "pop_end_2025_m": round_m(A["pop_2025"]["median"]),
                "pop_end_2026_m": round_m(A["pop_2026"]["median"]),
            },
            "B": {
                "loss_m": round_m(B["decline"]["median"]),
                "loss_pct": round_pct(B["pct"]["median"]),
                "pop_end_2025_m": round_m(B["pop_2025"]["median"]),
                "pop_end_2026_m": round_m(B["pop_2026"]["median"]),
            },
            "C": {
                "loss_m": round_m(C["decline"]["median"]),
                "loss_pct": round_pct(C["pct"]["median"]),
                "pop_end_2025_m": round_m(C["pop_2025"]["median"]),
                "pop_end_2026_m": round_m(C["pop_2026"]["median"]),
            },
            "D": {
                "loss_m": round_m(D["decline"]["median"]),
                "loss_pct": round_pct(D["pct"]["median"]),
                "pop_end_2025_m": round_m(D["pop_2025"]["median"]),
                "pop_end_2026_m": round_m(D["pop_2026"]["median"]),
                "loss_90_m": [
                    round_m(D["decline"]["p05"]),
                    round_m(D["decline"]["p95"]),
                ],
                "migration_share_pct": round(D["mig_share_median"], 1),
                "one_in_four_end_2026_vs_official_2021_pct": round(
                    D["loss_2026_from_official_2021_pct"], 1
                ),
            },
        },
    }
    (ARTIFACTS / "model_from_2021_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    # Keep model_d_summary.json in sync for notebook/constants consumers
    (ARTIFACTS / "model_d_summary.json").write_text(
        json.dumps(
            {
                "n": N,
                "seed": 2027,
                "window": "end-2021 → end-2025",
                "pop_end_2025": D["pop_2025"],
                "decline": D["decline"],
                "pct_decline": D["pct"],
                "pop_end_2026": D["pop_2026"],
                "loss_2026_median": float(np.median(pD) - np.median(pD26)),
                "p_below_8_5m": float(np.mean(pD < 8.5e6)),
                "pop_end_2025_m_median": D["pop_2025"]["median"] / 1e6,
                "pop_end_2026_m_median": D["pop_2026"]["median"] / 1e6,
                "decline_m_median": D["decline"]["median"] / 1e6,
                "migration_share_pct": D["mig_share_median"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("\nWrote", ARTIFACTS / "model_from_2021_summary.json")


if __name__ == "__main__":
    main()
