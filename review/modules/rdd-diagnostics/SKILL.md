---
name: rdd-diagnostics
description: >-
  Diagnostics for regression-discontinuity and regression-kink designs —
  sharp, fuzzy, discrete-score, multi-cutoff and geographic: which output row
  carries the verdict, bandwidth sensitivity, density and manipulation tests
  with manipulation-robust bounds, covariate continuity and covariate
  adjustment, placebo cutoffs, donut checks, RD plots, local-randomization
  inference, boundary-discontinuity estimation, extrapolation claims,
  heterogeneity and power. Invoke from `code-and-data` whenever a target
  result uses a cutoff, a kink in a policy schedule, or a boundary.
---

# RDD diagnostics

Re-run the design the way its method's authors prescribe, then test whether
units could sort across the cutoff. The published fit shows the cutoff at
its most flattering — one bandwidth, one polynomial, one kernel, one plot.
The checks below hold it to the published procedure (robust bias-corrected
inference at data-driven bandwidths, the falsification battery) and decide
whether the design identifies at all.

Trigger: any target result identified off a cutoff, a kink, or a boundary —
sharp, fuzzy, discrete-score, multi-cutoff, or geographic. `NOT_APPLICABLE`
when no meaningful cutoff exists; do not run placebo cutoffs on a design
without one.

Method cribs (source-audited; the index and what each governs is
`../../references/methods/rdd_methods_guide.md` §0). Cite the underlying
methods work (author, year, and page or section) behind every verdict-bearing
rule you apply, never the crib filename or crib section number. Code is in the
battery's `../../references/software-examples.md`.

## Software versions

Record the installed version of every RD package you run (`packageVersion`
in R, `which` in Stata) and, where the replication package states it, the
version the authors used; check the version after installing, because
prebuilt binaries can lag the source release. The packages change numbers
and calls between releases, so a mismatch with a paper's printed bandwidth or
estimate can be a version artefact rather than an author error:

- `rdrobust` 3.0.0: HC2/HC3 bias-regression residuals use the q-order
  leverage, so robust SEs under `vce = "hc2"/"hc3"` move slightly.
- `rdrobust` 4.0.0: clustered variance remapped — with `cluster`, the default
  `vce = "nn"` silently becomes CR1, `hc0`/`hc1` become CR1, `hc2`/`hc3`
  become CR2/CR3 — so every clustered bandwidth, SE and p-value changes
  (by a few percent with dozens of clusters, by multiples with a handful);
  `all`/`detail` moved from `rdrobust()` to `summary()`; the legacy CCT/IK/CV
  selectors (`rdbwselect_2014`) were removed.
- `rdrobust` 4.1.1 (October 2026; Python 2.1.x, Stata 11.1.x): standardisation inside bandwidth selection on by default; padded
  `bwcheck` floor; default `ginv.tol` 1e-15; a halved point estimate in sharp
  designs with covariates and `deriv >= 2` corrected; a stop with "Not enough
  variability" when a side has too few distinct running-variable values; a
  warning when either side has fewer than 10 clusters inside the bandwidth.
  Unclustered default fits agree with earlier releases to about seven
  significant figures.
- `rdlocrand` 3.0: window-selection and mass-point indexing bugs in 1.1 and
  2.0 fixed, so selected windows and downstream p-values change; polynomial
  (p > 0) inference is HC-robust large-sample (HC3 default) and no longer
  reports a permutation p-value; unsupported polynomial requests fall back to
  p = 0 with a warning.
- `rddensity` 2.5 and 3.0 give the same numbers; both run the mass-point
  adjustment and a table of binomial tests by default, which the 2018
  software article predates.
- Current `rdpower` and `rdhte` require `rdrobust` ≥ 4.0.0; where a project
  must keep an older `rdrobust` to reproduce a paper, install the current
  packages in a separate library.

