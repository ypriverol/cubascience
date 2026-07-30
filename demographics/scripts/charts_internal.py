from pathlib import Path
import sys
_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS, FIGURES
ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# -*- coding: utf-8 -*-
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt

SURF="#ffffff"; INK="#111111"; INK2="#444444"; MUTED="#7a7a75"; GRID="#e4e3dd"; BASE="#c3c2b7"
S1,S2,S3="#2a78d6","#eb6834","#1baf7a"; S4="#eda100"; RED="#e34948"; VIO="#7a3fb0"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.8,"xtick.color":MUTED,"ytick.color":MUTED,
 "xtick.labelsize":9,"ytick.labelsize":9,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.6); ax.tick_params(length=0)

# ===== Fig A: motor interno - decrecimiento natural acelerándose =====
obs={2019:636,2020:-7401,2021:-68549,2022:-24705,2023:-27354,2024:-56724,2025:-68150}
proj={2026:-71350,2027:-74471,2028:-77516,2029:-80489,2030:-83392}
fig,ax=plt.subplots(figsize=(9.0,4.5),dpi=200); style(ax)
xs=list(obs); vs=[obs[y]/1000 for y in xs]
ax.bar(xs,vs,color=[S3 if v>0 else (RED if y in(2021,) else S1) for y,v in zip(xs,[obs[y] for y in xs])],width=0.66)
px=list(proj); pv=[proj[y]/1000 for y in px]
ax.bar(px,pv,color=S1,width=0.66,alpha=0.42)
ax.axhline(0,color=BASE,lw=1)
ax.annotate("pico por COVID (2021)",xy=(2021,-34),xytext=(2021,14),textcoords="data",fontsize=8.6,color=RED,ha="center",
            fontweight="bold",arrowprops=dict(arrowstyle="-",color=RED,lw=0.8))
ax.annotate("2025: mismo nivel que 2021,\npero sin pandemia — ya es estructural",xy=(2025,-40),xytext=(2025.2,17),
            textcoords="data",fontsize=8.6,color=INK,ha="center",fontweight="bold",
            arrowprops=dict(arrowstyle="-",color=INK2,lw=0.8))
ax.annotate("proyección",(2028,-30),textcoords="data",fontsize=8.5,color=MUTED,ha="center",style="italic")
ax.axvspan(2025.5,2030.5,color=GRID,alpha=0.3,lw=0)
for y in xs:
    ax.annotate(f"{obs[y]/1000:+.0f}k" if abs(obs[y])>1500 else "+0.6k",(y,obs[y]/1000),
                xytext=(0,-12 if obs[y]<0 else 6),textcoords="offset points",ha="center",fontsize=7.8,color=INK2)
ax.set_xticks(list(xs)+list(px)); ax.set_ylim(-95,24)
ax.set_ylabel("Crecimiento natural: nacimientos − defunciones (miles)",fontsize=9.5)
ax.set_title("El motor interno: el decrecimiento natural se acelera",fontsize=13,fontweight="bold",loc="left",color=INK,pad=12)
fig.text(0.005,0.012,"De +636 personas en 2019 a −68 150 en 2025. Aun sin emigración, Cuba se contraería: mueren el doble de los que nacen. Fuente: ONEI.",fontsize=7.3,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(ARTIFACTS / "ms_natural.png"), bbox_inches="tight"); plt.close(fig)

# ===== Fig B: envejecimiento con proyección oficial a 2035 =====
struct={2000:(20.5,14.7),2005:(19.0,15.7),2010:(17.3,17.8),2015:(16.5,19.4),2019:(16.0,20.4),
        2020:(15.7,21.3),2021:(15.7,21.6),2022:(15.6,22.3)}
projs={2025:(15.1,25.0),2030:(13.8,29.4),2035:(12.8,33.1)}
yrs=sorted(struct); y014=[struct[y][0] for y in yrs]; y60=[struct[y][1] for y in yrs]
pyr=[2022]+sorted(projs); p014=[struct[2022][0]]+[projs[y][0] for y in sorted(projs)]; p60=[struct[2022][1]]+[projs[y][1] for y in sorted(projs)]
fig,ax=plt.subplots(figsize=(9.0,4.6),dpi=200); style(ax)
ax.axvspan(2022,2035.5,color=GRID,alpha=0.3,lw=0)
ax.plot(yrs,y60,color=S2,lw=2.4,marker="o",ms=5); ax.plot(pyr,p60,color=S2,lw=2.2,ls=(0,(4,2)))
ax.plot(yrs,y014,color=S1,lw=2.4,marker="o",ms=5); ax.plot(pyr,p014,color=S1,lw=2.2,ls=(0,(4,2)))
ax.annotate("60 años y más",(2000,15.5),color=S2,fontsize=10,fontweight="bold",va="top")
ax.annotate("33.1%\n(2035)",(2035,33.1),color=S2,fontsize=9,fontweight="bold",ha="right",va="bottom")
ax.annotate("0–14 años",(2000,22.5),color=S1,fontsize=10,fontweight="bold")
ax.annotate("12.8%\n(2035)",(2035,12.8),color=S1,fontsize=9,fontweight="bold",ha="right",va="top")
ax.annotate("proyección oficial ONEI",(2028.5,20),color=MUTED,fontsize=8.5,ha="center",style="italic")
ax.annotate("un tercio del país\nmayor de 60 en 2035",(2032,30),color=INK2,fontsize=8.3,ha="center")
ax.set_xlim(1999,2036); ax.set_ylim(10,35); ax.set_ylabel("% de la población",fontsize=10)
ax.set_title("Implosión desde dentro: la estructura por edades, 2000–2035",fontsize=12.5,fontweight="bold",loc="left",color=INK,pad=12)
fig.text(0.005,0.012,"La proyección oficial a 2035 ya se queda corta: la ONEI reportó 26.7% de 60+ a fin de 2025, por encima del 25% proyectado. Fuente: ONEI (tabla 3.12).",fontsize=7.1,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(ARTIFACTS / "ms_aging.png"), bbox_inches="tight"); plt.close(fig)

