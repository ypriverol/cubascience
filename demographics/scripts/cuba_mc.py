"""
Monte Carlo interval estimation of Cuba's population decline, end-2019 -> end-2025.

Accounting identity per component (2020..2025):
  P_end2025 = P_end2019 + births - deaths - net_emigration

Data anchors (ONEI vital statistics, as reported):
  births:  2020: 105,038 | 2021: 99,096 | 2022: 95,403 | 2023: 90,392 | 2024: 71,374 | 2025: 68,064
  deaths:  2020: 112,439 | 2021: 167,645 | 2022: 120,098 | 2023: 117,739 | 2024: 128,098 | 2025: 136,214
  ONEI net migration: 2021-2023: -1,005,006 (revision); 2024: -251,221; 2025: -245,264; 2020: ~-15k (borders closed most of year)
  ONEI populations: end-2020 11,181,595 ; end-2023 10,055,968 ; end-2024 9,748,007 ; end-2025 9,434,593
  Official end-2019: 11,193,470
  Albizu-Campos: corrected end-2020 10,557,977 ; end-2023 8,629,906 ; end-2024 8,025,624
    -> implies official baseline overstated by ~620k already at end-2020, and
       migration 2021-2024 ~2.3-2.4M vs ONEI ~1.26M.

Uncertainty model (each draw is one internally-consistent scenario):
 1. Baseline overstatement U0 at end-2019 (people already effectively abroad but still
    counted): 0 under pure-ONEI view; up to ~600k under Albizu view.
    U0 ~ 620,000 * B, with B ~ Beta(2, 3)  (mean ~0.4 -> ~248k; wide support 0-620k)
 2. Registered vital events: births known well (+-1%); deaths: registered total plus
    possible under-registration during 2021 COVID wave and 2024-25 crisis:
    deaths multiplier D ~ Normal(1.02, 0.015), truncated [1.0, 1.08]
    (Economist excess-death model suggests some deaths escaped even the registry,
     though most excess showed up in ONEI's own 2021 total.)
 3. Net emigration 2020-2025: ONEI recorded total R = 15k + 1,005,006 + 251,221 + 245,264
    = 1,516,491. True flow = R * M where M reflects the ONEI-vs-independent dispute.
    M ~ 1 + 0.55 * B2, B2 ~ Beta(1.6, 3.2)  -> M mean ~1.18, 95% range ~[1.01, 1.45]
    (M=1: ONEI revision fully captures flows; M~1.5+: Albizu-type estimate.
     Full Albizu implies M~1.7; we treat that as a low-probability tail because his
     45.5% US-share assumption is itself an estimate, but coverage extends toward it.)
    Correlation: scenarios with high baseline overstatement B also tend to accept
    higher hidden migration -> correlate B and B2 via a Gaussian copula (rho=0.5).
 4. The *decline since 2019* = (deaths - births) + net_emigration_2020_25.
    Note U0 does NOT enter the decline (those people had already left before 2020);
    it enters the percentage denominator: true end-2019 base = 11,193,470 - U0.

Outputs: median + 90% and 95% intervals for absolute decline, % decline,
end-2025 population, and component shares.
"""
import numpy as np

rng = np.random.default_rng(42)
N = 1_000_000

OFFICIAL_2019 = 11_193_470
BIRTHS = 105_038 + 99_096 + 95_403 + 90_392 + 71_374 + 68_064      # 529,367
DEATHS = 112_439 + 167_645 + 120_098 + 117_739 + 128_098 + 136_214  # 782,233
R_MIG = 15_000 + 1_005_006 + 251_221 + 245_264                      # 1,516,491

# correlated latent normals
z = rng.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], size=N)
from scipy.stats import norm, beta as beta_dist
u1, u2 = norm.cdf(z[:, 0]), norm.cdf(z[:, 1])
B  = beta_dist.ppf(u1, 1.5, 3.0)          # baseline overstatement fraction (mode near 0)
B2 = beta_dist.ppf(u2, 1.0, 3.5)          # hidden-migration fraction (density max at 0 = ONEI correct)

U0 = 620_000 * B
M  = 1 + 0.55 * B2

births = BIRTHS * rng.normal(1.0, 0.01, N)
dmult = np.clip(rng.normal(1.015, 0.012, N), 0.99, 1.06)
deaths = DEATHS * dmult
mig = R_MIG * M

natural_decrease = deaths - births
decline = natural_decrease + mig
base_true = OFFICIAL_2019 - U0
pct = 100 * decline / base_true
p2025 = base_true - decline

def summ(x, name, fmt=",.0f"):
    q = np.percentile(x, [2.5, 5, 25, 50, 75, 95, 97.5])
    print(f"{name}: median {q[3]:{fmt}} | 90% CI [{q[1]:{fmt}}, {q[5]:{fmt}}] | 95% CI [{q[0]:{fmt}}, {q[6]:{fmt}}]")

print(f"Registered components: births {BIRTHS:,}, deaths {DEATHS:,}, natural decrease {DEATHS-BIRTHS:,}, ONEI net mig {R_MIG:,}")
summ(decline, "Absolute decline 2019->2025")
summ(pct, "Percent decline", ".1f")
summ(p2025, "Population end-2025")
summ(mig, "Net emigration 2020-25")
summ(natural_decrease, "Natural decrease 2020-25")
summ(base_true, "True end-2019 base")

# share of decline from migration
summ(100 * mig / decline, "Migration share of decline (%)", ".1f")

# sanity checks against anchor scenarios
print("\nAnchors: ONEI-implied decline (M=1, U0=0):", f"{DEATHS-BIRTHS+R_MIG:,}",
      "->", f"{OFFICIAL_2019-(DEATHS-BIRTHS+R_MIG):,}", "end-2025 (ONEI says 9,434,593)")
print("Prob(end-2025 pop < 9,434,593):", np.mean(p2025 < 9_434_593).round(3))
print("Prob(end-2025 pop < 8,500,000):", np.mean(p2025 < 8_500_000).round(3))
print("Prob(decline > 2,000,000):", np.mean(decline > 2_000_000).round(3))

# family anecdote check: P(>=3 deaths in 6 years in a family of ~25)
from scipy.stats import poisson
for fam in (15, 25, 40):
    # avg crude death rate 2020-25 ~ (782,233/6)/10.4M ~ 12.5/1000; family skews older -> use 12.5-18
    for cdr in (0.0125, 0.018):
        lam = fam * cdr * 6
        print(f"family={fam}, cdr={cdr*1000:.1f}/1000: E[deaths/6y]={lam:.2f}, P(>=3)={1-poisson.cdf(2, lam):.2f}")
