# Estimating Cuba’s 2021–2026 population collapse

Quantitative estimate of Cuba’s population loss between **end-2021 and end-2026**.
**One in four Cubans gone in five years** (vs the official 2021 base by end-2026).

> **Central finding (Model D).** ≈**8.59 M** living population at end-2025
> (≈**−2.21 M**, **−20.5%** on the corrected base). Emigration ≈**91%** of the loss.
> Age-adjusted excess deaths 2024–2025 ≈**40–60k**. By end-2026, loss approaches
> ~**1 in 4** vs the **official 2021** base (a different definition from −20.5%).
>
> **Model E (provisional).** Vital reconstruction from ageing + health decadence +
> bad reporting → true births/deaths → population ≈**8.96 M** end-2025
> (−2.13 M, −19.2%). Preferred claims remain Model D until promoted.

The Monte Carlo window starts at **official end-2021** (11,113,215), not 2019.
Pre-crisis 2019 rates still appear only as methodological baselines (age schedule, IMR rise).

## Three products

| Product | Lang | Audience | Path |
|---|---|---|---|
| Scientific preprint | EN | Researchers | [`manuscript/en/latex/`](manuscript/en/latex/) → [`cuba-depopulation-2021-2026.pdf`](manuscript/en/cuba-depopulation-2021-2026.pdf) |
| Public essay | ES | General / diaspora | [`manuscript/es/cuba-despoblacion-2021-2026.md`](manuscript/es/cuba-despoblacion-2021-2026.md) |
| Social infographic | ES | Twitter / IG | [`infographic/`](infographic/) + `social_1x1.png`, `social_4x5.png` |
| Notebook companion | EN | Open science | [`demographics.ipynb`](demographics.ipynb) · [Pages](https://ypriverol.github.io/cubascience/demographics/) |

**Numbers source of truth:** [`data/claims.yaml`](data/claims.yaml)

Related bibliometrics study: [arXiv:2007.09638](https://arxiv.org/abs/2007.09638)

## Build the English PDF

```bash
cd manuscript/en/latex
latexmk -pdf main.tex
cp main.pdf ../cuba-depopulation-2021-2026.pdf
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

> Pérez-Riverol, Y. (2026). *Estimating Cuba’s 2021–2026 population collapse.* Working paper.
> PDF: `demographics/manuscript/en/cuba-depopulation-2021-2026.pdf`. Zenodo DOI forthcoming.

## License

Content: **CC BY 4.0**. Code: repository license (CC0 1.0). ONEI tables: public official data.
