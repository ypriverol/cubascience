# -*- coding: utf-8 -*-
"""Build the yearly HSDS feature matrix (value_norm in [0, 1])."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from constants import ARTIFACTS, DATA, get_claims
from mortality_data import age_structure_shares, infant_deaths_by_year

YEARS = list(range(2019, 2026))
SIGNALS = DATA / "mortality_signals.yaml"
OUT_CSV = DATA / "hsds_features.csv"
PUBLIC_MD = ARTIFACTS / "public_health_signals.md"


def _load_signals() -> dict:
    with SIGNALS.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _minmax(x: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.0
    v = (x - lo) / (hi - lo)
    return float(max(0.0, min(1.0, v)))


def _invert(n: float) -> float:
    return float(max(0.0, min(1.0, 1.0 - n)))


# --- Documented anchors (claims + manuscript; Excel fills where available) ---

# Official COVID-attributed deaths (order-of-magnitude public figure ~8.5k cumulative peak era).
# Used only for covid_misuse_ratio_norm integrity feature.
COVID_LABELS_BY_YEAR = {
    2019: 0,
    2020: 150,
    2021: 8000,  # bulk of ~8.5k official COVID labels through peak
    2022: 300,
    2023: 50,
    2024: 20,
    2025: 10,
}

# Mid-year population for CDR (ONEI path used in onei_audit.py)
POP_END = {
    2018: 11_209_000,  # rough pre
    2019: 11_193_470,
    2020: 11_181_595,
    2021: 11_113_215,
    2022: 11_089_511,
    2023: 10_055_968,
    2024: 9_748_007,
    2025: 9_434_593,
}

BIRTHS = {
    2019: 109_000,  # ~pre-crisis order (manuscript ~110k)
    2020: 105_000,
    2021: 99_096,
    2022: 95_403,
    2023: 90_392,
    2024: 71_374,
    2025: 68_064,
}

DEATHS = {
    2019: 109_000,  # near natural balance ~0 in 2019 narrative
    2020: 112_000,
    2021: 167_645,
    2022: 120_108,
    2023: 117_746,
    2024: 128_098,
    2025: 136_214,
}

# IMR per 1000 live births (manuscript: 5.0 → 9.9)
IMR = {
    2019: 5.0,
    2020: 4.9,
    2021: 7.6,
    2022: 7.5,
    2023: 7.1,
    2024: 7.1,
    2025: 9.9,
}

# Independent e0 gap vs ~78 official-era (years): Brønnum-Hansen & Albizu ~71–73 in 2021
E0_GAP = {
    2019: 1.0,
    2020: 3.0,
    2021: 6.0,
    2022: 5.5,
    2023: 5.0,
    2024: 5.5,
    2025: 6.0,
}

# Maternal mortality relative rise vs 2019 (0–1 already scaled for feature)
MMR_RISE = {
    2019: 0.0,
    2020: 0.2,
    2021: 0.7,
    2022: 0.5,
    2023: 0.45,
    2024: 0.55,
    2025: 0.6,
}

# Expert-coded web severity 0–1 (documented in public_health_signals.md)
HEALTHCARE_COLLAPSE = {
    2019: 0.15,
    2020: 0.35,
    2021: 0.75,
    2022: 0.70,
    2023: 0.80,
    2024: 0.90,
    2025: 0.95,
}

EPIDEMIC_PRESSURE = {
    2019: 0.05,
    2020: 0.55,
    2021: 0.95,
    2022: 0.45,
    2023: 0.35,
    2024: 0.40,
    2025: 0.35,
}

# ONEI migration seam / revision opacity (soft 0–1)
SEAM_FLAG = {
    2019: 0.1,
    2020: 0.2,
    2021: 0.3,
    2022: 0.85,  # CBP vs ONEI +991
    2023: 1.0,  # revision dump year
    2024: 0.7,
    2025: 0.65,
}

OPACITY = {
    2019: 0.2,
    2020: 0.35,
    2021: 0.5,
    2022: 0.85,
    2023: 0.9,
    2024: 0.8,
    2025: 0.75,
}


def _median_age_proxy(year: int, claims: dict) -> float:
    """Interpolate median age of stayers from ~38 (2019) to claims median_age_stayers."""
    target = float(claims["selectivity"]["median_age_stayers"])
    return 38.0 + (target - 38.0) * (year - 2019) / (2025 - 2019)


def _fertile_share_proxy(age_15_59_pct: float) -> float:
    """Working-age (15–59) share of total as fertile-adjacent stock proxy."""
    return age_15_59_pct / 100.0


def _covid_misuse_norm(year: int, signals: dict) -> float:
    """log10(all-cause jump or excess proxy / covid labels), then minmax."""
    labels = max(COVID_LABELS_BY_YEAR.get(year, 1), 1)
    # Use excess over 2019 deaths as severity numerator for the year
    excess = max(DEATHS[year] - DEATHS[2019], 1.0)
    if year == 2021:
        excess = max(DEATHS[2021] - DEATHS[2019], 1.0)
    ratio = excess / labels
    feat = signals["buckets"]["bad_reporting"]["features"]["covid_misuse_ratio_norm"]
    lo = float(feat["norm"]["ratio_lo"])
    hi = float(feat["norm"]["ratio_hi"])
    import math

    return _minmax(math.log10(max(ratio, 1e-9)), math.log10(lo), math.log10(hi))


def build_feature_matrix(years: list[int] | None = None) -> pd.DataFrame:
    years = years or YEARS
    signals = _load_signals()
    claims = get_claims()
    age = age_structure_shares().set_index("year")
    # Prefer claims remaining 60+ for 2025 if ONEI projection only
    rem60 = float(claims["selectivity"]["pct_age_60_plus_remaining"])

    # Fill IMR from infant deaths / births when Excel has deaths
    infants = infant_deaths_by_year().set_index("year")

    rows = []
    for year in years:
        # --- ageing ---
        if year in age.index:
            elderly_pct = float(age.loc[year, "age_60_plus_pct"])
            a1559 = float(age.loc[year, "age_15_59_pct"])
        else:
            elderly_pct = rem60 if year >= 2025 else 22.0
            a1559 = 60.0
        if year == 2025:
            elderly_pct = rem60  # Model-D-consistent remaining share

        elderly_share = elderly_pct / 100.0
        fertile_share = _fertile_share_proxy(a1559)
        median_age = _median_age_proxy(year, claims)

        # --- health ---
        imr = IMR[year]
        if year in infants.index and year in BIRTHS and BIRTHS[year] > 0:
            # Prefer rate from 3.16 counts when available
            imr_xls = 1000.0 * float(infants.loc[year, "infant_deaths"]) / BIRTHS[year]
            if year <= 2022:
                imr = imr_xls
        imr_rise = (imr / IMR[2019]) - 1.0

        pop = 0.5 * (POP_END.get(year - 1, POP_END[year]) + POP_END[year])
        cdr = 1000.0 * DEATHS[year] / pop
        cdr_2019 = 1000.0 * DEATHS[2019] / (0.5 * (POP_END[2018] + POP_END[2019]))
        cdr_rise = (cdr / cdr_2019) - 1.0

        raw = {
            "elderly_share_60plus": elderly_share,
            "median_age_proxy": median_age,
            "fertile_women_share_proxy": fertile_share,
            "imr_rise": imr_rise,
            "cdr_rise": cdr_rise,
            "mmr_rise": MMR_RISE[year],
            "e0_gap": E0_GAP[year],
            "healthcare_collapse_web": HEALTHCARE_COLLAPSE[year],
            "epidemic_pressure_web": EPIDEMIC_PRESSURE[year],
            "covid_misuse_ratio_norm": None,  # filled via special norm
            "onei_migration_seam_flag": SEAM_FLAG[year],
            "stats_opacity_vs_independents": OPACITY[year],
        }

        for bucket, bspec in signals["buckets"].items():
            for fid, fspec in bspec["features"].items():
                if fid == "covid_misuse_ratio_norm":
                    value = float("nan")  # unused; value_norm set below
                    value_norm = _covid_misuse_norm(year, signals)
                else:
                    value = float(raw[fid])
                    nrm = fspec.get("norm", {})
                    method = nrm.get("method", "minmax")
                    if method in {"identity", "identity_or_minmax"} and nrm.get("lo") is None:
                        value_norm = _minmax(value, 0.0, 1.0)
                    else:
                        value_norm = _minmax(value, float(nrm["lo"]), float(nrm["hi"]))
                    if fspec.get("invert_for_score"):
                        value_norm = _invert(value_norm)
                rows.append(
                    {
                        "year": year,
                        "bucket": bucket,
                        "feature": fid,
                        "value": value if fid != "covid_misuse_ratio_norm" else float("nan"),
                        "value_norm": value_norm,
                        "weight_default": float(fspec["default_weight"]),
                        "source_note": fspec.get("source", ""),
                    }
                )
    return pd.DataFrame(rows)


def write_public_health_signals_md() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    PUBLIC_MD.write_text(
        """# Public health severity codes (HSDS)