Never allege an error in a paper's RD numbers until the version is matched
or the gap is shown to survive it. Run the current release for the review's
own estimates and say so.

## Core checks

- **Which row carries the verdict.** High-order global polynomials are not
  defensible estimates; re-estimate with a local linear fit (triangular
  kernel) at a data-driven bandwidth. The headline is the conventional point
  estimate at the MSE-optimal bandwidth with the robust bias-corrected (RBC)
  interval and p-value; add the RBC interval at the CER-optimal bandwidth.
  The robust interval is centred on the bias-corrected point; quote it as
  printed and never re-centre it on the conventional estimate. In
  `rdrobust` ≥ 4.0.0 the default `summary()` prints one row — the
  conventional point estimate beside the robust z, p and interval;
  `summary(f, all = TRUE)` prints the conventional, bias-corrected and robust
  rows (in ≤ 3.0.0, `rdrobust(..., all = TRUE)`); `f$coef`, `f$se`, `f$pv`,
  `f$ci` hold the three rows in that order in every version. `vcov()` on an
  `rdrobust` fit is diagonal with placeholder zeros — never use it to test
  one row against another. A conventional SE,
  interval or star at an MSE- or CER-optimal bandwidth is the combination
  the selector's authors declare invalid and is reported only as a
  diagnostic. Four traps (`calonico_cattaneo_farrell_rbc_bandwidth.md`):
  - a t-ratio formed as the conventional coefficient over the robust SE is
    neither test. When only the robust interval is printed, its midpoint is
    the bias-corrected estimate and half its width over 1.96 is the robust
    SE; a printed z or p inconsistent with them means rows were mixed;
  - a point estimate taken from a `cerrd`/`certwo` run is undersmoothed, not
    MSE-optimal;
  - a local-quadratic interval at the local-linear MSE bandwidth is the RBC
    interval with ρ = 1 — not an independent robustness check;
  - a bootstrap of the conventional estimator, or an ad hoc smaller
    bandwidth with conventional SEs, does not remove the bias.
- **Bandwidth and order sensitivity over a small range.** Report τ̂ and the
  RBC interval at hCER, hMSE, 2·hCER and 2·hMSE, and at p = 1 and p = 2,
  passing b (or ρ) explicitly whenever h is set by hand
  (`rd_practice_guide.md` §6.5). Judge stability of the point estimate and
  overlap of the intervals. A loss of significance at hCER that comes from a
  longer interval is not fragility; drift at bandwidths far above hMSE is
  smoothing bias, not evidence against the paper. A result that holds only
  at a hand-picked bandwidth far from hMSE is fragile. Kernel changes
  rarely move estimates and carry little weight.
