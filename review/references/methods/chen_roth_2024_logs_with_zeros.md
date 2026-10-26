# Log-like transformations of zero-valued outcomes — Chen & Roth (2024)

Working distillation of Jiafeng Chen and Jonathan Roth, "Logs with Zeros?
Some Problems and Solutions," *Quarterly Journal of Economics* 139(2)
(2024): 891–936 — the published article (DOI 10.1093/qje/qjad054), not a
working paper. Verified against the published PDF (not distributed);
printed page = PDF page + 890 (PDF page 1 is printed page 891, and
the offset is constant — the printed folio is on every page). All cites
below are to the printed page.

Use in this battery:

1. **The unit-rescaling sweep** in `scale-sensitive-diagnostics` — what a
   moving estimate means and why (§§2–3 below).
2. **The functional-form row** of the design matrix — when `log(1+Y)`,
   `asinh(Y)`, `log(c+Y)`, or `√Y` on a zero-valued outcome is load-bearing.
3. **The alternative estimands to propose** when the transform is doing the
   work (§5) — the review should never stop at "the coefficient is
   unit-dependent"; name the honest parameter that replaces it.

## 1. The result — Proposition 1 (pp. 897–898)

Setup: binary treatment, outcome Y ∈ [0, ∞), ATE on a transform
θ(a) = E_P[m(aY(1)) − m(aY(0))], where a is the units scaling (a = 100 is
dollars→cents). Suppose:

i. m : [0,∞) → R is continuous and weakly increasing;
ii. m is "log-like": m(y)/log(y) → 1 as y → ∞ (satisfied by log(1+y) and
    arcsinh(y));
iii. treatment affects the extensive margin: P(Y(1) = 0) ≠ P(Y(0) = 0);
iv. E[|log Y(d)| | Y(d) > 0] < ∞ for d = 0, 1.

**Then for every θ\* ∈ (0, ∞) there exists an a with |θ(a)| = θ\***: θ(a) is
continuous, → 0 as a → 0, and |θ(a)| → ∞ as a → ∞. A percent is
unit-invariant; these ATEs are arbitrarily unit-dependent, so they cannot
be interpreted as approximate average percentage effects. The result is
about estimands — any consistent estimator inherits it (OLS, IPW, doubly
robust; Remark 4 extends it to a plain OLS estimand with no causal reading:
the coefficient on any X with m(Y) on the left is arbitrarily
scale-sensitive whenever the coefficient on 1[Y > 0] is nonzero, p. 902).

## 2. Why (§II.A, p. 898)

A percentage effect is undefined for an individual going 0 → nonzero, so
any ATE defined at zero implicitly sets the weight on extensive- versus
intensive-margin changes — and the units of Y set that weight. For
intensive movers m(Y(1)) − m(Y(0)) ≈ log(Y(1)/Y(0)), nearly unit-free; for
extensive movers the term is m(aY(1)) − m(0), which grows with a.

## 3. What the rescaling sweep measures — Remarks 1–7 (pp. 901–904)

- **Finite rescaling ≈ the extensive-margin effect (eq. 2, Remark 2,**
  pp. 901–902): multiplying Y by a large a changes the ATE by
  approximately (P(Y(1) > 0) − P(Y(0) > 0))·log a. The unit-rescaling sweep
  is therefore a measurement of the extensive-margin effect — run the
  extensive-margin regression (outcome 1[Y > 0]) alongside it and report
  both.
- **The t-statistic follows too (Remark 5,** pp. 902–903): as a → ∞ the
  t-stat on θ̂(a) converges to the t-stat on the extensive-margin estimate.
- **`log(c + Y)` is the same object (Remark 1,** p. 901): varying c in
  log(c + Y) is equivalent to varying the scale in log(1 + Y); the ATE
  blows up as c → 0. A paper's "robust to the choice of c" check *is* a
  units-sensitivity check.
- **"Make the nonzero values large" is backwards (Remark 6,** pp. 903–904):
  the Bellemare–Wichman (2020) advice to rescale so most nonzero values
  are large makes the ATE driven nearly *entirely* by the extensive
  margin.
- **Zero extensive-margin effect does not rescue it (Remark 7,** pp.
  903–904): by their Proposition 3 (Online Appendix), every non-log
  transform is scale-dependent for some strictly-positive DGP; and only if
  the extensive effect were exactly zero for all individuals is the right
  move to drop the zeros and use the ATE in logs. Otherwise bound the
  intensive effect (Lee 2009, under monotonicity; tight when the
  extensive-margin effect is near zero, fn. 31, p. 919).
- **Continuous treatments (Remark 3 + OA B.2):** any contrast averaging
  m(aY(d)) over dose d is arbitrarily scale-sensitive given an extensive
  margin.

## 4. The published record — Table I (§II.C, pp. 904–905)

17 AER articles since 2018 estimate an ATE for arcsinh(Y); 10 interpret it
as a percentage effect or elasticity. Of the 10 replicable, **5 change by
more than 100% of the original estimate** under a ×100 rescaling; only 3
move less than 10%, and all three have zero or near-zero (< 1 pp)
extensive-margin effects.

## 5. The trilemma — Proposition 2 (pp. 908–909)

With zero-valued outcomes, no parameter θ_g = E_P[g(Y(1), Y(0))] (g
nonconstant, weakly increasing in its first argument) is simultaneously:

(i) an average of individual-level treatment effects of that form;
(ii) scale invariant;
(iii) point identified from the marginal distributions.

Corollaries worth carrying (§III.A, p. 909): on strictly positive support
the *only* parameter satisfying (i)–(iii) is the ATE in logs (up to affine
transformation — their Proposition 3); and the average proportional effect
θ_Avg% = E[(Y(1) − Y(0))/Y(0)] is not point identified even with strictly
positive outcomes — it is exactly what a reader thinks an asinh
coefficient is, and it is not identified.

