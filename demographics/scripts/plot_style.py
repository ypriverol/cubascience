"""Shared seaborn publication style for demographics charts."""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

from constants import FIGURES, INFOGRAPHIC, INFOGRAPHIC_EN

# Crisis-forward palette (print-safe, high contrast)
INK = "#111827"
INK2 = "#4b5563"
MUTED = "#9ca3af"
GRID = "#e5e7eb"
BASE = "#d1d5db"
SURF = "#ffffff"
BLUE = "#2563eb"
RED = "#dc2626"
ORANGE = "#ea580c"
GREEN = "#059669"
VIO = "#7c3aed"
NAVY = "#1e3a5f"
CEIL = "#94a3b8"
SOFT_RED = "#fecaca"
SOFT_BLUE = "#dbeafe"
SOFT_GREEN = "#d1fae5"

DPI = 600  # manuscript / print PNGs
DPI_IG = 400  # social infographic panels (file-size tradeoff)
PALETTE = [BLUE, RED, ORANGE, GREEN, VIO, NAVY, CEIL]


def apply_style() -> None:
    sns.set_theme(
        style="whitegrid",
        context="notebook",
        font="DejaVu Sans",
        palette=PALETTE,
        rc={
            "font.size": 11,
            "axes.titlesize": 14.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 12,
            "axes.labelcolor": INK2,
            "axes.edgecolor": BASE,
            "axes.linewidth": 0.9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "xtick.color": INK2,
            "ytick.color": INK2,
            "grid.color": GRID,
            "grid.linewidth": 0.85,
            "figure.facecolor": SURF,
            "axes.facecolor": SURF,
            "savefig.facecolor": SURF,
            "savefig.dpi": DPI,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.14,
            "legend.frameon": False,
            "lines.linewidth": 2.6,
            "lines.markersize": 7.5,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "text.color": INK,
        },
    )
    # Keep left spine off; bottom subtle
    mpl.rcParams["axes.spines.left"] = False


def style_ax(ax, grid: str = "y") -> None:
    sns.despine(ax=ax, left=True, bottom=False)
    ax.spines["bottom"].set_color(BASE)
    ax.tick_params(length=0)
    ax.grid(False)
    if grid == "y":
        ax.yaxis.grid(True, color=GRID, lw=0.85)
        ax.xaxis.grid(False)
    elif grid == "x":
        ax.xaxis.grid(True, color=GRID, lw=0.85)
        ax.yaxis.grid(False)
    ax.set_axisbelow(True)
    ax.set_facecolor(SURF)


def title_block(ax, title: str, subtitle: str | None = None) -> None:
    ax.set_title(title, loc="left", color=INK, pad=20 if subtitle else 12)
    if subtitle:
        ax.text(
            0,
            1.02,
            subtitle,
            transform=ax.transAxes,
            fontsize=10.5,
            color=INK2,
            va="bottom",
        )


def save_fig(fig, path: Path, *, dpi: int | None = None) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        path,
        dpi=dpi or DPI,
        facecolor=SURF,
        edgecolor="none",
        bbox_inches="tight",
        pad_inches=0.14,
    )
    plt.close(fig)
    return path


def save_ig(fig, name: str) -> Path:
    return save_fig(fig, INFOGRAPHIC / name, dpi=DPI_IG)


def save_ig_en(fig, name: str) -> Path:
    return save_fig(fig, INFOGRAPHIC_EN / name, dpi=DPI_IG)


def save_ms(fig, name: str) -> Path:
    return save_fig(fig, FIGURES / name, dpi=DPI)
