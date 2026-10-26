# Panel methods: dependence structure, FE margins, dynamics, and selection

Source-audited crib for the panel battery. One decision spine: the claimed
margin (within/between), the dependence the SE must absorb, the dynamics the
estimator must survive, and the selection the sample actually supports.

**Sources audited (all source PDFs not distributed with the skill):**
- Cameron, Gelbach & Miller, "Robust Inference with Multiway Clustering,"
  *JBES* 29(2) (2011), 238–249 — published.
- Driscoll & Kraay, "Consistent Covariance Matrix Estimation with Spatially
  Dependent Panel Data," *ReStat* 80(4) (1998), 549–560 — published.
- Pesaran, "General Diagnostic Tests for Cross-Sectional Dependence in
  Panels," *Empirical Economics* 60 (2021), 13–50 — published.
- Pesaran, "Estimation and Inference in Large Heterogeneous Panels with a
  Multifactor Error Structure," *Econometrica* 74(4) (2006), 967–1012 —
  published.
- Bai, "Panel Data Models with Interactive Fixed Effects," *Econometrica*
  77(4) (2009), 1229–1279 — published.
- Mundlak, "On the Pooling of Time Series and Cross Section Data,"
  *Econometrica* 46(1) (1978), 69–85 — published.
- Nickell, "Biases in Dynamic Models with Fixed Effects," *Econometrica*
  49(6) (1981), 1417–1426 — published.
- Arellano & Bond, "Some Tests of Specification for Panel Data: Monte Carlo
  Evidence and an Application to Employment Equations," *Review of Economic
  Studies* 58(2) (1991), 277–297 — published.
- Lee, "Training, Wages, and Sample Selection: Estimating Sharp Bounds on
  Treatment Effects," *Review of Economic Studies* 76(3) (2009), 1071–1102 —
  published.
- Griliches & Hausman, "Errors in Variables in Panel Data," *Journal of
  Econometrics* 31 (1986), 93–118 — published. (Volume 31, not 32.)

Verification status: **source-audited 2026-09-22**. Interior claims carry
section numbers; page ranges are the printed folios above.

Use in this battery: `panel-diagnostics` (FE-margin adjudication, Pesaran CD
routing, attenuation inversion, attrition bounds) and the design-matrix
panel records.

## 1. Dependence has a geometry — match the SE to it

Clustering on one dimension is a claim that the other dimensions are clean.
Audit the geometry before accepting the SE:

- **Multiway/non-nested clustering** (CGM §§2–3): when errors correlate
  within two or more non-nested dimensions (e.g. state and year, or firm and
  industry-year), the variance estimator is the inclusion–exclusion sum of
  the one-way cluster variances (V1 + V2 − V12 for two-way). Nested
  dimensions reduce to clustering at the highest level only (p. 239).
  Inference is governed by the *smallest* number of clusters along any
  dimension — a state×year panel with 8 years is an 8-cluster problem on
  the time dimension regardless of N. Route few-effective-cluster cases to
  `mackinnon_nielsen_webb_2023_few_clusters.md`.
- **Driscoll–Kraay** (pp. 549–551): a nonparametric covariance estimator
  consistent under arbitrary cross-sectional dependence as T → ∞,
  regardless of N — it applies a kernel to cross-sectional sums, so it
  needs a long *time* dimension, not a long cross-section. Contrast:
  parametric spatial corrections require a known distance metric and N→∞;
  D-K requires neither. For panels with T ≥ ~20–30 and common shocks,
  D-K is the cheap robust alternative when full CCE is not run.

## 2. Cross-sectional dependence: test it, then treat it

- **Pesaran CD** (EE 2021, §§2–3): the CD test averages pairwise residual
  correlations and is N(0,1) under cross-sectional independence for fixed
  T, N large. Caveat: the plain CD test loses power when correlations are
  weak or pattern-structured (e.g. spatially decaying) — the CD(p) variants
  exploit spatial/dependence patterns when they are the relevant
  alternative (p. 15). Report CD beside the SE choice, not instead of it.
- **If dependence biases the coefficient, not just the SE** — i.e.
  unobserved common factors correlated with the regressors — SE fixes do
  not reach it. Two audited routes:
  - **Pesaran CCE** (Econometrica 2006, abstract/§2): augment the
    regression with cross-sectional averages of the dependent and
    individual-specific regressors; these proxy the unobserved factors and
    asymptotically (N→∞) eliminate the differential factor loadings. Mean
    group and pooled variants; computable by OLS on the augmented
    regression.
  - **Bai interactive FE** (Econometrica 2009, §§2–5): model the error as
    λ_i′F_t — loadings × factors — and estimate factors and loadings
    jointly with β. Large-N, large-T asymptotics (abstract; fixed-T
    factor models need other methods). Accommodates additive FEs plus
    interactive terms, a bias-corrected estimator, and a Hausman-type test of
    additive vs interactive structure (pp. 1230–1231). Use when the
    factor structure is itself the object (or CCE's proxy is inadequate
    for the heterogeneity claimed).

## 3. Which margin does the claim need? — Mundlak 1978

The within/between distinction is not a preference, it is the estimand:

- Mundlak's core result (pp. 71–74): the RE/GLS estimator is a matrix
  combination of the within and between estimators — and *any* such
  combination is biased for the slopes when the individual effects
  correlate with the regressors. Under correlated effects "there is only
  one estimator" — the within estimate (p. 71).
