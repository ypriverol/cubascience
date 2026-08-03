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
> **Provisional mortality residual.** Illustrative 2019-schedule residual ≈**~77k** in
> 2024–2025 (sensitivity 65–90k), coarse bridge in `scripts/mortality_schedule_residual.py`.
> Crude registered excess 2020–2025 ≈**153k** is a separate quantity.
>
> **Model E (provisional).** Vital reconstruction ≈**8.96 M** end-2025 (−2.13 M, −19.2%).
> Not preferred (different \(U_0\); ageing double-count risk). Details in the supplement.

The Monte Carlo window starts at **official end-2021** (11,113,215), not 2019.
Pre-crisis 2019 rates still appear only as methodological baselines (age schedule, IMR rise).
Models A–D are **scenarios**, not identified estimators.

## Three products

| Product | Lang | Audience | Path |
|---|---|---|---|
| Scientific preprint | EN | Researchers | [`manuscript/en/latex/`](manuscript/en/latex/) → [`cuba-depopulation-2021-2026.pdf`](manuscript/en/cuba-depopulation-2021-2026.pdf) |
| Supplement | EN | Researchers | [`cuba-depopulation-2021-2026-supplement.pdf`](manuscript/en/cuba-depopulation-2021-2026-supplement.pdf) (Model E; LE; provinces) |
| Public essay | ES | General / diaspora | [`manuscript/es/cuba-despoblacion-2021-2026.md`](manuscript/es/cuba-despoblacion-2021-2026.md) |
| Social infographic | ES | Twitter / IG | [`infographic/`](infographic/) + `social_1x1.png`, `social_4x5.png` |
| Notebook companion | EN | Open science | [`demographics.ipynb`](demographics.ipynb) · [Pages](https://ypriverol.github.io/cubascience/demographics/) |

**Numbers source of truth:** [`data/claims.yaml`](data/claims.yaml)

Related bibliometrics study: [arXiv:2007.09638](https://arxiv.org/abs/2007.09638)

## Build the English PDF

```bash
cd manuscript/en/latex
latexmk -pdf main.tex
latexmk -pdf supplement.tex
cp main.pdf ../cuba-depopulation-2021-2026.pdf
cp supplement.pdf ../cuba-depopulation-2021-2026-supplement.pdf
```

## Regenerate charts (600 dpi manuscript PNGs; 400 dpi IG)

```bash
cd demographics
export MPLBACKEND=Agg
python3 scripts/charts_publication.py   # ES infographic + EN manuscript figures
python3 scripts/charts_hsds.py          # Model E / HSDS figures (f12, f13)
```

Infographic panels: `infographic/ig_*.png` (6 charts, 400 dpi).  
Manuscript figures: `figures/f*.png` (English labels, 600 dpi for the LaTeX paper).

Model E scripts: `scripts/hsds_*.py` (features → score → deaths → births → population).
Artifacts: `artifacts/model_e_summary.json`, `artifacts/hsds_scores.json`.

## Cite

> Pérez-Riverol, Y. (2026). *Estimating Cuba’s 2021–2026 population decline.* Preprint.
> PDF: `demographics/manuscript/en/cuba-depopulation-2021-2026.pdf`
> (+ supplement). Zenodo DOI forthcoming.

## License

Content: **CC BY 4.0**. Code: repository license (CC0 1.0). ONEI tables: public official data.
