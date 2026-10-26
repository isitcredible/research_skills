---
name: code-and-data
description: >-
  Second review stage: read the code against the text (with the formula map), run the
  replication package and reproduce its anchors, audit how the load-bearing variables
  were built from their sources, and stress-test every result family with the
  fragility battery and its design-specific modules.
---

# Code and data

Find out whether the code does what the paper says, whether the data are what the
paper says, and whether each result survives defensible alternatives. A result that
survives every valid check is reported as strong — the battery is a test, not a
kill-generator. Contributions may be **estimates**, **theorems**
(`../modules/theory-diagnostics/`), **calibrated or simulated model numbers**
(`../modules/quantitative-model-diagnostics/`), or hybrids; classify each result
family. Any of them read through a model also has its premises tested
(`../modules/whimsical-assumptions-diagnostics/`).

Ground rules:
- **No finding without a construction** — an executed regression, a counterexample, a
  re-run sweep, or a code-text mismatch cited at `file:line` (its effect on the
  printed cell run before it counts against a claim, where the code runs); never a
  verbal argument.
- **The anchor is the authors' code, executed** in `work/pkg/`, every repair logged —
  failed repairs too, under "Tried and failed" in the job's `PROGRESS.md`.
  Missing generated intermediates are rebuilt from raw inputs, not treated as blockers.
- **A blocked check needs proof** — exact file, command, error, attempted repair.
- **Verification is not reanalysis.** "The deposited code does not produce the printed
  cell" is a narrow, high-confidence failure; "a different defensible specification
  gives a different answer" is a weaker disagreement. Keep them apart (Clemens,
  `../references/methods/clemens_2017_failed_replications.md`).

## A. Code against text (before running anything)

1. **Extract the claimed specifications** — outcome, regressors, controls, fixed
   effects, every filter and sample restriction, weights, the variance estimator.
   Take them from the displayed coefficient rows, not the table notes.
2. **Trace the code** to the lines that filter data and estimate models, and record
   every mismatch at `file:line`: hidden drops, undocumented trims, different
   controls/FE/clustering, convergence workarounds (raised iteration limits, relaxed
   tolerances, try/skip).
3. **Formula map** — `analysis/code-and-data/formula-map.csv`, one row per printed
   formula: numbered and lettered equations, appendix definitions, and every
   data-construction rule (compounding, normalisation, index or share construction,
   deflators, back-casting): `printed_ref | implementing file:line |
   identical/differs/not-implemented/no-code | exact discrepancy`. Enumerate the
   printed side from the text. A printed formula with no row has not been audited.
4. **Mirror sweep** — for every `differs`, grep the deposit for other implementations
   of the same transform. A slip reported only where first found understates its reach.
5. **Feasibility matrix** — `analysis/code-and-data/feasibility-matrix.csv`: `exhibit |
   required inputs | input status`. Required before any "cannot be validated" claim;
   one genuine input falsifies the blanket.
6. **Provenance** — every input the code touches gets its type from
   `review/deposit-inventory.json`; an `unknown` file is probed before it supports any
   "simulated" or "restricted" conclusion.
7. **Prescribe each correction precisely**: the native baseline must reproduce print
   first; one named edit; the full set of printed cells the object feeds. A
   discrepancy in a shared input is checked once per result family that uses it.

## B. Run the package and reproduce

- Inventory software and resources; map every result family (headline, mechanism,
  balance, placebo, robustness, appendix — not just the headline).
- **Reproduce anchors** natively: estimate, N, SE/p, fixed effects, weights,
  clustering. Tolerance: exact match on N and degrees of freedom; relative difference
  < 1e-4 on estimates and SEs, or agreement to the printed rounding. Outside tolerance
  → `NONREPRODUCED`, a finding with the difference and the repair log. The tolerance
  is fixed: never widen it, or drop a cell from the comparison, to turn a mismatch into
  a match. The one exception is a stochastic number whose seed the deposit omits: its
  value is `NONREPRODUCED` only if it lies outside the range of at least 199 seeded
  runs (a 1% false-alarm rate when the printed value is itself one draw); with fewer
  runs, report its rank among them and make no call. The missing seed is recorded as
  a documentation gap.
