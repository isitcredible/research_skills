# Local-randomization RD and discrete running variables — Cattaneo, Frandsen, Titiunik, Vazquez-Bare, Idrobo (2015–2024); Kolesár & Rothe (2018)

Distillation of six published texts: Cattaneo, Frandsen & Titiunik,
"Randomization Inference in the Regression Discontinuity Design: An
Application to Party Advantages in the U.S. Senate," *Journal of Causal
Inference* 3(1) (2015): 1–24 (CFT); Cattaneo, Titiunik & Vazquez-Bare,
"Inference in Regression Discontinuity Designs under Local Randomization,"
*Stata Journal* 16(2) (2016): 331–367 (SJ, the `rdlocrand` article);
Cattaneo & Vazquez-Bare, "The Choice of Neighborhood in Regression
Discontinuity Designs," *Observational Studies* 2 (2016): 134–146 (CVB);
Cattaneo, Titiunik & Vazquez-Bare, "Comparing Inference Approaches for RD
Designs: A Reexamination of the Effect of Head Start on Child Mortality,"
*Journal of Policy Analysis and Management* 36(3) (2017): 643–681 (JPAM;
its Supporting Information appendix is unpaginated and cited by PDF page);
Cattaneo, Idrobo & Titiunik, *A Practical Introduction to Regression
Discontinuity Designs: Extensions*, Cambridge Elements (Cambridge University
Press, 2024), DOI 10.1017/9781009441896, Sections 2 and 4 (CIT); and Kolesár
& Rothe, "Inference in Regression Discontinuity Designs with a Discrete
Running Variable," *American Economic Review* 108(8) (2018): 2277–2304 (KR).
All six were audited in their published versions. Source PDFs (not
distributed with the skill): `Cattaneo_Frandsen_Titiunik_2015_RandomizationInferenceRD_JCI.pdf`,
`Cattaneo_Titiunik_VazquezBare_2016_rdlocrand_StataJ.pdf`,
`Cattaneo_VazquezBare_2016_ChoiceOfNeighborhood_ObsStud.pdf`,
`Cattaneo_Titiunik_VazquezBare_2017_ComparingInferenceRD_JPAM.pdf`,
`Cattaneo_Idrobo_Titiunik_2024_PracticalRD_Extensions_CUP.pdf`,
`Kolesar_Rothe_2018_DiscreteRDD_AER_published.pdf`.

Software caveat: SJ documents the 2016 Stata syntax of `rdwinselect`,
`rdrandinf`, `rdsensitivity` and `rdrbounds` and says the R functions share
it. CIT (2024) shows later R calls whose arguments differ (for example
`wobs`, not documented in SJ). Neither source documents the R return-value
names. Check argument names and defaults in the installed help.

Verification status: source-audited 2026-10-15.

Use in this battery: `rdd-diagnostics` conditional check on local-randomization
inference, its density and covariate-balance core checks where the score is
discrete, the Kolesár–Rothe remedies in the discrete-score check, the design-matrix
local-randomization RD record, and the `rdlocrand` snippet in the software
examples. Sibling cribs: `kolesar_rothe_2018_discrete_rdd.md`,
`rdd_methods_guide.md`, `cattaneo_jansson_ma_2020_density_test.md`.

## 1. The assumption and how it differs from continuity

- Continuity identifies τ = E[Y(1) − Y(0) | X = c] by extrapolating two
  regression functions to the cutoff (CIT p. 2; JPAM pp. 651–652).
- Local randomization assumes a window W = [c − w, c + w] in which (LR1) the
  scores are unconfounded and the assignment mechanism is known, and (LR2)
  the potential outcomes do not depend on the score (CIT p. 10; CFT
  Assumption 1, p. 4; SJ p. 334). Under both, the regression functions are
  flat inside W (CIT pp. 10–11).
- Random assignment of the score does not deliver LR2. The score can affect
  outcomes directly, so the exclusion restriction is a separate assumption
  (CIT pp. 9–10; JPAM appendix, PDF pp. 40–42).
- With a continuous score, local randomization is strictly stronger than
  continuity. A design can satisfy continuity with no window that satisfies
  local randomization (CIT pp. 34–35; CFT p. 4; JPAM p. 677).
