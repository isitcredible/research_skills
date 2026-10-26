---
name: did-event-study-diagnostics
description: >-
  Diagnostics for difference-in-differences and event-study designs:
  treatment-timing inventory, estimator validity under heterogeneous
  effects, pre-period paths, anticipation, alternative comparison groups,
  and terminal-period sensitivity. Invoke from `code-and-data` whenever a
  target result compares units across treatment timing.
---

# DiD and event-study diagnostics

Interrogate the estimator, the comparison group, and the timing structure
each on its own terms. A two-way fixed-effects regression on staggered
adoption can put negative weights on some treatment effects and average
them into a number that represents no group's experience — so "parallel
trends look fine" plus a TWFE coefficient is not yet a validated design.

Trigger: any target result identified off treatment timing across units.
`NOT_APPLICABLE` when there is no adoption event or timing variation.

Method crib (source-audited):
`../../references/methods/did_event_study_guide.md` — estimand
decomposition, pre-test power, HonestDiD bounds, Conley–Taber routing.
`../../references/methods/schmidheiny_siegloch_2023_event_studies.md` —
endpoint binning is the identifying restriction when there are no
never-treated units; an unbinned saturated event study is underidentified
and "we bin at ±k" is an assumption to defend (are effects flat beyond
k?), not a footnote. Event-study and distributed-lag parameterizations
are numerically identical under correct reparametrization.
`../../references/methods/callaway_goodmanbacon_santanna_2024_continuous_did.md` —
continuous/dose treatments: even with two periods a TWFE dose coefficient
suffers from "at least one of three problems: negative weights, selection
bias, or non-intuitive weighting" (negative weights in its level-effect
decompositions), and the dose-response gradient mixes effect with
selection into dose — a dose gradient is not causal evidence by itself.
`../../references/methods/olden_moen_2022_triple_difference.md` (interim)
— DDD needs one parallel-trend assumption, not two, but only because
equal biases cancel across the third margin; the cancellation is an
assumption to defend, not a free robustness argument.

## Core checks

- **Adoption and timing inventory.** Which units adopt, when, whether
  adoption is staggered, whether treatment is absorbing or units switch
  out (reversible treatment invalidates the standard event-study estimators
  differently — it routes to dCDH's DID_M, which separates joiners from
  leavers), and whether any units are always- or never-treated.
  This inventory decides which estimators are valid; do it first. Count
  always/never-treated from the estimation sample itself (`frac_treated =
  mean(treat)` by unit on the exact regression frame) — not from the paper's
  text or a prior memo. Units that enter the panel already treated are
  always-treated; that usually means the coding is an external
  classification, not a discrete intervention — a substantive finding in
  itself.
- **Treatment intensity and third-margin variants.** If the treatment is
  continuous or multi-valued (dose, exposure, spending level), the binary
  toolkit does not carry over: even in two periods the TWFE dose
  coefficient carries at least one of negative weights (level-effect
  readings), selection bias (cross-dose readings), or non-intuitive
  weighting, and comparing ATT across doses
  mixes effect with selection into dose — route to the CGBS estimators or
  a defensible discretization, and demand the stronger assumption that
  handles selection into dose. For a staggered dose, the event-study ATT
  averaged over doses, or within a dose band, needs only ordinary parallel
  trends and is estimated with the binary staggered estimators (zero-dose
  units as never-treated, the sample cut to the band; CGBS 2024 AEA P&P,
  Thm 1); dose-response and causal-response claims still need the stronger
  assumption. If the design is triple-difference
  (group × post × eligibility margin), name the single load-bearing
  parallel-trend assumption and check the bias-cancellation condition —
  equal bias across the third margin — rather than accepting "three
  differences so it's robust"; heterogeneous selection across the margin
  kills the cancellation. And for any event-study figure without a
  never-treated group, ask what endpoint-binning normalization identifies
  the path and whether the plotted coefficients include the binned
  endpoints or suppress them.
