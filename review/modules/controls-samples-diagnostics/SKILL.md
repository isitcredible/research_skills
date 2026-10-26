---
name: controls-samples-diagnostics
description: >-
  Diagnostics for controls, samples, and denominators that define the
  estimand: mediator controls, control horse races, same-source covariates,
  covariate-by-period under fixed effects, treated shares from the
  regression sample, and denominator transportability. Invoke from
  `code-and-data` whenever a horse race, mediator, attribution claim,
  subset restriction, or same-source covariate touches a target result.
---

# Controls, samples, and denominators diagnostics

Establish what each control, sample restriction, and denominator does to
the estimand before reading any coefficient movement. Controls are treated
as free insurance, but a control can redefine the question *or inject bias
outright*: control for the mechanism and the effect "disappears"; control
for a variable built from the same source as the regressor and the two
fight over shared measurement error; restrict the sample and the claim
quietly becomes a claim about the subset; or add a control that is itself a
collider or a near-instrument and *manufacture* the bias it appears to
prevent (Cinelli, Forney & Pearl 2024). A coefficient drop can mean
confounding exposed — or the estimand changed mid-argument, or a bad
control was added; the checks below tell them apart.

Trigger: a control horse race, a mediator control, an aggregate attribution
claim, a subset restriction, covariates built from the same source as
the regressor, **a control the authors added to demonstrate robustness (a
kitchen-sink covariate set), a pre-treatment control claimed as safe, a
control or sample plausibly affected by the treatment or outcome,** or
**any discretionary specification choice not forced by
theory — a single-unit/small-group dummy, an ad-hoc interaction, a bespoke
sample carve-out, a hand-picked control, an unruled tuning constant — in
any target spec**. `NOT_APPLICABLE` when none of these touches a target result.

Method crib (interim — WP-audited):
`../../references/methods/goldsmithpinkham_hull_kolesar_2024_contamination.md` —
contamination bias under multiple treatments + controls; published AER
version pending.

## Core checks

