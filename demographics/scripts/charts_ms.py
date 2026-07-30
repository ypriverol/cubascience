from pathlib import Path
import sys
_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS, FIGURES
ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# -*- coding: utf-8 -*-
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
from scipy.stats import norm, beta as beta_dist

SURF="#ffffff"; INK="#111111"; INK2="#444444"; MUTED="#7a7a75"; GRID="#e4e3dd"; BASE="#c3c2b7"
S1,S2,S3="#2a78d6","#eb6834","#1baf7a"; S4="#eda100"; RED="#e34948"; VIO="#7a3fb0"
SEQ=["#cde2fb","#9ec5f4","#6da7ec","#3987e5","#2a78d6","#1c5cab"]
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.8,"xtick.color":MUTED,"ytick.color":MUTED,
 "xtick.labelsize":9,"ytick.labelsize":9,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.6); ax.tick_params(length=0)

# ===== Figura: descomposición en cascada (waterfall) hacia Modelo D =====
# valores en millones
steps=[
 ("Población\nfin-2019\n(oficial)",11.19,"base"),
 ("− ajuste de\nbase (padrón\ninflado)",-0.35,"neg"),
 ("+ nacimientos\n2020–25",0.53,"pos"),
 ("− defunciones\n2020–25",-0.81,"neg"),
 ("− emigración\nneta 2020–25",-2.00,"neg"),
 ("Población\nfin-2025\n(Modelo D)",8.56,"base"),
]
fig,ax=plt.subplots(figsize=(9.0,4.8),dpi=200); style(ax)
x=np.arange(len(steps)); running=steps[0][1]
for i,(lab,val,kind) in enumerate(steps):
    if kind=="base":
        ax.bar(i,val,color=INK if i==0 else VIO,width=0.62,zorder=3)
        ax.annotate(f"{val:.2f}M",(i,val),xytext=(0,6),textcoords="offset points",ha="center",fontsize=10,fontweight="bold",color=INK if i==0 else VIO)
        running=val
    else:
        bottom=running+val if val<0 else running
        color=RED if kind=="neg" else S3
        ax.bar(i,abs(val),bottom=min(running,running+val),color=color,width=0.62,alpha=0.9,zorder=3)
        ax.annotate(f"{val:+.2f}M",(i,max(running,running+val)),xytext=(0,6),textcoords="offset points",ha="center",fontsize=9.5,fontweight="bold",color=color)
        # connector
        ax.plot([i-0.31,i-0.69+0.38],[running,running],color=MUTED,lw=0.8,ls=(0,(2,2)))
        running=running+val
ax.plot([len(steps)-1-0.31,len(steps)-2+0.31],[running,running],color=MUTED,lw=0.8,ls=(0,(2,2)))
ax.set_xticks(x); ax.set_xticklabels([s[0] for s in steps],fontsize=8.5)
ax.set_ylim(0,12); ax.set_ylabel("Población (millones)",fontsize=10)
ax.set_title("Descomposición de la variación de población, 2019–2025 (Modelo D)",fontsize=13,fontweight="bold",loc="left",color=INK,pad=12)
fig.tight_layout(); fig.savefig(str(ARTIFACTS / "ms_waterfall.png"), bbox_inches="tight"); plt.close(fig)

# ===== Figura: distribución posterior Monte Carlo (Modelo D) en español =====
declD=np.load(str(ARTIFACTS / "modelD_decline.npy"))/1e6
q5,q50,q95=np.percentile(declD,[5,50,95])
fig,ax=plt.subplots(figsize=(9.0,4.2),dpi=200); style(ax)
counts,edges=np.histogram(declD,bins=90,range=(1.6,3.0),density=True)
centers=(edges[:-1]+edges[1:])/2; inci=(centers>=q5)&(centers<=q95)
ax.bar(centers[~inci],counts[~inci],width=(edges[1]-edges[0])*0.92,color=SEQ[1])
ax.bar(centers[inci],counts[inci],width=(edges[1]-edges[0])*0.92,color=SEQ[4])
ax.axvline(q50,color=INK,lw=1.4,ls=(0,(3,2)))
ax.annotate(f"mediana\n{q50:.2f} M",(q50+0.02,ax.get_ylim()[1]*0.9),color=INK,fontsize=9.5,fontweight="bold",va="top")
ax.annotate(f"intervalo del 90%: {q5:.2f}–{q95:.2f} M",(2.72,ax.get_ylim()[1]*0.55),color=SEQ[5],fontsize=10,fontweight="bold",ha="right")
ax.set_yticks([]); ax.set_xlim(1.6,3.0)
ax.set_xlabel("Pérdida total de población, fin-2019 → fin-2025 (millones)",fontsize=10)
ax.set_title("Distribución posterior del Modelo D (10⁶ simulaciones)",fontsize=13,fontweight="bold",loc="left",color=INK,pad=12)
fig.tight_layout(); fig.savefig(str(ARTIFACTS / "ms_posterior.png"), bbox_inches="tight"); plt.close(fig)
print("ms figs ok", round(q5,2),round(q50,2),round(q95,2))
