# Regression kink designs — Card, Lee, Pei & Weber (2015); Ganong & Jäger (2018)

Working distillation of David Card, David S. Lee, Zhuan Pei and Andrea Weber,
"Inference on Causal Effects in a Generalized Regression Kink Design,"
*Econometrica* 83(6) (2015): 2453–2483 (CLPW), and Peter Ganong and Simon
Jäger, "A Permutation Test for the Regression Kink Design," *Journal of the
American Statistical Association* 113(522) (2018): 494–504 (GJ). Both audited
in their published versions. Kink-specific passages of Calonico, Cattaneo &
Titiunik, "Robust Nonparametric Confidence Intervals for
Regression-Discontinuity Designs," *Econometrica* 82(6) (2014): 2295–2326
(CCT), and Calonico, Cattaneo, Farrell & Titiunik, "rdrobust: Software for
regression-discontinuity designs", *Stata Journal* 17(2) (2017): 372–404
(CCFT), are cited where they bear on kinks. Source PDFs (not distributed with
the skill): `Card_Lee_Pei_Weber_2015_RegressionKink_Econometrica.pdf`,
`Ganong_Jaeger_2018_PermutationTestRKD_JASA.pdf`,
`Calonico_Cattaneo_Titiunik_2014_RobustRDD_Econometrica.pdf`,
`Calonico_Cattaneo_Farrell_Titiunik_2017_rdrobust_StataJ.pdf`. CLPW's
supplement and the Upjohn working paper (Card et al. 2015a) where CLPW report
their own run of the GJ test were not audited.

Verification status: source-audited 2026-10-15.

Use in this battery: `rdd-diagnostics` — a regression-kink conditional check
(policy-rule audit, density and covariate smoothness, local-polynomial order
and bandwidth grid, placebo-kink permutation test, fuzzy first stage, power of
a null); the density, covariate-continuity, placebo-cutoff and fuzzy
first-stage core checks when the design is a kink; the unstated-bandwidth
sweep; the design-matrix RD records.

## 1. Estimand

A regression kink design (RKD) uses a policy variable B that is a known,
continuous function b(V) of an assignment variable V, with a change in slope
at a threshold (benefit maxima and minima, bracket changes in tax or aid
formulas; CLPW pp. 2453–2454). The sharp RKD estimand is the change in slope
of E[Y|V=v] at the kink divided by the known change in slope of b(v) there
(CLPW p. 2457, NST formula; Proposition 1, p. 2460; GJ eq. 5, p. 497).

Under CLPW's assumptions it identifies the treatment-on-the-treated / local
average response parameter: a weighted average of marginal effects
∂y/∂b across the whole population, each type weighted by its relative
likelihood of having V at the kink, f(0|U=u)/f(0) (Proposition 1(b),
p. 2460; Remark 1, p. 2462). Where U is strongly correlated with V the
estimate represents only the types that sit near the kink (Remark 1). At a
benefit maximum, where B is flat above the kink, the estimand is the limit of
TT as b approaches the capped level from below (fn. 10, p. 2462).

## 2. Identifying assumptions (sharp RKD, CLPW §2.2.1, pp. 2459–2460)

- **Known, continuous, kinked rule** (Assumption 3(i)): b(·) known,
  continuous everywhere, continuously differentiable away from 0, with
  unequal one-sided derivatives at 0. Continuity matters: if the rule's level
  also jumps at the threshold, the RK estimand does not point-identify an
  interpretable effect in the nonseparable model, while the RD estimand
  still does; absent strong prior knowledge of homogeneous effects "it seems
  advisable to use an RD design" (Remark 3, pp. 2463–2464).
- **Smooth effect of V** (Assumption 2): V may affect Y directly, provided
  its marginal effect ∂y/∂v is continuous — weaker than an exclusion
  restriction (p. 2460).
