# Design: CubaScience multi-theme repo + demographics notebook

**Date:** 2026-07-30  
**Status:** Approved in conversation; awaiting user review of this written spec  
**Related prior work:** [arXiv:2007.09638](https://arxiv.org/abs/2007.09638) (Cuban research output); new study on Cuban demographic crisis 2019–2026

## Goal

Reorganize `cubascience` into a **multi-theme hub** with two peer projects (science bibliometrics + demographics), a GitHub Pages landing page, and a **self-hosted English Jupyter notebook** for demographics that mirrors the role of `ciencia.ipynb` for the arXiv paper. Prepare bilingual (ES/EN) manuscripts for the demographics study. Keep the repo within GitHub size limits by zipping bulky literature.

## Decisions (locked)

| Decision | Choice |
|---|---|
| Repo scope | One multi-theme repo; science + demographics as peers |
| Demographics notebook | Full English paper companion (narrative + code + figures) |
| Hosting | Single Pages site: landing + `/science/` + `/demographics/` |
| Folder move | Full peer layout (`science/`, `demographics/`); root is hub only |
| Project memory | English local file; **gitignored**; never pushed or deployed |
| Large files | Zip literature PDFs; keep ONEI tables and site assets unzipped |

## Target repository layout

```
cubascience/
├── README.md
├── index.html                      # Landing: Science | Demographics
├── LICENSE
├── .gitignore                      # includes demographics project memory
├── .github/workflows/pages.yml
├── docs/superpowers/specs/         # design/plan docs
├── science/
│   ├── README.md
│   ├── ciencia.ipynb               # companion to arXiv:2007.09638
│   ├── analysis.py
│   ├── data/
│   └── images/
└── demographics/
    ├── README.md
    ├── demographics.ipynb          # NEW English paper companion
    ├── requirements.txt
    ├── PROJECT-MEMORY.md           # English; gitignored; not committed
    ├── manuscript/
    │   ├── es/cuba-despoblacion-2019-2026.md
    │   └── en/cuba-depopulation-2019-2026.md
    ├── infographic/
    ├── figures/
    ├── scripts/
    ├── data/
    │   ├── onei/                   # official ONEI .xls (canonical)
    │   └── SOURCES.md
    └── literature/
        ├── SOURCES.md              # inventory + origin URLs
        └── sources.zip             # PDFs / bulky non-essential refs
```

### Moves and cleanup

- Root bibliometrics (`ciencia.ipynb`, `data/`, `images/`, `analysis.py`) → `science/`
- `cuba-demographics/` → `demographics/`
- Duplicate `.xls` at the old demographics root → keep only under `data/onei/`
- Loose literature PDFs → `literature/sources.zip` + entries in `literature/SOURCES.md`
- Remove or stop tracking Spanish `MEMORIA-DEL-PROYECTO.md`; replace with gitignored English `PROJECT-MEMORY.md`
- Delete obsolete `.travis.yml` after Actions workflow works

## English notebook outline (`demographics/demographics.ipynb`)

Full reproducible companion (English), analogous to `ciencia.ipynb`:

1. Title, citation block, abstract; situate within CubaScience and cite arXiv:2007.09638 as the prior science study
2. Three population series (UN / ONEI / independent); figure
3. Demographic accounting identity; births vs deaths (“scissors”)
4. Models A–D via Monte Carlo (10⁶ iterations, Gaussian copula); Model D preferred (infant-mortality sentinel)
5. Triangulation of eight administrative sources; probable band ~8.0–8.9 M
6. Age-standardized excess mortality (~40–60k in 2024–2025)
7. Selectivity (age / sex / province) and destinations ledger
8. Projection through end of 2026
9. Conclusions and limitations (census delay, migration registration lag)

**Technical constraints:** relative paths only; reuse `scripts/` (import or thin wrappers); figures under `figures/`; convertible via `nbconvert` to `site/demographics/index.html`.

## Manuscripts

| Artifact | Location | Notes |
|---|---|---|
| Spanish manuscript | `demographics/manuscript/es/` | Move existing Spanish draft |
| English manuscript | `demographics/manuscript/en/` | New; aligned with notebook narrative |
| Infographic | `demographics/infographic/` | Remains Spanish-first unless changed later |
| Project memory | `demographics/PROJECT-MEMORY.md` | English; **`.gitignore`**; never deployed |

Notebook = interactive English companion. Manuscripts = citeable long-form ES/EN.

## CI / GitHub Pages

Replace Travis with GitHub Actions (`.github/workflows/pages.yml`):

1. Install dependencies for science + demographics
2. `nbconvert` `science/ciencia.ipynb` → `site/science/index.html`
3. `nbconvert` `demographics/demographics.ipynb` → `site/demographics/index.html`
4. Copy root landing `index.html` (and needed assets) into `site/`
5. Deploy `site/` to GitHub Pages

**URLs:**

- `https://ypriverol.github.io/cubascience/` — hub landing
- `/science/` — bibliometrics notebook HTML
- `/demographics/` — demographics notebook HTML

Landing presents both projects as equals, with cite links (Zenodo/arXiv for science; demographics cite block uses “preprint / Zenodo forthcoming” until a DOI exists).

Build output lives in `site/` (gitignored); only Actions publishes it to Pages.

## Size and packaging policy

- No committed file over GitHub’s 100 MB limit; prefer a lean working tree
- **Unzipped in git:** ONEI `.xls`, notebooks, scripts, figures needed by notebook/site
- **Zipped:** literature PDFs and other bulky non-essential references → `literature/sources.zip`
- **Documented only (not in repo):** anything that still cannot be stored; list download URL in `SOURCES.md`
- Deduplicate before commit; canonical ONEI path is `demographics/data/onei/`

## Out of scope (this redesign)

- Changing Model D methodology or re-estimating population numbers
- Rewriting the Spanish manuscript content beyond file moves
- Making the infographic bilingual
- Committing `PROJECT-MEMORY.md`
- Force-preserving old root notebook URL as the sole site content (landing replaces it; science moves to `/science/`)

## Success criteria

1. Repo root is a clear hub; `science/` and `demographics/` are self-contained peers
2. English `demographics.ipynb` runs locally and builds to Pages HTML
3. Landing page links both projects
4. Literature PDFs are in `sources.zip` (or documented externally); no duplicate ONEI tables at project root
5. `PROJECT-MEMORY.md` exists in English locally and is ignored by git
6. Travis removed; Actions deploys `site/` successfully
7. Root README documents both studies and how to reproduce notebooks

## Implementation notes (for the plan)

- Update import/data paths in `ciencia.ipynb` and demographics scripts after the move
- Use official GitHub Pages Actions (`actions/upload-pages-artifact` + `actions/deploy-pages`)
- Per-project `requirements.txt` (`science/` may keep or inherit current root pins; `demographics/` gets its own). Root keeps only a minimal CI helper list if needed
- English manuscript may start as a structured outline aligned to the notebook sections if full prose is not ready in the first pass; **notebook narrative is the priority deliverable**
- `.gitignore` must include at least: `site/`, `demographics/PROJECT-MEMORY.md`, `.ipynb_checkpoints/`, and common Python/build junk
