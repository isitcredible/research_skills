# Density manipulation testing — Cattaneo, Jansson & Ma (2018, 2020)

Distillation of Matias D. Cattaneo, Michael Jansson and Xinwei Ma, "Simple
Local Polynomial Density Estimators," *Journal of the American Statistical
Association* 115(531) (2020): 1449–1455 (published version; received
September 2017, accepted May 2019; main text audited, the supplemental
appendix with proofs, bandwidth formulas and simulations was not), and the
companion software article, Cattaneo, Jansson and Ma, "Manipulation testing
based on density discontinuity," *Stata Journal* 18(1) (2018): 234–261
(published). The software article cites the JASA paper as a 2017 working
paper and documents `rddensity` and `rdbwdensity` as first released; it does
not describe the later mass-point adjustment, the built-in binomial tests or
the separate `rdplotdensity` command. Defaults for those come from the R
package help (versions 2.5 and 3.0, which agree), and are marked as such. Interpretation draws on
Gerard, Rokkanen and Rothe, "Bounds on Treatment Effects in Regression
Discontinuity Designs with a Manipulated Running Variable," *Quantitative
Economics* 11 (2020): 839–870 (published; GRR below; the bounds themselves
are distilled in `rdd_methods_guide.md` §2), and on three Cattaneo-group texts for the
binomial test and discrete scores: Cattaneo & Titiunik, "Regression
Discontinuity Designs," *Annual Review of Economics* 14 (2022): 821–851;
Cattaneo, Titiunik & Vazquez-Bare, *Journal of Policy Analysis and
Management* 36 (2017): 643–681; Cattaneo, Idrobo & Titiunik, *A Practical
Introduction to Regression Discontinuity Designs: Extensions* (Cambridge
Elements, 2024). Source PDFs (not distributed with the skill):
`Cattaneo_Jansson_Ma_2020_LocalPolynomialDensity_JASA.pdf`,
`Cattaneo_Jansson_Ma_2018_rddensity_StataJ.pdf`,
`Gerard_Rokkanen_Rothe_2020_BoundsRDD_QuantitativeEconomics.pdf`.

Verification status: source-audited 2026-10-15.

Use in this battery: `rdd-diagnostics` core checks "Density test" and
"Manipulation-robust bounds" (reading a non-rejection); the conditional
"Discrete running variable and local randomization" check where it reroutes
the density test for discrete scores; the design-matrix RD core list and
local-randomization record; the `rddensity` snippet in the software examples.
Pairs with `rdd_methods_guide.md` §2 (GRR bounds).

## 1. The null hypothesis

The test asks whether the density of the running variable is continuous at
the known cutoff: H0 equates the left and right limits of f at the cutoff,
against the two-sided alternative that they differ (JASA §4, p. 1452; SJ
§2.1, p. 237). Units with score at or above the cutoff form the treated
side (SJ p. 237). The statistic is the difference of the two one-sided
density estimates, scaled by its standard error; the test is two-sided
(JASA p. 1453 rejects on |T|; SJ p. 243 uses the chi-squared form T²).

The rationale is one-directional: absent systematic manipulation the density
should be continuous, so a jump is read as evidence of self-selection or
sorting (SJ pp. 234–235). Density continuity is "neither necessary nor
sufficient for the validity of" an RD design (Cattaneo & Titiunik 2022,
p. 843). GRR make the link formal only under their model: with one-sided
manipulation, the jump identifies the share of manipulators among units just
right of the cutoff, τ = 1 − f(c−)/f(c+) (GRR Lemma 1, p. 846).

## 2. The estimator, and why it improves on McCrary

- The density at a point is the slope coefficient of a local polynomial fit
  to the empirical distribution function; it "does not require prebinning of
  the data" (JASA pp. 1449–1450). The only tuning parameter is the bandwidth
  (JASA p. 1449), and the estimator is valid at boundary points without
  modification, which a density test at a cutoff requires because each side
  is estimated as a boundary (JASA pp. 1450, 1452).
- McCrary (2008) built on the Cheng–Fan–Marron estimator, which needs
  prebinning and two tuning parameters (bin width and bandwidth) (JASA
  p. 1450; SJ p. 235).
- In the Head Start illustration McCrary's effective sample is 24 bins per
  side against 65–1,598 observations per side for the new tests (JASA
  Table 1, p. 1454); the authors attribute a reduction in power to the
  prebinning (JASA p. 1454).
- The software article claims better size, and more power under additional
  assumptions, than the alternatives then available (SJ abstract, p. 234).
- Recommended order: p = 2, the minimal odd choice analogous to local linear
  regression (JASA p. 1452).

## 3. Inference: only the robust row is valid at the default bandwidth

- `rddensity` computes the statistic at an MSE-optimal bandwidth for the
  order-p estimator, then tests with order q = p + 1 and the matching standard
  error (robust bias correction). This is the default and the recommended test
  (JASA p. 1453; SJ pp. 243, 251). With p = 2 this is T3(ĥ2), the JASA's
  recommended statistic (p. 1454).
