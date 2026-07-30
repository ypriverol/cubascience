# Demographics content pipeline implementation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Claim-sheet-first pipeline: EN LaTeX scientific PDF, ES public essay, Spanish social infographic crops, reproducible scripts/notebook.

**Architecture:** `data/claims.yaml` + `scripts/constants.py` feed all products; scripts use repo-relative `artifacts/` and `figures/`; EN paper in `manuscript/en/latex/`.

**Tech Stack:** Python, PyYAML, numpy/scipy, LaTeX (`latexmk`), Jupyter, HTML infographic.

## Global Constraints

- EN scientific artifact is LaTeX → PDF (not Markdown)
- ES essay = public communication; keep voice
- Infographic = Spanish social (+ A2 optional)
- Do not change Model D methodology / re-estimate populations
- Do not commit `PROJECT-MEMORY.md`
- Prefer cite-only for third-party literature (gitignore zip if kept locally)
- Deaths 2023 canonical: 117,739
- No commits unless user asks

---

### Task 1: Claim sheet + constants

**Files:**
- Create: `demographics/data/claims.yaml`
- Create: `demographics/scripts/constants.py`
- Modify: `demographics/scripts/notebook_support.py`
- Modify: `demographics/requirements.txt` (add pyyaml)

- [ ] Write claims.yaml with all canonical numbers + definitions
- [ ] Write constants.py loader
- [ ] Point notebook_support at constants
- [ ] Smoke: `python -c "from constants import claims; print(claims['model_d']['pop_end_2025_m'])"`

---

### Task 2: Path fixes + Model D artifact

**Files:**
- Create: `demographics/artifacts/` (+ `.gitkeep`)
- Modify: `scripts/model_d.py` and other scripts with `/home/claude/`
- Create: `artifacts/model_d_summary.json` via running model_d (or export helper)

- [ ] Add path helper / replace `/home/claude/` → artifacts/figures
- [ ] Run model_d; write JSON summary
- [ ] Add destinations_settled.csv

---

### Task 3: Literature policy

- [ ] Gitignore `literature/sources.zip`
- [ ] Update SOURCES.md files to cite-only

---

### Task 4: EN LaTeX paper

**Files:**
- Create: `manuscript/en/latex/main.tex`, `refs.bib`, build to PDF

- [ ] Scaffold article class paper
- [ ] Fill IMRaD from manuscript.html + notebook + claims
- [ ] Include figures from `../../figures/`
- [ ] Build PDF with latexmk

---

### Task 5: Notebook alignment

- [ ] Load claims/constants; document Model D artifact
- [ ] Re-execute lightly if needed

---

### Task 6: ES essay retarget

- [ ] Divulgación label; fix figure paths; repo link; claim-safe quarter/excess language

---

### Task 7: Infographic social

- [ ] Fix headline in infografia.html
- [ ] Generate 1:1 and 4:5 crops (Pillow/ffmpeg or HTML variants)

---

### Task 8: README updates

- [ ] Document three products + how to build LaTeX PDF
