# -*- coding: utf-8 -*-
import matplotlib as mpl, matplotlib.pyplot as plt, numpy as np
SURF="#ffffff"; INK="#111111"; INK2="#3f3f3f"; MUTED="#8a8a85"; GRID="#e7e6e0"; BASE="#c3c2b7"
BLUE="#2a78d6"; ORANGE="#eb6834"; GREEN="#1baf7a"; RED="#e0392f"; GREY="#b0b0aa"
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.9,"xtick.color":INK2,"ytick.color":INK2,
 "xtick.labelsize":11,"ytick.labelsize":11,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})

# asentados (miles), 2020-2025
dest=[("Estados Unidos",800,BLUE),("España",135,ORANGE),("Uruguay",35,GREEN),
      ("Otros (Rep. Dom.,\nGuyana, Rusia…)",45,GREY),("Rep. Dominicana",15,GREY),
      ("Brasil (asentados)",10,GREY),("México (asentados)",8,GREY)]
# ordenar desc
dest=sorted(dest,key=lambda x:-x[1])
fig,ax=plt.subplots(figsize=(9.4,5.0),dpi=200)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="x",color=GRID,lw=0.7)
y=np.arange(len(dest))[::-1]
ax.barh(y,[d[1] for d in dest],color=[d[2] for d in dest],height=0.66)
for i,d in zip(y,dest):
    ax.annotate(f"{d[1]:,}".replace(","," ")+" mil" if d[1]>=100 else f"{d[1]} mil",
                (d[1],i),xytext=(8,0),textcoords="offset points",va="center",fontsize=11,fontweight="bold",color=d[2] if d[2]!=GREY else INK2)
ax.set_yticks(y); ax.set_yticklabels([d[0] for d in dest],fontsize=10.8)
ax.set_xlim(0,900); ax.set_xlabel("Cubanos asentados 2020–2025 (miles)",fontsize=11.5)
ax.set_xticks([0,200,400,600,800]); ax.set_xticklabels(["0","200 mil","400 mil","600 mil","800 mil"])
ax.set_title("A dónde se fueron: el destino confirma el éxodo",fontsize=15,fontweight="bold",loc="left",color=INK,pad=34)
ax.text(0,1.055,"Sumando solo a quienes se asentaron (sin doble contar el tránsito): ~1,05 millones. EE. UU. es 8 de cada 10.",
        transform=ax.transAxes,fontsize=10.3,color=INK2,va="bottom")
ax.text(895,-1.35,"No sumados (tránsito hacia EE. UU., ya contados allí): México ~100 mil · Honduras · puente aéreo de Nicaragua ~100 mil (2023)",
        fontsize=8.5,color=MUTED,ha="right",style="italic")
ax.set_ylim(-1.7,len(dest)-0.3)
fig.tight_layout(); fig.savefig("/home/claude/f8_destinos.png",bbox_inches="tight"); plt.close(fig)

# cross-check: distintas estimaciones de la EMIGRACIÓN neta 2020-2025
fig,ax=plt.subplots(figsize=(9.4,3.4),dpi=200)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(length=0); ax.grid(axis="x",color=GRID,lw=0.7)
est=[("Libro mayor por destino\n(asentados, mínimo)",1.05,GREEN),
     ("ONEI (saldo neto oficial)",1.52,BLUE),
     ("Este estudio · Modelo D",2.00,RED),
     ("Albizu-Campos",1.80,ORANGE)]
y=np.arange(len(est))[::-1]
ax.barh(y,[e[1] for e in est],color=[e[2] for e in est],height=0.6)
for i,e in zip(y,est):
    ax.annotate(f"{e[1]:.2f} M",(e[1],i),xytext=(7,0),textcoords="offset points",va="center",fontsize=11,fontweight="bold",color=e[2])
ax.axvspan(1.0,1.6,color=GREEN,alpha=0.07,lw=0)
ax.set_yticks(y); ax.set_yticklabels([e[0] for e in est],fontsize=10.2)
ax.set_xlim(0,2.4); ax.set_xlabel("Emigración neta estimada 2020–2025 (millones)",fontsize=11)
ax.set_title("¿Cuántos emigraron? El destino ancla el piso, los modelos el techo",fontsize=13.5,fontweight="bold",loc="left",color=INK,pad=12)
fig.tight_layout(); fig.savefig("/home/claude/f8b_cruce.png",bbox_inches="tight"); plt.close(fig)
print("destinos listos")
