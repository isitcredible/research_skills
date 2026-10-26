---
name: experiment-diagnostics
description: >-
  Diagnostics for randomized experiments: assignment integrity, attrition
  and missingness, intent-to-treat estimation, prespecified outcome families
  with multiplicity control, randomization inference, and noncompliance
  handling. Invoke from `code-and-data` whenever a target result rests on
  randomized assignment.
---

# Experiment diagnostics

Randomization buys identification at baseline and nothing after it. Check
everything that happens after: attrition, noncompliance, outcome
multiplicity, and analysis-unit mismatches can each quietly rebuild the
selection problems randomization removed, and each has its own test.

Trigger: randomized assignment behind any target result. `NOT_APPLICABLE`
for observational designs.

Method cribs (source-audited):
`../../references/methods/young_2019_channelling_fisher.md` and
`../../references/methods/morgan_rubin_2012_rerandomization.md` —
restricted-assignment-set RI; a screened/rerandomized design analyzed
with pure-randomization theory gets conservative inference (safe
direction, but still the wrong distribution).

## Core checks

- **Assignment and analysis-unit match.** Randomized at the clinic,
  analyzed at the patient, is a clustering error; inference belongs at the
  level of assignment, with the cluster count reported. The whether-to-
  cluster decision is a *design* question, not a residual-correlation test
  (`../../references/methods/abadie_athey_imbens_wooldridge_2023_clustering.md`):
  cluster-level assignment is what forces the cluster adjustment, and in a
  fully unit-randomized trial clustering the SEs is a costly choice, not a
  default — check which variance component the design actually carries.
- **Collapse to the assignment unit (point estimate).** The unit-match check
  fixes inference; when treatment is assigned at a coarser level than the
  analysis rows, also collapse to one row per assigned unit (average the
  replicate subsamples) and confirm the coefficient itself, not only its
  interval, is read at that resolution. See `../../references/design-matrix.md`,
  "Collapse-test record".
- **Assignment integrity.** Balance on predetermined covariates, and the
  randomization procedure as actually implemented — batch, stratified,
  re-randomized — reflected in the analysis.
- **Post-treatment conditioning.** Check whether the headline spec controls
  for, or subsets on, a post-randomization variable (a mediator, an
  endogenous screen, an adjustment set chosen on results). An experiment
  re-imports bias exactly here; where present, hand to
  `controls-samples-diagnostics` with the model named.
- **Attrition and missingness.** Overall and differential by arm; when the
  differential is non-trivial (say, the arms' attrition rates differ beyond
  a stated tolerance, or attrition correlates with baseline outcomes), run
  Lee bounds or a stated worst-case analysis. A differential that is not
  statistically significant is not clearance: the bounds show whether it
  matters beside the effect. Attrition is the experiment's selection
  problem readmitted through the back door.
- **Intent-to-treat estimate.** The ITT is the design's protected quantity;
  report it before any per-protocol or treatment-on-treated number.
- **Prespecified outcome family and multiplicity adjustment.** Compare the
  outcomes reported against the outcomes collected (registry, pre-analysis
  plan, survey instrument), define the family from the claim structure, and
  adjust. An experiment with twenty outcomes and one star is the
  multiplicity failure in its purest form. Where a pre-analysis plan or
  registry entry exists, cite `../../references/methods/olken_2015_preanalysis.md`
  for the credibility limits of pre-registration; where the multiplicity is
  visible only in the paper's own spec table, report the pile-up of
  p-values just below the threshold descriptively — correlated specifications
  cluster around the baseline by construction, so the pile-up is not by itself
  evidence of search; price it with the specification sweep — and do not run the p-curve
  tests of `../../references/methods/elliott_kudrin_wuthrich_2022_phacking.md`
  on one paper's table: they are across-study tests. (Humps at cutoffs are
  what non-increasingness tests detect; the "no power" case is p-hacking
  that shifts mass left without humps, which the paper's bounds tests
  target.)
