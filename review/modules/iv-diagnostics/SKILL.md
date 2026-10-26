---
name: iv-diagnostics
description: >-
  Diagnostics for instrumented specifications: first-stage strength at the
  design's inference level, reduced form, weak-instrument-robust inference,
  exclusion threats, and omitted-variable-bias sensitivity on the exclusion
  restriction. Invoke from `code-and-data` whenever any target
  specification uses an instrument. Strength is not exogeneity.
---

# IV diagnostics

Test the two claims an instrument makes — strength and exclusion — as
separate claims. Papers lead with the first-stage F because it is easy to
make large, but IV identification stands or falls on the exclusion
restriction, and exclusion needs its own evidence: a large first-stage
statistic proves nothing about it.

Trigger: any instrumented specification among the target results. If no
target specification is instrumented, this skill is `NOT_APPLICABLE` — do
not run IV diagnostics on an OLS paper to fill a checklist.

## Core checks — run for every instrumented target

- **First stage**, with inference at the level the instrument actually
  varies. An instrument that varies at the region level clustered at the
  unit level has an overstated first stage; report the cluster count at the
  instrument-variation level — nominal G AND the partial-leverage
  effective count G* (`../../references/methods/mackinnon_nielsen_webb_2023_few_clusters.md`),
  since leverage imbalance is what the F counts wrong.
- **Collapse the instrument to its genuine values** (the point estimate, not
  just the cluster count). Clustering at the instrument-variation level
  repairs the first-stage's precision and leaves the estimate untouched.
  Where the instrument is donor-substituted, interpolated, or otherwise
  constant within a coarser unit, drop-to-source (or average genuine
  replicates) and re-read the first-stage F and the 2SLS coefficient: an F
  that collapses is lost identification, and the estimate bends toward OLS
  under the weak instrument. See `../../references/design-matrix.md`,
  "Collapse-test record".
