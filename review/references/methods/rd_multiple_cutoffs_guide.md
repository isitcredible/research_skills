# RD with multiple cutoffs, multiple scores, and extrapolation — Cattaneo, Keele, Titiunik & Vazquez-Bare (2016, 2021); Cattaneo, Titiunik & Vazquez-Bare (2020); Cattaneo, Idrobo & Titiunik (2024)

Sources, all published versions: (1) Matias D. Cattaneo, Luke Keele, Rocío
Titiunik and Gonzalo Vazquez-Bare, "Interpreting Regression Discontinuity
Designs with Multiple Cutoffs," *Journal of Politics* 78(4) (2016): 1229–1248
(hereafter CKTV16). The audited PDF is the publisher's online-first version
(published online 17 May 2016) and prints placeholder page numbers ("000"), so
it is cited by PDF page; the issue range 1229–1248 is taken from the later
papers' reference lists. The online appendix (sections S1–S5) was not audited.
(2) Same authors, "Extrapolating Treatment Effects in Multi-Cutoff Regression
Discontinuity Designs," *Journal of the American Statistical Association*
116(536) (2021): 1941–1952 (CKTV21); supplemental appendix not audited.
(3) Cattaneo, Titiunik and Vazquez-Bare, "Analysis of Regression-Discontinuity
Designs with Multiple Cutoffs or Multiple Scores," *Stata Journal* 20(4)
(2020): 866–891 (CTV20, the `rdmulti` article). (4) Cattaneo, Nicolás Idrobo
and Titiunik, *A Practical Introduction to Regression Discontinuity Designs:
Extensions*, Cambridge Elements in Quantitative and Computational Methods for
the Social Sciences (Cambridge University Press, 2024), §5 "Multi-Dimensional
RD Designs," pp. 77–105 (CIT24). Source PDFs (not distributed with the skill):
`Cattaneo_Keele_Titiunik_VazquezBare_2016_MultipleCutoffs_JOP.pdf`,
`Cattaneo_Keele_Titiunik_VazquezBare_2021_ExtrapolatingMultiCutoff_JASA.pdf`,
`Cattaneo_Titiunik_VazquezBare_2020_rdmulti_StataJ.pdf`,
`Cattaneo_Idrobo_Titiunik_2024_PracticalRD_Extensions_CUP.pdf`.

Verification status: source-audited 2026-10-15.

Use in this battery: the `rdd-diagnostics` conditional check "Multiple cutoffs
or scores"; the design-matrix RD conditional list; the `rdmulti` snippet in the
software examples; and the `claims` stage whenever a paper says anything about
RD effects for units away from the cutoff.

## 1. Three designs, and how to tell them apart

- **Noncumulative multiple cutoffs.** One score, one treatment, but different
  groups face different cutoffs (regions, years, schools). A unit with score x
  could have faced any cutoff; the cutoff variable C partitions the sample, so
  each unit faces exactly one cutoff (CTV20 pp. 867–868; CIT24 pp. 79–80).
  Close-election RDs with three or more candidates belong here: margin of
  victory is the vote share minus the strongest opponent's share, so the
  effective cutoff is the opponent's share and varies by race (CKTV16 PDF
  pp. 2–5, 11).
- **Cumulative multiple cutoffs.** One score, ordered cutoffs, a different dose
  of treatment in each score range; the cutoff a unit faces is a deterministic
  function of its score (CKTV16 PDF pp. 11–12; CIT24 p. 79). Example: Brazilian
  federal transfers stepping up at seven population thresholds (CKTV16 PDF
  p. 15).
- **Multiple scores.** Two or more running variables and an assignment rule
  over the plane; treatment changes along a boundary, the frontier shared by
  the treated and control areas (CIT24 p. 90). Hard thresholds on two exams
  and geographic borders are both cases (CIT24 pp. 90–91; CTV20 p. 870).

CIT24 lists three consequences of cumulative cutoffs (pp. 79–80): the treatment
usually differs across cutoffs, so an "overall effect" needs the treatment
redefined (for example, as receiving higher transfers of any amount); units facing different
cutoffs have systematically different scores, with no common support; and the
subpopulation "exposed to" a cutoff is ambiguous, because a unit between two
cutoffs is treated for the lower one and control for the upper one. CKTV16
calls classifying the design a crucial step (PDF p. 19).

## 2. The normalized-and-pooled estimand

