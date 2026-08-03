# Cuba demography survey — instrument and rationale

A convenience sample recruited from Twitter **cannot estimate national levels**.
The audience is a Cuban-science-diaspora following; it over-represents emigration
by an unknown and probably large factor. Any "% who left" computed from it is
uninterpretable as a national rate, and the first reviewer to see it will say so.

So the instrument is built around three designs that are *made* for biased
samples, and it is scoped to inform exactly one parameter the manuscript cannot
currently identify.

## What it can actually inform

The weakest quantity in the paper is the gap between the **1.05 M documented
settled floor** and the **~2.0 M migration engine** the central scenario runs.
Nothing in the repository identifies it: destination registers bound it from
below and stop. That gap is what this survey targets.

Everything else it produces is secondary and should be reported as such.

## The three designs

### 1. Network Scale-Up Method (NSUM) — the primary estimator

Ask how many people the respondent knows in groups of *known* size, to estimate
their personal network size `d`, then ask how many they know in the *unknown*
group. For respondent *i*:

```
d_i  =  N * SUM_k( c_ik )  /  SUM_k( N_k )
```

where `c_ik` is how many people respondent *i* knows in calibration group *k*,
`N_k` is that group's true size, and `N` is the total population. Then

```
N_unknown  =  N * SUM_i( y_i ) / SUM_i( d_i )
```

with `y_i` the number known in the target group (emigrated since 2021; died in
2024–2025).

Calibration groups must have a genuinely known `N` from ONEI or MINSAP. The
three in the form are placeholders — **replace them with groups whose size you
can cite**, and prefer groups with low visibility bias:

- primary-school teachers (ONEI education tables)
- people on dialysis (MINSAP; also directly relevant to the crisis)
- twins (demographic constant, ~1.2% of births, low social bias)

NSUM's known weaknesses, all of which must be reported: **transmission bias**
(respondents do not know that a contact has died or emigrated), **barrier
effects** (networks are not random across the population), and **recall decay**
over a multi-year window. These bias the estimate downward, so an NSUM emigration
figure is best read as another *floor* — but a floor constructed independently of
destination registers, which is exactly what the 1.05→2.0 M gap lacks.

### 2. Household roster anchored at December 2021

"In the household you belonged to in December 2021, how many people were there?
Of those, how many now live abroad? How many have died?"

Anchoring at Dec 2021 matches the manuscript's window exactly. Selection bias
still bites, so **stratify by respondent residence and report the on-island
subsample separately** — that stratum is the scientifically valuable one and the
hardest to recruit.

### 3. Sibling survival

"How many children did your mother give birth to in total? How many are alive
today? How many live abroad?"

This is the DHS maternal-mortality instrument adapted. Its virtue here is that
sibship composition does not depend on the respondent's own migration decision,
so it is far more robust to the sample's diaspora skew than any household
question. It gives a mortality signal without a census.

## Ethics — not boilerplate for this subject

Respondents may be on the island, reporting deaths and emigration under a state
that treats demographic statistics as contested. The instrument therefore:

- collects **no** name, contact, address, or municipality (province *group* only);
- has **no** free-text field, because free text de-anonymises;
- records **no** IP (Apps Script cannot read one) and sets no cookies;
- carries no analytics, no fonts, no third-party assets of any kind;
- states on the landing page what is collected, that raw responses are never
  published, and that only aggregates are released;
- requires explicit consent, and drops any submission without it.

Nobody is asked to identify a deceased person. Ages are banded.

**Before building anything, test that `script.google.com` is reachable from
Cuba.** US sanctions have historically restricted Google services there. If the
endpoint is blocked, the on-island stratum is lost and with it most of the
scientific value; use a Cloudflare Worker instead.

## Architecture

```
GitHub Pages (static index.html)  ──POST──▶  Apps Script web app  ──▶  Google Sheet
```

No server. Free. The Sheet stays private; the deployment URL is a public *write*
endpoint only.

Abuse controls: honeypot field, minimum completion time, per-browser token with a
submission cap. None of these identify anyone.

## Expected yield and what it will support

At 1–3% of ~11,000 followers: **100–300 responses**. Enough for an NSUM estimate
with wide intervals and a crude on-island/abroad split. Not enough to stratify by
province and age simultaneously. Plan the analysis for that sample size before
launching, and pre-register it — with a convenience sample, an unregistered
analysis is indistinguishable from fishing.

## Deployment

1. Create a Google Sheet; Extensions → Apps Script; paste `apps-script.gs`.
2. Deploy → New deployment → Web app; Execute as **Me**; Access **Anyone**.
3. Copy the `/exec` URL into `index.html` as `ENDPOINT`.
4. Publish `index.html` via GitHub Pages.
5. Replace the three calibration groups with ones whose population size you can
   cite, and put those sizes in the analysis script.
