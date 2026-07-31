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

SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
S1,S2,S3="#2a78d6","#eb6834","#1baf7a"; S4="#eda100"; RED="#e34948"; SEQ=["#cde2fb","#9ec5f4","#6da7ec","#3987e5","#2a78d6","#1c5cab"]
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.8,"xtick.color":MUTED,"ytick.color":MUTED,
 "xtick.labelsize":9,"ytick.labelsize":9,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.6); ax.tick_params(length=0)

# ===== 1. series de poblacion =====
fig,ax=plt.subplots(figsize=(8.6,5.0),dpi=200); style(ax)
un_y=[2019,2020,2021,2022,2023,2024,2025]; un_v=[11.20,11.176,11.11,11.06,11.02,10.98,10.94]
onei_y=[2019,2020,2023,2024,2025]; onei_v=[11.193,11.182,10.056,9.748,9.435]
alb_y=[2020,2021,2023,2024]; alb_v=[10.558,10.480,8.630,8.026]
ax.plot(un_y,un_v,color=S3,lw=2,marker="o",ms=5,zorder=3)
ax.plot(onei_y[:2],onei_v[:2],color=S1,lw=2,marker="o",ms=5,zorder=4)
ax.plot(onei_y[1:],onei_v[1:],color=S1,lw=2,ls=(0,(4,2)),marker="o",ms=5,zorder=4)
ax.plot(alb_y,alb_v,color=S2,lw=2,ls=(0,(4,2)),marker="o",ms=5,zorder=4)
ax.errorbar([2025.35],[8.24],yerr=[[8.24-7.62],[8.89-8.24]],fmt="D",color=INK,ecolor=INK,elinewidth=2,capsize=5,ms=7,zorder=5)
ax.annotate("ONU (WPP 2024)\nno actualiza migración",(2021.9,11.15),color=S3,fontsize=9.5,fontweight="bold",ha="left",va="bottom")
ax.annotate("ONEI (oficial,\nrevisado 2024)",(2022.35,10.42),color=S1,fontsize=9.5,fontweight="bold",ha="left")
ax.annotate("Albizu-Campos\n(independiente)",(2021.7,8.85),color=S2,fontsize=9.5,fontweight="bold",ha="left")
ax.annotate("Este análisis\n(Modelo C),\nfin-2025: 8.24M",(2025.5,8.2),color=INK,fontsize=8.5,fontweight="bold",ha="left",va="center")
for x,v in zip(onei_y,onei_v): ax.annotate(f"{v:.2f}",(x,v),textcoords="offset points",xytext=(0,8),fontsize=8.5,color=INK2,ha="center")
for x,v in zip(alb_y,alb_v): ax.annotate(f"{v:.2f}",(x,v),textcoords="offset points",xytext=(0,-14),fontsize=8.5,color=INK2,ha="center")
ax.set_xlim(2018.6,2027.2); ax.set_ylim(7.6,11.7); ax.set_xticks(range(2019,2026))
ax.set_ylabel("Población (millones, fin de año)",fontsize=10)
ax.set_title("Tres versiones de la población de Cuba, 2021–2026",fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Fuentes: ONEI; Albizu-Campos (2024, 2025); ONU WPP 2024. Línea discontinua = serie revisada o estimada, no observada anualmente.",fontsize=7.3,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(FIGURES / "es_1_series.png"), bbox_inches="tight"); plt.close(fig)

# ===== 2. tijera nacimientos/defunciones =====
fig,ax=plt.subplots(figsize=(8.6,4.6),dpi=200); style(ax)
years=list(range(2017,2026))
births=[114971,116333,109716,105038,99096,95403,90392,71374,68064]
deaths=[106941,106201,109080,112439,167645,120098,117739,128098,136214]
ax.plot(years,np.array(births)/1000,color=S1,lw=2,marker="o",ms=5)
ax.plot(years,np.array(deaths)/1000,color=S2,lw=2,marker="o",ms=5)
ax.annotate("Nacimientos",(2017,119),color=S1,fontsize=10.5,fontweight="bold")
ax.annotate("Defunciones",(2017,99),color=S2,fontsize=10.5,fontweight="bold")
ax.annotate("ola COVID\n167,645 muertes",(2021,169),color=INK2,fontsize=9,ha="center",va="bottom")
ax.annotate("68,064 — menos que\nen 1899",(2025.15,64),color=INK2,fontsize=9,ha="right",va="top")
ax.set_xlim(2016.6,2025.6); ax.set_ylim(55,185); ax.set_xticks(years)
ax.set_ylabel("Miles por año",fontsize=10)
ax.set_title("La tijera: las muertes ya duplican a los nacimientos",fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Fuente: ONEI, estadísticas vitales (hechos registrados), 2017–2025.",fontsize=7.3,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(FIGURES / "es_2_tijera.png"), bbox_inches="tight"); plt.close(fig)

# ===== 3. tres modelos + nowcast 2026 =====
def qs(a): return np.percentile(a,[5,50,95])/1e6
popB25=np.load(str(ARTIFACTS / "modelB_pop.npy")); popC25=np.load(str(ARTIFACTS / "modelC_pop.npy"))
popB26=np.load(str(ARTIFACTS / "modelB_pop2026.npy")); popC26=np.load(str(ARTIFACTS / "modelC_pop2026.npy"))
rows=[("Modelo A · ancla ONEI",np.array([8.58,9.06,9.34]),np.array([8.27,8.76,9.07]),S1),
      ("Modelo B · ajuste crisis",qs(popB25),qs(popB26),S2),
      ("Modelo C · peor caso",qs(popC25),qs(popC26),RED)]
fig,ax=plt.subplots(figsize=(8.8,4.6),dpi=200); style(ax)
y=np.arange(len(rows))[::-1]
for i,(name,e25,e26,c) in zip(y,rows):
    ax.plot([e25[0],e25[2]],[i+0.13]*2,color=c,lw=2.4,solid_capstyle="round",alpha=0.5)
    ax.plot(e25[1],i+0.13,"o",color=c,ms=9,zorder=4)
    ax.plot([e26[0],e26[2]],[i-0.13]*2,color=c,lw=2.4,solid_capstyle="round",alpha=0.5)
    ax.plot(e26[1],i-0.13,"D",color=c,ms=8,zorder=4)
    ax.annotate(f"{e25[1]:.2f}M",(e25[1],i+0.13),xytext=(0,9),textcoords="offset points",ha="center",fontsize=9,fontweight="bold",color=c)
    ax.annotate(f"{e26[1]:.2f}M",(e26[1],i-0.13),xytext=(0,-15),textcoords="offset points",ha="center",fontsize=9,fontweight="bold",color=c)
ax.axvline(9.4346,color=MUTED,lw=1,ls=(0,(2,2))); ax.annotate("ONEI oficial\nfin-2025: 9.43M",(9.4346,2.58),color=MUTED,fontsize=8,ha="center",va="top")
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=10)
ax.set_xlabel("Población residente (millones)",fontsize=10); ax.set_xlim(7.0,9.75)
ax.plot([],[],"o",color=INK2,label="● estimación fin-2025"); ax.plot([],[],"D",color=INK2,label="◆ proyección fin-2026")
ax.legend(frameon=False,fontsize=9,loc="lower right")
ax.set_title("Tres modelos y dónde queda Cuba a fines de 2026",fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Barras = intervalos del 90%. Fin-2026 es una proyección a 5 meses desde la distribución de cada modelo para fin-2025.",fontsize=7.3,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(FIGURES / "es_3_modelos.png"), bbox_inches="tight"); plt.close(fig)

# ===== 4. analogos =====
analogs=[("Siria 2011–20 (guerra)",50.0,">10",RED),("Venezuela 2013–24",25.0,"1–3",S4),
 ("Zimbabue 1998–08",25.0,"~2.5",S4),("Cuba 2021–25 · Modelo C",22.6,"~5.6",RED),
 ("Cuba 2021–25 · Modelo B",20.4,"~4.1",S2),("Cuba 2021–25 · Modelo A",16.4,"~3.3",S1),
 ("Puerto Rico 2010–20",11.8,"1.2 (pico 3.9)",S3),("Cuba Período Especial 90s",0.5,"~0",MUTED)]
fig,ax=plt.subplots(figsize=(8.8,5.0),dpi=200); style(ax)
yy=np.arange(len(analogs))[::-1]
ax.barh(yy,[a[1] for a in analogs],color=[a[3] for a in analogs],height=0.62)
for i,a in zip(yy,analogs): ax.annotate(f"{a[1]:.0f}%  ·  {a[2]} %/año",(a[1],i),xytext=(6,0),textcoords="offset points",va="center",fontsize=8.6,color=INK2)
ax.set_yticks(yy); ax.set_yticklabels([a[0] for a in analogs],fontsize=9.5)
ax.set_xlim(0,60); ax.set_xlabel("Pérdida acumulada de población en el período de crisis (%)",fontsize=10)
ax.grid(axis="y",visible=False); ax.grid(axis="x",color=GRID,lw=0.6)
ax.set_title("La pérdida de Cuba en contexto: rápida incluso para un colapso",fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Fuentes: R4V/ACNUR (Venezuela); Censo EEUU/PRB (Puerto Rico); CRS/OMS (Zimbabue); ONU (Siria); CMAJ (Cuba 90s). Tasa anual = acumulada ÷ años.",fontsize=6.9,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(FIGURES / "es_4_analogos.png"), bbox_inches="tight"); plt.close(fig)

# ===== 5. proyeccion a 2030 (desde Modelo C) =====
rng=np.random.default_rng(11); N=len(popC25)
P0=popC25.copy(); regime=rng.choice([0,1,2],size=N,p=[0.45,0.30,0.25])
mig_lvl=np.select([regime==0,regime==1,regime==2],[210_000,120_000,300_000]).astype(float)
fan={2025:np.percentile(P0,[5,25,50,75,95])}
pop=P0.copy()
for yr in range(2026,2031):
    k=yr-2025
    b=68_064*(0.965**k)*rng.normal(1,0.03,N)
    d=136_214*(1+0.006*k)*(1+0.12*beta_dist.ppf(rng.random(N),2,3))*rng.normal(1,0.02,N)
    m=mig_lvl*rng.normal(1,0.18,N)
    pop=pop-(d-b)-m; fan[yr]=np.percentile(pop,[5,25,50,75,95])
yrs=sorted(fan); arr=np.array([fan[y] for y in yrs])/1e6
fig,ax=plt.subplots(figsize=(8.6,4.8),dpi=200); style(ax)
ax.plot([2019,2020,2023,2024,2025],[11.193,11.182,10.056,9.748,9.435],color=INK,lw=2,marker="o",ms=4,zorder=5,label="ONEI observado")
ax.fill_between(yrs,arr[:,0],arr[:,4],color=SEQ[1],alpha=0.55,lw=0,label="banda 90%")
ax.fill_between(yrs,arr[:,1],arr[:,3],color=SEQ[3],alpha=0.6,lw=0,label="banda 50%")
ax.plot(yrs,arr[:,2],color=RED,lw=2.2,zorder=4,label="trayectoria mediana (Modelo C)")
ax.annotate(f"{arr[-1,2]:.1f}M\n(mediana 2030)",(2030,arr[-1,2]),color=RED,fontsize=9.5,fontweight="bold",ha="left",va="center",xytext=(6,0),textcoords="offset points")
ax.annotate(f"hasta\n{arr[-1,0]:.1f}M",(2030,arr[-1,0]),color=INK2,fontsize=8.5,ha="left",va="center",xytext=(6,0),textcoords="offset points")
ax.axvspan(2025,2030.4,color=GRID,alpha=0.25,lw=0); ax.annotate("proyección",(2027.5,10.9),color=MUTED,fontsize=9,ha="center",style="italic")
ax.set_xlim(2018.8,2031.4); ax.set_ylim(5.4,11.6); ax.set_xticks(range(2019,2031,2))
ax.set_ylabel("Población (millones)",fontsize=10)
ax.legend(frameon=False,fontsize=8.8,loc="lower left")
ax.set_title("Si las tendencias continúan: Cuba hacia 2030",fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Proyección desde la estimación fin-2025 del Modelo C; combina nacimientos en caída, muertes por envejecimiento y tres regímenes de emigración.",fontsize=7.0,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(str(FIGURES / "es_5_proyeccion.png"), bbox_inches="tight"); plt.close(fig)
print("charts es ok", arr[-1])
