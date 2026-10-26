---
name: scale-sensitive-diagnostics
description: >-
  Diagnostics for scale-sensitive transforms and count outcomes: unit
  rescaling inside ln(1+x) and asinh, count models on the full sample, count
  versus per-capita specifications, unstable ratios, and placebos in the
  corrected specification. Invoke from `code-and-data` whenever ln(1+x),
  asinh, counts, per-capita scaling, or weak denominators carry a target
  result.
---

# Scale-sensitive diagnostics

Establish whether the transform is doing the identifying work. `ln(1+x)`
and asinh look like harmless ways to keep zeros in a log specification, but
they smuggle in a choice of units, and the estimate can move with that
choice: measure in dollars rather than thousands of dollars and the
"elasticity" changes. The theorem behind that move, what the rescaling
sweep measures, and the alternative estimands (Poisson percentage effect,
explicitly calibrated margins, Lee bounds) are in
`../../references/methods/chen_roth_2024_logs_with_zeros.md`. The exact
asinh elasticity formulas and the data rules papers cite but violate are in
`../../references/methods/bellemare_wichman_2020_ihs_elasticities.md`, and
the literature-wide non-robustness record plus the harmonized
alternatives (normalized estimands, quantile regression) are in
`../../references/methods/fitzgerald_etal_2026_loglike.md`. Once a corrected
specification becomes the honest baseline, hold the paper's placebos to it
too.

Trigger: `ln(1+x)`, asinh, a count outcome, per-capita scaling, a floor, or
a ratio over a weak denominator in the outcome or a load-bearing regressor.
`NOT_APPLICABLE` when no such transform is load-bearing.

## Core checks

