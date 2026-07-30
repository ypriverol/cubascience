# -*- coding: utf-8 -*-
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt

SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; MUTED="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
S1,S2,S3="#2a78d6","#eb6834","#1baf7a"; S4="#eda100"; RED="#e34948"; SEQ=["#cde2fb","#9ec5f4","#6da7ec","#3987e5","#2a78d6","#1c5cab"]
mpl.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.edgecolor":BASE,
 "axes.labelcolor":INK2,"axes.linewidth":0.8,"xtick.color":MUTED,"ytick.color":MUTED,
 "xtick.labelsize":9,"ytick.labelsize":9,"figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF})
def style(ax):
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=GRID,lw=0.6); ax.tick_params(length=0)

# ===== 6. panel centinela: IMR y TBM indexados a 2019=100 =====
yrs=[2019,2020,2021,2022,2023,2024,2025]
imr={2019:5.0,2020:5.0,2021:7.6,2022:7.5,2023:7.1,2024:7.1,2025:9.9}
cdr={2019:9.7,2020:10.1,2021:15.0,2022:10.8,2023:11.1,2024:12.9,2025:14.2}
imr_i=[imr[y]/imr[2019]*100 for y in yrs]; cdr_i=[cdr[y]/cdr[2019]*100 for y in yrs]
fig,ax=plt.subplots(figsize=(8.6,4.9),dpi=200); style(ax)
ax.axhline(100,color=BASE,lw=1)
ax.plot(yrs,imr_i,color=S2,lw=2.4,marker="o",ms=6,zorder=4)
ax.plot(yrs,cdr_i,color=S1,lw=2.4,marker="o",ms=6,zorder=4)
ax.annotate("Mortalidad infantil\n(+98% vs 2019)",(2025,198),color=S2,fontsize=9.5,fontweight="bold",ha="right",va="bottom")
ax.annotate("Tasa bruta de\nmortalidad (+46%)",(2025,146),color=S1,fontsize=9.5,fontweight="bold",ha="right",va="top")
ax.annotate("nivel 2019",(2019.05,101),color=MUTED,fontsize=8,va="bottom")
for y in [2021,2024,2025]:
    ax.annotate(f"{imr_i[yrs.index(y)]:.0f}",(y,imr_i[yrs.index(y)]),xytext=(0,7),textcoords="offset points",ha="center",fontsize=8,color=INK2)
ax.set_xlim(2018.7,2025.5); ax.set_ylim(90,215); ax.set_xticks(yrs)
ax.set_ylabel("Índice (2019 = 100)",fontsize=10)
ax.set_title("Indicadores de alerta temprana: se deterioran al unísono",fontsize=13,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.05,"La mortalidad infantil —métrica que Cuba sí registra con rigor— predice un alza de mortalidad general de ~30% (elasticidad 0.3,",fontsize=7.4,color=MUTED)
fig.text(0.005,0.012,"calibrada con Venezuela). La TBM registrada subió +33% a 2024: la señal de alerta y las muertes registradas coinciden. Fuente: ONEI/MINSAP.",fontsize=7.4,color=MUTED)
fig.tight_layout(rect=(0,0.055,1,1)); fig.savefig("/home/claude/es_6_centinela.png",bbox_inches="tight"); plt.close(fig)