- **Density test.** Manipulation of the running variable is the design's
  central threat. Run `rddensity` (not a histogram, not McCrary's binned
  test) and quote the Robust row only — the conventional row over-rejects
  at the default bandwidth. Report the bandwidths, the effective N and the
  two density estimates on each side, and τ̂ = 1 − f̂(c−)/f̂(c+)
  (`cattaneo_jansson_ma_2020_density_test.md`). A rejection that appears only
  under `fitselect = "restricted"` rests on that restriction. Before reading
  a jump as manipulation, rule out mechanical causes: calendar artefacts,
  round-number heaps at the cutoff, a mass exactly at the cutoff value. A
  non-rejection is weak evidence — the test is low-powered and density
  continuity is neither necessary nor sufficient for validity — and is never
  recorded as clearance. Record its detectable jump — the review's own power
  calculation, not the authors': about 2.80 × the jackknife SE of the density
  difference (`sd_jk$diff`) at 80% power and two-sided 5%, set against the
  density level on each side. Mass points decide the route: with few distinct
  values near the cutoff the continuity test is not verdict-bearing — the
  binomial test in the smallest and the chosen window (via `rdwinselect` or
  `rddensity`'s binomial output) plus in-window covariate balance decides,
  with the continuity test reported beside it if it runs; with many, run
  `rddensity` with its mass-point adjustment and state the count.
- **Manipulation-robust bounds.** For every load-bearing estimate where
  one-sided manipulation is institutionally possible, run the Gerard–
  Rokkanen–Rothe bounds whatever the density test says, and report τ̂ with
  its interval and the breakdown τ* (the largest manipulation share at which
  the interval still excludes zero). If the upper confidence limit for τ
  exceeds τ*, the result is not robust to manipulation the data cannot rule
  out. The bounds concern non-manipulating compliers and assume manipulation
  in one direction and a continuous score; state the side manipulators can
  reach and why, from institutions (`rdd_methods_guide.md` §2). The authors'
  R and Stata implementation is `rdbounds`.
- **Predetermined covariates and placebo outcomes.** Run each covariate and
  placebo outcome through the headline's *procedure* — `rdrobust` with the
  covariate as outcome and RBC inference — at its *own* data-driven
  bandwidth (CER-optimal preferred for testing, MSE-optimal acceptable).
  That is the authors' test (`rd_practice_guide.md` §6.1). Also report each
  covariate's estimate at the headline bandwidth, labelled as the review's
  supplement: a covariate that balances only at its own bandwidth is a
  finding, and at a common bandwidth these estimates, with the adjustment
  coefficients, give the exact shift a covariate adjustment produces
  (`calonico_etal_2019_rd_covariates.md` §6).
  Test every covariate expected to move under manipulation. Grade a
  rejection by its magnitude and its relevance to the outcome; one small
  imbalance among many is reported, not decisive. Covariate imbalance with a
  continuous density is sorting the density test cannot see — report it as
  design-validity evidence on its own. In `rd2d`, test covariates point by
  point along the boundary (boundary bullet below).
- **Placebo cutoffs.** Estimate at a grid of artificial cutoffs on each side
  of the true one using only that side's observations (controls below,
  treated above), with the bandwidth reselected at each cutoff and RBC
  inference; report effective N, which shrinks near the true cutoff. A
  placebo that pools observations across the true cutoff is invalid and is
  redone. Also scan IMSE-binned means for jumps away from the cutoff, which
  global fits hide, and test any you find as a placebo cutoff.
- **Donut.** Drop |X − c| < r for several small radii, letting the bandwidth
  be reselected, and report per radius the bandwidth, estimate, RBC interval,
  effective N and excluded count on each side. It tests manipulation on the
  assumption that manipulators sit inside the radius, and sensitivity to the
  extrapolation the nearest observations drive; run it in every RD. A
  conclusion that flips once a handful of nearest units is dropped is
  fragile. A donut changes the estimand — say so.
- **RD plot.** Record the paper's bin type, bin count, polynomial order and
  fit window. Re-plot with data-driven bins (the `rdplot` default
  evenly-spaced mimicking-variance bins, plus IMSE `es` and `qsmv`) and with
  the local linear fit inside the `rdrobust` window, whose intercept gap
  should match the reported estimate. The default `rdplot` line is a
  *global* order-4 polynomial over the full support; a jump that appears
  only under the paper's bin choice or only in the global polynomial is a
  presentation finding. The plot never settles the jump — the RBC estimate
  does (`calonico_cattaneo_titiunik_2015_rd_plots.md`).

## Conditional checks

- **Covariate-adjusted headline** — when the RD regression includes
  controls or fixed effects. The unadjusted RBC estimate at its own
  MSE-optimal bandwidth is the benchmark. The adjusted estimate targets the
  same effect only if every covariate is predetermined and balanced at the
  cutoff, enters additively with a common coefficient (not interacted with
  treatment, not demeaned by side), and the bandwidth and RBC inference
  were re-selected with the covariates (`covs` in both `rdbwselect` and
  `rdrobust`). When adjustment moves the estimate, re-fit the adjusted
  model at the unadjusted bandwidth to split the move into a bandwidth part
  and an adjustment part; the adjustment part equals −τ̂Z(h)′γ̃Y(h) exactly.
  A material shift traced to covariates that jump at the cutoff is
  imbalance, a design-validity finding, not a better-controlled estimate.
  Significance that appears only after adjustment rests on the efficiency
  argument, which holds only under balance. Missing covariates shrink N —
  compare samples (`calonico_etal_2019_rd_covariates.md`).
