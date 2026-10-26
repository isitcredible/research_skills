# Continuity-based RD practice and falsification — Cattaneo, Idrobo & Titiunik (2020, 2024); Cattaneo & Titiunik (2022, 2024)

The authors' own recommended practice for local-polynomial RD analysis and
its falsification battery, distilled from four published sources. (1) Matias
D. Cattaneo, Nicolás Idrobo and Rocío Titiunik, *A Practical Introduction to
Regression Discontinuity Designs: Foundations*, Cambridge Elements in
Quantitative and Computational Methods for the Social Sciences (Cambridge
University Press; first published online November 2019, cited by the authors
as 2020), DOI 10.1017/9781108684606, with the authors' erratum of 19 January
2023 applied (§3 below). Cited "F". (2) The same authors, *A Practical
Introduction to Regression Discontinuity Designs: Extensions* (Cambridge
University Press, first published online March 2024), DOI
10.1017/9781009441896; Section 3, "The Fuzzy RD Design" (pp. 36–60), plus
the parts of Section 4 (discrete scores, pp. 60–76) that bear on the
falsification tests. Cited "E". (3) Matias D. Cattaneo and Rocío Titiunik,
"Regression Discontinuity Designs," *Annual Review of Economics* 14 (2022):
821–851, DOI 10.1146/annurev-economics-051520-021409. Cited "ARE". (4)
Cattaneo and Titiunik, "Comment: Protocols for Observational Studies: An
Application to Regression Discontinuity Designs," *Statistical Science*
39(4) (2024): 560–565, DOI 10.1214/24-STS943. Cited "STS". All four audited
in their published versions; page numbers are the printed ones. Source PDFs
(not distributed with the skill):
`Cattaneo_Idrobo_Titiunik_2020_PracticalRD_Foundations_CUP.pdf`,
`Cattaneo_Idrobo_Titiunik_2020_PracticalRD_Foundations_erratum.pdf`,
`Cattaneo_Idrobo_Titiunik_2024_PracticalRD_Extensions_CUP.pdf`,
`Cattaneo_Titiunik_2022_RDD_AnnuRevEcon.pdf`,
`Cattaneo_Titiunik_2024_ProtocolsRD_Comment_STS.pdf`.

Verification status: source-audited 2026-10-15.

Use in this battery: `rdd-diagnostics` core checks (which row carries the
verdict, bandwidth and order sensitivity, density test, predetermined
covariates and placebo outcomes, placebo cutoffs, donut, RD plot) and
conditional checks (covariate-adjusted headline, fuzzy RD, minimum
detectable effect); the design-matrix RD
checklist. Pairs with `rdd_methods_guide.md` (RBC construction, manipulation
bounds) and `kolesar_rothe_2018_discrete_rdd.md` (discrete scores).

## 1. Setting and estimand

- F treats the canonical sharp design: one continuous score, one cutoff,
  perfect compliance, parameter τ_SRD = E[Y(1) − Y(0) | X = c], identified
  by continuity of the two conditional mean functions at the cutoff (F §2;
  scope restated p. 97). The parameter is local: it describes units at the
  cutoff, not the population that received scores (STS p. 561).
- Everything in §§2–6 is the continuity framework. Local randomization is
  the authors' complement and the route when continuity methods are not
  directly applicable (F p. 33; STS p. 562).

## 2. Global polynomials are out; low-order local polynomials are in