- Neither assumption follows from the assignment rule. Both must be argued
  (CIT p. 34). Lee's (2008) imprecise-manipulation argument yields
  continuity, not local randomization (JPAM appendix, PDF pp. 40, 42).
- A continuity bandwidth is not a region of as-if random assignment. JPAM
  names the contrary reading a common misconception: the bandwidth is only
  the neighborhood where a low-order polynomial approximates the regression
  function (pp. 674–675). Continuity bandwidths are usually too wide for the
  local randomization assumptions to hold (p. 675).

## 2. Inference in the window: Fisher, Neyman, super-population

- Fisherian: potential outcomes fixed, sharp null of no effect for any unit
  in W, exact p-value from the assignment distribution, valid in any sample
  size (CIT pp. 14–16; SJ pp. 336–337). The mechanism must be assumed: fixed
  margins (complete randomization) or Bernoulli with a stated probability
  (CIT p. 17; CFT p. 5). JPAM uses fixed margins by default and Bernoulli
  only as a robustness check (p. 662). The two usually agree (CIT p. 23; SJ
  p. 364).
- Fisherian confidence intervals invert sharp nulls and need a treatment
  effect model, usually constant additive effects (CIT pp. 16–17; CFT p. 6).
  CFT also gives quantile-effect intervals that need no such model (p. 6).
  Point estimates require a sharp effect model. The ATE null is not sharp,
  so Fisherian methods give no general ATE estimate (CIT p. 17; JPAM p. 666).
- In Fisherian inference the difference in means is a test statistic, not
  an estimated effect (CIT p. 23). Rejecting the sharp null implies a nonzero
  ATE only if effects are assumed non-negative for every unit (JPAM p. 666).
- Neyman and super-population inference target the ATE in W with
  large-sample normal approximations and need many observations in W (CIT
  pp. 17–21). CIT suggests HC2 or HC3 variances as conservative choices
  (p. 21). Table 1 (CIT p. 19) compares the three frameworks.
- Unbiasedness of the plain difference in means: SJ p. 338 and JPAM p. 666
  say it holds under fixed margins and Bernoulli. CIT pp. 20–21 says it holds
  only under fixed margins; under Bernoulli it is consistent, and a weighted
  version is unbiased. The sources disagree; CIT is the later text.
- `rdrandinf` prints both: a finite-sample (Fisherian) p-value and a
  large-sample p-value for the ATE null, plus asymptotic power against d
  (default half the control-group SD in the window) (SJ pp. 344, 355; CIT
  pp. 22–23).
- The estimand differs. θ is the average effect over units in W. τ is an
  average at a point that holds no observations when the score is continuous.
  The two converge as W shrinks (CIT p. 20). Fisherian results apply only to
  the units observed in W (JPAM pp. 660, 666).

## 3. Window selection by covariate balance

Rule (CFT pp. 7–10; SJ pp. 335–336, 346; CIT pp. 24–27):

1. Use predetermined covariates (or placebo outcomes) that are associated
   with the score outside W0 but not inside it (CFT Assumptions 4–5,
   pp. 7–8). Covariates should relate to both outcome and treatment (CIT
   p. 26). If they are unrelated to the score everywhere, the selector
   returns the whole support (CIT p. 25 n. 1).
2. Build nested symmetric windows from a smallest window outward.
3. In each window, test the sharp null of no effect on each covariate and
   take the minimum p-value. A joint Hotelling statistic is an option (SJ
   p. 339; CIT p. 26).
4. The selected window is the largest one in which the minimum p-value is
   at least α* there and in every smaller window (SJ pp. 336, 346; CIT
   p. 25).

Settings and defaults:

- Smallest window: about 10 observations on each side. CFT's justification:
  with 10 per group and a one-SD shift, a difference-in-means randomization
  test has power of about 80% at α = 0.15 and 60% at 0.05 (CFT p. 9; SJ
  p. 336 n. 1; CIT p. 26). `rdwinselect` defaults: `obsmin(10)`,
  `obsstep(2)`, `nwindows(10)`, `level(.15)`, `statistic(ttest)`,
  `reps(1000)`, `seed(666)`, randomization inference unless `approximate`
  is set (SJ pp. 346–347). `wmin`/`wstep` define windows by length instead,
  and cannot be combined with `obsmin`/`obsstep` (SJ p. 346). In CIT's R
  call `wobs = 2` adds at least two observations per side at each step
  (p. 27).
