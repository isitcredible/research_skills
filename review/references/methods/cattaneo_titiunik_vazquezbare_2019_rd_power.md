# Power and sample size for local-polynomial RD — Cattaneo, Titiunik & Vazquez-Bare (2019)

Working distillation of Matias D. Cattaneo, Rocío Titiunik and Gonzalo
Vazquez-Bare, "Power calculations for regression-discontinuity designs,"
*Stata Journal* 19(1) (2019): 210–245, doi:10.1177/1536867X19830919 —
published version (journal furniture on the title page). Source PDF:
`Cattaneo_Titiunik_VazquezBare_2019_rdpower_StataJ.pdf` (not distributed with
the skill). Page numbers are journal pages; the PDF page equals the journal
page minus 209.

Verification status: source-audited 2026-10-15. Section 6 adds facts from
the current package repository (rdpackages.github.io/rdpower, accessed
2026-10-15). Those facts are not claims of the article.

Use in this battery: `rdd-diagnostics` conditional check **Minimum
detectable effect**; the design-matrix RD conditional line on `rdmde` /
`rdpower`; the `rdpower` snippet in the software examples. It pairs with
`gelman_carlin_2014_type_ms.md` for the retrospective reading.

## 1. What the article introduces

- Two Stata commands, **`rdpow`** and **`rdsampsi`**, with companion R
  functions "with the same syntax and capabilities" (abstract, p. 210;
  p. 244). The article does not name the R functions.
- **`rdmde` does not appear in this article.** A minimum-detectable-effect
  command was added to the package later (§6). Cite the package, not this
  article, for `rdmde`.
- `rdpow`: power of the RD test for a hypothesized effect τ_A, given the
  data and optionally a new sample size or bandwidth (pp. 212, 217–218).
- `rdsampsi`: the minimum effective sample size inside the window needed
  to reach a target power, plus the treated/control split (pp. 212,
  218–219).
- Both commands call `rdrobust` for bandwidths, biases and variances. All
  `rdrobust` options carry through, including covariates, clustering,
  fuzzy and kink designs, and the full list of selectors (p. 211; options
  pp. 221–223).

## 2. Two uses the article distinguishes (p. 212)

1. **Ex-post (observational).** The data are final. `rdpow` estimates the
   power of `rdrobust`'s RBC test against a hypothesized τ_A at the fixed
   sample size, for example to compare local-linear with local-quadratic
   power.
2. **Ex-ante (design).** The data are not yet collected. `rdsampsi`
   computes the sample needed. The article notes that RD typically needs
   larger samples than a randomized experiment for the same power
   (p. 212).

## 3. The power function, bandwidth and variance

- Generic approximation (eq. 1, p. 215): (τ̂ − τ − B)/√V → N(0, 1), with
  left and right biases B∓ and variances V∓ scaled by side-specific
  bandwidths h∓. It covers sharp, fuzzy, kink and fuzzy-kink designs,
  covariate adjustment and clustering (pp. 215–216).
- **Conventional (misspecification) power function** (p. 216): built from
  τ + B̂ and the conventional V̂. It is not the default. At τ = 0 it
  exceeds α, so "conventional inference with misspecification bias will
  show higher power but at the expense of size distortion" (p. 216).
- **RBC power function** (p. 217): β̂(τ) = 1 − Φ(τ/√V̂_bc + z_{1−α/2}) +
  Φ(τ/√V̂_bc − z_{1−α/2}), where V̂_bc is the robust bias-corrected
  variance. "This power function is the default in rdpow and rdsampsi."
  (p. 217).
- **Default bandwidth:** the common MSE-optimal bandwidth for p = 1 under
  `rdrobust`'s defaults (p. 217). The default selector is `mserd`
  (pp. 222, 226).
- **Default variance estimator:** `vce(nn 3)`, the nearest-neighbour
  heteroskedasticity-robust estimator. The hc0–hc3, nncluster and cluster
  variants are options (pp. 223, 226–227).
- Other defaults (pp. 221–222): `c(0)`, `alpha(0.05)`, `p(1)`, `q(2)`,
  `kernel(triangular)`, `deriv(0)`. `rdsampsi` adds `beta(0.8)`, and its
  `nratio` defaults to σ₊/(σ₋ + σ₊) (pp. 224–225).
- **Default alternative τ_A:** half the standard deviation of the control
  outcome inside [c − ĥ, c) (p. 217; option `tau()`, p. 221).
- **User overrides** (pp. 217–218, 221): `samph()` sets new bandwidths,
  `sampsi()` sets new in-window sample sizes, and `bias()` / `variance()`
  set the bias and variance directly. With new bandwidths or sample sizes
  the variance is rescaled by an adjusted effective n (p. 218). Without
  data, `nsamples()` supplies the four sample counts (p. 221; example
  p. 235).
- **Sampling rule for new data:** sample the units closest to the cutoff
  first, on each side, until the target counts M₀ and M₁ are reached
  (pp. 219–220).