## 6. The alternatives — pick by goal (§IV, pp. 910–919)

- **Interpretable units (§IV.A, pp. 913–917):** θ_ATE% =
  E[Y(1) − Y(0)] / E[Y(0)] — the ATE in levels as a percentage of the
  control mean. Point identified, scale invariant; escapes the trilemma by
  dropping (i) — it is the percentage change in the *mean*, not an average
  of individual percentages. Estimated by Poisson QMLE of
  Y = exp(α + βD)U: e^β − 1 = θ_ATE%. Caveats the review should state:
  it is levels-weighted, so it can be tail-dominated on skewed outcomes
  (their $100-for-all vs $35bn-for-Musk example, pp. 915–916), and it
  counts a 0→1 move the same as a 1→2 move — fine for counts, wrong when
  zero is a distinct economic state. Variants: θ_Median% (median QTE over
  median of Y(0)); normalizing the outcome itself (per-capita Y/X,
  pretreatment outcome, E[Y(0)|W]); rank transforms Ỹ = F(Y) (Delius &
  Sterck 2020 — Chetty et al. 2014 found ranks more stable than log(c+Y),
  which moves with c); and reporting effects on 1[Y ≥ y] at several
  thresholds, in percentage points.
- **Decreasing returns (§IV.B, pp. 917–918):** calibrate the margin value
  explicitly — m(y) = log(y) for y > 0, m(0) = −x, i.e. a 0→1 move is
  worth 100x%. Transparent and still scale-dependent by design; the value
  judgment is now in the open instead of inside the units.
- **Margins separately (§IV.C, pp. 918–919):** θ_Intensive =
  E[log Y(1) − log Y(0) | Y(1) > 0, Y(0) > 0] is scale invariant but not
  point identified → Lee (2009) bounds under the monotonicity assumption
  (anyone positive under control stays positive under treatment), reported
  alongside the extensive effect P(Y(1) > 0) − P(Y(0) > 0). The bounds are
  tight exactly when the extensive margin is small — i.e., when log-like
  ATEs are least scale-sensitive (fn 31). NB: two-part-model marginal
  effects are *not* θ_Intensive — they carry an added selection term
  (their Online Appendix D, against the Mullahy–Norton recommendation).
- **DiD caveat (pp. 913–914):** parallel trends for a log-like transform
  is specific to the transform *and* the units — PT for arcsinh-of-dollars
  does not imply PT for arcsinh-of-cents (Roth & Sant'Anna 2023).

## 7. Applications (§V, pp. 920–932)

RCT (Carranza et al. 2022), DiD (Sequeira 2016), IV (Berkouwer & Dean
2022). In the IV application the Lee bounds on θ_Intensive for compliers
are [−0.565, −0.538]; both of the authors' asinh specifications produce
estimates *outside* those bounds (p. 932).

## Reviewer checklist

- Load-bearing `log(1+Y)`/`asinh` outcome transform with zeros present →
  run the ×10/×100 rescale on the exact published spec; the movement is ≈
  the extensive-margin effect × log a (eq. 2).
- Always report the extensive-margin regression 1[Y > 0] ~ D alongside —
  its t-statistic is where the headline t-statistic converges (Remark 5).
- If the claim needs a percentage: propose θ_ATE% via PPML (stating it is
  a percent of the mean, not an average of individual percents) or split
  the margins (extensive effect + Lee bounds on θ_Intensive).
- A "robust to choice of c in log(c + Y)" defense is a units-sensitivity
  test by another name (Remark 1); "we rescaled so nonzero values are
  large" makes the dependence worse, not better (Remark 6).
- **Scope:** the paper is about zeros in the *outcome*. A zero-valued
  *regressor* is a different question — asinh of a regressor is still
  units-sensitive as a semi-elasticity (Thakral & Tô 2023; Aihounton &
  Henningsen 2021), while √ of a regressor rescales cleanly. Do not cite
  Chen–Roth for the regressor case.

## 8. Allied literature the battery draws on

Four sources extend this crib's results to the cases it does not cover —
each has its own crib:

- **asinh on *both* sides** (`bellemare_wichman_2020_ihs_elasticities.md`):
  the exact implied elasticity is β̂·[√(y²+1)/y]·[x/√(x²+1)], converging
  to β̂ only for large x, y — the coefficient-as-elasticity convention is
  an approximation with named data requirements (min |value| ≥ ~10;
  ≤ ~1/3 zeros), and elasticities are undefined at zeros. This is the
  constructive counterpart to Remark 6: not just "the defensive rescale
  is backwards" but "here is what the coefficient actually estimates".
- **Scale as a significance-selection channel**
  (`fitzgerald_etal_2026_loglike.md`): the rescaling sweep doubles as a
  multiple-testing diagnostic — 38% of published estimates sit at a local
  |t| maximum ("sweet spot"); adds the normalized-estimand alternative
  (divide by a constant — zeros-tolerant, scale-invariant) and quantile
  regression for intensive-margin slopes.
- **DiD-specific levels-vs-logs** (`mcconnell_2024_forest_logs.md`):
  levels and logs DiD are *different estimands* (additive vs
  multiplicative trends) that can disagree in sign when baseline outcome
  distributions differ — complementary to this paper's transform-specific
  PT point: the scale choice selects the estimand, not just its scale.
- **IV + unit FE + count outcome** (`jochmans_2022_iv_fe_count.md`):
  FE-IV-Poisson alternatives are inconsistent under fixed-T — the caveat
  that must travel with any "just use Poisson-IV" recommendation.