- Threshold: α* = 0.15 (CFT p. 9; SJ default). CIT recommends at least 0.15
  where possible and no lower than 0.10 (p. 26). The roles of Type I and
  Type II error are reversed: a false verdict of balance is the error to
  avoid (CFT p. 8).
- No multiple-testing correction, on purpose: correcting would enlarge the
  window (CFT p. 9; SJ p. 336; CVB p. 141; JPAM p. 667).
- Fisherian tests are recommended for selection because the small windows
  hold few observations (CIT p. 26). The `approximate` option is fast but can
  mislead in small samples (SJ p. 354).
- A recommended window is printed only when covariates are supplied (SJ
  p. 346).

Caveats the sources themselves show:

- The minimum p-value is not monotone in window length (SJ p. 354; JPAM
  p. 667; CIT p. 28). Report the whole p-value plot so readers can see how α*
  moves the window (CFT p. 9).
- The selected window depends on the step. In the Senate data, `wobs = 2`
  selects [−0.7652, 0.7652] and `wstep = 0.1` selects [−0.8287, 0.8287] (CIT
  pp. 27–29). SJ with `wmin(.5) wstep(.125)` recommends [−.875, .875], then
  analyses [−.75, .75] to match CFT (pp. 353–354).
- The authors adjust the threshold to the data. In the probation example the
  smallest window's minimum p-value is 0.138, and the call sets
  `level = 0.135` (CIT p. 75).
- Balance in the smallest window carries little information when that
  window holds few observations. This follows from the power argument
  above (inference).
- Choose the window before looking at outcomes. `rdwinselect` never shows
  outcome results, which limits specification search (CIT p. 29). JPAM
  selects with the KS statistic, starting at 0.3 and stepping by 0.2
  (p. 667). The statistic is a choice to record.

## 4. The within-window outcome model: p = 0 versus adjusted

- p = 0 (default): no transformation. This is the CFT exclusion restriction,
  potential outcomes constant in the score inside W (SJ p. 335; JPAM p. 663).
- p ≥ 1: JPAM's extension subtracts side-specific polynomial slopes fitted
  by least squares inside W, then randomizes the intercept-only transformed
  outcomes (pp. 662–663; SJ pp. 334–335). The slopes are assumed common to
  all units on a side. The adjustment needs the polynomial to be correctly
  specified in the observed sample; misspecification invalidates the
  results (JPAM p. 663).
- With p ≥ 1 the difference-in-means statistic is the difference in
  intercepts. It equals a local linear (or polynomial) estimate with a
  uniform kernel and h = w (JPAM p. 666; SJ p. 338). The estimand becomes
  the ATE with the score evaluated at the cutoff (JPAM pp. 665–666).
- `evall`/`evalr` (Stata `rdrandinf`) or `evalat(cutoff|means)` set where
  the transformation is evaluated; the default is the cutoff (SJ pp. 344,
  347). With p = 1 evaluated at the side means, the point estimate equals
  the p = 0 difference in means, though p-values can differ (SJ p. 365).
- With p > 0, `rdrandinf` gives no asymptotic p-value or power for the KS
  and rank-sum statistics (SJ p. 358).
- CFT checks robustness by testing the same window with linear and
  quadratic difference-in-intercept statistics (pp. 17–18). In Design II,
  the sharp null was rejected with the linear statistic and not with the
  quadratic one in the chosen window (p. 17).

## 5. Sensitivity across windows

- `rdsensitivity` computes p-values over a grid of window lengths
  (`wlist`) and null effects (`tlist`). Under a constant-effect model, the
  non-rejected range in each column is a confidence interval (SJ
  pp. 340–341, 359–360). `ci(window level)` returns the interval for one
  window in `wlist` (SJ p. 348). Default `wlist`: 10 windows, the first with
  10 treated and 10 control, adding 5 per group each step. Default `tlist`:
  10 points inside the asymptotic CI of the smallest window (SJ p. 348).
- Which windows are informative: CIT says results in windows larger than a
  balance-selected W0 "will not be reliable". The analysis "should only
  consider windows smaller than W0" (p. 34). CFT reports larger windows but
  would not read a change there as evidence against W0. Smaller windows test
  for heterogeneity inside W0 (CFT p. 17). In CFT's Design II, the null in
  W0 = [−0.75, 0.75] concealed a significant negative effect in [−0.5, 0.5]
  (pp. 18–19).
