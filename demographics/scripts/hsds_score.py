# -*- coding: utf-8 -*-
"""Yearly Health-System Deterioration Score S_t from the HSDS feature matrix."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from constants import ARTIFACTS, DATA
from hsds_features import build_feature_matrix, main as rebuild_features

SIGNALS = DATA / "mortality_signals.yaml"
OUT_JSON = ARTIFACTS / "hsds_scores.json"


def _load_signals() -> dict:
    with SIGNALS.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _feature_frame() -> pd.DataFrame:
    csv = DATA / "hsds_features.csv"
    if csv.exists():
        return pd.read_csv(csv)
    return build_feature_matrix()


def score_years(n_boot: int = 1000, seed: int = 2027) -> pd.DataFrame:
    """
    Weighted S_t with Dirichlet-like weight bootstrap within buckets.
    Returns year, S_median, S_p05, S_p95.
    """
    signals = _load_signals()
    mix = signals["bucket_mix"]
    df = _feature_frame()
    years = sorted(df["year"].unique())
    rng = np.random.default_rng(seed)

    # Point estimate with default weights
    point = {}
    for year in years:
        sub = df[df["year"] == year]
        bucket_scores = {}
        for bucket, w_mix in mix.items():
            b = sub[sub["bucket"] == bucket]
            if b.empty:
                bucket_scores[bucket] = 0.0
                continue
            w = b["weight_default"].to_numpy(dtype=float)
            w = w / w.sum()
            bucket_scores[bucket] = float(np.dot(w, b["value_norm"].to_numpy(dtype=float)))
        point[year] = sum(mix[b] * bucket_scores[b] for b in mix)

    # Bootstrap: resample within-bucket weights ~ Dirichlet(alpha=default_w)
    rows = []
    for year in years:
        sub = df[df["year"] == year]
        draws = []
        for _ in range(n_boot):
            bucket_scores = {}
            for bucket, w_mix in mix.items():
                b = sub[sub["bucket"] == bucket]
                alpha = np.clip(b["weight_default"].to_numpy(dtype=float), 1e-6, None)
                w = rng.dirichlet(alpha)
                bucket_scores[bucket] = float(np.dot(w, b["value_norm"].to_numpy(dtype=float)))
            # Mild mix jitter
            mix_alpha = np.array([mix[b] for b in mix], dtype=float)
            mix_draw = rng.dirichlet(np.clip(mix_alpha * 20.0, 1e-3, None))
            s = float(sum(mix_draw[i] * bucket_scores[b] for i, b in enumerate(mix)))
            draws.append(s)
        arr = np.asarray(draws)
        rows.append(
            {
                "year": int(year),
                "S_point": point[year],
                "S_median": float(np.median(arr)),
                "S_p05": float(np.quantile(arr, 0.05)),
                "S_p95": float(np.quantile(arr, 0.95)),
            }
        )
    return pd.DataFrame(rows).sort_values("year").reset_index(drop=True)


def write_scores(n_boot: int = 1000, seed: int = 2027) -> dict:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    if not (DATA / "hsds_features.csv").exists():
        rebuild_features()
    scores = score_years(n_boot=n_boot, seed=seed)
    payload = {
        "n_boot": n_boot,
        "seed": seed,
        "years": scores.to_dict(orient="records"),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    payload = write_scores()
    for row in payload["years"]:
        print(
            f"{row['year']}: S_med={row['S_median']:.3f} "
            f"[{row['S_p05']:.3f}, {row['S_p95']:.3f}]"
        )
    print(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
