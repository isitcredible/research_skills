# Boundary (geographic) discontinuity designs — Cattaneo, Titiunik & Yu (2026); Keele & Titiunik (2015); Cattaneo, Idrobo & Titiunik (2024)

Sources and versions audited (all source PDFs not distributed with the skill):

- **CTY-JoE** — Cattaneo, M. D., Titiunik, R. & Yu, R. R., "Estimation and
  inference in boundary discontinuity designs: Distance-based methods,"
  *Journal of Econometrics* 256 (2026), article 106266 (pp. 1–26) —
  **published** (`Cattaneo_Titiunik_Yu_2026_BDD_DistanceBased_JoE.pdf`).
  Cited by journal page.
- **CTY-Loc** — Cattaneo, Titiunik & Yu, "Estimation and inference in
  boundary discontinuity designs: Location-based methods," manuscript dated
  13 May 2026, to appear in *JASA* — **working paper; verify against the
  published version before quoting**
  (`Cattaneo_Titiunik_Yu_2026_BDD_LocationBased_JASA_wp.pdf`). Cited by
  manuscript page and section.
- **CTY-WC** — Cattaneo, Titiunik & Yu, "Boundary discontinuity designs:
  Theory and practice," manuscript dated 2 February 2026, chapter for
  *Advances in Economics and Econometrics: Thirteenth World Congress* (CUP)
  — **working paper; verify before quoting**
  (`Cattaneo_Titiunik_Yu_2026_BDD_TheoryPractice_ESWC_wp.pdf`). Cited by
  manuscript page.
- **rd2d-SW** — Cattaneo, Titiunik & Yu, "rd2d: Causal inference in boundary
  discontinuity designs," software article dated 28 May 2026 — **working
  paper; verify function arguments against the installed package help**
  (`Cattaneo_Titiunik_Yu_2026_rd2d_software_wp.pdf`). Cited by page.
- **KT** — Keele, L. J. & Titiunik, R., "Geographic boundaries as regression
  discontinuities," *Political Analysis* 23(1) (2015), 127–155 —
  **published** (`Keele_Titiunik_2015_GeographicBoundariesRD_PA.pdf`).
- **CIT** — Cattaneo, M. D., Idrobo, N. & Titiunik, R., *A Practical
  Introduction to Regression Discontinuity Designs: Extensions*, Cambridge
  Elements (CUP, 2024), §5.2 "Multi-Score RD Design," pp. 90–105 —
  **published**
  (`Cattaneo_Idrobo_Titiunik_2024_PracticalRD_Extensions_CUP.pdf`).