# ===== 7. exceso de mortalidad por año =====
excess={2020:2993,2021:57124,2022:12190,2023:14339,2024:27823,2025:38142}
fig,ax=plt.subplots(figsize=(8.6,4.5),dpi=200); style(ax)
xs=list(excess); vs=[excess[y]/1000 for y in xs]
cols=[S1 if y!=2021 else RED for y in xs]
ax.bar(xs,vs,color=cols,width=0.62)
for y,v in zip(xs,vs): ax.annotate(f"+{v:.0f}k",(y,v),xytext=(0,5),textcoords="offset points",ha="center",fontsize=9,fontweight="bold",color=INK2)
ax.annotate("ola COVID\n(subdeclarada como\n~8,500 muertes)",(2021,57),xytext=(2021.4,50),textcoords="data",fontsize=8.5,color=RED,ha="left",va="top")
ax.annotate("repunte de crisis:\napagones, epidemias,\nsistema de salud roto",(2024.5,33),fontsize=8.5,color=INK2,ha="center",va="bottom")
ax.set_xlim(2019.4,2025.6); ax.set_ylim(0,66); ax.set_xticks(xs)
ax.set_ylabel("Muertes en exceso vs escenario sin crisis (miles)",fontsize=9.5)
ax.set_title("~153,000 muertes en exceso, 2020–2025 (casi todas registradas)",fontsize=12.5,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"Exceso = muertes registradas por la ONEI menos las esperadas si la mortalidad de 2019 (ajustada por envejecimiento) hubiera continuado.",fontsize=7.2,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig("/home/claude/es_7_exceso.png",bbox_inches="tight"); plt.close(fig)

# ===== 8. cuatro modelos + nowcast 2026 (añade Modelo D) =====
def qs(a): return np.percentile(a,[5,50,95])/1e6
popB=np.load("/home/claude/modelB_pop.npy"); popC=np.load("/home/claude/modelC_pop.npy"); popD=np.load("/home/claude/modelD_pop.npy")
popB26=np.load("/home/claude/modelB_pop2026.npy"); popC26=np.load("/home/claude/modelC_pop2026.npy"); popD26=np.load("/home/claude/modelD_pop2026.npy")
rows=[("Modelo A · ancla ONEI",np.array([8.58,9.06,9.34]),np.array([8.27,8.76,9.07]),S1),
      ("Modelo D · centinela ★",qs(popD),qs(popD26),"#7a3fb0"),
      ("Modelo B · ajuste crisis",qs(popB),qs(popB26),S2),
      ("Modelo C · peor caso",qs(popC),qs(popC26),RED)]
fig,ax=plt.subplots(figsize=(8.8,4.9),dpi=200); style(ax)
y=np.arange(len(rows))[::-1]
for i,(name,e25,e26,c) in zip(y,rows):
    ax.plot([e25[0],e25[2]],[i+0.13]*2,color=c,lw=2.4,solid_capstyle="round",alpha=0.5)
    ax.plot(e25[1],i+0.13,"o",color=c,ms=9,zorder=4)
    ax.plot([e26[0],e26[2]],[i-0.13]*2,color=c,lw=2.4,solid_capstyle="round",alpha=0.5)
    ax.plot(e26[1],i-0.13,"D",color=c,ms=8,zorder=4)
    ax.annotate(f"{e25[1]:.2f}M",(e25[1],i+0.13),xytext=(0,9),textcoords="offset points",ha="center",fontsize=8.8,fontweight="bold",color=c)
    ax.annotate(f"{e26[1]:.2f}M",(e26[1],i-0.13),xytext=(0,-15),textcoords="offset points",ha="center",fontsize=8.8,fontweight="bold",color=c)
ax.axvline(9.4346,color=MUTED,lw=1,ls=(0,(2,2))); ax.annotate("ONEI oficial\nfin-2025: 9.43M",(9.4346,3.55),color=MUTED,fontsize=8,ha="center",va="top")
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=10)
ax.set_xlabel("Población residente (millones)",fontsize=10); ax.set_xlim(7.0,9.75)
ax.plot([],[],"o",color=INK2,label="● estimación fin-2025"); ax.plot([],[],"D",color=INK2,label="◆ proyección fin-2026")
ax.legend(frameon=False,fontsize=9,loc="lower right")
ax.set_title("Cuatro modelos: el centinela (D) converge con el ajuste por crisis (B)",fontsize=12.5,fontweight="bold",loc="left",color=INK,pad=14)
fig.text(0.005,0.012,"★ Modelo D reemplaza los multiplicadores arbitrarios de mortalidad por una estimación anclada en indicadores centinela. Barras = IC 90%.",fontsize=7.2,color=MUTED)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig("/home/claude/es_8_modelos4.png",bbox_inches="tight"); plt.close(fig)
print("charts d ok")
