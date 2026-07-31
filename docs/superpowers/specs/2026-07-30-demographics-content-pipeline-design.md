# Design: Demographics content pipeline (EN science / ES public / social IG)

**Date:** 2026-07-30  
**Status:** Approved in conversation; awaiting user review of this written spec  
**Prior audit:** claim conflicts, EN outline-only manuscript, broken `/home/claude/` paths, literature redistributability tension

## Goal

Turn the demographics project into three coherent products fed by one numbers backbone:

| Product | Language | Audience | Format |
|---|---|---|---|
| Scientific paper | English | Researchers (arXiv / Zenodo / journal) | **LaTeX → PDF** |
| Public essay | Spanish | General public / diaspora | Markdown (+ HTML/PDF optional) |
| Social trailer | Spanish | Twitter / Instagram / similar | Infographic + **1:1** and **4:5** crops |
| Notebook | English | Open reproducible companion | Jupyter (aligned to EN paper) |

Do **not** invent new population estimates or change Model D methodology in this pass — document and publish what is already estimated, with consistent definitions.

## Locked decisions

1. **Claim-sheet-first pipeline** (Approach 1).
2. Content sources for the EN paper: notebook spine + `scripts/model_*.py` **and** formal material from `manuscript/es/manuscript.html` (A+B+C).
3. EN citeable artifact is **LaTeX PDF**, analogous to the Spanish manuscript PDF workflow (not Markdown as the final paper).
4. ES `.md` essay keeps public voice; it is **not** the scientific paper.
5. Infographic remains **Spanish** and is optimized for social sharing (not only A2 print).
6. `manuscript/es/manuscript.html` is a **source draft** to mine for EN Methods/Results; after EN LaTeX exists, it is not a third public face (retire, archive, or clearly mark “superseded”).

## Architecture

```
data/claims.yaml  +  scripts/constants.py
         │
         ├──────────► manuscript/en/latex/  → PDF (scientific)
         ├──────────► demographics.ipynb    (companion)
         ├──────────► manuscript/es/*.md    (public essay)
         └──────────► infographic/ + social crops (ES)
```

Scripts write under repo-relative `figures/`, `artifacts/`, `infographic/` only (no `/home/claude/`).

## Claim sheet (`demographics/data/claims.yaml`)

Machine-readable single source of truth. Every public number has an id, value, unit, definition, and allowed products (`en_paper | es_essay | social | notebook`).

### Canonical conflict resolutions

| Family | Rule |
|---|---|
| Model D end-2025 | **8.56 M**; loss **2.31 M (−21.3%)** on corrected base |
| “Quarter” / ¼ language | Only as **~25% by end-2026** vs **official 2021 base** (or cumulative ~2.9 M). Never as Model D −21% to 2025 |
| Excess mortality | **Primary (science + social):** age-adjusted **40–60k in 2024–2025**. **Secondary:** crude registered excess ~153k (2020–25) / ~66k (2024–25) — always labeled |
| Migration share of loss | **~86%** |
| Working-age emigrants | **77%** aged 15–59 (retire bare “80%” or footnote as alternate source) |
| Destinations | **Settled** ledger is primary (~800k US, ~130–135k Spain, …). Encounters / nationality applications are separate rows |
| Vital events | ONEI July 2026: births/deaths **68,064 / 136,214**; deaths 2023 canonical **117,739** (as in MC models); footnote Anuario **117,746** if cited |
| Models A–D | Medians, 90% CIs, end-2026 points from scripts; regenerate claim sheet from runs when possible |

`scripts/constants.py` loads the YAML; models, charts, notebook, and LaTeX build scripts consume it (or a generated `claims.json` / CSV export).

## English scientific paper (LaTeX → PDF)

**Location:** `demographics/manuscript/en/latex/` (e.g. `main.tex`, `refs.bib`, figures via relative paths to `../../figures/`).

**Working draft (optional):** keep/update `manuscript/en/cuba-depopulation-2021-2026.md` as an outline synced to sections — not the submission artifact.

**Target structure (~4–8k words):**