The formal pooling-based paper (Cattaneo, Titiunik & Yu, "pooling-based
methods," cited as 2026c / [22]) was not available; everything said here
about pooled nearest-distance estimators comes from CTY-WC's summary of it
and is marked as such.

Verification status: **source-audited 2026-10-15** for CTY-JoE, KT and CIT;
**WP-audited 2026-10-15** for CTY-Loc, CTY-WC and rd2d-SW.

Use in this battery: `rdd-diagnostics` conditional checks
*Boundary-discontinuity designs* and *Spatial dependence*; the
design-matrix RD checklist and boundary-discontinuity record; the `rd2d`
block of the software examples. It also bears on any design-validity lead
about sorting or compound treatment at a border.

## 1. Estimands

- **BATEC** (boundary average treatment effect curve): τ(x) = E[Y(1) − Y(0)
  | X = x] for each point x on the boundary B, X the bivariate score
  (CTY-JoE p. 2; CTY-Loc p. 1; rd2d-SW p. 5). KT call it the geographic
  treatment effect curve and show it is identified, point by point, under
  two-dimensional continuity of the potential-outcome regressions (KT pp.
  131, Assumption 1 and Proposition 1). The design identifies a curve, not a
  number (KT p. 131).
- **WBATE**: ∫ τ(x) w(x) dx / ∫ w(x) dx along B, w a user-chosen bounded
  positive weight (CTY-Loc §4, pp. 14–15; CTY-JoE p. 12–14). With w = f_X
  (the score density on B) the WBATE is the density-weighted **BATE**
  (CTY-Loc p. 9; KT p. 132). Equal weights on a grid give the simple average
  of the grid-point estimates (rd2d-SW p. 6); that equals arc-length
  weighting only if the grid is equally spaced in arc length (inference from
  the quadrature formula, CTY-Loc p. 14). The authors also allow data-based
  weights ω_j w(b_j) = N_j / Σ N_l, N_j the count of observations within h
  of b_j (CTY-Loc p. 14). A WBATE over a trimmed subset of B is a different
  estimand, defined on that subset (CTY-Loc p. 14; rd2d-SW p. 15).
- **LBATE**: sup over B of τ(x), the largest boundary effect; the smallest
  is handled by applying it to −τ (CTY-Loc §5, p. 16). rd2d-SW (p. 13) says
  it should be reported together with the full BATEC and the WBATE.
- **Pooled nearest-distance estimand.** A pooled RD on D_i = signed distance
  to the *closest* boundary point converges, under regularity conditions on
  B and the distance function, to the density-weighted BATE (CTY-WC pp.
  25–26, derived for the local difference in means, spec. (1); the other,
  more flexible specifications "enjoy similar properties," p. 25). CTY-JoE
  (p. 25) states the same classification: pooling-based methods identify a
  scalar parameter corresponding to a WBATE. The pooled estimator therefore
  averages a heterogeneous curve with density weights; it does not assume a
  constant effect, but it cannot reveal heterogeneity (CTY-WC p. 29; CIT p.
  95). KT (p. 137) show a naive pooled design cannot recover τ(b) at any
  point unless effects are constant along B.
- **Fuzzy versions** (fuzzy BATEC = ITT curve / first-stage curve; fuzzy
  WBATE, fuzzy LBATE) are Wald-ratio estimands; a complier interpretation
  needs local exclusion, monotonicity and a nonzero first stage (rd2d-SW p.
  7; CTY-Loc §6).

## 2. Two identification routes, one target

- **Location-based**: local polynomial in the bivariate score X_i − x,
  fitted separately on each side, at each boundary point (CTY-Loc eq. (1),
  p. 8; CTY-WC spec. (11), p. 34). Identification is the bivariate
  continuity argument (CTY-Loc p. 7).
- **Distance-based**: for each boundary point x, a univariate RD on the
  signed distance D_i(x) = ±d(X_i, x) to *that point*, cutoff 0, treated
  side non-negative (CTY-JoE p. 2; rd2d-SW p. 19). The induced regression
  θ_t,x(r) averages potential outcomes over level sets of the distance
  function, so its limit need not equal μ_t(x) in general; CTY-JoE Theorem 1
  (p. 5) gives sufficient conditions (rectifiable B, distance metric
  equivalent to Euclidean, regularity) under which the distance-based
  estimand equals τ(x). KT Appendix D (p. 151) and CIT (p. 94) state the
  same route informally.
- Both routes target the **same** BATEC and functionals of it (CTY-JoE p.
  25; rd2d-SW pp. 20–22: under the distance-based identification conditions
  the distance-based WBATE and LBATE are plug-in estimators of the same
  τ_WBATE and τ_LBATE). The difference is estimator bias and efficiency, not
  the causal target. Inference: a location-vs-distance gap is a diagnostic
  of geometry-induced bias or weak support, not a second estimand.
- The pooled nearest-distance RD is a third reduction that discards location
  along the border: "Pooling-based methods discard location information"
  (CTY-JoE p. 2). CTY-JoE's results do **not** cover it (pp. 2, 5).

## 3. The failure mode CTY-JoE diagnoses: kink bias in distance-based estimators

- **Mechanism.** Near a kink or corner of B, for small r the circle {u :
  d(u, x) = r} on the treated side is a complete arc, but beyond some r it
  is truncated by the boundary, so r ↦ θ_t,x(r) is continuous but not
  differentiable there (Fig. 1, p. 7). The induced univariate regression is
  then at best Lipschitz, however smooth μ_0, μ_1 are (pp. 3, 6).
- **Theorem 2 (p. 6).** Uniformly over B and over a class of data-generating
  processes, the misspecification bias of the p-th order distance-based
  estimator is of order exactly h — bounded above and below — for any p ≥ 0.
  The lower bound is attained with an L-shaped boundary with a 90° kink (p.
  7). For any sample size there is a neighbourhood of a kink where the bias
  is at best order h (p. 7).
- **Theorem 3 (p. 7).** If B is locally (or globally) C^(κ+2), the bias
  improves to h^min(κ, p+1) pointwise (or uniformly). A single kink in an
  otherwise smooth boundary destroys the uniform rate (p. 7).
- **Consequences for practice.** Robust bias correction with order p+1
  assumes bias of order h^(p+1); near kinks raising p does not shrink the
  bias, so RBC is ineffective uniformly over B and undersmoothing relative
  to the p = 0 MSE bandwidth is needed (pp. 6, 9–10). The local MSE-optimal
  bandwidth near a kink is of order n^(−1/4); the authors offer a global
  rule h = C·n^(−1/4) (conservative, never larger than the pointwise
  MSE-optimal one) and a kink-adaptive bandwidth when kink locations are
  known (p. 9). Theorem 6 (p. 10): over rectifiable boundaries no isotropic
  (distance-only) estimator beats the uniform rate n^(−1/4), whatever the
  smoothness of μ. Geographic borders are where this bites; the paper cites
  the fractal-coastline debate (p. 3), and CTY-WC (p. 7) notes geographic
  borders are at best piecewise linear with kinks.
- **Variance and bandwidth.** The distance-based estimator's variance is of
  bivariate order (nh²)^(−1) despite the univariate regression (p. 8).
  Treating D_i(x) as an intrinsically univariate score and using a
  univariate MSE selector (rdrobust) gives h ≍ n^(−1/(3+2p)), smaller than
  the correct n^(−1/(4+2p)): undersmoothing, higher variance, conservative
  inference (p. 9; CIT p. 93 states the same).
- **Simulation (pp. 11–12).** Ignoring the kink produced visibly larger bias
  in point estimates near it, but coverage stayed near nominal because the
  signal-to-noise ratio was modest; the authors warn stronger signals could
  distort inference.
- **Recommended responses (p. 25):** prefer location-based methods when the
  bivariate score is reliable; otherwise account for geometry — restrict to
  locally smooth segments or use proximity-adaptive bandwidths — and report
  that these choices can change the estimand. Uniform inference for
  distance-based methods additionally needs the boundary not to be locally
  too long or highly oscillatory within an h-ball (Theorem 5(ii), p. 9).
- **Location-based contrast.** Location-based bias is of order h^(p+1)
  because smoothing is in the plane; this matters when B has corners
  (CTY-Loc p. 10; CTY-WC p. 34). Scope condition: CTY-Loc's main theorems
  assume a piecewise-linear boundary with finitely many segments, which "may
  be restrictive in geographic" settings; irregular boundaries are covered
  in the supplement under geometric conditions not reproduced in the main
  text (CTY-Loc pp. 8, 26–28).

## 4. Pooled distance-to-border RD with segment fixed effects

- **Prevalence.** Of 82 published BD papers reviewed, 76 (about 93%) pool on
  nearest distance and report one average (CTY-WC p. 10).
- **Taxonomy (CTY-WC pp. 14–21).** With T_i the treatment indicator, D_i
  nearest signed distance, ι_L(S_i) boundary-segment fixed effects
  (indicator of the closest of L segments) and localization |D_i| ≤ h: (1)
  difference in means; (2) (1) + segment FE (Black 1999); (3) segment FE +
  polynomial in latitude/longitude, no treatment interaction (Dell 2010;
  "has become a common strategy," p. 18); (4) polynomial in D_i, no
  interaction; (5) (4) + segment FE; (6) segment FE + r_p(D_i) +
  T_i·r_p(D_i); (7) segment FE + r_p(X_i) + T_i·r_p(X_i); (8)
  segment-specific RDs (T_i interacted with segment indicators). Spec. (10)
  is the per-point distance RD; (11) the location-based fit.
- **What is wrong with the common versions.** Specs (1)–(5) omit the
  interaction that lets the control and treated fits differ, which the
  authors say potentially introduces larger misspecification bias (p. 19).
  Under a continuity interpretation the local constant of (1)–(2) controls
  bias poorly (p. 16). The literature's three limitations: missing
  interactions, ad-hoc bandwidths, and conventional inference at large
  bandwidths that over-rejects (p. 37). Recommendation: specs (6) or (7), an
  MSE-optimal bandwidth, and robust bias-corrected inference (p. 37);
  standard rdrobust can be used for the pooled analysis provided "the
  regularity conditions are satisfied" (p. 28).
- **Pooled bias and variance (CTY-WC pp. 26–27, summarizing the pooling
  paper).** Bias is O(h) in general without further restrictions on B; with
  the interacted spec. (6) and additional regularity it may improve to
  O(h^(p+1)). Variance is of one-dimensional order (nh)^(−1). So the order-h
  phenomenon has a pooled analogue at the level of a general guarantee, but
  the source does not tie it to kinks specifically and does not analyse
  segment FE separately.
- **What segment FE do and do not do.** No source shows that segment FE
  remove geometry-induced bias, restore location information, or make an
  unlocalized comparison into an RD; localization by |D_i| ≤ h and the
  interacted polynomial are what the chapter's recommendation turns on. KT
  (p. 132) note Dell's segment FE capture heterogeneity only coarsely and
  that point-specific effects can be integrated to any segment. *Inference,
  not in the sources:* in an OLS fit with segment FE and a common T
  coefficient, the coefficient is a variance-weighted combination of
  within-segment contrasts, so its implicit weights need not be the density
  weights of the BATE; the source derives the BATE limit only for spec. (1).
- **Contiguous-pair comparisons.** CTY-WC (p. 5) treats Card–Krueger as an
  "ancestor" of the BD design because it did not use distance to the
  boundary; it lists Dube et al. (2010), with county adjacency as the
  distance notion, as a BD design of type (1)/(2) (p. 39). A contiguous-pair
  design is therefore a pooled local-constant comparison with a fixed,
  non-shrinking localization, whose credibility rests on a
  local-randomization reading inside the pair (inference from pp. 14–16).
- **Coarse coordinates.** When the score is a district centroid shared by
  many individuals (Dell 2010), the score has mass points and the
  continuous-score theory does not apply directly (CTY-WC p. 22; KT p. 132:
  with cluster-level coordinates individual assignment is not a
  deterministic function of an individual score).

## 5. Inference: pointwise intervals, uniform bands, aggregates

- **Pointwise**: Wald interval with normal quantile, valid under a
  small-bias condition; MSE-optimal bandwidths violate it, hence RBC (p then
  p+1 at the same bandwidth) (CTY-Loc pp. 12–14; rd2d-SW p. 12). RBC
  intervals are generally not centred on the point estimate (rd2d-SW p. 12).
- **Uniform bands**: the t-process is not asymptotically tight, so bands use
  a Gaussian approximation to the supremum, simulated on the grid with the
  estimated cross-point covariance, regularized if not positive definite
  (CTY-Loc pp. 12–14; CTY-JoE pp. 8–10). Uniform validity needs stronger
  rate conditions than pointwise (CTY-Loc Theorem 3(ii)).
- **Reusing observations** across nearby points makes point estimates
  correlated (CIT p. 95); KT used a fixed 1.1 km bandwidth against 1.15 km
  point spacing to limit reuse (KT p. 146); CIT (p. 104) give half the
  spacing (0.575 km) as the bandwidth that uses each observation at only one
  point. KT (pp. 139–140) flag multiple testing across grid points. Uniform
  bands are the design-consistent answer to both (inference linking the two
  sources).
- **WBATE**: variance of order (nh)^(−1), faster than the pointwise
  (nh²)^(−1), because only points within O(h) of each other covary (CTY-Loc
  p. 15; rd2d-SW p. 13). Its standard error is the double integral of the
  BATEC covariance kernel, not a function of the pointwise SEs alone
  (rd2d-SW p. 13). The MSE-optimal WBATE bandwidth has exponent 1/(2p+3),
  not the pointwise 1/(2p+4) (CTY-Loc p. 15).
- **LBATE**: interval obtained by projecting the uniform band; conservative
  (CTY-Loc Theorem 6, p. 16; rd2d-SW p. 14).
- **Dependence**: all formal results assume i.i.d. sampling, which "may be
  restrictive in some geographic applications" (CTY-Loc p. 7). Cluster- or
  spatially-robust variance estimators can be paired with the estimators "in
  principle"; the authors list "dependence-robust pointwise and uniform
  inference for BD designs" as future work (CTY-Loc §8.5, p. 29). KT (p.
  128) require that inference account for possible spatial correlation and
  (Appendix B, p. 150) note the assignment level may be the area, not the
  individual, in which case there are two observations.

