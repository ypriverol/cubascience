#!/usr/bin/env python3
"""Cross-check headline numerals in scripts against data/claims.yaml."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from constants import CLAIMS_YAML, get_claims

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

# Script arrays that must match claims.yaml vital_series
CHECKS = {
    "charts_publication.py": {
        "births": "vital_series.births",
        "deaths": "vital_series.deaths",
    },
    "charts.py": {
        "births": "vital_series.births",
        "deaths": "vital_series.deaths",
    },
}


def _get_nested(d: dict, path: str):
    cur = d
    for part in path.split("."):
        cur = cur[part]
    return cur


def _extract_array(text: str, name: str) -> list[int] | None:
    # births=[...] or b = np.array([...])
    patterns = [
        rf"{name}\s*=\s*\[([\d,\s]+)\]",
        rf"{name}=np\.array\(\[([\d,\s]+)\]\)",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return [int(x.strip()) for x in m.group(1).split(",") if x.strip()]
    return None


def main() -> int:
    claims = get_claims()
    errors: list[str] = []

    vital_b = _get_nested(claims, "vital_series.births")
    vital_d = _get_nested(claims, "vital_series.deaths")

    for rel, fields in CHECKS.items():
        path = SCRIPTS / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for var, claim_path in fields.items():
            arr = _extract_array(text, var if var != "births" else "b")
            if var == "births" and arr is None:
                arr = _extract_array(text, "births")
            if var == "deaths" and arr is None:
                arr = _extract_array(text, "d")
            expected = _get_nested(claims, claim_path)
            if arr is None:
                continue
            if len(arr) != len(expected):
                errors.append(f"{rel}: {var} length {len(arr)} != claims {len(expected)}")
            elif arr != expected:
                errors.append(f"{rel}: {var} drift from claims.yaml (first mismatch)")

    # Scalar anchors
    v = claims["vital"]
    if v["natural_balance_2025"] != v["births_2025"] - v["deaths_2025"]:
        errors.append("claims.yaml: natural_balance_2025 != births_2025 - deaths_2025")

    if errors:
        print("CLAIMS AUDIT FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"claims audit OK ({CLAIMS_YAML.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
