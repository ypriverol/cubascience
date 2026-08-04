# Model E claims proposal (do not auto-promote)

Preferred public model remains **central**.

## Comparison (end-2025)

| Model | Label | Loss M | Loss % | Pop M |
|---|---|---:|---:|---:|

| E | vital reconstruction (HSDS) | 2.13 | 19.2 | 8.96 |

## Proposed YAML block (append only)

```yaml
model_e:
  pop_end_2025_m: 8.96
  loss_2021_2025_m: 2.13
  loss_pct_corrected_base: 19.2
  loss_90_m:
  - 1.9
  - 2.44
  pop_end_2026_m: 8.66
  migration_share_of_loss_pct: 87.8
  natural_decrease_share_of_loss_pct: 12.2
  definition: Vital reconstruction via HSDS; provisional beside preferred Model D.
  promote: false

```

## Notes

- Migration share ≈ 88%; natural-decrease share ≈ 12%.
- Sum B* median 314563 vs reg 325233.
- Sum D* median 575270 vs reg 502149.
- Task 8 adversarial gate decides promote vs keep-beside.
