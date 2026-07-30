from pathlib import Path
import sys
_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS, FIGURES
ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm, beta as beta_dist

SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
S1,S2,S3="#2a78d6","#eb6834","#1baf7a"
SEQ=["#cde2fb","#9ec5f4","#6da7ec","#3987e5","#2a78d6","#1c5cab"]
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.8,"xtick.color":MUTED,"ytick.color":MUTED,
 "xtick.labelsize":9,"ytick.labelsize":9,"figure.facecolor":SURF,"axes.facecolor":SURF,
 "savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.6); ax.tick_params(length=0)

# ---------- Chart 4: Model A vs Model B decline distributions ----------
# recompute Model A
rng=np.random.default_rng(42); N=1_000_000
z=rng.multivariate_normal([0,0],[[1,.5],[.5,1]],size=N); u1,u2=norm.cdf(z[:,0]),norm.cdf(z[:,1])
B=beta_dist.ppf(u1,1.5,3.0); B2=beta_dist.ppf(u2,1.0,3.5)
BIRTHS=529_367; DEATHS=782_233; RMIG=1_516_491
declA=(DEATHS*np.clip(rng.normal(1.015,0.012,N),0.99,1.06)-BIRTHS*rng.normal(1,0.01,N)+RMIG*(1+0.55*B2))/1e6
declB=np.load(str(ARTIFACTS / "modelB_decline.npy"))/1e6

fig,ax=plt.subplots(figsize=(8.6,4.4),dpi=200); style(ax)
bins=np.linspace(1.6,3.0,110)
ax.hist(declA,bins=bins,density=True,color=S1,alpha=0.75,label="Model A · baseline (ONEI-anchored)")
ax.hist(declB,bins=bins,density=True,color=S2,alpha=0.65,label="Model B · crisis-adjusted")
for arr,c,lab,dy in [(declA,S1,"A",0.92),(declB,S2,"B",0.80)]:
    m=np.median(arr); ax.axvline(m,color=c,lw=1.3,ls=(0,(3,2)))
    ax.annotate(f"median {lab}\n{m:.2f}M",(m,ax.get_ylim()[1]*dy),color=c,fontsize=9,
                fontweight="bold",ha="center",va="top")
ax.set_yticks([]); ax.set_xlim(1.6,3.0)
ax.set_xlabel("Total population decline, end-2019 → end-2025 (millions)",fontsize=10)
ax.legend(frameon=False,fontsize=9.5,loc="upper right")
ax.set_title("Two models of the loss: how much you assume is hidden",
             fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Model A anchors on ONEI's revised figures; Model B leans toward independent estimates and adds death under-registration + epidemic excess.",
         fontsize=7.3,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(ARTIFACTS / "chart4_modelAB.png"), bbox_inches="tight"); plt.close(fig)

# ---------- Chart 5: projection fan to 2030 ----------
fan=np.load(str(ARTIFACTS / "fan.npy"), allow_pickle=True).item()
yrs=sorted(fan.keys()); arr=np.array([fan[y] for y in yrs])/1e6  # cols: p5,p25,p50,p75,p95
fig,ax=plt.subplots(figsize=(8.6,4.8),dpi=200); style(ax)
# historical observed (ONEI) up to 2025
hist_y=[2019,2020,2023,2024,2025]; hist_v=[11.193,11.182,10.056,9.748,9.435]
ax.plot(hist_y,hist_v,color=INK,lw=2,marker="o",ms=4,zorder=5,label="ONEI observed")
ax.fill_between(yrs,arr[:,0],arr[:,4],color=SEQ[1],alpha=0.55,lw=0,label="90% projection band")
ax.fill_between(yrs,arr[:,1],arr[:,3],color=SEQ[3],alpha=0.6,lw=0,label="50% band")
ax.plot(yrs,arr[:,2],color=S1,lw=2.2,zorder=4,label="Model B median path")
# markers of endpoints
ax.annotate(f"{arr[-1,2]:.1f}M\n(median 2030)",(2030,arr[-1,2]),color=S1,fontsize=9.5,
            fontweight="bold",ha="left",va="center",xytext=(6,0),textcoords="offset points")
ax.annotate(f"as low as\n{arr[-1,0]:.1f}M",(2030,arr[-1,0]),color=INK2,fontsize=8.5,
            ha="left",va="center",xytext=(6,0),textcoords="offset points")
ax.axvspan(2025,2030.4,color=GRID,alpha=0.25,lw=0)
ax.annotate("projection",(2027.5,11.0),color=MUTED,fontsize=9,ha="center",style="italic")
ax.set_xlim(2018.8,2031.4); ax.set_ylim(5.8,11.6); ax.set_xticks(range(2019,2031,2))
ax.set_ylabel("Population (millions)",fontsize=10)
ax.legend(frameon=False,fontsize=8.8,loc="lower left")
ax.set_title("If current trends hold: Cuba's population to 2030",
             fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Projection starts from Model B's end-2025 estimate; combines declining births, aging-driven deaths, and three emigration regimes.",
         fontsize=7.3,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(ARTIFACTS / "chart5_projection.png"), bbox_inches="tight"); plt.close(fig)
print("ok",arr[-1])