- Global fourth- or fifth-order polynomials approximate well overall but
  badly at boundary points (Runge's phenomenon) and can weight observations
  far from the cutoff heavily; since the RD estimate sits at a boundary,
  global fits "can be highly misleading" and the authors "recommend against
  using global polynomial methods for formal RD analysis" (F pp. 34–35). ARE
  adds overfitting and general lack of robustness, citing Gelman and Imbens
  (2019), and confines global polynomials to visualization (ARE pp.
  833–834).
- Recommended instead: weighted least squares of Y on a low-order polynomial
  in (X − c), separately on each side, using only observations within a
  bandwidth h, with kernel weights; the estimate is the difference in
  intercepts (F pp. 35–36; ARE pp. 833–835). The polynomial is read as a
  local approximation, not a correctly specified model (F p. 35).

## 3. Defaults: kernel, order, bandwidth

- **Kernel.** Triangular is the recommended choice: with an MSE-optimal
  bandwidth it gives an MSE-optimal point estimator (F pp. 37, 45). The
  uniform kernel minimizes asymptotic variance (F p. 38) and so has an
  inference-optimality property (ARE p. 834). Results are typically not
  "very sensitive to the particular choice of kernel used" (F p. 38); the
  worked example moves from 2.927 to 2.937 (F p. 47).
- **Order.** p = 0 has undesirable properties at boundary points; higher p
  overfits; local linear is the default (F p. 38). ARE: p = 1 default, p = 2
  or 3 "also a reasonable choice in some empirical settings" with Pei et al.
  (2021) for a data-driven choice (ARE p. 834). Changing p changes the point
  estimate; the question is whether conclusions change (F pp. 50–51).
- **Bandwidth.** Data-driven, never ad hoc: an arbitrary h is "not
  advisable" (F p. 51) and is discouraged because it invites specification
  search (F p. 40; ARE p. 834). hMSE ∝ n^(−1/(2p+3)) (F p. 42). `mserd`
  imposes one h on both sides; `msetwo` allows two (F pp. 51–52);
  `rdbwselect(..., all = TRUE)` prints ten selectors — `mserd`, `msetwo`,
  `msesum`, `msecomb1` (min of mserd and msesum), `msecomb2` (median of
  msetwo, mserd, msesum) and their five CER analogues (F pp. 68–69). A
  separate bias bandwidth b, with ρ = h/b, is printed alongside h (F pp. 49,
  60).
- **Regularization.** On by default in every MSE selector; `scaleregul = 0`
  removes it. In the worked example removing it doubles h (17.239 to 34.983)
  with a stable point estimate (F pp. 44, 55, 57).
- **Printed defaults** of a bare `rdrobust(y, x)` call: `mserd`, triangular,
  NN variance estimator, p = 1, bias order 2 (F p. 82). Of a bare
  `rddensity(X)`: unrestricted model, triangular kernel, `comb` bandwidth,
  jackknife variance, p = 2, q = 3 (F p. 88).
- **Erratum.** The leading bias is B = h^(p+1)·𝓑; F prints h^(2(p+1)) in the
  bias expression on p. 40, in the sentence on p. 41 (the bandwidth term
  h^(2(p+1)) should read h) and in the plug-in on p. 43. The squared bias in
  the MSE, h^(2(p+1))𝓑², is unaffected. The erratum also warns that package
  updates mean current RD-package versions may not reproduce the printed
  numbers exactly; the replication repository explains how to restore
  backward compatibility.

## 4. Inference

- Conventional least-squares intervals at hMSE ignore the smoothing bias and
  are invalid; the authors "strongly discourage researchers" from
  conventional inference with local polynomial methods unless the bias is
  credibly small, which rules out MSE-optimal bandwidths (F pp. 57–60).
  Back-of-envelope coverage of a nominal 95% interval is about 80% (ARE p.
  835).
- Undersmoothing is valid in theory but ad hoc (no rule for how far to
  shrink), costs power, and uses different observations for estimation and
  inference (F pp. 59–60; ARE pp. 835–836). Standard bias correction leaves
  the variance unadjusted and covers poorly (F pp. 60–61).
- RBC: subtract the bias estimate and studentize with a variance that
  includes the bias-correction step; valid at hMSE, valid with h = b (F pp.
  61–62, Table 3). It is valid whenever the conventional interval is valid
  (ARE p. 836).
- Recommended reporting: MSE-optimal point estimate τ̂ at hMSE; RBC interval
  with hMSE (valid) or hCER (valid and coverage-error optimal); hCER < hMSE
  in all practically relevant samples (F p. 63). The bias-corrected point
  estimate is omitted from default output on purpose, because it is not
  MSE-optimal; `all = TRUE` prints it (F pp. 65–66). At a common h the RBC
  interval is longer than the conventional one (F p. 65).
- Clustering changes the variance estimator, hence the selected bandwidth,
  hence the point estimate; cluster-robust variances "can be smaller or
  larger" so the interval can shorten or lengthen (F p. 74). In F's example
  the clustered `mserd` bandwidth widens (17.239 to 19.035, p. 75); in E's
  discrete example it narrows (0.470 to 0.428, E p. 69).

## 5. Covariate adjustment

- Covariates must be predetermined and balanced at the cutoff; adjustment
  cannot restore identification when treated and control units differ at the
  cutoff (F pp. 69–71; STS p. 563). The only valid general justification is
  efficiency: "valid justification for including covariates in RD analysis
  is the potential for efficiency gains" (F p. 71).
- Add covariates linearly and additively, not interacted with treatment;
  with interactions, zero covariate discontinuity no longer guarantees the
  adjusted estimator targets τ_SRD (F pp. 70–71).
- Reselect the bandwidth with covariates included (`covs` in both
  `rdbwselect` and `rdrobust`) (F pp. 71–73). If the covariates are truly
  predetermined, adjusted and unadjusted point estimates should be similar
  while the interval shortens (F pp. 73–74). A protocol should state how
  disagreements between adjusted and unadjusted estimates will be resolved
  (STS p. 562).

## 6. The falsification battery

F p. 79 names five tests: (i) null effect on predetermined covariates or
placebo outcomes; (ii) continuity of the score density; (iii) effects at
artificial cutoffs; (iv) exclusion of observations near the cutoff; (v)
sensitivity to bandwidth. ARE §4 (pp. 842–845) and STS p. 563 list the same
set.

### 6.1 Predetermined covariates and placebo outcomes — at whose bandwidth

- Predetermined covariates are fixed before assignment; placebo outcomes are
  post-assignment variables the mechanism cannot affect, and are
  application-specific (F p. 79; ARE p. 843; called negative control
  outcomes in STS p. 563).
- Principle: they "should be analyzed in the same way as the outcome of
  interest" (F p. 79). The authors mean the same *procedure*, applied with
  each variable's own bandwidth: for each covariate researchers "should
  first choose an optimal" bandwidth and then use local polynomial RBC
  inference within it (F p. 80). Because each covariate has its own
  curvature, "the statistical analysis must be conducted separately for each
  covariate, choosing a different optimal bandwidth for each covariate
  analyzed" (F p. 80).
- F's Table 4 (p. 83) runs each covariate at its own MSE-optimal bandwidth
  (10.360 to 13.940; the outcome's is 17.239). F then adds that "for
  falsification purposes it may be more appropriate to use the CER-optimal
  bandwidth" because only the null matters; MSE-optimal gives more power
  with possibly larger size distortion (F p. 84). E does exactly that:
  `rdrobust(covariate, X, bwselect = "cerrd")`, with each covariate at its
  own CER-optimal bandwidth (E p. 57; Table 4, p. 58: 4.91 to 6.68; Table 7,
  p. 67), stating "we implement the local polynomial analysis with a
  bandwidth that optimizes the coverage-error (CER) of the confidence
  intervals" (E p. 60).
- None of the four sources runs a covariate test at the outcome regression's
  bandwidth. (Inference: a reviewer who wants balance evidence in the exact
  neighbourhood the headline uses may add that run, labelled as the
  reviewer's supplement, not as the authors' test.)
- Run it for "all important covariates," meaning all those expected to
  correlate with treatment under manipulation; a convincing design shows no
  discontinuity in any (F p. 82). Plot each covariate within its own
  bandwidth with p = 1 and triangular weights (F p. 84).
- Reading: null covariates with a clear outcome effect support validity; the
  converse does not undermine it, since a valid design can have a null
  outcome effect (F pp. 84–85). Non-rejection of balance is the usual
  reading, but ARE notes that testing the null that the groups *differ*
  would control the right error (Hartman 2021) (ARE p. 843). One rejection
  among several is judged by magnitude: E reports a p = 0.001 imbalance in
  first-year credits (0.08 credits against a mean of 4.43) and calls it a
  matter for further investigation only if it could plausibly affect the
  outcome (E p. 66). A protocol should say in advance how many and which
  imbalanced covariates will be tolerated and what follows if that is
  exceeded (STS p. 562).

### 6.2 Density of the running variable

- Two tools. A binomial test with success probability 1/2 in a small window,
  exact under its assumptions, repeated over nested windows because the
  continuity framework gives no rule for the window (F pp. 86–87). And the
  local-polynomial density test (`rddensity`), which needs no pre-binning
  and has better size and power than earlier approaches (F p. 87).
- The authors' reading of a non-rejection: "failing to reject implies that
  there is no statistical evidence of manipulation at the cutoff" and
  supports validity (F p. 87). ARE qualifies the logic: density continuity
  is "neither necessary nor sufficient for the validity of an RD design,"
  though a discontinuity is heuristically linked to sorting (ARE p. 843).
  The binomial test works with continuous or discrete scores (ARE p. 844).
- With a discrete score and many mass points (429), E runs `rddensity(X,
  bino = FALSE)` as the continuity-based density test, read alongside the
  binomial test (E pp. 64–66).

### 6.3 Placebo cutoffs

- Estimate the RD effect at artificial cutoffs, with RBC inference inside a
  bandwidth optimally chosen around each artificial cutoff (F p. 89).
- Restrict to one side: "for artificial cutoffs below the real cutoff we use
  only control observations" and above it only treated ones, so that each
  test uses units of one treatment status and the true effect cannot
  contaminate it (F pp. 89–90). ARE: "this validation method should be
  implemented for units below and above the cutoff separately" (ARE p. 844).
- The example uses a grid of cutoffs on both sides; bandwidths are
  reselected at each (2.362 to 4.642) and effective samples shrink, to 30
  observations left of the artificial cutoff at c = 1 (F pp. 90–91, Table
  5). Continuity away from the cutoff is neither necessary nor sufficient
  for continuity at it; a jump that substantive knowledge (another policy at
  that score) cannot explain casts doubt on the design (F p. 89; ARE p.
  844).

### 6.4 Donut hole

- Purpose, per the authors: if manipulation occurred, the units nearest the
  cutoff are the most likely manipulators; even without manipulation, the
  test measures sensitivity "of the results to the unavoidable extrapolation
  involved in local polynomial" fitting, since the nearest observations are
  the most influential (F p. 92; ARE pp. 844–845).
- Procedure: drop |X − c| < r, rerun `rdrobust`, which selects a new
  bandwidth; repeat for several radii (F pp. 93–94). Report, per radius, the
  new bandwidth, point estimate, RBC interval and p-value, effective N, and
  excluded observations on each side (F p. 95, Table 6: radii 0.1 to 0.5
  remove 2 to 27 of 2,629 observations). The effective sample can fall by
  more than the excluded count because the bandwidth moves (F pp. 93–94).

### 6.5 Bandwidth sensitivity

- Bias grows and variance falls with h, so intervals shorten and shift as h
  grows (F p. 96). Hence sensitivity "is only useful over small ranges
  around the MSE-optimal bandwidth" for point estimates, and near hCER when
  the emphasis is inference; far from those values results are "mechanically
  determined" by bias or variance (F p. 96). ARE: "considering much larger
  bandwidths is not advisable due to the implied misspecification bias" (ARE
  p. 845).
- The illustration uses four values: hCER, hMSE, 2·hCER, 2·hMSE, each with
  its RBC interval (F pp. 96–97). At hCER the point estimate matches but the
  longer interval no longer excludes zero; the authors still read the set as
  consistent (F p. 97).

## 7. Fuzzy RD (E §3, pp. 36–60)

- **Estimands.** ITT effects of assignment T on Y (τ_Y) and on take-up D
  (τ_D, the first stage) are sharp-RD objects: continuity of E[Y(1, D(1)) |
  X], E[Y(0, D(0)) | X], E[D(1) | X], E[D(0) | X] at c (E pp. 41–43). The
  fuzzy parameter τ_FRD = τ_Y / τ_D is the average effect of receipt for
  compliers at the cutoff under an exclusion restriction plus monotonicity
  (no defiers) (E pp. 44–46; ARE pp. 827–828). It equals the sharp effect
  for all units only under local independence of potential outcomes and
  compliance, which the authors call rarely invoked and implausible in most
  applications (E p. 46). The exclusion restriction fails when merely being
  assigned changes behaviour (ARE p. 828).
- **Estimation and inference.** Ratio of two local-polynomial intercept
  differences; RBC inference, the interval centred on τ̂_FRD minus its
  estimated bias (E pp. 46–47; ARE p. 836). For the ratio, use one bandwidth
  for numerator and denominator; `rdrobust(y, x, fuzzy = d)` picks a single
  MSE-optimal bandwidth for the linearized ratio and reports an RBC interval
  for it (E pp. 48–49, 54). Separate bandwidths are not wrong in theory but
  use different observations (E p. 54). With one-sided noncompliance
  `rdrobust` warns, sets the control-side bandwidth to the score range, and
  the printed common h is the treated-side value (E pp. 52–53). In local
  randomization, Fisherian inference permutes T, not D; the `tsls` statistic
  in `rdrandinf` returns only a large-sample p-value (E pp. 47, 56–57).
- **Weak first stage.** First test τ_D = 0; that "should be the first step
  in the analysis of any Fuzzy RD design" (E p. 49). Nonzero is not enough:
  with a small first stage Gaussian approximations fail even in large
  samples (E p. 49). Measure strength by the first-stage F; the IV rule of
  thumb of 10 is, "in the RD context, this threshold is likely to be too
  low," and the cited recommendation is F ≥ 20 (E p. 50). The source does
  not say which F (conventional or robust) to compute. Weak-IV-robust
  methods exist but give long, often uninformative intervals; the authors
  recommend avoiding fuzzy designs with weak first stages, and "If the
  first-stage effect is weak, researchers should report only ITT effects" (E
  p. 50). Weak-identification references: Feir, Lemieux and Marmer (2016),
  He (2018) (ARE p. 837; E p. 60).
