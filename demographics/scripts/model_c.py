"""
Model C (worst-case, analog-calibrated) + end-2026 NOWCAST + analog comparison.

The analog research disciplines the pessimism with hard numbers. Peak *annual*
population-loss rates actually observed in comparable non-war collapses:
  - Puerto Rico 2017->2018 (Maria): -3.9%/yr  (hard census number; US-adjacent
    emigration surge + disaster mortality pulse) -> the best single analog.
  - Venezuela peak: ~1-3%/yr sustained, ~25% lost over a decade, ~almost all
    emigration; excess mortality a secondary elderly-concentrated pulse.
  - Zimbabwe: ~25% over a decade, mostly emigration.
  - Syria (war outlier, upper bound): >10%/yr displacement at peak.
Cuba's OWN recent pace (ONEI): 2024 -3.1%, 2025 -3.3%. So Cuba is ALREADY running
at Puerto-Rico-post-Maria speed, every year, for four years. That is the key
finding: Cuba is not below the analogs -- it is at or beyond the worst non-war
analog, sustained. This both (a) makes a very pessimistic reading credible and
(b) caps it: nothing non-war has sustained >4%/yr for years.

Mortality calibration from analogs:
  - Sustained crisis raised general mortality ~20% (Venezuela, Cuba-elderly 1990s).
  - Acute infrastructure/disaster pulses: +22% (Maria 6-month), +28% (NYC blackout).
  - BUT Cuba's registered deaths ALREADY embed most of this (2021 +49%; 2024-25
    elevated). So Model C adds an elderly-concentrated UNREGISTERED pulse on top,
    calibrated so total excess vs a no-crisis counterfactual stays within the
    analog envelope, not beyond it.

Model C priors (vs Model B): push emigration toward full Albizu, widen death
under-registration to the analog ceiling, add explicit blackout/epidemic pulse.
"""
from pathlib import Path
import sys
_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
from constants import ARTIFACTS, FIGURES
ARTIFACTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


import numpy as np
from scipy.stats import norm, beta as beta_dist

rng = np.random.default_rng(2026)
N = 1_000_000

OFFICIAL_2019 = 11_193_470
BIRTHS = 105_038 + 99_096 + 95_403 + 90_392 + 71_374 + 68_064      # 529,367
DEATHS_REG = 112_439 + 167_645 + 120_098 + 117_739 + 128_098 + 136_214  # 782,233
R_MIG = 15_000 + 1_005_006 + 251_221 + 245_264                     # 1,516,491

cov = np.array([[1,.55,.40],[.55,1,.45],[.40,.45,1]])
z = rng.multivariate_normal([0,0,0], cov, size=N); u = norm.cdf(z)

# baseline overstatement 0..760k, mean high (~430k) -- full electoral-roll critique
U0 = 760_000 * beta_dist.ppf(u[:,0], 2.4, 1.9)
# emigration multiplier: mean ~1.45, up to ~1.78 (full Albizu ~1.7-1.8)
M = 1 + 0.80 * beta_dist.ppf(u[:,1], 2.4, 2.2)
# death under-registration to analog ceiling: 1.02..1.18 mean ~ +8.5%
Dfac = 1.02 + 0.16 * beta_dist.ppf(u[:,2], 2.2, 2.4)
# explicit unregistered blackout/epidemic elderly pulse 2024-25: 10k..120k, mean ~48k
pulse = np.minimum(rng.gamma(3.2, 15000, N), 140_000)

births = BIRTHS * rng.normal(1.0, 0.01, N)
deaths = DEATHS_REG * Dfac + pulse
mig = R_MIG * M
decline = (deaths - births) + mig
base = OFFICIAL_2019 - U0
p2025 = base - decline
pct = 100*decline/base

def S(x,n,f=",.0f"):
    q=np.percentile(x,[2.5,5,50,95,97.5])
    print(f"{n}: median {q[2]:{f}} | 90% [{q[1]:{f}}, {q[3]:{f}}] | 95% [{q[0]:{f}}, {q[4]:{f}}]")

print("=== MODEL C (worst-case, analog-calibrated) end-2019->end-2025 ===")
print(f"adj deaths median {np.median(deaths):,.0f} (under-reg {np.median(deaths)/DEATHS_REG-1:+.1%})")
S(decline,"Total decline"); S(pct,"Percent decline",".1f"); S(p2025,"Pop end-2025")
S(mig,"Net emigration 2020-25"); S(100*mig/decline,"Migration share %",".1f")
# implied peak annual loss rate check vs analogs
print("implied avg annual loss rate 2020-25:", round(float(np.median(pct))/6,2),
      "%/yr (Puerto Rico Maria peak was -3.9%/yr single year)")