- The conventional statistic Tp at an MSE-optimal bandwidth is invalid: its
  first-order bias makes it over-reject (JASA p. 1454; SJ p. 244). The `all`
  option prints it beside the robust row, labelled "Conventional" (SJ
  pp. 245, 251). In the simulations the conventional test at the infeasible
  MSE-optimal bandwidth has empirical size 0.208 (plug-in SE) and 0.232
  (jackknife SE) at nominal 0.05, p = 2 (SJ Table 1, p. 255). The robust row
  stays near nominal size (SJ pp. 255, 257).
- A conventional test is valid only with an undersmoothed bandwidth (SJ
  p. 244).
- Standard errors: jackknife by default, with a plug-in alternative for large
  samples (SJ p. 240; options p. 245).
- Software defaults (SJ pp. 244–245; same in the R help, versions 2.5 and 3.0): `c` = 0,
  p = 2, q = p + 1, kernel triangular, `fitselect` unrestricted, `bwselect`
  comb, `vce` jackknife.
- The R help (2.5 and 3.0) adds `massPoints = TRUE` and `bino = TRUE` as defaults.
  It also adds `regularize = TRUE`, which forces each local neighbourhood to
  hold at least 20 + p + 1 observations and 20 + p + 1 unique values.

## 4. Bandwidths and the restricted model

- `rdbwdensity` offers AMSE-based selectors (SJ pp. 240–242):
  - `each`: separate left and right bandwidths, available only in the
    unrestricted model;
  - `diff`: one common bandwidth chosen for the difference of the densities;
  - `sum`: one common bandwidth chosen for their sum;
  - `comb` (default): the median of each/diff/sum on each side in the
    unrestricted model, and the minimum of diff and sum in the restricted
    model.
- `comb` exists because some bias constants can be exactly zero for
  particular p, which makes a single selector degenerate (SJ p. 242).
- The restricted model imposes equal distribution function and equal
  higher-order derivatives on both sides, leaving only the density itself
  free to jump. It forces a common bandwidth (SJ pp. 239–240). The power
  gain is conditional on those restrictions holding (SJ p. 239).
- In the Senate example the restricted test gives p = 0.140 against 0.381
  unrestricted (SJ pp. 248, 251).
- Inference: a rejection that appears only under the restricted model rests
  on the equal-derivatives restriction and should be reported as such.

## 5. Power, and how to read a non-rejection

- Simulation design (SJ §6.2, Table 2, p. 258): n = 1,000, a scaled t(5)
  score, cutoff 0.5, 2,000 replications.
- The default test (p = 2, q = 3, estimated separate bandwidths, jackknife
  SE) rejects at these rates, by f+/f− (density just right of the cutoff
  over density just left):

  | f+/f− | 0.5 | 0.8 | 1.2 | 1.3 | 1.5 |
  |---|---|---|---|---|---|
  | rejection rate | 0.450 | 0.118 | 0.062 | 0.104 | 0.200 |

- Bias correction costs some power relative to the invalid conventional
  statistic (SJ p. 259).
- Inference (combining SJ Table 2 with GRR Lemma 1): f+/f− = 1.5 means
  one-third of units just right of the cutoff are manipulators (τ = 0.33).
  In this design that share is missed four times in five. A non-rejection
  at a sample of this size does not bound τ near zero.
- GRR (pp. 840–841): "a non-rejection may not be due to the absence of"
  manipulation, but to low power.
- Inference (not in the sources; a power calculation on the test's own
  statistic): the robust statistic is the density difference over its
  jackknife SE (`hat$diff / sd_jk$diff` in the R fit, the robust-order SE),
  so the jump detectable with 80% power at two-sided 5% is about
  2.80 × `sd_jk$diff`. Set it against the density level on each side to
  express it as a manipulation share.
- GRR recommend their bounds "irrespective of the outcome" of the density
  test (pp. 841, 862).
- In GRR's application the estimated τ is 0.064 (95% CI 0.038–0.089), with
  102,791 observations within the bandwidth (Table 2, p. 861). Assuming
  τ = 0.025 instead of zero doubles the width of the confidence interval
  (p. 861).

## 6. What the test cannot detect

- **Density-preserving sorting.** The test sees counts, not identities.
  Sorting that leaves the density continuous passes. Examples (inference):
  flows across the cutoff in both directions that offset each other, or a
  change in which units sit just above the cutoff without a change in how
  many. GRR model only one-sided manipulation, stated as their "only
  substantial requirement" (p. 841). Under that model a continuous density
  implies τ = 0 (Lemma 1, p. 846), so their bounds collapse to the point
  estimate when the density is continuous. Predetermined-covariate balance
  is the complementary check. GRR also show that the distribution of
  covariates among manipulators and non-manipulators is identified (§3.4,
  p. 853).
- **Mechanical discontinuities** produce a jump with no manipulation.
  Examples: calendar artefacts, and heaping at a round-number cutoff that
  coincides with the threshold.
  - GRR drop workers previously laid off after the 28th of a month. Otherwise
    the 28-day February creates bunching at their 16-month cutoff without
    manipulation (fn. 15, pp. 857–858).
  - GRR's model rules out manipulators sitting exactly at the cutoff value.
    If they did, they could be identified by that value and removed (GRR
    pp. 843–844).