## 6. Design threats specific to geography (KT)

- **Compound treatments** (KT pp. 133–136): administrative borders often
  coincide (counties, school districts, legislative districts, media
  markets), so the border shifts several treatments at once. Identifying one
  requires **Compound Treatment Irrelevance** (Assumption 2, p. 133), an
  exclusion-type restriction (fn. 8, p. 136). Remedies: restrict to segments
  where the other units are constant on both sides (pp. 143–144, which also
  conditions on distance), argue irrelevance with pre-period placebo
  outcomes (p. 149), or redefine the estimand as the compound effect (p.
  135). The ideal segment can lack data near the border (Lake Tahoe example,
  p. 135).
- **Sorting.** "The biggest challenge is that often agents are able to sort
  very precisely around the boundary" (p. 149); compound treatments increase
  the reasons to sort (p. 149). Falsification: estimate the BATEC on
  predetermined covariates at each boundary point and map it (pp. 140, 149);
  spatial nearest-neighbour balance can differ from naive-distance balance
  (pp. 140, 145–146). A lagged outcome affected by earlier treatment is not
  predetermined (past turnout, p. 142). CTY-Loc's application runs the
  covariate placebo with its own bandwidths and reports a covariate WBATE
  and LBATE (Table 1(d), p. 27).
- **Naive distance.** "this naive distance does not account for distance
  along the border" (p. 137): units at the same perpendicular distance can
  be far apart, so pooled balance tests can mask local imbalance (pp. 137,
  140).