- **Unit-rescaling sweep inside the transform.** Re-estimate with the
  variable in different units (×10, ×1000, per-thousand) inside the
  `ln(1+x)` or asinh — always alongside its mandatory companion on the same
  sample, the extensive-margin regression `1[Y>0] ~ D`. Interpret movement
  against its prediction (≈ extensive-margin effect × log a; the headline t
  converges to the extensive-margin t as the scale factor grows): movement
  equal to the prediction is the *expected* behavior of a nonzero extensive
  margin — the estimand conflates margins — and the prescription is Lee
  bounds on the intensive-margin effect under monotonicity (tight when the
  extensive margin is small, judged by its interval, not its p-value), not
  acceptance of the transform; drop zeros and take the ATE in logs only if
  the extensive effect is zero for every unit (Chen–Roth Remark 7).
  Reserve "the transform is doing the work" for movement that changes the substantive answer (calibrate against the crib's Table I
  magnitudes; the claim's own CI is the tolerance). For a transformed
  *regressor* the same sweep applies but the estimand is a units-sensitive
  semi-elasticity (Aihounton–Henningsen 2021; Thakral–Tô 2023), not the
  Chen–Roth ATE result — do not cite Chen–Roth for the regressor case; √X
  rescales cleanly.
- **asinh–asinh is a third case: the coefficient is not an elasticity.**
  When BOTH sides are log-like, β̂ approximates a log-log elasticity only
  where both inputs are large — the exact implied elasticity is
  β̂·[√(y²+1)/y]·[x/√(x²+1)] (Bellemare–Wichman 2020), which converges to
  β̂ only as x, y → large and diverges near zero, where the elasticity is
  undefined outright. A paper quoting an asinh–asinh coefficient as "the
  elasticity" without evaluating the formula has not reported an
  elasticity at all. Compute it at named evaluation points (mean AND
  median — the gap is often the finding), check the inputs against BW's
  own data rules (min nonzero |value| ≥ ~10; ≤ ~1/3 zeros), and run the
  rescaling sweep as a 2-D grid — both sides are units-sensitive, so the
  coefficient moves under rescaling of either variable.
- **The sweet-spot check (Fitzgerald et al. 2026).** The published unit
  scale is itself a researcher degree of freedom: in their 46-paper
  reanalysis 38% of estimates sit at a local |t| maximum — rescaling in
  either direction shrinks significance. So the sweep is a hypothesis
  test, not just a sensitivity display: report where the published scale
  sits on the |t|-vs-scale surface, and flag compliance failures with
  the data rules (99.8% of their estimates violate the min ≥ 10
  rule; 32% of transformed outcomes and 38% of exposures are non-positive
  in over a third of observations). The
  zeros-tolerant alternative that avoids the transform entirely is the
  **normalized estimand** — divide outcomes/treatments by a constant
  (unit mean, control-group mean, SD) so the answer is a percentage
  deviation with a scale-invariant coefficient and t-stat; use a
  dispersion normalizer where the mean can be negative. Quantile
  regression (Liu–Kaplan 2025) is the consistent intensive-margin route.
- **Count model on the full sample.** Estimate Poisson PML on the
  untransformed outcome — consistent for the conditional mean on any
  non-negative outcome, continuous included, not only counts — zeros
  included, and compare with the transformed specification and its implicit
  sample. Report e^β − 1 explicitly as θ_ATE%: a percentage of the *mean*,
  levels-weighted and potentially tail-dominated — not an average of
  individual percentages; θ_Avg% ("what a reader thinks an asinh
  coefficient is") is not point-identified even on strictly positive
  support. Run it both ways: where the paper headlines a
  *negative-binomial* count model, the load-bearing check is the same spec
  as full-sample Poisson PML (consistent for the conditional mean under
  weak assumptions — Gourieroux–Monfort–Trognon — while NB is efficient
  only under its own variance assumption and heavily down-weights
  high-count observations). NB significant + full-sample Poisson ≈ 0 (or
  sign-flipped) = the effect is concentrated in a specific count range —
  identify which before adjudicating, since Poisson's θ_ATE% is
  tail-dominated by construction (a few huge control units can carry the
  mean effect just as well as NB can down-weight it): check whether the
  authors' own "Poisson excl. outliers" needed a top-x% trim, list the
  largest-count units and their treatment status, and drop the top
  1/3/5/10% by hand — if Poisson barely moves it is the whole upper tail,
  not one defensible outlier.
- **Count versus per-capita** — where population scales the outcome: the
  two answer different questions, and the paper should be held to the one
  its claim needs. Run both on the same sample — the count spec with
  log-population as an exposure offset in PPML (the per-capita percentage
  effect without the ratio's denominator instability) beside the per-capita
  spec — and report side by side: the spec the claim needs is
  verdict-bearing, the other is the rebuttal.
- **Differences or probabilities in place of unstable ratios.** Ratios over
  small or noisy denominators explode; re-express the quantity as a
  difference or a probability and report whether the finding survives the
  re-expression. When the headline is "X is N× Y" and Y's sampling
  distribution straddles zero, the bootstrap ratio CI explodes and flips
  sign — report the difference (X − Y) and P(X > Y) instead, and separate
  genuine weak identification of the denominator from ill-conditioned fits.
- **Extensive/intensive decomposition is location-dependent.** A
  `dummy + ln(x)` split measures the zeros-vs-positives gap at the point
  where ln(·) = 0, which the units choice can push outside the data's
  support — the dummy's sign and significance both move with units.
  Unit-free objects only: the pure step (dummy alone), the within-positives
  ln(x) slope, and levels t-stats. Before citing any decomposition, locate
  the dummy and re-run at two other unit locations.
- **Placebos in the SAME corrected specification as the main effect.** When
  a corrected specification (count model, rescaled transform) becomes the
  honest baseline, the placebos and robustness checks must run in it too. A
  placebo that only ever ran in the fragile specification proves nothing
  about the corrected one.

## Conditional checks

- **Transform-dependent parallel trends** — when the transformed outcome
  feeds a DiD/event-study: parallel trends for asinh-of-dollars does not
  imply parallel trends for asinh-of-cents — flat pre-trends in one unit
  say nothing about another. Pre-trends must be re-examined in the
  corrected specification's units.
- **Recognize the defensive variants.** `log(c+Y)` with "robust to the
  choice of c" is a units-sensitivity check in disguise; rescaling so
  nonzeros are large (the Bellemare–Wichman defense) makes the units
  dependence *worse*, not better — recognize the backwards argument.
  Two-part/two-stage marginal effects are not the intensive-margin effect
  (they carry a selection term — Chen–Roth Online Appendix D, building on
  Angrist 2001, against Mullahy–Norton's recommendation of two-part
  models). asinh on an outcome that
  spans zero both ways is outside the count-model fix; the sweep is the
  instrument there.
- **The IV-count-model caveat (Jochmans 2022).** When the design is IV
  *and* the outcome needs the count-model fix, "PPML-IV with unit fixed
  effects" is not the clean alternative it looks: the pseudo-Poisson
  estimator's incidental-parameters immunity does NOT extend to its IV
  generalizations (Mullahy 1997; Windmeijer–Santos Silva 1997), whose
  FE versions are inconsistent under fixed-T and asymptotically biased
  in long panels without bias correction — the consistent short-panel
  route is a differencing estimator (Wooldridge/Windmeijer), a different
  object. Proposals and author specs alike carry this caveat; crib:
  `../../references/methods/jochmans_2022_iv_fe_count.md`.
- **Bootstrap-through-the-model** — when a headline quantity (long-run
  effect, net present value, aggregate contribution) is derived by pushing
  the estimate through further modeling: propagate the uncertainty through
  the whole pipeline instead of treating the downstream arithmetic as
  exact. For a tail-dominated integral (social cost of carbon, NPV,
  long-run multiplier) the headline is driven by the response's *decay
  shape*, not its level: a CI built by perturbing only the amplitude while
  holding shape parameters fixed understates the uncertainty badly.
  Re-estimate the full response on resampled data and refit ALL shape
  parameters per draw; and to combine two uncertainty sources use ONE
  bootstrap that propagates both — never add two ranges that each contain
  sampling variance. Watch for degenerate resampled fits (an ∞-horizon
  integral blows up on a few pathological draws): trim, report the count —
  frequent degeneracy is itself evidence of weak identification.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record
transform-dependence findings in the module report's `## Leads for later stages` (folded into the `code-and-data` report)
for `claims` in plain terms: "the effect
exists in log(1+x) of dollars but not thousands of dollars" is a sentence a
story either survives or does not.
