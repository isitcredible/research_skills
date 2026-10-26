---
name: quantitative-model-diagnostics
description: >-
  Diagnostics for calibrated and quantitative-theory results — a headline
  number ("X explains 40% of Y") produced by solving or simulating a model.
  Inventories the free parameters, sweeps the calibration over defensible
  ranges, tests fit on non-targeted moments, and checks the code solves the
  model the text describes. Invoke from `code-and-data` whenever a load-
  bearing magnitude comes out of a calibrated/simulated model. The fragility
  sweep, applied to a model instead of a regression.
---

# Quantitative-model diagnostics

A calibrated model is a machine for turning parameter choices into a headline
number. Some of those parameters are pinned to external evidence; some are set
inside the model to hit chosen targets; some are simply assumed. The result's
credibility is the credibility of those choices — and a number that holds only
at a knife-edge value, or that its own model reproduces only because it was
built to, is fragile in exactly the way a coefficient that lives in one
influential region is fragile. This module puts that fragility on the record.

Trigger: any target result whose magnitude is produced by solving, simulating,
or calibrating a model — a quantitative-theory exercise, a structural
decomposition, a "our model accounts for X%" claim, the quantitative section of
a hybrid theory paper. `NOT_APPLICABLE` when no load-bearing number comes out of
a model; say so and name the estimates instead.

Boundaries. Where the model is proved as well as calibrated, this module runs
**alongside** `theory-diagnostics` (it audits the numbers; that module audits
the proof). Where structural parameters are *estimated* on data with standard
errors (GMM/SMM/MLE), the empirical inference and identification checks still
apply through the ordinary battery. Where the model is fitted to **trending
aggregates over time**, `time-series-diagnostics` fires too — minimizing fit residuals does not guarantee stationarity; fitted-residual tests need reference distributions that account for estimation and selection, and in-sample fit alone is not evidence
of fit.

Method crib (source-audited):
`../../references/methods/andrews_gentzkow_shapiro_2017_moment_sensitivity.md` —
the Λ sensitivity matrix: which data moments each estimated parameter
loads on, at negligible cost. A structural estimate whose headline loads
on a few disputed moments is fragile in a way no standard error shows;
a model that cannot report its moment loadings asks the reader to take
identification on faith. This is the structural analogue of Rotemberg
weights — name the load-bearing moments, then check them.

## Discipline — a fragility claim is a re-run, never an assertion

Every number here traces to a script and a log in the job tree, re-run clean
before it is reported (the battery's reproducibility rule is not waived for a
model). You may not call a result knife-edge, or a moment mismatched, from
reading the calibration table. Run the sweep, pull the range from the output,
and report it. Equally: if the headline survives every defensible perturbation,
report that it survived — a robust quantitative result is a strong one, and a
manufactured failure is a failed check.

## Core checks — run for every model-produced target

- **Free-parameter inventory, with anchor provenance.** For every parameter,
  record: its value, its source (externally calibrated to a cited estimate /
  internally set to match a stated target / assumed with no external anchor),
  whether the headline result depends on it, and the status of its anchor.
  An external citation must measure the SAME quantity under the same
  definition — same horizon, population, units; a micro elasticity anchoring
  a macro parameter is the classic mismatch, and a mismatched anchor is a
  named finding, not a citation. An anchor the battery or the data audit has
  impeached demotes every parameter resting on it to "assumed with no
  anchor": bar "the model matches its targets" language until the internal
  block is re-solved at the target's defensible interval, and an impeached
  *untargeted* moment cannot count as overfit evidence either. The
  assumed-with-no-anchor parameters are where the result is most exposed;
  name them explicitly. A parameter "disciplined by the data" that is
  actually free to hit the target is an internal one mislabelled.
