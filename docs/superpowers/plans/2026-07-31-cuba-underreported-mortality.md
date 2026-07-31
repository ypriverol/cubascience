# Cuba vital-event reconstruction via health deterioration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** From ageing, health-system decadence, and documented official underreporting, reconstruct **true deaths**, **true births**, and then a **final living population** — Model E, an end-to-end companion (or successor) to today’s Model D.

**Architecture:** Index-first vital reconstruction.

```text
Excel + web signals
        ↓
Health-System Deterioration Score S_t
        ↓
┌───────────────────┬────────────────────┐
│  True deaths D*_t │  True births B*_t   │
└─────────┬─────────┴──────────┬─────────┘
          │                    │
          └──────────┬─────────┘
                     ↓
        P*_t = P*_{t-1} + B*_t − D*_t − M*_t
                     ↓
        end-2025 / end-2026 population band
```

Migration \(M^*\) still uses destinations + ONEI, but **deaths and births are reconstructed**, not treated as nearly-complete registers. Ageing shapes both the death schedule and the fertile-woman base. Health decadence and bad reporting (including COVID misuse) raise the deterioration score that drives \(D^*\) and \(B^*\).

**Tech Stack:** Python 3, numpy/scipy, pandas, PyYAML, matplotlib/seaborn; web search (cite-only).

## Global Constraints

- Outputs are always three labeled series: **true deaths**, **true births**, **true population** (vs ONEI).
- Ageing is first-class (ONEI 3.12/3.3 + selective emigration).
- Health decadence + official misuse feed a **deterioration score**, not a raw ×30 on all deaths.
- Local ONEI Excels are the spine; web sources score severity.
- Claim-sheet hygiene: “one in four” stays official 2021 → end-2026 until explicitly redefined.
- Provisional name: **Model E**; do not silent-overwrite preferred Model D.
- Paths: `demographics/scripts/`, `demographics/artifacts/`, `demographics/data/claims.yaml`.

### One-sentence product

**Ageing + collapsing health system + history of bad official numbers → how many really die and are born → how many are really left.**

---

## File structure

| File | Responsibility |
|---|---|
| `demographics/data/mortality_signals.yaml` | Features, weights, transfer priors |
| `demographics/data/hsds_features.csv` | Year×feature matrix |
| `demographics/scripts/mortality_data.py` | ONEI Excel loaders |
| `demographics/scripts/hsds_features.py` | Normalized features |
| `demographics/scripts/hsds_score.py` | Score \(S_t\) |
| `demographics/scripts/hsds_deaths.py` | Ageing × decadence → \(D^*_t\) |
| `demographics/scripts/hsds_births.py` | Fertile stock × crisis fertility → \(B^*_t\) |
| `demographics/scripts/hsds_population.py` | Model E population MC |
| `demographics/scripts/hsds_ensemble.py` | Compare E vs A–D; claims proposal |
| `demographics/artifacts/model_e_summary.json` | B*, D*, M*, P* posteriors |
| `demographics/scripts/charts_hsds.py` | Score, vitals, population figures |
| `demographics/manuscript/en/latex/main.tex` | Model E write-up after stable |

Identity:

\[
P^*_{2025}=P^*_{2021}+\sum_{t=2022}^{2025}(B^*_t-D^*_t-M^*_t),\quad
P^*_{2021}=P^{\mathrm{off}}_{2021}-U_0
\]

---

### Task 1: Feature dictionary (ageing + decadence + bad reporting)

**Files:**
- Create: `demographics/data/mortality_signals.yaml`
- Create: `demographics/artifacts/hsds_feature_dictionary.md`
- Modify: `demographics/literature/SOURCES.md`

- [ ] **Step 1: Confirm Excel inventory**

```bash
ls demographics/data/onei/3.15* demographics/data/onei/3.16* demographics/data/onei/3.17* demographics/data/onei/3.12* demographics/data/onei/3.13* demographics/data/onei/3.3*
```

- [ ] **Step 2: Define features in three buckets**