- **Fuzzy RD** — when take-up, not just assignment, is discontinuous at the
  cutoff. Report the first stage first, with its RBC interval and an F
  statistic, stating how it was computed (the source gives no definition). Below
  F = 20 the ratio is not interpretable as a treatment effect and the claim
  falls back to the intention-to-treat effect. The ratio must come from one
  bandwidth with RBC inference (`rdrobust(..., fuzzy = d)`), not from two
  separately estimated effects. τ_FRD is the complier effect at the cutoff
  under exclusion and monotonicity; a paper that presents it as the effect
  for all units overclaims unless it defends local independence. Run the
  density and covariate tests on assignment, not take-up, and plot the
  first stage beside the reduced form (`rd_practice_guide.md` §7).
- **Regression kink design** — when identification comes from a change in
  the *slope* of a policy rule (benefit cap or floor, tax bracket, phase-out)
  or any `deriv = 1` estimate. Reconstruct the policy rule from the statute
  and record the slope change used as denominator; if the rule's level also
  jumps at the kink, the kink estimand needs a constant-effect assumption or
  an RD estimate instead. Test each covariate for both a level jump (`deriv = 0`)
  and a slope change (`rdrobust(..., deriv = 1)`), and test the score density for
  a level jump via `rddensity` (`fitselect = "unrestricted"` — never the
  restricted fit, which imposes equal slopes at the kink) plus a slope change in
  the binned density (`regression_kink_guide.md` §4); visible bunching at the
  kink fails the design. Report p = 1 and p = 2
  across default, unregularised (`scaleregul = 0`) and, for fuzzy kinks,
  ratio-targeted selectors, each with RBC intervals. Run the paper's exact
  estimator at 100 or more placebo kinks where the policy has none and
  report the share significant under the paper's inference and the
  Ganong–Jäger permutation p-value: RBC alone does not control size under
  curvature. A fuzzy kink needs a large share of observations exactly on
  the statutory schedule and kinks of one sign; its first stage must survive
  bias correction. Scale `deriv = 1` output by the policy slope change before
  comparing, and set `p` explicitly. A null kink estimate needs a power
  demonstration from the placebo distribution (`regression_kink_guide.md`).
- **Discrete running variable and local randomization** — when the score
  takes few distinct values near the cutoff, or the paper reads its design
  as a local experiment or reports randomization inference. Count the mass
  points within the window on each side and the observations per point; the
  count decides the route (`rd_local_randomization_guide.md` §7). With few
  mass points: (i) the continuity density test is not verdict-bearing and the
  binomial test in the smallest and the chosen window plus in-window
  covariate balance decides; (ii) the local-randomization analysis is verdict-bearing and
  any continuity estimate is a parametric extrapolation between the nearest
  mass points, reported as such; (iii) both decisions go in the estimand
  record. Choose the window on predetermined-covariate balance
  (`rdwinselect`, α* = 0.15 where possible and never below 0.10, a small
  observation step) or,
  with a discrete score, start from the two mass points adjacent to the
  cutoff and enlarge one point at a time. Re-test in windows *inside* the
  chosen one; agreement only in wider windows is not support. Report the
  Fisherian p-value for the sharp null and the large-sample p-value for the
  average effect, labelled, with the effect model behind any interval.
  Because `rdrandinf` (`ci()`) and `rdsensitivity` (`tlist()`) invert
  confidence intervals over the supplied effect grid and silently clamp the
  interval at the grid endpoints when the grid is too narrow, assert that
  neither bound of the returned interval (`r(CI)` / `ri$ci`) equals
  `min(grid)` or `max(grid)` — if it hits an endpoint, widen the grid and
  re-run (or report that direction as unbounded when widening still does not
  reject). Label every estimate with its estimand — the window average θ or the
  cutoff effect τ; they are not the same target. A window taken from an MSE
  or CER selector is not a local-randomization window. A local-randomization
  fit with p = 1 is the local linear estimator with a uniform kernel and
  h = w — not independent corroboration. When a paper clusters standard
  errors by the running variable, recompute unclustered EHW errors: any
  interval with correct coverage is at least as wide, so significance that
  holds only under clustering fails (`kolesar_rothe_2018_discrete_rdd.md`).
  With rich support, a narrower window with EHW errors is the first remedy;
  otherwise a Kolesár–Rothe BSD interval over a stated, justified range of
  the curvature bound K. Heaping of a continuous latent score belongs to the
  donut check, not this one.