Normalizing the score to X − C and running one RD at zero recovers, under
continuity of the regression functions and of the score density at every
cutoff (CKTV16 Assumptions 1–3, Lemma 1, PDF p. 8):

τ_P = Σ_c τ(c) ω(c), with τ(c) = E[Y(1) − Y(0) | X = c, C = c] and
ω(c) = f_{X|C}(c|c) P[C = c] / Σ_c' f_{X|C}(c'|c') P[C = c'] = P[C = c | X̃ = 0]
(CTV20 p. 869; CIT24 pp. 83–84).

- The weight on a cutoff rises with how common that cutoff is **and** with the
  density of the score at that cutoff among units facing it. It is therefore
  not the simple average of the cutoff-specific effects (CKTV16 PDF p. 8), and
  not a population-share average either. In CIT24's SPP example two areas of
  similar size get weights 0.384 and 0.534 because one has more students near
  its cutoff; the rural area gets 0.082 (p. 89).
- Each component is local twice over: at X = c and among units facing c.
  CKTV16 says the components "intensify the local nature of the effect"
  (PDF p. 8).
- **Fuzzy designs:** the pooled Wald ratio is again a weighted average of
  cutoff-specific complier effects, but each weight also carries the local
  complier share at that cutoff (CKTV16 Lemma 2, PDF p. 18). A cutoff with weak
  take-up contributes little to a pooled fuzzy estimate.
- **Finite samples:** the pooled estimate need not be a weighted average of the
  cutoff-specific estimates; it carries an extra term from the bandwidth and
  slope differences that vanishes asymptotically. In CKTV21 the pooled 0.125
  lies outside the two cutoff-specific estimates 0.137 and 0.169 (p. 1949,
  Table 1 p. 1943). The paper calls the explicitly weighted average (0.156) a
  proper weighted average and suggests it may give the more accurate
  assessment of the overall effect (p. 1949).
- **Power:** pooling aggregates sample sizes; in the transfers example the
  pooled 90% interval excludes zero while every cutoff-specific 95% and 90%
  interval includes it (CKTV16 PDF p. 16). Cutoff-specific intervals widen
  where the density near the cutoff is low (PDF p. 14).

When pooling is interpretable (CKTV16 recommendations for practice, PDF
p. 18): first tabulate or histogram the cutoff values among units near the
cutoff. If most mass sits at one cutoff, the design is close to a single-cutoff
RD. Otherwise the options are to report τ_P explicitly as the weighted average
it is, to assume constant effects, or to check robustness by dropping
subsets — a low-weight cutoff with an aberrant effect can make the pooled
number unrepresentative. The constant-effect route is labelled very strong
(PDF p. 9). The authors also suggest researchers may prefer weights chosen for
the application (PDF p. 19).

## 3. What the cutoff-specific effects can be read as

CKTV16 builds a ladder of assumptions (PDF pp. 9–11):

- With continuity alone, τ(c) is the effect at X = c for the units facing c.
- Constant effects within a cutoff (Proposition 1) or score ignorability
  (Assumption 4, Proposition 2) make τ(c) the effect for all units facing c,
  at any score — still only at the cutoff values in the support of C.
- **Cutoff ignorability** (Assumption 5) has two parts: (a) given the score,
  potential outcomes are mean independent of the cutoff faced; (b) the cutoff
  level does not affect potential outcomes directly (an exclusion restriction).
  Only under this do the cutoff-specific estimates trace a treatment-effect
  curve over the score (Proposition 3, PDF pp. 10–11). The authors call it
  generally strong (PDF p. 11).

Without cutoff ignorability, differences between τ(c1) and τ(c2) mix two
things: different score locations and different subpopulations. CKTV21 says the
cutoff-specific estimates "are not directly comparable" for that reason
(p. 1943). In the Brazil incumbency example, a negative effect near a 49%
opponent share may reflect different electoral environments rather than a
different effect of the PSDB's own vote share (CKTV16 PDF p. 15).

Under cumulative cutoffs, cutoff ignorability is untenable whenever the score
is related to potential outcomes, because units facing different cutoffs have
different scores by construction (CKTV16 PDF p. 12; CIT24 p. 80). Each
cutoff-specific effect is also an increment relative to the previous dose, not
an effect of "treatment" (CIT24 p. 82).

## 4. Estimating cutoff by cutoff

- Noncumulative: subset to units facing c and run a single-cutoff RD; a
  continuous cutoff (opponent vote share) is discretized into a grid or bins
  (CKTV16 PDF pp. 7, 13–14; CTV20 p. 868). CKTV16 uses the 600 treated and 600
  control observations nearest each grid value (PDF p. 14).