- **Coefficient movement versus standard-error inflation.** Print before/after estimates, intervals, SEs, sample, and identifying variation; report changes in units (percentage changes only with a nonzero, meaningful denominator). A stable coefficient with a wider interval indicates reduced precision; a coefficient moving toward zero indicates attenuation in that specification. Neither pattern establishes whether the added control is valid. Check temporal and causal ordering, collider/mediator risks, changed estimands, and loss of identifying variation. VIF diagnoses linear dependence among regressors, not causal validity: low VIF cannot prove confounding or a zero causal effect. Interpret the result against the paper's actual claim and a substantively justified specification. Two naming requirements make the check answerable: for every contested control, name which catalog model the paper's causal structure implies (the Cinelli–Forney–Pearl crib's model number) — if the paper has no causal model, that absence is itself the finding — and name the reference specification against which movement is measured, with the reason; movement relative to an unnamed baseline supports opposite stories. When the paper's defense is coefficient stability across control sets, route to the OVB-sensitivity record (Cinelli–Hazlett robustness value benchmarked to named covariates, or Oster δ/Rmax) — "the coefficient was stable" alone is not a sensitivity analysis. And test whether the stability check could have detected anything: when the added controls are noisy proxies for the true confounder, attenuation makes coefficient invariance expected even under confounding — the more powerful test is the balancing regression (proxy on the left, treatment on the right), per `../../references/methods/pei_pischke_schwandt_2019_left_right.md`. A paper resting identification on RHS stability with poorly measured proxies has weak evidence, whatever the stability.

- **Mediator controls identified and removed.** A control that sits on the
  causal path from treatment to outcome answers a different question;
  re-estimate without it and report both numbers with the distinction
  stated. Before prescribing removal, ask whether the mediator is itself
  confounded (a treatment→mediator confounder or a mediator↔outcome
  confounder): then both the with- and without-control estimates are biased
  and the finding is "unidentified without stronger assumptions," not "the
  mediator inflated it."
- **Bad controls that inject bias — test by removal, watch the direction.**
  Beyond mediators, a control can *create* the bias it appears to remove.
  Re-estimate without each suspect control and report not just whether
  significance moves but *which way the point estimate moves*: movement toward the null or other anchors is sensitivity evidence, not proof the control was harmful. Establish control validity from the causal structure and provenance; the null and other estimates are not known truth.
  - **M-bias (pre-treatment collider).** Do not exempt a covariate because it
    is "pre-treatment." If it is a common effect of unobserved causes of both
    treatment and outcome, conditioning on it opens a back-door; test removal and interpret movement conditional on the proposed causal structure.
  - **Bias amplification (near-instrument).** Flag any covariate that predicts
    the treatment strongly but has no independent path to the outcome. Under
    residual confounding it amplifies existing bias; remove it and report the
    move.
  - **Selection / case-control (collider or descendant of the outcome).**
    Treat a post-outcome control, or a sample/frame selected on a variable
    the outcome affects, as a collider until shown otherwise — it induces a
    spurious association that no coefficient stability can dispel.
    Exception (crib Model 18 only — Z caused by Y alone): under a true null,
    the adjusted test of zero remains valid — the bias afflicts the point
    estimate and any non-null claim, not the null test. Not when the
    treatment also causes Z (Model 17, X → Z ← Y): there the null test is
    biased too.

  The 18-model classification behind these rows — including the
  counterexamples to "pre-treatment = safe" (M-bias, bias amplification)
  and "post-treatment = bad" (neutral Models 14–15) — is the verified crib
  `../../references/methods/cinelli_forney_pearl_2024_bad_controls.md`.
- **OLS estimand under effect heterogeneity — the coefficient is not the
  ATE.** When an OLS coefficient with controls is read as a causal *average*
  effect, check what OLS actually recovers once effects vary across units.
  Even with a correctly specified linear model and valid controls, OLS
  returns a *conditional-variance-weighted* average of the underlying
  effects (Angrist 1998; Aronow & Samii 2016 — weights (D − E[D|X])²,
  non-negative), and with a binary treatment its weights on the ATT and
  ATU lie in [0, 1] but can sit far from the population shares
  (Słoczyński 2022) — so it need not equal the ATE the prose claims. The
  weights go **negative** when E[D|X] is nonlinear in the included
  controls, or with multiple treatments (Goldsmith-Pinkham, Hull & Kolesár
  2024, below); then the coefficient can fall outside the range of every
  unit-level effect.
  This is an estimand problem, not a functional-form problem: it survives
  passing every `binstest`/`nprobust` linearity check.
  - **Action.** Recover the target average directly and report the gap:
    reweight to the covariate/treatment distribution (regression-adjusted
    `margins`, an explicitly weighted estimator, or an AIPW/doubly-robust
    estimator, which also survives if *either* the outcome or the
    propensity model is right) and compare it to the unweighted OLS
    coefficient. A coefficient that diverges materially from the reweighted
    ATE — or that rests on strata carrying negative weights — is answering a
    different question than the paper states; record it as an
    estimand-redefinition finding for `claims`.
  - For a two-way fixed-effects / staggered-DiD coefficient the same
    pathology is the negative-weighting (forbidden-comparison) problem —
    hand to `did-event-study-diagnostics` rather than re-deriving it here.
  - **Multi-treatment and interacted specifications:** contamination bias
    (Goldsmith-Pinkham, Hull & Kolesár 2024) — each coefficient picks up the
    other treatments' heterogeneous effects even with correct controls. In
    a horse race between treatments in one regression, re-estimate each arm
    in a separately-interacted specification that blocks cross-treatment
    leakage and compare.
- **Same-source covariates.** Check controls built from the same underlying
  source as the regressor for near-duplication and shared no-data
  artifacts; a horse race between two versions of the same measurement is
  not a horse race. Report the artifact: the (residualised) correlation
  between the two versions and a construction-provenance diff —
  near-duplication is shown, not asserted. The `code-and-data` data audit's hidden-input
  check is the same hazard upstream; cross-reference it.
- **Covariate-by-period under fixed effects** — where the claim requires a
  time-invariant covariate's effect to vary: entered flat under unit FE it
  is absorbed, and its "insignificance" is mechanical.
- **Treated shares computed from the regression sample**, not taken from
  the text — the paper's descriptive shares and the estimation sample's
  shares routinely differ, and magnitude calculations built on the wrong
  one inherit the error.
- **Denominator transportability** — for aggregate attribution claims:
  a share of a net quantity is defined only at the level whose net the claim
  names. Where unit-level signs differ, the share can exceed 100% and hides
  offsetting movements: report the per-unit sign distribution and the gross
  positive and negative contributions beside it, and read the share as a
  statement about the net, never about the units. "Transportable" means the share describes the same denominator
  population the claim is about; when composition differs, report gross
  positive and negative contributions separately rather than a share of a
  net quantity.

## Conditional checks

- **Author-included discretionary specification choices — interrogate the choice, do not reproduce it.** Any term or tuning the authors added that theory did not force — a single-unit/small-group dummy, an ad-hoc interaction, a bespoke sample carve-out, a hand-picked control, a tuning constant chosen without a stated rule — is a researcher degree of freedom, not standard furniture. Treat each as an object of suspicion and establish:
  - **What it is for.** State the mechanism it nominally serves, and whether the paper justifies it anywhere in prose; a stated justification is weighed here, not an exemption from the checks below. "Disclosed in a table note" is not a justification.
  - **Selection on the outcome.** Check whether the choice tracks *how the data behave* — how badly a unit fits, which window is significant — rather than a principle stated in advance. The general tell: an equally-defensible alternative choice was available and would not have helped the result.
  - **Symmetric application.** Is the same treatment applied to comparable cases on the other side, or only where it rescues the result? Swap the choice onto an equally-qualified alternative — move the dummy, shift the window, drop or re-center the interaction — and report whether significance moves. If inference depends on the choice, report specification sensitivity. Infer outcome-driven selection only with documentary or code evidence of the selection process; crossing a significance threshold alone does not establish it.
  - **Every column, especially the weakest.** Re-run without the choice, or under the alternative, in every spec it enters (OLS/GAM, IV/2SLS, mechanism, placebo) — not only the headline. Report where the choice matters, even if it is inert in the headline.
  - **Single-unit dummy.** In an otherwise unrestricted OLS regression, a dummy for one observation removes that observation's contribution to the slope normal equations. Examine both residual size and leverage, the stated reason, and comparable units; low leverage does not prove the dummy serves no purpose. Re-run the relevant specifications without it and report estimate and uncertainty changes. Check IV effects separately; do not transfer the OLS equivalence mechanically to every estimator or attribute motive from coefficient movement.

- **Saturated group-by-period fixed effects or an explicit sample
  restriction** in place of single-group dummies — when *you* need to ask
  whether one group drives the result, answer it as a design choice, not a
  dummy coefficient.
- **Efficiency ordering of valid controls** — when the authors lean on a
  precision claim ("adding controls tightens the estimate"). Among controls
  that are all valid (block back-doors, touch no causal path), those closer
  to the *outcome* improve precision while those closer to the *treatment*
  hurt it and risk amplification. Check whether their precision-buying
  control set is outcome-side (legitimate) or treatment-side (fragile).

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record
estimand-redefinition findings in the module report's `## Leads for later stages` (folded into the `code-and-data` report)
for `claims` explicitly: "controlling
for X changes the question" is a story-level finding, and the supportable
claim must be written for the question the surviving specification actually
answers.