- **Smooth density** (Assumption 4): the density of V conditional on U, and
  its first derivative in v, are continuous at the kink. Continuity of the
  density suffices for RD; RKD needs the derivative to be continuous too
  (p. 2460). The condition rules out precise manipulation of V but allows
  some influence over it, e.g. sorting with optimization errors
  (pp. 2454, 2459). Extreme bunching at a kink of the Saez type violates it;
  models with optimization frictions may not (p. 2480).
- **Positive density at the kink** for a non-trivial set of types
  (Assumption 3(ii), p. 2459).

## 3. Fuzzy RKD (CLPW §2.2.2, pp. 2464–2467)

The fuzzy design allows B = b(V, ε) — unobserved inputs to the formula (in
the Austrian application, the number of dependants), non-compliance, and
measurement error in V and B (pp. 2464–2465). The estimand replaces the
known slope change with the estimated first-stage slope change in E[B|V]
(Proposition 2, p. 2466; eq. 3.5, p. 2471). Added conditions:

- b(·, e) continuous at the threshold for every type (Assumption 3a); a
  level jump again breaks the RK estimand (p. 2465).
- **A mass point at zero in the measurement error of V**: without it no
  first-stage kink is observed and further assumptions are needed (p. 2466).
  CLPW read the majority of observations lying exactly on the benefit
  schedule as evidence of this mass point (p. 2466).
- **Monotonicity** (Assumption 6): the kink has the same sign for every type
  (p. 2465). It holds in CLPW's application because the benefit schedules for
  different numbers of dependants are parallel (p. 2466).
- Smooth joint density of V and the measurement errors, and smooth
  probability of no measurement error (Assumptions 4a, 5, p. 2465).

Weights (Remark 5, p. 2467): types with larger individual kinks get more
weight; types whose schedule has no kink at the threshold get none;
non-compliers can get positive weight if the schedule they follow is kinked;
observations with mismeasured V contribute nothing. The existence of a
first-stage kink is itself a test of Assumptions 3a and 6 (Remark 4,
p. 2467). Y and (B, V) may come from different datasets; the two-sample case
is in the supplement (fn. 14, p. 2471; not audited).

## 4. Testable implications (CLPW §2.3, pp. 2469–2470)

- **Corollary 1**: the density of V (of the observed V* in the fuzzy case)
  is continuously differentiable at the kink. A kink *or* a discontinuity in
  the density is evidence against the design — the analogue of the McCrary
  test, but on the slope of the density as well as its level (p. 2469).
- **Corollary 2**: for predetermined covariates X, the derivative in v of
  Pr[X ≤ x | V = v] is continuous at the kink. The design implies that the
  derivatives of covariate conditional expectations or quantiles are
  continuous — stronger than the continuity an RD implies (p. 2470). CCFT
  state the same for covariate-adjusted kink estimation: "balanced" means
  equal first derivatives at the cutoff, testable by running `rdrobust` with
  the covariate as the outcome (pp. 376, 396).
- CLPW's own density test (p. 2475, fn. 21): minimum-chi-squared polynomial
  fits to a 300-euro-bin histogram, continuity imposed, first and higher
  derivatives free to change at the threshold; AIC picks a quartic; change in
  the density's first derivative 2.00 × 10⁻⁴ (SE 1.24 × 10⁻⁴), t = 1.61.

`rddensity` tests equality of the two one-sided density *levels*; its
`fitselect(restricted)` option imposes equal c.d.f. and higher-order density
derivatives on both sides to gain power (Cattaneo, Jansson & Ma 2018, *Stata
Journal* 18(1), pp. 239, 245; the default is unrestricted). Inference: for an
RKD the restricted test assumes away the density kink that Corollary 1 asks
about, and the unrestricted test checks only the level.

## 5. Estimation (CLPW §3, pp. 2470–2473; CCT §3, pp. 2305–2309)