- Cumulative: restrict the sample around cutoff c_j to scores between the
  neighbouring cutoffs, or split at a midpoint or median between adjacent
  cutoffs (CKTV16 PDF pp. 13, 15; CIT24 p. 80). `rdms` without a range
  restriction uses observations that received the next dose as "treated"; CTV20
  warns that "This feature can result in inconsistent estimators" (p. 884) and
  supplies `range()` (p. 877).
- Adjacent cumulative estimates share observations and are not independent
  unless bandwidths are chosen not to overlap (CTV20 p. 870; CIT24 p. 83).
  Joint inference across cutoffs is possible by bootstrap or the joint
  asymptotic distribution (CKTV16 PDF p. 13).
- Falsification (density, covariates) is run per cutoff subsample with the
  one-dimensional tools (CIT24 p. 81); CTV20 notes `rddensity` and `rdlocrand`
  apply in these settings (pp. 867–868).

## 5. Multi-score designs

- The estimand is a curve τ(b) = E[Y(1) − Y(0) | X = b] over boundary points b
  (CTV20 p. 870; CIT24 p. 92). In practice it is estimated at a finite set of
  boundary points, which maps the problem into a multi-cutoff one (CIT24 p. 93).
- Location-specific effects: use the signed distance of each unit to the point
  b as a scalar score (CIT24 pp. 93–94). Two caveats (p. 93): near a kink or
  irregular stretch of boundary the collapsed score can carry large
  misspecification error, so inference is pointwise but not uniformly valid;
  and a one-dimensional MSE-optimal bandwidth on the distance is too small
  asymptotically, which costs efficiency.
- Choose boundary points where both treated and control observations are
  dense; sparse stretches mean excessive extrapolation (CIT24 pp. 94–95, 103).
  Reusing observations across points correlates the estimates (p. 95).
- Pooled effect: signed shortest distance to the boundary as the score (CIT24
  p. 95; `xnorm` in `rdms`, CTV20 p. 888). It cannot show heterogeneity along
  the boundary, and on a long boundary it can compare treated and control units
  that are close to the boundary but far from each other (CIT24 p. 95).
- `rdms` computes only Euclidean distance on the raw inputs. On latitude and
  longitude this gave 0.034 at a point where the chordal-distance estimate was
  −0.002 (CIT24 p. 104). Geographic designs need a chosen metric (geodetic,
  chordal, travel distance; p. 94) and bivariate methods from Cattaneo,
  Titiunik and Yu, which the book cites as in development (pp. 93, 105); the
  battery's boundary-discontinuity record governs those.

## 6. Extrapolation away from the cutoff (CKTV21)

Setup (pp. 1944–1946): two cutoffs l < h, groups indexed by the cutoff they
face. τ_l(x̄) = μ_{1,l}(x̄) − μ_{0,l}(x̄) for l < x̄ ≤ h is the effect, for the
**units facing the low cutoff**, at a score above l. μ_{1,l}(x̄) is observed;
μ_{0,l}(x̄) is not, because every unit facing l is treated above l. Units facing
h are untreated at x̄, but differ from the l group in observed and unobserved
ways (Definition 1, cutoff bias B(x) = μ_{0,l}(x) − μ_{0,h}(x)).

- **Identifying assumption** (Assumption 2, constant bias): B(l) = B(x) for
  all x in (l, h) — the control regression functions of the two groups are
  parallel over the extrapolation region, the RD analogue of parallel trends
  over the score (pp. 1944, 1946). Plus continuity of all μ_{d,c} on [l, h]
  (Assumption 1).
- **Result** (Theorem 1, p. 1947): τ_l(x̄) = μ_l(x̄) − [μ_h(x̄) + B(l)], with
  B(l) estimated at the low cutoff from the l group's controls just below l and
  the h group's controls at l.
- **Direction matters** (p. 1947): left-to-right extrapolation needs parallel
  control functions. Right-to-left needs parallel treated functions, which
  effectively imposes constant treatment effects across cutoffs.
- **Scope** (p. 1945): only the subpopulations defined by the cutoffs actually
  used; the method is stated not to be appropriate for other populations. The
  identified range is between the cutoffs.
