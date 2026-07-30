"""
Model B (crisis-adjusted, pessimistic) + forward projection to 2030.

Motivation (from research):
 - In Cuba the FACT of death is historically registered ~99-100%; the 2021 spike
   to 167,645 proves deaths were counted. So dengue/chikungunya/cancer deaths that
   occur ON the island mostly ARE already inside the 782,233 registered deaths
   (2020-25) -- they are just coded to other causes. Cause-misattribution does NOT
   change the population total.
 - BUT three mechanisms can push TRUE deaths above the registered total in 2024-26:
     (a) funeral/cemetery collapse (Santiago, Havana, Matanzas 2024-26) -> burial-
         before-registration, delayed/lost certificates;
     (b) epidemic undercount at the TOTAL level during the 2025 arbovirus wave
         (PAHO: highest chikungunya incidence in the Americas; WHO lab-confirmed
         only ~3%);
     (c) publication lag / suppression of the Anuario.
   Model B therefore widens the death under-registration factor and adds an
   explicit 2024-25 crisis-mortality excess term.
 - Model B also leans the EMIGRATION multiplier toward the independent
   (Albizu-Campos) view, which is where the largest divergence from ONEI lives.

Two cross-checks are used to DISCIPLINE the pessimism so it is not arbitrary:
 1. Life-expectancy cross-check: independent LE ~71-73 (2021), not fully recovered.
    A period LE in the low 70s for an aging population is consistent with crude
    death rates of ~12-15/1000 -- which the registered series already shows
    (2024 CDR 12.9, 2025 ~14.4 on the smaller base). This BOUNDS how much hidden
    death is plausible: if huge numbers were dying unrecorded, the registered CDR
    plus the hidden part would imply an LE far below anything observed. So the
    death under-registration is capped at +14%.
 2. Emigration is bounded above by destination-country administrative data
    (US + Spain + Brazil + Mexico + Uruguay + others), which even summed with
    generous undercount does not exceed ~2.5M for 2021-25.
"""
import numpy as np
from scipy.stats import norm, beta as beta_dist, poisson

rng = np.random.default_rng(7)
N = 1_000_000

OFFICIAL_2019 = 11_193_470
BIRTHS = 105_038 + 99_096 + 95_403 + 90_392 + 71_374 + 68_064      # 529,367
DEATHS_REG = 112_439 + 167_645 + 120_098 + 117_739 + 128_098 + 136_214  # 782,233
R_MIG = 15_000 + 1_005_006 + 251_221 + 245_264                     # 1,516,491

# ---- correlated latent draws: baseline overstatement, migration, mortality ----
cov = np.array([[1, .55, .35],
                [.55, 1, .40],
                [.35, .40, 1]])
z = rng.multivariate_normal([0, 0, 0], cov, size=N)
u = norm.cdf(z)

# (1) baseline already-departed at end-2019: 0..700k, mean ~ 350k (Albizu electoral-roll critique)
B0 = beta_dist.ppf(u[:, 0], 2.2, 2.2)
U0 = 700_000 * B0

# (2) emigration multiplier: mean ~1.34, 95% up to ~1.72 (toward full Albizu ~1.7)
Bmig = beta_dist.ppf(u[:, 1], 2.0, 2.6)
M = 1 + 0.72 * Bmig

# (3) death under-registration factor: 1.00..1.14, mean ~ +5.5%
#     (funeral collapse + epidemic + lag). Capped by the LE cross-check.
Bmort = beta_dist.ppf(u[:, 2], 2.0, 2.8)
Dfac = 1 + 0.14 * Bmort

# (4) explicit epidemic / crisis excess deaths NOT captured even in the adjusted
#     registered series (2024-25): a Poisson-ish extra term, 0..~60k, centered ~25k.
#     Rationale: 2025 arbovirus wave + oncology/dialysis service collapse deaths that
#     slipped registration during the funeral crisis. Kept modest because most such
#     deaths DO get registered eventually.
epi_excess = rng.gamma(shape=3.0, scale=9000, size=N)   # mean 27k, long right tail
epi_excess = np.minimum(epi_excess, 90_000)

births = BIRTHS * rng.normal(1.0, 0.01, N)
deaths = DEATHS_REG * Dfac + epi_excess
mig = R_MIG * M

natural_decrease = deaths - births
decline = natural_decrease + mig
base_true = OFFICIAL_2019 - U0
pct = 100 * decline / base_true
p2025 = base_true - decline

def summ(x, name, fmt=",.0f"):
    q = np.percentile(x, [2.5, 5, 50, 95, 97.5])
    print(f"{name}: median {q[2]:{fmt}} | 90% [{q[1]:{fmt}}, {q[3]:{fmt}}] | 95% [{q[0]:{fmt}}, {q[4]:{fmt}}]")

