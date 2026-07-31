# Literature sources

Third-party PDFs used during research are **not redistributed** in this repository
(copyright). Obtain them from the original publishers. A local `sources.zip` may
exist on the author’s machine for convenience; it is **gitignored**.

| Document | How to obtain |
|---|---|
| Albizu-Campos — emigration / demographic emptying (2024) | Author / publisher copies |
| Maternal mortality in Cuba (“el color cuenta”) | Author / publisher copies |
| Cuba Capacity Building Project — demographic/systemic crisis | Project site / publisher |
| COMPUMAT 2025 WGIM materials | Conference proceedings |
| Cancer mortality fact sheets | Registro Nacional de Cáncer / MINSAP |
| Nutrition socioeconomic correlates | Journal publisher |

Peer-reviewed:

- Brønnum-Hansen, H. & Albizu-Campos Espiñeira, J. C. (2023). *Journal of Population Research.* doi:10.1007/s12546-023-09296-w

Official ONEI tables: `../data/onei/` (see `../data/SOURCES.md`).

## Model E / HSDS public severity (cite-only; Task 1–2)

These support **health decadence** and **bad reporting** features in
`../data/mortality_signals.yaml`. Do not redistribute third-party PDFs.

| Signal | Typical use in HSDS | Where to look |
|---|---|---|
| Official COVID-attributed deaths vs all-cause 2021 jump | `covid_misuse_ratio_norm` (log-ratio integrity feature, **not** ×N on all deaths) | MINSAP / ONEI releases; WHO COVID dashboard archives |
| Medicine shortages, hospital blackouts, staffing exit | `healthcare_collapse_web` (0–1 coded) | Cuban independent press; PAHO/WHO situation notes |
| Epidemic / dengue / post-COVID burden | `epidemic_pressure_web` (0–1 coded) | MINSAP epi bulletins; PAHO |
| Maternal mortality rise | `mmr_rise` | Albizu maternal mortality report (cite-only; see above) |
| Independent life expectancy | `e0_gap` | Brønnum-Hansen & Albizu-Campos (2023), doi above |
| Destination admin lower bounds (e.g. US CBP) | `stats_opacity_vs_independents` | CBP southwest land border encounter data; host-country stats |

Feature freeze write-up: `../artifacts/hsds_feature_dictionary.md`.
