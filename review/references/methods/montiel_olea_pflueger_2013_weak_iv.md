# Robust weak-instrument testing: the effective F — Montiel Olea & Pflueger (2013)

Working distillation of José Luis Montiel Olea and Carolin Pflueger,
"A Robust Test for Weak Instruments," *Journal of Business & Economic
Statistics* 31(3) (2013): 358–369 — the published article (DOI
10.1080/00401706.2013.806694), not a working paper. Verified against
the published PDF (not distributed); printed page = PDF page + 357 (PDF
p.1 = printed p. 358). All cites are to the printed page.

Use in this battery:

1. **The weak-IV row of `iv-diagnostics`** when errors are clustered,
   autocorrelated, or heteroskedastic — the setting where Stock–Yogo
   critical values do not apply (see
   `stock_yogo_2002_weak_instruments.md` for the i.i.d. case).
2. **Auditing a printed "first-stage F > 10"** — under non-i.i.d.
   errors the relevant statistic is the effective F, and the relevant
   threshold can be over twice 10 (§3).

## 1. What is tested (§2, pp. 359–361)

Null hypothesis: the **Nagar bias** of the estimator (TSLS or LIML)
exceeds a fraction τ of a "worst-case" benchmark bias (the bias of a
benchmark estimator — OLS-type worst case). Testing τ = 10% at 5% is
the standard implementation: reject "weak instruments" when the
effective F exceeds the critical value.

## 2. The statistic and the recipe (§§2–3, pp. 360–363)

The **effective F-statistic F̃_eff is a scaled version of the
*non-robust* first-stage F** — not a Kleibergen–Paap-style robust F. The
robustness enters through the *critical value and degrees of freedom*,
which are computed from Ŵ, the estimated asymptotic covariance matrix
of the reduced-form OLS coefficients (their eqs. 3–5):

1. Partial out additional exogenous regressors (projection residuals);
   normalize the instruments to be orthonormal.
2. Estimate Ŵ = covariance of the reduced-form coefficients under the
   *same* error assumption the inference uses — heteroskedasticity-
   robust for cross-sections, HAC for time series, clustered for panels
   (p. 361). **This is where the robustness lives.**
3. F̃_eff = (reduced-form fit) / [S·tr(Ŵ₂)] — the nonrobust first-stage
   F numerator scaled by the trace of the instrument block of Ŵ
   (eq. 3).
4. Effective degrees of freedom K̂_eff (eq. 4): a Patnaik-style moment
   match on Ŵ₂ and x = B_e(Ŵ, Σ̂)/τ, where B_e bounds the Nagar bias of
   estimator e relative to the benchmark.

## 3. The two procedures (§2.2, pp. 361–363)

- **Generalized test** — any number of instruments, TSLS or LIML;
  critical value = upper-α quantile of a Patnaik-approximated
  distribution evaluated at K̂_eff; requires a numerical routine
  (Stata `weakivtest`; the authors' MATLAB code).
- **Simplified test** — TSLS only, conservative by construction
  (protects against the worst-case covariance); the 5% critical value
  is read off their Table 1 and depends only on K̂_eff. For τ = 10%
  the simplified critical values run **from 11 up to 23.1** (p. 359):
  rejecting "weak" whenever F̃_eff > 23.1 is the maximally safe rule —
  meaning **a first-stage F of 10 is not generally adequate**, and even
  F ≈ 15 can fail the test with enough instruments.

Their Figure 1 compares against Stock–Yogo: the SY critical value is
defined only when overidentification ≥ 2 and rests on i.i.d. errors;
MOP's nests it as the homoskedastic special case.

## 4. Practice points for the review

- Under i.i.d. errors F̃_eff reduces toward the plain first-stage F,
  but **under clustering or autocorrelation the two diverge** — the
  scaling denominator tr(Ŵ₂) is robust while the numerator is the
  non-robust fit. A paper quoting a Kleibergen–Paap rk Wald F in an
  overidentified model has computed a *different* statistic; MOP is the
  test to run, not a relabelling of KP (just-identified, the two
  coincide).
- The test is one-sided on bias: passing it certifies strength; it
  says nothing about exclusion (the skill's strength-vs-exclusion
  separation applies unchanged).
- The test covers one endogenous regressor only (§2.1, p. 359); Andrews–Stock–Sun
  (2019, fn. 4) know of no analog for several (the extension is
  Lewis–Mertens).

## Reviewer checklist

- Clustered/HAC VCE in the second stage → Stock–Yogo critical values
  are invalid; require F̃_eff or a KP statistic plus the MOP critical
  value, not "F > 10".
- Report which procedure (generalized vs simplified), the τ tested
  (default 10%), K̂_eff, and F̃_eff itself.
- Still report a weak-IV-robust CI (Anderson–Rubin or CLR) — the MOP
  test certifies the first stage; the robust set is the honest
  uncertainty statement when it fails or is marginal.
