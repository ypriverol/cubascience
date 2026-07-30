"""Shared publication-quality matplotlib style for demographics charts."""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

from constants import FIGURES, INFOGRAPHIC

# Palette — high contrast, print-safe
INK = "#0b1220"
INK2 = "#3a4556"
MUTED = "#8b939c"
GRID = "#e6e9ee"
BASE = "#c5cbd3"
SURF = "#ffffff"
BLUE = "#1a6bb5"
RED = "#c62828"
ORANGE = "#e07020"
GREEN = "#1b8a5a"
VIO = "#6b3fa0"
NAVY = "#12314f"
CEIL = "#9aa3ad"

DPI = 300


def apply_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "text.color": INK,
            "axes.edgecolor": BASE,
            "axes.labelcolor": INK2,
            "axes.linewidth": 1.05,
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.labelsize": 12,
            "xtick.color": INK2,
            "ytick.color": INK2,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "figure.facecolor": SURF,
            "axes.facecolor": SURF,
            "savefig.facecolor": SURF,
            "savefig.dpi": DPI,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.12,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def style_ax(ax, grid: str = "y") -> None:
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASE)
    ax.tick_params(length=0)
    if grid == "y":
        ax.grid(axis="y", color=GRID, lw=0.9, zorder=0)
    elif grid == "x":
        ax.grid(axis="x", color=GRID, lw=0.9, zorder=0)
    ax.set_axisbelow(True)


def title_block(ax, title: str, subtitle: str | None = None) -> None:
    ax.set_title(title, loc="left", color=INK, pad=18 if subtitle else 12)
    if subtitle:
        ax.text(
            0,
            1.015,
            subtitle,
            transform=ax.transAxes,
            fontsize=10.5,
            color=INK2,
            va="bottom",
        )


def save_fig(fig, path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, facecolor=SURF, edgecolor="none")
    plt.close(fig)
    return path


def save_ig(fig, name: str) -> Path:
    """Infographic charts live next to infografia.html."""
    return save_fig(fig, INFOGRAPHIC / name)


def save_ms(fig, name: str) -> Path:
    """Manuscript / notebook figures."""
    return save_fig(fig, FIGURES / name)
