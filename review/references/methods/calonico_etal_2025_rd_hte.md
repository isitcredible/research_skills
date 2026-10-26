# Treatment-effect heterogeneity in RD designs — Calonico, Cattaneo, Farrell, Palomba & Titiunik (2025)

Working distillation of Sebastian Calonico, Matias D. Cattaneo, Max H. Farrell,
Filippo Palomba and Rocío Titiunik, "Treatment Effect Heterogeneity in
Regression Discontinuity Designs," manuscript dated **July 3, 2025** — a
**working paper**: the title page carries no journal furniture, and the paper's
own reference list cites the companion software as arXiv:2507.01128. Verify
against the published version before quoting. The audited text is the
28-page main paper only; the supplemental appendix (MSE expansion, bias and
variance formulas, results without Assumption 2, kink designs, the survey of
AEA papers) was not available and is not covered here. Source PDF:
`Calonico_Cattaneo_Farrell_Palomba_Titiunik_2025_HTE_RD_wp.pdf` (not
distributed with the skill). Page numbers are the manuscript's own, which
equal the PDF pages.

Verification status: WP-audited 2026-10-15. Section 8 adds software facts
from the package repository (rdpackages.github.io/rdhte, accessed
2026-10-15); those are not claims of the paper.

Use in this battery: `rdd-diagnostics` conditional check **Heterogeneous RD
effects**; the design-matrix RD conditional line on `rdhte`; the `rdhte`
snippet in the software examples.

## 1. Scope

- Sharp RD with a continuous running variable only (§2, p. 6; Assumption 1,
  p. 12). Fuzzy designs are named as future research (§5, p. 22). Kink
  designs are covered only in the supplemental appendix (p. 9, p. 22).
- The heterogeneity variables W are pretreatment covariates chosen by the
  researcher. Covariates Z used only for precision are a separate set
  (p. 6, pp. 10–11).
- The authors recommend against using covariates to "fix" a broken RD
  design (pp. 5–6).

## 2. Estimand and specification

- Target: the CATE at the cutoff, κ(w) = E[Y(1) − Y(0) | X = 0, W = w],
  eq. (2.4), p. 8.
- Estimator: one kernel-weighted local-linear regression of Y on T, W, T·W,
  X, T·X, X·W and T·X·W, eq. (2.5), p. 9, with κ̂(w) = θ̂ + ξ̂′w, eq. (2.6).
  The coefficient on T is no longer the average effect. It is κ(0), the
  effect for the baseline group. ξ̂ is the difference from baseline (binary
  W) or the slope of κ(w) (continuous W) (p. 9).
- The fit is nonparametric in X only. There is no approximation to unknown
  functions of W (pp. 9–10). Changing which covariates enter W, or how they
  are coded, changes the estimand (p. 10).
- Categorical W must enter as indicators for every relevant category, which
  makes them orthogonal binaries (p. 10). Continuous W enters directly, and
  polynomials may be added (p. 10, p. 14).
- Mixed adjustment (eq. 2.7, p. 11) adds efficiency covariates Z, interacted
  with W but not with T or X. Fixed effects enter the same way (p. 12).
- **Sample splitting.** The paper does not say a subgroup split is invalid.
  For discrete W, separate standard RD fits by subgroup (eq. 2.2) recover
  the estimates in (2.5). Joint estimation is preferred because it is
  simple and makes adding controls natural (p. 10). The paper's objection
  is to the inference that usually comes with the split (§§5–6 below).
  *Inference:* the equivalence is exact when each subgroup fit uses the
  same bandwidth and kernel as the corresponding cell of the joint fit.

## 3. Identification

- **Assumption 1** (p. 12) includes continuity in x of E[W | X = x]. The
  paper reads this as no RD effect on W, and it calls the requirement that
  W be pretreatment the most important substantive condition (pp. 12–13).
- **Assumption 2** (local CATE structure, p. 13): E[Y(1) − Y(0) | X = x,
  W = w] = θ(x) + ξ(x)′w and E[Y(0) | X = x, W = w] = α(x) + λ(x)′w. This
  makes κ(w) linear in w at the cutoff.
- For binary W, or orthogonal indicators of a categorical variable,
  Assumption 2 holds automatically (p. 14). For continuous W it restricts
  the long regression, and the paper asks for caution in interpretation
  (p. 14).
- Without Assumption 2 the coefficients converge to a best mean-square
  approximation that is "often neither useful nor interpretable as
  heterogeneous causal effects" (p. 14; also pp. 14–15).