```yaml
buckets:
  ageing:
    - elderly_share_60plus
    - median_age_proxy
    - fertile_women_share_proxy
  health_decadence:
    - imr_rise
    - cdr_rise
    - mmr_rise
    - e0_gap
    - healthcare_collapse_web
    - epidemic_pressure_web
  bad_reporting:
    - covid_misuse_ratio_norm
    - onei_migration_seam_flag
    - stats_opacity_vs_independents
```

COVID misuse = normalized integrity/severity feature (e.g. \(\log_{10}\) of excess÷label), **not** a direct multiplier on all deaths.

- [ ] **Step 3: Commit**

```bash
git add demographics/data/mortality_signals.yaml demographics/artifacts/hsds_feature_dictionary.md demographics/literature/SOURCES.md
git commit -m "Define HSDS features for vital-event population reconstruction."
```

---

### Task 2: Yearly feature matrix (Excels + public severity)

**Files:**
- Create: `demographics/scripts/mortality_data.py`
- Create: `demographics/scripts/hsds_features.py`
- Create: `demographics/scripts/test_hsds_features.py`
- Create: `demographics/data/hsds_features.csv`
- Create: `demographics/artifacts/public_health_signals.md`

- [ ] **Step 1: Write failing test — norms in [0,1]**

```python
from hsds_features import build_feature_matrix

def test_norms_bounded():
    df = build_feature_matrix()
    assert df["value_norm"].between(0, 1).all()
```

- [ ] **Step 2: Implement ONEI loaders + web severity 0–1 by year**

- [ ] **Step 3: Write CSV; commit**

```bash
git add demographics/scripts/mortality_data.py demographics/scripts/hsds_features.py demographics/scripts/test_hsds_features.py demographics/data/hsds_features.csv demographics/artifacts/public_health_signals.md
git commit -m "Build HSDS feature matrix for vital reconstruction."
```

---

### Task 3: Deterioration score \(S_t\)

**Files:**
- Create: `demographics/scripts/hsds_score.py`
- Create: `demographics/scripts/test_hsds_score.py`
- Create: `demographics/artifacts/hsds_scores.json`

- [ ] **Step 1: Weighted score + weight bootstrap**

```python
def score_years(n_boot=1000, seed=2027) -> "pd.DataFrame":
    # year, S_median, S_p05, S_p95
    ...
```

- [ ] **Step 2: Sanity — high \(S\) in 2021 and 2024–25; low in 2019**

- [ ] **Step 3: Commit**

```bash
git add demographics/scripts/hsds_score.py demographics/scripts/test_hsds_score.py demographics/artifacts/hsds_scores.json
git commit -m "Compute yearly health-system deterioration scores."
```

---

### Task 4: True deaths \(D^*_t\)

**Files:**
- Create: `demographics/scripts/hsds_deaths.py`
- Create: `demographics/scripts/test_hsds_deaths.py`
- Create: `demographics/artifacts/model_e_deaths.json`

```text
Expected_from_ageing_t = Σ_a m_a,base · P*_a,t   # 2019 schedule on aged stock
Decadence_uplift_t     = f(S_t)                 # rates worse when system collapses
D*_t                   = Expected_from_ageing_t · Decadence_uplift_t · ε
H_t                    = max(D*_t − D_reg_t, 0)
```

- [ ] **Step 1: Age-schedule expected deaths from 3.15 + age stocks**

- [ ] **Step 2: Map \(S_t\) → uplift with MC priors**

- [ ] **Step 3: Save \(D^*\) / \(H\) bands for 2022–2025; commit**

```bash
git add demographics/scripts/hsds_deaths.py demographics/scripts/test_hsds_deaths.py demographics/artifacts/model_e_deaths.json
git commit -m "Estimate true deaths from ageing and deterioration score."
```

---

### Task 5: True births \(B^*_t\)

**Files:**
- Create: `demographics/scripts/hsds_births.py`
- Create: `demographics/scripts/test_hsds_births.py`
- Create: `demographics/artifacts/model_e_births.json`

```text
Women_fertile*_t = age structure under selective emigration
TFR*_t           = crisis path · g(S_t)
B*_t             = fertility exposure · ASFR(TFR*_t) · ε
```

