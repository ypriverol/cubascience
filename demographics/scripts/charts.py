import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm, beta as beta_dist

# ---- palette (dataviz reference, light mode) ----
SURF = "#fcfcfb"; PAGE = "#f9f9f7"
INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"
GRID = "#e1e0d9"; BASE = "#c3c2b7"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"   # blue, orange, aqua
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6", "#1c5cab"]

mpl.rcParams.update({
    "font.family": "DejaVu Sans", "text.color": INK,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2, "axes.linewidth": 0.8,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
})

def style_ax(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.grid(axis="x", visible=False)
    ax.tick_params(length=0)

# ================= Chart 1: population series =================
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=200)
style_ax(ax)

un_y   = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
un_v   = [11.20, 11.176, 11.11, 11.06, 11.02, 10.98, 10.94]
onei_y = [2019, 2020, 2023, 2024, 2025]
onei_v = [11.193, 11.182, 10.056, 9.748, 9.435]
alb_y  = [2020, 2021, 2023, 2024]
alb_v  = [10.558, 10.480, 8.630, 8.026]

ax.plot(un_y, un_v, color=S3, lw=2, marker="o", ms=5, zorder=3)
ax.plot(onei_y[:2], onei_v[:2], color=S1, lw=2, marker="o", ms=5, zorder=4)
ax.plot(onei_y[1:], onei_v[1:], color=S1, lw=2, ls=(0, (4, 2)), marker="o", ms=5, zorder=4)
ax.plot(alb_y, alb_v, color=S2, lw=2, ls=(0, (4, 2)), marker="o", ms=5, zorder=4)

# this analysis: end-2025 median + 90% CI
ax.errorbar([2025.35], [9.056], yerr=[[9.056-8.577], [9.339-9.056]], fmt="D",
            color=INK, ecolor=INK, elinewidth=2, capsize=5, ms=7, zorder=5)

ax.annotate("UN WPP 2024\n(migration not updated)", (2022.1, 11.14), color=S3,
            fontsize=9.5, fontweight="bold", ha="left", va="bottom")
ax.annotate("ONEI (official,\nrevised 2024)", (2022.35, 10.42), color=S1,
            fontsize=9.5, fontweight="bold", ha="left")
ax.annotate("Albizu-Campos\n(independent)", (2021.7, 8.85), color=S2,
            fontsize=9.5, fontweight="bold", ha="left")
ax.annotate("This analysis,\nend-2025:\n9.06M\n[8.6–9.3M] 90% CI", (2025.5, 9.02), color=INK,
            fontsize=9, fontweight="bold", ha="left", va="center")

for x, v in zip(onei_y, onei_v):
    ax.annotate(f"{v:.2f}", (x, v), textcoords="offset points", xytext=(0, 8),
                fontsize=8.5, color=INK2, ha="center")
for x, v in zip(alb_y, alb_v):
    ax.annotate(f"{v:.2f}", (x, v), textcoords="offset points", xytext=(0, -14),
                fontsize=8.5, color=INK2, ha="center")

ax.set_xlim(2018.6, 2027.2); ax.set_ylim(7.6, 11.7)
ax.set_xticks(range(2019, 2026))
ax.set_ylabel("Population (millions, end of year)", fontsize=10)
ax.set_title("Three versions of Cuba's population, 2019–2025",
             fontsize=13, fontweight="bold", loc="left", color=INK, pad=14)
fig.text(0.005, 0.012, "Sources: ONEI; Albizu-Campos (2024, 2025); UN World Population Prospects 2024. Dashed = series revised or estimated, not annually observed.",
         fontsize=7.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("/home/claude/chart1_population_series.png", bbox_inches="tight")
plt.close(fig)

# ================= Chart 2: births vs deaths =================
fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=200)
style_ax(ax)
years = list(range(2017, 2026))
births = [114971, 116333, 109716, 105038, 99096, 95403, 90392, 71374, 68064]
deaths = [106941, 106201, 109080, 112439, 167645, 120098, 117739, 128098, 136214]