- **Manipulation away from the cutoff** that does not change the local
  density is outside the test (inference from the local null in §1).

## 7. Discrete, heaped and mass-point running variables

- The JASA theory assumes a continuous random variable with a distribution
  function p + 1 times continuously differentiable near the evaluation point,
  and a positive density there (§2, p. 1450; Assumption 1, p. 1451). A truly
  discrete score has no density, so the null in §1 is not defined for it.
- The software article nevertheless says the methods "can also be used under
  additional assumptions" in RD designs with a discrete running variable
  (SJ p. 235). It does not state those assumptions. It cites Frandsen (2017)
  as a manipulation test built for discrete scores (SJ p. 235).
- Cattaneo, Idrobo & Titiunik (2024) make the number of distinct mass points
  the deciding quantity:
  - Local polynomial methods treat each mass point roughly as one
    observation. With many mass points near the cutoff they may still be
    appropriate; with few, local randomization is the natural alternative
    (p. 61).
  - They run `rddensity` on a discrete score with 429 mass points as a
    legitimate continuity-based falsification test (pp. 64–66).
- Inference: with heaping, a continuous score rounded to a grid, the
  estimator is smoothing a step-function CDF. The effective information is
  the number of heaps within the bandwidth, not N. If a heap falls at the
  cutoff it is assigned to the treated side by the ≥ convention (SJ p. 237)
  and inflates the right-hand density.

## 8. The binomial test near the cutoff

- The JASA paper lists the finite-sample binomial test of Cattaneo, Titiunik
  & Vazquez-Bare (2017) as an existing alternative, based on local
  randomization (p. 1452).
- The test (CTV 2017, p. 650): within a window [c − h, c + h], under random
  assignment with probability q, the count of units on the treated side is
  binomial. Absent other information, q = 1/2 is the natural choice. The
  p-value is exact.
- The test is valid for continuous or discrete scores (Cattaneo & Titiunik
  2022, p. 844): "Unlike the continuity-based density test, the binomial
  test can be used when the score" is continuous or discrete.
- The window is the tuning parameter. With q = 1/2 the test assumes equal
  expected mass on both sides of the window. Inference: that assumption is
  questionable for a wide window where the density slopes, so the test
  belongs in small windows.
- Implementations:
  - `rdwinselect` (in `rdlocrand`) reports a binomial-test p-value for each
    nested window (rdlocrand article, *Stata Journal* 16(2) (2016),
    pp. 346, 353).
  - In R versions 2.5 and 3.0, `rddensity` runs binomial tests by default
    (`bino = TRUE`; `binoP = 0.5`; 10 nested windows, the smallest holding
    at least 20 observations per side, per the help). The help cites the
    same exact-binomial approach.
  - Cattaneo, Idrobo & Titiunik (2024, p. 57) use `rddensity` with a
    `binoW` window to run the local-randomization density test.

## 9. Fuzzy designs

The test is run on the running variable, which is the assignment side. In a
fuzzy design it therefore checks the intention-to-treat mechanism: the "test
applies to the intention-to-treat mechanism" (SJ p. 237). It is not run on
take-up.

## Review use

- **Trigger.** Any RD result. Run `rddensity` with its defaults on the
  estimation sample and cutoff the paper uses.
- **Report.** The robust row's T and p-value, the bandwidths and effective N
  on each side, the two density estimates, and the implied τ̂ = 1 − f̂−/f̂+.
- **Wrong or outdated test reported by the paper.** A paper that reports
  the "Conventional" row, a conventional Wald test at an MSE-optimal
  bandwidth, or McCrary's binned test has reported an over-rejecting or a
  lower-powered test. Re-run with the robust default and record which the
  paper used.
- **Non-rejection.** Never clearance. Set the effective N against the power
  figures in §5. Where the claim is load-bearing, compute GRR's fixed-τ
  breakdown point: the largest assumed manipulation share at which the
  headline interval still excludes zero (GRR pp. 855–856). Compare it with the upper
  confidence limit for τ. If that limit exceeds the breakdown point, the
  test has not ruled out enough manipulation to overturn the result.
- **Rejection.** Not an automatic kill. First check for mechanical causes:
  calendar effects, round-number heaps at the cutoff, observations exactly
  at the cutoff value. Then take the GRR route: bounds plus the
  manipulation-robust interval, with the one-sided-manipulation assumption
  argued from institutions.
- **Restricted model.** A rejection that appears only under
  `fitselect(restricted)` rests on the equal-derivatives restriction. Say
  so.
- **Discrete scores.** Count the distinct values within the density
  bandwidth on each side.
  - Many mass points: `rddensity` is admissible. Confirm the mass-point
    adjustment was on.
  - Few mass points: the continuity test is not verdict-bearing. The
    manipulation check is the binomial test in the smallest window and the
    chosen window, plus covariate balance in the same windows.
  - Report the continuity test beside it whenever it can be run.
- **Covariate imbalance without a density jump.** Sorting the density test
  cannot see, and GRR bounds do not address it, since τ̂ ≈ 0. It is a
  separate design-validity finding.
