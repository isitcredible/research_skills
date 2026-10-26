# OVB sensitivity: robustness value and partial R² — Cinelli & Hazlett (2020)

Working distillation of Carlos Cinelli and Chad Hazlett, "Making Sense of
Sensitivity: Extending Omitted Variable Bias." This crib was verified
against the **JRSS-B preprint** (not distributed); the published version
is *JRSS Series B* 82(1) (2020): 39–67.
Equation and section numbers below follow the preprint; the
published version's numbering matches for the core results but verify
before quoting page numbers. Software: R `sensemakr`, Stata `sensemakr`,
`iv.sensemakr` for the IV extension.

Use in this battery:

1. **The OVB-sensitivity record** in the design matrix — the robustness
   value, the partial R² input, the benchmark bounds (§§1–3).
2. **The exclusion-restriction sensitivity in `iv-diagnostics`** — the
   same machinery applied to the instrument on the Anderson–Rubin fit.
3. **What the numbers mean and don't** — the RV is a statement about the
   estimate's fragility, not about whether a confounder exists (§4).

## 1. The partial-R² reparameterization (§4, eqs. 8–14)

The OVB formula reparameterized: with Z the omitted confounder, the bias
of the full-covariate-adjusted estimate depends on two scale-free
quantities — the partial R² of Z with the treatment (R²_{D~Z|X}) and of
Z with the outcome (R²_{Y~Z|D,X}). Both lie in [0,1]; the contour plot of
adjusted estimates over that unit square is the sensitivity display.

Key asymmetry (§4.x): the bias factor is **bounded in the outcome
association and unbounded in the treatment association** — a confounder
strongly related to treatment can do arbitrary damage even explaining
little residual outcome variance, while outcome association alone caps
the bias. The "extreme scenario" bound (confounder explains ALL residual
outcome variation, R²_{Y~Z|D,X} = 1) gives the adjusted-estimate bound —
the extreme robustness value the record asks for.

Multiple confounders: any set Z reduces to the single linear combination
Z* = Zγ̂, which has the same partial R² with the outcome and *no greater*
partial R² with the treatment — so the single-confounder formulas bound
the multivariate case (§4.5). Nonlinear confounding and misspecification
of observed covariates are absorbed by defining Z as the basis functions.

## 2. The robustness value (§4.3, eqs. 18–20)

RV_q = the partial R² that a confounder needs **with both treatment and
outcome** (equal strength both ways) to reduce the estimate by 100·q%:

  RV_q = ½( √(f_q⁴ + 4f_q²) − f_q² ),   f_q = q·|f_{Y~D|X}|,

where f_{Y~D|X} = |t|/√df is the partial Cohen's f of the treatment —
computable from any regression table (t and df). For significance loss
at level α, replace f_q by f_{q,α} = f_q − f*_{α,df−1} (f* = critical
t/√df); if f_{q,α} < 0 the RV is zero — the estimate is already
insignificant at α.

Interpretation: a confounder explaining RV% of residual variance of
*both* treatment and outcome suffices to overturn; a confounder with
*both* associations below RV% cannot. One-sided cases (one association
above RV%, the other below) are not settled by the RV — use the
extreme-scenario bound or the sensitivity contours (preprint §5.1,
Darfur example: "For cases where one association is over 13.9% and the
other is below, we conduct additional analyses"). RV near 0 → even weak confounders
kill the result; near 1 → only a confounder explaining nearly all
residual variation could.

## 3. Benchmarking (§4.4)

Formal version of "as strong as covariate X_j": bound the confounder's
partial R²s by κ times the observed covariate's, with κ chosen on
substance ("a confounder twice as strong as education"). The paper
*replaces* the informal practice of comparing to unadjusted statistics —
unadjusted covariate associations understate the relevant bound because
they omit the covariate's residual (post-X) associations. Bounds can be
set separately for the treatment side and the outcome side by different
covariate groups.

## 4. What the numbers are (reporting standard, §5)

Routine-reporting pair the paper proposes: (i) the partial R² of the
treatment with the outcome, (ii) the robustness value. The battery's
OVB-sensitivity record adds (iii) the benchmark multiples κ. None of
these is a verdict — they quantify how much confounding the claim can
absorb; whether such a confounder exists is a substantive argument the
review cannot settle from the regression table.

For IV (`iv.sensemakr`): the same computations run on the
Anderson–Rubin reduced-form fit of outcome on instrument, measuring how
strong a confounder of the *instrument* must be to overturn — the
exclusion/exogeneity sensitivity, distinct from strength.

## Reviewer checklist

- Inputs needed: treatment (or instrument) coefficient, SE, residual df,
  and the adjusted R²s — all standard-table objects; no re-estimation
  needed to start.
- Report RV_q at the claim's relevant q (usually q = 1, and RV_{q,α} for
  significance) *beside its benchmarks*, never bare: an RV below what a
  single named covariate already explains is a fragility finding; an RV
  beyond any plausible confounder is a robustness finding — report which.
- Do not report partial R² of treatment-with-outcome as a
  "variance-explained" number — it is a sensitivity input; the design
  matrix keeps it out of the decomposition row for this reason.
- For coefficient-stability-style selection-on-observables arguments see
  `oster_2013_unobservable_selection.md` — a different sensitivity logic
  (movement × R² under proportional selection), complementary, not a
  substitute.