- Separate local polynomials of order p on each side; the sharp estimator is
  the difference of the two first-derivative coefficients divided by the
  known slope change, the fuzzy estimator the ratio of outcome to first-stage
  slope changes (pp. 2470–2471). Kink estimators converge at rate √(nh³)
  (p. 2471) rather than RD's √(nh). Imposing continuity of the level at the
  kink changes neither asymptotic variance (uniform kernel) nor bias
  (p. 2471; GJ eq. 7 uses the constrained form).
- **Polynomial order.** CCT treat the sharp kink with a local-quadratic point
  estimator — "more appropriate to employ a local-quadratic estimator" for
  boundary-bias reasons — and a local-cubic bias estimate (p. 2305; fuzzy
  kink, p. 2308). CLPW agree that rate arguments favour p = 2 but deny a
  universal rule: asymptotic rates do not justify
  "p = 1 as the universally preferred choice for RDD or p = 2 as the universally preferred choice for RKD"
  (pp. 2471–2472). The choice depends on sample size and the CEF's
  derivatives; they propose simulation from DGPs fitted to the data, or
  comparing estimated AMSE (p. 2472).
- **Kernel.** CLPW use a uniform kernel; the triangular kernel gives similar
  results (p. 2472). GJ report that the RK literature has mostly used the
  uniform kernel with local linear or quadratic fits (p. 497).
- **Bandwidth.** CCT's MSE-optimal selector covers the νth-derivative
  discontinuity, with ν = 1 for RKD (CLPW p. 2472; CCT Lemma 1, p. 2310).
  Two issues CLPW raise (p. 2472): (i) the regularization term in the IK and
  CCT selectors gives RK bandwidths that are too small in their data, so they
  also run selectors without it; (ii) the default CCT bandwidth is
  MSE-optimal for the reduced-form kink, not the fuzzy ratio, so they derive
  fuzzy-IK and fuzzy-CCT selectors (supplement §B.2, not audited). For fuzzy
  RD, CCFT report that `rdbwselect` now targets the ratio by default when
  compliance is imperfect on both sides, and the reduced-form numerator
  otherwise (p. 389, the selection paragraph).
- **Bias and inference.** At the MSE-optimal bandwidth the bias is
  first-order, so conventional intervals can under-cover; CLPW report
  conventional estimates with CCT robust bias-corrected intervals (RBC)
  (pp. 2472–2473). CCT's sharp-kink RBC result requires the CEF to be four
  times continuously differentiable (Theorem 2, p. 2306).

**CLPW's application** (Austrian UI, fuzzy RKD at the benefit maximum,
≈275,000 claims; Table I, p. 2477; pp. 2478–2479): local linear and local
quadratic × five selectors (default CCT; CCT without regularization;
fuzzy CCT; fuzzy IK; Fan–Gijbels rule of thumb). Despite a visually clear
first-stage kink, the default-CCT local-linear first stage is only marginally
significant (t = 2.5) and its RBC interval includes zero. Local-linear
elasticities from the three larger-bandwidth selectors are 1.4–1.9, and only
one of their three RBC intervals excludes zero (fuzzy CCT, [0.1, 5.1]).
Local-quadratic elasticities are negative in three of five cases, which
"renders the local quadratic procedures uninformative" (p. 2479). Point
estimates are volatile at small bandwidths and stabilize between 4,000 and
9,000 euros (Figure 4, p. 2479).

**Software** (CCFT pp. 382, 401): `rdrobust y x, deriv(1)` is the sharp kink;
`fuzzy(t) deriv(1)` the fuzzy kink. The R help says `deriv = 1` estimates
the kink only up to scale and that `scalepar` supplies a known multiplicative
factor such as the sharp-kink denominator. In the package code (R releases
2.2 through 4.1.1, and Stata), when `p` is not given and `deriv` is set,
`p = deriv + 1` (local quadratic for a kink) and `q = p + 1`; otherwise the
default is p = 1. `scaleregul = 0` removes the regularization term. Release
4.1.1 corrected a sharp fit with covariates and `deriv >= 2`, whose estimate
had been halved. These package details come from the help files and code,
not the audited articles; confirm them in the installed version.