## 4. The illustration: what moves power (U.S. Senate data, n = 1,297)

All numbers below are power against τ = 5 vote-share points at α = 0.05,
unless stated otherwise.
- Default RBC, local linear, h = 17.708: power 0.818 (pp. 228–229). Adding
  three covariates: 0.812 (p. 229).
- Manual h(16 18), b(18 20): 0.707 (p. 230).
- Uniform kernel with state-clustered SEs: 0.958 (p. 231).
- With `all`: conventional power is 0.964 against RBC 0.818, and the
  conventional test has a size distortion of 0.0133 (p. 232).
- Inflating the variance by 20%: power falls to 0.745 (p. 234).
- Polynomial order: at h = 20, local linear gives 0.724 and local quadratic
  0.488 (pp. 235–236). At their own MSE-optimal bandwidths: 0.818 against
  0.666 (pp. 236–237).
- `rdsampsi`, target power 0.8: RBC needs 656 in-window observations (290
  left, 366 right). Conventional needs 381, with a size distortion of
  0.057 (pp. 238, 240).
- A local-constant fit needs one-half to one-third of the local-linear
  sample. The article warns that "this feature should not be interpreted
  as implying that the constant specification is superior" (p. 243),
  because a lower order means a larger misspecification bias.

## 5. What the article does not discuss

- It contains no minimum-detectable-effect output and no discussion of
  observed or post hoc power, in which τ_A is set to the estimate.
- It does not cover power for the density (manipulation) test, covariate
  balance tests or local-randomization inference. It is limited to the
  continuity-based local-polynomial RD estimand (p. 211).
- *Inference:* power evaluated at the point estimate is a monotone
  transform of that estimate's own z-statistic. It adds nothing to the
  printed p-value, and it is always low for a null. The informative
  calculation fixes τ_A from outside the data: a prior literature, a
  policy-relevant effect, or the effect the paper's argument requires
  (the retrospective design analysis in `gelman_carlin_2014_type_ms.md`).

## 6. Later software (package repository, not the article)

Source: rdpackages.github.io/rdpower and its R source, accessed 2026-10-15.
Confirm in the installed help.
- The current release lists three tools: `rdpower` (ex-post power),
  `rdsampsi` (sample size) and `rdmde` (MDE). In the current Stata
  distribution the power help file is named `rdpower`, where the 2019
  article used `rdpow`. Stata install: `net install rdpower,
  from(https://raw.githubusercontent.com/rdpackages/rdpower/main/stata)
  replace`.
- **Name collision:** an unrelated SSC module, also called `rdpower`
  (E. C. Hedberg; power for randomized, cluster and block designs), is
  what `ssc install rdpower` fetches. It has a different syntax and does
  not do RD.
- R `rdmde(data = cbind(Y, R), cutoff = 0, alpha = 0.05, beta = 0.8,
  samph, sampsi, bias, variance, covs, p = 1, h, b, kernel = 'triangular',
  bwselect = 'mserd', vce = 'nn', cluster, fuzzy, ...)`. The headline MDE
  uses the RBC variance at the `rdrobust` main bandwidth, unless `samph`
  or `variance` override it. Bias enters only the conventional MDE.
  `init.cond` (default 0.2 × SD of Y below the cutoff) is a solver
  starting value, not an alternative hypothesis.

## Review use

- **Trigger.** An RD null or small effect carries the argument ('no
  effect of …', 'rules out …', 'precisely estimated zero'), or the paper
  reports its own RD power analysis.
- **Match the specification.** Compute power or MDE at the paper's
  bandwidth, polynomial order, kernel, covariates and clustering: pass
  `h`/`samph`, `p`, `kernel`, `covs`, `vce`/`cluster`. A default run
  re-selects an MSE-optimal bandwidth with an unclustered NN variance,
  which describes a different test from the one that produced the null.
- **Use the RBC power function** (the default). Conventional power is
  overstated, with a size distortion (pp. 216, 232). Lowering the
  polynomial order to raise power is not a defence (p. 243).
- **Choose τ_A from outside the data.** Never use the estimate itself, and
  do not accept the default half-SD unquoted. Report power at the effect
  the paper's own argument or the literature treats as meaningful, and
  report the MDE at 80% power with two-sided α = 0.05.
- **Quick check without data** (*inference*, from the RBC power function
  on p. 217, ignoring the opposite tail): se_rbc ≈ (RBC CI width)/3.92,
  and MDE₈₀ ≈ 2.80 × se_rbc ≈ 0.71 × the RBC CI width. If the MDE exceeds
  the smallest effect the paper says it rules out, the null is
  uninformative about that effect.
- **What a failure costs.** An underpowered null is reported as
  'inconclusive at effects below the MDE', not as evidence of no effect. A
  paper that claims to rule out an effect smaller than its MDE has
  overclaimed.
- **Scope.** These tools do not give a detectable effect for the density
  or balance tests. A non-rejected `rddensity` test needs its own
  sensitivity argument.
