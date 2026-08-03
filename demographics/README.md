# Estimating Cuba’s 2021–2026 population decline

Quantitative scenario audit of Cuba’s population loss between **end-2021 and end-2026**.

> **Primary uncertainty.** Across scenarios A–D, cumulative 2021–2025 loss ≈**1.8–2.4 M**.
>
> **Illustrative central scenario (Model D).** ≈**8.59 M** living population at end-2025
> (≈**−2.21 M**, **−20.5%** on the corrected base). Emigration ≈**91%** of absolute loss.
> Model A (ONEI-anchored) remains the floor neighbourhood (≈**9.16 M**).
>
> **Register-gap aside (not the scientific lead).** Against the **official 2021** base,
> the end-2026 gap approaches ~**1 in 4** — a different definition from Model D −20.5%.
>
> **Mortality attributable to health-system collapse.** Age-standardised decomposition
> (`scripts/attributable_mortality.py`), on **observed** ONEI 3.3 age denominators:
> at 2025 levels ≈**28.6k deaths/year** (90% band 18.7–38.3k) are attributable to
> health-system deterioration, against ≈**22.3k/year** explained by ageing alone —
> while the population is ~2 M smaller. Post-COVID 2022–2025 ≈**74.9k** (49.1–101.2k);
> 2024–2025 ≈**50.2k**. This **supersedes** the crude 2019-CDR bridge (~77k for
> 2024–2025, which charged the whole ageing shift to the crisis). Crude registered
> excess 2020–2025 ≈**153k** is a separate, cruder quantity and must not be added.
>
> **Model E (provisional).** Vital reconstruction ≈**8.96 M** end-2025 (−2.13 M, −19.2%).
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
python3 scripts/model_from_2021.py        # Models A–D + 2026 continuation
python3 scripts/attributable_mortality.py # ageing vs health-system decomposition
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

Content: **CC BY 4.0**. Code: repository license (CC0 1.0). ONEI tables: public official data.
