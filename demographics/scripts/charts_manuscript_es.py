#!/usr/bin/env python3
"""
Spanish manuscript figure set.

The Spanish manuscript is a scientific mirror of the English preprint, so it
needs the same figures with Spanish labels. Panels already parameterised by
language in charts_publication are reused; the pair is written to figures/ with
an `_es` suffix so the LaTeX graphicspath is the same for both languages.

f14 (attributable mortality) is produced by charts_attributable.py instead.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from charts_publication import (  # noqa: E402
    _age,
    _aging,
    _pop_series,
    _scissors,
    _triangulation,
    _waterfall,
)
from plot_style import apply_style, save_ms  # noqa: E402

PANELS = [
    (_pop_series, "f1_poblacion_es.png", (8.4, 4.4)),
    (_scissors, "f2_tijera_es.png", (8.4, 4.25)),
    (_waterfall, "f3_cascada_es.png", (8.3, 4.35)),
    (_aging, "f4_envejece_es.png", (8.3, 4.4)),
    (_triangulation, "f7_triangulacion_es.png", (8.5, 4.9)),
    (_age, "f10_edad_es.png", (8.4, 4.25)),
]


def main() -> None:
    apply_style()
    for panel, name, size in PANELS:
        fig, ax = plt.subplots(figsize=size)
        panel(ax, "es")
        fig.tight_layout()
        print("wrote", save_ms(fig, name))


if __name__ == "__main__":
    main()
