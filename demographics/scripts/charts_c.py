from pathlib import Path
import sys
_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS, FIGURES
ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt

SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
S1,S2,S3="#2a78d6","#eb6834","#1baf7a"; S4="#eda100"; RED="#e34948"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.8,"xtick.color":MUTED,"ytick.color":MUTED,
 "xtick.labelsize":9,"ytick.labelsize":9,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.6); ax.tick_params(length=0)

# ---------- Chart 6: three models end-2025 + end-2026 nowcast ----------
popB25=np.load(str(ARTIFACTS / "modelB_pop.npy")); popC25=np.load(str(ARTIFACTS / "modelC_pop.npy"))
popB26=np.load(str(ARTIFACTS / "modelB_pop2026.npy")); popC26=np.load(str(ARTIFACTS / "modelC_pop2026.npy"))
# Model A end-2025 approx from earlier (median 9.06, ci 8.58-9.34) and 2026 (8.76, 8.27-9.07)
def qs(a): return np.percentile(a,[5,50,95])/1e6
rows=[
 ("Model A · ONEI-anchored", np.array([8.58,9.06,9.34]), np.array([8.27,8.76,9.07]), S1),
 ("Model B · crisis-adjusted", qs(popB25), qs(popB26), S2),
 ("Model C · worst-case", qs(popC25), qs(popC26), RED),
]
fig,ax=plt.subplots(figsize=(8.8,4.6),dpi=200); style(ax)
y=np.arange(len(rows))[::-1]
for i,(name,e25,e26,c) in zip(y,rows):
    ax.plot([e25[0],e25[2]],[i+0.13,i+0.13],color=c,lw=2.4,solid_capstyle="round",alpha=0.5)
    ax.plot(e25[1],i+0.13,"o",color=c,ms=9,zorder=4)
    ax.plot([e26[0],e26[2]],[i-0.13,i-0.13],color=c,lw=2.4,solid_capstyle="round",alpha=0.5)
    ax.plot(e26[1],i-0.13,"D",color=c,ms=8,zorder=4)
    ax.annotate(f"{e25[1]:.2f}M",(e25[1],i+0.13),xytext=(0,9),textcoords="offset points",
                ha="center",fontsize=9,fontweight="bold",color=c)
    ax.annotate(f"{e26[1]:.2f}M",(e26[1],i-0.13),xytext=(0,-15),textcoords="offset points",
                ha="center",fontsize=9,fontweight="bold",color=c)
ax.axvline(9.4346,color=MUTED,lw=1,ls=(0,(2,2))); ax.annotate("ONEI official\nend-2025: 9.43M",(9.4346,2.55),
    color=MUTED,fontsize=8,ha="center",va="top")
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=10)
ax.set_xlabel("Resident population (millions)",fontsize=10); ax.set_xlim(7.0,9.7)
# legend
ax.plot([],[],"o",color=INK2,label="● end-2025 estimate"); ax.plot([],[],"D",color=INK2,label="◆ end-2026 nowcast")
ax.legend(frameon=False,fontsize=9,loc="lower right")
ax.set_title("Three models, and where each puts Cuba by the end of 2026",
             fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Bars = 90% intervals. End-2026 is a nowcast (5 months out) from each model's end-2025 posterior.",fontsize=7.3,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(ARTIFACTS / "chart6_models_nowcast.png"), bbox_inches="tight"); plt.close(fig)

# ---------- Chart 7: analog comparison (cumulative % loss + annual rate) ----------
analogs=[
 ("Syria 2011–20 (war)",50.0,">10",RED),
 ("Venezuela 2013–24",25.0,"1–3",S4),
 ("Zimbabwe 1998–08",25.0,"~2.5",S4),
 ("Cuba 2021–25 · Model C",22.6,"~5.6",RED),
 ("Cuba 2021–25 · Model B",20.4,"~4.1",S2),
 ("Cuba 2021–25 · Model A",16.4,"~3.3",S1),
 ("Puerto Rico 2010–20",11.8,"1.2 (3.9 peak)",S3),
 ("Cuba Special Period 90s",0.5,"~0",MUTED),
]
fig,ax=plt.subplots(figsize=(8.8,5.0),dpi=200); style(ax)
names=[a[0] for a in analogs]; vals=[a[1] for a in analogs]; cols=[a[3] for a in analogs]
yy=np.arange(len(analogs))[::-1]
ax.barh(yy,vals,color=cols,height=0.62)
for i,a in zip(yy,analogs):
    ax.annotate(f"{a[1]:.0f}%  ·  {a[2]} %/yr",(a[1],i),xytext=(6,0),textcoords="offset points",
                va="center",fontsize=8.7,color=INK2)
ax.set_yticks(yy); ax.set_yticklabels(names,fontsize=9.5)
ax.set_xlim(0,58); ax.set_xlabel("Cumulative population loss over the crisis window (%)",fontsize=10)
ax.grid(axis="y",visible=False); ax.grid(axis="x",color=GRID,lw=0.6)
ax.set_title("Cuba's loss in context: fast even by the standards of collapse",
             fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Sources: R4V/UNHCR (Venezuela); US Census/PRB (Puerto Rico); CRS/WHO (Zimbabwe); UN (Syria); CMAJ (Cuba 1990s). Annual rate = cumulative ÷ years.",fontsize=7.0,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(ARTIFACTS / "chart7_analogs.png"), bbox_inches="tight"); plt.close(fig)
print("charts ok")
