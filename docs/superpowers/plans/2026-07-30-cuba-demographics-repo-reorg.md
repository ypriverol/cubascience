# CubaScience multi-theme reorg + demographics notebook

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the repo into peer `science/` and `demographics/` projects, add an English self-hosted demographics Jupyter companion, bilingual manuscript folders, GitHub Pages landing + Actions CI, and zip bulky literature.

**Architecture:** Root becomes a hub (README + landing HTML). Bibliometrics moves to `science/` with relative paths unchanged inside that folder. Demographics becomes `demographics/` with `demographics.ipynb` as the English paper companion, manuscripts under `manuscript/{es,en}/`, literature PDFs in `literature/sources.zip`, and project memory gitignored.

**Tech Stack:** Python 3, Jupyter/`nbconvert`, numpy/scipy/matplotlib/plotly, GitHub Actions Pages.

## Global Constraints

- Do not commit `demographics/PROJECT-MEMORY.md` (gitignored English project memory)
- Do not change Model D methodology or re-estimate population numbers
- Relative paths only inside notebooks
- Official Pages deploy via `actions/upload-pages-artifact` + `actions/deploy-pages`
- `site/` is build output and gitignored
- No commits unless the user explicitly asks (user rule overrides “commit each task”)

---

### Task 1: Peer directory reorganization

**Files:**
- Move: root `ciencia.ipynb`, `analysis.py`, `data/`, `images/` → `science/`
- Move: `cuba-demographics/` → `demographics/`
- Create: `science/README.md`, `science/requirements.txt`
- Modify: `.gitignore`

**Interfaces:**
- Produces: `science/` and `demographics/` as canonical project roots

- [x] **Step 1:** Create `science/`; move bibliometrics files into it
- [x] **Step 2:** Rename `cuba-demographics` → `demographics`
- [x] **Step 3:** Deduplicate loose root `.xls` into `demographics/data/onei/` (keep ONEI copies only)
- [x] **Step 4:** Update `.gitignore` for `site/`, `demographics/PROJECT-MEMORY.md`, checkpoints
- [x] **Step 5:** Verify `ls science demographics` and that science notebook still references `data/...` relatively

---

### Task 2: Literature zip + English project memory

**Files:**
- Create: `demographics/literature/SOURCES.md`, `demographics/literature/sources.zip`
- Create: `demographics/PROJECT-MEMORY.md` (gitignored)
- Modify: `demographics/data/SOURCES.md` if needed
- Delete: loose PDFs at `demographics/*.pdf` after zip

**Interfaces:**
- Produces: local/repo literature archive; English memory file ignored by git

- [ ] **Step 1:** Create `demographics/literature/`; zip all loose PDFs into `sources.zip`
- [ ] **Step 2:** Write `literature/SOURCES.md` inventory
- [ ] **Step 3:** Translate former `MEMORIA-DEL-PROYECTO.md` → `PROJECT-MEMORY.md` (English); remove/stop tracking Spanish memoria
- [ ] **Step 4:** Confirm `git check-ignore demographics/PROJECT-MEMORY.md` succeeds

---

### Task 3: Manuscript ES/EN layout

**Files:**
- Move: existing Spanish md/html/pdf into `demographics/manuscript/es/`
- Create: `demographics/manuscript/en/cuba-depopulation-2021-2026.md` (structured outline aligned to notebook)

- [ ] **Step 1:** Create `manuscript/es` and `manuscript/en`
- [ ] **Step 2:** Move Spanish manuscript artifacts into `es/`
- [ ] **Step 3:** Write English manuscript outline (sections mirroring notebook)

---

### Task 4: English demographics notebook

**Files:**
- Create: `demographics/demographics.ipynb`
- Create/Modify: thin helpers under `demographics/scripts/` if needed for imports
- Modify: `demographics/requirements.txt`

**Interfaces:**
- Consumes: constants/results from `scripts/cuba_mc.py`, `model_d.py`, chart scripts / precomputed figures
- Produces: runnable English companion notebook

- [ ] **Step 1:** Scaffold notebook with markdown sections 1–9 from the design
- [ ] **Step 2:** Add code cells that reproduce key tables/figures (prefer calling existing scripts or embedding verified anchor numbers + showing existing `figures/`)
- [ ] **Step 3:** Smoke-test: `jupyter nbconvert --execute` or at least validate JSON + import paths
- [ ] **Step 4:** Write `demographics/README.md` for the cleaned project

---

### Task 5: Hub landing page + root README

**Files:**
- Create: root `index.html`
- Modify: root `README.md`
- Create: minimal shared CI `requirements.txt` at root if needed

- [ ] **Step 1:** Write landing HTML linking `/science/` and `/demographics/`
- [ ] **Step 2:** Rewrite root README as multi-theme hub (cite arXiv:2007.09638 + demographics)

---

### Task 6: GitHub Actions Pages workflow

**Files:**
- Create: `.github/workflows/pages.yml`
- Delete: `.travis.yml` when Actions file is in place

- [ ] **Step 1:** Add workflow: install deps, nbconvert both notebooks into `site/`, copy landing, upload/deploy Pages artifact
- [ ] **Step 2:** Locally dry-run nbconvert into `site/` to verify paths
- [ ] **Step 3:** Remove `.travis.yml`

---

### Task 7: Path fixes + verification

**Files:**
- Modify: any absolute paths in `demographics/scripts/render_*.py`
- Modify: science notebook only if paths break after move

- [ ] **Step 1:** Grep for absolute `/Users/` paths; fix to relative
- [ ] **Step 2:** Verify directory tree matches design
- [ ] **Step 3:** Run Codacy CLI on edited Python/workflow files if available

---

## Done when

All success criteria from `docs/superpowers/specs/2026-07-30-cuba-demographics-repo-design.md` are met locally (Pages deploy may await push + repo settings).
