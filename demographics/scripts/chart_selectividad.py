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
BLUE="#2a78d6"; ORANGE="#eb6834"; RED="#e0392f"; GREEN="#1baf7a"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.9,"xtick.color":INK2,"ytick.color":INK2,
 "xtick.labelsize":11.5,"ytick.labelsize":10.5,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})

# ---- F7: se van los jóvenes, se quedan los viejos ----
fig,ax=plt.subplots(figsize=(9.2,4.7),dpi=200)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="y",color=GRID,lw=0.7)
bands=["Niños\n(0–14)","Edad de trabajar\ny de tener hijos (15–59)","Mayores\n(60+)"]
emig=[15,77,8]; resid=[16,57,27]
x=np.arange(3); w=0.36
ax.bar(x-w/2,emig,w,color=ORANGE,label="Los que se van (emigrantes)")
ax.bar(x+w/2,resid,w,color=BLUE,label="Los que se quedan (residentes)")
for xi,v in zip(x-w/2,emig): ax.annotate(f"{v}%",(xi,v),xytext=(0,4),textcoords="offset points",ha="center",fontsize=11,fontweight="bold",color=ORANGE)
for xi,v in zip(x+w/2,resid): ax.annotate(f"{v}%",(xi,v),xytext=(0,4),textcoords="offset points",ha="center",fontsize=11,fontweight="bold",color=BLUE)
ax.set_xticks(x); ax.set_xticklabels(bands,fontsize=10.5); ax.set_ylim(0,90)
ax.set_ylabel("% del grupo",fontsize=11.5); ax.set_yticks([0,20,40,60,80])
ax.legend(frameon=False,fontsize=10.5,loc="upper right")
ax.set_title("Se van los jóvenes, se quedan los viejos",fontsize=15,fontweight="bold",loc="left",color=INK,pad=30)
ax.text(0,1.045,"El 77% de quienes emigran tienen 15–59 años; entre los que se quedan, 1 de cada 4 supera los 60. Edad mediana: se van ~30, se quedan 45.",
        transform=ax.transAxes,fontsize=10,color=INK2,va="bottom")
fig.tight_layout(); fig.savefig(str(FIGURES / "f10_edad.png"), bbox_inches="tight"); plt.close(fig)

# ---- F8: provincias ----
rates=[("La Habana",32.8),("Matanzas",28.2),("Cienfuegos",27.5),("Artemisa",26.8),("Mayabeque",26.1),
 ("Camagüey",25.7),("Sancti Spíritus",25.4),("Villa Clara",25.3),("Santiago de Cuba",22.6),("Pinar del Río",22.4),
 ("Ciego de Ávila",22.3),("Isla de la Juventud",21.4),("Guantánamo",21.0),("Granma",21.0),("Las Tunas",20.3),("Holguín",19.6)]
fig,ax=plt.subplots(figsize=(9.2,5.4),dpi=200)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="x",color=GRID,lw=0.7)
y=np.arange(len(rates))[::-1]
cols=[RED if r[0]=="La Habana" else BLUE for r in rates]
ax.barh(y,[r[1] for r in rates],color=cols,height=0.66)
for i,r in zip(y,rates): ax.annotate(f"−{r[1]:.1f}",(r[1],i),xytext=(6,0),textcoords="offset points",va="center",fontsize=9.8,fontweight="bold",color=RED if r[0]=="La Habana" else INK2)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rates],fontsize=10)
ax.set_xlim(0,37); ax.set_xlabel("Emigración neta en 2025 (por cada 1000 habitantes)",fontsize=11)
ax.set_title("El vaciamiento es nacional; la capital va primero",fontsize=15,fontweight="bold",loc="left",color=INK,pad=30)
ax.text(0,1.03,"Todas las provincias pierden ~2% de su gente al año; La Habana y el occidente, más rápido que el oriente. Fuente: ONEI 2025.",
        transform=ax.transAxes,fontsize=10,color=INK2,va="bottom")
fig.tight_layout(); fig.savefig(str(FIGURES / "f11_provincias.png"), bbox_inches="tight"); plt.close(fig)
print("figuras selectividad listas")