- **Boundary-discontinuity designs** — an RD whose score is a
  two-dimensional location or distance to a border, including pooled
  distance-to-border regressions and contiguous-pair comparisons.
  **GATE: this check is not done until the aggregate is on disk.**
  (`rd_boundary_designs_guide.md`.)
  1. Classify the paper's pooled border regression by the Cattaneo–Titiunik–
     Yu specification taxonomy and record treatment interaction, bandwidth
     source and inference. Segment fixed effects do not make a border
     regression an RD; a specification without the treatment × score-
     polynomial interaction, an ad hoc bandwidth, or conventional inference
     at an MSE-sized or wider bandwidth is each a finding. A contiguous-pair
     comparison is at most a pooled local-constant boundary comparison with
     fixed localisation; the compound-treatment, sorting and balance checks
     still apply to it.
  2. Fit location-based `rd2d` with the covariance stored
     (`params.cov = "main"`), clustered at the paper's level with the default
     joint fit, and an evaluation grid spaced by arc length that includes the
     border's kinks and corners and only points with data on both sides.
     Project coordinates first; Euclidean distance on raw latitude and
     longitude is wrong.
  3. Report the **WBATE** with stated weights and RBC interval. The pooled
     border estimate targets a *density-weighted* average of the boundary
     effect curve, so the like-for-like comparison is the density-type WBATE
     (weights proportional to observations near each grid point). That
     limit is derived for the local difference in means and carries over to
     the treatment-interacted specifications; a regression with segment fixed
     effects and a common treatment coefficient has implicit weights that
     need not be the density weights — record which specification the paper
     ran. An
     equal-weight WBATE is a second, differently weighted average. The
     WBATE interval is centred on the bias-corrected aggregate, so the
     printed point can lie outside its own interval — quote both as printed.
     A hand average of the point estimates reproduces the equal-weight point
     but has no valid standard error; never report one.
  4. Report the **BATEC** with a **uniform** band (`cbands`). Claims about
     where along the border the effect is present, absent, larger or
     smaller are judged on the uniform band, never on counts of pointwise
     significant points. Without the stored covariance `summary()` stops
     with an error; without `cbands` it returns no band. Either is an
     incomplete check — repair it or record
     BLOCKED with command proof; the stage stays INTERIM only while an
     untried repair remains. **LBATE** only when a largest-effect claim is
     made.
  5. Distance-based estimates (the paper's per-point distance RDs or
     `rd2d.distance`) at grid points within a bandwidth of a kink or corner
     of the border carry first-order bias that RBC does not remove; refit
     them location-based and with the distance fit's kink options. The
     location- and distance-based fits target the same curve; a gap between
     them is a geometry or support diagnostic. Give each estimator and
     weighting its own `estimand_id` (e.g. `rd2d_WBATE_density_location`,
     `rd2d_WBATE_equal_location`, `rd2d_WBATE_density_distance`,
     `rd2d_BATEC_point`, `rd2d_LBATE`) — `../../scripts/check_manifest.py`
     keys its consensus check on that field.
  6. Overlay the other administrative borders (county, district,
     municipality) segment by segment. Where they coincide with the
     treatment border, the estimate identifies the treatment only under
     compound-treatment irrelevance; require restriction to segments where
     the other units are constant, pre-period placebo outcomes, or relabelling
     as the compound effect.
  7. Test covariates point by point along the border with a uniform band and
     a covariate WBATE; a pooled balance table can hide segment-level
     imbalance. If coordinates are shared centroids, the score has mass
     points — route to the discrete check.
  A report that only quotes the min/max of the pointwise curve has used
  `rd2d` as a heterogeneity check and has **not** completed this check.
  Where the design is genuinely one-dimensional, mark it `NOT_APPLICABLE`.
