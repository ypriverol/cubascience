from pathlib import Path
import sys
_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS, FIGURES
ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# -*- coding: utf-8 -*-
import matplotlib as mpl, matplotlib.pyplot as plt, numpy as np
SURF="#ffffff"; INK="#111111"; INK2="#3f3f3f"; MUTED="#8a8a85"; GRID="#e7e6e0"; BASE="#c3c2b7"
BLUE="#5598e7"; RED="#e0392f"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.9,"xtick.color":INK2,"ytick.color":INK2,
 "xtick.labelsize":11.5,"ytick.labelsize":10.5,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
fig,ax=plt.subplots(figsize=(9.2,4.7),dpi=200)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="y",color=GRID,lw=0.7)
years=["2024","2025"]; x=np.arange(2); w=0.34
exp=[112.5,113.8]; reg=[128.1,136.2]
ax.bar(x-w/2,exp,w,color=BLUE,label="Muertes esperadas (con la mortalidad de 2019, ya envejecida)")
ax.bar(x+w/2,reg,w,color=RED,label="Muertes registradas (ONEI)")
for xi,v in zip(x-w/2,exp): ax.annotate(f"{v:.0f} mil",(xi,v),xytext=(0,5),textcoords="offset points",ha="center",fontsize=10.5,fontweight="bold",color="#2a6bbf")
for xi,v in zip(x+w/2,reg): ax.annotate(f"{v:.0f} mil",(xi,v),xytext=(0,5),textcoords="offset points",ha="center",fontsize=10.5,fontweight="bold",color=RED)
# exceso
for i,(e,r) in enumerate(zip(exp,reg)):
    ax.annotate(f"+{r-e:.0f} mil\nde más",(x[i]+w/2,r),xytext=(34,-6),textcoords="offset points",ha="left",va="top",fontsize=10,fontweight="bold",color=INK)
ax.set_xticks(x); ax.set_xticklabels(years); ax.set_ylim(0,155)
ax.set_ylabel("Defunciones (miles)",fontsize=11.5)
ax.set_yticks([0,40,80,120]); ax.set_yticklabels(["0","40 mil","80 mil","120 mil"])
ax.legend(frameon=False,fontsize=9.7,loc="upper left",bbox_to_anchor=(0,1.0))
ax.set_title("Aun descontando el envejecimiento, mueren más de lo normal",fontsize=15,fontweight="bold",loc="left",color=INK,pad=30)
ax.text(0,1.045,"En 2024–2025 hubo ~40 000–60 000 muertes por encima de lo esperado; las tasas de los mayores de 60 están ~11–27% sobre 2019.",
        transform=ax.transAxes,fontsize=10.2,color=INK2,va="bottom")
fig.tight_layout(); fig.savefig(str(FIGURES / "f9_exceso.png"), bbox_inches="tight"); plt.close(fig)
print("exceso figura lista")
