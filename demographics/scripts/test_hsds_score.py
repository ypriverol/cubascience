# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hsds_score import score_years


def test_score_shape_and_bounds():
    df = score_years(n_boot=200, seed=1)
    assert list(df["year"]) == list(range(2019, 2026))
    assert df["S_median"].between(0, 1).all()
    assert (df["S_p05"] <= df["S_median"]).all()
    assert (df["S_median"] <= df["S_p95"]).all()


def test_crisis_years_higher_than_2019():
    df = score_years(n_boot=200, seed=1).set_index("year")
    s2019 = df.loc[2019, "S_median"]
    assert df.loc[2021, "S_median"] > s2019
    assert df.loc[2024, "S_median"] > s2019
    assert df.loc[2025, "S_median"] > s2019


if __name__ == "__main__":
    test_score_shape_and_bounds()
    test_crisis_years_higher_than_2019()
    print("ok")
