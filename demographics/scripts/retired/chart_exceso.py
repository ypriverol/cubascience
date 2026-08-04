#!/usr/bin/env python3
"""Regenerate excess-mortality figures (delegates to charts_publication)."""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import FIGURES, get_claims
FIGURES.mkdir(parents=True, exist_ok=True)

# -*- coding: utf-8 -*-
import matplotlib as mpl, matplotlib.pyplot as plt, numpy as np

C = get_claims()
XM = C["excess_mortality"]["provisional_schedule_residual_2024_2025"]
pt = int(round(XM["point_illustrative"] / 1000))
bl = int(round(XM["band_low"] / 1000))
bh = int(round(XM["band_high"] / 1000))
crude = int(C["excess_mortality"]["secondary_crude_registered_2020_2025"] / 1000)

SURF="#ffffff"; INK="#111111"; INK2="#3f3f3f"; MUTED="#8a8a85"; GRID="#e7e6e0"; BASE="#c3c2b7"
BLUE="#5598e7"; RED="#e0392f"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.9,"xtick.color":INK2,"ytick.color":INK2,
 "xtick.labelsize":11.5,"ytick.labelsize":10.5,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
fig,ax=plt.subplots(figsize=(9.2,4.7),dpi=200)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="y",color=GRID,lw=0.7)
years=[str(y) for y in XM["years"]]; x=np.arange(2); w=0.34
exp=list(XM["expected_deaths_k"]); reg=list(XM["registered_deaths_k"])
ax.bar(x-w/2,exp,w,color=BLUE,label="Muertes esperadas (con la mortalidad de 2019, ya envejecida)")
ax.bar(x+w/2,reg,w,color=RED,label="Muertes registradas (ONEI)")
for xi,v in zip(x-w/2,exp): ax.annotate(f"{v:.0f} mil",(xi,v),xytext=(0,5),textcoords="offset points",ha="center",fontsize=10.5,fontweight="bold",color="#2a6bbf")
for xi,v in zip(x+w/2,reg): ax.annotate(f"{v:.0f} mil",(xi,v),xytext=(0,5),textcoords="offset points",ha="center",fontsize=10.5,fontweight="bold",color=RED)
for i,(e,r) in enumerate(zip(exp,reg)):
    ax.annotate(f"+{r-e:.0f} mil\nde más",(x[i]+w/2,r),xytext=(34,-6),textcoords="offset points",ha="left",va="top",fontsize=10,fontweight="bold",color=INK)
ax.set_xticks(x); ax.set_xticklabels(years); ax.set_ylim(0,155)
ax.set_ylabel("Defunciones (miles)",fontsize=11.5)
ax.set_yticks([0,40,80,120]); ax.set_yticklabels(["0","40 mil","80 mil","120 mil"])
ax.legend(frameon=False,fontsize=9.7,loc="upper left",bbox_to_anchor=(0,1.0))
ax.set_title("Aun descontando el envejecimiento, mueren más de lo normal",fontsize=15,fontweight="bold",loc="left",color=INK,pad=30)
ax.text(0,1.045,f"Residual provisional ~{pt} mil en 2024–2025 (banda {bl}–{bh} mil); distinto del exceso bruto ~{crude} mil (2020–2025). Puente CDR 2019; pipeline edad–sexo ONEI 3.15 pendiente.",
        transform=ax.transAxes,fontsize=10.2,color=INK2,va="bottom")
fig.tight_layout(); fig.savefig(str(FIGURES / "f9_exceso.png"), bbox_inches="tight"); plt.close(fig)
print("exceso figura lista")