- **Calibration-sensitivity sweep.** Perturb each load-bearing parameter across
  its *defensible* range — the spread of estimates in the literature, not only
  what the paper cites, or
  plausible bounds where none is cited — and report the headline quantity's
  range, one parameter at a time and then jointly across the parameters the
  result is most sensitive to. State the result in the paper's own units ("the
  40% share ranges 18%–71% across defensible calibrations"). A number that
  collapses off a single point is the finding. State the sweep convention:
  externally-calibrated parameters are swept with the internal block
  re-matched to targets, or explicitly held fixed — say which, since holding
  the block fixed conflates parameter sensitivity with mechanical
  target-breaking. For internally-set parameters report target-uncertainty
  propagation: re-solve for the parameter at the target's interval
  endpoints. Report the **breaking set**, not just the range — the parameter
  values at which the claim fails and whether the defensible range
  intersects it ("breaks only outside the defensible range" vs "breaks
  inside it"). Count solver outcomes: N-solved/N-attempted per sweep arm — silently
  dropped no-solution cells manufacture robustness, no-solution cells
  counted as movement manufacture a kill, and under equilibrium
  multiplicity state which branch the sweep rides. Before a "robust"
  verdict, screen interactions over the parameters the headline depends on
  (a two-way grid over the top-k at minimum): a fragility living in a
  two-parameter interaction escapes the one-at-a-time sweep.
- **Targeted vs non-targeted moments.** A model fit to match a set of moments
  matches them *by construction* — that is not evidence. Its test is the moments
  it did **not** target: list the calibration targets, then report the model's
  fit against untargeted moments the data can supply. A model that nails its
  targets and misses everything else is over-fit, not validated.
- **Mechanism attribution.** Decompose the headline number into the channels or
  parameters that drive it (shut each mechanism off in turn; report how much of
  the result each accounts for). This is the model analog of the variance-share
  question — which part of the machine produces the answer — and it routinely
  disagrees with the paper's narrative about *why* the number is what it is.
  In nonlinear models the shut-off shares need not sum: report the sum and
  the interaction residual — a "60% channel A" from a decomposition that does
  not reconcile is not a share. And check the headline is falsifiable by the
  model at all: a structural decomposition that is an accounting identity
  cannot fail, and reporting it as a model success promotes an unfalsifiable
  statistic — record in the inventory whether the headline is an identity or
  a model-determined quantity. Where the model is *estimated* (GMM/SMM/MLE)
  rather than purely calibrated, the formal version of this check is the
  Λ sensitivity matrix — which data moments each parameter loads on — which
  the AGS crib shows reduces to the OVB formula in the orthogonality case;
  a headline carried by moments the paper does not defend is the finding.
- **Solve-the-stated-model check.** Confirm the code implements the model the
  text describes — the same equations, parameter values, calibration targets,
  and closure. Read the solver as the empirical battery reads an estimation
  script: the gap between the written model and the solved one is where the
  result can live. Check the numerical solution is actually a solution at the
  calibrated point (solver convergence, Euler-equation or residual errors, grid/
  discretization sensitivity) and, where the claim needs it, equilibrium
  existence and uniqueness there. For nonlinear models check the solution
  *method*, not only the discretization — a headline from a first-order
  perturbation solve can be an artifact of the approximation; re-solve at a
  higher order or globally where feasible.
- **Parameter identification.** For each internally-calibrated parameter,
  check the target actually pins it down — does the objective or target
  moment respond to it? A flat direction means the calibrated value is
  arbitrary among near-minima and the headline sits on an unidentified
  point while matching every target: a finding in its own right, which the
  defensible-range sweep cannot reveal. For *estimated* structural
  parameters (GMM/SMM/MLE) weak identification is owned here — report
  objective curvature and identification-robust confidence sets; no
  empirical module covers it.

## Conditional checks — run when the trigger is present

- **Closure / functional-form sensitivity** — when the paper's functional form
  or market-structure assumption is a choice theory did not force (CES vs
  Cobb–Douglas, a particular utility or matching function, a specific closure).
  Re-solve under a defensible alternative and report whether the headline
  survives. If the result tracks *which* form was chosen, the form is doing the
  work.
- **Bootstrap-through-the-model** — when a headline is a long-run,
  net-present-value, or welfare quantity obtained by pushing an estimate
  through further model machinery: propagate the estimate's own uncertainty
  through the model to a band on the final number, rather than reporting a point.
- **External / out-of-sample implication** — when the model implies something
  checkable outside its calibration sample (another period, another country, a
  held-out moment): confront it and report the result.
- **Prior-informativeness ratio** — when parameters are estimated by Bayesian
  machinery: for each key parameter compare the posterior SD to the prior SD,
  and the posterior-mean displacement (|posterior − prior mean| relative to
  prior SD). Read the SD ratio as bands: near 1 = prior-dominated (the data
  did not move the uncertainty), intermediate = partially informative, small
  = data-dominated — a flat "~0.1 flags the prior" threshold flags nearly
  everything and mislabels a 5× uncertainty reduction as data silence. Run a
  prior-sensitivity check on each flagged parameter and report how much of
  the headline survives a defensible alternative prior.
- **Simulation-selection in the paper's own evidence** — when the paper's case
  includes its own Monte Carlo or simulation results: the DGPs displayed are
  author-chosen. Ask which parameter regions, failure modes, or alternative
  DGPs were *not* shown — a validation covering only the DGPs where the method
  works is a selected set. Construct or request the adversarial case the paper
  omitted and report whether the method survives it.

## Report back

Emit `quantitative-model-diagnostics-REPORT.md`. Lead with what the sweep did to
the headline number and what the non-targeted moments show — the range and the
fit, not a row per parameter. For each check record the saved script path, the
parameter grid or alternative used, and the numbers pulled from its log.
Account for coverage: the free-parameter inventory in full, what was
`NOT_APPLICABLE` and why, what was blocked (exact file, command, error). Hand
the sensitivity range and any over-fit or knife-edge finding to the module report
and to `claims` as it appears — how wide the defensible range is bears
directly on how strong a claim the number can carry.
