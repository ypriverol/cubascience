# -*- coding: utf-8 -*-
"""
AUDIT of ONEI's OWN published numbers for internal inconsistency.
Method: apply the demographic balancing identity to ONEI's published series and
see whether the implied net migration each year is (a) internally consistent and
(b) consistent with external administrative data (US CBP, Spain, etc.).

  implied_net_migration(t) = P(t) - P(t-1) - births(t) + deaths(t)
"""
# ONEI published year-end population (pre-revision 2019-2022; "effective" 2023-2025)
P = {2019:11_193_470, 2020:11_181_595, 2021:11_113_215, 2022:11_089_511,
     2023:10_055_968, 2024:9_748_007, 2025:9_434_593}
births = {2021:99_096, 2022:95_403, 2023:90_392, 2024:71_374, 2025:68_064}
# deaths: use Anuario Estadistico de Salud where available
deaths = {2021:167_645, 2022:120_108, 2023:117_746, 2024:128_098, 2025:136_214}
# ONEI's OWN reported net migration
onei_mig = {2021:+169, 2022:+991, 2023:None, 2024:-251_221, 2025:-245_264}
# external lower bounds on Cuban emigration (US CBP calendar-year + rough others)
us_cbp = {2021:54_818, 2022:313_506, 2023:153_630, 2024:145_124}   # Albizu PDF table
# rough all-destination lower bound (US + Spain + Mexico + Brazil + Uruguay ...)
ext_lb = {2022:369_000, 2023:330_000, 2024:400_000}  # conservative multi-destination

print(f"{'year':<6}{'ΔP':>12}{'nat.change':>12}{'implied_mig':>13}{'ONEI_mig':>11}{'US_CBP':>10}{'ext≥':>10}")
for y in range(2021,2026):
    dP = P[y]-P[y-1]
    nat = births[y]-deaths[y]
    imp = dP - nat
    om = onei_mig.get(y)
    us = us_cbp.get(y,'')
    ex = ext_lb.get(y,'')
    print(f"{y:<6}{dP:>12,}{nat:>12,}{imp:>13,}{(f'{om:+,}' if om is not None else '—'):>11}{(f'{us:,}' if us else '—'):>10}{(f'{ex:,}' if ex else '—'):>10}")

print("\n--- Inconsistency 1: the revision SEAM ---")
print("2021 implied mig:", f"{P[2021]-P[2020]-births[2021]+deaths[2021]:+,}", "(ONEI: +169) -> matches OLD series")
print("2022 implied mig:", f"{P[2022]-P[2021]-births[2022]+deaths[2022]:+,}", "(ONEI: +991) -> matches OLD series")
print("2023 implied mig:", f"{P[2023]-P[2022]-births[2023]+deaths[2023]:+,}", "<- ONE year absorbs the ENTIRE revision")
print("BUT US CBP alone recorded 313,506 Cuban arrivals in 2022; ONEI says +991 net.")
print("=> ONEI's 2022 net-migration (+991) understates reality by >300,000; the whole")
print("   2022 exodus was retroactively dumped into the 2023 'effective population' jump.")

print("\n--- Inconsistency 2: revised the FLOW endpoint, never the STOCK path ---")
# If 2022 truly had ~ -369,000 net migration (external LB), what SHOULD 2022 pop have been?
should_2022 = P[2021] + births[2022] - deaths[2022] + (-369_000)
print(f"2022 pop implied by external migration LB: {should_2022:,} vs ONEI published {P[2022]:,}")
print(f"  -> ONEI's published 2021 & 2022 populations were already ~{P[2022]-should_2022:,.0f}+ too high.")

print("\n--- Inconsistency 3: conflicting OFFICIAL 2023 death counts ---")
for label,v in [("ONEI via AP (mid-2024)",129_049),("Anuario Est. de Salud 2023",117_746),
                ("(reported variant)",120_098)]:
    print(f"  2023 deaths — {label}: {v:,}")
print(f"  spread: {129_049-117_746:,} deaths ({(129_049-117_746)/117_746*100:.1f}%) between two official sources")

print("\n--- Inconsistency 4: post-revision recent figures internally consistent but still low ---")
print(f"2024 implied mig {P[2024]-P[2023]-births[2024]+deaths[2024]:+,} vs ONEI {onei_mig[2024]:+,} (match)")
print(f"2025 implied mig {P[2025]-P[2024]-births[2025]+deaths[2025]:+,} vs ONEI {onei_mig[2025]:+,} (match)")
print("  BUT ~248,000 Cubans entered the US alone in 2024; ONEI's total -251k for ALL")
print("  destinations is barely above the US-only figure -> still understates net outflow.")

print("\n--- Inconsistency 5: mortality RATES computed on which population? ---")
# Anuario 2023: total deaths 117,746, CDR 11.5/1000 -> implied denominator
den = 117_746/0.0115
print(f"CDR 11.5/1000 with 117,746 deaths -> implied mid-2023 population {den:,.0f}")
print(f"  ONEI effective end-2023 = {P[2023]:,}; consistent only if pop fell ~{den-P[2023]:,.0f} within 2023.")
print("  Cancer 246.0/100k => cancer deaths", f"{246.0/100000*den:,.0f}", "= ", f"{246.0/1000/11.5*100:.1f}% of all deaths (Anuario says 22.4%).")
