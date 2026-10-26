---
name: synthetic-control-diagnostics
description: >-
  Diagnostics for synthetic control and synthetic difference-in-differences:
  pre-period adequacy, placebo-unit rank, weight diagnostics including
  lagged-outcome degeneracy, terminal-period sensitivity, and in-time
  placebos. Invoke from `code-and-data` whenever a target result uses a
  synthetic comparison unit.
---

# Synthetic-control diagnostics

Ask how the fit was achieved, how the treated unit ranks against placebos,
and whether the gap survives the choice of endpoint. A synthetic control is
only as good as its donor weights, and the weights can be manufactured:
match on enough lagged outcomes and the fit becomes mechanical while the
covariates become decoration — so a tight pre-period fit is where the
questions start, not where they end.

Trigger: a synthetic control or synthetic difference-in-differences
comparison behind any target result. `NOT_APPLICABLE` otherwise.

Method crib (source-audited):
`../../references/methods/synthetic_control_guide.md` — Abadie-Diamond-Hainmueller fit/placebo
machinery, Ferman spec-search accounting, Kaul all-lags pathology, BMF
augmentation, CWZ conformal, `scpi` prediction intervals, SDID.
`../../references/methods/cattaneo_feng_titiunik_2021_sc_intervals.md` —
JASA: conditional prediction intervals on the counterfactual itself.
The permutation rank test answers "is this gap unusual among placebos?",
not "what is the CI on the effect?". The CFT interval is around the
synthetic counterfactual: the test is whether it contains the treated
unit's observed outcome. A tight rank p with a treated outcome inside the
interval means the effect is not distinguishable from prediction error under
CFT's assumptions — a test under rule 8 (report its power), not a correction; a
wide interval that still excludes the treated outcome is not. Report the interval alongside the
rank.

## Core checks

- **Pre-period adequacy — and route the answer.** Is the pre-treatment
  window long enough to discipline the fit and support the chosen inference
  procedure? A short pre-period plus many donors is a recipe for overfitting
  the fit and underpowering the test. When T0 is short relative to the donor
  count or the post-period, a tight pre-fit is manufactured evidence: require
  a penalized/augmented estimator and report the placebo grid's resolution
  limit; when T0 is adequate, unlock the in-time placebo and the pre-period
  holdout below. State the rule you applied.
- **Placebo-unit distribution and rank.** Run the full procedure on every
  donor as if it were treated; report where the treated unit's effect ranks
  in that distribution. Specify the statistic: the canonical ranking is the
  **post/pre RMSPE ratio** (Abadie–Diamond–Hainmueller), not the raw gap —
  donors with poor pre-fit produce large mechanical gaps and contaminate the
  null. Screen the pool: state the treated unit's own pre-RMSPE and exclude
  placebos whose pre-RMSPE exceeds a stated multiple of it. Then report J
  and the smallest attainable p — the grid is 1/(J+1), and when that exceeds
  α the test cannot reject and the record is "resolution-limited,
  uninformative," not a null; symmetrically, a grid-minimum rank is not a
  clean p-value. The rank is the design-based test — a treated effect
  inside the screened placebo distribution is no evidence of an effect
  however dramatic the gap plot looks; read it beside the conformal and
  `scpi` intervals below.
- **Weight diagnostics.** Report the donor weights: sparse, extreme, or
  degenerate weights mean the "synthetic" unit is really one or two donors,
  and the design inherits their idiosyncrasies. Then check those donors for
  their own shocks in the treatment period, run a donor leave-one-out refit
  (drop each positive-weight donor, report the gap range), and screen the
  *placebo pool* for donors that received similar interventions — a
  contaminated placebo pool shrinks the apparent rank.
- **Terminal-period sensitivity.** Recompute the effect dropping the final
  periods; divergence that lives at the end of the sample is fragile to it.
- **Alternative-estimator refit.** Re-fit the headline gap under augmented
  SC (Ben-Michael–Feller–Rothstein — the standard repair for imperfect
  pre-fit), SDID, and/or generalized SC; report whether the gap survives the
  estimator, not just the donor set.
