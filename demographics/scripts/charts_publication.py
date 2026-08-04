#!/usr/bin/env python3
"""Regenerate publication charts: Spanish infographic + English manuscript (seaborn style, 600 dpi MS)."""
from __future__ import annotations

import json

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from constants import ARTIFACTS, get_claims  # noqa: E402
from plot_style import (  # noqa: E402
    BLUE,
    CEIL,
    GREEN,
    INK,
    INK2,
    MUTED,
    ORANGE,
    RED,
    SOFT_GREEN,
    SOFT_RED,
    VIO,
    apply_style,
    save_ig,
    save_ig_en,
    save_ms,
    style_ax,
    title_block,
)

apply_style()
C = get_claims()
MD = C["population_scenarios"]["scenarios"]["central"]
TRI = C["triangulation"]["sources"]
SEL = C["selectivity"]
VIT = C["vital_series"]
POP_OFF = C["population_official_m"]
PATH = C["model_d_path_m"]
# The retired crude-CDR bridge lives at
# C["excess_mortality"]["provisional_schedule_residual_2024_2025"]. Reading it
# here put "~77k, sensitivity 65-90k" and 95k/92k expected-death bars into the
# shipped infographic PNGs, against an age-standardised artifact of 50.1k
# [32.6-67.5k] and 112,076 expected. Driven from the artifact now.
_AM = json.loads((ARTIFACTS / "attributable_mortality.json").read_text(encoding="utf-8"))
_AM_BY = {r["year"]: r for r in _AM["by_year"]}
_CUM_2425 = _AM["cumulative_excess"]["2024_2025"]
_EXC_YEARS = [2024, 2025]
_EXC_EXPECTED_K = [_AM_BY[y]["expected_deaths_2019_schedule"]["median"] / 1000 for y in _EXC_YEARS]
_EXC_REGISTERED_K = [_AM_BY[y]["registered_deaths"] / 1000 for y in _EXC_YEARS]

# Scenario values are read from the artifact, never typed. Round 6 found 22.7,
# 8.59 and a 2.2 M waterfall total hard-coded here and rendered into the shipped
# PDFs, contradicting the LaTeX caption on the same page.
_PS = json.loads((ARTIFACTS / "population_scenarios.json").read_text(encoding="utf-8"))
SC = _PS["scenarios"]
_C = SC["central"]
_GAP = _C["gap_vs_official_2021"] / 1e6
_POP = _C["pop_end_2025"] / 1e6
_EMIG = _C["emigration_share_of_gap_pct"]
_U0 = _C["components"]["baseline_overstatement_U0"] / 1e6
_MIG = _C["components"]["net_emigration_2022_2025"] / 1e6
_NAT = _C["components"]["natural_decrease"] / 1e6
# Top of the exit-correcting family (housing x occupancy), not a typed constant.
_TRI_HI = max(s["estimate"] for s in C["triangulation"]["sources"]
              if isinstance(s.get("estimate"), (int, float))
              and s["estimate"] < 9.0)


