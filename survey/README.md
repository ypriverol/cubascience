# Cuba family experience survey (2019–2026)

Short convenience-sample instrument: **~10 questions**, Spanish, no free text.

## Where responses are stored (tracing)

**Every valid submission goes to one place only:**

```
Respondent browser  →  POST  →  Google Apps Script (/exec URL)
                                      ↓
                            Private Google Sheet (your account)
                                      ↓
                            Tab: responses  (one row per person)
```

| Tab | Who can see it | Contents |
|-----|----------------|----------|
| **`responses`** | **You only** (Sheet must stay private) | Full answers + `received_utc` + anonymous `token` |
| **`audit`** | You only | Rejected attempts: timestamp + reason (no answers saved) |
| **`summary`** | You only | Updated by `refreshSummary()` — counts and medians |

**Nothing is written to GitHub, the public website, or analytics tools.**  
The `/exec` URL is a **write-only** public endpoint: strangers can POST but **cannot read** the Sheet.

### How to check progress

1. **Open the Sheet** → tab `responses` → row count − 1 = total N.
2. **Run `refreshSummary()`** in Apps Script (▶ Run) → read tab `summary`:
   - `total_stored`, `on_island`, `abroad`, `last_7_days`, median emigration/deaths counts.
3. **Optional weekly trigger:** Apps Script → Triggers → `refreshSummary` → Time-driven → Week timer.
4. **Optional remote peek:** Script property `ADMIN_KEY` → open  
   `YOUR_EXEC_URL?key=YOUR_ADMIN_KEY` → JSON stats (no raw rows).

Run **`auditReport()`** in the editor if you suspect spam — shows drop reasons (`honeypot`, `too_fast`, `bad_num_*`, `daily_cap`, etc.).

---

## Anti-abuse / “can’t be hacked”

No public form is fully attack-proof. This design **limits damage** and **keeps garbage out of analysis**:

| Control | Layer | Effect |
|---------|--------|--------|
| Private Sheet | Google | Raw data never exposed via API read |
| Honeypot field `website` | Server | Bots that auto-fill all inputs → dropped |
| Min time 15 s / max 2 h | Server | Too fast or scripted replay → dropped |
| Token format + max **2** stored per browser | Server | Same device can’t flood hundreds of rows |
| **250 rows/day** global cap | Server | Limits mass POST even with many tokens |
| Enum validation (`resides`, province, age…) | Server | Random POST bodies rejected |
| Numeric bounds (0–200, etc.) | Server + browser | Absurd counts rejected |
| `fam_died_60plus ≤ fam_died` | Server + browser | Logic check |
| `resides=cuba` + recent `left_year` | Server | Inconsistent answers dropped |
| Script lock on append | Server | Race-safe under concurrent POSTs |
| `no-cors` + opaque response | Browser | Attackers can’t easily probe per-row status |
| No free text | Form | No injection / doxxing via text fields |

**What attackers can still do:** POST fake but *valid-looking* rows until the daily cap (pollutes convenience sample). Mitigation: monitor `audit`, watch for spikes, close the form when `total_stored` hits target N, pre-register analysis.

**What you must do:**

- Keep the **Sheet private** (not “anyone with link”).
- Do **not** publish the Sheet ID or `ADMIN_KEY`.
- Redeploy Apps Script after changing `apps-script.gs` (Manage deployments → Edit → New version).
- Replace `ENDPOINT` in `index.html` only with your deployment URL.

---

## Sample size targets

| Goal | N |
|------|---|
| Pilot | 50–100 |
| Descriptive memo / blog sidebar | **200–400** |
| Stratify on-island vs abroad | **≥300 total**, **≥80 on-island** |

At ~1–3% of ~10k followers → expect **100–300** responses. Pre-register: e.g. “close at 300 or 30 days.”

---

## Fields (must match `apps-script.gs`)

**Context:** `resides`, `province_group`, `left_year`, `age_band`  
**Structure:** `uncles_aunts`, `cousins`, `children`  
**2019–2026:** `fam_left_2019_2026`, `fam_died_2019_2026`, `fam_died_60plus`  
**Meta:** `consent`, `token`, `elapsed_s`, `received_utc`

---

## Deploy checklist

1. New **private** Google Sheet.
2. Extensions → Apps Script → paste `apps-script.gs` → Save.
3. (Optional) Project settings → Script properties → `ADMIN_KEY` = long random string.
4. Deploy → Web app → Execute as **Me**, Access **Anyone**.
5. Copy `/exec` URL → `survey/index.html` → `ENDPOINT`.
6. Merge to `master` → live at `https://ypriverol.github.io/cubascience/survey/`.
7. Test one real submission → confirm row in `responses`.
8. Run `refreshSummary()` once → confirm `summary` tab.

---

## Analysis (planned)

Export Sheet (File → Download CSV) → local only →  
`demographics/artifacts/survey_responses/` (gitignored) → aggregate script TBD.

Report **aggregates only**; never raw rows.
