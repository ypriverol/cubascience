# -*- coding: utf-8 -*-
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt

SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
S1,S2,S3="#2a78d6","#eb6834","#1baf7a"; RED="#e34948"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.8,"xtick.color":MUTED,"ytick.color":MUTED,
 "xtick.labelsize":9.5,"ytick.labelsize":9,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.6); ax.tick_params(length=0)

# Emigration by year: ONEI official net outflow (abs) vs US CBP arrivals (lower bound)
years=[2021,2022,2023,2024]
onei=[0.169,0.991,None,251.221]     # thousands; 2023 lumped into revision (shown separately)
usc=[54.818,313.506,153.630,145.124]
fig,ax=plt.subplots(figsize=(8.8,4.9),dpi=200); style(ax)
w=0.38; x=np.arange(len(years))
# ONEI bars (2021,2022,2024); 2023 drawn hatched as the "lump"
onei_plot=[0.169,0.991,0,251.221]
b1=ax.bar(x-w/2,onei_plot,w,color=S1,label="Saldo migratorio oficial ONEI")
# 2023 lump annotation
ax.bar(x[2]-w/2,0,w,color=S1)
b2=ax.bar(x+w/2,usc,w,color=S2,label="Llegadas de cubanos a EEUU (CBP, solo un destino)")
onei_labels={0:"+169",1:"+991",2:"sin cifra\nanual",3:"−251k"}
for idx,(xi,v) in enumerate(zip(x-w/2,onei_plot)):
    ax.annotate(onei_labels[idx],(xi,v),xytext=(0,6),textcoords="offset points",ha="center",fontsize=8.5,color=S1,fontweight="bold")
for xi,v in zip(x+w/2,usc):
    ax.annotate(f"{v:.0f}k",(xi,v),xytext=(0,5),textcoords="offset points",ha="center",fontsize=8.5,color=S2,fontweight="bold")
# the smoking gun annotation on 2022
ax.annotate("En 2022 la ONEI declaró un saldo\nmigratorio de +991 personas…\n…mientras 313,506 cubanos\nentraban solo a EEUU",
            (x[1]+w/2,313.506),xytext=(x[1]-0.05,255),textcoords="data",fontsize=9,color=INK,ha="center",va="top",
            fontweight="bold")
ax.annotate("todo el éxodo de 2022 se\n'reubicó' en el salto de 2023\n(revisión de −1,006k en un año)",
            (x[2],120),fontsize=8.6,color=RED,ha="center",va="center")
ax.set_xticks(x); ax.set_xticklabels(years); ax.set_ylim(0,340)
ax.set_ylabel("Miles de personas por año",fontsize=10)
ax.legend(frameon=False,fontsize=9,loc="upper right")
ax.set_title("El descuadre de 2022: las cifras oficiales no cuadran",fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"El saldo oficial de 2021–2022 (≈0) es incompatible con las llegadas documentadas a EEUU. La ONEI corrigió el resultado final (2023) sin corregir el camino.",fontsize=7.2,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig("/home/claude/es_9_costura.png",bbox_inches="tight"); plt.close(fig)
print("audit chart ok")