- **Randomization inference** where feasible — the design's own exact test,
  using the actual assignment mechanism. Name the permuted statistic: the
  t-statistic permutation under the true mechanism is the standard object
  (Young's randomization-t). Coefficient permutations (the
  randomization-c) test the same sharp null, but prefer the -t: it stays
  exact in joint tests and robust under heterogeneous effects, where the
  -c does not (Young 2019, §III.B).
  The permutation must respect the mechanism — permute within strata for a
  stratified design, condition on the re-randomization criterion where the
  design used one — or the RI p-value is invalid. Permuting arm *labels* while
  leaving arm-*derived* columns (treatment dummies, control flags, cell
  memberships) at their observed values is not a permutation of the
  assignment — it permutes only the margins whose columns are actually
  re-derived, and an "invariance" or degeneracy rate measured under it is a
  harness artifact. Re-derive every assignment-descended column from the
  permuted labels, and validate the generator before trusting it: rebuilding
  from the *observed* labels must reproduce the shipped columns exactly.
  The per-coefficient test
  inherits the omnibus caveat: it is a sharp-null test. Where RI is
  infeasible, record why and what was run instead. A degenerate or invariant
  direct statistic is NOT infeasibility — when the natural statistic is
  mechanically invariant under valid permutations (a pooled or selected cell
  whose membership barely moves), the obligation is to construct the
  instrument that is informative: typically re-running the full
  selection/estimation pipeline on each permutation and taking the selected
  estimate as the test statistic. "Untestable" may be recorded only after a
  feasible alternative instrument has been named and ruled out; an
  identified-but-unrun feasible instrument is an unfinished required check,
  which the status rules do not allow to stand under COMPLETE. Robust and
  cluster-robust
  standard errors were biased *downward* in Young's sample of AEA
  experiments — in other designs small-G cluster-robust SEs can be biased
  upward (the few-cluster record applies); RI is the honest benchmark, and
  where a starred coefficient survives conventional SEs but not its own
  permutation test, the star is a
  finite-sample artifact.
- **Omnibus joint-null test (the experiment-wide test, not the starred
  column).** Before crediting any single significant coefficient, test the
  sharp null that treatment affected *no* outcome at all — jointly, across
  the treatment×outcome coefficients in the family the claim draws on (the
  prespecified family containing the claimed outcome, else every outcome
  collected — registry, survey instrument — so selective reporting cannot
  shrink the family) — by randomization
  inference on a joint statistic. This is the test individual stars are
  selected to survive and the experiment as a whole often cannot: Young
  (2019, QJE) re-tested 53 AEA-journal experiments with their designs' own
  randomization inference and found joint tests of the treatment effects
  reported together in a table produced 33–49% fewer significant results
  than conventional inference (49% at .01, 33% at .05; individual tests
  13–22%). A paper-wide omnibus result and the 30–40% headline appear only
  in the superseded working paper — do not cite them. If the
  omnibus null cannot be rejected, say so first — it subordinates every
  per-outcome result. Pair this with the leverage diagnostic (the battery's leave-one-out/influence check): a
  joint result carried by one or two high-leverage observations has a far
  smaller effective sample than its nominal *n*.

## Conditional checks

- **Balance tests get the null backwards by default.** A baseline-covariate
  balance table that reports "no significant differences" is using the
  wrong null — non-rejection of "no difference" is weak evidence for
  balance, especially underpowered. The correct structure is equivalence
  testing: H0 is "imbalance ≥ ε" for a substantively stated bound, and the
  burden is on the paper to *reject* it (TOST or CI-in-region). Record any
  "balanced (p > 0.1)" claim as untested, not confirmed. Crib:
  `../../references/methods/eggers_tunon_dafoe_2024_placebo_tests.md`
  (Hartman–Hidalgo equivalence section). The same crib covers placebo-test
  typology for in-time/outcome placebos run inside the experiment.
- **Noncompliance** — when take-up differs from assignment: report take-up
  by arm and estimate treatment-on-treated with assignment as the
  instrument, alongside the ITT, never instead of it.
- **Interference and spillovers** — when treatment can cross units through
  markets, networks, or shared locations: the stable-unit assumption is a
  claim, not a given; test it where the design allows.
- **Design-stage forking paths** — when conditions, stimuli, instructions,
  or exclusion rules could have been tuned after piloting: iterated
  piloting conditional on results is a selection process in the *design*,
  not the analysis — the published experiment is then a replication of a
  selected pilot, and its "confirmation" is partly an artifact of the
  search. Check (i) condition scripts and instructions for asymmetry — does
  one arm's wording prime the predicted response; (ii) exclusion and
  validation rules added where the result is weak — attention checks can
  remove exactly the participants whose reasoning would shrink the gap;
  (iii) whether the stimuli or sampled cases span the domain the claim
  generalizes over — one instance of a stimulus class cannot carry a claim
  about the class. Sources: `../../references/methods/gelman_loken_2013_forking_paths.md`,
  `../../references/methods/simmons_nelson_simonsohn_2011_false_positive.md`.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record differential attrition, take-up patterns, and outcome-family findings in the module report's `## Leads for later stages` (folded into the `code-and-data` report) for `claims` —
who complied and who left determines which population the story is about.

## Source

The randomization-inference / leverage / omnibus-joint-null bundle above is
Young, Alwyn. 2019. "Channelling Fisher: Randomization Tests and the
Statistical Insignificance of Seemingly Significant Experimental Results."
*Quarterly Journal of Economics* 134 (2): 557–98. Digest and published-version
numbers: `../../references/methods/young_2019_channelling_fisher.md`.
