from pathlib import Path
import sys
_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS, FIGURES
ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# -*- coding: utf-8 -*-
"""Gráficos de alta calidad (300 dpi) para el infográfico, estilo unificado."""
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
from scipy.stats import norm, beta as beta_dist

INK="#0f1720"; INK2="#3f4a56"; MUTED="#8a938f"; GRID="#e8ebe9"; BASE="#cdd3d0"; SURF="#ffffff"
BLUE="#1f6fd6"; RED="#e23b34"; ORANGE="#ef7a3d"; GREEN="#12a67a"; VIO="#7a3fb0"; NAVY="#12314f"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":1.0,"xtick.color":INK2,"ytick.color":INK2,
 "xtick.labelsize":13,"ytick.labelsize":12,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.9); ax.tick_params(length=0)
def save(fig,name): fig.savefig(str(FIGURES / name) if str(name).startswith(("ig_","f")) else str(ARTIFACTS / name),bbox_inches="tight",dpi=300); plt.close(fig)

# ===== 1. Población real vs oficial =====
fig,ax=plt.subplots(figsize=(7.8,3.7)); style(ax)
oy=[2019,2020,2021,2022,2023,2024,2025]; ov=[11.19,11.18,11.11,11.09,10.06,9.75,9.43]
ey=[2019,2025,2026,2030]; ev=[11.19,8.56,8.27,7.0]
ax.axvspan(2025,2030.5,color=GRID,alpha=0.5,lw=0)
ax.plot(oy,ov,color=BLUE,lw=3.4,marker="o",ms=6,zorder=4)
ax.plot(ey,ev,color=RED,lw=3.6,marker="o",ms=7,zorder=5)
ax.plot([2025,2030],[8.56,7.0],color=RED,lw=3.6,ls=(0,(1.5,1.4)),zorder=5)
ax.annotate("cifra oficial",(2023.9,9.9),color=BLUE,fontsize=13,fontweight="bold",ha="right")
ax.annotate("estimación real",(2022.5,8.95),color=RED,fontsize=13,fontweight="bold",ha="center")
ax.annotate("11,2 M",(2019,11.19),xytext=(0,9),textcoords="offset points",fontsize=12.5,fontweight="bold",ha="center")
ax.annotate("8,6 M",(2025,8.56),xytext=(-6,-16),textcoords="offset points",color=RED,fontsize=12.5,fontweight="bold",ha="right")
ax.annotate("7 M (2030)",(2030,7.0),xytext=(8,0),textcoords="offset points",color=RED,fontsize=12.5,fontweight="bold",va="center")
ax.text(2027.6,10.5,"proyección",color=MUTED,fontsize=12,style="italic",ha="center")
ax.set_xlim(2018.6,2031.2); ax.set_ylim(6.3,11.8); ax.set_xticks(range(2019,2031,2))
ax.set_ylabel("Millones de habitantes",fontsize=13)
save(fig,"ig_poblacion.png")

# ===== 2. Nacimientos vs defunciones =====
fig,ax=plt.subplots(figsize=(7.8,3.6)); style(ax)
yy=list(range(2017,2026)); b=[115.0,116.3,109.7,105.0,99.1,95.4,90.4,71.4,68.1]; d=[106.9,106.2,109.1,112.4,167.6,120.1,117.7,128.1,136.2]
ax.plot(yy,b,color=BLUE,lw=3.4,marker="o",ms=6); ax.plot(yy,d,color=RED,lw=3.4,marker="o",ms=6)
ax.fill_between(yy,b,d,where=(np.array(d)>np.array(b)),color=RED,alpha=0.08)
ax.annotate("NACIMIENTOS",(2017,117),color=BLUE,fontsize=12.5,fontweight="bold",va="bottom")
ax.annotate("DEFUNCIONES",(2017,100),color=RED,fontsize=12.5,fontweight="bold",va="top")
ax.annotate("68 mil",(2025,68.1),xytext=(-2,-4),textcoords="offset points",color=BLUE,fontsize=12,fontweight="bold",ha="right",va="top")
ax.annotate("136 mil",(2025,136.2),xytext=(-2,4),textcoords="offset points",color=RED,fontsize=12,fontweight="bold",ha="right",va="bottom")
ax.set_xlim(2016.6,2025.7); ax.set_ylim(55,180); ax.set_xticks(range(2017,2026,2))
ax.set_ylabel("Miles por año",fontsize=13)
save(fig,"ig_tijera.png")

