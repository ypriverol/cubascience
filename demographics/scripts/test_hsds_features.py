# -*- coding: utf-8 -*-
"""Tests for HSDS feature matrix."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hsds_features import build_feature_matrix


def test_norms_bounded():
    df = build_feature_matrix()
    assert df["value_norm"].between(0, 1).all()


def test_expected_shape():
    df = build_feature_matrix()
    assert set(df["year"]) == set(range(2019, 2026))
    assert df.groupby(["year", "feature"]).size().max() == 1
    assert df["feature"].nunique() == 12


if __name__ == "__main__":
    test_norms_bounded()
    test_expected_shape()
    print("ok")
