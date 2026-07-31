# Model E adversarial gate notes

Date: 2026-07-31  
Decision: **keep Model E beside preferred Model D** (`promote: false`).

## Checks

### Are \(B^*\) and \(D^*\) identified separately, or only \(B^*-D^*\)?
Partially separate. \(D^*\) uses ageing-scaled 2019 schedule × \(f(S_t)\); \(B^*\) is register-anchored with small TFR depression from \(S_t\). The population identity still needs \(M^*\), so the **level** of \(P^*\) is not identified from vitals alone. Component shares (mig ≈88%, natural decrease ≈12%) are informative but prior-dependent.

### Does high \(S\) double-count ageing already in the death schedule?
Risk is real. Ageing enters both (i) expected deaths via elderly-share scaling and (ii) the ageing bucket of \(S_t\). Mitigation: decadence uplift uses \((S_t-S_{2019})\) with a modest \(\alpha\in[0.15,0.55]\), and the ageing mix weight is only 0.25. Gate: do not raise \(\alpha\) without removing elderly share from \(S\).

### Is COVID misuse overweighting the score?
`covid_misuse_ratio_norm` is 40% of the bad-reporting bucket (bucket mix 0.25 → ~10% of \(S\)). It never multiplies all-cause deaths by 20–50×. Acceptable for v1; sensitivity on that weight belongs in a follow-up.

### Does E actually change population vs D, or only re-label components?
E changes the **composition** more than the headline: pop end-2025 **8.96M** vs D **8.59M** (still inside the 1.8–2.4M loss envelope). Hidden deaths sum ~+73k over 2022–2025 vs register; births slightly below register. Migration remains dominant. E does **not** overturn the emigration-first story.

### Promote?
**No.** Keep D as preferred public model. Ship E as methods companion + claim-sheet block with `promote: false`. Revisit after (a) full age-schedule from ONEI 3.15, (b) weight sensitivity on COVID/ageing, (c) joint posterior rather than sequential medians.

## Ruling
Park promotion. Ledger: Model E complete as provisional companion.