- **Data density.** Positive score density near B is assumed and "can be
  restrictive in geographic contexts" (p. 131); check the distribution of
  distances, which may not reach zero (CIT p. 103); thin segments mean
  extrapolation (CIT pp. 94–95).
- **Distance metric.** Euclidean distance on raw latitude/longitude
  overstates distances; use geodetic or chordal (KT fn. 15, p. 142; CIT p.
  94). `rdms` computes Euclidean distance on its raw inputs, which changed a
  point estimate from −0.002 to 0.034 in the KT data (CIT p. 104).
- **Interference** across a residential border is possible; KT suggest
  dropping nearly adjacent units as a check (Appendix A, pp. 149–150).

## 7. Software: rd2d (R; Python and Stata mirror it)

From rd2d-SW; check the installed help for anything not listed here.

- **Commands**: `rd2d()` / `rdbw2d()` (location), `rd2d.distance()` /
  `rdbw2d.distance()` (distance) in R; `rd2d`, `rd2d_dist` in Python and
  Stata (pp. 3, 28–30).
- **Location fit**: `rd2d(Y = Y, X = X, assignment = T, b = b, params.cov =
  "main")`, `b` a J×2 grid (pp. 6, 10). `params.cov = "main"` stores the
  cross-boundary covariance needed for uniform bands and aggregates (pp. 5,
  10). Fuzzy: `fuzzy = W` with `params.cov = c("main", "itt", "fs")`;
  `output = "itt"`, `"fs"`, `"main"` (main = fuzzy ratio); `bwparam =
  "main"` or `"itt"` (pp. 7–8).