ax.plot(years, np.array(births)/1000, color=S1, lw=2, marker="o", ms=5)
ax.plot(years, np.array(deaths)/1000, color=S2, lw=2, marker="o", ms=5)
ax.annotate("Births", (2017, 119), color=S1, fontsize=10.5, fontweight="bold")
ax.annotate("Deaths", (2017, 100), color=S2, fontsize=10.5, fontweight="bold")
ax.annotate("COVID wave\n167,645 deaths", (2021, 169), color=INK2, fontsize=9,
            ha="center", va="bottom")
ax.annotate("68,064 — fewest births\nsince at least 1899", (2025.15, 64), color=INK2,
            fontsize=9, ha="right", va="top")
ax.annotate("136,214", (2025, 139), color=INK2, fontsize=8.5, ha="center")
ax.set_xlim(2016.6, 2025.6); ax.set_ylim(55, 185)
ax.set_xticks(years)
ax.set_ylabel("Thousands per year", fontsize=10)
ax.set_title("The scissors: deaths now double births",
             fontsize=13, fontweight="bold", loc="left", color=INK, pad=14)
fig.text(0.005, 0.012, "Source: ONEI vital statistics (registered events), 2017–2025.",
         fontsize=7.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("/home/claude/chart2_births_deaths.png", bbox_inches="tight")
plt.close(fig)

# ================= Chart 3: Monte Carlo posterior =================
rng = np.random.default_rng(42)
N = 1_000_000
z = rng.multivariate_normal([0, 0], [[1, .5], [.5, 1]], size=N)
u1, u2 = norm.cdf(z[:, 0]), norm.cdf(z[:, 1])
B = beta_dist.ppf(u1, 1.5, 3.0); B2 = beta_dist.ppf(u2, 1.0, 3.5)
BIRTHS = 529_367; DEATHS = 782_233; R_MIG = 1_516_491
births_s = BIRTHS * rng.normal(1.0, 0.01, N)
deaths_s = DEATHS * np.clip(rng.normal(1.015, 0.012, N), 0.99, 1.06)
mig = R_MIG * (1 + 0.55 * B2)
decline = (deaths_s - births_s + mig) / 1e6

q5, q50, q95 = np.percentile(decline, [5, 50, 95])
fig, ax = plt.subplots(figsize=(8.6, 4.2), dpi=200)
style_ax(ax)
counts, edges = np.histogram(decline, bins=90, range=(1.7, 2.6), density=True)
centers = (edges[:-1] + edges[1:]) / 2
in_ci = (centers >= q5) & (centers <= q95)
ax.bar(centers[~in_ci], counts[~in_ci], width=(edges[1]-edges[0])*0.92, color=SEQ[1])
ax.bar(centers[in_ci], counts[in_ci], width=(edges[1]-edges[0])*0.92, color=SEQ[4])
ax.axvline(q50, color=INK, lw=1.4, ls=(0, (3, 2)))
ax.annotate(f"median\n{q50:.2f}M", (q50 + 0.015, ax.get_ylim()[1]*0.93), color=INK,
            fontsize=9.5, fontweight="bold", va="top")
ax.annotate(f"90% interval: {q5:.2f}M – {q95:.2f}M", (2.58, ax.get_ylim()[1]*0.6),
            color=SEQ[5], fontsize=10, fontweight="bold", ha="right")
ax.annotate("ONEI-consistent\nscenarios", xy=(1.79, ax.get_ylim()[1]*0.42),
            xytext=(1.73, ax.get_ylim()[1]*0.72), color=INK2, fontsize=9, ha="center",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.set_xlim(1.66, 2.62)
ax.annotate("higher hidden\nemigration\n(toward Albizu-Campos)", (2.38, ax.get_ylim()[1]*0.25),
            color=INK2, fontsize=9, ha="center")
ax.set_yticks([])
ax.set_xlabel("Total population decline, end-2019 → end-2025 (millions)", fontsize=10)
ax.set_title("Monte Carlo estimate of Cuba's population loss since 2019",
             fontsize=13, fontweight="bold", loc="left", color=INK, pad=14)
fig.text(0.005, 0.012, "1,000,000 simulations combining registered vital statistics with uncertainty in emigration undercount and death registration.",
         fontsize=7.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("/home/claude/chart3_posterior.png", bbox_inches="tight")
plt.close(fig)
print("done", q5, q50, q95)