- **Estimation** (p. 1947): four local-polynomial fits (local linear,
  triangular kernel, MSE-optimal bandwidths), RBC inference; the variance
  includes the covariance between μ̂_{0,h}(l) and μ̂_{0,h}(x̄) when their
  bandwidths overlap. The paper says implementation details are in its
  replication files; none of the audited sources names a packaged command for
  this estimator, and the `rdmulti` article documents none.
- **Testing** (§3.3, pp. 1947–1948): constant bias is not testable; the paper
  offers falsification only, noting that a "falsification test cannot
  demonstrate that an assumption holds". Two tests, both on units with X < l
  where both groups are controls: (i) a global polynomial regression with
  group interactions, H0 that the group-by-score interaction terms are zero
  (the two control functions differ only by a vertical shift); (ii)
  nonparametric equality of the first derivatives of the two control functions
  over a grid of points below l, pointwise or by a supremum statistic.
- **Application** (pp. 1943, 1948–1949): ACCES loan eligibility in Colombia,
  l = −850 (years 2000–2008) and h = −571 (2009–2010). Global test F p = 0.919
  (N = 257); derivative test p = 0.988. At x̄ = −650 the naive difference is
  0.050, the estimated bias −0.142, the extrapolated effect 0.191, RBC CI
  [0.080, 0.336]. Because the groups are different years, the approach also
  assumes the underlying population is stable over time; a 2007–2010 sample is
  reported in the supplement as a check (p. 1948).
- **Small samples** (pp. 1949–1950, Table 5): RBC coverage for τ_l(x̄) is about 90%
  at the smallest simulated N, driven by the few observations available for
  μ_{0,l}(l), rising to about 94% at N = 5000.
- **Fuzzy extension** (§6, pp. 1950–1951): with one-sided noncompliance and
  monotonicity, dividing the adjusted intention-to-treat contrast by the
  treated take-up rate gives the extrapolated effect for compliers.
- **Other routes** (p. 1944): approaches using external information
  (pre-intervention outcomes, multiple measures of the score, covariates that
  make the score ignorable) and within-design approaches (derivative-based
  marginal extrapolation; fuzzy-compliance variation). Local randomization
  methods have internal validity only inside their window (p. 1944).

Inference (this crib, not the source): the falsification tests examine the
region below l, while the assumption is used on (l, h). A pass is evidence about
an adjacent region, read together with the test's power; it is not a check of
the extrapolation region itself.

## 7. `rdmulti` syntax and output (CTV20; CIT24)

- `rdmc` — noncumulative (and pooled analysis of any multi-cutoff design).
  Stata `rdmc depvar runvar, cvar(cutoff_var)`, where `cutoff_var` holds the
  cutoff **each unit faces** (CTV20 pp. 871, 879); R
  `rdmc(Y, X, C)` with C unit-level (CIT24 p. 88). Per-cutoff options are
  passed as variables with one row per cutoff (`hvar()`, `pvar()`,
  `bwselectvar()`, `kernelvar()`, `covsvar()`, `vcevar()`, ...); pooled options
  via `pooled_opt()`; `plot` draws estimates and weights (CTV20 pp. 871–873).
- Output rows (CTV20 pp. 879–880; CIT24 pp. 88–89): one per cutoff, then
  **Weighted** (cutoff-specific estimates times estimated weights ω̂(c), the
  share of units within the pooled bandwidth that face c; by default the
  bandwidth is the one `rdrobust` picks for the pooled fit, CTV20 p. 869) and
  **Pooled** (`rdrobust` on the normalized score). The two converge to the same
  parameter but differ in finite samples. The `Coef.` column is conventional;
  intervals and p-values are robust bias-corrected.
- Tests across cutoffs use the stored bias-corrected estimates and robust
  variances: Stata `e(b)`/`e(V)` with `lincom` (CTV20 p. 881); R `out$B`,
  `out$V` (conventional `out$Coefs`, weights `out$W`). In CIT24's example the
  bias-corrected difference is 0.163 against a conventional 0.146, z = 2.556,
  p = 0.011 (p. 89).
