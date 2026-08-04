"""Load canonical claims and project paths for demographics scripts/notebook."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"
ARTIFACTS = ROOT / "artifacts"
INFOGRAPHIC = ROOT / "infographic"
INFOGRAPHIC_EN = INFOGRAPHIC / "en"
CLAIMS_YAML = DATA / "claims.yaml"
CLAIMS_JSON = ARTIFACTS / "claims.json"

ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
INFOGRAPHIC_EN.mkdir(parents=True, exist_ok=True)


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as e:
        raise ImportError("PyYAML is required: pip install pyyaml") from e
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_claims(path: Path | None = None) -> dict[str, Any]:
    path = path or CLAIMS_YAML
    claims = _load_yaml(path)
    CLAIMS_JSON.write_text(json.dumps(claims, indent=2), encoding="utf-8")
    return claims


def get_claims() -> dict[str, Any]:
    """Cached-style load (re-reads file; fine for scripts)."""
    return load_claims()


# Convenience anchors used by notebook_support
def model_d_anchors(claims: dict[str, Any] | None = None) -> dict[str, float]:
    c = claims or get_claims()
    d = c["population_scenarios"]["scenarios"]["central"]
    v = c["vital"]
    # `.get(k, default)` evaluates the default eagerly, so this raised KeyError
    # the moment the fallback key was retired -- which is what stopped the
    # shipped notebook from running at all.
    em = c["excess_mortality"]
    for key in ("provisional_schedule_residual_2024_2025",
                "primary_age_adjusted_2024_2025",
                "cumulative_excess_2024_2025"):
        if key in em:
            x = em[key]
            break
    else:
        raise KeyError(
            "no excess-mortality anchor in claims.yaml; tried "
            "provisional_schedule_residual_2024_2025, "
            "primary_age_adjusted_2024_2025, cumulative_excess_2024_2025")
    s = c["selectivity"]
    return {
        "population_end_2025_model_d_m": float(d["pop_end_2025_m"]),
        "loss_vs_2021_m": float(d["gap_m"]),
        "loss_vs_2021_pct": float(d["gap_pct"]),
        # aliases kept for older notebook cells
        "loss_vs_2019_m": float(d["gap_m"]),
        "loss_vs_2019_pct": float(d["gap_pct"]),
        "births_2025": int(v["births_2025"]),
        "deaths_2025": int(v["deaths_2025"]),
        "natural_balance_2025": int(v["natural_balance_2025"]),
        "tfr_2025": float(v["tfr_2025"]),
        "pct_age_60_plus": float(s["pct_age_60_plus_remaining"]),
        "median_age": float(s["median_age_stayers"]),
        "excess_deaths_2024_25_low": int(x.get("band_low", x.get("low", 30000))),
        "excess_deaths_2024_25_high": int(x.get("band_high", x.get("high", 60000))),
        "onei_end_2025": int(v["onei_pop_end_2025"]),
        "pop_end_2026_m": float(d["pop_end_2026_m"]),
        "migration_share_pct": float(d["emigration_share_of_gap_pct"]),
    }