## 6. The failure GJ document: spurious kinks from curvature

- **Mechanism** (GJ pp. 495, 497–498). Curvature in E[Y|V] biases a local
  polynomial slope-change estimator. For local linear RK the leading bias is
  proportional to (m₊⁽²⁾ + m₋⁽²⁾)h — the *sum* of the one-sided second
  derivatives — so a CEF that is smoothly curved through the kink, with no
  slope change at all, produces a non-zero kink estimate. For local quadratic
  the leading bias involves third derivatives (p. 498; general formula, CCT
  p. 2310). GJ's Figure 1 (p. 495): 1,000 draws from a quadratic DGP with no
  kink look like the piecewise-linear kinked DGP, and a local linear RK
  estimator finds a highly significant slope change in both.
- **Prevalence.** Of 44 RK studies GJ tabulate, most use linear or quadratic
  specifications (Table A.1, p. 495; appendix not audited).
- **Size in calibrated simulations** (Table 1, p. 501). Natural cubic
  splines (100 knots) fitted to the CLPW (bottom-kink) and Kolsrud et al.
  (Sweden) binned data, no kink imposed; 10,000 observations per dataset;
  each of 100 equally spaced placebo kinks treated as the policy kink;
  200 FG / 50 CCT draws. Share of placebo kinks rejected at 5%: local linear,
  Fan–Gijbels bandwidth, conventional inference **0.38 (CLPW) and 0.37
  (KLNS)**; CCT (local linear, quadratic bias correction) 0.05 and 0.05;
  permutation test 0.05. The CLPW failure arises because the procedure
  cannot tell a global U-shape from a kink (p. 501).
- **Artificial DGPs** (Table 2, p. 502; 10,000 obs, 100 placebo kinks on
  [−1, 1]). Linear DGP: FG 0.05, CCT 0.05. Nonlinear DGP 2: FG 0.56, CCT
  0.24. Sine DGP 3: FG 0.94, CCT 0.15. Permutation 0.05 throughout. CCT
  improves on FG but still over-rejects under strong curvature.
- **Power** (Tables 1 and 3, pp. 501, 503). With a true kink in the
  CLPW-calibrated DGP, failure-to-reject rates are FG 0.12, CCT 0.92,
  permutation 0.73; in the KLNS calibration all three always reject. In the
  CLPW data placebo slope changes tend to share the sign of the true kink; in
  KLNS they do not (p. 501). Power falls when the CEF is highly nonlinear
  relative to the kink size: DGP 3 with kink 5, CCT fails to reject 0.82 and
  permutation 0.87 (Table 3).
- Higher-order (quadratic, cubic) estimators with conventional inference
  lower Type I and raise Type II error (p. 501; Tables A.2–A.6 not audited).

## 7. GJ's permutation test (GJ §3, pp. 498–500)

- **Statistic**: the reduced-form slope change at a candidate kink k, built
  with the researcher's own bandwidth rule, polynomial order and CCT bias
  correction (p. 498).
- **Assumption — random kink placement**: the true kink location is a draw
  from a known distribution P. Violated if policy-makers placed the kink in
  response to the shape of E[Y|V], e.g. where curvature is high or low
  (pp. 498–499).