- **Falsification.** Density test and covariate or placebo tests are run on
  assignment T, not receipt D: covariate effects are ITT effects, and the
  density test compares units with T = 1 and T = 0 (E pp. 50–51, 57). E runs
  covariates at their own CER-optimal bandwidths (E pp. 57–60).

## 8. RD plots

- The standard RD plot overlays a global fourth- or fifth-order polynomial
  fit (fit to raw data) and binned local means; raw scatter plots rarely
  reveal a jump even when the effect is large (F pp. 17–18). Default
  `rdplot` uses a global order-4 fit over the full support with uniform
  weights (F pp. 22–23) and mimicking-variance evenly-spaced bins (F p. 80).
  Start with mimicking-variance bins, compare evenly-spaced with
  quantile-spaced bins, then IMSE-optimal bins for global shape (F p. 32).
- To illustrate the local estimate, restrict to |X − c| ≤ h and pass the
  same `p`, `h` and `kernel` as `rdrobust` (F pp. 54–55, 84).
- "RD plots should not be used as substitutes for the formal estimation and
  inference of RD effects"; a jump in the global fit is suggestive only, and
  plot specification alone changes what viewers conclude (Korting et al.
  2021) (ARE p. 833).

## 9. Discrete scores (as far as these sources go)

- The deciding quantity is the number of mass points. With many, continuity
  methods may still apply, but their effective sample is the number of mass
  points, not units, and extrapolation between mass points is unavoidable;
  with few, local randomization is the natural primary analysis (E pp.
  60–62, 69–70; ARE p. 842; STS p. 562). E shows clustering by score value
  as an option (E p. 69). ARE notes that uniform-in-bias methods, including
  Kolesár and Rothe (2018), require a manually set smoothness constant,
  which is equivalent to choosing the bandwidth by hand (ARE pp. 840, 842).

