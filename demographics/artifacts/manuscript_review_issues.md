# Manuscript improvement issues

Issue drafts derived from the critical review of the demographics manuscript and figures.

## Prioritized backlog

| Priority | Title | Focus |
|---|---|---|
| P0 | Resolve internal numeric inconsistencies across claims, scripts, and artifacts | Reconcile canonical values before further revision |
| P0 | Make `claims.yaml` the real single source of truth | Remove drift from hard-coded values |
| P1 | Reframe manuscript from “estimate” to “scenario audit” | Align title, abstract, and claims with methods |
| P1 | Reduce overemphasis on Model D point estimates | Lead with scenario envelope, not a pseudo-point estimate |
| P1 | Implement reproducible ONEI 3.15 age-sex mortality pipeline | Replace illustrative mortality residual inputs |
| P1 | Revise figures to reduce rhetorical overreach | Clarify scenario-only paths and non-independent triangulation |
| P2 | Move provisional mortality residual out of the main headline | Keep provisional mortality work secondary until reproducible |
| P2 | Audit and soften editorial language in the manuscript | Improve journal fit and credibility |
| P2 | Tighten comparative-context tables and claims | Harmonize sources, time windows, and definitions |
| P2 | Document which inputs are observed, derived, assumed, or expert-coded | Improve reviewability and provenance |
| P2 | Strengthen sourcing for selectivity claims | Trace subgroup claims to explicit data or derivations |
| P3 | Clarify Model E’s evidentiary status and sensitivity limits | Keep Model E useful without overclaiming |

## Copy-paste GitHub issue drafts

### 1) Resolve internal numeric inconsistencies across claims, scripts, and artifacts

**Summary**
Several quantities disagree across `/home/runner/work/cubascience/cubascience/demographics/data/claims.yaml`, generated JSON artifacts, plotting scripts, and manuscript text.

**Examples already identified**
- 2022–2025 registered deaths: 502,149 vs 502,159
- Natural balance in 2025: -68,149 vs -68,150
- 2023 deaths: 117,739 vs 117,746
- 2022 deaths: 120,098 vs 120,108

**Tasks**
- Audit all repeated headline quantities across claims, scripts, artifacts, notebook, and manuscript files
- Choose one canonical value for each disputed quantity
- Regenerate downstream artifacts and figures from the canonical source
- Add a short note documenting any intentional alternate values or footnotes

**Why this matters**
This is the highest-priority credibility and reproducibility issue.

---

### 2) Make `claims.yaml` the real single source of truth

**Summary**
The repo states that `claims.yaml` is canonical, but multiple plotting scripts and artifacts still hard-code numbers.

**Tasks**
- Identify all hard-coded publication values in `/home/runner/work/cubascience/cubascience/demographics/scripts/`
- Replace them with reads from canonical claims or generated artifacts where feasible
- Document provenance for each headline figure and manuscript claim
- Add a lightweight consistency check so future drift is easier to catch

**Why this matters**
The current setup makes numerical drift too easy.

---

### 3) Reframe manuscript from “estimate” to “scenario audit”

**Summary**
The manuscript title and framing present the work as an estimate, while the methods explicitly state that Models A–D are scenarios rather than identified estimators.

**Tasks**
- Revise title, abstract, introduction, discussion, and conclusion language
- Replace estimate-like wording with scenario-audit wording where appropriate
- Make Model D’s role consistent throughout as an illustrative central scenario
- Update captions and README references that currently imply stronger identification

**Why this matters**
This resolves a core mismatch between framing and methods.

---

### 4) Reduce overemphasis on Model D point estimates

**Summary**
Values like 8.59M, 20.5%, and 91% migration share are given too much prominence relative to the paper’s own uncertainty structure.

**Tasks**
- Lead the results with the across-scenario loss envelope
- Downgrade Model D from headline estimate to illustrative central scenario
- Reword summary statements, captions, and graphical callouts accordingly
- Re-check abstract and conclusion for false precision

**Why this matters**
It will make the central claims better match the evidentiary basis.

---

### 5) Implement reproducible ONEI 3.15 age-sex mortality pipeline

