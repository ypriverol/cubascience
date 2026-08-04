#!/usr/bin/env python3
"""
Figure: why deaths rose while the population fell.

Panel A  Change in annual deaths versus 2019, decomposed into population size
         (fewer residents), ageing (older residents), and rate deterioration
         (the health system itself).  Diverging stack around zero; the dot is
         the net observed change.
Panel B  Annual deaths attributable to health-system deterioration, with the
         90% band.  2026 is a scenario continuation, drawn dashed.

Palette: BLUE / AMBER / RED, validated for CVD separation (worst adjacent
deutan dE 10.0, normal 19.2).  Amber sits below 3:1 against the surface, so
every stacked segment carries a direct label as the required relief.

Reads artifacts/attributable_mortality.json (run attributable_mortality.py first).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import ARTIFACTS  # noqa: E402
from plot_style import (  # noqa: E402
    BLUE,
    INK,
    INK2,
    MUTED,
    RED,
    apply_style,
    save_ms,
    style_ax,
    title_block,
)

AMBER = "#ca8a04"
SRC = ARTIFACTS / "attributable_mortality.json"

TEXT = {
    "en": {
        "title_a": "Deaths rose while the population fell",
        "sub_a": "Change in annual deaths vs 2019, by driver. Dot = net observed change.",
        "title_b": "Excess deaths vs the 2019 age-specific schedule",
        "sub_b": "Median and 90% band. 2026 is a scenario continuation, not an observation.",
        "size": "Fewer residents",
        "ageing": "Older residents",
        "rate": "Rate deterioration",
        "ylab_a": "Deaths vs 2019 (thousands)",
        "ylab_b": "Attributable deaths per year (thousands)",
        "covid": "COVID-19 wave",
        "scen": "scenario",
        "net": "net change",
    },
    "es": {
        "title_a": "Las muertes suben mientras la población cae",
        "sub_a": "Cambio en defunciones anuales vs 2019, por causa. Punto = cambio neto observado.",
        "title_b": "Exceso de defunciones vs la tabla de tasas por edad de 2019",
        "sub_b": "Mediana y banda del 90%. 2026 es continuación de escenario, no una observación.",
        "size": "Menos residentes",
        "ageing": "Residentes más viejos",
        "rate": "Deterioro de tasas",
        "ylab_a": "Defunciones vs 2019 (miles)",
        "ylab_b": "Defunciones atribuibles por año (miles)",
        "covid": "ola de COVID-19",
        "scen": "escenario",
        "net": "cambio neto",
    },
}


def _load() -> dict:
    if not SRC.exists():
        raise SystemExit(
            f"missing {SRC} — run `python3 attributable_mortality.py` first"
        )
    return json.loads(SRC.read_text(encoding="utf-8"))


def _panel_a(ax, data: dict, t: dict) -> None:
    style_ax(ax)
    rows = data["by_year"]
    years = [r["year"] for r in rows]
    x = np.arange(len(years))
    size = np.array([r["population_size_effect_vs_2019"]["median"] for r in rows]) / 1e3
    ageing = np.array([r["ageing_effect_vs_2019"]["median"] for r in rows]) / 1e3
    rate = np.array([r["excess_vs_2019_schedule"]["median"] for r in rows]) / 1e3
    net = np.array([r["total_deaths_incl_unregistered"]["median"] for r in rows]) / 1e3
    net = net - data["base_2019"]["total_deaths"] / 1e3

    # Positive contributions stack upward from zero; the negative one hangs below.
    # 2px surface gap between segments (plot_style surface is white).
    ax.bar(x, ageing, width=0.66, color=AMBER, label=t["ageing"],
           edgecolor="white", linewidth=1.6, zorder=3)
    ax.bar(x, rate, width=0.66, bottom=ageing, color=RED, label=t["rate"],
           edgecolor="white", linewidth=1.6, zorder=3)
    ax.bar(x, size, width=0.66, color=BLUE, label=t["size"],
           edgecolor="white", linewidth=1.6, zorder=3)

    ax.axhline(0, color=INK2, lw=1.1, zorder=4)
    # Offset left of centre: the segment value labels are centred, and a dot on
    # top of them is unreadable.
    ax.plot(x - 0.23, net, "o", color=INK, ms=7.5, zorder=6,
            markeredgecolor="white", markeredgewidth=1.6)

    # Direct labels on every segment: required relief for the amber contrast WARN.
    for i in range(len(years)):
        if ageing[i] > 3:
            ax.text(x[i], ageing[i] / 2, f"{ageing[i]:.0f}", ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white", zorder=5)
        if rate[i] > 3:
            ax.text(x[i], ageing[i] + rate[i] / 2, f"{rate[i]:.0f}", ha="center",
                    va="center", fontsize=9, fontweight="bold", color="white", zorder=5)
        # `-0` reads as a typo; show a plain zero when the effect rounds away.
        lab = f"{size[i]:.0f}" if abs(size[i]) >= 0.5 else "0"
        ax.text(x[i], size[i] - 1.6, lab, ha="center", va="top",
                fontsize=9, fontweight="bold", color=BLUE, zorder=5)

    i21 = years.index(2021)
    ax.annotate(t["covid"], (x[i21], ageing[i21] + rate[i21]), xytext=(0, 10),
                textcoords="offset points", ha="center", fontsize=9.5,
                color=RED, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) if y != 2026 else "2026*" for y in years])
    ax.set_ylabel(t["ylab_a"])
    ax.set_ylim(-31, 90)
    ax.set_xlim(-0.7, len(years) - 0.3)
    # The net-change dot goes in the legend rather than an in-plot callout that
    # would land on top of the 2021 bar.
    handles, labels = ax.get_legend_handles_labels()
    handles.append(Line2D([], [], marker="o", color="none", markerfacecolor=INK,
                          markeredgecolor="white", markeredgewidth=1.6, ms=7.5))
    labels.append(t["net"])
    ax.legend(handles, labels, fontsize=9.5, loc="upper right", ncol=1, title=None)
    title_block(ax, t["title_a"], t["sub_a"])


def _panel_b(ax, data: dict, t: dict) -> None:
    style_ax(ax)
    rows = data["by_year"]
    years = np.array([r["year"] for r in rows])
    med = np.array([r["excess_vs_2019_schedule"]["median"] for r in rows]) / 1e3
    lo = np.array([r["excess_vs_2019_schedule"]["p05"] for r in rows]) / 1e3
    hi = np.array([r["excess_vs_2019_schedule"]["p95"] for r in rows]) / 1e3

    ax.fill_between(years, lo, hi, color=RED, alpha=0.14, lw=0, zorder=2)
    obs = years <= 2025
    ax.plot(years[obs], med[obs], color=RED, lw=2.6, marker="o", ms=8,
            markeredgecolor="white", markeredgewidth=1.6, zorder=4)
    ax.plot(years[years >= 2025], med[years >= 2025], color=RED, lw=2.4,
            ls=(0, (1.8, 1.5)), zorder=4)
    ax.plot([2026], [med[-1]], "o", color=RED, ms=8, mfc="white",
            markeredgewidth=2.2, zorder=5)
    ax.axhline(0, color=INK2, lw=1.0, zorder=1)

    for yr, v in ((2021, med[years == 2021][0]), (2025, med[years == 2025][0])):
        ax.annotate(f"{v:.0f}k", (yr, v), xytext=(0, 11), textcoords="offset points",
                    ha="center", fontsize=10.5, fontweight="bold", color=RED)
    # Label the dashed segment under its midpoint: beside the 2026 point it
    # collides with both the line and the 26k callout.
    ax.annotate(t["scen"], (2025.5, 0.5 * (med[-2] + med[-1])), xytext=(0, -24),
                textcoords="offset points", ha="center", fontsize=9.5,
                color=MUTED, style="italic")

    ax.set_xticks(years)
    ax.set_xticklabels([str(y) if y != 2026 else "2026*" for y in years])
    ax.set_ylabel(t["ylab_b"])
    ax.set_ylim(-8, 72)
    ax.set_xlim(2019.6, 2026.5)
    title_block(ax, t["title_b"], t["sub_b"])


def build(lang: str) -> Path:
    apply_style()
    data = _load()
    t = TEXT[lang]
    fig, axes = plt.subplots(1, 2, figsize=(13.6, 5.0))
    _panel_a(axes[0], data, t)
    _panel_b(axes[1], data, t)
    fig.tight_layout(w_pad=3.0)
    name = "f14_atribuible.png" if lang == "en" else "f14_atribuible_es.png"
    return save_ms(fig, name)


def main() -> None:
    for lang in ("en", "es"):
        print("wrote", build(lang))


if __name__ == "__main__":
    main()