## 10. Errors and open issues the ARE review names

Errors to catch: reading an RD plot or a global-fit jump as the estimate (p.
833); global polynomials for estimation (pp. 833–834); arbitrary bandwidths
(p. 834); conventional least-squares inference at hMSE, roughly 80% coverage
(p. 835); undersmoothing by an arbitrary factor (pp. 835–836); treating the
number of units as the effective sample with a discrete score (p. 842);
ex-post power at the observed effect, where an MDE is preferred because
"ex-post power calculations using observed effect sizes are often
unreliable" (p. 842); two-sided placebo-cutoff samples (p. 844); much wider
bandwidths in sensitivity analysis (p. 845). Open issues: extrapolation away
from the cutoff, ex-ante experimental design and data collection, and
high-dimensional and machine-learning methods for heterogeneity and
multidimensional designs (p. 845); weak identification and specification
tests in fuzzy designs, and running-variable measurement error (p. 837).

## 11. What a protocol should fix in advance (STS)

The score, cutoff, treatment and assignment rule, which must have actually
occurred (p. 561); the study population, all units with a score (p. 561);
the treatment's causal path to the scientific question (p. 561); primary and
secondary outcomes (pp. 561–562). Statistical methods: continuity, local
randomization or both, and which is primary (continuity when the score is
continuous with enough observations; local randomization for few unique
score values or too few observations); for local polynomials, the bandwidth
selector, polynomial order, kernel, treatment of misspecification error and
quantification of uncertainty; for local randomization, window selection,
test statistics, Fisherian or large-sample inference, the assignment
mechanism and any regression adjustment (p. 562). Covariates: the
falsification list, the tolerance for imbalance and the response if it is
exceeded; whether, how and with which covariates to adjust, and how
adjusted–unadjusted disagreements are resolved; heterogeneity subgroups (pp.
562–563). Falsification: covariate and placebo-outcome lists and their
inference; density, bandwidth or window variation, and donut analyses with
implementation details; Rosenbaum sensitivity in the local-randomization
framework (p. 563). Multiplicity: a few primary outcomes, or a
Bonferroni-type correction stated in advance; sample splitting is usually
infeasible because effective samples are often 10–20% of observations in
continuity analyses (p. 563). Timing: before the outcome is analyzed. A
continuity protocol names the bandwidth method, not the value, unless a
large sample allows a planning split with h₂ = h₁·(n₁/n₂)^(1/(3+2p)); score
histograms and density plots may be inspected first, the outcome–score
relation may not (p. 564).

