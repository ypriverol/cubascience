# Cuba 2019–2026: depopulation in figures

Quantitative estimate of Cuba’s population loss between 2019 and 2026, combining
**Monte Carlo simulation** on the demographic accounting identity with
**triangulation of independent administrative registers**.

> **Central finding.** Not emigration alone. A dual engine: young people leave
> **and** births collapse while deaths rise. ONEI’s official headcount no longer
> matches who actually lives on the island. Preferred Model D: ≈**8.56 M** at
> end-2025 (≈**−2.3 M**, **−21%** vs 2019).

English interactive companion: [`demographics.ipynb`](demographics.ipynb)  
(GitHub Pages: [`/demographics/`](https://ypriverol.github.io/cubascience/demographics/))

Spanish / English manuscripts: `manuscript/es/`, `manuscript/en/`

Related CubaScience study (bibliometrics): [arXiv:2007.09638](https://arxiv.org/abs/2007.09638)

## Layout

```
demographics/
├── demographics.ipynb   English Jupyter companion (self-hosted)
├── manuscript/es|en/    Bilingual manuscripts
├── infographic/         A2 infographic + charts
├── figures/             Manuscript figures (PNG)
├── scripts/             Monte Carlo models + chart/render scripts
├── data/onei/           Official ONEI tables
├── literature/          sources.zip + inventory
└── requirements.txt
```

## Reproduce

```bash
pip install -r requirements.txt
jupyter notebook demographics.ipynb
cd scripts && python3 model_d.py && python3 charts_final.py
```

## Cite

> Pérez-Riverol, Y. (2026). *Cuba 2019–2026: depopulation in figures.*
> [Preprint]. Zenodo (DOI forthcoming).

## License

Content: **CC BY 4.0**. Code: repository license (CC0 1.0). ONEI tables: public official data.