- The Mundlak device: model E[α_i | x̄_i] = x̄_i′γ and add the group means —
  the RE regression then reproduces the within estimator for the
  time-varying slopes while separately identifying the between component.
  This is the cheapest available margin-decomposition: report within,
  between, and the contrast. If between ≠ within and the claim needs the
  between (cross-unit) margin, the burden is on the effects–regressors
  orthogonality claim, not on "we used RE because it was significant."

## 4. Dynamics — Nickell bias and Arellano–Bond

- **Nickell 1981** (abstract, p. 1417): the within-group estimator in a
  dynamic model (lagged dependent variable) with fixed effects is
  inconsistent as N→∞ when T is fixed — the Nickell bias is O(1/T),
  downward on the persistence coefficient. A within estimate of ρ on a
  T=10 panel carries a material downward bias regardless of N.
- **Arellano–Bond 1991** (§§2–3, pp. 277–280): difference the equation to
  remove the FE, then instrument the differenced lagged dependent variable
  with lagged *levels* (valid under no serial correlation in the
  levels errors). Diagnostics that must accompany any AB/diff-GMM claim:
  - **m1/m2 tests** — first-differenced residuals should show m(1)
    (mechanical) but no m(2); significant m(2) invalidates the
    instrument set.
  - **Sargan/Hansen overid** on the instrument count.
  - Instrument proliferation: the instrument count grows quadratically
    in T — collapsed/restricted instrument matrices are not optional
    polish, they are what keeps the overid test honest.
- Modern caveats worth flagging: lagged levels are weak instruments for
  the difference when ρ is near 1 (Blundell–Bond system-GMM is the fix,
  at the price of a stronger initial-conditions assumption) — check that
  a system-GMM result isn't resting on the very persistence it reports.

## 5. Measurement error is amplified by the transformation — G-H 1986

Griliches–Hausman (pp. 93–97): with i.i.d. measurement error in the
regressor, within and first-difference estimators attenuate *more* than
levels OLS — differencing lowers the signal-to-noise ratio when the true
regressor is persistent and the error is transitory. The attenuation
inversion: the estimator that "solves" the FE problem worsens the EIV
problem, and first differences are typically the worst offender. Review
rule: when a within/FD estimate is "surprisingly small," test the EIV
account (known attenuation factor under i.i.d. error vs the true regressor
serial correlation) before accepting an economic null — and before
accepting the paper's claim that within is the "clean" margin.

## 6. Attrition and selection — Lee 2009 bounds

Outcome-correlated attrition is a selection problem, not an inference
problem. Lee's trimming procedure (ReStud 2009, §§2–3): with a randomly
(or as-if randomly) assigned binary treatment (Assumption 1,
independence) and monotone selection (treatment only weakly increases
observed-outcome probability — no exclusion restriction, no bounded
support needed), bound the effect for the always-observed subpopulation
— not the population ATE — by trimming the over-selected share of the
treated group's outcome distribution at the quantiles that equalise the
observed-sample shares. Review use: when a panel's observed outcome
conditions on selection (employment for wages, survival for outcomes)
and the treatment meets those conditions, report Lee bounds beside the
point estimate; otherwise reweight (IPW) where feasible. A "balanced
subsample" restriction silently assumes the attrition was random.

## 7. Reviewer checklist

- Dependence geometry named before the SE: which dimensions cluster, are
  they nested or non-nested (CGM), and does the *smallest* dimension's
  cluster count survive the few-cluster crib?
- Pesaran CD reported for the residual; weak-pattern alternatives run as
  CD(p) where spatial decay is the relevant alternative.
- If factors correlate with regressors: CCE or Bai interactive FE beside
  the FE estimate — SE-only fixes don't reach coefficient bias.
- Margin adjudication: within/between contrast reported (Mundlak device);
  claims needing the between margin carry the orthogonality burden.
- Margin-switch tell: sibling specifications that differ in FE/differencing
  identify different margins — a "levels" spec without unit FEs identified
  off the permanent/between component is not a robustness check of the
  within estimate, and a coefficient that moves across that switch is
  answering a different question. When a paper quietly moves margins
  between headline and appendix, name the margin each spec draws on.
- Dynamic panels: Nickell O(1/T) bias acknowledged; AB output carries
  m1/m2 + Sargan + instrument count; system-GMM flagged when ρ is near 1.
- "Within/FD estimate is small" triggers the G-H attenuation check, not
  an economic null.
- Outcome-correlated attrition → Lee bounds beside the estimate.

## Continuous treatment with no stayers

de Chaisemartin, D'Haultfœuille & Vazquez-Bare, "Difference-in-Difference
Estimators with Continuous Treatments and No Stayers," *AEA Papers and
Proceedings* 114 (2024): 610–613 (published). When no unit's treatment is
unchanged between periods (weather, prices), the target is a weighted
average of slopes (the WAOSS of de Chaisemartin et al. 2023), identified as
the limit of a DiD between all units and quasi-stayers (Thm 1; assumptions:
static model, parallel trends conditional on period-one treatment, bounded
Lipschitz potential outcomes, quasi-stayers exist). Nonparametric
estimation converges at n^(2/5); placebos must restrict to earlier-period
quasi-stayers and may converge slower still. A parametric two-step GMM
estimator is √n. Application, Deschênes–Greenstone 1997–2002 degree days:
TWFE −0.024 (0.007) vs −0.018 (0.011).