- CVB: window sensitivity is very important even for local randomization
  methods (p. 143).

## 6. Rosenbaum-style bounds (`rdrbounds`)

- Model: inside W, Bernoulli assignment with
  P(D = 1) = exp(γU)/(1 + exp(γ)) for an unobserved binary U. The odds of
  treatment for two units differ by at most Γ = exp(γ) (SJ p. 341; JPAM
  p. 673). γ = 0 is a randomized experiment.
- Output: the Bernoulli p-value per window, then lower and upper p-value
  bounds for each Γ and window. Reading down a column is Rosenbaum's
  sensitivity analysis. Reading along a row shows sensitivity to the window
  (SJ pp. 363–364). The bounds apply to the sharp-null p-value, not to an
  effect size.
- Defaults differ from `rdrandinf`: `statistic(ranksum)`, `reps(500)`,
  `expgamma(1.5 2 2.5 3)`, and `prob()` set to the treated share in each
  window. `fmpval` adds the fixed-margins p-value (SJ pp. 349–350).
- Γ grids in practice: SJ uses 1.5–3 (p. 363); JPAM uses 1.1–1.4 and reports
  the largest upper bound in the chosen window (p. 673).
- Interference: `interfci()` gives Rosenbaum's (2007) interval for Δ, the
  excess of the observed statistic over a uniformity trial. It is not an
  interval for the point estimate and need not contain it (SJ pp. 340, 359;
  JPAM pp. 671–672).

## 7. Discrete running variables

- First step: count observations, distinct mass points, and observations
  per mass point near the cutoff (CIT pp. 62–64).
- Local polynomial methods "behave essentially as if each mass point is a
  single observation" (CIT p. 61). The effective sample is the number of
  mass points; collapsing to cell means gives close to the same fit (CIT
  pp. 69–70).