- Theorem 1 (p. 14): under Assumptions 1–2, h → 0 and nh → ∞, κ̂(w) is
  consistent for κ(w).

## 4. What the interacted fit cannot do

- It does not estimate the average effect τ (p. 11). Two possible remedies
  are rejected: demeaning W on each side of the cutoff, and averaging the
  fitted CATEs. Both amount to Nadaraya–Watson estimation at a boundary,
  with bias of order h (p. 11).
- The average effect should come from the standard fit (2.2), or the
  covariate-adjusted fit (2.3) with non-interacted covariates (p. 11).

## 5. Bandwidth choice

- Theorem 2 (p. 16): the MSE-optimal bandwidth h*_s = (V_s / (4B²_s n))^{1/5}
  depends on the target, through the selector vector s. Subgroup effects,
  slopes and differences each have their own optimum. A small group
  (higher variance) or a group with different curvature (different bias)
  moves it (p. 16).
- Common bandwidth: the paper says the constant matters less than getting
  the magnitude right, and that "this perspective supports the common
  practice of employing the same bandwidth for the estimation of all
  heterogeneous RD treatment effects" (p. 16).
- Options it endorses (p. 17): group-specific bandwidths; one common
  bandwidth (for example the ATE bandwidth from (2.2)); the median of the
  relevant bandwidths; or, for robust inference, the smallest of the set.
  Different bandwidths for different tasks "may yield more accurate
  inference in some applications" (p. 17).
- In the application, the discretized subgroup rows use subgroup-specific
  bandwidths (for example h = 0.188 below the median and 0.154 above). The
  continuous-income rows use one h = 0.152 (Table 1, p. 23).

## 6. Robust bias-corrected inference

- At an MSE-optimal bandwidth the estimator's limiting distribution is not
  centred on the target, so conventional inference is invalid (pp. 15,
  17–18).
- RBC (eq. 3.2, p. 18) subtracts an estimate of the bias and uses a
  variance that includes the variability of the bias correction. Theorem 3
  (p. 18) gives asymptotic normality for any linear combination s′ς at
  h = h*_s. Heteroskedasticity- and cluster-robust variance estimators are
  covered in the supplement (p. 18).
- A CI for κ(w) uses s = (1, w)′ (p. 19). **The test of no heterogeneity**
  for binary W is H0: ξ(0) = 0, with s = (0, 1)′ (p. 19).
- Report the point estimates from the unadjusted fit next to the RBC
  intervals and p-values, not the bias-corrected point (p. 19).
- Application (Akhtari et al. 2022, *AER*): the original paper paired a
  data-driven optimal bandwidth with conventional standard errors. The
  authors write that "valid inference requires robust bias correction, as
  standard errors from the linear fit are invalid when paired with the
  optimal bandwidth" (p. 20). After RBC, the effect is significant only
  below median income (above median: RBC CI [−0.043; 0.238], p = 0.174).
  The RBC 95% CI for the difference is [−0.422, −0.078] (p. 20; Table 1,
  p. 23).

## 7. Discrete versus continuous heterogeneity variables

- The paper's survey of AEA papers reports three patterns (p. 4): most
  studies use binary covariates, often by discretizing continuous ones; one
  ad hoc bandwidth serves both average and heterogeneity analysis; and
  "inference is rarely conducted properly, regardless of bandwidth choice
  or covariate granularity" (p. 4).
- The application compares a median split, quartiles, deciles, and income
  entered linearly and quadratically (pp. 20–21; Table 1 and Fig. 1,
  pp. 23–24). The continuous models match the discretized pattern and
  are more precise, but they need Assumption 2. The choice is left to the
  researcher (p. 21).
- One coarse split can hide the shape: the application finds most of the
  variation across the median and little within the halves (p. 21).

## 8. Software

**What the paper says.** It names one package, `rdhte`, as a
general-purpose implementation (p. 6; reference list, p. 25). It does not
describe `rdbwhte`, `rdhte_lincom`, any argument name, or any default.

