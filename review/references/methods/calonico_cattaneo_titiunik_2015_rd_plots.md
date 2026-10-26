# RD plots — Calonico, Cattaneo & Titiunik (2015)

Working distillation of Sebastian Calonico, Matias D. Cattaneo and Rocío
Titiunik, "Optimal Data-Driven Regression Discontinuity Plots," *Journal of
the American Statistical Association* 110(512) (December 2015): 1753–1769,
doi:10.1080/01621459.2015.1017578. Version audited: the published article
(JASA furniture on p. 1753; received October 2014, revised January 2015).
The supplemental appendix (proofs, ES-versus-QS IMSE formulas, the
weights-to-scale table, further applications and simulations) was **not**
audited. Source PDF (not distributed with the skill):
`Calonico_Cattaneo_Titiunik_2015_RDPlots_JASA.pdf`. The article states no
software defaults; the `rdplot` defaults in §8 come from two published
companion sources: Calonico, Cattaneo, Farrell & Titiunik, "rdrobust:
Software for Regression Discontinuity Designs," *Stata Journal* 17(2)
(2017): 372–404 ("CCFT 2017"), and Cattaneo, Idrobo & Titiunik, *A
Practical Introduction to Regression Discontinuity Designs: Foundations*
(Cambridge Elements, 2020), §3 pp. 16–32 ("CIT 2020").

Verification status: source-audited 2026-10-15 (main text only; supplement
not audited).

Use in this battery: `rdd-diagnostics` core check **RD plot**; the
covariate and placebo-cutoff checks (RD plots
of covariates and the search for jumps away from the cutoff); the fuzzy
first-stage check (plots of take-up).

## 1. What an RD plot is (§1 pp. 1753–1754; §2.1 pp. 1756–1757)

Two ingredients, fitted separately on each side of the cutoff:

1. a **global polynomial fit** of order k of Y on X using the raw
   observations on that side — in practice k = 4 or k = 5 "are almost
   always the preferred choices" (p. 1756); the paper does not study the
   choice of k;
2. **local sample means** of Y over a disjoint partition (bins) of the
   support on each side; the partitions are built separately for
   [xl, x̄) and [x̄, xu], so no bin straddles the cutoff (p. 1757).

The paper's subject is the number and placement of bins, not estimation or
inference of the RD effect (p. 1756). A raw scatterplot is uninformative:
in the Lee (2008) House data no jump is visible in the cloud despite a
highly significant effect, and the problem is worse for binary outcomes
(p. 1755).

## 2. The two purposes of the binned means (pp. 1754–1755)

- **Detection of discontinuities.** The binned means are a discontinuous
  estimate of the regression function, so they can show jumps
  **away from the cutoff**, which would cast doubt on the continuity
  assumption. Global polynomial fits typically "hide the presence of such
  discontinuities"; the local means do not (p. 1754).
- **Representation of variability.** The means act as an undersmoothed,
  disciplined scatterplot that shows the data's spread, not a trace of the
  regression function (p. 1755).

Each purpose has its own optimal bin count (§4).

## 3. What the global polynomial fit is and is not (pp. 1756–1757)

