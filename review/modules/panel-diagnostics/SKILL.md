---
name: panel-diagnostics
description: >-
  Diagnostics for panel designs without a discrete treatment event: unit and
  time dependence, serial-correlation-robust inference, fixed-effect
  structure sensitivity, balance and attrition, and group-level leave-outs.
  Invoke from `code-and-data` for panel variation that is not an
  adoption-event design.
---

# Panel diagnostics

Establish what variation actually identifies the coefficient once the fixed
effects have taken their share, whether the error structure supports the
reported precision, and which units supply the identification. A panel
regression borrows its credibility from the fixed effects, and the fixed
effects decide what variation is left — the estimate is only as good as the
answer to "what varies, for whom, after all this is absorbed?"

Trigger: panel variation among the target results with no discrete
treatment event — otherwise use `did-event-study-diagnostics`.

Method crib (source-audited):
`../../references/methods/panel_methods_guide.md` — multiway/nested
clustering geometry, D-K, Pesaran CD→CCE/interactive-FE routing, Mundlak
margin contrast, Nickell bias and AB diagnostics, G-H attenuation, Lee
bounds.
`../../references/methods/abadie_athey_imbens_wooldridge_2023_clustering.md` —
the *whether*-to-cluster frame this guide's *how* presumes: clustering is
a design problem (two-stage sampling or cluster-level assignment), not a
residual-correlation test. When the panel holds nearly all clusters (all
states, all years), conventional clustered SEs are inflated by the missing
finite-population correction only if effects are heterogeneous across
clusters and assignment varies within them; with cluster-level
assignment, cluster at the assignment level.

## Core checks

- **Unit and time dependence — located, then remedied.** Identify how errors
  correlate within units over time and across units within periods; cluster
  at the level the dependence lives, and report the cluster count. Then
  remedy by location: within-unit-over-time → unit clustering plus a
  persistence measurement (below); across-units-within-period → a Pesaran CD
  diagnostic first, then two-way clustering (Cameron–Gelbach–Miller) or
  Driscoll–Kraay (needs a long T, ≥ ~20–30) for common shocks uncorrelated with the
  regressor. If exposure to a common
  factor plausibly correlates with the regressor, the dependence biases the
  *coefficient*, not just the SE — run a CCE (Pesaran) or interactive-FE
  (Bai; needs both N and T large) specification and report the movement as
  a point-estimate finding.
  A single `vce(cluster unit)` answers only the first location.
- **Collapse test on the point estimate.** Clustering repairs the standard
  error, not the coefficient. Where a regressor is constant within a coarser
  unit than its rows (an aggregate variable on micro units, coarse-resolution
  coding), distinguish the two cases before calling anything wrong: genuine
  rows with a coarse regressor — the estimand-preserving collapse (original
  weights/controls retained) typically reproduces the coefficient exactly,
  and equal-weight re-estimation is a *named sensitivity with a different
  estimand*, not a correction (but a large gap undercuts a common-effect claim, and
  with high residual intraclass correlation the equal-weight fit is the more
  precise one); versus donor-substituted/imputed copies,
  where drop-to-source IS the correction. See
  `../../references/design-matrix.md`, "Collapse-test record".
- **Serial-correlation-robust inference.** Measure the persistence first —
  residual and regressor AR within units — then report inference under at
  least one method whose validity does not ride on low persistence (block/
  time-clustered bootstrap, or the time-aggregated / long-differences
  specification) beside the clustered baseline. If the corrected interval
  loses significance, route through the MDE machinery rather than reporting
  "no effect"; if no validated correction exists at this persistence, report
  "uninformative at this T/ρ," not a discounted pass.
- **Dynamics (lagged dependent variable).** A within estimator with a lagged
  outcome carries Nickell bias — O(1/T), downward on the persistence coefficient,
  whatever N is. At short T, report it beside a difference- or system-GMM
  estimate whose output carries m1/m2, Sargan/Hansen and the (collapsed)
  instrument count; flag system GMM when the persistence coefficient is near 1.
- **Continuous treatment with no stayers** (temperature, rainfall, prices:
  every unit's treatment changes each period). There is no untreated
  comparison, so TWFE imposes a linear, homogeneous effect; identification
  rests on quasi-stayers, units whose treatment barely moves
  (de Chaisemartin–D'Haultfœuille–Vazquez-Bare 2024, AEA P&P). Their
  nonparametric estimator converges at n^(2/5), not √n, and placebo
  pre-tests are weak; their parametric two-step estimator is √n. Report it
  beside the TWFE coefficient (in Deschênes–Greenstone's 1997–2002 county
  data, −0.024, s.e. 0.007, becomes −0.018, s.e. 0.011).
- **Fixed-effect structure sensitivity — adjudicate the margin.** Re-
  estimate across defensible FE structures (unit, time, unit and time,
  region-by-period where the claim allows it) and report the coefficient
  path across them. Before reading the path, state which variation margin
  the claim requires — within-unit change, between-unit levels, or
  within-region-period — with the reason; estimates on other margins are
  rebuttals of the paper's framing, not verdicts on the claim. Run the
  Mundlak / correlated-random-effects between-vs-within contrast:
  disagreement between the margins is itself a finding (they answer
  different questions), so name which one the paper's prose invokes. And
  check the attenuation direction: where the regressor is smooth,
  interpolated, or constructed, report its within-vs-total variance share
  and the between estimate beside the within — if the within-variation is
  mostly noise, the FE estimate is the *attenuated* one and the usual
  credibility ordering inverts (Griliches–Hausman). A result that exists
  only under one FE structure is a finding about that structure.
  State what identifying variation remains under each — a two-way FE
  estimate identified off three switching units is a small-N design wearing
  a large-N panel's clothes; hand that to `small-n-diagnostics`.
- **Balance, attrition, and timing paths.** Who enters and exits the panel,
  and whether entry and exit correlate with the regressor of interest **and
  with the outcome**. Outcome-correlated or post-treatment exit is
  selection — report it, and bound or reweight where feasible (Lee bounds
  need a randomly or as-if randomly assigned binary treatment and monotone
  selection, and bound the effect for the always-observed; IPW). Only where
  neither is feasible — say why — quote the within estimate with the exit
  pattern stated.
- **Unit and group leave-outs.** Leave out each unit and each natural group
  (region, industry, cohort); report the full coefficient range.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record the what-variation-identifies-this answer in the module report's `## Leads for later stages` (folded into the `code-and-data` report) for `claims`: the FE structure
defines the comparison the story is allowed to claim, and a story told about
levels when the estimate is within-unit change is a framing gap.