Expert-coded 0–1 yearly scores for web features. Cite-only; not a survey.

## `healthcare_collapse_web`

| Year | Score | Rationale (short) |
|---|---:|---|
| 2019 | 0.15 | Pre-crisis shortages already noted; system still functional |
| 2020 | 0.35 | COVID onset; supply stress |
| 2021 | 0.75 | Peak COVID collapse narratives; oxygen / ICU stress |
| 2022 | 0.70 | Persistent medicine gaps after peak |
| 2023 | 0.80 | Blackouts + staffing exit deepen |
| 2024 | 0.90 | Widespread pharmacy empty-shelf reports |
| 2025 | 0.95 | Continued decadence; IMR spike year |

## `epidemic_pressure_web`

| Year | Score | Rationale (short) |
|---|---:|---|
| 2019 | 0.05 | Baseline |
| 2020 | 0.55 | COVID year 1 |
| 2021 | 0.95 | COVID mortality peak (all-cause) |
| 2022 | 0.45 | Post-peak residual |
| 2023 | 0.35 | Dengue / seasonal pressure |
| 2024 | 0.40 | Ongoing epi burden |
| 2025 | 0.35 | Ongoing |

Lookups: MINSAP / PAHO notes; independent Cuban press; WHO COVID archives
(see `literature/SOURCES.md`). Codes are severity inputs to S_t, not death counts.
""",
        encoding="utf-8",
    )


def main() -> Path:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    write_public_health_signals_md()
    df = build_feature_matrix()
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"wrote {OUT_CSV} rows={len(df)}")
    print(f"wrote {PUBLIC_MD}")
    return OUT_CSV


if __name__ == "__main__":
    main()
