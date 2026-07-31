# -*- coding: utf-8 -*-
"""Publication charts for HSDS score and Model E vitals / population."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from constants import ARTIFACTS, DATA, FIGURES  # noqa: E402
from plot_style import BLUE, INK, INK2, RED, apply_style, save_ms  # noqa: E402


def _scores() -> pd.DataFrame:
    payload = json.loads((ARTIFACTS / "hsds_scores.json").read_text())
    return pd.DataFrame(payload["years"])


def _deaths() -> pd.DataFrame:
    payload = json.loads((ARTIFACTS / "model_e_deaths.json").read_text())
    return pd.DataFrame(payload["years"])


def _births() -> pd.DataFrame:
    payload = json.loads((ARTIFACTS / "model_e_births.json").read_text())
    return pd.DataFrame(payload["years"])


def chart_vitals() -> Path:
    apply_style()
    scores = _scores()
    deaths = _deaths()
    births = _births()

    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.8))

    ax = axes[0]
    ax.fill_between(scores["year"], scores["S_p05"], scores["S_p95"], color=BLUE, alpha=0.2)
    ax.plot(scores["year"], scores["S_median"], color=BLUE, lw=2.2, marker="o")
    ax.set_title("Health-system deterioration $S_t$")
    ax.set_ylabel("Score (0–1)")
    ax.set_ylim(0, 1)
    ax.set_xlabel("Year")

    ax = axes[1]
    ax.plot(deaths["year"], deaths["D_reg"], color=INK2, lw=1.8, marker="s", label="Registered")
    ax.plot(
        deaths["year"],
        [d["median"] for d in deaths["D_star"]],
        color=RED,
        lw=2.2,
        marker="o",
        label=r"$D^*$ (Model E)",
    )
    ax.fill_between(
        deaths["year"],
        [d["p05"] for d in deaths["D_star"]],
        [d["p95"] for d in deaths["D_star"]],
        color=RED,
        alpha=0.15,
    )
    ax.set_title("Deaths: reconstructed vs registered")
    ax.set_ylabel("Deaths")
    ax.legend(frameon=False, fontsize=8)
    ax.set_xlabel("Year")

    ax = axes[2]
    ax.plot(births["year"], births["B_reg"], color=INK2, lw=1.8, marker="s", label="Registered")
    ax.plot(
        births["year"],
        [b["median"] for b in births["B_star"]],
        color=BLUE,
        lw=2.2,
        marker="o",
        label=r"$B^*$ (Model E)",
    )
    ax.fill_between(
        births["year"],
        [b["p05"] for b in births["B_star"]],
        [b["p95"] for b in births["B_star"]],
        color=BLUE,
        alpha=0.15,
    )
    ax.set_title("Births: reconstructed vs registered")
    ax.set_ylabel("Births")
    ax.legend(frameon=False, fontsize=8)
    ax.set_xlabel("Year")

    fig.suptitle("Model E vital reconstruction (HSDS)", color=INK, fontsize=12, y=1.02)
    fig.tight_layout()
    return save_ms(fig, "f12_hsds_vitals.png")


def chart_population() -> Path:
    apply_style()
    e = json.loads((ARTIFACTS / "model_e_summary.json").read_text())
    claims = json.loads((ARTIFACTS / "claims.json").read_text()) if (ARTIFACTS / "claims.json").exists() else None
    if claims is None:
        from constants import get_claims

        claims = get_claims()

    labels = []
    pops = []
    for m in claims["models_summary"]:
        labels.append(m["id"])
        pops.append(m["pop_end_2025_m"])
    labels.append("E")
    pops.append(e["pop_2025"]["median"] / 1e6)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    colors = [INK2] * (len(labels) - 1) + [RED]
    # highlight D
    for i, lab in enumerate(labels):
        if lab == "D":
            colors[i] = BLUE
    ax.bar(labels, pops, color=colors, edgecolor="white")
    ax.axhline(9.43, color=INK2, ls="--", lw=1, label="ONEI end-2025 (9.43M)")
    ax.set_ylabel("Population end-2025 (millions)")
    ax.set_title("Model E beside A–D (preferred remains D)")
    ax.set_ylim(7.5, 10.0)
    ax.legend(frameon=False, fontsize=8)
    for i, v in enumerate(pops):
        ax.text(i, v + 0.05, f"{v:.2f}", ha="center", fontsize=8, color=INK)
    fig.tight_layout()
    return save_ms(fig, "f13_model_e_population.png")


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    p1 = chart_vitals()
    p2 = chart_population()
    print("wrote", p1)
    print("wrote", p2)


if __name__ == "__main__":
    main()
