# Author response to manuscript review issues

**Review source:** [`manuscript_review_issues.md`](manuscript_review_issues.md) @ `bee1df9`  
**Response date:** 2 August 2026  
**Manuscript branch reviewed:** `feature/preprint-slim-supplement` (post–adversarial-review pass)

This document responds to each backlog item. Status codes:

| Status | Meaning |
|---|---|
| **Done** | Addressed in the current manuscript / claims / figures |
| **Partial** | Direction accepted; implementation incomplete |
| **Accepted** | Agree; planned work not yet merged |
| **Deferred** | Valid but out of scope for the current preprint revision |

---

## P0 — Resolve internal numeric inconsistencies

**Reviewer concern:** Disagreements across `claims.yaml`, artifacts, scripts, and manuscript (e.g. 502,149 vs 502,159 deaths; −68,149 vs −68,150 natural balance; 117,739 vs 117,746 for 2023 deaths).

**Response:** **Partial — accepted as P0.**

We agree this is the top reproducibility risk. Current resolution policy:

| Quantity | Canonical (public claims) | Alternate value | Resolution |
|---|---|---|---|
| Registered deaths 2022–2025 | **502,149** | 502,159 in `model_e_deaths.json` / Model E summaries | Model E internal artifact uses a slightly different registration pull; **public headline uses 502,149** from ONEI identity window in `model_from_2021.py`. Will add explicit crosswalk note in artifacts. |
| Natural balance 2025 | **−68,150** | −68,149 in prior draft | Arithmetic fix: 136,214 − 68,064 = −68,150. |
| Deaths 2023 | **117,739** (canonical) | 117,746 (Anuario footnote) | **Both documented** in `claims.yaml` (`deaths_2023_canonical` + `deaths_2023_anuario_footnote`). Manuscript and charts use 117,739; footnote explains Anuario table variant. |
| Deaths 2022 | **120,098** | 120,108 in Model E death JSON | Same as sum issue: Model E path vs ONEI headline; **120,098** for publication. |

**Planned actions:**
1. Add `scripts/audit_claims.py` (or notebook cell) that diffs `claims.yaml` against hard-coded arrays in `scripts/charts*.py` and manuscript LaTeX literals.
2. Regenerate `artifacts/claims.json` on every chart build.
3. Document intentional alternates in `claims.yaml` under a `footnotes:` block rather than silent drift.

---

## P0 — Make `claims.yaml` the real single source of truth

**Response:** **Partial — accepted.**

**Already done:**
- `scripts/constants.py` loads `claims.yaml` and exposes anchors for notebook/scripts.
- `charts_publication.py` reads model D, triangulation, and selectivity from claims.
- Headline scenario table, destination ledger, and excess-mortality keys live in YAML.

**Still hard-coded (known debt):**
- Year-series arrays in `charts_publication.py`, `charts.py`, `charts_es.py`, `chart_exceso.py` (births/deaths time series; illustrative expected deaths 112.5k / 113.8k).
- Mortality residual bar inputs (~38k band) in plotting scripts.
- Some legacy scripts (`charts_final.py` still uses 117,746).

**Planned actions:**
1. Move vital time series and mortality-residual illustration inputs into `claims.yaml` (or `data/vital_series.csv` referenced from claims).
2. Route all publication chart scripts through `constants.get_claims()` only.
3. CI check: fail if grep finds headline numerals in scripts that are absent from claims.

---

## P1 — Reframe from “estimate” to “scenario audit”

**Response:** **Partial — substantially addressed, title still mixed.**

**Done since review:**
- Title uses *population decline* (not *collapse*).
- Abstract opens with *audits the 2021–2025 headcount decline with transparent scenario ensembles*.
- Methods state Models A–D are *scenarios, not identified estimators*; Model D is *illustrative central scenario*.
- Discussion states Model D is *not an identified point estimate*.
- Infographics (ES + EN) use scenario envelope language.

**Remaining gap:**
- Title still reads *Estimating Cuba's…* which the reviewer correctly flags as estimate-framing.
- Introduction line 73 still says *This paper estimates…* and uses *honest scenario intervals* (tone + framing).