def _pop_series(ax, lang: str) -> None:
    style_ax(ax)
    off_years = POP_OFF["years"]
    off_vals = POP_OFF["values"]
    official = pd.DataFrame({"year": off_years, "pop": off_vals, "series": "official"})
    path_years = PATH["years"]
    path_vals = PATH["values"]
    model = pd.DataFrame({"year": path_years, "pop": path_vals, "series": "model"})
    ax.axvspan(2025, 2030.6, color=SOFT_GREEN, alpha=0.35, lw=0, zorder=0)
    sns.lineplot(
        data=official,
        x="year",
        y="pop",
        ax=ax,
        color=BLUE,
        linewidth=2.8,
        marker="o",
        markersize=8,
        zorder=4,
        legend=False,
    )
    sns.lineplot(
        data=model.iloc[:3],
        x="year",
        y="pop",
        ax=ax,
        color=RED,
        linewidth=3.0,
        marker="o",
        markersize=8.5,
        zorder=5,
        legend=False,
    )
    ax.plot(
        model["year"].iloc[2:],
        model["pop"].iloc[2:],
        color=RED,
        lw=2.8,
        ls=(0, (1.8, 1.5)),
        marker="o",
        ms=8,
        zorder=5,
    )
    ax.annotate("11.1 M", (2021, 11.11), xytext=(0, 9), textcoords="offset points", fontsize=11, fontweight="bold", ha="center")
    ax.annotate(
        f"{MD['pop_end_2025_m']:.1f} M",
        (2025, MD["pop_end_2025_m"]),
        xytext=(-6, -16),
        textcoords="offset points",
        color=RED,
        fontsize=11,
        fontweight="bold",
        ha="right",
    )
    ax.annotate("≈7 M (2030)", (2030, 7.0), xytext=(8, 0), textcoords="offset points", color=RED, fontsize=11, fontweight="bold", va="center")
    ax.set_xlim(2018.5, 2031.2)
    ax.set_ylim(6.2, 11.9)
    ax.set_xticks(range(2019, 2031, 2))
    ax.set_xlabel("")
    if lang == "es":
        # Sits above the blue line at 2024-25; the old (2023.7, 9.95) anchor fell
        # straight on the red Model D line. "estimación real" also overclaimed:
        # D is a scenario, not a measurement.
        ax.annotate("cifra oficial", (2024.6, 10.3), color=BLUE, fontsize=12, fontweight="bold", ha="center")
        ax.annotate("escenario central", (2022.3, 9.0), color=RED, fontsize=12, fontweight="bold", ha="center")
        ax.text(2027.7, 10.45, "proyección ilustrativa", color=MUTED, fontsize=11, style="italic", ha="center")
        ax.set_ylabel("Millones de habitantes")
        title_block(
            ax,
            "Despoblación acelerada de Cuba, 2021–2026",
            f"Brecha vs el stock oficial de 2021: {SC['central']['gap_pct']:.1f}% en 2025, ~25% hacia 2026 (escenario central).",
        )
    else:
        ax.annotate("official series", (2024.6, 10.3), color=BLUE, fontsize=12, fontweight="bold", ha="center")
        ax.annotate("central scenario", (2022.3, 9.0), color=RED, fontsize=12, fontweight="bold", ha="center")
        ax.text(2027.7, 10.45, "illustrative scenario", color=MUTED, fontsize=11, style="italic", ha="center")
        ax.set_ylabel("Population (millions)")
        title_block(
            ax,
            "Cuba’s 2021–2026 population decline",
            f"Gap vs the official 2021 stock: {SC['central']['gap_pct']:.1f}% by 2025, ~25% by 2026 (central scenario).",
        )