It is a series estimate of μ−(x) and μ+(x) over the whole support, fitted
to raw observations, there to show the global shape. The paper lists three
defects of global polynomials (p. 1757): counterintuitive weighting schemes
(Gelman and Imbens), erratic behaviour near the boundaries of the support
(Runge's phenomenon) and oversmoothing of "potential discontinuities in
the interior" of the support. The binned means exist to counter these
defects. CIT 2020 pp. 34–35 draws the consequence: global polynomials
serve RD plots because the aim there is to show the whole regression
function, but they give unreliable point estimates and inference at the
cutoff, a boundary point, and should not be used for formal RD analysis.

Inference, not the source's words: the vertical gap between the two
plotted polynomials at the cutoff is a global-polynomial RD estimate. It
is neither the paper's local estimate nor evidence for it.

## 4. Number of bins: IMSE-optimal versus mimicking variance (§§3.2–3.3, 4.2–4.3)

More bins mean less bias and more variance (p. 1757). With weight
w(x) = f(x) recommended (p. 1762):

- **IMSE-optimal** J = ⌈(2B/V)^(1/3) n^(1/3)⌉ per side (eq. 1 for ES,
  eq. 4 for QS; pp. 1758, 1761). Its bin means trace out the regression
  function. The authors recommend it for visually checking for
  discontinuities, followed by formal placebo tests with robust RD
  inference (p. 1758). CIT 2020 p. 25: IMSE plots are often so smooth
  that the means nearly lie on the global fit, and may miss the local
  variability near the cutoff.
- **Mimicking variance (MV)** J = ⌈(V±/V_ES,±) · n / log(n)²⌉ (eq. 3 for
  ES, eq. 6 for QS; pp. 1760–1761): chosen so the binned means' integrated
  variability matches that of the raw data, up to the log(n) factor
  required by the theory. It generally gives more bins than the IMSE rule
  (p. 1760).
- **Weighted IMSE** (eq. 2, p. 1759): J = ω × J_IMSE. Any ad hoc bin count
  can be rationalised as WIMSE-optimal under some variance/bias weights
  (p. 1759), so a label of "optimal" says little. Its use is to express an
  ad hoc choice as a scale factor relative to the IMSE choice.
- Lee data, n = 6558 (Figs. 2–3, p. 1766): ES IMSE 20 | 17 bins, ES MV
  84 | 130; QS IMSE 48 | 19, QS MV 119 | 144 (left | right, spacings
  estimators).

## 5. Evenly spaced versus quantile spaced bins (§§3–4, 6.3)

- **ES**: equal-length bins on each side (p. 1757), the most common ad hoc
  practice (e.g., Lee's 0.5-point bins = 200 per side). Bins can be empty
  in finite samples (p. 1761), and the precision of the means varies with
  the number of observations per bin.
- **QS**: bin edges at the empirical quantiles of X on each side (p. 1760),
  so each bin holds about N±/J± observations (p. 1761). Mean variability
  then varies only through heteroskedasticity (p. 1760). QS is "covariate
  design adaptive" and may suit sparse data (p. 1755).
- Neither dominates in general; the selectors coincide when X is uniform;
  in the 16 simulation designs QS did better on IMSE where the density is
  low in some regions (p. 1768). CIT 2020 p. 21 adds that a QS plot shows
  the density of the score at a glance: it looks empty where observations
  are few.

## 6. Data-driven implementation (§5, pp. 1761–1764)

Spacings estimators (order statistics and concomitants) estimate the
constants without extra tuning parameters and are the recommended choice wherever
they apply (p. 1762). They require continuously distributed outcomes. For
binary or other discrete outcomes the concomitant method is invalid, and
the polynomial (series) estimators of Remarks 1–2 must be used
(pp. 1763–1764). Consistency (Theorems 3–4) treats the polynomial order
as growing, kₙ → ∞ with kₙ⁷/n → 0 (p. 1763).

## 7. How bin choice can manufacture or hide a jump

What the source shows: ad hoc bin choices "misrepresent the actual
behavior of the data" (p. 1755). Fig. 1 plots the same data with 250, 100
and 20 bins per side and gets "very different representations of the
underlying data" — and so of the design's validity (p. 1755).

Inference, not the source's words — the mechanisms a reviewer should
check:

- *Few wide bins.* The bin next to the cutoff averages outcomes over a
  wide interval; with a steep regression function its mean sits far from
  the boundary value, so the gap between the two innermost dots can
  exaggerate, shrink or reverse the jump.
- *Many narrow bins.* Noise in thin bins buries a real jump, as in the
  raw scatter (p. 1755).
- *ES bins under sparse data.* Means near the cutoff or in the tails rest
  on a handful of observations and can create spurious steps.
- *Polynomial overlay.* The eye reads the quartic's gap at the boundary,
  where global fits behave worst (p. 1757); an IMSE-binned plot whose dots
  hug the fit adds little independent evidence (CIT 2020 p. 25).
- *Asymmetric choices.* Different bin widths, bin types or support limits
  on the two sides change the visual contrast without changing the data.

## 8. Extensions and `rdplot` defaults

- **Fuzzy RD** (§7.1, p. 1768): the results apply unchanged to the
  reduced form (Y on X) and to the first stage (T on X). Because T is
  binary, the first-stage plot needs the Remark 1–2 selectors.
- **Covariates** (§7.2, p. 1768): either condition on discrete covariates
  (plot by subsample), or remove covariate effects with an
  additive-separable GAM/backfitting step and plot the adjusted outcome.
  The article gives no software option for this.
- **`rdplot` defaults** (companion sources, not the article): bins are
  ES with the mimicking-variance count (CIT 2020 p. 80); the polynomial
  fit uses a uniform kernel (CCFT 2017 p. 386; CIT 2020 p. 22) over the
  full support unless `h` is set (CCFT 2017 p. 387; CIT 2020 p. 23); the
  documented output for calls that do not set `p` reports polynomial
  order 4 (CIT 2020 p. 23; CCFT 2017 p. 391); `scale` defaults to 1 and
  `support` to the sample range (CCFT 2017 p. 387). The output reports
  the IMSE and MV bin counts, the implied scale and the WIMSE weights
  (CCFT 2017 p. 391). Bin confidence intervals are optional (`ci`); with
  IMSE bins they may carry first-order smoothing bias, so use MV bins or
  undersmooth (`scale`, `nbins`) when showing them (CCFT 2017
  pp. 391–392).
- **Plotting the actual estimate.** Restrict the sample to the rdrobust
  window and set `h`, `p = 1` and `kernel = "triangular"` to match the
  estimate (CCFT 2017 pp. 392–394; CIT 2020 pp. 54–55, R snippet:
  `rdplot(Y[abs(X) <= h], X[abs(X) <= h], p = 1, kernel = "triangular")`).
  The same construction serves covariate plots inside each covariate's
  bandwidth (CIT 2020 p. 84).

## Review use

- **Trigger.** Any RD figure offered as evidence of the jump, of
  continuity, of covariate balance or of first-stage strength.
- **Record what the paper's figure is.** Bin type (ES/QS), count per side,
  selector or ad hoc, polynomial order, fit window and kernel. If the
  paper does not say, call the bins ad hoc.
- **Re-plot from the data.** Run `rdplot` at its default (ES, MV) and
  with `binselect = "es"` (IMSE) and `"qsmv"`; compare with the paper's
  figure. A jump visible only under the paper's bin choice is a
  presentation artefact; report the bin counts that produce and remove
  it.
- **Separate fit from means.** The gap between global quartics at the
  cutoff is not the paper's estimate; never cite it as one. For a visual
  of the estimate, use the local plot in §8 and check that its intercept
  gap matches the reported point estimate.
- **Look away from the cutoff.** Jumps in the IMSE-binned means at other
  values of X are the falsification signal the plot was designed for
  (p. 1754): test them as placebo cutoffs with robust RD inference
  (p. 1758).
- **No inference from the picture.** A plot cannot clear or convict a
  jump; the RBC estimate decides. If bin CIs are shown, check that MV or
  undersmoothed bins were used.
- **Fuzzy designs.** Demand the first-stage plot beside the reduced form.
- **Binary outcomes.** Spacings-based bin selectors are invalid; the
  polynomial-based variants apply (Remarks 1–2). Check the installed help
  for the option name; this article does not give it.
- **Cost of failure.** A visual jump that disappears under data-driven
  bins adds nothing beyond the RBC estimate and must not be described as
  *clear* or *visible* evidence. A discontinuity in the binned means away
  from the cutoff, confirmed by a placebo test, undercuts the continuity
  assumption the whole design rests on.