- **Estimator validity under heterogeneous effects.** With staggered
  adoption and effects that vary by cohort or over time, re-estimate with an
  estimator robust to that heterogeneity and compare it with the TWFE
  number. First name the claimed estimand and its aggregation — overall ATT,
  event-time path, or cohort×time grid — because Callaway–Sant'Anna,
  Sun–Abraham, imputation, and stacked estimators embed different
  control-group defaults and different aggregations; "the robust number" is
  not one number. State which identifying assumption the chosen estimator
  adds (no-anticipation, conditional vs unconditional parallel trends) and
  which control-group convention it defaults to. When the decomposition
  shows negative-weighted/forbidden comparisons carrying the estimate and
  the heterogeneity-robust estimates diverge materially from it (the
  published coefficient outside the robust estimate's confidence interval,
  or a change of sign; a change of significance with overlapping point
  estimates is a precision difference, reported as such), flag
  the published coefficient `validity = invalid`, naming the convention in
  its `results.csv` row's `notes` (the forbidden comparisons and the weight
  they carry): it is a non-estimand — an artifact of the estimator, not
  "a different estimate" — and may be quoted only as such. A gap between the robust estimand and the
  published number is a finding about the published estimate.
- **Event-time coefficient path with uncertainty — and its power.** Every
  event-time coefficient, not a pooled post dummy (endpoint bins stay, with their
  normalization defended as above). Pre-period coefficients test the design;
  post-period dynamics test the story's timing. Two readings:
  (a) read the pre-period coefficients against their base period. Under a
  universal base (one omitted reference period; `csdid, long2`;
  `did` with `base_period = "universal"`), a common non-zero offset is a
  step at the reference period — anticipation or a violation, not a pass;
  test the *slope* (last 2–3 pre-period coefficients equal to each other,
  or a linear pre-trend) and the step against the reference period
  separately. Under a varying base (the `csdid`/`did` default), each
  pre-period coefficient is a one-period change, so a common non-zero
  offset is a linear trend: test the coefficients' equality to zero —
  equality to each other passes a trend; (b) when the published "post"
  indicator pools three or more treated dates into one dummy, the averaged coefficient can be
  carried entirely by the latest date — read the post-period event-study
  coefficients individually; a flat-then-terminal-spike path is also what a
  late cross-sectional correlation averaged into a long-window DiD looks
  like.
  Then grade the pre-trend read honestly — a non-rejection is NOT
  validation: (i) report what violations the pre-test could detect — the
  Roth (2022, AER:I) pre-test power analysis at the observed coefficient
  covariance (`pretrends`), since a flat path consistent with violations
  large enough to generate the post effect is uninformative; (ii) report the
  HonestDiD sensitivity — the breakdown M̄/Δ (Rambachan–Roth 2023) at which
  the headline conclusion flips — as the quantified version of "how much
  trend violation does this survive". **When feeding `csdid` or R `did` into
  HonestDiD, a universal base period is mandatory** (`csdid …, long2`, never
  default varying base and never `long`, which reverses the pre-period signs;
  R `did::att_gt(..., base_period = "universal")`): running `honestdid` after
  default `csdid` executes without error on period-to-period first differences
  rather than cumulative deviations from the reference period. In Stata
  `honestdid`, `pre()` and `post()` take positive vector positions in `e(b)`
  (read from `matrix list e(b)` after `estat event`), never negative event
  times (`pre(-4/-1)`). `check_inference.py` F11 enforces both; (iii) read the
  path under the paper's
  transform AND under the claim's required scale — parallel trends in levels
  does not imply parallel trends in logs/asinh (Roth–Sant'Anna 2023), so a
  claim needing log-PT is not cleared by a flat levels path; (iv) read it
  under the paper's conditioning set — a path computed without the
  time-varying controls is a different object than the headline's
  identifying assumption.
- **Placebo cutoff inside the pre-period.** When the panel has more than
  two pre-treatment dates, re-run the exact headline spec on the
  pre-period-only sample with the treatment cutoff reassigned to a date
  inside it (mid-pre-period, not on the eve of real treatment; truncate
  year-interacted controls to in-sample years). A placebo "effect"
  comparable in sign, magnitude, and significance means the design detects
  sample-composition / pre-existing gaps, not the treatment — a
  single-number result directly comparable to the printed headline.
- **Anticipation — with a differential diagnosis.** Effects that begin
  before treatment are a design problem, not an early success — but name
  which problem: anticipation proper (an "effect of announcement" estimand
  — legitimate if claimed, tested by shifting the event window), an
  Ashenfelter dip (selection into treatment on a transitory shock —
  biases the post-treatment estimate up), a mis-coded adoption date, or a
  genuine trend failure. They carry different verdicts.
- **Alternative comparison groups.** Re-estimate against never-treated,
  not-yet-treated, and any natural regional comparison; the choice of
  comparison should not carry the result silently. Not-yet-treated controls
  are clean only within pre-adoption windows under no-anticipation — run
  them through the clean-control machinery (Callaway–Sant'Anna / stacked
  specifications), not a second TWFE.
- **Cluster level aligned with treatment assignment**, with the cluster
  counts reported — treated and control clusters separately. G=50 states
  with 3 treated states is a 3-cluster design for the coefficient's
  asymptotics: clustered SEs and the wild bootstrap resample mostly
  controls and do not fix it; use Conley–Taber / assignment-permutation
  inference or mark the design uninformative, and hand the case to
  `small-n-diagnostics`. Report the partial-leverage effective count G*
  beside the nominal counts where leverages are unequal — the nominal G is
  the wrong object when one treated state carries the weight. With enough
  clusters to cluster at all, CV1 intervals still undercover when treated
  and control counts are unequal or effects are heterogeneous, and more
  control clusters make it worse (Hansen 2025, JAE: worst-case coverage
  61% in the baseline design, 36% with unequal treated-cluster sizes; the
  wild bootstrap fails under large heterogeneity). Report the jackknife
  (CV3) SE with Hansen's adjusted t_K/a interval, or Bell–McCaffrey, beside
  the paper's.
- **Collapse test on the point estimate.** The cluster-level check fixes
  precision only. Where the treatment or a key regressor is constant within a
  coarser unit than the analysis rows, also collapse to the genuine units
  (average; drop-to-source for imputed values) and report whether the
  coefficient moves, not just whether the interval widens. See
  `../../references/design-matrix.md`, "Collapse-test record".
- **Terminal-period sensitivity.** Drop the last period or two; results
  that live in the terminal periods deserve to say so.

## Conditional checks

- **Heterogeneous-effect decomposition** — when adoption is staggered:
  decompose the TWFE estimate into its 2×2 comparison components
  (`bacondecomp`; those weights are non-negative) and report the
  forbidden-comparison share; report negative weights on cell-level ATTs
  from `twowayfeweights` (dCDH).
- **Balanced-panel check** — when composition changes over event time:
  re-estimate on the balanced panel to separate composition from dynamics.
- **Spillover checks** — when untreated units may be exposed through
  markets, borders, or networks: an exposed control group biases the
  comparison toward or away from the finding, and the direction is
  knowable.
- **Coincident differential shock.** Trajectory matching — parallel-trends
  tests, SDID weights, in-time placebos — neutralises a *pre-existing
  differential trend* with a pre-period footprint. It does NOT neutralise a
  shock that lands at the same time as the treatment and is correlated with
  treatment status: that shock has no pre-period signature, and flat
  pre-trends are fully consistent with it. When treatment timing coincides
  with a macro shock, ask whether the confound is a trend (matchable) or a
  coincident differential shock (not), whether treatment correlates with
  exposure to the shock, and whether shock controls enter the *preferred*
  estimator.
- **No-event negative-control treatment** — for exposure×post designs
  (suitability, endowment, exposure interacted with post): run a same-family
  variable that had no treatment/introduction event at the cutoff as the
  "treatment" (a same-family suitability or endowment variable with no introduction event at the cutoff).
  If it loads, the design captures the family gradient, not the event —
  cleaner than a substitute *treated* variable, whose loading is ambiguous.
  Where the paper already controls for the placebo variable, run the mirror:
  placebo-as-treatment with the original treatment as control — a symmetric
  loading means the treatment label is arbitrary. Report which outcomes the
  placebo does and does not touch; it may kill one and not another.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record pre-trend violations, anticipation, and comparison-group fragility in the module report's `## Leads for later stages` (folded into the `code-and-data` report) for `claims` —
the timing path is also the mechanism's timeline, and a mismatch between
them is story evidence.
