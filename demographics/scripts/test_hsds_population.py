# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hsds_population import run_model_e


def test_model_e_sane_band():
    p = run_model_e(n=8_000, seed=5)
    med = p["pop_2025"]["median"]
    assert 7.5e6 < med < 10.0e6
    assert p["pop_2026"]["median"] < med
    assert 50.0 < p["mig_share_median"] < 99.0


if __name__ == "__main__":
    test_model_e_sane_band()
    print("ok")
