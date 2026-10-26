# Synthetic control: fit, specification searching, augmentation, and inference

Source-audited crib for the synthetic-control battery. One decision spine:
what does the pre-treatment fit actually constrain, how much specification
discretion was available, and what does the placebo grid resolve.

**Sources audited:**
- Abadie, Diamond & Hainmueller, "Synthetic Control Methods for Comparative
  Case Studies," *JASA* 105(490) (2010), 493–505 — published (library copy,
  not distributed with the skill).
- Ferman, Pinto & Possebom, "Cherry Picking with Synthetic Controls,"
  *Journal of Policy Analysis and Management* 39(2) (2020), 510–532 —
  published (library copy).
- Ben-Michael, Feller & Rothstein, "The Augmented Synthetic Control
  Method," *JASA* 116(536) (2021), 1789–1803 — published.
- Chernozhukov, Wüthrich & Zhu, "An Exact and Robust Conformal Inference
  Method for Counterfactual and Synthetic Controls," *JASA* 116(536)
  (2021), 1849–1864 — published.
- Arkhangelsky, Athey, Hirshberg, Imbens & Wager, "Synthetic
  Difference-in-Differences," *American Economic Review* 111(12) (2021),
  4088–4118 — published.
- Kaul, Klößner, Pfeifer & Schieler, "Standard Synthetic Control Methods:
  The Case of Using All Preintervention Outcomes Together With
  Covariates," *JBES* 40(3) (2022), 1362–1376 — published.

Verification status: **source-audited 2026-09-22**.

Use in this battery: `synthetic-control-diagnostics` (placebo-rank
specification, estimator refit, all-pre-outcomes pathology, Ferman
specification-discretion accounting).

## 1. What the estimator is — ADH 2010

The synthetic control is a weighted average of donor units chosen to match
the treated unit on pre-intervention outcomes and other predictors
(pp. 493–495, §2). Two structural facts for the audit:

- The weights minimize pre-intervention discrepancy over a predictor set
  X_1 = (Z_1, Ȳ_1^{K1}, …, Ȳ_1^{KM}) — covariates plus linear combinations
  of the pre-intervention outcome path (§3.2). A synthetic control that
  fits covariates and a *long* pre-intervention outcome path can only
  reproduce unobserved-factor-driven discrepancies that the factor
  structure itself shares (§2.2) — fit quality is doing identification
  work.
- If pre-treatment fit is poor, the method itself says do not proceed
  (p. 500); a synthetic estimate on a failed pre-fit is not a result, it
  is a report that the donor pool cannot synthesize the treated unit.

## 2. Inference — the placebo RMSPE machinery

ADH's in-space placebo: re-run the full synthetic-control exercise on each
donor unit, then compare the treated unit's post/pre RMSPE ratio against
the distribution of placebo ratios (§3.3). Two audit points:

- The ratio is post-RMSPE / pre-RMSPE, not the raw gap — and placebo units
  with hopeless pre-fits must be screened out or the comparison pool is
  padded with uninformative controls (ADH use fit screens in the
  application).
- The grid's resolution is the number of admissible placebos — with J
  donors the finest achievable two-sided resolution is ~1/(J+1). A
  placebo "p-value" near that floor is resolution-limited, not evidence
  of a null. Report the attainable grid, and where the grid is coarse,
  conformal inference (§4) is the sharper instrument.

## 3. The all-pre-outcomes pathology — Kaul et al. 2022

Kaul et al. (abstract, §§2–3): when the entire pre-intervention outcome
path is included as separate predictors together with covariates, the
covariates become irrelevant — their V-weights go to zero — because the
outcome lags span the space the covariates were meant to inform.
Consequences:

- "We included covariates" is cosmetic under all-lags predictor sets —
  audit the V matrix / predictor list; if all outcome lags are separate
  predictors, the covariate list is decoration.
- The fix they demonstrate: restrict the number of outcome lags used as
  predictors (or use summary linear combinations, as ADH's Ȳ^K notation
  intends) so covariates can obtain positive weight.
- Related mis-citation, flagged in the module: Ferman et al. 2020 are
  about specification-searching discretion (below), not about this
  pathology — do not cite them for the all-lags result.

