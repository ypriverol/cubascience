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
BLUE="#2a78d6"; ORANGE="#eb6834"; GREEN="#1baf7a"; RED="#e0392f"; VIO="#7a3fb0"; GREY="#9a9a94"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.9,"xtick.color":INK2,"ytick.color":INK2,
 "xtick.labelsize":11,"ytick.labelsize":10.5,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})

# estimaciones (etiqueta, valor M, año, grupo, color)
# grupo: 0 = registros no depurados (techos)  1 = oficial  2 = ajustadas/flujos
rows=[
 ("ONU (WPP 2024) — no actualiza migración", 10.9, 0, GREY),
 ("Denominador del MINSAP (tasas de salud)", 10.24, 0, GREY),
 ("Padrón electoral — nivel (no depurado)", 10.0, 0, GREY),
 ("ONEI — cifra oficial", 9.43, 1, BLUE),
 ("Viviendas × ocupación (~2,2)", 8.7, 2, GREEN),
 ("Albizu-Campos (2023)", 8.62, 2, ORANGE),
 ("Este estudio · Modelo D (2025)", 8.59, 2, RED),
 ("Albizu-Campos (2024)", 8.03, 2, ORANGE),
]
fig,ax=plt.subplots(figsize=(9.4,5.2),dpi=200)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="x",color=GRID,lw=0.7)
# banda "zona más probable"
ax.axvspan(8.0,8.9,color=GREEN,alpha=0.08,lw=0)
y=np.arange(len(rows))[::-1]
for i,(lab,val,grp,col) in zip(y,rows):
    ax.plot([0,val],[i,i],color=col,lw=1.2,alpha=0.25)
    mk="D" if "Modelo D" in lab else "o"
    ax.plot(val,i,mk,color=col,ms=14 if mk=="D" else 11,zorder=4,
            markeredgecolor="white",markeredgewidth=1.2)
    ax.annotate(f"{val:.2f}",(val,i),xytext=(11,0),textcoords="offset points",va="center",
                fontsize=10.5,fontweight="bold",color=col)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=10.2)
ax.set_xlim(7.4,11.4); ax.set_xlabel("Población estimada (millones)",fontsize=11.5)
# corchetes de grupo
ax.annotate("Registros que NO depuran\nemigrantes → techos",(11.15,6.5),fontsize=9.5,color=GREY,
            fontweight="bold",ha="right",va="center")
ax.annotate("Estimaciones ajustadas\ny basadas en flujos",(9.0,1.0),fontsize=9.5,color=INK2,
            fontweight="bold",ha="left",va="center")
ax.text(8.45,-1.15,"zona más probable  8,0–8,9 M",color=GREEN,fontsize=9.5,fontweight="bold",ha="center")
ax.set_title("Cuántos cubanos quedan: seis formas de estimarlo",fontsize=15,fontweight="bold",loc="left",color=INK,pad=34)
ax.text(0,1.055,"Las fuentes que no borran a los que se fueron dan cifras altas; las que sí lo corrigen convergen en ~8,5 millones.",
        transform=ax.transAxes,fontsize=10.3,color=INK2,va="bottom")
ax.set_ylim(-1.6,len(rows)-0.4)
fig.tight_layout(); fig.savefig(str(FIGURES / "f7_triangulacion.png"), bbox_inches="tight"); plt.close(fig)
print("triangulacion lista")