**Planned revision (next pass):**
- Title candidate: *Scenario audit of Cuba's 2021–2026 population decline* (or *Auditing Cuba's…*).
- Replace *estimates* / *estimate* in intro and captions where the object is a scenario, not a point estimator.
- Keep *estimate* only where referring to external studies (Albizu, UN WPP).

---

## P1 — Reduce overemphasis on Model D point estimates

**Response:** **Partial — improved, not fully demoted.**

**Done:**
- Abstract **leads** with across-scenario envelope **1.8–2.4 M**.
- Results open with envelope before Model D medians.
- Within-scenario 90% bands labelled *prior-predictive*, not sampling error.
- Register-gap *1 in 4* demoted to aside (not scientific lead).
- Model A floor neighbourhood reported alongside D.

**Remaining gap:**
- Abstract and conclusion still give prominent lines to 8.59 M, 20.5%, and 91% migration share without always pairing them with *illustrative* / *under fixed priors*.
- Waterfall figure (f3) visually centres Model D decomposition.

**Planned actions:**
- Pair every Model D headline number with *illustrative* or *under scenario D priors* in abstract/conclusion.
- Waterfall caption: add *scenario D median decomposition, not identified attribution*.

---

## P1 — Reproducible ONEI 3.15 age–sex mortality pipeline

**Response:** **Accepted — not yet implemented.**

We agree the provisional ~38k residual **cannot** graduate to a primary claim until expected deaths are computed from ONEI table 3.15 applied to explicit \(P_{a,t}\).

**Current honest labelling:**
- Manuscript, claims, and figures call the residual *provisional* / *illustrative*.
- Kitagawa language removed.
- Sensitivity band 30–60k retained explicitly.

**Planned work (separate issue / milestone):**
1. Script: `scripts/mortality_schedule_residual.py` reading ONEI 3.15 + age structure.
2. Output: `artifacts/mortality_residual_2024_2025.json`.
3. Replace hard-coded 112.5 / 113.8k in charts once pipeline exists.

**Deferred for this preprint:** Full pipeline is required before any journal submission; acceptable for Zenodo preprint if labelled provisional.

---

## P1 — Revise figures to reduce rhetorical overreach

**Response:** **Partial.**

| Figure | Review concern | Current status |
|---|---|---|
| f1 population path | 2030 path too assertive | Post-2026 segment labelled *illustrative scenario* in caption and chart subtitle; dashed extension retained for communication |
| f3 waterfall | Implies identified decomposition | Caption still strong; **needs softening** (see P1 Model D) |
| f7 triangulation | Model D looks like external validation | **Fixed:** role `estimand_not_validator`; caption states D is not a validator |
| f5 life expectancy | Over-corroboration | Moved to **supplement**; main text says LE re-expresses mortality |
| f9 excess mortality | Illustrative inputs | **Fixed:** provisional labelling, 30–60k band, separated from crude 153k |

Infographics (ES/EN) regenerated with same cautious labels.

---

## P2 — Move provisional mortality residual out of main headline

**Response:** **Partial.**

**Done:** Demoted in abstract ordering (envelope first); labelled provisional throughout; removed Kitagawa; infographic uses *residual provisional* panel title.

**Still in main text:** One results paragraph and figure panel remain — appropriate for transparency, but we will **shorten** the results paragraph and ensure the abstract does not imply age-adjusted identification.

---

## P2 — Audit and soften editorial language

**Response:** **Accepted — partial pass done, more needed.**

| Term | Status |
|---|---|
| *collapse* | **Removed** from title and public products |
| *honest* | **Still present** (intro, results) — **will replace** with *ONEI-anchored* / *conservative* |
| *empties* / *emptying* | **Still present** — **will replace** with *net population loss* / *subnational outflow* where editorial |
| *with integrity* | **Still in conclusions** — **will replace** with *conducted under standard census practice* or similar |
| *order-of-magnitude impossibility* | **Still in discussion** — **will soften** to *inconsistent with destination records at any plausible uniqueness factor* |

We accept the tone critique for journal review; preprint may retain slightly stronger migration-accounting language if sourced, but the flagged phrases above will be neutralised in the next edit pass.

