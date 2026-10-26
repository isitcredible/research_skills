# Prediction intervals for synthetic control — Cattaneo, Feng & Titiunik (2021)

Working distillation of Matias D. Cattaneo, Yingjie Feng and Rocio
Titiunik, "Prediction Intervals for Synthetic Control Methods",
*Journal of the American Statistical Association* 116(536) (2021):
1865–1880. The source PDF (not distributed with the skill) is the **published JASA article**
(`Cattaneo_Feng_Titiunik_2021_SCprediction_JASA.pdf`).

## The result

SC had no principled uncertainty quantification — Abadie–Diamond–
Hainmueller's design-based permutation is the standard but is not a
confidence interval for the effect. CFT develop **conditional
prediction intervals** for the SC counterfactual (§§2–3): treating the
SC as a prediction of the treated unit's post-treatment counterfactual,
they construct nonasymptotic intervals via concentration inequalities
on the prediction error, valid conditional on the pretreatment fit —
no large-T or placebo-permutation assumptions needed. Applies to the
standard constrained-weights SC and extensions.

## Why the battery needs it

The SC module had the construction-side checks (donor pool, RMSPE,
in-time/in-space placebos, augmentation — ADH, Abadie 2021, various
estimators) but no *inference* anchor other than permutation p-values.
Permutation tests answer "is the treated unit's gap unusual relative
to placebos?" — a different question than "what is the CI on the
effect?" — and can reject sharply even when the effect estimate is
imprecise. CFT supplies the missing interval.

## Review use

- `synthetic-control-diagnostics`: if the paper reports only
  permutation p-values, ask for a prediction interval. The interval is
  around the synthetic counterfactual; the test is whether it contains
  the treated unit's observed outcome. A tight permutation p with the
  treated outcome inside the interval means the effect is not
  distinguishable from prediction error under CFT's assumptions — a test
  under rule 8 (report its power against the paper's estimate), not a
  correction; a wide interval that still excludes the treated outcome is
  not. The interval also exposes the
  pretreatment-fit fragility (intervals widen as pretreatment fit
  degrades).
- `small-n-diagnostics`: SC is the extreme case of small-N inference —
  one treated unit — and CFT is the formally correct small-N object
  where the permutation approach is heuristic.