## Review use

- **Specification.** Trigger: any RD headline. A global polynomial estimate,
  an unexplained fixed bandwidth, or a conventional interval at an
  MSE-optimal bandwidth is a finding (§§2–4). Re-estimate with `rdrobust`
  defaults (§3) and report τ̂ at hMSE with the RBC interval at hMSE and
  hCER. A paper that reports RBC at hCER follows the recommended practice.
  Report p = 2 beside p = 1; a shifted point estimate is expected, and only
  a changed conclusion counts against the claim.
- **Covariates and placebo outcomes.** Run every predetermined covariate and
  placebo outcome as an outcome, each at its own data-driven bandwidth
  (CER-optimal preferred for testing, MSE-optimal acceptable), with RBC
  inference (§6.1). A run at the outcome's bandwidth is a supplement and
  must be labelled as the reviewer's. Failure: a discontinuity, with
  material magnitude, in a covariate tied to the outcome or to the plausible
  manipulation channel. Cost: the continuity assumption is in doubt and
  covariate adjustment cannot repair it (§5); reprice the claim. A lone
  small rejection among many covariates is reported with its magnitude, not
  treated as decisive.
- **Density.** Run `rddensity` and binomial tests over nested windows. In a
  fuzzy design, test the score by assignment, not by take-up. Non-rejection
  is weak support (the test is neither necessary nor sufficient). The
  manipulation-robust bounds in `rdd_methods_guide.md` §2 run whatever the
  test says; a rejection first triggers the checks for mechanical causes.
