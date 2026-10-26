---
name: cross-sectional-diagnostics
description: >-
  Diagnostics for cross-sectional observational designs: functional form,
  common support, influence and leave-region-out, dependence structure
  including geography, negative controls, and omitted-variable-bias
  robustness values benchmarked against named covariates. Invoke from
  `code-and-data` for cross-sectional claims resting on a control set.
---

# Cross-sectional diagnostics

Measure how much the claim depends on choices the reader cannot see — which
controls, which functional form, which observations, which error structure —
and how much unobserved confounding it could absorb. A cross-sectional
regression with controls is the weakest design in the battery, so audit it
on the evidence's terms, not the paper's: the control set is itself a claim
to be tested, not a given.

Trigger: a cross-sectional observational claim among the target results.
`NOT_APPLICABLE` for results whose identification another module covers;
OLS columns the claim leans on stay in scope.

## Core checks

- **Functional form and common support.** Re-estimate under defensible
  alternative forms; check that treated and untreated observations overlap
  in covariate space, and report where the estimate comes from
  extrapolation. When support fails, route the answer: re-estimate on the
  supported region (trim or re-weight) and report whether the estimate
  survives on common support; an estimate carried by extrapolation is
  labelled descriptive, not verdict-bearing. Where a claim rests on an
  imposed shape (linearity,
  monotonicity), test it rather than eyeball a scatter: `binstest`
  (binscatter) formally rejects or clears the parametric form, and
  `nprobust`/`lpdensity` give a nonparametric conditional-mean or density
  alternative with valid inference — see the battery's software examples.
- **Influence and leave-region/group-out.** Cross-country and cross-region
  regressions are routinely carried by a continent or a handful of
  observations; report the full leave-out range. Leverage is a property of
  the functional form, not of the observation: reproduce the exact
  published column first, then run DFBETA/influence on *that* spec — the
  influential tail can sit at opposite ends under levels versus logs, and a
  "leverage" unit whose deletion *strengthens* the authors is a fragility
  story that self-destructs. Check the sign of `b_full − b_drop` before
  pitching the finding.
- **Dependence structure, including geography.** Neighbors resemble
  neighbors; unit-level robust errors on spatially smooth data fake
  precision. The gate has two tiers: for **every** spatially exposed result
  the SE-side record is Conley **and** Müller–Watson SCPC — a non-smooth
  regressor does not exempt it, because spatially correlated errors fake
  precision either way. When the regressor is *smooth or interpolated* over
  space, add the coefficient-side and noise rows: a spatial-lag/SLX refit,
  the Kelly matched-noise placebo, **and** Conley–Kelly–Kozbur
  pre-whitening — the "full spatial record" is all five rows. Conley only repairs the standard errors; SLX/SAR test
  whether the *point estimate* is spillover-inflated (in gap audits it has
  halved the own-unit coefficient while inference held). An SE-only pass
  that reports "spatial dependence doesn't overturn it" can hide a
  magnitude twice the honest value. In Stata, `scpc` aborts with
  `e(V_modelbased) missing` whenever the preceding regression omitted `robust`
  or `cluster()` (`e(V_modelbased)` is only stored under a sandwich VCE): never
  log `e(V_modelbased) missing` as "package failed / unavailable" — refit the
  levels regression with `robust`/`cluster()` and run `scpc`, and alongside it
  (or if levels SCPC fails on high-dimensional controls) run contrast-space SCPC
  (C-SCPC, the $h \to \infty$ benchmark) by applying `scpc` to the LBM-GLS
  transformed model from `spurtransform` (or in R via `spuR::spur` /
  `scpcR::scpc`). The audited space–time
  protocol behind the spatial record is
  `../../references/methods/spurious_space_time_unified_guide.md`.
- **Collapse test on the point estimate.** A cross-country or cross-region
  regressor is often one coarse value spread across many finer rows (a
  regional figure assigned to each country, a donor-substituted or
  interpolated value). Clustering the standard error does not touch the
  coefficient; collapse to the genuine independent units — average, or
  drop-to-source for donor/imputed values — and report whether the estimate
  moves. See `../../references/design-matrix.md`, "Collapse-test record".
- **Transparent covariate sensitivity.** Report how the estimate moves
  across the defensible control sets — not the paper's preferred ladder
  only, and with shrinkage distinguished from standard-error inflation when
  a control "kills" the result (see `controls-samples-diagnostics` when
  horse races or mediators are in play).
- **Negative controls** where substantively justified: an outcome or
  exposure the mechanism cannot touch, run in the same design.

## Conditional checks

- **Omitted-variable-bias robustness value** — when the causal claim rests
  on the control set. Compute the robustness value and the treatment's
  partial R², and benchmark against named observed covariates: the multiple
  of a named covariate's strength an unobserved confounder would need to
  overturn the claim (`sensemakr` implements this; the OVB-sensitivity
  record in the battery's `../../references/design-matrix.md` lists the fields).
  A robustness value near what a single named covariate already explains is
  a different finding from one no plausible confounder could reach — report
  which. The robustness value is NOT a verdict; it quantifies what the
  claim can absorb, not whether confounding exists.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record the selection-on-observables verdict and any geography-carries-it finding in the module report's `## Leads for later stages` (folded into the `code-and-data` report) for `claims` — a cross-sectional contrast that is really a
between-continent contrast is a story finding as much as a statistical one.
