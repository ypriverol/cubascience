# HSDS feature dictionary (Model E)

Freeze date: 2026-07-31. Machine-readable twin: `demographics/data/mortality_signals.yaml`.

## Purpose

Build a yearly **Health-System Deterioration Score** \(S_t\) from three buckets:

1. **Ageing** — who is left to die and who can still give birth  
2. **Health decadence** — how badly the system is failing  
3. **Bad reporting** — how much official numbers mislead (including COVID misuse as integrity, not ×30 on deaths)

Later: \(S_t \rightarrow D^*_t, B^*_t \rightarrow P^*\). Preferred public model remains **D** until Task 8.

## ONEI Excel spine (confirmed present)

| File | Role |
|---|---|
| `3.12…estructura…edades…xls` | Age structure |
| `3.3…grupos de edades…xls` | Mean pop by age/sex/zone |
| `3.15…defunciones…quinquenales…xls` | Age–sex death schedule |
| `3.16…menores de un año…xls` | Infant deaths / IMR |
| `3.17…esperanza de vida…xls` | Life expectancy |
| `3.13…movimiento natural…xls` | Registered births/deaths |

## Bucket mix (default)

| Bucket | Mix weight |
|---|---|
| ageing | 0.25 |
| health_decadence | 0.50 |
| bad_reporting | 0.25 |

Within each bucket, feature `default_weight` values sum to 1.0.

## Features

### Ageing

| id | What | Source | Norm | Weight |
|---|---|---|---|---|
| `elderly_share_60plus` | Share 60+ | ONEI 3.12/3.3; claims selectivity | minmax 0.18–0.30 | 0.45 |
| `median_age_proxy` | Median age remaining | claims + age stocks | minmax 38–48 | 0.25 |
| `fertile_women_share_proxy` | Fertile-age women share (**inverted** for score) | ONEI + 77% exit ages 15–59 | minmax 0.18–0.28 then invert | 0.30 |

### Health decadence

| id | What | Source | Norm | Weight |
|---|---|---|---|---|
| `imr_rise` | IMR rise vs 2019 | ONEI 3.16 | minmax 0–1 relative rise | 0.22 |
| `cdr_rise` | CDR rise vs baseline | ONEI / Anuario / claims | minmax 0–0.50 relative | 0.18 |
| `mmr_rise` | Maternal mortality rise | cite-only maternal reports | minmax 0–1 | 0.12 |
| `e0_gap` | Years below independent e0 | ONEI 3.17 + Brønnum-Hansen & Albizu (2023) | minmax 0–8 years | 0.18 |
| `healthcare_collapse_web` | Shortages / blackouts / staffing | public web (Task 2) | already 0–1 | 0.18 |
| `epidemic_pressure_web` | COVID / epidemic pressure | public epi (Task 2) | already 0–1 | 0.12 |

IMR remains a **sentinel** (harder to hide), not a direct estimator of total deaths.

### Bad reporting

| id | What | Source | Norm | Weight |
|---|---|---|---|---|
| `covid_misuse_ratio_norm` | \(\mathrm{log}_{10}\) of (all-cause jump or excess ÷ COVID labels), then minmax | official COVID labels vs 2021 jump / excess bands | log10 ratio then minmax over ~1–50 | 0.40 |
| `onei_migration_seam_flag` | Revision / seam year opacity | `onei_audit.py` identity | 0–1 | 0.35 |
| `stats_opacity_vs_independents` | Official vs independent / destination admin | Albizu (cite-only); CBP LBs | 0–1 | 0.25 |

**Hard rule:** `covid_misuse_ratio_norm` raises \(S_t\). It must **not** multiply registered all-cause deaths by 20–50×.

## Normalization contract (Task 2)

Every row in `hsds_features.csv` must expose `value_norm ∈ [0, 1]`. Continuous series use documented `(lo, hi)` from YAML; web severity codes are expert 0–1 with citations in `artifacts/public_health_signals.md`.

## Double-counting watch (Task 8)

Age structure already enters expected deaths \(\sum_a m_{a,\mathrm{base}} P^*_{a,t}\). The ageing bucket in \(S_t\) mainly informs **crisis uplift** and birth-base stress; the adversarial gate must check that high \(S\) does not double-count ageing already in the death schedule.