- **Conformal inference.** Chernozhukov–Wüthrich–Zhu conformal intervals are
  the second design-based inference route beside the placebo rank and
  `scpi`; where the placebo grid is coarse, conformal is often the
  higher-resolution test.
- **Model-based prediction intervals (`scpi`).** The placebo rank is one
  inference route; `scpi` (Cattaneo–Feng–Palomba–Titiunik) is a second,
  independent one — it puts a prediction interval around the synthetic
  counterfactual that carries the estimator's own in-sample and out-of-sample
  uncertainty. Report it beside the placebo rank: a gap that ranks extreme
  among placebos while the treated outcome sits inside the counterfactual's
  `scpi` interval is not the clean effect the gap plot implies; a treated
  outcome outside a wide interval is still outside it.
  Re-run under alternative weight constraints (simplex, lasso, ridge, ols) and
  report whether the gap survives the constraint. (`scpi` implements this — data
  prep, `scest`, `scpi`, `scplot`; see the battery's software examples.)

## Conditional checks

- **Lagged-outcome degeneracy** — when lagged outcomes enter the matching
  variables: check whether they collapse the weights onto the outcome path,
  making the fit mechanical and the covariate matching irrelevant. Report
  the fit with and without the saturated lag set. This is a proved
  pathology, not a suspicion: Kaul, Klößner, Pfeifer & Schieler (2022,
  *JBES*) prove that when every pre-period outcome enters as a separate
  predictor, every other covariate is rendered irrelevant to the weights,
  however much it matters for the post-period — so a paper that "matches on
  covariates X, Y, Z and lagged outcomes" is usually doing lagged-outcome
  matching with the covariates as decoration. Read the V-weights table:
  structural covariates at 0.000–0.01 with a few lag years at 0.4+ is the
  signature. Ferman, Pinto & Possebom (2020) are routinely mis-cited: their
  position is a fork — use *fewer* lags if covariates should do work, all
  lags if they needn't — plus multiple specifications and combined test
  statistics (Imbens–Rubin), not "one alternative spec." Fixes: match on
  structural covariates only, set V exogenously, cross-validate V (Abadie et
  al.'s own recommendation), or use a method without the pathology (SDID,
  penalised SC, matrix completion).
- **SDID needs a large pre-period for its inference.** Synthetic DiD is not
  SC — the ridge penalty, time weights, and jackknife inference rest on
  T0 → ∞ (pre-periods). With single-digit T0 the weights are underdetermined,
  the "flat pre-trends" are partly an overfitting artifact, and the
  large-N_co, large-T0 conditions behind all three variance estimators are
  not in force — the bootstrap (re-estimates the weights), the jackknife
  (fixes them; conservative only under those conditions, undefined at one
  treated unit) and the placebo estimator (the one-treated-unit route,
  which needs homoskedasticity across units). Count the pre-periods before
  accepting an SDID's inference; a placebo treatment date inside the pre-window converts
  the caveat into demonstrated instability on their numbers. But do not lead
  a critique with it when a coincident-shock or identification argument is
  available — overfitting is orthogonal to a shock with no pre-period
  footprint, and leading with it implicitly concedes a better-powered SDID
  would identify the effect.
- **In-time (backdated) placebo** — when the pre-period allows it: assign a
  fake treatment date inside the pre-period and confirm the procedure finds
  nothing.
- **Pre-period holdout** — the direct test of mechanical fit: reserve part
  of the pre-period, re-estimate the weights on the training portion only,
  and check whether the fitted unit tracks the held-out pre-periods. Weights
  that fail to extrapolate within the pre-period were fit, not found.
- **Staggered adoption or multiple treated units** — use `scdataMulti`
  (`scpi`); pooled and unit-level results are different objects.
- **SDID time-weight concentration** — for SDID targets, report the
  concentration of the time weights λ across pre-periods beside the donor
  weights, and re-estimate the SDID claim under plain DiD and SC as
  sensitivities.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record donor-composition findings in the module report's `## Leads for later stages` (folded into the `code-and-data` report) for `claims`: when the synthetic unit is really one donor
economy, the counterfactual claim is a comparison with that economy, and the
story must survive being said that way.
