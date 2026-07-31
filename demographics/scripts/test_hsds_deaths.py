# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hsds_deaths import estimate_deaths


def test_deaths_positive_and_ordered():
    p = estimate_deaths(n=5_000, seed=3)
    assert len(p["years"]) == 4
    for y in p["years"]:
        assert y["D_star"]["p05"] <= y["D_star"]["median"] <= y["D_star"]["p95"]
        assert y["D_star"]["median"] > 50_000


if __name__ == "__main__":
    test_deaths_positive_and_ordered()
    print("ok")