# ===== 3. Exceso de mortalidad 2024-25 =====
fig,ax=plt.subplots(figsize=(7.8,3.6)); style(ax)
x=np.arange(2); w=0.34; exp=[112.5,113.8]; reg=[128.1,136.2]
ax.bar(x-w/2,exp,w,color="#7fb0e8",label="Esperadas (mortalidad 2019, ya envejecida)")
ax.bar(x+w/2,reg,w,color=RED,label="Registradas")
for xi,v in zip(x-w/2,exp): ax.annotate(f"{v:.0f}",(xi,v),xytext=(0,4),textcoords="offset points",ha="center",fontsize=12,fontweight="bold",color="#2a6bbf")
for xi,v in zip(x+w/2,reg): ax.annotate(f"{v:.0f}",(xi,v),xytext=(0,4),textcoords="offset points",ha="center",fontsize=12,fontweight="bold",color=RED)
for i,(e,r) in enumerate(zip(exp,reg)): ax.annotate(f"+{r-e:.0f} mil",(x[i]+w/2,r),xytext=(30,-4),textcoords="offset points",ha="left",va="top",fontsize=11.5,fontweight="bold",color=INK)
ax.set_xticks(x); ax.set_xticklabels(["2024","2025"],fontsize=13.5); ax.set_ylim(0,155)
ax.set_ylabel("Defunciones (miles)",fontsize=13); ax.set_yticks([0,40,80,120])
ax.legend(frameon=False,fontsize=10.5,loc="upper left")
save(fig,"ig_exceso.png")

# ===== 4. Quién se va / quién se queda =====
fig,ax=plt.subplots(figsize=(7.8,3.6)); style(ax)
bands=["Niños\n(0–14)","Edad de trabajar\ny tener hijos (15–59)","Mayores\n(60+)"]; emig=[15,77,8]; resid=[16,57,27]
x=np.arange(3); w=0.36
ax.bar(x-w/2,emig,w,color=ORANGE,label="Se van"); ax.bar(x+w/2,resid,w,color=BLUE,label="Se quedan")
for xi,v in zip(x-w/2,emig): ax.annotate(f"{v}%",(xi,v),xytext=(0,4),textcoords="offset points",ha="center",fontsize=12,fontweight="bold",color=ORANGE)
for xi,v in zip(x+w/2,resid): ax.annotate(f"{v}%",(xi,v),xytext=(0,4),textcoords="offset points",ha="center",fontsize=12,fontweight="bold",color=BLUE)
ax.set_xticks(x); ax.set_xticklabels(bands,fontsize=11); ax.set_ylim(0,90); ax.set_yticks([0,20,40,60,80])
ax.set_ylabel("% del grupo",fontsize=13); ax.legend(frameon=False,fontsize=11.5,loc="upper right")
save(fig,"ig_edad.png")

# ===== 5. Triangulación =====
fig,ax=plt.subplots(figsize=(7.8,4.2))
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="x",color=GRID,lw=0.9)
rows=[("ONU (no actualiza migración)",10.9,MUTED),("Denominador del MINSAP",10.24,MUTED),
 ("Padrón electoral (nivel)",10.0,MUTED),("ONEI — oficial",9.43,BLUE),
 ("Viviendas × ocupación",8.7,GREEN),("Albizu-Campos (2023)",8.62,ORANGE),
 ("Este estudio (Modelo D)",8.56,RED),("Albizu-Campos (2024)",8.03,ORANGE)]
ax.axvspan(8.0,8.9,color=GREEN,alpha=0.10,lw=0)
y=np.arange(len(rows))[::-1]
for i,(lab,val,col) in zip(y,rows):
    mk="D" if "Modelo D" in lab else "o"
    ax.plot(val,i,mk,color=col,ms=15 if mk=="D" else 12,zorder=4,markeredgecolor="white",markeredgewidth=1.4)
    ax.annotate(f"{val:.2f}",(val,i),xytext=(11,0),textcoords="offset points",va="center",fontsize=11.5,fontweight="bold",color=col if col!=MUTED else INK2)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=11.5)
ax.set_xlim(7.4,11.5); ax.set_xlabel("Población estimada (millones)",fontsize=13)
ax.text(8.45,-1.05,"zona más probable 8,0–8,9 M",color=GREEN,fontsize=11,fontweight="bold",ha="center")
ax.set_ylim(-1.5,len(rows)-0.4)
save(fig,"ig_triangulacion.png")

# ===== 6. Provincias =====
fig,ax=plt.subplots(figsize=(7.8,4.5))
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="x",color=GRID,lw=0.9)
rates=[("La Habana",32.8),("Matanzas",28.2),("Cienfuegos",27.5),("Artemisa",26.8),("Mayabeque",26.1),
 ("Camagüey",25.7),("Sancti Spíritus",25.4),("Villa Clara",25.3),("Santiago de Cuba",22.6),("Pinar del Río",22.4),
 ("Ciego de Ávila",22.3),("Isla de la Juventud",21.4),("Guantánamo",21.0),("Granma",21.0),("Las Tunas",20.3),("Holguín",19.6)]
y=np.arange(len(rates))[::-1]; cols=[RED if r[0]=="La Habana" else BLUE for r in rates]
ax.barh(y,[r[1] for r in rates],color=cols,height=0.68)
for i,r in zip(y,rates): ax.annotate(f"−{r[1]:.0f}",(r[1],i),xytext=(5,0),textcoords="offset points",va="center",fontsize=10.5,fontweight="bold",color=RED if r[0]=="La Habana" else INK2)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rates],fontsize=10.5)
ax.set_xlim(0,37); ax.set_xlabel("Emigración neta 2025 (por 1000 hab.)",fontsize=13)
save(fig,"ig_provincias.png")
print("ig charts ok")