## 4. Specification searching — Ferman, Pinto & Possebom 2020

Cherry-picking is a real, quantified pathology (abstract, pp. 510–511):

- Specification-searching opportunities are asymptotically irrelevant only
  under restrictions on the SC specification set; at the pre-treatment
  lengths and specification menus common in applications, there is
  substantial room to manufacture significance.
- The discretion lives in the choice of predictor set, V weights, and
  donor pool — a "significant" synthetic estimate can be selected from
  specifications that would have yielded nulls.
- Their recommendations (pp. 522–523; apply as an audit checklist): use
  all pre-treatment outcome lags as the benchmark specification unless a
  strong prior requires balancing specific covariates (then fewer lags,
  from specifications meeting their conditions); present results for many
  specifications, always including the all-lags benchmark; for a single
  test across them, combine the specification-level test statistics
  (Imbens–Rubin).

So an SC result presented as a single specification carries an unpriced
degrees-of-freedom discount — the module's spec-sweep is the instrument
that prices it.

## 5. Augmentation and the donor-shortage repair — BMF 2021

Augmented SCM (abstract, §§2–3): when exact pre-treatment fit is
infeasible (the usual case), fit an outcome model (their proposal: ridge)
on the residuals of the SCM pre-fit and de-bias the SCM estimate —
analogous to bias-corrected matching. Properties for the audit:

- Ridge augmentation directly controls pre-treatment fit while minimizing
  extrapolation; it permits negative weights on some donor units — so
  "negative weights" alone is not a defect, but their *size* is the
  extrapolation measure.
- The augmented estimate repairs imperfect pre-fit; it does not repair a
  donor pool missing the treated unit's support — check the convex-hull
  question before crediting augmentation.
- Review rule: report the SCM pre-fit (pre-RMSPE) and the augmentation's
  implied bias correction beside the headline gap; if the correction is
  large relative to the gap, the headline is the outcome model, not the
  weights.

## 6. Conformal inference — CWZ 2021

CWZ (abstract, §§2–3): a conformal/permutation inference procedure with
model-free validity — the validity holds under weak, verifiable
conditions and is robust to estimator misspecification; it accommodates
modern high-dimensional SC-type estimators and constructs per-period
effect intervals by test inversion. (`scpi` is a different object:
Cattaneo–Feng–Palomba–Titiunik prediction intervals for the synthetic
counterfactual — `cattaneo_feng_titiunik_2021_sc_intervals.md`.) Use when the placebo grid is
coarse, the estimator is augmented/ML-flavored, or the exchangeability of
naive in-space placebos is doubtful.

## 7. SDID — Arkhangelsky et al. 2021

SDID (abstract, §§2–3) re-weights a TWFE regression twice: unit weights
that make the weighted donor average track the treated pre-path (SC-like),
and time weights that balance pre-exposure periods (DiD-like), then runs
the doubly-weighted TWFE. It inherits DiD's tolerance for imperfect
pre-level fit (the intercept shift absorbs it) and SC's parallel-trends
relief (weights do the work). For the review: when a paper's SC pre-fit
is mediocre and a DiD alternative exists, SDID is the honest middle
estimator — its placebo/CI machinery (bootstrap/jackknife over the
relevant margin) replaces the RMSPE grid.

## 8. Reviewer checklist

- Pre-treatment fit reported (pre-RMSPE) and adequate *before* any
  post-treatment reading; poor pre-fit + an estimate = ADH's own
  disqualifier.
- Placebo inference specified: post/pre RMSPE ratio, fit screen applied
  to placebos, attainable-grid resolution stated, treated unit's rank
  reported against the screened grid.
- Predictor set audited for the all-lags pathology (Kaul et al.): if all
  outcome lags are predictors, the covariate list is decorative — flag.
- Specification discretion priced: the defensible spec set enumerated,
  estimates reported across it (Ferman et al.) — not one chosen spec.
- Estimator refit under ridge-augmented SC (BMF) with the implied bias
  correction reported; donor-pool support (convex hull) checked.
- Coarse grids or augmented/ML estimators → CWZ conformal or `scpi`
  prediction intervals as the inference, or SDID when the DiD margin is
  defensible.