1. Title, author, abstract, keywords  
2. Introduction — three population series; census gap (from notebook + `manuscript.html`)  
3. Methods — accounting identity; priors; Gaussian copula; Models A–D; IMR elasticity ≈0.30; Kitagawa excess; triangulation; destinations ledger; seeds; \(N=10^6\)  
4. Results — tables of medians/CIs; figure captions for `f1`…`f11` set  
5. Discussion — why Model D is preferred given adversarial lean toward A; migration registration lag; dual engine  
6. Limitations — structural vs within-model uncertainty; data gaps  
7. Data & code availability — public repo; ONEI tables; **no** “code on request”  
8. References — proper bibliography (bibliometrics arXiv:2007.09638 is related prior work, not this study’s primary cite)

**Build:** `latexmk` / `pdflatex` locally; optional CI artifact later. Output PDF under `manuscript/en/` (e.g. `cuba-depopulation-2021-2026.pdf`).

## English notebook

- Remains the interactive companion to the EN paper.  
- Loads claim sheet / `artifacts/model_d_summary.json` (produced by `model_d.py` at \(N=10^6\)).  
- May keep a lighter interactive MC (\(N=10^5\)) if clearly labeled.  
- Prefer markdown figures + tables from claims over duplicated narrative that can drift.

## Spanish public essay

**File:** `manuscript/es/cuba-despoblacion-2021-2026.md`

- Keep rhetorical voice (anecdote, second person, adversarial narrative).  
- Front-matter / lede label: *artículo de divulgación* / public communication — not peer-reviewed science.  
- All quantitative claims from claim sheet.  
- Fix broken `es_*.png` references → `figures/f*.png` or dedicated social exports.  
- Replace “código a pedido” with GitHub/Pages links.  
- Soften or footnote speculative 2030 “6 millones” on social-facing excerpts.

## Spanish social infographic

- Keep A2 print asset if useful.  
- Add **1:1** and **4:5** crops for Twitter/IG.  
- Headline must follow claim-sheet “quarter” rule (year + base explicit).  
- On-card excess: **40–60 mil (2024–25, ajustado por edad)** only, unless a second labeled line fits.  
- CTA: link to Spanish essay + EN PDF/DOI when available.  
- Remove or replace placeholder Zenodo `XXXXXXX` when DOI exists.

## Reproducibility & data packaging

1. Fix all script I/O to repo-relative paths.  
2. Centralize constants via claim sheet.  
3. Commit small summary artifacts (`artifacts/*.json`) from full MC runs — not million-draw dumps.  
4. Add `data/destinations_settled.csv` (aggregated public stats only).  
5. Literature: **prefer cite-only** for third-party PDFs; if a local zip is kept for the author, **gitignore** it and document URLs in `literature/SOURCES.md` / `data/SOURCES.md` (resolve current contradiction).  
6. Document seeds and software versions in EN paper Data/Code section.

## Out of scope

- Re-estimating population or changing Model D priors/elasticity.  
- Bilingual infographic.  
- Full journal typesetting beyond a clean LaTeX preprint.  
- Committing `PROJECT-MEMORY.md`.

## Success criteria

1. `claims.yaml` exists; EN PDF, ES essay, IG, and notebook agree on every headline number/definition.  
2. EN LaTeX builds to a complete IMRaD PDF with figures and bibliography.  
3. ES essay is clearly labeled as public communication and figure links work.  
4. Social crops (1:1, 4:5) exist in Spanish with claim-safe headline.  
5. Scripts run without `/home/claude/` paths; Model D summary artifact regenerates claims or validates them.  
6. Literature policy is consistent (no silent redistribution conflict).  
7. “Code on request” language removed from public-facing texts.

## Implementation order (for the plan)

1. Claim sheet + constants module + conflict fixes  
2. Path fixes + Model D summary artifact + destinations CSV  
3. Literature policy cleanup  
4. EN LaTeX paper (content from notebook + `manuscript.html` + claims)  
5. Notebook alignment  
6. ES essay retarget + figure fixes  
7. Infographic social crops + headline fix  
8. README / citation / optional Pages link to EN PDF
