#!/usr/bin/env python3
"""
Cross-check headline numerals in scripts against data/claims.yaml.

The previous version silently passed everything: its regex could not match
`np.array(VIT["births"], ...)`, so `_extract_array` returned None and every
check was skipped, and its file list covered only the two scripts that already
read claims.yaml. It validated nothing.

This version scans EVERY script for headline values that must agree with the
claim sheet, and fails on any occurrence of a known-stale value.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from constants import CLAIMS_YAML, get_claims

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SELF = Path(__file__).name

# Values that were once published and must never reappear in a script.
# value -> (what it should be now, why)
# Integers are unambiguous and flagged anywhere in the file.
STALE = {
    "117746": ("117739", "2023 deaths: use the canonical Indicadores figure"),
    "502159": ("502149", "2022-2025 registered deaths in the identity window"),
    "68149": ("68150", "2025 natural balance (computed)"),
}
# Short decimals recur legitimately as other models' interval bounds (Model A's
# 2026 lower bound is also 8.27), so these are flagged only on a line that names
# Model D.
STALE_MODEL_D = {
    "8.56": ("8.58", "central scenario end-2025 population"),
    "8.27": ("8.29", "central scenario end-2026 population"),
}


def _series_literals(text: str, name: str) -> list[int] | None:
    """Find `name = [1, 2, 3]` style literals (ignoring claims-driven lookups)."""
    m = re.search(rf"\b{name}\s*=\s*\[([\d,\s]+)\]", text)
    if not m:
        return None
    return [int(x) for x in m.group(1).replace("\n", "").split(",") if x.strip()]


def main() -> int:
    claims = get_claims()
    errors: list[str] = []

    births = claims["vital_series"]["births"]
    deaths = claims["vital_series"]["deaths"]
    cen = claims["population_scenarios"]["scenarios"]["central"]
    expected_alive = {str(cen["pop_end_2025_m"]), str(cen["pop_end_2026_m"])}

    for path in sorted(SCRIPTS.glob("*.py")):
        if path.name == SELF:
            continue
        text = path.read_text(encoding="utf-8")
        stripped = re.sub(r"#.*", "", text)

        for bad, (good, why) in STALE.items():
            if re.search(rf"(?<![\d.]){re.escape(bad)}(?![\d])", stripped):
                errors.append(f"{path.name}: stale {bad} -> should be {good} ({why})")

        for lineno, line in enumerate(stripped.splitlines(), 1):
            if not re.search(r"Model[o]?\s*~?D", line):
                continue
            for bad, (good, why) in STALE_MODEL_D.items():
                if re.search(rf"(?<![\d.]){re.escape(bad)}(?![\d])", line):
                    errors.append(
                        f"{path.name}:{lineno}: stale {bad} -> should be {good} ({why})")

        for name, expected in (("births", births), ("deaths", deaths),
                               ("b", births), ("d", deaths)):
            arr = _series_literals(stripped, name)
            if arr and len(arr) == len(expected) and arr != expected:
                errors.append(
                    f"{path.name}: hard-coded `{name}` series differs from "
                    f"claims.yaml vital_series"
                )

    # Internal consistency of the claim sheet itself.
    v = claims["vital"]
    if v["natural_balance_2025"] != v["births_2025"] - v["deaths_2025"]:
        errors.append("claims.yaml: natural_balance_2025 != births_2025 - deaths_2025")
    if v["births_2022_2025"] != 325_233 or v["deaths_2022_2025_registered"] != 502_149:
        errors.append("claims.yaml: identity-window vital anchors changed unexpectedly")
    ident = (v["official_pop_end_2021"] + v["births_2022_2025"]
             - v["deaths_2022_2025_registered"] - v["onei_pop_end_2025"])
    if ident != v["onei_net_mig_2022_2025"]:
        errors.append(
            f"claims.yaml: onei_net_mig_2022_2025 breaks the accounting identity "
            f"({ident} != {v['onei_net_mig_2022_2025']})"
        )

    ds = claims["destinations_settled"]
    if ds["us"] + ds["non_us_total"] != ds["floor_total"]:
        errors.append("claims.yaml: destinations floor_total != us + non_us_total")
    if ds["spain"] + ds["uruguay"] + ds["rest"] != ds["non_us_total"]:
        errors.append("claims.yaml: destinations non-US breakdown does not sum")

    am = claims["attributable_mortality"]["decomposition_2025"]
    total = (am["population_size_effect"] + am["ageing_effect"]
             + am["excess_vs_2019_schedule"])
    # Tolerance was 5% (~1,565 deaths), wide enough that a term could drift by
    # more than a thousand and still pass. The identity is exact per draw, so the
    # only slack needed is median non-additivity.
    if abs(total - am["observed_rise_incl_unregistered"]) > 250:
        errors.append(
            f"claims.yaml: decomposition does not reconstruct the observed rise "
            f"({total} vs {am['observed_rise_incl_unregistered']})"
        )

    # The claim sheet must agree with the artifacts it summarises. Without this
    # the audit passed while claims.yaml carried a superseded scenario table.
    import json
    ART = ROOT / "artifacts"
    ps_f = ART / "population_scenarios.json"
    if ps_f.exists():
        ps = json.loads(ps_f.read_text(encoding="utf-8"))
        env = ps["envelope"]
        cy = claims["population_scenarios"]
        for got, want, name in (
            (cy["envelope_gap_m"], [env["gap_low_m"], env["gap_high_m"]], "envelope_gap_m"),
            (cy["envelope_gap_pct"], [env["pct_low"], env["pct_high"]], "envelope_gap_pct"),
        ):
            if [round(float(x), 2) for x in got] != [round(float(x), 2) for x in want]:
                errors.append(f"claims.yaml {name} {got} != artifact {want}")
        for key in ("conservative", "central", "upper"):
            a = ps["scenarios"][key]
            b = cy["scenarios"][key]
            if abs(b["pop_end_2025_m"] - a["pop_end_2025"] / 1e6) > 0.006:
                errors.append(
                    f"claims.yaml scenarios.{key}.pop_end_2025_m "
                    f"{b['pop_end_2025_m']} != artifact {a['pop_end_2025']/1e6:.3f}")

    am_f = ART / "attributable_mortality.json"
    if am_f.exists():
        am = json.loads(am_f.read_text(encoding="utf-8"))
        cam = claims["attributable_mortality"]
        by = {r["year"]: r for r in am["by_year"]}
        checks = [
            (cam["annual_2025"]["median"],
             by[2025]["excess_vs_2019_schedule"]["median"], "annual_2025.median"),
            (cam["decomposition_2025"]["ageing_effect"],
             by[2025]["ageing_effect_vs_2019"]["median"], "decomposition_2025.ageing_effect"),
            (cam["decomposition_2025"]["excess_vs_2019_schedule"],
             by[2025]["excess_vs_2019_schedule"]["median"],
             "decomposition_2025.excess_vs_2019_schedule"),
            # Never compared to the artifact before. It drifted inside a single
            # commit and shipped stale in both abstracts and both headline tables.
            (cam["decomposition_2025"]["population_size_effect"],
             by[2025]["population_size_effect_vs_2019"]["median"],
             "decomposition_2025.population_size_effect"),
            (cam["annual_2026_scenario"]["median"],
             by[2026]["excess_vs_2019_schedule"]["median"], "annual_2026_scenario.median"),
        ]
        for got, want, name in checks:
            if abs(float(got) - float(want)) > 50:
                errors.append(f"claims.yaml {name} {got} != artifact {want}")
        for win, key in (("2024_2025", "2024_2025"), ("2020_2025", "2020_2025"),
                         ("2022_2025_post_covid", "2022_2025_post_covid")):
            a = am["cumulative_excess"][key]
            b = cam["cumulative"][win]
            for f in ("median", "p05", "p95"):
                if abs(float(b[f]) - float(a[f])) > 100:
                    errors.append(
                        f"claims.yaml cumulative.{win}.{f} {b[f]} != artifact {a[f]}")

    if errors:
        print("CLAIMS AUDIT FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"claims audit OK ({CLAIMS_YAML.name}); "
          f"{len(list(SCRIPTS.glob('*.py')))} scripts scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
