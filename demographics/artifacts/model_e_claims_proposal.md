# Model E claims proposal (do not auto-promote)

Preferred public model remains **D**.

## Comparison (end-2025)

| Model | Label | Loss M | Loss % | Pop M |
|---|---|---:|---:|---:|
| A | A · conservative | 1.8 | 16.4 | 9.16 |
| B | B · crisis-adjusted | 2.19 | 20.4 | 8.57 |
| C | C · worst case | 2.41 | 22.6 | 8.26 |
| D | D · sentinel | 2.21 | 20.5 | 8.59 |
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
