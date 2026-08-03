from pathlib import Path
import sys
_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS, FIGURES
ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# -*- coding: utf-8 -*-
"""Seis figuras simples para público general. Un mensaje claro por gráfica, letra grande."""
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt

SURF="#ffffff"; INK="#111111"; INK2="#3f3f3f"; MUTED="#8a8a85"; GRID="#e7e6e0"; BASE="#c3c2b7"
BLUE="#2a78d6"; ORANGE="#eb6834"; GREEN="#1baf7a"; RED="#e0392f"; VIO="#7a3fb0"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.9,"xtick.color":INK2,"ytick.color":INK2,
 "xtick.labelsize":11,"ytick.labelsize":10.5,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.7); ax.tick_params(length=0)
def title(ax,t,sub=None):
    ax.set_title(t,fontsize=15.5,fontweight="bold",loc="left",color=INK,pad=(20 if sub else 12))
    if sub: ax.text(0,1.02,sub,transform=ax.transAxes,fontsize=10.5,color=INK2,va="bottom")

# ================= F1: la población se desploma =================
fig,ax=plt.subplots(figsize=(9.2,5.0),dpi=200); style(ax)
oy=[2019,2020,2021,2022,2023,2024,2025]; ov=[11.19,11.18,11.11,11.09,10.06,9.75,9.43]
ey=[2019,2025,2026,2030]; ev=[11.19,8.59,8.29,7.0]
ax.plot(oy,ov,color=BLUE,lw=3,marker="o",ms=6,zorder=4)
ax.plot(ey,ev,color=RED,lw=3,marker="o",ms=7,zorder=5)
ax.plot([2025,2030],[8.59,7.0],color=RED,lw=3,ls=(0,(1.5,1.5)),zorder=5)
ax.axvspan(2025,2030.5,color=GRID,alpha=0.35,lw=0)
ax.annotate("cifra oficial",(2024,9.75),color=BLUE,fontsize=12,fontweight="bold",ha="right",va="bottom")
ax.annotate("9,4 M",(2025,9.43),xytext=(8,2),textcoords="offset points",color=BLUE,fontsize=11,fontweight="bold")
ax.annotate("estimación real\n(este estudio)",(2022.6,8.9),color=RED,fontsize=12,fontweight="bold",ha="center")
ax.annotate("11,2 M",(2019,11.19),xytext=(0,9),textcoords="offset points",color=INK,fontsize=11,fontweight="bold",ha="center")
ax.annotate("8,6 M",(2025,8.59),xytext=(-6,-16),textcoords="offset points",color=RED,fontsize=11,fontweight="bold",ha="right")
ax.annotate("8,3 M\n(2026)",(2026,8.29),xytext=(8,-4),textcoords="offset points",color=RED,fontsize=11,fontweight="bold")
ax.annotate("7 M\n(2030)",(2030,7.0),xytext=(8,0),textcoords="offset points",color=RED,fontsize=11.5,fontweight="bold",va="center")
ax.text(2027.6,10.4,"proyección",color=MUTED,fontsize=11,style="italic",ha="center")
ax.set_xlim(2018.6,2031.2); ax.set_ylim(6.3,11.8); ax.set_xticks(range(2019,2031,2))
ax.set_ylabel("Habitantes (millones)",fontsize=11.5)
title(ax,"Cuba se vacía: casi un cuarto de la población en siete años",
      "De 11,2 millones en 2019 a unos 8,3 en 2026. La cifra oficial va por detrás de la realidad.")
fig.tight_layout(); fig.savefig(str(FIGURES / "f1_poblacion.png"), bbox_inches="tight"); plt.close(fig)