**Package repository, not the paper** (rdpackages.github.io/rdhte and the R
source, accessed 2026-10-15; confirm in the installed help):
- `rdhte`: point estimation and RBC inference for conditional RD effects.
  `rdbwhte`: bandwidth selection for these effects. `rdhte_lincom`:
  post-estimation tests of linear combinations, `rdhte_lincom(model,
  linfct, level = 95)`, which returns individual tests (not adjusted for
  multiplicity) and a joint Wald test, evaluated at the per-group
  bandwidths. `rdhte_contrast(model, contrast)` (version 0.2.0) refits a
  chosen contrast at the bandwidth MSE-optimal for that contrast and returns
  its RBC estimate, SE, p-value and interval; it is the direct test of "the
  effect is larger in group g" and gives a different interval from
  `rdhte_lincom`. Hypothesis names in `linfct` follow the name of the
  object passed as `covs.hte` (check `names(fit$coef)`).
- R `rdhte(y, x, c = 0, covs.hte, covs.eff, p = 1, kernel = "tri", h,
  vce = "hc3", cluster, bwselect = "mserd", bw.joint = FALSE, ...)`. `q`
  defaults to p + 1.
- `bw.joint = FALSE` (the default) gives each group its own bandwidth. A
  continuous `covs.hte` always gets one joint bandwidth.
- A factor `covs.hte`, or a single 0/1 indicator, is treated as categorical.
  Any other numeric covariate is treated as continuous, so a numeric code
  for quartile 1–4 is fitted as a linear slope.
- No fuzzy-design argument (consistent with §1).
- The default `vce = "hc3"` differs from `rdrobust`'s nearest-neighbour
  default; with `cluster` the default becomes CR1. Match the paper's
  variance and cluster choice explicitly.

## 9. Interpretation

- κ(w) is the effect of the RD treatment for units at the cutoff with
  W = w, under Assumption 2 (pp. 13–14). This is what the abstract means
  by a causal interpretation.
- *Inference, not stated in the paper:* ξ compares treatment effects across
  subpopulations defined by W. It is not the effect of changing W. W is
  correlated with whatever else differs between those subpopulations, so
  'the effect is larger in poor municipalities' does not show that poverty
  causes the larger effect. Reading a CATE difference as a mechanism needs
  the exclusion assumptions in `fu_slough_2026_hte_mechanisms.md`.

## Review use

- **Trigger.** An RD paper claims the discontinuity differs by a covariate
  (subgroup table, interaction term, split-sample columns, 'the effect is
  concentrated among …').
- **Design scope.** If the design is fuzzy, the paper's framework does not
  cover it (p. 22). *Inference:* check the subgroup reduced form with this
  method, and check the subgroup first stage separately before accepting
  a subgroup LATE contrast.
- **Pretreatment check.** Run the RD continuity test on W itself at its own
  data-driven bandwidth (`rd_practice_guide.md` §6.1), and at the headline
  bandwidth as a labelled supplement. If W jumps at the cutoff, Assumption 1
  fails (pp. 12–13), and the subgroups are not comparable across the
  cutoff.
- **Inference check.** Each subgroup estimate needs an RBC interval, and
  the heterogeneity claim needs an RBC interval or test for the
  *difference* (ξ, p. 19). Conventional SEs at an MSE-optimal bandwidth
  are invalid (p. 20). A pattern where one subgroup is significant and the
  other is not does not establish heterogeneity (see
  `gelman_stern_2006_difference_test.md`). If the difference interval
  covers zero, the claim is 'heterogeneity not established'.
- **Do not fault a split as such.** Separate subgroup fits are legitimate
  (p. 10), and group-specific bandwidths are a permitted option (p. 17).
  Fault the inference, not the split.
- **Bandwidth.** Record whether the paper used a common or a group-specific
  bandwidth and how it was chosen. Re-run with the ATE bandwidth and with
  group-specific bandwidths. As the robust option, add the smallest
  bandwidth in the set (p. 17). A difference that survives only one of
  these is fragile.
- **Continuous W.** A linear (or polynomial) interaction imposes Assumption
  2 (p. 14). Compare it with a discretized fit, as the paper does (p. 21).
  If the binned estimates depart from the fitted line, the linear-in-W
  summary is not a causal heterogeneity estimate.
- **Coding is part of the estimand.** Median split, quartiles and deciles
  are different estimands (p. 10). *Inference:* if the cut point was not
  fixed before the analysis, treat the chosen split as one draw from a
  set of options and ask for the others.
- **No averaging.** An overall effect built by averaging subgroup
  estimates, or taken from the T coefficient of an interacted model, is
  not the RD average effect (pp. 9, 11). The overall effect comes from the
  standard fit.
- **Software pitfalls.** Pass categorical heterogeneity variables to
  `rdhte` as factors, set `cluster` to the paper's level, and state
  `bw.joint` (§8).