- **Summaries**: `summary(fit, output = "main", cbands = "main", WBATE = w,
  LBATE = TRUE)`, with `w <- rep(1, nrow(b))` in every example (pp. 6,
  13–14). Every source example passes `output` explicitly; the default is
  not stated. Bands and aggregate rows are appended to the per-point table
  only when requested and only if the covariance was stored (pp. 6, 10).
  Column and list-element names of the returned object are not documented in
  the article.
- **Distance fit**: `rd2d.distance(Y = Y, distance = D, b = b, ...)`, D an
  n×J signed-distance matrix, one column per grid point, non-negative on the
  treated side (pp. 19–20); there is no `assignment` argument in the
  examples. One example stores bands with `cbands = TRUE` at fit time (p.
  20), others with `params.cov` (pp. 23–24). Scalar `h`, or a J×2 matrix of
  control/treated bandwidths (p. 23).
- **Defaults**: triangular product kernel, p = 1, q = 2, `vce = "hc1"`,
  `fitmethod = "joint"`, `masspoints = "check"`, `level = 95`, `bwselect =
  "mserd"`, `method = "dpi"`, `stdvars = TRUE` (p. 11; distance analogue p.
  23). Selectors: `mserd`, `cerrd`, `imserd`, `icerrd`, `msetwo`, `certwo`,
  `imsetwo`, `icertwo` (p. 10). `bwcheck` default 50 + p + 1 in `rd2d()` and
  `rd2d.distance()`, 20 in standalone `rdbw2d()`; `scaleregul` 3 via
  `rd2d()`, 1 in `rdbw2d()` and `rd2d.distance()` (pp. 16, 23). `repp =
  1000` Gaussian draws in summary methods (p. 17).
- **Bandwidth reporting**: up to four bandwidths `h01`, `h02` (control side,
  coordinates 1, 2) and `h11`, `h12` (treated side) (p. 10). Uniform bands
  and aggregates must use the same bandwidths as the covariance (p. 16). The
  article does not document the format of a user-supplied `h` for `rd2d()`.
