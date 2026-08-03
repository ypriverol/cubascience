# Adversarial review — 3 August 2026

Three independent hostile reviewers were run against the revised package: one on
the new attributable-mortality model, one on the two manuscripts, one on the
sources and provenance chain. Each was instructed to refute rather than confirm.

This file records what was found and what was done. Items marked **open** are
real and unfixed.

---

## Fixed — model (`scripts/attributable_mortality.py`)

| # | Defect | Resolution |
|---|---|---|
| 1 | **The stated data constraint was false.** The model claimed "no annual single-age resident population is published post-2012" and used ONEI 3.12 *shares* accordingly. ONEI 3.3 — already in the repo, read by no script — publishes mid-year population **by age, annually, 2006–2022**. | Added `mortality_data.mean_population_by_age()`; the model now uses observed denominators. 2019 rates changed from 3 groups to {0-14, 15-59, 60-64, 65+}. |
| 2 | **The 60+ count fell 67k in 2024.** Deriving it as (share × official total) multiplied ONEI's one-step 2023 register catch-up by an age share, deleting elderly residents who never emigrated. Cuba's 60+ count has risen every year since 2006. | Elderly groups are now observed to 2022 and cohort-projected after, with entrants from 55-59 and elderly emigration at the 8% share. Regression test `test_elderly_population_never_falls`. |
| 3 | **The decomposition was not additive.** `size_effect` used clean rates while `struct_size` used drifted/noised rates, leaking up to +2,085 deaths into the ageing term. The unit test tolerance sat just above the known failure. | The 2019 reference now uses the same perturbed rates as the target year, so the identity closes exactly. Test asserts `identity_residual <= 1`. |
| 4 | **The within-60+ drift prior had the wrong sign.** Support was [0, +8%]; the observed shift is *negative* (the 1960s cohort entering at 60-64 makes the 60+ group younger — 60-64 rose from 25.7% to 27.9% of 60+ between 2019 and 2022). | The 60-64/65+ split now captures this structurally; the residual drift is symmetric `N(0, 0.03)`. |
| 5 | **Population noise was drawn inside the year loop**, so a wrong stock averaged itself down across years and understated cumulative bands by ~12–14%. | Moved outside the loop with the other systematic parameters. |
| 6 | "Robust to stock choice" was a tautology: `elderly_uplift = p_off/p_d` made the two branches algebraically identical, and implied 0% elderly emigrants against the claim sheet's 8%. | Both branches now run separate cohort projections with elderly emigration honoured; the robustness claim is stated in the manuscript as an explicit modelling assumption, not a finding. |
| 7 | `Ignorado` redistribution mutated its own denominator (order-dependent). | Shares computed once up front. |
| 8 | 2019 denominators were end-year, not mid-year, and from the wrong table. | Now ONEI 3.3 mid-2019 (11,201,549). |

**Effect on the headline:** 2024–2025 attributable moved 47.1k → **50.2k**; 2022
moved 7.4k → **12.8k**; 2025 annual moved 26.4k → **28.6k**. The year-by-year
profile changed materially and the manuscript narrative was rewritten to match.

## Fixed — manuscripts

| # | Defect | Resolution |
|---|---|---|
| 1 | **CRITICAL:** "roughly 48,000 more deaths a year than in 2019" quoted the sum of the two *positive* decomposition terms while describing it as the observed rise, which is ~31,300. Two components were presented as summing to 155% of the quantity they were shares of. | Rewritten in both languages: the rise is ~31,300; ageing and health system are shares of the *gross* increase, and they exceed the net rise because the smaller population pulls the other way. |
| 2 | "about 1.6 million fewer residents" — the size term implies ~2.0M. | Corrected to ~2 million in both languages and in `claims.yaml`. |
| 3 | Discussion claimed the infant-mortality sentinel "independently supports" death-registration completeness; Methods explicitly forbids that reading. | Reduced from three robustness properties to two; completeness is now stated as an assumption the sentinel makes plausible but does not establish. |
| 4 | The robustness argument required a ~29% Model-D elderly share, a figure the paper elsewhere calls an "illustrative sketch". | The ~29% is now stated explicitly as an assumption of the decomposition, with its conservative direction explained. |
| 5 | "register-gap loss is roughly 20–23%" — Models A–C give 17.6–25.7%. | Corrected to 18–26%. |
| 6 | Conclusion's "working scenario band 8.6–9.0M" contradicted three other bands and dropped both endpoints of the declared primary uncertainty statement. | Replaced with the end-2026 across-scenario band 7.9–8.9M. |
| 7 | The ageing term was called "a delayed migratory effect"; it is computed from the observed ONEI age structure and does not partition migration-induced from cohort ageing. | Now explicitly stated as not identified. |
| 8 | "not a COVID-19 tail" was an exclusion claim a residual cannot deliver. | Softened; post-acute COVID and coding drift named as unexcluded contributors. |
| 9 | 0.5M less migration was said to move the stock 0.3M. | Corrected to ~9.1M. |
| 10 | "nearly half are under 35" understated the claim sheet's median leaver age of 30. | Restated as the median. |
| 11 | Venezuela's window differed between two adjacent tables (2013–24 vs 2013–20). | Harmonised. |
| 12 | Stray `\label{sec:nowcast}` captured the table counter; EN/ES date, subtitle and supplement pointer diverged; ES referenced a Spanish supplement that does not exist. | All fixed; ES now says the supplement is English-only. |
| 13 | Spanish: "población mayor" (= elderly population) for "higher population"; "300,000 pérdidas" (reads as casualties); "puente crudo", "check de consistencia", "reparto de servilleta", "desastre huracanado", "priores", "vio subir", "tanto menor" and other calques/anglicisms. | All corrected; gender agreement re-checked after bulk substitution. |