**Summary**
The manuscript references a pending reproducible age-sex mortality pipeline, but the current provisional residual still relies on illustrative expected-death inputs.

**Tasks**
- Build the explicit ONEI 3.15 age-sex expected-deaths pipeline
- Publish the resulting derived outputs in the repo
- Replace illustrative expected values in the mortality figure and text with pipeline outputs
- Document assumptions and sensitivity choices clearly

**Why this matters**
This is required before the mortality residual can carry more weight in the paper.

---

### 6) Revise figures to reduce rhetorical overreach

**Summary**
Several figures currently imply stronger identification or stronger evidentiary support than the underlying methods justify.

**Targets**
- Population path figure with 2030 continuation
- Waterfall decomposition figure
- Triangulation figure
- Life-expectancy figure
- Mortality residual figure

**Tasks**
- Review captions, labels, callouts, and visual hierarchy
- Mark scenario-only extensions more explicitly
- Separate ceilings, official counts, soft anchors, and study estimand more clearly
- Revisit any figure that visually obscures overlap between `U0` and `M`

**Why this matters**
The visuals should be as cautious as the best parts of the text.

---

### 7) Move provisional mortality residual out of the main headline

**Summary**
The ~38k 2024–2025 mortality residual is explicitly provisional and should not carry headline weight until the full age-sex pipeline is complete.

**Tasks**
- Reduce prominence in abstract, results, and conclusion
- Keep it clearly separated from crude registered excess mortality
- Move emphasis to the supplement if needed
- Reassess once the full mortality pipeline exists

**Why this matters**
It avoids overclaiming a result the manuscript itself labels provisional.

---

### 8) Audit and soften editorial language in the manuscript

**Summary**
Some wording reads as rhetorical or advocacy-style rather than scientific.

**Examples to review**
- “honest”
- “empties” / “emptying”
- “collapse”
- “with integrity”
- “order-of-magnitude impossibility”

**Tasks**
- Review abstract, discussion, conclusion, and captions first
- Replace charged wording with neutral scientific language
- Keep strong claims, but phrase them with evidence-led tone

**Why this matters**
Tone affects reviewer trust.

---

### 9) Tighten comparative-context tables and claims

**Summary**
The historical and regional comparison sections are useful, but currently too approximate for a paper making strong quantitative claims.

**Tasks**
- Audit sources and definitions for each comparator
- Harmonize time windows and metrics where possible
- Remove or soften weak comparisons
- Make uncertainty and comparability limits explicit

**Why this matters**
This is a likely reviewer target if left vague.

---

### 10) Document which inputs are observed, derived, assumed, or expert-coded

**Summary**
The project mixes official observations, derived accounting quantities, prior assumptions, and expert-coded HSDS inputs, but this taxonomy is not yet explicit enough.

**Tasks**
- Add a provenance table for major quantities
- Classify each headline input as observed, derived, assumed, or expert-coded
- Link important manuscript claims to source files or artifact outputs
- Make the same distinctions visible in the supplement if needed

**Why this matters**
This will make the work easier to review and defend.

---

### 11) Strengthen sourcing for selectivity claims

**Summary**
Important subgroup claims such as female-majority flow, age selectivity, and reproductive-age skew need clearer provenance in the repository.

**Tasks**
- Trace claims like ~57% female and ~133 women per 100 men to explicit data or derivations
- Add source notes or derivation notes near the claims or in artifacts
- Distinguish direct measures from interpretive summaries

**Why this matters**
Unsupported subgroup claims create avoidable reviewer risk.

---

### 12) Clarify Model E’s evidentiary status and sensitivity limits

**Summary**
Model E is appropriately marked provisional, but its dependence on expert-coded HSDS inputs and a different `U0` prior needs even clearer presentation.

**Tasks**
- Expand limitations around HSDS subjectivity and transfer assumptions
- Clarify that the higher stock partly reflects a different baseline prior
- Add clearer sensitivity framing in the supplement and any summary tables
- Keep Model E visibly secondary until the adversarial concerns are resolved

**Why this matters**
This preserves Model E as a useful companion without overstating what it shows.