- **Choosing P** (p. 499): (1) estimate the stochastic process that moves
  the kink (Austria's earnings ceiling follows lagged aggregate wage growth);
  (2) a grid spanning documented policy proposals; (3) a Cattaneo–Frandsen–
  Titiunik local-randomization window; (4) the whole range of the data,
  using the empirical distribution of V.
- **Null**: policy irrelevance at every v — stronger than the local null of
  RD randomization inference (p. 499). Under it and random placement the
  test has exact finite-sample size (Proposition 1, p. 499; proof in
  Appendix B, not audited).
- **p-value**: two-sided = twice the smaller one-sided fraction of placebo
  estimates, including the one at the actual kink, lying at or beyond it.
  Example: 20th lowest of 1,000 gives p = 0.04 (p. 499).
- **Interval**: invert the test over constant effects by subtracting
  candidate effects from the data (p. 500; algorithm in Appendix C, not
  audited).
- **Recommendations** (pp. 503–504): (1) avoid linear and quadratic RK
  estimators with FG bandwidths; (2) use CCT's robust procedure as the
  preferred estimator; (3) use the placebo distribution to judge whether an
  economically meaningful effect is detectable; (4) report permutation
  p-values; (5) report robustness to the assumed placebo-kink distribution.
  GJ present the test as a complement to RBC inference, not a replacement
  (pp. 495, 503).
- Inference (not in GJ): placebo kinks whose estimation window contains the
  true kink, or another policy kink, mix in any real effect; restricting the
  grid to placebos whose windows exclude them is the natural refinement.

## Review use

Trigger: the identifying variation is a change in the *slope* of a policy
rule in an assignment variable — a benefit cap or floor, a bracket or
phase-out in a tax, aid or subsidy formula, a reimbursement schedule — or
the paper runs `rdrobust ..., deriv(1)` or divides a slope change by a slope
change. `NOT_APPLICABLE` otherwise.

1. **Rule audit.** Reconstruct b(v) from the statute. A level jump at the
   kink voids the RK estimand under heterogeneous effects (CLPW Remark 3);
   the paper needs an RD or a constant-effect argument. Record the slope
   change used as denominator. If observed B departs from the schedule, a
   sharp estimator is misspecified; fuzzy designs need a mass of
   observations exactly on the schedule and a same-sign kink for every type.
2. **Density smoothness.** Test the density of V for a jump *and* a slope
   change at the kink. A level-only `rddensity` run is incomplete; a
   restricted-fit run assumes the answer. Visible bunching at the kink
   (common where V is chosen, e.g. taxable income at a bracket) fails the
   design's key assumption.
3. **Covariate smoothness.** Run each predetermined covariate as an outcome
   with `deriv(1)` at its own data-driven bandwidth (the Cattaneo group's
   procedure for covariate tests, `rd_practice_guide.md` §6.1), and report it
   at the outcome's bandwidth and order as a labelled supplement. Jump tests
   are the RD implication, not the RK one.
4. **Order × bandwidth grid.** Re-estimate with p = 1 and p = 2 and at least
   the default CCT, unregularized CCT and (fuzzy) ratio-targeted selectors,
   reporting conventional estimates with RBC intervals, plus estimate-by-
   bandwidth plots. A result significant only with local linear, a rule-of-
   thumb bandwidth and conventional SEs is unestablished; sign changes across
   local-quadratic cells make the design uninformative (CLPW p. 2479).
5. **Placebo-kink permutation.** Run the paper's exact estimator at ≥100
   placebo kinks over a stated support with no policy kink. Report the share
   significant under the paper's own inference and the GJ permutation
   p-value. A share well above 5% means curvature can manufacture the
   headline significance; permutation p > 0.05 means the headline is not
   distinguishable from the placebo distribution. State the support and
   whether the kink's location could depend on the CEF's shape.
6. **Fuzzy first stage.** Report the first-stage kink with RBC inference
   across the grid. A first stage that loses significance under bias
   correction makes the ratio unstable (CLPW Table I).
7. **Nulls.** A null RK estimate in a curved CEF is uninformative until power
   is shown from the placebo distribution: in the CLPW calibration CCT misses
   a true kink 92% of the time (GJ Table 1).
8. **Scope.** The estimate is a weighted average of marginal effects for
   types near the kink (and, fuzzy, with large individual kinks). A claim
   about the population elasticity outruns it.
9. **Scale.** Sharp-kink software output is the outcome slope change; check
   that it was divided by the policy slope change and that `p` was set
   explicitly when reproducing.
