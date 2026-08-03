# External data: where to get it, and what Cuba actually has

Verified against the live WHO endpoints on 2026-08-03. Every URL below was
resolved from the WHO Mortality Database landing page, not guessed.

## What is already in this repo

`data/who/cuba_morticd10_2021_2023.csv` — Cuba's full ICD-10 submission for
**2021, 2022 and 2023**: 9,399 rows of deaths by cause x 5-year age group x sex.
Extracted from `morticd10_part6`, filtered to `Country == 2150`.

This matters more than it looks. **Cuba has submitted 2023 to WHO but ONEI's own
published tables (3.15, 3.3) stop at 2022.** The WHO file is currently the most
recent age-disaggregated Cuban mortality data in existence, and it is
cause-specific, which ONEI 3.15 is not.

## WHO Mortality Database

Landing page: <https://www.who.int/data/data-collection-tools/who-mortality-database>

| File | URL | Why you want it |
|---|---|---|
| **Availability** | [`mort_availability.zip`](https://cdn.who.int/media/docs/default-source/world-health-data-platform/mortality-raw-data/mort_availability.zip?sfvrsn=23261e11_33) | Country x year coverage. Confirms Cuba runs 1959–**2023**. Download this first, always. |
| **ICD-10 part 6/6** | [`morticd10_part6.zip`](https://cdn.who.int/media/docs/default-source/world-health-data-platform/mortality-raw-data/morticd10_part6.zip?sfvrsn=ec801a61_4) | 2021 onwards. **This is the one with Cuba's crisis years** (~6.8 MB). |
| ICD-10 part 5/6 | [`morticd10_part5.zip`](https://cdn.who.int/media/docs/default-source/world-health-data-platform/mortality-raw-data/morticd10_part5.zip?sfvrsn=ad970d0b_34&ua=1) | 2017–2020: the pre-crisis baseline you standardise against. |
| ICD-10 part 4/6 | [`morticd10_part4.zip`](https://cdn.who.int/media/docs/default-source/world-health-data-platform/mortality-raw-data/morticd10_part4.zip?sfvrsn=259c5c23_30&ua=1) | 2013–2016. |
| **Population / live births** | [`mort_pop.zip`](https://cdn.who.int/media/docs/default-source/world-health-data-platform/mortality-raw-data/mort_pop.zip?sfvrsn=937039fc_26) | Denominators — **but see the warning below.** |
| Country codes | [`mort_country_codes.zip`](https://cdn.who.int/media/docs/default-source/world-health-data-platform/mortality-raw-data/mort_country_codes.zip?sfvrsn=800faac2_5&ua=1) | Cuba = **2150**. |
| Documentation | [`mort_documentation.zip`](https://cdn.who.int/media/docs/default-source/world-health-data-platform/mortality-raw-data/mort_documentation71f9e29d-7e3f-41e6-aafc-c4c1775c7aa3.zip?sfvrsn=40cce9be_42) | Age-format codes and the cause list. Needed to read `Frmat`. |
| Notes | [`mort_notes.zip`](https://cdn.who.int/media/docs/default-source/world-health-data-platform/mortality-raw-data/mort_notes.zip?sfvrsn=2020c859_19&ua=1) | Per-country-year caveats. |

### Warning: WHO has no recent Cuban population denominators

`mort_pop` carries Cuban population only to **1996**. So the WHO file gives you
numerators (deaths by cause and age) but *not* denominators for the crisis years.
Use ONEI 3.3 for population, which this repo already parses via
`mortality_data.mean_population_by_age()` — observed to 2022, cohort-projected
after. This is the binding constraint on any cause-specific rate for Cuba.

### Reading the file

`Frmat` is the age-group coding; Cuba 2021–2023 uses **Frmat 0**, the most
detailed: `Deaths1` is all ages, `Deaths2`–`Deaths6` are single years 0–4,
`Deaths7` is 5–9, then five-year groups through `Deaths25` = 95+, and
`Deaths26` = age unknown. `List` 104 is the ICD-10 detailed list; `Cause` `AAA`
is all causes. Do **not** open these in Excel — import them.

Sanity check that the extract is right: all-cause `AAA` totals are 167,675
(2021), 120,108 (2022), 117,749 (2023).

## PAHO PLISA

<https://www.paho.org/en/enlace/data-portal> — the Mortality & Causes of Death
module exports CSV.

PLISA is a JavaScript dashboard with no stable direct-download URL, so it cannot
be scripted; the export has to be produced from the UI. It is worth doing anyway
for one reason: **PLISA carries the regional comparators already age-standardised
to the PAHO standard population**, which is what you need to put Cuba's rates
beside its neighbours without recomputing everyone else's.

Request, per country and year: `Cause_ICD10`, `Age_Group` (5-year), `Deaths`,
`Population`, `Sex`.

## Caution on comparisons

Cuba's published cause-specific rates are **crude**. Roughly **41% of Cuba's
crude death rate is age structure alone** (see
`artifacts/age_standardised_mortality.json`). Any comparison of a Cuban crude
rate — or worse, a Cuban 75+ age-specific rate — against a regional
age-standardised all-ages rate is meaningless and will overstate Cuba's position
by a factor of two to twenty. Standardise both sides to the same population
before comparing anything.