Registered births are a strong anchor; allow \(B^*\) near \(B^{\mathrm{reg}}\) unless score + missing-women evidence say otherwise. Use published TFR 1.29 (2025) as a floor/anchor.

- [ ] **Step 1: Fertile-age stock under 77% working-age exit**

- [ ] **Step 2: Link \(S_t\) to extra TFR depression**

- [ ] **Step 3: Save \(B^*\) band; commit**

```bash
git add demographics/scripts/hsds_births.py demographics/scripts/test_hsds_births.py demographics/artifacts/model_e_births.json
git commit -m "Estimate true births under exit and crisis fertility."
```

---

### Task 6: Population from reconstructed vitals (Model E)

**Files:**
- Create: `demographics/scripts/hsds_population.py`
- Create: `demographics/scripts/hsds_ensemble.py`
- Create: `demographics/artifacts/model_e_summary.json`

```python
P = official_2021 - U0
for t in 2022..2025:
    P = P + B_star[t] - D_star[t] - M_star[t]
# 2026 nowcast
```

\(M^*\): reuse Model D migration bridge; optionally correlate higher \(S_t\) with more exit.

- [ ] **Step 1: Model E MC \(N=10^6\)**

- [ ] **Step 2: Table vs A–D (pop, loss %, mig share, natural decrease share)**

- [ ] **Step 3: Propose claims Model E block without overwriting D**

- [ ] **Step 4: Commit**

```bash
git add demographics/scripts/hsds_population.py demographics/scripts/hsds_ensemble.py demographics/artifacts/model_e_summary.json
git commit -m "Add Model E population from reconstructed births and deaths."
```

---

### Task 7: Charts + manuscript

**Files:**
- Create: `demographics/scripts/charts_hsds.py`
- Create: `demographics/figures/f12_hsds_vitals.png`
- Create: `demographics/figures/f13_model_e_population.png`
- Modify: `demographics/manuscript/en/latex/main.tex`
- Modify: `demographics/README.md`

- [ ] **Step 1: Plot \(S_t\), \(D^*\) vs \(D^{\mathrm{reg}}\), \(B^*\) vs \(B^{\mathrm{reg}}\)**

- [ ] **Step 2: Plot Model E vs D population path**

- [ ] **Step 3: Methods/Results; rebuild PDF; commit**

```bash
cd demographics/manuscript/en/latex && latexmk -pdf -interaction=nonstopmode main.tex
cp main.pdf ../cuba-depopulation-2019-2026.pdf
git add demographics/scripts/charts_hsds.py demographics/figures/f12_hsds_vitals.png demographics/figures/f13_model_e_population.png demographics/manuscript/en/latex/main.tex demographics/manuscript/en/cuba-depopulation-2019-2026.pdf demographics/README.md
git commit -m "Document Model E vital reconstruction in figures and preprint."
```

---

### Task 8: Adversarial gate before promoting Model E

**Files:**
- Create: `demographics/artifacts/model_e_adversarial_notes.md`
- Modify: `demographics/data/claims.yaml` (only if promote)

Checks:
- Are \(B^*\) and \(D^*\) identified separately, or only \(B^*-D^*\)?
- Does high \(S\) double-count ageing already in the death schedule?
- Is COVID misuse overweighting the score?
- Does E actually change population vs D, or only re-label components?
- Promote only with an explicit decision.

- [ ] **Step 1: Write notes + keep/promote**

- [ ] **Step 2: If promote — update preferred model and public copy carefully**

- [ ] **Step 3: Commit**

---

## Success

1. Yearly deterioration score from ageing + health decadence + bad reporting.  
2. Reconstructed **deaths** and **births** with uncertainty.  
3. Reconstructed **population** (Model E) comparable to A–D.  
4. Clear decision whether E replaces or sits beside D.

## Spec coverage

| Your intent | Task |
|---|---|
| Ageing population | 1, 4, 5 |
| Health-system decadence | 1–4 |
| Bad official reports (incl. COVID) | 1–3 |
| Estimate deaths | 4 |
| Estimate births | 5 |
| Final population from those | 6 |