# ================= F2: mueren el doble de los que nacen =================
fig,ax=plt.subplots(figsize=(9.2,4.7),dpi=200); style(ax)
yy=list(range(2017,2026))
b=[114971,116333,109716,105038,99096,95403,90392,71374,68064]
d=[106941,106201,109080,112439,167645,120098,117739,128098,136214]
ax.plot(yy,np.array(b)/1000,color=BLUE,lw=3,marker="o",ms=6)
ax.plot(yy,np.array(d)/1000,color=RED,lw=3,marker="o",ms=6)
ax.fill_between(yy,np.array(b)/1000,np.array(d)/1000,where=(np.array(d)>np.array(b)),color=RED,alpha=0.08)
ax.annotate("NACIMIENTOS",(2017,116),color=BLUE,fontsize=12,fontweight="bold",va="bottom")
ax.annotate("DEFUNCIONES",(2017,100),color=RED,fontsize=12,fontweight="bold",va="top")
ax.annotate("68 mil\nen 2025",(2025,68),xytext=(-4,-2),textcoords="offset points",color=BLUE,fontsize=10.5,fontweight="bold",ha="right",va="top")
ax.annotate("136 mil\nen 2025",(2025,136),xytext=(-4,4),textcoords="offset points",color=RED,fontsize=10.5,fontweight="bold",ha="right",va="bottom")
ax.set_xlim(2016.6,2025.7); ax.set_ylim(55,180); ax.set_xticks(yy)
ax.set_ylabel("Miles por año",fontsize=11.5)
title(ax,"En Cuba mueren casi el doble de los que nacen",
      "Aunque nadie emigrara, el país ya se encogería. En 2025 nacieron menos bebés que en 1899.")
fig.tight_layout(); fig.savefig(str(FIGURES / "f2_tijera.png"), bbox_inches="tight"); plt.close(fig)

# ================= F3: a dónde fue la gente (cascada) =================
fig,ax=plt.subplots(figsize=(9.2,4.8),dpi=200); style(ax)
steps=[("Población\n2019",11.19,"base"),("Se fueron\n(emigración)",-2.00,"neg"),
       ("Muertes de\nmás que nacim.",-0.28,"neg"),("Ajuste de\npadrón",-0.35,"neg"),
       ("Población real\n2025",8.59,"base")]
running=steps[0][1]
for i,(lab,val,kind) in enumerate(steps):
    if kind=="base":
        ax.bar(i,val,color=INK if i==0 else VIO,width=0.62,zorder=3)
        ax.annotate(f"{val:.1f} M",(i,val),xytext=(0,7),textcoords="offset points",ha="center",fontsize=12,fontweight="bold",color=INK if i==0 else VIO)
        running=val
    else:
        ax.bar(i,abs(val),bottom=running+val,color=RED,width=0.62,alpha=0.9,zorder=3)
        ax.annotate(f"−{abs(val):.1f} M" if abs(val)>=0.1 else "",(i,running),xytext=(0,7),textcoords="offset points",ha="center",fontsize=11,fontweight="bold",color=RED)
        ax.plot([i-0.31,i-0.69],[running,running],color=MUTED,lw=0.9,ls=(0,(2,2)))
        running=running+val
ax.plot([len(steps)-1-0.31,len(steps)-2+0.31],[running,running],color=MUTED,lw=0.9,ls=(0,(2,2)))
ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps],fontsize=10)
ax.set_ylim(0,12); ax.set_ylabel("Habitantes (millones)",fontsize=11.5)
ax.set_yticks([0,3,6,9,12])
title(ax,"¿A dónde fueron 2,6 millones de personas?",
      "La mayoría emigró; el resto son muertes y nacimientos que no ocurrieron.")
fig.tight_layout(); fig.savefig(str(FIGURES / "f3_cascada.png"), bbox_inches="tight"); plt.close(fig)

# ================= F4: el país envejece (oficial + nuestro modelo) =================
fig,ax=plt.subplots(figsize=(9.2,4.9),dpi=200); style(ax)
yrs=[2000,2005,2010,2015,2019,2020,2021,2022]; y60=[14.7,15.7,17.8,19.4,20.4,21.3,21.6,22.3]; y014=[20.5,19.0,17.3,16.5,16.0,15.7,15.7,15.6]
py=[2022,2025,2030,2035]; p60=[22.3,26.7,29.4,33.1]; p014=[15.6,15.1,13.8,12.8]
oy=[2019,2025,2030,2035]; om=[20.2,28.0,35.0,40.0]   # nuestro modelo (aprox)
ax.axvspan(2022,2035.6,color=GRID,alpha=0.35,lw=0)
ax.plot(yrs,y60,color=ORANGE,lw=3,marker="o",ms=5); ax.plot(py,p60,color=ORANGE,lw=3,ls=(0,(2,2)))
ax.plot(oy,om,color=RED,lw=3,ls=(0,(1,1.4)),marker="D",ms=6,zorder=5)
ax.plot(yrs,y014,color=BLUE,lw=3,marker="o",ms=5); ax.plot(py,p014,color=BLUE,lw=3,ls=(0,(2,2)))
ax.annotate("MAYORES DE 60\n(cifra oficial)",(2003,16.0),color=ORANGE,fontsize=11,fontweight="bold",va="top")
ax.annotate("33% en 2035",(2035,33.1),color=ORANGE,fontsize=11,fontweight="bold",ha="right",va="top")
ax.annotate("~40% según\nnuestra estimación",(2035,40),color=RED,fontsize=11,fontweight="bold",ha="right",va="bottom")
ax.annotate("NIÑOS (0–14)",(2000,21.3),color=BLUE,fontsize=11.5,fontweight="bold")
ax.annotate("13%",(2035,12.8),color=BLUE,fontsize=11.5,fontweight="bold",ha="right",va="top")
ax.text(2028.5,18.5,"proyección",color=MUTED,fontsize=10.5,style="italic",ha="center")
ax.set_xlim(1999,2036.5); ax.set_ylim(10,42); ax.set_xticks(range(2000,2036,5))
ax.set_ylabel("% de la población",fontsize=11.5)
title(ax,"Un país cada vez más viejo: hacia un tercio (o más) mayor de 60",
      "Como la emigración se lleva sobre todo a jóvenes, bajo nuestra estimación el envejecimiento es aún peor.")
