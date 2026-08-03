#!/usr/bin/env python3
"""Compute provisional 2019-schedule mortality residual from ONEI tables."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import ARTIFACTS, get_claims  # noqa: E402
from mortality_data import expected_deaths_from_2019_schedule  # noqa: E402

OUT = ARTIFACTS / "mortality_residual_2024_2025.json"


def main() -> None:
    claims = get_claims()
    reg = claims["excess_mortality"]["provisional_schedule_residual_2024_2025"]["registered_deaths_k"]
    years = [2024, 2025]
    rows = []
    for y, reg_k in zip(years, reg):
        exp = expected_deaths_from_2019_schedule(y)
        residual = reg_k * 1000 - exp["expected_deaths"]
        rows.append(
            {
                "year": y,
                "expected_deaths": round(exp["expected_deaths"]),
                "expected_deaths_k": round(exp["expected_deaths"] / 1000, 1),
                "registered_deaths": int(reg_k * 1000),
                "registered_deaths_k": reg_k,
                "residual": round(residual),
                "detail": exp,
            }
        )
    combined = sum(r["residual"] for r in rows)
    out = {
        "combined_residual": combined,
        "years": rows,
        "status": "provisional — coarse 2019 schedule bridge; refine with full age-sex cells",
        "note": claims["excess_mortality"]["provisional_schedule_residual_2024_2025"]["method"],
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {OUT} combined_residual={combined}")


if __name__ == "__main__":
    main()
