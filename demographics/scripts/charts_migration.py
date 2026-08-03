#!/usr/bin/env python3
"""
Figure: the migration claim, in three panels.

Panel A  WHO leaves -- age composition of emigrants against remaining residents.
Panel B  WHAT ONEI SAYS -- declared net migration against what other countries
         recorded arriving. In 2021 and 2022 ONEI reports net *positive*
         migration while the US alone registered 54,818 and 313,506 arrivals.
Panel C  HOW MUCH IS DOCUMENTED -- the bridge from a settled floor of 1.05 M to
         the ~2.0 M migration engine. Only the floor is ledger-like.

Panels A and B were previously separate figures; merged because they make one
argument and were read as two.

Palette: BLUE (official) vs RED (external), validated -- worst adjacent pair
protan dE 29.9, normal 38.2, both well clear of the floors.

Reads data/claims.yaml and artifacts/consistency_report.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from charts_publication import _age  # noqa: E402
from constants import ARTIFACTS, get_claims  # noqa: E402
from plot_style import (  # noqa: E402
    BLUE, INK, INK2, MUTED, RED, apply_style, save_ms, style_ax, title_block,
)

TEXT = {
    "en": {
        "ta": "ONEI reports almost no one left in 2021–22",
        "sa": "Net migration ONEI declares, against Cubans other countries recorded arriving.",
        "onei": "ONEI declared net outflow",
        "ext": "Recorded arrivals, US alone",
        "yl_a": "People per year (thousands)",
        "tb": "Only the first step is a ledger",
        "sb": "From documented settled emigrants to the central scenario's migration engine.",
        "yl_b": "Cumulative net emigration (millions)",
        "steps": ["Settled floor\n(US admin +\nnon-US)", "ONEI net\n2022–25",
                  "Albizu-Campos\ntype net", "Central\nscenario"],
        "kinds": ["documented", "official", "independent", "prior"],
        "net_in": "ONEI declares net ARRIVALS in both years: +169 and +991",
    },
    "es": {
        "ta": "La ONEI dice que casi nadie se fue en 2021–22",
        "sa": "Saldo migratorio declarado por la ONEI, frente a los cubanos que otros países registraron llegando.",
        "onei": "Salida neta declarada por la ONEI",
        "ext": "Llegadas registradas, solo EE.UU.",
        "yl_a": "Personas por año (miles)",
        "tb": "Solo el primer paso es un libro mayor",
        "sb": "Del emigrante asentado documentado al motor migratorio del escenario central.",
        "yl_b": "Emigración neta acumulada (millones)",
        "steps": ["Piso asentados\n(admin. EE.UU.\n+ no EE.UU.)", "Neto ONEI\n2022–25",
                  "Neto tipo\nAlbizu-Campos", "Escenario\ncentral"],
        "kinds": ["documentado", "oficial", "independiente", "prior"],
        "net_in": "La ONEI declara LLEGADAS netas en ambos años: +169 y +991",
    },
}


def _panel_a(ax, t: dict) -> None:
    style_ax(ax)
    rep = json.loads((ARTIFACTS / "consistency_report.json").read_text(encoding="utf-8"))
    rows = [r for r in rep["tests"] if r["test"] == "T5_external_contradiction"]
    rows.sort(key=lambda r: r["year"])
    years = [r["year"] for r in rows]
    # Declared net outflow is 0 in years ONEI reported net *inflow*; show the
    # signed value so the +169 / +991 absurdity is visible rather than clipped.
    declared = {2021: -0.169, 2022: -0.991, 2024: 251.221}
    onei = np.array([declared[y] for y in years])
    ext = np.array([r["us_arrivals_only"] / 1e3 for r in rows])

    x = np.arange(len(years))
    w = 0.38
    ax.bar(x - w / 2, onei, w, color=BLUE, label=t["onei"],
           edgecolor="white", linewidth=1.4, zorder=3)
    ax.bar(x + w / 2, ext, w, color=RED, label=t["ext"],
           edgecolor="white", linewidth=1.4, zorder=3)
    ax.axhline(0, color=INK2, lw=1.1, zorder=4)

    # A bar of -169 people is invisible and "-169" reads as a departure count.
    # State what ONEI actually claimed: net ARRIVALS exceeded departures.
    for xi, v in zip(x - w / 2, onei):
        if v >= 1:
            ax.annotate(f"{v:,.0f}k", (xi, v), xytext=(0, 6),
                        textcoords="offset points", ha="center", fontsize=10,
                        fontweight="bold", color=BLUE)
    # One consolidated callout below the axis. Per-bar labels for the near-zero
    # years collided with each other and with the neighbouring red bars; the
    # missing blue bar already makes the visual point.
    ax.annotate(t["net_in"], (0.5, 0), xytext=(0, -12), textcoords="offset points",
                ha="center", va="top", fontsize=9.5, fontweight="bold", color=BLUE)
    for xi, v in zip(x + w / 2, ext):
        ax.annotate(f"{v:,.0f}k", (xi, v), xytext=(0, 6), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold", color=RED)
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years])
    ax.set_ylabel(t["yl_a"])
    ax.set_ylim(-52, 440)
    ax.legend(fontsize=9.5, loc="upper right")
    title_block(ax, t["ta"], t["sa"])


def _panel_b(ax, t: dict) -> None:
    style_ax(ax)
    c = get_claims()["migration_bridge"]
    vals = [c["settled_floor_m"], c["onei_R_m"], c["albizu_net_m"],
            c["model_d_median_Rm_m"]]
    # Only the first bar is documented; the rest are progressively softer.
    colors = [RED, BLUE, "#94a3b8", "#cbd5e1"]
    x = np.arange(len(vals))
    ax.bar(x, vals, 0.62, color=colors, edgecolor="white", linewidth=1.4, zorder=3)
    for xi, v in zip(x, vals):
        ax.annotate(f"{v:.2f} M", (xi, v), xytext=(0, 7), textcoords="offset points",
                    ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_xticks(x)
    # The kind ("documented" / "prior") belongs with the label, not inside the
    # bar, where it overflowed the bar width.
    ax.set_xticklabels([f"{s}\n[{k}]" for s, k in zip(t["steps"], t["kinds"])],
                       fontsize=8.8)
    ax.set_ylabel(t["yl_b"])
    ax.set_ylim(0, 2.45)
    title_block(ax, t["tb"], t["sb"])


def build(lang: str) -> Path:
    apply_style()
    t = TEXT[lang]
    fig, axes = plt.subplots(1, 3, figsize=(19.2, 5.1))
    _age(axes[0], lang)
    _panel_a(axes[1], t)
    _panel_b(axes[2], t)
    fig.tight_layout(w_pad=3.4)
    return save_ms(fig, "f15_migracion.png" if lang == "en" else "f15_migracion_es.png")


def main() -> None:
    for lang in ("en", "es"):
        print("wrote", build(lang))


if __name__ == "__main__":
    main()
