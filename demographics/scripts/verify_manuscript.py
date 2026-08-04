#!/usr/bin/env python3
"""
Gate the MANUSCRIPTS against the claim sheet and the artifacts.

Why this exists
---------------
Three rounds of review found the same class of defect and nothing else: the
manuscript quoting numbers the pipeline had already superseded. Each revision
fixed the instances and created new ones, because every headline figure was
hand-copied from an artifact into two LaTeX files. The drift was generative, so
patching instances could never converge.

`audit_claims.py` closed half the loop (claims.yaml vs artifacts). This closes
the other half: every headline numeral in main.tex must match the claim sheet,
and the two language versions must agree.

Three checks:
  1. HEADLINE   every registered quantity appears in EN and ES with the value
                the artifacts currently produce.
  2. PARITY     the two manuscripts contain the same multi-digit numerals
                (year tokens excepted -- Spanish absorbs them into sentence-final
                punctuation, which is a formatting artefact, not a claim).
  3. RETIRED    values the project has explicitly superseded must not reappear.

Exit 1 on any failure. Run it before every commit that touches a manuscript.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from constants import ARTIFACTS, ROOT, get_claims  # noqa: E402

MS = ROOT / "manuscript"
EN = MS / "en" / "latex" / "main.tex"
ES = MS / "es" / "latex" / "main.tex"
# Everything the README advertises as a public product. Retired values must not
# survive in any of them -- they contradicted the paper for three rounds because
# only the two main .tex files were ever checked.
COMPANIONS = [MS / "en" / "latex" / "supplement.tex",
              ROOT / "demographics.ipynb",
              # Added after round 5. Each of these shipped a retired value while
              # the gate reported clean, because the gate had never been pointed
              # at them. provenance.yaml still carried 8.59 and the 1.8-2.4
              # envelope; the READMEs and the generated .md manuscripts are
              # advertised products too.
              ROOT / "data" / "provenance.yaml",
              ROOT / "README.md",
              ROOT.parent / "README.md",
              MS / "en" / "cuba-depopulation-2021-2026.md",
              # Round 6: this path was wrong, and `if c.exists()` SKIPPED it
              # silently -- the gate reported 12 products scanned and the ES
              # markdown manuscript had never been checked once. Missing
              # companions now fail instead of vanishing.
              MS / "es" / "cuba-despoblacion-2021-2026.md"] + \
    sorted((ROOT / "infographic").rglob("*.html"))

# Round 6: retired values had migrated into the FIGURES, where no check looked.
# charts_publication.py hard-coded 22.7 and a [11.11, -2.01, -0.18, -0.33, 8.59]
# waterfall, so the shipped PDFs displayed values their own captions contradicted
# on the same page. The chart scripts draw the manuscript; they are companions.
CHART_SCRIPTS = sorted(p for p in (ROOT / "scripts").glob("*.py")
                       if p.name.startswith(("charts", "chart_", "ig_", "render_")))

# Values the project has retired. Any reappearance in a manuscript is drift.
RETIRED = {
    "8.59": "central end-2025 population (now 8.58)",
    "2.52": "central gap (now 2.53)",
    "8.30": "central end-2026 population (now 8.29)",
    "1.94": "old envelope low (now 1.97)",
    "2.80": "old envelope high (now 2.79)",
    "17.4": "old envelope low pct (now 17.8)",
    "25.2": "old envelope high pct (now 25.1)",
    "22.7": "old central gap pct (now 22.8)",
    "112006": "expected deaths 2025 (transposition of 112,086)",
    "1.216": "SMR 2025 (now 1.215)",
    "9.18": "old conservative end-2025 population (now 9.14)",
    # The retired A/B/C scenario table, which survived in the supplement and the
    # infographics for five rounds because only individual headline numbers were
    # ever listed here.
    # The retired percentages (16.4 / 20.4 / 20.5 / 22.6) are deliberately NOT listed:
    # 20.4 is also the live 2019 elderly share, so a bare-numeral rule would fire
    # on a correct sentence. They are reachable only through the scenario table,
    # which the loss and population values below already cover.
    "1.80": "retired scenario A loss (now 1.97)",
    "2.19": "retired scenario B loss (now 2.53)",
    "2.41": "retired scenario C loss (now 2.79)",
    "9.16": "retired scenario A population (now 9.14)",
    "8.57": "retired scenario B population (now 8.58)",
    "8.26": "retired scenario C population (now 8.32)",
    "8.56": "superseded central end-2025 population (now 8.58)",
    "8.27": "superseded central end-2026 population (now 8.29)",
    "8.96": "retired Model E headline",
    "19426": "superseded 2025 size effect (now 19,468)",
    "19400": "superseded 2025 size effect, rounded (now 19,500)",
}


def _tex(p: Path) -> str:
    """
    Strip comments: a retired value in a comment is not a claim.

    Python sources use `#`, and the chart scripts document WHY a value was
    retired -- without this, the gate fires on its own explanatory comments.
    """
    src = p.read_text(encoding="utf-8")
    if p.suffix == ".py":
        return re.sub(r"#.*", "", src)
    return re.sub(r"(?<!\\)%.*", "", src)


# ONEI table numbers are citations, not quantities. The two languages phrase
# repeated references differently ("ONEI 3.15 and 3.3 ... both ONEI 3.15 and 3.3"
# vs "los cuadros 3.15 y 3.3 ... ambos"), which is style, not a claim difference.
TABLE_REFS = {"3.1", "3.3", "3.7", "3.8", "3.12", "3.13", "3.15", "3.16", "3.17",
              "3.22"}


def _numerals(text: str) -> collections.Counter:
    t = text.replace("\\,", "").replace("{,}", "")
    # Strip a trailing period: Spanish sentence-final punctuation attaches to
    # the numeral ("800\,000." vs "800{,}000"), which is formatting, not a
    # different claim. This was the sole cause of the residual parity noise.
    toks = [x.rstrip(".") for x in re.findall(r"\d[\d.]*", t)]
    return collections.Counter(x for x in toks if x and x not in TABLE_REFS)


def _fmt(v: float, kind: str) -> list[str]:
    """The LaTeX spellings a value may legitimately take."""
    if kind == "millions":
        return [f"{v/1e6:.2f}"]
    if kind == "thousands_sep":
        n = int(round(v, -2))
        return [f"{n:,}".replace(",", "{,}"), f"{n:,}".replace(",", "\\,")]
    if kind == "pct":
        return [f"{v:.1f}"]
    return [str(int(round(v)))]


def build_registry() -> list[dict]:
    """Headline quantities, resolved live from the artifacts."""
    ps = json.loads((ARTIFACTS / "population_scenarios.json").read_text(encoding="utf-8"))
    am = json.loads((ARTIFACTS / "attributable_mortality.json").read_text(encoding="utf-8"))
    sc, by = ps["scenarios"], {r["year"]: r for r in am["by_year"]}
    env = ps["envelope"]
    reg = [
        {"name": "central pop end-2025", "v": sc["central"]["pop_end_2025"], "kind": "millions"},
        {"name": "central pop end-2026", "v": sc["central"]["pop_end_2026"], "kind": "millions"},
        {"name": "central gap", "v": sc["central"]["gap_vs_official_2021"], "kind": "millions"},
        {"name": "conservative pop end-2025", "v": sc["conservative"]["pop_end_2025"], "kind": "millions"},
        {"name": "upper pop end-2025", "v": sc["upper"]["pop_end_2025"], "kind": "millions"},
        {"name": "null gap", "v": sc["null"]["gap_vs_official_2021"], "kind": "millions"},
        {"name": "envelope gap low", "v": env["gap_low_m"] * 1e6, "kind": "millions"},
        {"name": "envelope gap high", "v": env["gap_high_m"] * 1e6, "kind": "millions"},
        {"name": "central gap pct", "v": sc["central"]["gap_pct"], "kind": "pct"},
        {"name": "excess 2025", "v": by[2025]["excess_vs_2019_schedule"]["median"],
         "kind": "thousands_sep"},
        {"name": "ageing 2025", "v": by[2025]["ageing_effect_vs_2019"]["median"],
         "kind": "thousands_sep"},
        # Registered after round 5: this one drifted inside a single commit that
        # touched attributable_mortality.py without re-copying the manuscript
        # number, and no check looked at it.
        {"name": "size effect 2025", "v": abs(by[2025]["population_size_effect_vs_2019"]["median"]),
         "kind": "thousands_sep"},
        {"name": "excess 2022-25 p95", "v": am["cumulative_excess"]["2022_2025_post_covid"]["p95"],
         "kind": "thousands_sep"},
        {"name": "excess 2022-25 p05", "v": am["cumulative_excess"]["2022_2025_post_covid"]["p05"],
         "kind": "thousands_sep"},
        {"name": "excess 2025 p05", "v": by[2025]["excess_vs_2019_schedule"]["p05"],
         "kind": "thousands_sep"},
        {"name": "excess 2025 p95", "v": by[2025]["excess_vs_2019_schedule"]["p95"],
         "kind": "thousands_sep"},
        {"name": "excess 2022-25", "v": am["cumulative_excess"]["2022_2025_post_covid"]["median"],
         "kind": "thousands_sep"},
    ]
    return reg


def main() -> int:
    if not EN.exists() or not ES.exists():
        print("manuscript sources missing", file=sys.stderr)
        return 1
    en, es = _tex(EN), _tex(ES)
    errors: list[str] = []

    # 1. HEADLINE -- existence AND placement.
    # An existence-only test let a wrong abstract value pass so long as the right
    # value survived anywhere else and both languages drifted together, which is
    # exactly what a careless global sync produces.
    abstracts = {}
    for lang, txt in (("EN", en), ("ES", es)):
        m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", txt, re.S)
        abstracts[lang] = m.group(1) if m else ""
    ABSTRACT_CRITICAL = {"central pop end-2025", "central gap", "central gap pct",
                         "excess 2025", "excess 2022-25"}
    for item in build_registry():
        forms = _fmt(item["v"], item["kind"])
        for lang, txt in (("EN", en), ("ES", es)):
            if not any(f in txt for f in forms):
                errors.append(
                    f"{lang}: '{item['name']}' = {forms[0]} "
                    f"not found in the manuscript (artifact value)")
            elif item["name"] in ABSTRACT_CRITICAL and abstracts[lang] and \
                    not any(f in abstracts[lang] for f in forms):
                errors.append(
                    f"{lang}: '{item['name']}' = {forms[0]} is in the body but "
                    f"NOT in the abstract (placement check)")

    # 2. PARITY -- year tokens excepted (Spanish punctuation absorbs them)
    ne, ns = _numerals(en), _numerals(es)
    years = {str(y) for y in range(1900, 2036)}
    for tok in sorted(set(ne) | set(ns)):
        if len(tok) < 4 or tok in years:
            continue
        if ne.get(tok, 0) != ns.get(tok, 0):
            errors.append(f"parity: '{tok}' appears {ne.get(tok,0)}x in EN, "
                          f"{ns.get(tok,0)}x in ES")

    # 3. RETIRED -- across the manuscripts AND every advertised companion product
    targets = [("EN", en), ("ES", es)]
    for c in COMPANIONS + CHART_SCRIPTS:
        if not c.exists():
            errors.append(f"companion missing: {c} -- a listed product that does "
                          f"not exist is a broken path, not an absent check")
            continue
        try:
            targets.append((c.name, _tex(c)))
        except Exception as exc:
            errors.append(f"companion unreadable: {c} ({exc})")
    for bad, why in RETIRED.items():
        for label, txt in targets:
            if re.search(rf"(?<![\d.]){re.escape(bad)}(?![\d])", txt):
                errors.append(f"{label}: retired value {bad} reappeared -- {why}")

    if errors:
        print(f"MANUSCRIPT VERIFICATION FAILED ({len(errors)} issues):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"manuscript verification OK — {len(build_registry())} headline "
          f"quantities matched in both languages; numeral parity clean; "
          f"{len(COMPANIONS)} companion products and {len(CHART_SCRIPTS)} chart "
          f"scripts scanned for retired values")
    return 0


if __name__ == "__main__":
    sys.exit(main())
