#!/usr/bin/env python3
"""
Population scenarios, end-2021 -> end-2026. Simplified replacement for
model_from_2021.py.

What changed and why
--------------------
The previous version ran 10^6 Monte Carlo draws with a Gaussian copula over five
prior sets and reported a median to four significant figures. Testing showed the
median was reproducible to 0.05% (4,253 people) by plugging three prior medians
into the accounting identity: the simulation was computing a point estimate that
is pure arithmetic, plus a band the paper then told readers not to use.

So:
  * The point estimate is now stated as the arithmetic it always was.
  * The copula is gone. It moved the median by ~2,200 people and only widened a
    band that is not the primary uncertainty statement. Twelve correlation
    parameters, no effect on anything reported.
  * Model B is gone: it landed within 0.02 M of Model D, i.e. the same scenario
    with different dials.
  * Model E is gone: see hsds_* scripts, retired in favour of
    attributable_mortality.py, which estimates the same quantity from observed
    age-specific data instead of a hand-weighted dimensionless index.
  * Loss is reported on ONE base: the official end-2021 stock. The previous dual
    headline (-20.5% on a corrected base, ~25% on the official base) cost several
    paragraphs of defensive explanation and was self-inflicted.

Three scenarios remain, and each earns its place:
  FLOOR    ONEI-anchored (M ~ 1). The conservative end.
  CENTRAL  crisis-adjusted, migration prior above ONEI, small residual
           death under-registration bounded by the register's own behaviour.
  UPPER    stress case. Defines the top of the envelope.

A small Monte Carlo is retained ONLY to produce the within-scenario spread, which
is labelled as prior-predictive and is not the primary uncertainty statement.
The across-scenario envelope is.

Outputs ``artifacts/population_scenarios.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta as beta_dist

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import ARTIFACTS  # noqa: E402

OUT = ARTIFACTS / "population_scenarios.json"

N = 200_000          # only for the band; the point estimate is closed form
SEED = 2027

# ONEI anchors, 2022-2025 window.
P2021 = 11_113_215
BIRTHS = 325_233
DEATHS = 502_149
R = 1_501_706        # identity-consistent ONEI net emigration

# Scenario = three numbers. U0 = end-2021 roll overstatement (people already
# abroad but still counted); M = multiplier on ONEI net emigration;
# Dfac = residual death under-registration.
SCENARIOS = {
    "null": {
        "label": "Null (ONEI at face value)",
        "U0": (1e-9, 1.0, 1.0), "M": (1e-9, 1.0, 1.0), "D": (1e-9, 1.0, 1.0),
        "note": "U0=0, M=1, Dfac=1. Reproduces ONEI's published end-2025 figure "
                "exactly, because R is defined as the residual that closes the "
                "identity. Included so the envelope does not exclude the "
                "official series by construction.",
    },
    "conservative": {
        "label": "Conservative",
        "U0": (450_000, 1.5, 3.0), "M": (0.40, 1.0, 3.5), "D": (0.06, 2.0, 3.0),
        "note": "Adds a modest correction. NOT 'M approx 1': its median M is "
                "1.072, i.e. 7% more emigration than ONEI reports.",
    },
    "central": {
        "label": "Crisis-adjusted central",
        "U0": (700_000, 2.0, 2.4), "M": (0.72, 2.2, 2.4), "D": (0.09, 1.8, 3.2),
        "note": "Migration prior above ONEI; death under-registration capped at "
                "9%, just above the 7.5% the register itself shed in 2022.",
    },
    "upper": {
        "label": "Upper stress",
        "U0": (800_000, 2.4, 1.9), "M": (0.80, 2.4, 2.2), "D": (0.16, 2.2, 2.4),
        "note": "Defines the top of the envelope.",
    },
}

# End-2026 continuation: births, a 4% death lift, and a three-regime migration
# mixture. Scenario assumptions, not a forecast.
B26 = 65_682
D26_LIFT = 1.04
MIG26 = (150_000, 210_000, 300_000)
MIG26_P = (0.35, 0.35, 0.30)


def _mean(scale: float, a: float, b: float) -> float:
    """
    Beta mean, not median. P_2025 is LINEAR in (U0, M, Dfac), so the mean
    plug-in is exact -- it equals the Monte Carlo mean identically. The median
    plug-in is not exact and was off by 23,354 people in the conservative
    scenario, contradicting the 0.05% agreement the Methods claimed.
    """
    return scale * a / (a + b)


def closed_form(s: dict) -> dict:
    """The point estimate: three medians and the accounting identity."""
    U0 = _mean(*s["U0"])
    M = 1 + _mean(*s["M"])
    Dfac = 1 + _mean(*s["D"])
    deaths = DEATHS * Dfac
    mig = R * M
    natural = deaths - BIRTHS
    p2025 = P2021 - U0 - natural - mig
    # ONE base: the official end-2021 stock. The gap has three parts and they sum.
    gap = P2021 - p2025
    d26 = 136_214 * D26_LIFT * Dfac
    mig26 = sum(p * m for p, m in zip(MIG26_P, MIG26))
    p2026 = p2025 - (d26 - B26) - mig26
    return {
        "U0": U0, "M": M, "Dfac": Dfac,
        "pop_end_2025": p2025, "pop_end_2026": p2026,
        "gap_vs_official_2021": gap,
        "gap_pct": 100 * gap / P2021,
        "components": {
            "baseline_overstatement_U0": U0,
            "net_emigration_2022_2025": mig,
            "natural_decrease": natural,
        },
        "emigration_share_of_gap_pct": 100 * (mig + U0) / gap,
        "flow_emigration_share_pct": 100 * mig / (mig + natural),
    }


def band(s: dict, rng: np.random.Generator) -> dict:
    """Within-scenario prior spread. Independent margins: no copula."""
    U0 = s["U0"][0] * beta_dist.ppf(rng.random(N), s["U0"][1], s["U0"][2])
    M = 1 + s["M"][0] * beta_dist.ppf(rng.random(N), s["M"][1], s["M"][2])
    Dfac = 1 + s["D"][0] * beta_dist.ppf(rng.random(N), s["D"][1], s["D"][2])
    births = BIRTHS * rng.normal(1, 0.01, N)
    p2025 = P2021 - U0 - (DEATHS * Dfac - births) - R * M
    gap = P2021 - p2025
    q = np.percentile(p2025, [5, 50, 95])
    mean_p = float(p2025.mean())
    qg = np.percentile(gap, [5, 50, 95])
    return {
        "pop_end_2025_p05": float(q[0]), "pop_end_2025_median": float(q[1]),
        "pop_end_2025_p95": float(q[2]), "pop_end_2025_mean": mean_p,
        "gap_p05": float(qg[0]), "gap_p95": float(qg[2]),
    }


def main() -> None:
    rng = np.random.default_rng(SEED)
    out = {}
    for key, s in SCENARIOS.items():
        cf = closed_form(s)
        bd = band(s, rng)
        cf["band"] = bd
        cf["closed_form_vs_mc_mean"] = round(cf["pop_end_2025"] - bd["pop_end_2025_mean"])
        cf["label"] = s["label"]
        cf["note"] = s["note"]
        out[key] = cf

    gaps = [out[k]["gap_vs_official_2021"] for k in out if k != "null"]
    envelope = {
        "gap_low_m": round(min(gaps) / 1e6, 2),
        "gap_high_m": round(max(gaps) / 1e6, 2),
        "pct_low": round(100 * min(gaps) / P2021, 1),
        "pct_high": round(100 * max(gaps) / P2021, 1),
        "statement": "Range across the three assumption sets. This is NOT a "
                     "confidence interval and has no coverage property: it is "
                     "the span of three chosen scenarios. The null scenario "
                     "(ONEI at face value) sits BELOW it at zero added "
                     "correction and is reported separately.",
    }

    report = {
        "base": "official end-2021 stock, 11,113,215 — one base, no corrected variant",
        "window": "end-2021 -> end-2025 (+ end-2026 continuation)",
        "point_estimates": "closed form: three prior MEANS in the accounting identity (exact by linearity)",
        "band_draws": N,
        "copula": "none — independent margins",
        "retired": {
            "model_B": "landed within 0.02 M of the central scenario",
            "model_E": "dominated by attributable_mortality.py",
            "gaussian_copula": "moved the median ~2,200 people; widened an unused band",
            "corrected_base": "dual headline removed; one base only",
        },
        "scenarios": out,
        "envelope": envelope,
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Population scenarios — base: official end-2021 (11,113,215)\n")
    print(f"{'scenario':<26}{'pop 2025':>11}{'gap':>10}{'gap %':>8}"
          f"{'pop 2026':>11}{'emig share':>12}{'cf-mc':>8}")
    print("-" * 86)
    for k, v in out.items():
        print(f"{v['label']:<26}{v['pop_end_2025']/1e6:>10.2f}M{v['gap_vs_official_2021']/1e6:>9.2f}M"
              f"{v['gap_pct']:>7.1f}%{v['pop_end_2026']/1e6:>10.2f}M"
              f"{v['emigration_share_of_gap_pct']:>11.0f}%{v['closed_form_vs_mc_mean']:>8,}")
    e = envelope
    print(f"\nENVELOPE (primary statement): gap {e['gap_low_m']}–{e['gap_high_m']} M "
          f"({e['pct_low']}–{e['pct_high']}% of the official 2021 stock)")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