fig.tight_layout(); fig.savefig(str(FIGURES / "f4_envejece.png"), bbox_inches="tight"); plt.close(fig)

# ================= F5: hasta la esperanza de vida baja =================
fig,ax=plt.subplots(figsize=(9.2,4.5),dpi=200); style(ax)
tx=[2002,2006,2012,2015,2019]; tv=[76.99,77.97,78.45,78.07,77.70]
ax.plot(tx,tv,color=BLUE,lw=3,marker="o",ms=6)
ax.plot([2019,2021],[77.70,71.25],color=RED,lw=3,ls=(0,(2,2)),marker="D",ms=8)
ax.annotate("máximo: 78,5 años\n(2011–13)",(2012,78.45),xytext=(0,10),textcoords="offset points",ha="center",fontsize=11,fontweight="bold",color=BLUE)
ax.annotate("77,7\n(2018–20)",(2019,77.70),xytext=(8,-2),textcoords="offset points",fontsize=10.5,color=BLUE,fontweight="bold")
ax.annotate("71 años en 2021\n(estimación independiente)",(2021,71.25),xytext=(-10,6),textcoords="offset points",ha="right",fontsize=11,fontweight="bold",color=RED)
ax.set_xlim(2000,2023.5); ax.set_ylim(70,80); ax.set_xticks(range(2000,2024,5))
ax.set_ylabel("Años de vida al nacer",fontsize=11.5)
title(ax,"Hasta la esperanza de vida retrocede",
      "El logro insignia del sistema cubano cae desde 2013, según los propios datos oficiales.")
fig.tight_layout(); fig.savefig(str(FIGURES / "f5_esperanza.png"), bbox_inches="tight"); plt.close(fig)

# ================= F6: las cifras oficiales no cuadran =================
fig,ax=plt.subplots(figsize=(9.2,4.7),dpi=200); style(ax)
ax.bar([0],[0.991],width=0.5,color=BLUE)
ax.bar([1],[313.5],width=0.5,color=RED)
ax.annotate("+991 personas",(0,0.991),xytext=(0,8),textcoords="offset points",ha="center",fontsize=12,fontweight="bold",color=BLUE)
ax.annotate("313 506\npersonas",(1,313.5),xytext=(0,8),textcoords="offset points",ha="center",fontsize=12,fontweight="bold",color=RED)
ax.set_xticks([0,1]); ax.set_xticklabels(["Saldo migratorio que\ndeclaró el gobierno (2022)","Cubanos que llegaron\nSOLO a EE. UU. (2022)"],fontsize=11)
ax.set_ylim(0,360); ax.set_ylabel("Personas",fontsize=11.5); ax.set_yticks([0,100000/1000*1,200,300])
ax.set_yticklabels(["0","100 mil","200 mil","300 mil"])
title(ax,"Las cifras oficiales no cuadran",
      "En 2022 el gobierno dijo que casi nadie emigró, el mismo año en que un tercio de millón se iba solo a EE. UU.")
fig.tight_layout(); fig.savefig(str(FIGURES / "f6_cifras.png"), bbox_inches="tight"); plt.close(fig)
print("6 figuras listas")
