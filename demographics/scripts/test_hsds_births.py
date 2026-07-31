# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hsds_births import estimate_births


def test_births_near_register():
    p = estimate_births(n=5_000, seed=4)
    for y in p["years"]:
        med = y["B_star"]["median"]
        reg = y["B_reg"]
        assert 0.85 * reg <= med <= 1.10 * reg


if __name__ == "__main__":
    test_births_near_register()
    print("ok")
