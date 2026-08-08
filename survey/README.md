# Cuba family experience survey (2019–2026)

Short convenience-sample instrument: **~10 questions**, Spanish, no free text.
Collects extended-family structure (uncles/aunts, cousins, children) and counts
of relatives who **left Cuba** or **died** between 2019 and 2026.

## What it can inform

This is **not** a national census. A Twitter/diaspora sample over-represents
emigration. Aggregates still help:

| Field | Study use |
|-------|-----------|
| `uncles_aunts`, `cousins`, `children` | Family-network scale (denominator context) |
| `fam_left_2019_2026` | Migration intensity vs ONEI net migration (2022–2025 window) |
| `fam_died_2019_2026`, `fam_died_60plus` | Mortality experience vs registered deaths / excess-mortality band |
| `resides` | Stratify on-island vs abroad subsamples |
| `province_group`, `age_band` | Coarse geography and selectivity |

Report only **aggregates**; never raw rows.

## Fields (must match `apps-script.gs`)

**Context:** `resides`, `province_group`, `left_year`, `age_band`

**Family structure (alive today):** `uncles_aunts`, `cousins`, `children`

**Events 2019–2026 (extended family):** `fam_left_2019_2026`, `fam_died_2019_2026`, `fam_died_60plus`

**Meta:** `consent`, `token`, `elapsed_s`, `received_utc`

## Ethics

- No name, contact, address, or municipality (province **group** only).
- No free-text fields.
- No IP stored by the script; no analytics or third-party assets.
- Explicit consent required.
- Test `script.google.com` reachability from Cuba before launch.

## Architecture

```
GitHub Pages (survey/index.html)  ──POST──▶  Apps Script  ──▶  private Google Sheet
```

1. Create a Google Sheet → Extensions → Apps Script → paste `apps-script.gs`.
2. Deploy → Web app → Execute as **Me**, Access **Anyone**.
3. Copy the `/exec` URL into `index.html` as `ENDPOINT`.
4. Merge to `master` → CI publishes to `https://ypriverol.github.io/cubascience/survey/`.

Abuse controls: honeypot, minimum completion time (15 s), per-browser token cap (3).

## Analysis (planned)

Export Sheet → `demographics/artifacts/survey_responses/` (gitignored) →
aggregate script in `demographics/scripts/` (not yet implemented).