print("=== MODEL B (crisis-adjusted) : end-2019 -> end-2025 ===")
print(f"Registered deaths anchor {DEATHS_REG:,} | adj deaths median {np.median(deaths):,.0f} "
      f"(implied under-reg {np.median(deaths)/DEATHS_REG-1:+.1%})")
summ(decline, "Total decline")
summ(pct, "Percent decline", ".1f")
summ(p2025, "Population end-2025")
summ(mig, "Net emigration 2020-25")
summ(deaths, "True deaths 2020-25 (adj)")
summ(natural_decrease, "Natural decrease")
summ(100*mig/decline, "Migration share (%)", ".1f")
print("P(pop end-2025 < 8.5M):", round(float(np.mean(p2025 < 8_500_000)), 3))
print("P(pop end-2025 < 8.0M):", round(float(np.mean(p2025 < 8_000_000)), 3))
print("P(decline > 2.5M):", round(float(np.mean(decline > 2_500_000)), 3))

# save posterior for chart
np.save("/home/claude/modelB_decline.npy", decline)
np.save("/home/claude/modelB_pop.npy", p2025)

# ================= FORWARD PROJECTION to 2030 =================
# Start each path from Model B end-2025 population draw (uncertainty carried forward).
# Annual components 2026-2030:
#   births: start 68,064, decline 3%/yr (fewer women of childbearing age) with noise
#   deaths: start ~136,214 registered; on a shrinking+aging base the crude rate rises;
#           model deaths roughly flat-to-slightly-rising in absolute terms as aging
#           offsets the smaller base, plus under-registration/epidemic factor kept.
#   migration: three regimes (border politics uncertain):
#       - "persistent exodus": ~230k/yr (2025 level continues)
#       - "partial closure":   ~120k/yr (US shut, southern routes absorb some)
#       - "escalation":        ~330k/yr (crisis worsens, new routes open)
#     drawn per path with weights.
print("\n=== PROJECTION to end-2030 (Model B base) ===")
P0 = p2025.copy()
regime = rng.choice([0, 1, 2], size=N, p=[0.45, 0.30, 0.25])
mig_lvl = np.select([regime == 0, regime == 1, regime == 2],
                    [230_000, 120_000, 330_000]).astype(float)
pop = P0.copy()
for yr in range(2026, 2031):
    k = yr - 2025
    b = 68_064 * (0.965 ** k) * rng.normal(1.0, 0.03, N)
    d = 136_214 * (1.0 + 0.005 * k) * (1 + 0.10 * beta_dist.ppf(rng.random(N), 2, 3)) * rng.normal(1.0, 0.02, N)
    m = mig_lvl * rng.normal(1.0, 0.18, N)
    pop = pop - (d - b) - m
    q = np.percentile(pop, [5, 50, 95])
    print(f"end-{yr}: median {q[1]/1e6:.2f}M | 90% [{q[0]/1e6:.2f}, {q[2]/1e6:.2f}]M")
np.save("/home/claude/proj_2030.npy", pop)

# store yearly fan for chart
fan = {}
pop = P0.copy()
fan[2025] = np.percentile(P0, [5, 25, 50, 75, 95])
pop2 = P0.copy()
for yr in range(2026, 2031):
    k = yr - 2025
    b = 68_064 * (0.965 ** k) * rng.normal(1.0, 0.03, N)
    d = 136_214 * (1.0 + 0.005 * k) * (1 + 0.10 * beta_dist.ppf(rng.random(N), 2, 3)) * rng.normal(1.0, 0.02, N)
    m = mig_lvl * rng.normal(1.0, 0.18, N)
    pop2 = pop2 - (d - b) - m
    fan[yr] = np.percentile(pop2, [5, 25, 50, 75, 95])
np.save("/home/claude/fan.npy", fan, allow_pickle=True)

# ================= family-death Bayesian angle =================
print("\n=== Family signal: does '3 deaths in 6 years' imply hidden mortality? ===")
# If observed deaths in a family exceed Poisson expectation under the OFFICIAL CDR,
# that is (weak) evidence for a higher true CDR. Show the likelihood ratio.
fam = 25
for cdr_label, cdr in [("official-ish 12.5/1000", 0.0125),
                       ("aging-family 16/1000", 0.016),
                       ("crisis 20/1000", 0.020)]:
    lam = fam * cdr * 6
    print(f"  fam={fam}, {cdr_label}: E={lam:.2f}, P(>=3)={1-poisson.cdf(2, lam):.2f}, P(exactly 3)={poisson.pmf(3, lam):.2f}")
