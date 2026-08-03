#!/usr/bin/env python3
"""Regenerate excess-mortality figures (delegates to charts_publication)."""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from charts_publication import _excess, main as regen_all  # noqa: E402
from plot_style import apply_style, save_ms  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402


def main() -> None:
    apply_style()
    for lang, name in (("en", "f9_exceso.png"), ("es", "f9_exceso_es.png")):
        fig, ax = plt.subplots(figsize=(8.4, 4.25))
        _excess(ax, lang)
        fig.tight_layout()
        save_ms(fig, name)
        print(f"wrote figures/{name} ({lang})")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        regen_all()
    else:
        main()