- `rdms` — cumulative cutoffs or two scores. Stata
  `rdms depvar runvar1 [runvar2 treatvar], cvar(cutoff_var1 [cutoff_var2])
  [range() xnorm() ...]` (CTV20 p. 876). For cumulative cutoffs `cvar()` is a
  short list of the cutoff values, one row per cutoff, not a unit-level
  variable (CTV20 pp. 883–884). For two scores the cutoff variables hold the
  coordinates of the chosen boundary points and `treatvar` is the treatment
  indicator (pp. 877, 888). R:
  `rdms(Y = Y, X = X, X2 = X2, zvar = Zvar, C = cvec, C2 = cvec2)`, positional
  order `rdms(Y, X, C, X2, zvar, C2)`, pooled via `xnorm =` (CIT24 pp. 97, 99,
  104). In the published examples `rdms` prints a Pooled row only when `xnorm`
  is supplied (CTV20 p. 888; CIT24 p. 99). The sources do not give the R name
  of the range option; in the package source (version 2.0.0) it is
  `rangemat`, and `xnorm` also yields a pooled row for cumulative cutoffs —
  confirm both in the installed help.
- Pooled estimate for cumulative cutoffs: assign each unit to its nearest
  cutoff and run `rdmc` (CTV20 p. 885).
- `rdmcplot depvar runvar, cvar()` — RD plots per cutoff group (CTV20 p. 874).

## 8. What the sources say not to do

- Do not read τ_P as the average effect across cutoffs or across the
  population (CKTV16 PDF pp. 2, 8).
- Do not interpret differences among cutoff-specific effects as how the effect
  varies with the score unless cutoff ignorability is defended; under
  cumulative cutoffs it is implausible (CKTV16 PDF pp. 11–12, 19).
- Do not let a cutoff's estimation window include units at the next dose
  (CTV20 p. 884).
- Do not extrapolate to populations or score values outside those the cutoffs
  define, and do not present a non-rejected falsification test as proof of the
  extrapolation assumption (CKTV21 pp. 1945, 1947).
- Do not use `rdms` distances on raw geographic coordinates without deciding
  that Euclidean distance is the right metric (CIT24 p. 104).

## Review use

1. **Trigger.** Fire whenever cutoffs vary across units (by region, year,
   school, or a normalized score), whenever a cumulative dose schedule is
   pooled, whenever two or more scores jointly assign treatment, and whenever a
   close-election RD has races with three or more candidates. Classify the
   design (noncumulative, cumulative, multi-score) in the estimand record.
2. **Pooled headline.** If the paper's headline is a normalized-and-pooled
   estimate, compute the weights ω̂(c) and the cutoff-specific estimates
   (`rdmc`). Report the share of weight carried by the largest cutoff. If one
   cutoff carries most of the weight, the headline is close to that cutoff's
   effect and must be described that way. If cutoff-specific effects differ
   and the paper presents the pooled number as the effect, the claim is restated as
   a density-weighted average at the cutoffs. Not a kill; a rescoping. For a
   fuzzy pooled estimate, also report the first stage per cutoff.
3. **Heterogeneity claims across cutoffs.** Require a formal test on
   bias-corrected estimates with robust variances (account for shared
   observations under cumulative cutoffs). A claim that the effect rises with
   the score, or a policy conclusion drawn from cross-cutoff differences,
   needs cutoff ignorability argued explicitly; under cumulative cutoffs mark it
   unsupported.
4. **Cumulative estimation.** Check that each cutoff's sample excludes units at
   the next dose (range restriction, midpoint or median split). If it does not,
   the cutoff-specific estimates are contaminated; re-estimate with the
   restriction before judging them.
5. **Per-cutoff validity.** Run density and covariate-balance tests within each
   cutoff subsample, not only on the pooled normalized score. *Inference:* a
   pooled test can average away sorting concentrated at one cutoff.
6. **Multi-score.** Require boundary-point estimates at points with dense data
   on both sides, the distance metric stated, and the pooled distance estimate
   alongside. For geographic boundaries route to the boundary-discontinuity
   record.
7. **Extrapolation rule.** Any statement about effects for units away from the
   cutoff — higher or lower scorers, the average applicant, a scaled-up or
   universal program, a moved threshold — is an external-validity claim. It is
   graded unsupported unless the paper names an extrapolation assumption and
   defends it. For the multi-cutoff constant-bias route, demand: the target
   subpopulation (the group facing the lower cutoff) and the score range
   between the cutoffs; the direction (right-to-left implies constant effects
   across cutoffs); both falsification tests with their power, read as evidence
   about the region below the lower cutoff; evidence that the cutoff groups are
   not separated by a change in population (different years or places); and
   RBC inference including the covariance term. Claims beyond the highest
   cutoff, below the lowest, or for populations not exposed to any cutoff are
   not identified by this method. Failure costs the claim its estimated
   status: it becomes an assumption, and the verdict on the external-validity
   claim is unsupported, not refuted.