## Fixed — sources

| # | Defect | Resolution |
|---|---|---|
| 1 | `garcia2019` DOI resolved to a paper on urine metals and cardiovascular disease. | Corrected to `10.1093/ije/dyz072` (verified via Crossref). |
| 2 | `coleman2006` DOI resolved to an unsigned "SHORT REVIEWS" section. | Corrected to `10.1111/j.1728-4457.2006.00131.x`. |
| 3 | `diazbriquets2014` and `pagegarcia2020` had wrong pagination/issue. | Corrected against Crossref. |
| 4 | `bronnum2023` had the wrong title and a truncated author list. | Corrected. |
| 5 | `albizu2023` had no publisher, URL or DOI while carrying two headline claims. | Replaced with the locatable Horizonte Cubano / Columbia Law report. |
| 6 | **Both SOURCES.md files stated the third-party PDF bundle was gitignored and not redistributed; `literature/sources.zip` (9.7 MB of copyrighted PDFs) was tracked and committed.** | Untracked and added to `.gitignore`. **Note: it remains in git history** — see open items. |
| 7 | `26.7%` (2025 share aged 60+) was attributed to ONEI 3.12 in `charts_internal.py`; 3.12 projects 25.0% and stops observing at 2022, and the Indicadores PDF has no age-structure table. | False attribution removed from the chart; `claims.yaml` marks the value `unverified_reported`; both manuscripts now state the discrepancy. |
| 8 | `audit_claims.py` was a **no-op** — its regex could not match the array form actually used, so every check was skipped. | Rewritten to scan all 45 scripts; verified it fails on an injected regression. It immediately caught live drift (Model D 8.56/8.27 in `charts_final.py`, `chart_triang.py`, `charts_ms.py`), now fixed. |
| 9 | `claims.yaml` described ONEI's published −68,149 natural balance as an earlier draft's arithmetic error. | Reworded as a source discrepancy in ONEI. |
| 10 | Supplement and `provenance.yaml` still advertised the deprecated crude bridge as a live provenance row. | Marked superseded; the attributable-mortality row added. |
| 11 | Three triangulation anchors (MINSAP 10.24, electoral roll 10.00, housing × occupancy 8.70) have no citation anywhere in the repo. | Recorded in `claims.yaml` under `triangulation.unsourced_anchors` so they cannot be described as independent measurements. |

---

## Open — not fixed

1. **`literature/sources.zip` remains in git history.** Untracking stops further
   redistribution but does not remove past commits. Fully removing it requires a
   history rewrite (`git filter-repo`) and a force-push — the author's call.
2. **2023 and 2024 births/deaths have no in-repo provenance.** `90,392` /
   `71,374` / `117,739` / `128,098` appear in none of the shipped ONEI files;
   they come from Anuario editions not included. They should be sourced
   explicitly or the files added.
3. **Selectivity splits (15/77/8, median ages 30/45) remain effectively
   unsourced.** `selectivity.yaml` cites the Albizu reports plus a circular
   reference back to `claims.yaml`. Only median age 45 checks out, and only for
   the whole resident population rather than "stayers".
4. **The 800,000 US settled figure** rests on a self-citation to the repo's own
   CSV plus a Pew section index, and `claims.yaml` already concedes it is a
   "ceiling/floor hybrid".
5. **Model E's expert-coded HSDS inputs** (`healthcare_collapse_web`,
   `epidemic_pressure_web`) cite "Cuban independent press" with no individual
   report identified.
6. **ONEI 3.13 is internally corrupt** for 2017+ (2019 deaths 101,892 against
   3.15's 109,080; non-integer death counts). The loader now flags these rows
   `unreliable` and callers drop them, but the table is still listed as a source
   in `data/SOURCES.md`.
7. **Comparative-context tables** (Venezuela, Puerto Rico, Zimbabwe, regional
   growth) still have no per-row citations.