def _scissors(ax, lang: str) -> None:
    style_ax(ax)
    yy = VIT["years"]
    b = np.array(VIT["births"], dtype=float) / 1000
    d = np.array(VIT["deaths"], dtype=float) / 1000
    df = pd.DataFrame({"year": yy + yy, "count": np.r_[b, d], "kind": ["births"] * len(yy) + ["deaths"] * len(yy)})
    ax.fill_between(yy, b, d, where=(d > b), color=SOFT_RED, alpha=0.55, interpolate=True, zorder=1)
    sns.lineplot(
        data=df,
        x="year",
        y="count",
        hue="kind",
        ax=ax,
        palette={"births": BLUE, "deaths": RED},
        linewidth=2.8,
        marker="o",
        markersize=7.5,
        legend=False,
        zorder=3,
    )
    ax.annotate("68k", (2025, 68.064), xytext=(-2, -4), textcoords="offset points", color=BLUE, fontsize=11, fontweight="bold", ha="right", va="top")
    ax.annotate("136k", (2025, 136.214), xytext=(-2, 4), textcoords="offset points", color=RED, fontsize=11, fontweight="bold", ha="right", va="bottom")
    ax.set_xlim(2016.5, 2025.8)
    ax.set_ylim(50, 185)
    ax.set_xticks(range(2017, 2026, 2))
    ax.set_xlabel("")
    if lang == "es":
        ax.annotate("NACIMIENTOS", (2017.1, 118), color=BLUE, fontsize=11.5, fontweight="bold")
        ax.annotate("DEFUNCIONES", (2017.1, 99), color=RED, fontsize=11.5, fontweight="bold")
        ax.set_ylabel("Miles por año")
        title_block(ax, "La tijera demográfica: mueren casi el doble", f"Aunque nadie emigrara, el país ya se encogería (−{abs(C['vital']['natural_balance_2025']):,} en 2025).".replace(",", " "))
    else:
        ax.annotate("BIRTHS", (2017.1, 118), color=BLUE, fontsize=11.5, fontweight="bold")
        ax.annotate("DEATHS", (2017.1, 99), color=RED, fontsize=11.5, fontweight="bold")
        ax.set_ylabel("Thousands per year")
        title_block(ax, "Demographic scissors: deaths roughly double births", f"Natural decrease alone removes ~{abs(C['vital']['natural_balance_2025']):,} people in 2025.".replace(",", " "))


def _excess_subtitle(lang: str) -> str:
    pt = int(round(_CUM_2425["median"] / 1000))
    bl = int(round(_CUM_2425["p05"] / 1000))
    bh = int(round(_CUM_2425["p95"] / 1000))
    if lang == "es":
        return (
            f"Exceso vs la tabla de tasas por edad de 2019: ~{pt} mil en 2024–2025 "
            f"(rango {bl}–{bh} mil). No es una atribución causal."
        )
    return (
        f"Excess vs the 2019 age-specific schedule: ~{pt}k over 2024–2025 "
        f"(range {bl}–{bh}k). Not a causal attribution."
    )


