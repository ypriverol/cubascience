# Manuscript improvement issues

Issue drafts derived from the critical review of the demographics manuscript and figures.

**Author response:** see [`manuscript_review_response.md`](manuscript_review_response.md) (2026-08-02 implementation pass).

## Prioritized backlog

| Priority | Title | Focus | Status (2026-08-02) |
|---|---|---|---|
| P0 | Resolve internal numeric inconsistencies across claims, scripts, and artifacts | Reconcile canonical values before further revision | **Done** — `audit_claims.py`; footnotes; script drift fixed |
| P0 | Make `claims.yaml` the real single source of truth | Remove drift from hard-coded values | **Done** — vital series + population paths; charts read claims |
| P1 | Reframe manuscript from “estimate” to “scenario audit” | Align title, abstract, and claims with methods | **Done** — title + intro/abstract |
| P1 | Reduce overemphasis on Model D point estimates | Lead with scenario envelope, not a pseudo-point estimate | **Done** — abstract/results pairing; waterfall caption |
| P1 | Implement reproducible ONEI 3.15 age-sex mortality pipeline | Replace illustrative mortality residual inputs | **Partial** — `mortality_schedule_residual.py` (coarse CDR bridge; ~77k combined) |
| P1 | Revise figures to reduce rhetorical overreach | Clarify scenario-only paths and non-independent triangulation | **Done** — captions + chart subtitles |
| P2 | Move provisional mortality residual out of the main headline | Keep provisional mortality work secondary until reproducible | **Done** — shortened results; secondary in conclusions |
| P2 | Audit and soften editorial language in the manuscript | Improve journal fit and credibility | **Done** — main.tex tone pass |
| P2 | Tighten comparative-context tables and claims | Harmonize sources, time windows, and definitions | **Done** — caption footnotes |
| P2 | Document which inputs are observed, derived, assumed, or expert-coded | Improve reviewability and provenance | **Done** — `provenance.yaml` + supplement table |
| P2 | Strengthen sourcing for selectivity claims | Trace subgroup claims to explicit data or derivations | **Done** — `selectivity.yaml`; sex-ratio softened in EN |
| P3 | Clarify Model E’s evidentiary status and sensitivity limits | Keep Model E useful without overclaiming | **Done** — supplement adversarial gate expanded |

<!-- Original issue drafts below unchanged for traceability -->