# ===== Fig C: esperanza de vida oficial (declive) + independiente =====
tri=[("2001–03",2002,76.997),("2005–07",2006,77.97),("2011–13",2012,78.45),("2014–16",2015,78.068),("2018–20",2019,77.70)]
fig,ax=plt.subplots(figsize=(9.0,4.2),dpi=200); style(ax)
tx=[t[1] for t in tri]; tv=[t[2] for t in tri]
ax.plot(tx,tv,color=S1,lw=2.4,marker="o",ms=6,zorder=4)
ax.plot([2019,2021],[77.70,71.25],color=RED,lw=2,ls=(0,(3,2)),marker="D",ms=7,zorder=5)
ax.annotate("máximo oficial\n78.45 (2011–13)",(2012,78.45),xytext=(0,8),textcoords="offset points",ha="center",fontsize=8.5,color=S1,fontweight="bold")
ax.annotate("77.70\n(2018–20)",(2019,77.70),xytext=(6,-4),textcoords="offset points",ha="left",fontsize=8.5,color=S1)
ax.annotate("71.25 (2021)\nestimación independiente\n(Albizu-Campos)",(2021,71.25),xytext=(-8,4),textcoords="offset points",ha="right",fontsize=8.5,color=RED,fontweight="bold")
ax.set_xlim(2000,2023); ax.set_ylim(70,79.5); ax.set_ylabel("Esperanza de vida al nacer (años)",fontsize=10)
ax.set_title("La esperanza de vida ya caía en los datos oficiales",fontsize=12.5,fontweight="bold",loc="left",color=INK,pad=12)
fig.text(0.005,0.012,"Serie oficial por trienios (azul): máximo en 2011–13, en descenso desde entonces. La estimación independiente para 2021 (rojo) marca el desplome de la crisis. Fuente: ONEI (tabla 3.17); Albizu-Campos.",fontsize=7.0,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(ARTIFACTS / "ms_life_exp.png"), bbox_inches="tight"); plt.close(fig)

# ===== regenerar análogos SIN Puerto Rico =====
analogs=[("Siria 2011–20 (guerra)",50.0,">10",RED),("Venezuela 2013–24",25.0,"1–3",S4),
 ("Zimbabue 1998–08",25.0,"~2.5",S4),("Cuba 2019–25 · Modelo C",23.5,"3.9",RED),
 ("Cuba 2019–25 · Modelo D ★",21.3,"3.5",VIO),("Cuba 2019–25 · Modelo A",17.6,"2.9",S1),
 ("Cuba Período Especial 90s",0.5,"~0",MUTED)]
fig,ax=plt.subplots(figsize=(9.0,4.5),dpi=200); style(ax)
yy=np.arange(len(analogs))[::-1]
ax.barh(yy,[a[1] for a in analogs],color=[a[3] for a in analogs],height=0.6)
for i,a in zip(yy,analogs): ax.annotate(f"{a[1]:.0f}%  ·  {a[2]} %/año",(a[1],i),xytext=(6,0),textcoords="offset points",va="center",fontsize=8.6,color=INK2)
ax.set_yticks(yy); ax.set_yticklabels([a[0] for a in analogs],fontsize=9.5)
ax.set_xlim(0,60); ax.set_xlabel("Pérdida acumulada de población en el período de crisis (%)",fontsize=10)
ax.grid(axis="y",visible=False); ax.grid(axis="x",color=GRID,lw=0.6)
ax.set_title("La pérdida de Cuba en contexto comparado",fontsize=13,fontweight="bold",loc="left",color=INK,pad=12)
fig.text(0.005,0.012,"Fuentes: R4V/ACNUR (Venezuela); CRS/OMS (Zimbabue); ONU (Siria); CMAJ (Cuba 90s). Tasa anual = acumulada ÷ años.",fontsize=7.1,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(FIGURES / "es_4_analogos_noPR.png"), bbox_inches="tight"); plt.close(fig)
print("internal figs ok")
