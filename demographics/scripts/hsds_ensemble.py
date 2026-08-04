# -*- coding: utf-8 -*-
"""Compare Model E to A–D and propose a claims.yaml Model E block (do not overwrite D)."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from constants import ARTIFACTS, DATA, get_claims
from hsds_population import run_model_e

OUT_MD = ARTIFACTS / "model_e_claims_proposal.md"


def main() -> None:
    e = run_model_e(n=50_000, seed=2027)
    claims = get_claims()
    rows = []
    for m in claims.get("models_summary", []):
        rows.append(
            f"| {m['id']} | {m.get('label','')} | {m.get('decline_m')} | "
            f"{m.get('decline_pct')} | {m.get('pop_end_2025_m')} |"
        )
    e_loss_m = e["decline_2021_2025"]["median"] / 1e6
    e_pct = e["pct_corrected_base"]["median"]
    e_pop = e["pop_2025"]["median"] / 1e6
    e_pop26 = e["pop_2026"]["median"] / 1e6

    proposal = {
        "model_e": {
            "pop_end_2025_m": round(e_pop, 2),
            "loss_2021_2025_m": round(e_loss_m, 2),
            "loss_pct_corrected_base": round(e_pct, 1),
            "loss_90_m": [
                round(e["decline_2021_2025"]["p05"] / 1e6, 2),
                round(e["decline_2021_2025"]["p95"] / 1e6, 2),
            ],
            "pop_end_2026_m": round(e_pop26, 2),
            "migration_share_of_loss_pct": round(e["mig_share_median"], 1),
            "natural_decrease_share_of_loss_pct": round(
                e["natural_decrease_share_median"], 1
            ),
            "definition": "Vital reconstruction via HSDS; provisional beside preferred Model D.",
            "promote": False,
        }
    }

    md = f"""# Model E claims proposal (do not auto-promote)

Preferred public model remains **{claims['meta']['preferred_scenario']}**.

## Comparison (end-2025)

| Model | Label | Loss M | Loss % | Pop M |
|---|---|---:|---:|---:|
{chr(10).join(rows)}
| E | vital reconstruction (HSDS) | {e_loss_m:.2f} | {e_pct:.1f} | {e_pop:.2f} |

## Proposed YAML block (append only)

```yaml
{yaml.safe_dump(proposal, sort_keys=False)}
```

## Notes

- Migration share ≈ {e['mig_share_median']:.0f}%; natural-decrease share ≈ {e['natural_decrease_share_median']:.0f}%.
- Sum B* median {e['sum_B_star_median']:.0f} vs reg {e['anchors']['B_reg_2022_2025']}.
- Sum D* median {e['sum_D_star_median']:.0f} vs reg {e['anchors']['D_reg_2022_2025']}.
- Task 8 adversarial gate decides promote vs keep-beside.
"""
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")
    # Keep machine summary from population run
    print(md)
    print(f"wrote {OUT_MD}")
    print(f"summary {ARTIFACTS / 'model_e_summary.json'}")


if __name__ == "__main__":
    main()
