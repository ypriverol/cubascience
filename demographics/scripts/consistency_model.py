#!/usr/bin/env python3
"""
Inconsistency detector for ONEI's published demographic numbers.

The pipeline this belongs to has four layers:

  L1  REPORTED    what ONEI publishes, verbatim
  L2  INTERNAL    tests that use ONLY official numbers and check them against
                  each other and against the accounting identity. A failure here
                  is unarguable: the state's own figures contradict themselves.
  L3  EXTERNAL    destination registers and third-party series that bound the
                  official numbers from outside.
  L4  CORRECTED   the scenario ensemble (Models A-D) and the attributable-
                  mortality decomposition, which consume L2/L3 as priors.

This script is L2 and L3. It emits one record per test with the observed value,
the value implied by another official source, the residual, and a verdict.

Design rule: a test only fires on numbers that are BOTH official. Where an
external source is used it is labelled `external` and treated as a bound, never
as a truth value.

Outputs ``artifacts/consistency_report.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import ARTIFACTS, DATA, get_claims  # noqa: E402

OUT = ARTIFACTS / "consistency_report.json"

# ---------------------------------------------------------------- L1 REPORTED
# ONEI published year-end population. 2019-2022 are the pre-revision series;
# 2023-2025 are the "effective population" series published after July 2024.
POP = {2019: 11_193_470, 2020: 11_181_595, 2021: 11_113_215, 2022: 11_089_511,
       2023: 10_055_968, 2024: 9_748_007, 2025: 9_434_593}
BIRTHS = {2021: 99_096, 2022: 95_403, 2023: 90_392, 2024: 71_374, 2025: 68_064}
# ONEI's own declared net migration, where it published one.
ONEI_MIG = {2021: +169, 2022: +991, 2023: None, 2024: -251_221, 2025: -245_264}

# Every official death total we can find for a given year, with its provenance.
# Same year, same state, different numbers.
DEATH_SOURCES = {
    2021: {"onei_indicadores": 167_645, "who_submission": 167_675},
    2022: {"onei_first_reported": 129_049, "onei_published": 120_098,
           "who_submission": 120_108},
    2023: {"onei_indicadores": 117_739, "anuario_salud": 117_746,
           "who_submission": 117_749},
    2024: {"onei_indicadores": 128_098},
    2025: {"onei_indicadores": 136_214},
}

# ---------------------------------------------------------------- L3 EXTERNAL
# Lower bounds only. These are counts of Cubans recorded ARRIVING elsewhere, so
# they bound emigration from below; they are never treated as net migration.
US_ARRIVALS = {2021: 54_818, 2022: 313_506, 2023: 153_630, 2024: 145_124}
MULTI_DEST_FLOOR = {2022: 369_000, 2023: 330_000, 2024: 400_000}


def _canonical_deaths(year: int) -> int:
    """The figure the rest of the project uses."""
    return int(get_claims()["vital_series"]["deaths"][
        get_claims()["vital_series"]["years"].index(year)])


def t1_accounting_identity() -> list[dict]:
    """P(t) = P(t-1) + B(t) - D(t) + M(t). Solve for M and compare to declared."""
    out = []
    for y in range(2021, 2026):
        d = _canonical_deaths(y)
        implied = POP[y] - POP[y - 1] - BIRTHS[y] + d
        declared = ONEI_MIG.get(y)
        rec = {
            "test": "T1_accounting_identity",
            "year": y,
            "implied_net_migration": int(implied),
            "declared_net_migration": declared,
            "residual": None if declared is None else int(implied - declared),
            "severity": "info",
        }
        if declared is not None and abs(implied - declared) > 5_000:
            rec["severity"] = "high"
            rec["verdict"] = ("declared net migration does not reproduce the "
                              "published population path")
        elif declared is not None:
            rec["verdict"] = "internally consistent"
        else:
            rec["verdict"] = "no declared figure published for this year"
        out.append(rec)
    return out


def t2_multisource_deaths() -> list[dict]:
    """Same year, same state, different official death totals."""
    out = []
    for year, src in DEATH_SOURCES.items():
        if len(src) < 2:
            continue
        lo, hi = min(src.values()), max(src.values())
        spread = hi - lo
        rec = {
            "test": "T2_multisource_death_totals",
            "year": year,
            "sources": src,
            "spread": int(spread),
            "spread_pct": round(100 * spread / lo, 2),
            "canonical_used": _canonical_deaths(year),
            "severity": "high" if spread / lo > 0.02 else "low",
            "verdict": ("official sources disagree materially"
                        if spread / lo > 0.02
                        else "trivial disagreement between official sources"),
        }
        out.append(rec)
    return out


def t3_revision_seam() -> list[dict]:
    """
    Does a single year absorb a multi-year correction?

    A genuine one-year population fall is bounded by that year's vital events
    plus plausible migration. A fall far larger than that is a register
    correction being booked as if it were a flow.
    """
    out = []
    for y in range(2021, 2026):
        d = _canonical_deaths(y)
        drop = POP[y - 1] - POP[y]
        natural = d - BIRTHS[y]
        implied_mig = drop - natural
        # Largest single-year Cuban emigration any external source supports.
        plausible_max = 400_000
        rec = {
            "test": "T3_revision_seam",
            "year": y,
            "population_drop": int(drop),
            "natural_decrease": int(natural),
            "implied_migration_component": int(implied_mig),
            "external_plausible_annual_max": plausible_max,
            "excess_over_plausible": int(max(0, implied_mig - plausible_max)),
            "severity": "high" if implied_mig > plausible_max else "info",
        }
        rec["verdict"] = (
            "single-year drop exceeds any documented annual emigration: this is a "
            "backlog correction booked as one year's flow"
            if implied_mig > plausible_max else
            "single-year change is within plausible annual flow"
        )
        out.append(rec)
    return out


def t4_rate_vs_count() -> list[dict]:
    """A published crude death rate implies a denominator. Does it match?"""
    out = []
    # Anuario Estadistico de Salud 2023: 117,746 deaths at a CDR of 11.5/1000.
    checks = [{"year": 2023, "deaths": 117_746, "cdr": 11.5,
               "source": "Anuario Estadistico de Salud 2023"}]
    for c in checks:
        implied_pop = c["deaths"] / c["cdr"] * 1000
        published_end = POP[c["year"]]
        published_mid = 0.5 * (POP[c["year"] - 1] + POP[c["year"]])
        out.append({
            "test": "T4_rate_implies_denominator",
            "year": c["year"],
            "source": c["source"],
            "published_cdr_per_1000": c["cdr"],
            "implied_mid_year_population": int(round(implied_pop)),
            "published_mid_year_population": int(round(published_mid)),
            "published_end_year_population": published_end,
            "residual_vs_published_mid": int(round(implied_pop - published_mid)),
            "severity": "high" if abs(implied_pop - published_mid) > 2e5 else "low",
            "verdict": ("the rate and the population series cannot both be right"
                        if abs(implied_pop - published_mid) > 2e5
                        else "rate and denominator broadly reconcile"),
        })
    return out


def t5_external_contradiction() -> list[dict]:
    """Declared net migration against counts of Cubans recorded arriving abroad."""
    out = []
    for y, us in US_ARRIVALS.items():
        declared = ONEI_MIG.get(y)
        if declared is None:
            continue
        # Declared NET outflow, expressed as a positive number of leavers.
        declared_out = -declared if declared < 0 else 0
        rec = {
            "test": "T5_external_contradiction",
            "year": y,
            "declared_net_outflow": int(declared_out),
            "us_arrivals_only": int(us),
            "multi_destination_floor": MULTI_DEST_FLOOR.get(y),
            "shortfall_vs_us_only": int(max(0, us - declared_out)),
            "source_class": "external_lower_bound",
        }
        floor = MULTI_DEST_FLOOR.get(y)
        rec["shortfall_vs_multi_destination"] = (
            int(max(0, floor - declared_out)) if floor else None)
        if us > declared_out:
            rec["severity"] = "high"
            rec["verdict"] = ("more Cubans were recorded arriving in the US alone "
                              "than ONEI reports leaving for the entire world")
        elif floor and floor > declared_out:
            # The US-only test passes but the all-destination floor still bites.
            rec["severity"] = "high"
            rec["verdict"] = ("declared outflow clears the US-only floor but falls "
                              "below the multi-destination lower bound, so the "
                              "declared total cannot cover the recorded arrivals")
        else:
            rec["severity"] = "info"
            rec["verdict"] = "declared outflow exceeds every external lower bound"
        out.append(rec)
    return out


def t6_stock_never_corrected() -> list[dict]:
    """
    ONEI revised the 2023 endpoint but never restated 2021-2022. If 2022's true
    net migration was at least the external floor, the published 2022 stock was
    already too high by that amount.
    """
    y = 2022
    floor = MULTI_DEST_FLOOR[y]
    should_be = POP[y - 1] + BIRTHS[y] - _canonical_deaths(y) - floor
    return [{
        "test": "T6_stock_path_never_restated",
        "year": y,
        "published_population": POP[y],
        "population_implied_by_external_floor": int(round(should_be)),
        "overstatement": int(round(POP[y] - should_be)),
        "severity": "high",
        "verdict": ("the revision corrected the 2023 level but left the 2021-2022 "
                    "path intact, so the published stock for those years remains "
                    "too high by at least this much"),
    }]


def main() -> None:
    tests = (t1_accounting_identity() + t2_multisource_deaths()
             + t3_revision_seam() + t4_rate_vs_count()
             + t5_external_contradiction() + t6_stock_never_corrected())
    high = [t for t in tests if t.get("severity") == "high"]

    report = {
        "layers": {
            "L1_reported": "ONEI published series (this file, top)",
            "L2_internal": "T1-T4: official numbers against each other",
            "L3_external": "T5-T6: destination registers as lower bounds",
            "L4_corrected": "scripts/model_from_2021.py (population) and "
                            "scripts/attributable_mortality.py (deaths)",
        },
        "n_tests": len(tests),
        "n_high_severity": len(high),
        "tests": tests,
        "reading": (
            "T1/T2/T4 use only official sources, so a failure there is the state's "
            "own numbers contradicting each other. T5/T6 use external arrival "
            "counts, which bound emigration from below and never fix its level. "
            "Nothing here identifies the true population: it identifies where the "
            "official series cannot be taken at face value, which is what the "
            "scenario priors in L4 are built to absorb."
        ),
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"CONSISTENCY REPORT — {len(tests)} tests, {len(high)} high severity\n")
    for t in tests:
        mark = "!!" if t.get("severity") == "high" else "  "
        print(f"{mark} [{t['test']}] {t.get('year','')}")
        for k, v in t.items():
            if k in ("test", "year", "severity", "verdict"):
                continue
            print(f"      {k}: {v}")
        if "verdict" in t:
            print(f"      -> {t['verdict']}")
        print()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
