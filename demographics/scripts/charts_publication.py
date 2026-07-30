#!/usr/bin/env python3
"""Regenerate publication charts: Spanish infographic + English manuscript (300 dpi)."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import get_claims  # noqa: E402
from plot_style import (  # noqa: E402
    BLUE,
    CEIL,
    GREEN,
    INK,
    INK2,
    MUTED,
    ORANGE,
    RED,
    VIO,
    apply_style,
    save_ig,
    save_ms,
    style_ax,
    title_block,
)

apply_style()
C = get_claims()
MD = C["model_d"]
TRI = C["triangulation"]["sources"]
SEL = C["selectivity"]


def _pop_series(ax, lang: str) -> None:
    style_ax(ax)
    oy = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    ov = [11.19, 11.18, 11.11, 11.09, 10.06, 9.75, 9.43]
    ey = [2019, 2025, 2026, 2030]
    ev = [11.19, MD["pop_end_2025_m"], MD["pop_end_2026_m"], 7.0]
    ax.axvspan(2025, 2030.6, color="#eef1f4", lw=0, zorder=0)
    ax.plot(oy, ov, color=BLUE, lw=2.8, marker="o", ms=6.5, zorder=4)
    ax.plot(ey[:3], ev[:3], color=RED, lw=3.0, marker="o", ms=7, zorder=5)
    ax.plot(ey[2:], ev[2:], color=RED, lw=3.0, ls=(0, (1.6, 1.4)), marker="o", ms=7, zorder=5)
    ax.annotate("11.2 M", (2019, 11.19), xytext=(0, 8), textcoords="offset points", fontsize=11, fontweight="bold", ha="center")
    ax.annotate(
        f"{MD['pop_end_2025_m']:.1f} M",
        (2025, MD["pop_end_2025_m"]),
        xytext=(-5, -15),
        textcoords="offset points",
        color=RED,
        fontsize=11,
        fontweight="bold",
        ha="right",
    )
    ax.annotate("7 M (2030)", (2030, 7.0), xytext=(8, 0), textcoords="offset points", color=RED, fontsize=11, fontweight="bold", va="center")
    ax.set_xlim(2018.5, 2031.2)
    ax.set_ylim(6.2, 11.9)
    ax.set_xticks(range(2019, 2031, 2))
    if lang == "es":
        ax.annotate("cifra oficial", (2023.7, 9.95), color=BLUE, fontsize=12, fontweight="bold", ha="right")
        ax.annotate("estimación real", (2022.4, 8.95), color=RED, fontsize=12, fontweight="bold", ha="center")
        ax.text(2027.7, 10.45, "proyección", color=MUTED, fontsize=11, style="italic", ha="center")
        ax.set_ylabel("Millones de habitantes")
        title_block(
            ax,
            "Cuba se vacía: de 11,2 M (2019) a ~8,3 M (2026)",
            "Modelo D preferido. La cifra oficial va detrás de la población residente real.",
        )
    else:
        ax.annotate("official series", (2023.7, 9.95), color=BLUE, fontsize=12, fontweight="bold", ha="right")
        ax.annotate("Model D estimate", (2022.4, 8.95), color=RED, fontsize=12, fontweight="bold", ha="center")
        ax.text(2027.7, 10.45, "projection", color=MUTED, fontsize=11, style="italic", ha="center")
        ax.set_ylabel("Population (millions)")
        title_block(
            ax,
            "Living population vs official headcount, 2019–2030",
            "Preferred Model D: ~8.56 M end-2025; ~8.27 M end-2026 (illustrative path toward ~7 M by 2030).",
        )


def _scissors(ax, lang: str) -> None:
    style_ax(ax)
    yy = list(range(2017, 2026))
    b = np.array([114971, 116333, 109716, 105038, 99096, 95403, 90392, 71374, 68064]) / 1000
    d = np.array([106941, 106201, 109080, 112439, 167645, 120098, 117739, 128098, 136214]) / 1000
    ax.plot(yy, b, color=BLUE, lw=2.8, marker="o", ms=6)
    ax.plot(yy, d, color=RED, lw=2.8, marker="o", ms=6)
    ax.fill_between(yy, b, d, where=(d > b), color=RED, alpha=0.10, interpolate=True)
    ax.annotate("68k", (2025, 68.064), xytext=(-2, -4), textcoords="offset points", color=BLUE, fontsize=11, fontweight="bold", ha="right", va="top")
    ax.annotate("136k", (2025, 136.214), xytext=(-2, 4), textcoords="offset points", color=RED, fontsize=11, fontweight="bold", ha="right", va="bottom")
    ax.set_xlim(2016.5, 2025.8)
    ax.set_ylim(50, 185)
    ax.set_xticks(range(2017, 2026, 2))
    if lang == "es":
        ax.annotate("NACIMIENTOS", (2017.1, 118), color=BLUE, fontsize=11.5, fontweight="bold")
        ax.annotate("DEFUNCIONES", (2017.1, 99), color=RED, fontsize=11.5, fontweight="bold")
        ax.set_ylabel("Miles por año")
        title_block(ax, "Mueren casi el doble de los que nacen", "Aunque nadie emigrara, el país ya se encogería.")
    else:
        ax.annotate("BIRTHS", (2017.1, 118), color=BLUE, fontsize=11.5, fontweight="bold")
        ax.annotate("DEATHS", (2017.1, 99), color=RED, fontsize=11.5, fontweight="bold")
        ax.set_ylabel("Thousands per year")
        title_block(ax, "Deaths already roughly double births", "Natural decrease alone removes ~68k people in 2025.")


def _excess(ax, lang: str) -> None:
    style_ax(ax)
    x = np.arange(2)
    w = 0.34
    # Age-context bars used in IG; labels clarify vs 40–60k Kitagawa primary claim
    exp = [112.5, 113.8]
    reg = [128.1, 136.2]
    ax.bar(x - w / 2, exp, w, color="#7fb0e8", label="Expected (2019 rates, aged pop.)" if lang == "en" else "Esperadas (tasas 2019, población envejecida)")
    ax.bar(x + w / 2, reg, w, color=RED, label="Registered" if lang == "en" else "Registradas")
    for xi, v in zip(x - w / 2, exp):
        ax.annotate(f"{v:.0f}", (xi, v), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=BLUE)
    for xi, v in zip(x + w / 2, reg):
        ax.annotate(f"{v:.0f}", (xi, v), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=RED)
    for i, (e, r) in enumerate(zip(exp, reg)):
        ax.annotate(f"+{r - e:.0f}k", (x[i] + w / 2, r), xytext=(22, -2), textcoords="offset points", ha="left", fontsize=10.5, fontweight="bold", color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(["2024", "2025"])
    ax.set_ylim(0, 160)
    ax.set_yticks([0, 40, 80, 120])
    ax.legend(fontsize=9.5, loc="upper left")
    if lang == "es":
        ax.set_ylabel("Defunciones (miles)")
        title_block(
            ax,
            "Exceso de mortalidad 2024–2025 (contexto registrado)",
            "La cifra primaria del estudio es 40–60 mil muertes en exceso ajustadas por edad.",
        )
    else:
        ax.set_ylabel("Deaths (thousands)")
        title_block(
            ax,
            "Registered deaths vs aged 2019-schedule expectation",
            "Primary scientific claim remains age-adjusted excess ≈40–60k in 2024–2025.",
        )


def _age(ax, lang: str) -> None:
    style_ax(ax)
    if lang == "es":
        bands = ["Niños\n(0–14)", "Edad laboral\ny fértil (15–59)", "Mayores\n(60+)"]
        lab_e, lab_r = "Se van", "Se quedan"
        ylab = "% del grupo"
        title_block(ax, "Quién se va y quién se queda", "El 77% de quienes emigran tienen 15–59 años.")
    else:
        bands = ["Children\n(0–14)", "Working / fertile\nages (15–59)", "Older adults\n(60+)"]
        lab_e, lab_r = "Emigrants", "Remaining"
        ylab = "Share of group (%)"
        title_block(ax, "Who leaves and who stays", "77% of emigrants are aged 15–59.")
    emig = [15, SEL["emigrants_age_15_59_pct"], 8]
    resid = [16, 57, int(round(SEL["pct_age_60_plus_remaining"]))]
    x = np.arange(3)
    w = 0.36
    ax.bar(x - w / 2, emig, w, color=ORANGE, label=lab_e)
    ax.bar(x + w / 2, resid, w, color=BLUE, label=lab_r)
    for xi, v in zip(x - w / 2, emig):
        ax.annotate(f"{v:.0f}%", (xi, v), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=ORANGE)
    for xi, v in zip(x + w / 2, resid):
        ax.annotate(f"{v:.0f}%", (xi, v), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=BLUE)
    ax.set_xticks(x)
    ax.set_xticklabels(bands, fontsize=10.5)
    ax.set_ylim(0, 92)
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_ylabel(ylab)
    ax.legend(fontsize=11, loc="upper right")


def _triangulation(ax, lang: str) -> None:
    style_ax(ax, grid="x")
    rows = [(r["source"], r["estimate"], r["role"]) for r in TRI]
    colors = []
    for _, _, role in rows:
        colors.append({"ceiling": CEIL, "official": BLUE, "occupancy": GREEN, "independent": ORANGE, "preferred": RED}.get(role, INK2))
    ax.axvspan(
        C["triangulation"]["band_low_m"],
        C["triangulation"]["band_high_m"],
        color=GREEN,
        alpha=0.12,
        lw=0,
    )
    y = np.arange(len(rows))[::-1]
    for i, ((lab, val, _), col) in zip(y, zip(rows, colors)):
        mk = "D" if "Model D" in lab or "Modelo D" in lab or "This study" in lab or "Este estudio" in lab else "o"
        ax.plot(val, i, mk, color=col, ms=14 if mk == "D" else 11, zorder=4, markeredgecolor="white", markeredgewidth=1.2)
        ax.annotate(f"{val:.2f}", (val, i), xytext=(10, 0), textcoords="offset points", va="center", fontsize=10.5, fontweight="bold", color=col if col != CEIL else INK2)
    labels = []
    for lab, _, _ in rows:
        if lang == "en":
            labels.append(lab)
        else:
            # Spanish display labels for IG
            mapping = {
                "UN (stale migration)": "ONU (no actualiza migración)",
                "MINSAP denominator": "Denominador del MINSAP",
                "Electoral roll (level)": "Padrón electoral (nivel)",
                "ONEI official": "ONEI — oficial",
                "Housing × occupancy": "Viviendas × ocupación",
                "Albizu-Campos (2023)": "Albizu-Campos (2023)",
                "This study (Model D)": "Este estudio (Modelo D)",
                "Albizu-Campos (2024)": "Albizu-Campos (2024)",
            }
            labels.append(mapping.get(lab, lab))
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10.5)
    ax.set_xlim(7.35, 11.55)
    if lang == "es":
        ax.set_xlabel("Población estimada (millones)")
        ax.text(8.45, -1.15, "zona más probable 8,0–8,9 M", color=GREEN, fontsize=10.5, fontweight="bold", ha="center")
        title_block(ax, "Ocho fuentes independientes", "Los registros que no depuran emigrados actúan como techos.")
    else:
        ax.set_xlabel("Estimated population (millions)")
        ax.text(8.45, -1.15, "most probable band 8.0–8.9 M", color=GREEN, fontsize=10.5, fontweight="bold", ha="center")
        title_block(ax, "Triangulation across eight independent sources", "Registers that do not purge emigrants act as ceilings.")
    ax.set_ylim(-1.6, len(rows) - 0.35)


def _provinces(ax, lang: str) -> None:
    style_ax(ax, grid="x")
    rates = [
        ("La Habana", 32.8),
        ("Matanzas", 28.2),
        ("Cienfuegos", 27.5),
        ("Artemisa", 26.8),
        ("Mayabeque", 26.1),
        ("Camagüey", 25.7),
        ("Sancti Spíritus", 25.4),
        ("Villa Clara", 25.3),
        ("Santiago de Cuba", 22.6),
        ("Pinar del Río", 22.4),
        ("Ciego de Ávila", 22.3),
        ("Isla de la Juventud", 21.4),
        ("Guantánamo", 21.0),
        ("Granma", 21.0),
        ("Las Tunas", 20.3),
        ("Holguín", 19.6),
    ]
    y = np.arange(len(rates))[::-1]
    cols = [RED if r[0] == "La Habana" else BLUE for r in rates]
    ax.barh(y, [r[1] for r in rates], color=cols, height=0.68)
    for i, r in zip(y, rates):
        ax.annotate(f"−{r[1]:.0f}", (r[1], i), xytext=(5, 0), textcoords="offset points", va="center", fontsize=10, fontweight="bold", color=RED if r[0] == "La Habana" else INK2)
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rates], fontsize=10)
    ax.set_xlim(0, 38)
    if lang == "es":
        ax.set_xlabel("Emigración neta 2025 (por 1000 hab.)")
        title_block(ax, "El vaciamiento es nacional — La Habana va primero", "Tasa de saldo migratorio neto por provincia, 2025.")
    else:
        ax.set_xlabel("Net emigration rate 2025 (per 1,000)")
        title_block(ax, "National emptying — Havana leads", "Net migration rate by province, 2025.")


def _aging(ax) -> None:
    """English manuscript only (not on IG)."""
    style_ax(ax)
    yrs = [2000, 2005, 2010, 2015, 2019, 2020, 2021, 2022]
    y60 = [14.7, 15.7, 17.8, 19.4, 20.4, 21.3, 21.6, 22.3]
    y014 = [20.5, 19.0, 17.3, 16.5, 16.0, 15.7, 15.7, 15.6]
    py = [2022, 2025, 2030, 2035]
    p60 = [22.3, 26.7, 29.4, 33.1]
    p014 = [15.6, 15.1, 13.8, 12.8]
    oy = [2019, 2025, 2030, 2035]
    om = [20.2, 28.0, 35.0, 40.0]
    ax.axvspan(2022, 2035.6, color="#eef1f4", lw=0)
    ax.plot(yrs, y60, color=ORANGE, lw=2.8, marker="o", ms=5)
    ax.plot(py, p60, color=ORANGE, lw=2.8, ls=(0, (2, 2)))
    ax.plot(oy, om, color=RED, lw=2.8, ls=(0, (1, 1.4)), marker="D", ms=6, zorder=5)
    ax.plot(yrs, y014, color=BLUE, lw=2.8, marker="o", ms=5)
    ax.plot(py, p014, color=BLUE, lw=2.8, ls=(0, (2, 2)))
    ax.annotate("AGE 60+\n(official)", (2003, 16.0), color=ORANGE, fontsize=10.5, fontweight="bold", va="top")
    ax.annotate("~40% (this study)", (2035, 40), color=RED, fontsize=10.5, fontweight="bold", ha="right", va="bottom")
    ax.annotate("AGES 0–14", (2000, 21.3), color=BLUE, fontsize=10.5, fontweight="bold")
    ax.text(2028.5, 18.5, "projection", color=MUTED, fontsize=10, style="italic", ha="center")
    ax.set_xlim(1999, 2036.5)
    ax.set_ylim(10, 43)
    ax.set_xticks(range(2000, 2036, 5))
    ax.set_ylabel("% of population")
    title_block(ax, "Accelerated ageing as young adults leave", "Official path to ~33% aged 60+ by 2035; selective emigration pushes higher.")


def _waterfall(ax) -> None:
    style_ax(ax)
    steps = [
        ("Population\n2019", 11.19, "base"),
        ("Net\nemigration", -2.00, "neg"),
        ("Natural\ndecrease", -0.28, "neg"),
        ("Baseline\nadjustment", -0.35, "neg"),
        ("Living pop.\nend-2025", 8.56, "base"),
    ]
    running = steps[0][1]
    for i, (lab, val, kind) in enumerate(steps):
        if kind == "base":
            ax.bar(i, val, color=INK if i == 0 else VIO, width=0.62, zorder=3)
            ax.annotate(f"{val:.2f} M", (i, val), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=INK if i == 0 else VIO)
            running = val
        else:
            ax.bar(i, abs(val), bottom=running + val, color=RED, width=0.62, alpha=0.92, zorder=3)
            ax.annotate(f"−{abs(val):.2f}", (i, running), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=10.5, fontweight="bold", color=RED)
            ax.plot([i - 0.31, i - 0.69], [running, running], color=MUTED, lw=0.9, ls=(0, (2, 2)))
            running = running + val
    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels([s[0] for s in steps], fontsize=9.5)
    ax.set_ylim(0, 12.2)
    ax.set_ylabel("Population (millions)")
    title_block(ax, "Accounting decomposition of the 2019→2025 loss", "Emigration dominates; natural decrease and baseline correction complete the identity.")


def make_pair(drawer, ig_name: str | None, ms_name: str) -> None:
    if ig_name:
        fig, ax = plt.subplots(figsize=(8.2, 4.15 if "prov" not in ig_name and "triang" not in ig_name else 4.6))
        drawer(ax, "es")
        fig.tight_layout()
        save_ig(fig, ig_name)
    fig, ax = plt.subplots(figsize=(8.2, 4.15 if "prov" not in ms_name and "triang" not in ms_name else 4.6))
    drawer(ax, "en")
    fig.tight_layout()
    save_ms(fig, ms_name)


def main() -> None:
    # Shared IG + EN manuscript set
    make_pair(_pop_series, "ig_poblacion.png", "f1_poblacion.png")
    make_pair(_scissors, "ig_tijera.png", "f2_tijera.png")
    make_pair(_excess, "ig_exceso.png", "f9_exceso.png")
    make_pair(_age, "ig_edad.png", "f10_edad.png")

    fig, ax = plt.subplots(figsize=(8.4, 4.7))
    _triangulation(ax, "es")
    fig.tight_layout()
    save_ig(fig, "ig_triangulacion.png")
    fig, ax = plt.subplots(figsize=(8.4, 4.7))
    _triangulation(ax, "en")
    fig.tight_layout()
    save_ms(fig, "f7_triangulacion.png")

    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    _provinces(ax, "es")
    fig.tight_layout()
    save_ig(fig, "ig_provincias.png")
    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    _provinces(ax, "en")
    fig.tight_layout()
    save_ms(fig, "f11_provincias.png")

    # EN-only extras for the scientific paper
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    _aging(ax)
    fig.tight_layout()
    save_ms(fig, "f4_envejece.png")

    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    _waterfall(ax)
    fig.tight_layout()
    save_ms(fig, "f3_cascada.png")

    # Life expectancy (EN manuscript)
    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    style_ax(ax)
    tx = [2002, 2006, 2012, 2015, 2019]
    tv = [76.99, 77.97, 78.45, 78.07, 77.70]
    ax.plot(tx, tv, color=BLUE, lw=2.8, marker="o", ms=6)
    ax.plot([2019, 2021], [77.70, 71.25], color=RED, lw=2.8, ls=(0, (2, 2)), marker="D", ms=8)
    ax.annotate("peak 78.45\n(2011–13)", (2012, 78.45), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=10.5, fontweight="bold", color=BLUE)
    ax.annotate("71.25 (2021)\nindependent", (2021, 71.25), xytext=(-8, 8), textcoords="offset points", ha="right", fontsize=10.5, fontweight="bold", color=RED)
    ax.set_xlim(2000, 2023.5)
    ax.set_ylim(70, 80)
    ax.set_xticks(range(2000, 2024, 5))
    ax.set_ylabel("Years at birth")
    title_block(ax, "Life expectancy stalls then falls", "Official series peaks then declines; independent 2021 estimate is sharply lower.")
    fig.tight_layout()
    save_ms(fig, "f5_esperanza.png")

    print("publication charts regenerated (IG ES + manuscript EN)")


if __name__ == "__main__":
    main()
