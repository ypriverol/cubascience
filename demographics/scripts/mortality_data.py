# -*- coding: utf-8 -*-
"""Load ONEI Excel tables used by the HSDS / Model E pipeline."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from constants import DATA

ONEI = DATA / "onei"


def _xls(pattern: str) -> Path:
    matches = sorted(ONEI.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No ONEI file matching {pattern} under {ONEI}")
    return matches[0]


def age_structure_shares() -> pd.DataFrame:
    """Yearly percent shares: age_0_14, age_15_59, age_60_plus (ONEI 3.12)."""
    df = pd.read_excel(_xls("3.12*"), header=None)
    rows = []
    for _, row in df.iterrows():
        label = row[0]
        if label is None or (isinstance(label, float) and pd.isna(label)):
            continue
        s = str(label).strip()
        # e.g. "2019 (b)" or "2025"
        year_tok = s.split()[0]
        if not year_tok.isdigit():
            continue
        year = int(year_tok)
        if year < 2000 or year > 2035:
            continue
        try:
            a014 = float(row[2])
            a1559 = float(row[3])
            a60 = float(row[4])
        except (TypeError, ValueError):
            continue
        rows.append(
            {
                "year": year,
                "age_0_14_pct": a014,
                "age_15_59_pct": a1559,
                "age_60_plus_pct": a60,
                "source_file": "3.12",
                # Projection block rows lack (a)/(b) census/SIE markers
                "is_projection": "(" not in s,
            }
        )
    out = pd.DataFrame(rows).drop_duplicates("year", keep="first")
    return out.sort_values("year").reset_index(drop=True)


def infant_deaths_by_year() -> pd.DataFrame:
    """Total infant deaths by calendar year (ONEI 3.16)."""
    df = pd.read_excel(_xls("3.16*"), header=None)
    years = df.iloc[4].tolist()
    totals = df.iloc[7].tolist()
    rows = []
    for y, t in zip(years, totals):
        try:
            year = int(float(y))
            val = float(t)
        except (TypeError, ValueError):
            continue
        if year < 1985 or year > 2030:
            continue
        rows.append({"year": year, "infant_deaths": val, "source_file": "3.16"})
    return pd.DataFrame(rows).sort_values("year").reset_index(drop=True)


def cuba_natural_movement() -> pd.DataFrame:
    """National births and total deaths from ONEI 3.13 (Cuba block, left panel)."""
    df = pd.read_excel(_xls("3.13*"), header=None)
    rows = []
    for _, row in df.iterrows():
        v = row[0]
        try:
            year = int(float(v))
        except (TypeError, ValueError):
            continue
        if year < 1985 or year > 2030:
            continue
        try:
            births = float(row[1])
            infant = float(row[2]) if pd.notna(row[2]) else float("nan")
            deaths = float(row[4])
            pop_mean = float(row[7]) if pd.notna(row[7]) else float("nan")
        except (TypeError, ValueError):
            continue
        rows.append(
            {
                "year": year,
                "births": births,
                "infant_deaths_3_13": infant,
                "deaths": deaths,
                "pop_mean": pop_mean,
                "source_file": "3.13",
            }
        )
    # Keep first occurrence per year (left panel = earlier block)
    out = pd.DataFrame(rows).drop_duplicates("year", keep="first")
    return out.sort_values("year").reset_index(drop=True)


def life_expectancy_at_birth_panels() -> pd.DataFrame:
    """
    Best-effort e0 from ONEI 3.17 multi-panel layout.
    Returns period-label rows when parsable; may be empty if layout changes.
    """
    df = pd.read_excel(_xls("3.17*"), header=None)
    # Title cells often encode period, e.g. "..., 2001-2003"
    periods = []
    for col in range(0, min(df.shape[1], 60), 4):
        title = df.iloc[0, col]
        if not isinstance(title, str) or "Esperanza" not in title:
            continue
        # Find "Menos de 1" under this block
        for r in range(4, min(20, df.shape[0])):
            if str(df.iloc[r, col]).strip() in {"Menos de 1", "Menos de 1 "}:
                raw = df.iloc[r, col + 1]
                try:
                    if isinstance(raw, str):
                        raw = raw.replace(",", ".")
                    e0 = float(raw)
                except (TypeError, ValueError):
                    e0 = float("nan")
                periods.append(
                    {
                        "panel_title": title,
                        "e0_total": e0,
                        "source_file": "3.17",
                    }
                )
                break
    return pd.DataFrame(periods)