---

## P2 — Tighten comparative-context tables

**Response:** **Partial.**

**Done:** Removed Syria/Zimbabwe; kept Venezuela + Puerto Rico with *peacetime emigration-driven* framing; Cuba row labelled *Model D, corrected base*.

**Remaining:** Regional growth table uses approximate rates without single source column; war/disaster comparators need footnotes on non-comparability.

**Planned:** Add source column or move table to supplement with full citations; soften Puerto Rico row (disaster confounding).

---

## P2 — Document observed / derived / assumed / expert-coded inputs

**Response:** **Accepted — not yet implemented.**

**Planned:** New supplement table (or `data/provenance.yaml`):

| Quantity | Class | Source |
|---|---|---|
| ONEI B, D, R 2022–25 | Observed | ONEI Anuario |
| U₀, M, D_fac priors | Assumed | Model scripts |
| HSDS features | Expert-coded | `hsds_features.py` |
| Destination floor 1.05 M | Derived (ledger) | `destinations_settled.csv` |
| Expected deaths 2024–25 | Assumed (illustrative) | Pending 3.15 pipeline |

---

## P2 — Strengthen sourcing for selectivity claims

**Response:** **Accepted — gap acknowledged.**

Claims **~57% female** and **~133 women per 100 men** (reproductive ages) appear in the manuscript but lack a cited artifact path in-repo.

**Planned:**
1. Trace to ONEI emigration-by-age-sex tables or published flow estimates.
2. Add `data/selectivity.yaml` with source rows and derivation note.
3. If only available from external reports, cite explicitly and mark as *external, not recomputed here*.

Until sourced, we will **soften** to *majority female* unless the exact percentages are verified.

---

## P3 — Clarify Model E evidentiary status

**Response:** **Done / partial.**

**Done:**
- Model E in main table with *(prov.)* label; not preferred in claims.
- Supplement + `artifacts/model_e_adversarial_notes.md` document U₀ prior difference, ageing double-count risk, HSDS subjectivity.
- Manuscript: *adversarial gate does not promote E over D*.

**Remaining:** Expand supplement limitations paragraph on expert-coded HSDS transfer assumptions (one short subsection).

---

## Summary matrix

| # | Issue | Status | Next action |
|---|---|---|---|
| 1 | Numeric inconsistencies | Partial | `audit_claims.py` + crosswalk notes |
| 2 | claims.yaml enforcement | Partial | Move time series to data; CI check |
| 3 | Scenario-audit framing | Partial | Retitle; remove *Estimating* / *estimates* |
| 4 | Model D de-emphasis | Partial | Abstract/conclusion pairing; waterfall caption |
| 5 | ONEI 3.15 pipeline | Accepted | New script + artifact (pre-journal) |
| 6 | Figure rhetoric | Partial | Waterfall + f1 caption pass |
| 7 | Mortality residual prominence | Partial | Shorten results paragraph |
| 8 | Editorial tone | Accepted | Replace flagged terms (next edit) |
| 9 | Comparison tables | Partial | Source footnotes |
| 10 | Provenance taxonomy | Accepted | Supplement table |
| 11 | Selectivity sourcing | Accepted | `selectivity.yaml` or soften claims |
| 12 | Model E limits | Partial | Supplement paragraph |

---

## Recommended immediate PR (before wider circulation)

1. **P0:** Claims audit script + fix `charts_final.py` 117,746 drift; document 502,149 vs 502,159.
2. **P1 framing:** Title/subtitle pass (*scenario audit*).
3. **P2 tone:** Replace *honest*, *emptying*, *with integrity*, *impossibility* in `main.tex`.
4. **P2 selectivity:** Source or soften 57% / 133:100 claims.

The adversarial-review pass (commits through `5bfec4c` + local infographic/manuscript edits) already addressed destination ledger honesty, IMR elasticity, Kitagawa removal, triangulation roles, bilingual infographics, and continuous Methods/Results/Discussion prose. This response maps the **new** review backlog onto what remains.

---

*Prepared for maintainers / co-authors. Not a public-facing reply to reviewers unless adapted.*
