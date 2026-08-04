# Estimating Cuba’s 2021–2026 population decline

Quantitative scenario audit of Cuba’s population loss between **end-2021 and end-2026**.

> **One base: the official end-2021 stock (11,113,215).** The gap by end-2025 spans
> **1.97–2.79 M (17.8–25.1%)** across three assumption sets. A **null** scenario taking
> ONEI at face value gives 1.68 M and reproduces the official figure exactly.
>
> **Central scenario.** ≈**8.58 M** living at end-2025 against 9.43 M officially — a gap of
> **2.53 M (22.8%)**, of which **1.68 M is decline ONEI itself published** and **0.85 M is
> this paper's correction**. The 0.85 M is the actual claim. Emigration ≈**92%** of the gap.
>
> Point figures are closed-form arithmetic on three prior means; no parameter is informed
> by a likelihood, and the ranges are prior sensitivity ranges, not confidence intervals.
>
> **Excess mortality against the 2019 age-specific schedule.** Age-standardised decomposition
> (`scripts/attributable_mortality.py`), on **observed** ONEI 3.3 age denominators:
> at 2025 levels ≈**28.5k deaths/year** (prior sensitivity range 18.6–38.2k) of **excess
> against the 2019 age-specific schedule** — deliberately *not* called "attributable to
> health-system deterioration" — against ≈**22.4k/year** explained by ageing alone.
> Post-COVID 2022–2025 ≈**74.8k** (47.0–103.0k); 2024–2025 ≈**50.1k**. Counterfactual
> choice moves these more than the simulation does: 23.7–38.0k and 60.5–103.3k. This **supersedes** the crude 2019-CDR bridge (~77k for
> 2024–2025, which charged the whole ageing shift to the crisis). Crude registered
> excess 2020–2025 ≈**153k** is a separate, cruder quantity and must not be added.
>
> **Model E is retired.** It was superseded by the age-standardised excess-mortality
> decomposition, which estimates the same quantity from observed age denominators.
> Its numeric results are not reproduced here: a retired headline that stays in a
> README gets quoted as current.
> Not preferred (different \(U_0\); ageing double-count risk). Details in the supplement.

The Monte Carlo window starts at **official end-2021** (11,113,215), not 2019.
Pre-crisis 2019 rates still appear only as methodological baselines (age schedule, IMR rise).
Models A–D are **scenarios**, not identified estimators.

## Products

Both manuscripts are scientific preprints with the same structure
(Introduction / Methods / Results / Discussion / Disclaimers), the same figures
and the same numbers. The Spanish version is a mirror of the English one, not a
separate essay.

| Product | Lang | Audience | Path |
|---|---|---|---|
| Scientific preprint | EN | Researchers | [`manuscript/en/latex/`](manuscript/en/latex/) → [`cuba-depopulation-2021-2026.pdf`](manuscript/en/cuba-depopulation-2021-2026.pdf) |
| Scientific preprint | ES | Researchers / diaspora | [`manuscript/es/latex/`](manuscript/es/latex/) → [`Cuba_despoblacion_2021-2026_manuscrito.pdf`](manuscript/es/Cuba_despoblacion_2021-2026_manuscrito.pdf) |
| Supplement | EN | Researchers | [`cuba-depopulation-2021-2026-supplement.pdf`](manuscript/en/cuba-depopulation-2021-2026-supplement.pdf) (Model E; LE; provinces) |
| Web Markdown | EN + ES | Site | `manuscript/*/*.md` — **generated** from LaTeX, do not hand-edit |
| Social infographic | ES | Twitter / IG | [`infographic/`](infographic/) + `social_1x1.png`, `social_4x5.png` |
| Notebook companion | EN | Open science | [`demographics.ipynb`](demographics.ipynb) · [Pages](https://ypriverol.github.io/cubascience/demographics/) |

**Numbers source of truth:** [`data/claims.yaml`](data/claims.yaml)

Related bibliometrics study: [arXiv:2007.09638](https://arxiv.org/abs/2007.09638)

## Build the PDFs

```bash
cd manuscript/en/latex && latexmk -pdf main.tex && latexmk -pdf supplement.tex
cp main.pdf ../cuba-depopulation-2021-2026.pdf
cp supplement.pdf ../cuba-depopulation-2021-2026-supplement.pdf

cd ../../es/latex && latexmk -pdf main.tex
cp main.pdf ../Cuba_despoblacion_2021-2026_manuscrito.pdf

# Web Markdown is derived from the LaTeX (needs pandoc):
python3 ../../../scripts/render_manuscript_md.py
```

## Regenerate models and charts (600 dpi manuscript PNGs; 400 dpi IG)

```bash
cd demographics
export MPLBACKEND=Agg
python3 scripts/model_population.py        # scenarios: null/conservative/central/upper
python3 scripts/attributable_mortality.py # ageing vs rate-deterioration decomposition
python3 scripts/age_standardised_mortality.py # WHO-standardised ASMR + SMR
python3 scripts/consistency_model.py       # 18 internal-consistency tests
python3 scripts/charts_publication.py     # ES infographic + EN manuscript figures
python3 scripts/charts_manuscript_es.py   # ES manuscript figure set (f*_es.png)
python3 scripts/charts_attributable.py    # f14 attributable mortality (EN + ES)
python3 scripts/charts_hsds.py            # Model E / HSDS figures (f12, f13)
python3 scripts/audit_claims.py           # claims.yaml vs script literals
```

Infographic panels: `infographic/ig_*.png` (6 charts, 400 dpi).  
Manuscript figures: `figures/f*.png` (English labels) and `figures/f*_es.png`
(Spanish labels), 600 dpi for the LaTeX papers.

Model E scripts: `scripts/hsds_*.py` (features → score → deaths → births → population).
Artifacts: `artifacts/model_e_summary.json`, `artifacts/hsds_scores.json`.

## Cite

> Pérez-Riverol, Y. (2026). *Estimating Cuba’s 2021–2026 population decline.* Preprint.
> PDF: `demographics/manuscript/en/cuba-depopulation-2021-2026.pdf`
> (+ supplement). Zenodo DOI forthcoming.

## License

Content: **CC0 1.0** (see `LICENSE`; an earlier version of this line said CC BY 4.0, which no shipped licence text supported). Code: repository license (CC0 1.0). ONEI tables: public official data.