- **Reconcile code with paper cell by cell**: what variation identifies the cell;
  outcome, transform and units as the table claims; every claimed subsample rebuilt
  against *all* published columns (a match matrix, not a diagonal); subset labels
  checked with `n_dropped`/`n_kept` (a bounding box is not a region); the code
  implements the cited method, not a lookalike. Mismatch triage: rounding, then base
  categories, then which variance estimator reproduces the print (tables mix them by
  row), then which code block produced the table — transcribing printed values from
  page images. Do not write "reproduces" before this comparison exists.

## C. Data audit

Reproduction shows you have the authors' file, not that the file is right. Errors
and fabrication live upstream in construction. A false fraud charge is the most
damaging error this audit can make; credulity is the other failure.

**Always (the lite pass, every empirical paper):**
- Fix the target (anchored headline specification, load-bearing variables, version).
- Map each load-bearing variable's chain: `stated source → extraction → transcription
  → cleaning → imputation → transformation → merge → estimation field`. Identify the
  regressor numerically against its source (a per-capita series hides a population, a
  real series a deflator, a share a denominator). Note who could audit it:
  field-collected, hand-coded (the clean falsification target), or third-party.
- File forensics: workbook `docProps` and `calcChain`, `.dta` timestamps, hidden
  sheets/names/links, zip-internal dates; duplicates, impossible values, digit and
  heaping tests (`../references/anomaly-tests.md`), excess similarity, breaks at
  source or batch seams (a turning point at a splice is suspect); recompute aggregates
  from subgroup cells — an unexplained residual is a finding.
- Second records: where another copy of the same observations exists (an
  author-site file, a later pooled or replication dataset, an earlier deposit
  version; `../references/source-protocol.md`), match it to the deposit row by
  row, diff every matched cell, list rows found in one copy and not the other,
  and re-run the headline tests on each version.

**Escalate to the full audit** when a load-bearing variable is imputed or
reconstructed, a construction concern or anomaly flag survives, missingness is
material, or the data are the paper's contribution:
- Get the exact cited sources (`../references/source-protocol.md`; a later edition is
  not the cited source), record identity and hash, map digital pages to print.
- Check fidelity on a reproducible random sample plus the high-leverage cases, file
  against source exactly, using printed totals as checksums. Keep three standards
  apart: the cited page, the cited corpus searched, and historical truth. Silence in
  the corpus is not "didn't happen". Each load-bearing variable is covered separately.
- Re-plot raw points without fitted curves (a pattern visible only through the fit is
  the model, not the data); check figure furniture against the series.
- Rebuild the construction and propagate the range of defensible codings: middle of
  the range = honest noise; reachable only at the result-maximising fork = discretion;
  outside the range = fabrication. Interval-code genuinely vague sources rather than
  forcing a point. Re-run on measured-only observations.
- Missingness: which field, how much, what pattern, and what estimand results.

Statuses per load-bearing variable in `analysis/code-and-data/source-coverage.csv`:
`SOURCE_CHECKED` · `PARTIAL` · `INTERNAL_ONLY` (only the deposit's own chain checked —
coherence, never correspondence to a source) · `BLOCKED` · `NOT_APPLICABLE`. While any
chain is open, report scoped facts ("the 20 checked observations matched"), never "the
data passed". Findings go to `analysis/code-and-data/data-findings.csv` (template
`../assets/data-findings.csv`).

**Every construction choice that reaches an estimation field is quantified** — caps,
fills, weights, rescales: re-run the tables it feeds under the defensible alternative,
or record the row `BLOCKED` naming the missing input. State the direction (a defect that
understates the paper's estimate is still a defect). Before calling a choice a defect,
check the authors could have done otherwise — read the pipeline to its end. Would the
same error running the other way be dismissed?

**Evidence ladder**: (1) documentation gap → (2) verified error → (3) undisclosed
discretion → (4) misrepresentation → (5) fabrication. Never use a higher rung's
language on a lower rung's evidence; rule out innocent explanations (wrong version,
OCR, your own bug — always first) before rungs 4–5. Corrections that move a result
feed straight into the battery (D) before the report is written.

## D. Fragility battery

**Construction ledger** — `analysis/code-and-data/construction-ledger.md`: every
analytic choice (transforms, sample restrictions with dropped counts against the
stated N, variable constructions, simulation machinery with seeds, winsorising,
imputation, rescaling) and **every discretionary specification choice** not forced by
theory. A choice the text justifies stays on the ledger with its justification beside
it: the test is whether the alternative is as defensible, not whether a reason was
given. Each becomes a hypothesis: what is it for; does an
equally defensible alternative move the result, and which way; is it applied
symmetrically? Re-run the alternative in **every column it enters**. A shared object
lists its users on a `consumers: F1, F2` line.

**Manifest** — `analysis/code-and-data/battery-manifest.csv`, one row per check
(every distinct estimator a row; an unrunnable check a row too, never absent):
`id | family | hypothesis | spec | artifact | seed | state | validity | row_role`,
plus `variant_of | patch | moments | ledger_item | consumer` where they apply.
- `state`: `done` (executed and its output inspected) · `NONREPRODUCED` · `PROXY`
  (name the substitute and its limits) · `BLOCKED` · `NOT_RUN` · `NOT_APPLICABLE`.
- `validity`: `clean` · `unvalidated` (a review-built calculation still awaiting its
  patch and moments file; once it has them it is `clean` here, and the challenge stage
  later rebuilds it against its requirements, a failed requirement making it
  `invalid`) · `invalid` (degenerate, unbounded, capped, or without power against the paper's estimate — say which in
  the notes). Only clean rows are test outcomes; the rest are evidence that a
  procedure is uninformative here. A correction of the paper's own estimate (rule 8:
  its own estimand under the inference the design requires, or its printed method as
  written) is never `invalid` for low power: the corrected interval is the result.
- `row_role`: `verdict-bearing`, or `rebuttal` (a re-run of the paper's own selected
  estimate — stability of that number, not an independent test). A rebuttal that
  holds corroborates nothing; one that fails counts against the claim.
- A review-built variant needs `patch` (diff against the shipped builder, only the
  defective lines changed; for a defect in shipped data, the data diff) and `moments`
  (the sidecar file). **A variant implementing
  the paper's own documented method** — a printed equation, a stated appendix rule — is
  never `invalid` however far it moves: code disagreeing with the documented method
  is the finding, reported as a measured discrepancy.

**Results** — `analysis/code-and-data/results.csv` (schema `../assets/results.csv`):
every check that produced a number. Run `python3 <review skill>/scripts/check_manifest.py
--root <job>` and `python3 <review skill>/scripts/check_inference.py --root <job>`; both
must pass before `COMPLETE`. Run them once the fired modules have reported: before that,
failures for missing module reports are expected and the stage is `INTERIM`.

**For each empirical estimate report three things**: practical magnitude (outcome
units, against the baseline rate; standardised at the regressor's real variation),
design-appropriate significance, and Shapley/LMG share of explained variance (R
`relaimpo`/`domir`, Stata `shapley2` — `../references/software-examples.md`; never
partial R² or η²; `NOT_APPLICABLE` where no R²-style decomposition exists,
`NOT_RUN` where one exists but cannot be run). They can disagree; that is information.

**The checks:**
1. **Finish the authors' own battery** first: a check run on a subset but claimed in
   general is extended to the omitted cells by editing their script.
2. **Inference**: cluster or randomisation inference at the real assignment level;
   few-cluster tools (jackknife, CV3, restricted wild bootstrap —
   `../references/methods/mackinnon_nielsen_webb_2023_few_clusters.md`,
   `../references/methods/hansen_2026_jackknife_se.md`); multiple-testing correction per claim family;
   spatial and serial correlation per `../references/design-matrix.md`; the collapse
   test where a key regressor is constant within coarser units; "significant in A, not
   B" needs a direct A−B test (`../references/methods/gelman_stern_2006_difference_test.md`); Type M / Edlin
   factor on headline estimates (`../references/methods/gelman_carlin_2014_type_ms.md`).
3. **Stability**: leave-one-out, influence, transforms, subsets, timing, negative
   controls, placebos (inside the corrected specification; one that passes is a failure to
   reject unless equivalence-tested — `../references/methods/eggers_tunon_dafoe_2024_placebo_tests.md`). Check the sign before
   reporting a leave-out; give levels and denominators with every %; undo load-bearing
   transforms where invertible.
4. **Specifications the authors avoided**: their robustness menu is the floor. Run the
   defensible ones they conspicuously did not — e.g. a pre-treatment level × period
   control for a time-invariant treatment, numerator and denominator entered
   separately where a ratio hides levels, the untried comparison group or FE
   structure. "Robust" is relative to a threat: name it and say whether it was tested.
5. **Modules**: for every result family, walk the table and fire every module whose
   condition holds; record the walk in `analysis/code-and-data/module-walk.md` (fired /
   not fired, with the evidence). Each fired
   module runs as its own job from its `SKILL.md` and writes
   `analysis/code-and-data/<module>-REPORT.md`; a module ruled not applicable writes a
   stub whose marker line is `Status: NOT_APPLICABLE — <the failed condition>` (the
   gates exempt a stub from the module's required lines, and fail a fired module whose
   report is one). The walk states each module's outcomes in that module's own terms
   (a premise that cannot be relaxed is whimsical effect `UNTESTED` with its `warrant`
   grade, not "graded UNTESTED"). A paragraph from general knowledge in place of a
   module run is the commonest silent failure here.

   **Fired modules as separate agents.** The stage agent does A–D and the walk; the
   fired modules then run in parallel; the stage agent resumes to fold them in, finish
   its report and run the gates. Each module agent writes its own report, puts its
   leads under that report's `## Leads for later stages` (the stage agent folds them
   into the stage report), keeps scripts and logs in `work/scripts/` and `work/logs/`
   with names prefixed by the module, and appends its rows to `results.csv` and
   `battery-manifest.csv` under a file lock, in the stage's column order. Once modules
   have appended, no builder regenerates a shared ledger from scratch: the stage edits
   its own rows in place.

   | Design feature in any result family | Module (`../modules/`) |
   |---|---|
   | Cutoff, threshold, running variable, kink in a policy schedule, geographic boundary | `rdd-diagnostics` |
   | Instrument / 2SLS / fuzzy design | `iv-diagnostics` |
   | Cross-sectional OLS on a control set (esp. spatial units) | `cross-sectional-diagnostics` |
   | `ln(1+x)`, asinh, counts, per-capita scaling, weak denominators | `scale-sensitive-diagnostics` |
   | Few units or clusters, or a load-bearing null | `small-n-diagnostics` |
   | Horse race, mediator control, same-source covariate, subset restriction, transported denominator, any discretionary choice | `controls-samples-diagnostics` |
   | Panel variation without a discrete treatment event | `panel-diagnostics` |
   | Difference-in-differences / event study | `did-event-study-diagnostics` |
   | Shift-share / exposure-weighted regressor or instrument | `shift-share-diagnostics` |
   | Synthetic control / synthetic DiD | `synthetic-control-diagnostics` |
   | Randomised assignment | `experiment-diagnostics` |
   | Levels regression of trending series, or a model fitted to trending aggregates | `time-series-diagnostics` |
   | A load-bearing theorem, proof or derivation | `theory-diagnostics` |
   | A headline number from solving, simulating or calibrating a model | `quantitative-model-diagnostics` |
   | Any load-bearing conclusion or prescription derived from a model (proved, calibrated, or an estimate read through one) | `whimsical-assumptions-diagnostics` |

   Simulation and resampling loops follow `../references/simulation-harness.md`.
6. **Account for survival**: name each surviving check's estimand and role beside the
   claim — a survivor re-estimating the same selected number is stability, not
   corroboration — and record any margin with no valid test as untested.

## Output

`review/code-and-data-REPORT.md` from `../assets/report-template.md`, findings `C1, C2,
…`, with sections for code against text, reproduction, data audit (statuses and the
ladder rung reached) and the battery; every artifact above; module reports. Each
unresolved item says whether it is feasible and whether the verdict depends on it — a
feasible, verdict-bearing item is either run or explicitly waived by the operator.
Leads for `claims`: which estimates survive, under what, and which margins are
untested.

`COMPLETE` = every family anchored, ledger and manifest built, applicable checks done
with inspected output, `check_manifest.py` and `check_inference.py` passing. `INTERIM` = a required check or
artifact missing (name it, keep working on what is independent). `BLOCKED` = nothing
anchorable, with exact evidence — printed tables still read.