- **The IV-precision sanity check.** The analogous-OLS comparison is a
  free diagnostic: with homoskedastic SEs on the same sample, 2SLS cannot
  beat OLS on precision, so a 2SLS standard error *below* the comparable
  OLS SE under clustering suggests the clustered variance collapsing under
  leverage (a dominant cluster's residuals set the whole CV1 meat) rather
  than extra precision. Robust/clustered SEs carry no such ordering, so it
  is a tell, not proof: re-read both SEs under CV3/jackknife first, and
  escalate if the ordering survives only under CV1; do not let the table read
  "IV is more precise than OLS" (see the few-clusters crib's Hansen
  2026 section).
- **Reduced form.** The outcome regressed on the instrument directly. If the
  reduced form is fragile, the IV estimate is fragile no matter what the
  two-stage output says. And probe confounding on the *reduced form*, not
  the structural equation: the exclusion restriction is about the
  instrument, so "is the IV confounded by X" is tested as instrument→outcome
  with X controlled — not endogenous→outcome.
- **Weak-instrument-robust inference** — an Anderson–Rubin confidence set or
  equivalent, reported beside the conventional interval. If the robust set is
  unbounded or much wider, that is the finding. Under a weak first stage
  (MOP effective F below its critical value, or below the claim-matched
  threshold in the weak-IV guides crib, whichever the claim needs) the 2SLS
  point and t-interval are unstable under trivial spec changes: say what "the
  IV does" from the AR/tF set, and quote a 2SLS point only from a column that
  reproduces exactly. When clusters are few or
  unequal in leverage, report the first-stage F under **both** the CV1 the
  paper prints and the CV3/jackknife variance the leverage warrants — the
  same instrument can read F ≈ 2,400 on CV1 and F ≈ 26 on CV3, and the
  honest number is the second — then pair the AR set with a tF/VtF set:
  critical values
  are a function of the first-stage F̂ and, for VtF, the null-imposed
  residual correlation r̂ — computed on cluster-robust inputs (CV3 SEs and a
  cluster-consistent first-stage F);
  see `../../references/methods/mackinnon_nielsen_webb_2023_few_clusters.md`
  — the AR set inherits the cluster asymptotics that G* measures.
- **VtF on jackknife inputs — required, and not what `vtf` does.** In any
  design with few or unequal clusters or shocks, the VtF set is computed from
  the jackknife covariance of the reduced-form and first-stage coefficients
  (π̂, γ̂), built from the same leave-out fits as CV3 (and, for shift-share,
  from the delete-one-shock fits): F̂ = γ̂²/V̂_γγ and r̂(b₀) from that matrix,
  critical values looked up in the authors' `vtf95.mmat`, the set inverted
  over b₀. Stata's `vtf.ado` cannot do this: it takes only `robust` or
  `cluster()` and so always returns the CR1/HC1 set. Run it only as a
  companion row tagged `VtF-CR1-robustness`; a CR1 VtF that "barely widens"
  the printed interval is the CR1 variance agreeing with itself, not evidence
  of strength. With jackknife F̂ ≤ 3.84 the VtF set is unbounded; report it so.
  The tool lacking the option is never a reason to skip the computation or to
  log it as a limitation: build it by hand from the leave-out fits.
  `check_inference.py` F6/F7 enforce this.
- **Null-imposed Anderson–Rubin sets — required, and not what `boottest …, ar`
  does.** In Stata's `boottest` (`boottest.mata`, `ARubin` branch), the `ar`
  option sets the bootstrap DGP to the model constraints only (`DGP.SetR(*pR1)`),
  running an unrestricted wild bootstrap even though the output header prints
  "null imposed"; and `boottest …, jk` adds an `(M_{gg}^{-1} − I)X_g t₁` term
  to the jackknife residual that vanishes only at `b₀ = 0`, so any non-zero
  null or inverted confidence set from `boottest …, jk` is not MNW's WCR-S.
  Build the AR set by hand: for each candidate `b₀` on a wide grid, form the
  transformed outcome `y_b0 = y − b₀ · endog`, regress `y_b0` on the
  instrument(s) and exogenous controls (re-absorbing fixed effects), test the
  instrument coefficient(s) against `0` with `boottest …, jk noci` (followed
  immediately by `assert !missing(r(p))`) or with the delete-one-cluster /
  delete-one-shock jackknife F, and bisect the grid crossings. Never report
  `boottest`'s own `ar` or `jk` confidence interval as the few-cluster AR or
  WCR-S set; a `boottest …, ar` call is permitted only as a companion row
  tagged `AR-boottest-robustness`. `check_inference.py` F8–F10 enforce this.
- **Weak-IV statistic matched to the VCE.** Under clustered or robust errors
  judge strength by the Montiel Olea–Pflueger effective F (`check_inference.py`
  F13 requires every `iv-diagnostics` report to state the MOP effective F or
  `Effective-F: not applicable — <reason>`). Just-identified with one
  endogenous regressor, `F_eff` equals the robust first-stage F and the
  Kleibergen–Paap rk Wald F (`e(widstat)` under `robust`/`cluster()`) and may
  be read against Stock–Yogo t-size critical values (Andrews–Stock–Sun 2019,
  pp. 738–739) — but a 16.38 pretest certifies only an 85% interval (Lee et
  al. 2022), so the inference itself comes from tF/VtF or AR. Overidentified,
  use MOP's bias-based critical values (τ = 10%: up to 23.1); KP is then a
  different statistic and neither table fits it.
  Cragg–Donald (`e(cdid)`, or `e(widstat)` without `robust`/`cluster()`) is
  the i.i.d.-error statistic and is never quoted as the first-stage F of a
  clustered or robust model; a paper's printed F that matches Cragg–Donald
  while the second stage is clustered is itself a finding. When Stata's
  `weakivtest` fails or refuses an `ivreghdfe` / multi-way-FE fit (because
  `weakivtest` rejects absorbed FEs or `ivreghdfe` post-estimation), never
  log MOP effective F as "unavailable in the tools used": either partial out
  the exogenous controls and absorbed FEs from `y`, `endog`, and `Z` via
  `reghdfe …, absorb(…) resid` and run `ivreg2` + `weakivtest` on the
  residualised variables, or compute `F_eff = π̂' Q̂_ZZ π̂ / tr(Σ̂_ππ Q̂_ZZ)`
  directly from the first-stage regression of the endogenous variable on the
  excluded instruments under the design's VCE (MOP 2013 eq. 3; for a single
  instrument this is the robust/clustered Kleibergen–Paap first-stage F).
  The source-audited cribs for this row:
  `../../references/methods/stock_yogo_2002_weak_instruments.md` (i.i.d.-error
  bias and size critical values, and why "F > 10" is a one-cell folklore
  rule) and `../../references/methods/montiel_olea_pflueger_2013_weak_iv.md`
  (the effective-F test under robust/clustered/HAC errors — the version
  that applies when the second stage isn't i.i.d.). The survey-level crib
  `../../references/methods/weak_iv_guides_andrews_stock_sun_keane_neal.md`
  adds the claim-matched thresholds (F ≥ 50 for "2SLS beats OLS" in the
  archetype, F > 104.7 for exact 5% t-test size) and the
  contaminated-subsample warning: 2SLS SEs run artificially small precisely
  where the estimate is most OLS-contaminated, so an IV estimate near the
  OLS point estimate with a smaller SE is the signature of that failure
  mode, not precision. Same crib: Anderson–Rubin (or CLR) in lieu of the
  t-test even at strong first stages — t/Wald IV output alone is a gap
  whatever F says.
- **Sensitivity to plausible controls.** Add the controls the exclusion
  story implies should be innocuous; movement in the IV estimate is evidence
  about exclusion, not a nuisance. The sharp version: when the paper
  controls a continuous confounder with coarse bins, re-run varying only
  that control to finer bins or continuous — if significance dies AND the
  first-stage F collapses, the instrument was proxying the confounder (its
  strength was between-bin variation). That is an exclusion red flag, not a
  power loss.
- **Instrument validity has a test where it applies — run it, don't assume
  exclusion.** For a binary treatment with a discrete instrument
  (randomized-encouragement designs are the canonical case), the LATE
  identifying assumptions have testable implications: the implied complier
  outcome densities must be nonnegative, and Kitagawa's variance-weighted
  KS statistic tests this with a single instrument — no overidentifying
  restriction needed, so it works exactly where Sargan/Hansen is vacuous.
  A rejection means exclusion/monotonicity fails; a paper that asserts
  "the instrument is plausibly exogenous" where this test applies and does
  not run it has an unchecked assumption. Crib:
  `../../references/methods/kitagawa_2015_instrument_validity.md` (scope:
  binary treatment, discrete instrument; Huber–Mellace and Mourifié–Wan
  are alternative tests for the same binary/discrete case, Mourifié–Wan
  with covariates — for a continuous instrument, state the gap).
- **A constructed treatment may BE the instrument.** When the treatment
  variable was built using the instrument (or geography collinear with it —
  e.g. treatment attributed by where the instrument is measured), the first
  stage is mechanical and the just-identified 2SLS is circular: it keeps
  only the instrument-projected component and identifies the instrument's
  effect relabelled, not the treatment's. Test the conjecture, don't assert
  it — the RF/FS decomposition: re-estimate dropping the leverage units and
  report β beside its first-stage (instrument→treatment, where construction
  enters) and reduced-form (instrument→outcome, construction-free)
  components. A collapse running through the RF is a geography/
  external-validity finding; through the FS, a construction artifact.
- **Leave-group-out first stages.** Where the instrument's variation has
  natural groups (regions, cohorts, industries), re-estimate leaving each
  out; an instrument whose strength lives in one group is a different design
  from the one described.

## Conditional checks — run when the trigger is present

- **Overidentification diagnostics** — when multiple instruments exist.
  Passing overidentification tests under correlated invalidity proves
  little; say so if the instruments share a source.
- **Monotonicity and treatment margins** — when the paper makes LATE claims:
  who are the compliers, and is the no-defiers assumption plausible?
- **Spatial dependence** — when the instrument is geographically smooth. A
  smooth instrument sails through unit-level clustering untouched; apply the
  spatial checks from the battery's spatial record.
- **Placebo conditioning on the instrument.** Diff each placebo
  regression's actual controls against its table note. A placebo that
  silently conditions on the real instrument (or a close correlate) can pass
  for the wrong reason — the genuine signal is partialled out. Re-run it
  exactly as the note describes, without the hidden control, before
  believing it.
- **Magnitude–validity non-separation.** An implausible elasticity on a
  weak or placebo-leaking instrument — especially IV running above OLS — is
  the invalidity surfacing as a number, not a cosmetic blemish on a valid
  design. Never conclude "the magnitude is meaningless but the effect
  exists"; the defensible object is the reduced-form correlation, stated as
  a fact about the units, not the treatment.
- **Omitted-variable-bias sensitivity on the exclusion restriction** — when
  identification rests on an assumed-as-good-as-random instrument. Compute
  the robustness value for the instrument (the `iv.sensemakr` approach on
  the Anderson–Rubin fit; formulas and the benchmarking protocol in
  `../../references/methods/cinelli_hazlett_2020_sensitivity.md`): how strong an
  unobserved confounder of the
  instrument would have to be, benchmarked against named observed
  covariates, to overturn the finding. A robustness value near what a single
  named covariate already explains is a different finding from one no
  plausible confounder could reach — report which. The robustness value is
  NOT a verdict; it quantifies how much confounding the claim can absorb,
  not whether such confounding exists.

See the OVB-sensitivity record in the battery's `../../references/design-matrix.md`
for the required fields, and `../../references/software-examples.md` for tested
command patterns.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record exclusion threats and identification findings in the module report's `## Leads for later stages` (folded into the `code-and-data` report) for `claims` as design-validity evidence the
moment they appear — they bear on what story the estimate can support, not
only on the battery verdict.