- **Clustering**: `cluster = id`; `fitmethod = "joint"` adds both sides'
  influence contributions within a cluster that straddles the border;
  `"separate"` is the older convention and can give different SEs and
  bandwidths (p. 11).
- **Covariates**: `covs.eff = Z`, common coefficients across sides, carried
  into bandwidths, bands and aggregates; meant not to change the estimand
  (pp. 18–19). Using covariates as outcomes for falsification is a separate
  task (p. 19).
- **Kinks (distance only)**: the default treats B as locally smooth and uses
  RBC with q = p + 1; `kink.unknown` shrinks bandwidths to
  unknown-irregularity rates and sets q = p; `kink.position` (logical vector
  or grid indices) adapts bandwidths to known kinks (p. 24). CTY-JoE (p. 10)
  describes the n^(−1/4) rule as the package default when smoothness is
  unknown; the two descriptions differ, so check which setting a paper used
  and the installed help.
- **Grid**: for a piecewise-linear boundary, place points about equally
  spaced in arc length and force kinks, corners and key locations into the
  grid; refine the grid and check that the critical value, band and
  aggregates are stable; trimming endpoints or thin corners redefines the
  target set (p. 15).
- **Reporting list** (p. 17): target set, grid, selector, fitting
  convention, clustering, covariate adjustment, covariance-regularization
  warnings, simulation count; inspect the first-stage curve before the fuzzy
  ratio (p. 17).

## Review use

1. **Classify the border design first.** Map the paper's regression onto
   CTY-WC specs (1)–(11). Record: score (perpendicular distance, per-point
   distance, coordinates, adjacency), localization rule and bandwidth
   source, whether T is interacted with the polynomial, segment FE,
   inference (conventional vs RBC). Specs (1)–(5) at an ad-hoc or MSE-sized
   bandwidth with conventional SEs carry all three limitations of CTY-WC p.
   37; record each as a finding.
2. **Re-estimate the pooled number properly** where data allow: rdrobust on
   the signed nearest distance (separate fits each side, MSE-optimal h,
   RBC). A result that exists only in a non-interacted spec is fragile.
3. **Set the paper's pooled estimate against a density-weighted WBATE.** The
   pooled estimand is the density-weighted BATE; equal grid weights target a
   different average unless density is flat along the border. Report
   equal-weight and density-type (N_j-based) WBATEs; a gap between them is a
   heterogeneity-by-density finding, not a contradiction.
4. **Report the BATEC with uniform bands.** Any claim about where along the
   border the effect is present, absent, larger or smaller, or that it is
   positive everywhere, needs the uniform band; counting
   pointwise-significant grid points is not evidence of it. LBATE intervals
   are conservative.
5. **Kinks.** List the boundary's kinks and corners. For any distance-based
   estimate (the paper's own per-point distance RDs, or rd2d.distance) at
   points within a bandwidth of a kink, treat point estimates as possibly
   order-h biased whatever the polynomial order; rerun with `kink.position`
   or `kink.unknown` and with location-based `rd2d`. A conclusion that rests
   on distance-based estimates near kinks and moves under location-based
   estimation is not robust.
6. **Compound treatment.** Overlay other administrative borders on the
   treatment border. Where they coincide, the estimate is a compound effect
   unless the paper isolates segments or defends irrelevance; an unaddressed
   overlap moves the claim from an effect of T to an effect of crossing this
   border.
7. **Sorting and balance.** Demand covariate BATECs (with uniform bands and
   a covariate WBATE) along the border, not one pooled balance table. Lagged
   outcomes influenced by earlier treatment do not count as predetermined.
8. **Support and metric.** Check side-specific effective N at each grid
   point, the minimum distances, and whether coordinates were projected or
   distances computed as chordal/geodetic. Thin segments or coordinates
   shared within districts (mass points) limit what the continuity estimate
   can claim.
9. **Dependence.** Rerun with clustering at the paper's level using
   `fitmethod = "joint"`, and say that no source provides spatially robust
   uniform bands; for the paper's own pooled regression, the battery's
   spatial record applies to that regression.
10. **Costs.** A pooled border effect with missing interactions,
    conventional inference at a wide bandwidth, unaddressed compound
    treatment, or a uniform band that includes zero across most of the
    border is downgraded from an effect at the border to an average contrast
    near the border, with the specific failure named.