- Many mass points (CIT's example has 429): continuity methods are usable,
  including `rddensity` and CER-optimal covariate tests (CIT pp. 64–67).
  But τ at the cutoff is not nonparametrically point-identified with a
  discrete score, so parametric extrapolation from the nearest mass points
  is unavoidable at any sample size (CIT p. 71).
- Few mass points: polynomial fits are exploratory only unless strong
  parametric assumptions are imposed. Bandwidth selectors are inappropriate
  with very few (CIT pp. 62, 71). JPAM: for a discrete score "we recommend
  using local randomization methods as the primary analysis", with
  continuity methods possible under additional assumptions (p. 678).
- Local randomization with a discrete score uses the smallest window
  [x₋₁, c], the two mass points where treatment switches. No window selection
  is needed if both hold enough observations (CIT pp. 71–73; JPAM p. 678).
  If they do not, enlarge one mass point at a time using the covariate
  selector (CIT p. 73). Local randomization works with as few as two mass
  points (CIT p. 71).
- Whether LR2 is plausible depends on the measurement scale. One day of age
  is plausibly ignorable; one year of age at 64 may not be (CIT pp. 72–73).
  The descriptive alternative θ_SDS = E[Y(1)|X = c] − E[Y(0)|X = x₋₁] needs no
  local randomization but has no causal reading (CIT pp. 73–74).
- Density in the smallest window: CIT's binomial test rejects with 208
  control and 67 treated observations (p. 74). CIT does not treat this as
  proof of manipulation. Adjacent GPA values need not be equally likely,
  and covariate balance in the window is checked next (pp. 74–75). The
  q = 1/2 choice is justified from a large-sample view only for continuous
  scores (CIT p. 31). CVB and JPAM point to Frandsen (2017) for a
  discrete-score density test (CVB p. 142; JPAM p. 649).
- Clustering by the score. CIT shows `rdrobust` with `cluster = X` as an
  option that may be desirable in some applications (p. 69). KR show that running-variable
  clustering does not deliver valid inference: "CIs do not guard against
  model misspecification" (p. 2277). CRV standard errors are usually smaller
  than EHW ones when misspecification and the number of support points are
  small to moderate (pp. 2290–2291). In KR's CPS placebo study, nominal 95%
  CRV intervals cover as little as 58 percent (p. 2279; Table 1, p. 2283).
  CIT does not cite KR. On interval validity, follow KR.
- KR's remedies (pp. 2302–2303): with rich support, narrow the window and
  use EHW standard errors. Otherwise use an honest CI: BSD (second
  derivative bounded by a stated K, valid for discrete or continuous
  scores) or BME (designed for few support points with many observations
  at each). Details are in `kolesar_rothe_2018_discrete_rdd.md`.
- Heaping or rounding of a continuous latent score is a different problem
  from a truly discrete score (KR p. 2278 n. 2, citing Dong 2015). CIT lists
  rounding and heaping only as further reading (p. 77).

## 8. Falsification inside the window

- Test every predetermined covariate and placebo outcome in W0 with the
  same statistic and mechanism as the outcome (CIT p. 30). The covariates
  used to pick W0 are balanced by construction, so test another set as well
  (CIT p. 31).
- Placebo cutoffs: use windows of the same half-length around each
  artificial cutoff, with treated units only above the true cutoff and
  control units only below (CIT p. 33).
- In the continuity framework, each covariate gets its own bandwidth (CIT
  p. 30, with CER-optimal bandwidths per covariate, pp. 58, 66–67). CVB
  says not to reuse one neighborhood across outcomes, covariates and
  purposes (p. 143).

## Review use

- **Trigger.** The check fires when the score is discrete, or when the paper
  describes assignment near the cutoff as as-if random, uses a small fixed
  window, or reports randomization inference. Count mass points and
  observations per mass point within the paper's bandwidth before anything
  else. A paper that reports N in the thousands from a few dozen mass points
  has an effective sample of a few dozen for any local polynomial fit
  (CIT pp. 61, 69).
- **Estimand label.** Record whether each number is τ at the cutoff or θ in
  a stated window. A local-randomization result is not the RD effect at the
  cutoff unless p ≥ 1 is used and the polynomial is defended (CIT p. 20;
  JPAM pp. 663, 666). With a discrete score, any claim about τ at c rests on
  parametric extrapolation from the adjacent mass points (CIT p. 71). Say
  so, and price the claim as model-dependent.
- **Window provenance.** Failure: the window is ad hoc, chosen after
  outcome results, uses α* below 0.10, or starts from a smallest window with
  well under 10 observations per side. Recompute with `rdwinselect` at
  α* = 0.15 and the paper's covariates. Report the p-value plot and the
  windows from both an observation step and a length step. If the paper's
  window exceeds every reasonable selector's, its local-randomization claim
  is unsupported.
- **Null and interval.** A Fisherian p-value tests the sharp null. If the
  paper reads it as evidence about the average effect, require the
  large-sample p-value or a stated monotonicity assumption (JPAM p. 666).
  A randomization CI needs its effect model stated, usually constant
  additive effects (CIT p. 24). Record statistic, mechanism, repetitions and
  seed. A p-value within Monte Carlo error of 0.05 at 1,000 draws needs a
  rerun with more draws. That last rule is our inference; SJ's default is
  `reps(1000)`, and CFT and JPAM use 10,000.
- **Sensitivity.** Rerun in windows nested inside W0 (CIT p. 34; CFT
  p. 17). A sign change or loss of significance in a smaller window is a
  heterogeneity finding against a pooled claim. Results that hold only in
  windows larger than W0 do not support the claim. Report `rdrbounds` in W0:
  the Γ at which the upper-bound p-value crosses 0.05.
- **Discrete score and clustered errors.** If the paper's significance rests
  on CRV standard errors smaller than EHW ones, the claim fails. KR: any
  "CI with correct coverage must be at least as wide as the EHW CI"
  (p. 2299). Rebuild with EHW in a narrow window, or with BSD over a stated
  K range.
- **Density with a discrete score.** Run the binomial test at the smallest
  window and the selected window (`rdwinselect` reports it). An imbalance
  triggers covariate checks and an argument about the probabilities of the
  mass points (CIT pp. 74–75). It is not by itself a manipulation verdict.
  `rddensity` is still usable when mass points are numerous (CIT p. 64).
- **Agreement.** When local randomization and continuity disagree, the
  likely cause is a failed exclusion restriction with continuity intact.
  The continuity estimate then stands and the local-randomization one does
  not (JPAM p. 676). For a continuous score, local randomization is a
  robustness check. For a discrete score with few mass points, it is
  primary (JPAM p. 678; CIT p. 7).
