# Cuba 2019–2026: depopulation in figures

Quantitative estimate of Cuba’s population loss between 2019 and 2026, combining
**Monte Carlo simulation** on the demographic accounting identity with
**triangulation of independent administrative registers**.

> **Central finding (Model D).** ≈**8.56 M** living population at end-2025
> (≈**−2.3 M**, **−21%** on the corrected base). Emigration ≈**86%** of the loss.
> Age-adjusted excess deaths 2024–2025 ≈**40–60k**. By end-2026, loss approaches
> ~**1 in 4** vs the **official 2019** base (a different definition from −21%).

## Three products

| Product | Lang | Audience | Path |
|---|---|---|---|
| Scientific preprint | EN | Researchers | [`manuscript/en/latex/`](manuscript/en/latex/) → [`cuba-depopulation-2019-2026.pdf`](manuscript/en/cuba-depopulation-2019-2026.pdf) |
| Public essay | ES | General / diaspora | [`manuscript/es/cuba-despoblacion-2019-2026.md`](manuscript/es/cuba-despoblacion-2019-2026.md) |
| Social infographic | ES | Twitter / IG | [`infographic/`](infographic/) + `social_1x1.png`, `social_4x5.png` |
| Notebook companion | EN | Open science | [`demographics.ipynb`](demographics.ipynb) · [Pages](https://ypriverol.github.io/cubascience/demographics/) |

**Numbers source of truth:** [`data/claims.yaml`](data/claims.yaml)

Related bibliometrics study: [arXiv:2007.09638](https://arxiv.org/abs/2007.09638)

## Build the English PDF

```bash
cd manuscript/en/latex
latexmk -pdf main.tex
cp main.pdf ../cuba-depopulation-2019-2026.pdf
```

## Regenerate charts (300 dpi)

```bash
cd demographics
export MPLBACKEND=Agg
python3 scripts/charts_publication.py   # ES infographic + EN manuscript figures
```

Infographic panels: `infographic/ig_*.png` (6 charts).  
Manuscript figures: `figures/f*.png` (English labels for the LaTeX paper).

## Cite

> Pérez-Riverol, Y. (2026). *Cuba’s depopulation, 2019–2026.* Working paper.
> PDF: `demographics/manuscript/en/cuba-depopulation-2019-2026.pdf`. Zenodo DOI forthcoming.

## License

Content: **CC BY 4.0**. Code: repository license (CC0 1.0). ONEI tables: public official data.