- **Multiple cutoffs or scores** — when units face different thresholds,
  cutoffs are cumulative doses, a close-election RD has three or more
  candidates, or the design has two non-geographic running variables.
  Classify the design as cumulative or non-cumulative. A normalised-and-
  pooled estimate is a weighted average of cutoff-specific effects, with
  weights proportional to each cutoff's frequency times the score density at
  it (and, in fuzzy designs, its complier share) — not the mean across
  cutoffs. Report `rdmc`'s cutoff-specific estimates and estimated weights
  beside the headline, and restate it as a density-weighted average, or as
  approximately one cutoff's effect if that cutoff carries most of the
  weight. With cumulative cutoffs each estimate is the increment from the
  previous dose and must use only units between neighbouring cutoffs. Test
  differences across cutoffs on the bias-corrected estimates and robust
  variances (`out$B`, `out$V`), not the printed conventional coefficients.
  Reading those differences as variation of the effect with the score needs
  cutoff ignorability, which is untenable under cumulative cutoffs. Run the
  density and covariate tests within each cutoff subsample as well as
  pooled. Two-score designs give boundary-point effects plus a pooled
  distance effect, not "per-score" effects; geographic coordinates go to the
  boundary check, not `rdms` (`rd_multiple_cutoffs_guide.md`).
- **Extrapolation away from the cutoff** — when the paper states an effect
  for units away from the cutoff: other scores, the average applicant, a
  scaled-up or universal programme, a moved threshold. That is an
  external-validity claim and is graded unsupported unless the paper names
  and defends an extrapolation assumption. For the multi-cutoff
  constant-bias method record the target group and score range, the
  direction, both falsification tests with their power, whether the cutoff
  groups differ by period or place, and inference that includes the
  covariance between the two fits. Claims beyond the highest or below the
  lowest cutoff, or for populations never exposed to a cutoff, are not
  identified by it. A failure turns the claim from estimated to assumed —
  unsupported, not refuted (`rd_multiple_cutoffs_guide.md` §6). Hand the
  claim to `claims`.
- **Heterogeneous RD effects** — when the paper claims the discontinuity
  differs across a subgroup. Separate subgroup fits are legitimate; what
  fails is conventional SEs at an MSE-optimal bandwidth and two subgroup
  intervals compared by eye. Require RBC intervals per subgroup and an RBC
  interval or test for the *difference* — `rdhte_contrast`, which refits at
  the bandwidth optimal for the contrast, or `rdhte_lincom` at the
  per-group bandwidths; they give different intervals, so name the one
  reported. One significant subgroup beside one insignificant one is not
  heterogeneity. `rdhte` defaults to `vce = "hc3"`, not `rdrobust`'s
  nearest-neighbour variance; match the paper's variance and clustering.
  Test the heterogeneity variable itself for a jump at the cutoff — it must
  be pretreatment. Record common versus group-specific bandwidths and re-run
  with the other; a difference present under only one choice is fragile. A
  continuous heterogeneity variable imposes linearity — compare with a
  binned fit. The coding of the variable (median split, quartiles) is part
  of the estimand. Re-run with the smallest bandwidth in the set, the
  authors' choice for robust inference. `rdhte` covers sharp designs only; an overall effect is
  never built by averaging subgroup effects (`calonico_etal_2025_rd_hte.md`).