def _excess(ax, lang: str) -> None:
    style_ax(ax)
    if lang == "es":
        lab_e, lab_r = "Esperadas (tasas 2019)", "Registradas"
        ylab = "Defunciones (miles)"
        title = "Exceso de defunciones vs la tabla de tasas por edad de 2019, 2024–2025"
    else:
        lab_e, lab_r = "Expected (2019 rates)", "Registered"
        ylab = "Deaths (thousands)"
        title = "Excess deaths vs the 2019 age-specific schedule, 2024–2025"
    sub = _excess_subtitle(lang)
    rows = []
    for y, e, r in zip(_EXC_YEARS, _EXC_EXPECTED_K, _EXC_REGISTERED_K):
        rows.append({"year": str(y), "deaths": e, "kind": lab_e})
        rows.append({"year": str(y), "deaths": r, "kind": lab_r})
    df = pd.DataFrame(rows)
    sns.barplot(
        data=df,
        x="year",
        y="deaths",
        hue="kind",
        ax=ax,
        palette={lab_e: "#93c5fd", lab_r: RED},
        width=0.72,
        edgecolor="white",
        linewidth=0.6,
    )
    for container, color in zip(ax.containers, ["#1d4ed8", RED]):
        for bar in container:
            h = bar.get_height()
            ax.annotate(
                f"{h:.0f}",
                (bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                fontsize=11,
                fontweight="bold",
                color=color,
            )
    # gap callouts on registered bars
    for i, (e, r) in enumerate(zip(_EXC_EXPECTED_K, _EXC_REGISTERED_K)):
        ax.annotate(
            f"+{r - e:.0f}k",
            (i + 0.18, r),
            xytext=(18, 0),
            textcoords="offset points",
            ha="left",
            fontsize=10.5,
            fontweight="bold",
            color=INK,
        )
    ax.set_ylim(0, 165)
    ax.set_yticks([0, 40, 80, 120])
    ax.set_ylabel(ylab)
    ax.set_xlabel("")
    ax.legend(fontsize=9.5, loc="upper left", title=None)
    title_block(ax, title, sub)


def _age(ax, lang: str) -> None:
    style_ax(ax)
    if lang == "es":
        bands = ["Niños (0–14)", "Edad laboral y fértil (15–59)", "Mayores (60+)"]
        lab_e, lab_r = "Se van", "Se quedan"
        ylab = "% del grupo"
        title = "Quién se va y quién se queda"
        sub = "Éxodo selectivo: el 77% de quienes emigran tienen 15–59 años."
    else:
        bands = ["Children (0–14)", "Working / fertile ages (15–59)", "Older adults (60+)"]
        lab_e, lab_r = "Emigrants", "Remaining"
        ylab = "Share of group (%)"
        title = "Who leaves — and who remains"
        sub = "Selective exodus: 77% of emigrants are aged 15–59."
    emig = [SEL["emigrants_children_pct"], SEL["emigrants_age_15_59_pct"], SEL["emigrants_60_plus_pct"]]
    resid = [SEL["residents_children_pct"], SEL["residents_15_59_pct"], int(round(SEL["pct_age_60_plus_remaining"]))]
    df = pd.DataFrame(
        {
            "band": bands * 2,
            "share": emig + resid,
            "group": [lab_e] * 3 + [lab_r] * 3,
        }
    )
    sns.barplot(
        data=df,
        x="band",
        y="share",
        hue="group",
        ax=ax,
        palette={lab_e: ORANGE, lab_r: BLUE},
        width=0.75,
        edgecolor="white",
        linewidth=0.6,
    )
    for container, color in zip(ax.containers, [ORANGE, BLUE]):
        for bar in container:
            h = bar.get_height()
            ax.annotate(
                f"{h:.0f}%",
                (bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                fontsize=11,
                fontweight="bold",
                color=color,
            )
    ax.set_ylim(0, 95)
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_ylabel(ylab)
    ax.set_xlabel("")
    ax.legend(fontsize=11, loc="upper right", title=None)
    title_block(ax, title, sub)


def _triangulation(ax, lang: str) -> None:
    style_ax(ax, grid="x")
    rows = [(r["source"], float(r["estimate"]), r["role"]) for r in TRI]
    role_color = {
        "ceiling": CEIL,
        "official": BLUE,
        "occupancy": GREEN,
        "occupancy_fragile": GREEN,
        "independent": ORANGE,
        "independent_shared_assumptions": ORANGE,
        "preferred": RED,
        "estimand_not_validator": RED,
    }
    ax.axvspan(
        C["triangulation"]["band_low_m"],
        C["triangulation"]["band_high_m"],
        color=SOFT_GREEN,
        alpha=0.55,
        lw=0,
        zorder=0,
    )
    y = np.arange(len(rows))[::-1]
    mapping_es = {
        "UN (stale migration)": "ONU (no actualiza migración)",
        "MINSAP denominator": "Denominador del MINSAP",
        "Electoral roll (level)": "Padrón electoral (nivel)",
        "ONEI official": "ONEI — oficial",
        "Housing × occupancy": "Viviendas × ocupación",
        "Albizu-Campos (2023)": "Albizu-Campos (2023)",
        "This study (central scenario)": "Este estudio (escenario central)",
        "Albizu-Campos (2024)": "Albizu-Campos (2024)",
    }
    for i, (lab, val, role) in zip(y, rows):
        col = role_color.get(role, INK2)
        preferred = role in ("preferred", "estimand_not_validator")
        ax.hlines(i, 7.4, val, colors=col, linewidths=1.2 if preferred else 0.7, alpha=0.35, zorder=2)
        ax.plot(
            val,
            i,
            "D" if preferred else "o",
            color=col,
            ms=15 if preferred else 11,
            zorder=4,
            markeredgecolor="white",
            markeredgewidth=1.4,
        )
        ax.annotate(
            f"{val:.2f}",
            (val, i),
            xytext=(10, 0),
            textcoords="offset points",
            va="center",
            fontsize=10.5,
            fontweight="bold",
            color=col if col != CEIL else INK2,
        )
    labels = [mapping_es.get(lab, lab) if lang == "es" else lab for lab, _, _ in rows]
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10.5)
    ax.set_xlim(7.35, 11.55)
    if lang == "es":
        ax.set_xlabel("Población estimada (millones)")
        ax.text(8.45, -1.15, f"zona más probable 8,0–{_TRI_HI:.1f} M".replace(".",","), color=GREEN, fontsize=10.5, fontweight="bold", ha="center")
        title_block(ax, "Triangulación: ¿cuántos cubanos quedan?", "Los registros que no depuran emigrados actúan como techos.")
    else:
        ax.set_xlabel("Estimated population (millions)")
        ax.text(8.45, -1.15, f"most probable band 8.0–{_TRI_HI:.1f} M", color=GREEN, fontsize=10.5, fontweight="bold", ha="center")
        title_block(ax, "How many Cubans remain? Eight external registers", "Registers that do not purge emigrants act as ceilings.")
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
    df = pd.DataFrame(rates, columns=["province", "rate"]).sort_values("rate", ascending=True)
    colors = [RED if p == "La Habana" else BLUE for p in df["province"]]
    sns.barplot(
        data=df,
        y="province",
        x="rate",
        ax=ax,
        hue="province",
        palette=dict(zip(df["province"], colors)),
        legend=False,
        edgecolor="white",
        linewidth=0.4,
    )
    for i, (_, row) in enumerate(df.iterrows()):
        ax.annotate(
            f"−{row['rate']:.0f}",
            (row["rate"], i),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=RED if row["province"] == "La Habana" else INK2,
        )
    ax.set_xlim(0, 38)
    ax.set_ylabel("")
    if lang == "es":
        ax.set_xlabel("Emigración neta 2025 (por 1000 hab.)")
        title_block(ax, "Vaciamiento nacional — La Habana va primero", "Ninguna provincia pierde menos del ~2% de su gente al año.")
    else:
        ax.set_xlabel("Net emigration rate 2025 (per 1,000)")
        title_block(ax, "National emptying — Havana leads", "No province loses less than about 2% of its people per year.")


def _aging(ax, lang: str = "en") -> None:
    style_ax(ax)
    yrs = [2000, 2005, 2010, 2015, 2019, 2020, 2021, 2022]
    y60 = [14.7, 15.7, 17.8, 19.4, 20.4, 21.3, 21.6, 22.3]
    y014 = [20.5, 19.0, 17.3, 16.5, 16.0, 15.7, 15.7, 15.6]
    py = [2022, 2025, 2030, 2035]
    p60 = [22.3, 26.7, 29.4, 33.1]
    p014 = [15.6, 15.1, 13.8, 12.8]
    oy = [2019, 2025, 2030, 2035]
    om = [20.2, 28.0, 35.0, 40.0]
    ax.axvspan(2022, 2035.6, color=SOFT_GREEN, alpha=0.35, lw=0)
    ax.plot(yrs, y60, color=ORANGE, lw=2.8, marker="o", ms=6)
    ax.plot(py, p60, color=ORANGE, lw=2.8, ls=(0, (2, 2)))
    ax.plot(oy, om, color=RED, lw=2.8, ls=(0, (1, 1.4)), marker="D", ms=7, zorder=5)
    ax.plot(yrs, y014, color=BLUE, lw=2.8, marker="o", ms=6)
    ax.plot(py, p014, color=BLUE, lw=2.8, ls=(0, (2, 2)))
    if lang == "es":
        l60, l014 = "60 AÑOS Y MÁS\n(oficial)", "0–14 AÑOS"
        lill, lproj = "~40% (ilustrativo)", "proyección"
        ylab = "% de la población"
        title = "Envejecimiento acelerado de quienes se quedan"
        sub = "Trayectoria oficial hacia ~33% de 60+ en 2035; la emigración selectiva lo empuja al alza."
    else:
        l60, l014 = "AGE 60+\n(official)", "AGES 0–14"
        lill, lproj = "~40% (illustrative)", "projection"
        ylab = "% of population"
        title = "Accelerated ageing of those who remain"
        sub = "Official path to ~33% aged 60+ by 2035; selective emigration pushes higher."
    # (2003, 16.0) sat directly on the orange line; the 2010-2018 band above it is clear.
    ax.annotate(l60, (2010.5, 21.4), color=ORANGE, fontsize=10.5, fontweight="bold",
                ha="left", va="bottom")
    ax.annotate(lill, (2035, 40), color=RED, fontsize=10.5, fontweight="bold", ha="right", va="bottom")
    ax.annotate(l014, (2000, 21.3), color=BLUE, fontsize=10.5, fontweight="bold")
    ax.text(2028.5, 18.5, lproj, color=MUTED, fontsize=10, style="italic", ha="center")
    ax.set_xlim(1999, 2036.5)
    ax.set_ylim(10, 43)
    ax.set_xticks(range(2000, 2036, 5))
    ax.set_ylabel(ylab)
    title_block(ax, title, sub)


def _waterfall(ax, lang: str = "en") -> None:
    style_ax(ax)
    # Model D medians on end-2021 → end-2025 window (rounded)
    if lang == "es":
        # "Población real" would contradict the paper's framing: D is a scenario,
        # not a measurement of the living population.
        labels = ["Población\nfin-2021", "Emigración\nneta", "Variación\nnatural",
                  "Ajuste de\nbase", "Escenario D\nfin-2025"]
        ylab = "Población (millones)"
        title = "Adónde fueron 2.2 millones de personas (2021→2025)"
        sub = ("Medianas del escenario D con priores fijos (~91% emigración); "
               "no es atribución identificada.")
    else:
        labels = ["Population\nend-2021", "Net\nemigration", "Natural\ndecrease",
                  "Baseline\nadjustment", "Living pop.\nend-2025"]
        ylab = "Population (millions)"
        title = f"Where {_GAP:.2f} million people went (2021\u21922025)"
        sub = (f"Central-scenario decomposition under fixed priors "
               f"(~{_EMIG:.0f}% emigration); not identified attribution.")
    # Driven from population_scenarios.json. These were hard-coded, so the
    # shipped figure showed 8.59 and a 2.2 M total while the caption on the
    # same page said 8.58 and 2.53 M.
    steps = list(zip(labels, [11.113, -_MIG, -_NAT, -_U0, _POP],
                     ["base", "neg", "neg", "neg", "base"]))
    running = steps[0][1]
    for i, (lab, val, kind) in enumerate(steps):
        if kind == "base":
            color = INK if i == 0 else VIO
            ax.bar(i, val, color=color, width=0.62, zorder=3, edgecolor="white", linewidth=0.5)
            ax.annotate(f"{val:.2f} M", (i, val), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=color)
            running = val
        else:
            ax.bar(i, abs(val), bottom=running + val, color=RED, width=0.62, alpha=0.92, zorder=3, edgecolor="white", linewidth=0.5)
            ax.annotate(f"−{abs(val):.2f}", (i, running), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=10.5, fontweight="bold", color=RED)
            ax.plot([i - 0.31, i - 0.69], [running, running], color=MUTED, lw=0.9, ls=(0, (2, 2)))
            running = running + val
    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels([s[0] for s in steps], fontsize=9.5)
    ax.set_ylim(0, 12.2)
    ax.set_ylabel(ylab)
    title_block(ax, title, sub)


def _life_expectancy(ax) -> None:
    style_ax(ax)
    tx = [2002, 2006, 2012, 2015, 2019]
    tv = [76.99, 77.97, 78.45, 78.07, 77.70]
    ax.plot(tx, tv, color=BLUE, lw=2.8, marker="o", ms=7)
    ax.plot([2019, 2021], [77.70, 71.25], color=RED, lw=2.8, ls=(0, (2, 2)), marker="D", ms=9)
    ax.fill_between([2019, 2021], [77.70, 71.25], [77.70, 77.70], color=SOFT_RED, alpha=0.45, zorder=1)
    ax.annotate("peak 78.45\n(2011–13)", (2012, 78.45), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=10.5, fontweight="bold", color=BLUE)
    ax.annotate("71.25 (2021)\nindependent", (2021, 71.25), xytext=(-8, 8), textcoords="offset points", ha="right", fontsize=10.5, fontweight="bold", color=RED)
    ax.set_xlim(2000, 2023.5)
    ax.set_ylim(70, 80)
    ax.set_xticks(range(2000, 2024, 5))
    ax.set_ylabel("Years at birth")
    title_block(
        ax,
        "Life expectancy stalls, then falls",
        "Official series peaks then declines; independent 2021 estimate is a sharp health-system shock.",
    )


def make_pair(drawer, ig_name: str | None, ms_name: str) -> None:
    tall = any(k in (ig_name or "") + ms_name for k in ("prov", "triang"))
    figsize = (8.4, 5.0 if tall else 4.25)
    if ig_name:
        fig, ax = plt.subplots(figsize=figsize)
        drawer(ax, "es")
        fig.tight_layout()
        save_ig(fig, ig_name)
        fig, ax = plt.subplots(figsize=figsize)
        drawer(ax, "en")
        fig.tight_layout()
        save_ig_en(fig, ig_name)
    fig, ax = plt.subplots(figsize=figsize)
    drawer(ax, "en")
    fig.tight_layout()
    save_ms(fig, ms_name)


def main() -> None:
    make_pair(_pop_series, "ig_poblacion.png", "f1_poblacion.png")
    make_pair(_scissors, "ig_tijera.png", "f2_tijera.png")
    make_pair(_excess, "ig_exceso.png", "f9_exceso.png")
    fig, ax = plt.subplots(figsize=(8.4, 4.25))
    _excess(ax, "es")
    fig.tight_layout()
    save_ms(fig, "f9_exceso_es.png")
    make_pair(_age, "ig_edad.png", "f10_edad.png")

    fig, ax = plt.subplots(figsize=(8.5, 4.9))
    _triangulation(ax, "es")
    fig.tight_layout()
    save_ig(fig, "ig_triangulacion.png")
    fig, ax = plt.subplots(figsize=(8.5, 4.9))
    _triangulation(ax, "en")
    fig.tight_layout()
    save_ig_en(fig, "ig_triangulacion.png")
    fig, ax = plt.subplots(figsize=(8.5, 4.9))
    _triangulation(ax, "en")
    fig.tight_layout()
    save_ms(fig, "f7_triangulacion.png")

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    _provinces(ax, "es")
    fig.tight_layout()
    save_ig(fig, "ig_provincias.png")
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    _provinces(ax, "en")
    fig.tight_layout()
    save_ig_en(fig, "ig_provincias.png")
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    _provinces(ax, "en")
    fig.tight_layout()
    save_ms(fig, "f11_provincias.png")

    fig, ax = plt.subplots(figsize=(8.3, 4.4))
    _aging(ax)
    fig.tight_layout()
    save_ms(fig, "f4_envejece.png")

    fig, ax = plt.subplots(figsize=(8.3, 4.35))
    _waterfall(ax)
    fig.tight_layout()
    save_ms(fig, "f3_cascada.png")

    fig, ax = plt.subplots(figsize=(8.3, 4.1))
    _life_expectancy(ax)
    fig.tight_layout()
    save_ms(fig, "f5_esperanza.png")

    print("publication charts regenerated (seaborn style; IG ES + IG EN + manuscript EN)")


if __name__ == "__main__":
    main()
