# Contamination bias in multiple-treatment regressions — GPHK (2024)

Working distillation of Paul Goldsmith-Pinkham, Peter Hull, and Michal
Kolesár, "Contamination Bias in Linear Regressions," *American Economic
Review* 114(12) (2024), 4015–4051.

**Verification status: interim — audited against the working paper**
(`GoldsmithPinkham_Hull_Kolesar_2024_ContaminationBias_AERwp.pdf`,
not distributed with the skill). The published AER version was not obtained at audit time;
cite by section only and re-verify page anchors when it lands. (An
Anna's Archive drop carrying this filename was actually a different
paper — Wallace, Goldsmith-Pinkham & Schwartz NBER WP 30512 — and was
binned.)

Use in this battery: `controls-samples-diagnostics` — the
contamination-bias row for regressions with multiple mutually exclusive
treatments or a multi-valued treatment under controls.

## 1. The result

With several treatments D_i = (D_i1, …, D_iJ) and flexible controls W_i,
the coefficient on D_ij from the standard saturated-by-controls
regression does **not** estimate a convex average of the j-th treatment's
effects: it is contaminated by **non-convex averages of the other
treatments' effects** (abstract/§1). Single-binary-treatment regressions
with flexible controls do estimate a convex average — the contamination
is specifically a *multiple*-treatment phenomenon.

## 2. The repairs they discuss

Three approaches that avoid contamination bias (abstract): direct
estimation of the contamination-free contrast, targeting the
easiest-to-estimate weighted average effect, and
multiple-treatment-robust estimators. Their re-analysis of nine empirical
applications finds economically and statistically meaningful
contamination in observational studies; experimental applications are
less exposed (abstract).

## 3. Review-side use

- Any regression with ≥2 mutually exclusive or simultaneous treatments
  and controls (e.g. multiple policy arms, several instruments-as-
  regressors, event-study-type lead/lag structures read as separate
  treatments) is exposed — the check is whether the headline coefficient
  is the convex average it is presented as.
- A "negative" or sign-flipped coefficient in such a regression may be
  a contamination artifact — non-convex weights can flip a coefficient
  below zero even when every component effect is positive.
- When the claim needs an uncontaminated estimate, route to the
  paper's recommended estimators rather than re-weighting by hand.

## 4. Reviewer checklist

- Multiple treatments + controls → contamination check is mandatory,
  not optional.
- Report whether the paper's estimand is the contaminated coefficient
  or the convex average it intended.
- Published version pending: quote the WP by section, and re-audit page
  anchors when the AER PDF arrives.