- **Minimum detectable effect** — when a null or small RD result is
  load-bearing. Compute power or the MDE with the RBC power function
  (`rdpower` / `rdmde`) at the paper's own bandwidth, order, kernel,
  covariates and clustering, against an effect fixed from outside the data —
  never the paper's own estimate. Conventional-variance power is not
  admissible. Without the data, the MDE at 80% power and two-sided α = 0.05
  is approximately 0.71 × the width of the printed RBC interval. A null whose
  MDE exceeds the smallest effect the paper claims to rule out is
  uninformative about it (`cattaneo_titiunik_vazquezbare_2019_rd_power.md`).
  For local-randomization headlines, use randomization power instead.
- **Spatial dependence** — for geographic RDDs, apply the battery's spatial
  record to the paper's own pooled border regression. For `rd2d` fits report
  clustered (joint) results and state that spatially robust uniform
  inference has no source-backed implementation. If assignment is at the
  area level, count the areas: the design may have as few as two units.
- **Clustering.** Every `rdbwselect` selector, MSE and CER alike,
  re-selects h and b with the cluster-robust variance, so clustered and
  unclustered default runs use different windows and the clustered SE can
  come out smaller or larger. The CER selectors also rescale by the number of
  clusters instead of N, which makes the CER bandwidth a larger fraction of
  its MSE base; the MSE base itself can move either way. State the `vce`
  behind every clustered number (in `rdrobust` ≥ 4.0.0, CR1 unless `cr2`/
  `cr3` is set). Compare SEs at fixed h and b before
  attributing a change to clustering, and never write "clustering enlarges
  every SE" or any all/every/none claim over a spec grid without running the
  whole grid — when SE direction is mixed, report the significance count.
  Clustered RBC inference needs many clusters inside the window: read the
  per-side cluster counts `rdrobust` prints, and route fewer than about 10
  on a side to `small-n-diagnostics`.
- **Unstated bandwidth: back it out from printed N.** First establish which
  N the column reports — total, the effective N inside h on each side, or
  the sample left after covariate missingness. Then, on each side
  separately, sort the absolute running variable in the estimation sample
  (after any donut): the N-th value on that side is the implied window edge
  for that side, an interval rather than a point when values tie. Validate
  on columns whose windows ARE stated, then sweep candidate selectors
  (`rdbwselect` variants including `msetwo`/`certwo`; legacy CCT/IK/CV via
  `rdbwselect_2014`, which exists only in `rdrobust` ≤ 3.0.0; Fan–Gijbels for
  kinks × kernel × order × covariates ×
  vce and clustering × `scaleregul` × fuzzy target × donut × package
  version), judging hits by implied window N with a tolerance scaled to the
  window and the ties. A CER bandwidth for p = 1 without clustering is
  n^(−1/20) × the MSE bandwidth with b unchanged — a usable signature.
  Demand a *joint* hit across every column, and run the sweep on the
  published data series as well as your rebuild; a match on only one
  identifies their outcome data too. A null result — no selector and version
  fits all columns — is itself a finding: the "optimal" label is
  unrationalizable.

The local-randomization, boundary-discontinuity, regression-kink and
RD-extrapolation records in the battery's `../../references/design-matrix.md`
list the fields a complete run reports.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error).
Record sorting evidence, confounded-boundary findings, estimand changes
(complier, window, density-weighted, non-manipulator), and extrapolation
claims in the module report's
`## Leads for later stages` (folded into the `code-and-data` report) for `claims` as design-validity evidence — a
boundary that separates more than the treatment is a story problem, not
only a statistical one.