- **Placebo cutoffs.** Use a grid on each side of the true cutoff, using
  only same-side observations, with a bandwidth reselected at each cutoff
  and RBC inference. A test that pools observations across the true cutoff
  is invalid and is redone. Report effective N, because power collapses near
  the true cutoff.
- **Donut.** Run in every RD, not only under suspected heaping. Use several
  small radii, a reselected bandwidth, and report effective N and excluded
  counts per side. Failure: the estimate moves materially or the conclusion
  flips once a handful of nearest units are dropped. That points to
  manipulators near the cutoff or to extrapolation-driven fragility.
- **Bandwidth sensitivity.** Run at hCER, hMSE, 2·hCER and 2·hMSE, not a
  wide grid. Judge stability of the point estimate and overlap of the
  intervals. A loss of significance at hCER that comes from a longer
  interval is not fragility. Drift at bandwidths far above hMSE is bias and
  is not evidence against the paper.
- **Fuzzy.** Report the first stage first with its F. Below 20, the ratio
  estimate is not interpretable as a treatment effect and the paper should
  be held to ITT. Check that the ratio comes from a single bandwidth with
  RBC inference. A τ_FRD described as the effect for everyone, rather than
  for compliers at the cutoff, overstates the estimand unless local
  independence is defended.
- **Covariate adjustment.** Confirm the covariates are predetermined, enter
  additively without treatment interactions, and that the bandwidth was
  reselected with them. A large gap between adjusted and unadjusted
  estimates signals imbalance, not a gain in precision.
- **Replication mismatches.** Before alleging an error in a paper's
  `rdrobust` numbers, record the package version: updates move printed
  results (§3 erratum).
- **Pre-specification.** Where a paper claims a protocol, check the §11
  items against what was run. Where it does not, every unexplained choice
  from §11 (selector, order, kernel, covariate set, donut radii, cutoff
  grid) is a researcher degree of freedom to vary.