print("P(pop end-2025 < 8.0M):", round(float(np.mean(p2025<8_000_000)),3))
print("P(pop end-2025 < 7.5M):", round(float(np.mean(p2025<7_500_000)),3))

# ================= END-2026 NOWCAST (all three models) =================
# 2026 annual components (Jan-Dec 2026):
#  births ~ 68064*0.965 = 65,682 (continued ~3.5% decline)
#  deaths: registered 2025 136,214; 2026 crisis worse (blackouts all year, infant
#          mortality 9.9/1000, epidemics, food) -> base 139-146k + model's under-reg
#  migration 2026: US shut, Spain Nieto window closed Oct 2025, southern routes
#          partly absorb -> regimes: 150k / 210k / 300k (weights 0.35/0.35/0.30)
def nowcast_2026(p2025_draws, dfac_draws, mig_center):
    b = 65_682 * rng.normal(1.0, 0.03, N)
    d = (142_000 * rng.normal(1.0, 0.03, N)) * np.clip(dfac_draws/np.mean(dfac_draws),0.9,1.15)
    reg = rng.choice([0,1,2], size=N, p=[0.35,0.35,0.30])
    m = np.select([reg==0,reg==1,reg==2],[150_000,210_000,300_000]).astype(float)*rng.normal(1,0.15,N)
    return p2025_draws - (d-b) - m

print("\n=== END-2026 NOWCAST (from each model's end-2025 posterior) ===")
# reconstruct A and B end-2025 posteriors quickly
def modelA_pop():
    z2=rng.multivariate_normal([0,0],[[1,.5],[.5,1]],size=N); u1,u2=norm.cdf(z2[:,0]),norm.cdf(z2[:,1])
    B2=beta_dist.ppf(u2,1.0,3.5); B0=beta_dist.ppf(u1,1.5,3.0)
    dA=DEATHS_REG*np.clip(rng.normal(1.015,0.012,N),0.99,1.06)
    return (OFFICIAL_2019-620_000*B0) - ((dA-BIRTHS*rng.normal(1,0.01,N))+R_MIG*(1+0.55*B2)), np.full(N,1.02)
popA_2025, dfacA = modelA_pop()
popB_2025 = np.load(str(ARTIFACTS / "modelB_pop.npy"))
dfacB = np.clip(rng.normal(1.055,0.03,N),1.0,1.14)

for name,p25,df in [("Model A (ONEI)",popA_2025,dfacA),
                    ("Model B (crisis-adj)",popB_2025,df:=dfacB),
                    ("Model C (worst-case)",p2025,Dfac)]:
    p26 = nowcast_2026(p25, df, None)
    q=np.percentile(p26,[5,50,95]); q25=np.percentile(p25,[50])
    print(f"{name}: end-2025 {q25[0]/1e6:.2f}M -> end-2026 median {q[1]/1e6:.2f}M | 90% [{q[0]/1e6:.2f},{q[2]/1e6:.2f}]M "
          f"| loss in 2026 ~{(q25[0]-q[1])/1e3:.0f}k")

# save Model C for charts
np.save(str(ARTIFACTS / "modelC_decline.npy"),  decline)
np.save(str(ARTIFACTS / "modelC_pop.npy"),  p2025)
np.save(str(ARTIFACTS / "modelC_pop2026.npy"),  nowcast_2026(p2025, Dfac, None))
np.save(str(ARTIFACTS / "modelB_pop2026.npy"),  nowcast_2026(popB_2025, dfacB, None))

# ================= ANALOG COMPARISON (cumulative % loss over the crisis window) =================
print("\n=== ANALOG: cumulative population loss (context) ===")
analogs = {
 "Cuba 2019-25 (Model A)": 17.6,
 "Cuba 2019-25 (Model B)": 21.3,
 "Cuba 2019-25 (Model C)": float(np.median(pct)),
 "Venezuela 2013-24": 25.0,
 "Puerto Rico 2010-20": 11.8,
 "Zimbabwe 1998-08": 25.0,
 "Syria 2011-20 (war)": 50.0,
 "Cuba Special Period 90s": 0.5,
}
for k,v in analogs.items(): print(f"  {k}: {v:.1f}%")
np.save(str(ARTIFACTS / "analogs.npy"),  analogs, allow_pickle=True)
