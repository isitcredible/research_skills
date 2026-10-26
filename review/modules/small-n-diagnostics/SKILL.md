---
name: small-n-diagnostics
description: >-
  Diagnostics for small samples and minimum detectable effects: MDE at
  conventional power against claimed and plausible effect sizes, lean
  re-tests when saturated controls overfit, and estimator-specific
  small-sample artifacts. Invoke from `code-and-data` whenever units or
  clusters are few, or a null carries interpretive weight.
---

# Small-N diagnostics

Establish what the design could actually detect and what its reported
precision is worth. A small sample cuts in both directions at once: too
little power to detect a plausible effect, and too few degrees of freedom
to survive the controls piled on it — so a null proves nothing on its own,
and a precise-looking estimate may owe its precision to a small-sample
artifact of the estimator. The checks below put numbers on both directions
so the result can be read at its true weight.

Trigger: few units or few clusters behind any target result, or a null or
near-null that carries interpretive weight — whether the paper leans on the
null or the battery produced it. `NOT_APPLICABLE` when the design has ample
units and no null is load-bearing.

## Core checks

- **Minimum detectable effect at conventional power**, computed against
  both the claimed effect size and the effects the mechanism or the
  specialist literature makes plausible. State the comparison in the same
  units as the claim: "this design could detect an effect of X; the
  plausible effect is Y." Underpowered does not mean refuted — and a null
  from an underpowered design is uninformative in both directions
  — the evidence `claims` needs to decide whether a null is informative.
- **Lean and bivariate re-tests** — when saturated controls sit on a small
  sample: re-estimate with minimal controls. In a small sample, a control
  set approaching the number of observations manufactures fit; the lean
  specification shows what the data alone support.
- **Effective number of clusters, not nominal.** For every clustered
  target compute the partial-leverage effective count G* (Carter et al.
  2017; ρ = 0 iff the spec carries cluster FEs) —
  see `../../references/methods/mackinnon_nielsen_webb_2023_few_clusters.md`.
  The prior question — *whether and at what level* clustering is owed —
  is a design question, not a residual-correlation test: it is answered
  from how clusters entered the sample and how treatment was assigned
  (`../../references/methods/abadie_athey_imbens_wooldridge_2023_clustering.md`); a design can fail at either stage — cluster at the right
  level and still have G* ≈ 2, or cluster on residual correlation alone
  where the design carries no cluster-level assignment.
  A shift-share regressor is a clustered target at the shock level
  whatever the unit-level SEs are. Heteroskedasticity-robust SEs over
  units that look independent do not exempt it, because the units share
  the shocks. Run this check there, through the shift-share module's
  shock-level jackknife row. A few-cluster tool applied to unit-level
  cells (a wild bootstrap over demographic or regional cells) is not the
  shock-level answer, and must not be reported as one.
  Fifty nominal clusters with one dominant leverage behave as ~1–2.

  **THE WILD CLUSTER BOOTSTRAP IS NOT THE FEW-CLUSTERS ANSWER.** Your training says
  it is, and that plain `boottest` is how to run it. Both are wrong when G* is small.
  Plain `boottest` is WCR-C. With one dominant cluster its draws mostly re-sign that
  cluster, and its p-value can be far too small or far too large. Runs have repeatedly
  headlined WCR-C p-values that the jackknife and randomization overturned.
  `../../scripts/check_inference.py` fails the run on it. When G* is small or leverages are
  unequal, do this, in this order:

  1. **G\* and partial leverages**, top clusters named.
  2. **CV3 (delete-one-cluster jackknife) leads**, beside CV1. Re-fit non-cluster FEs
     and controls in each leave-out; partial out only FEs nested within the clusters.
     When coding CV3 by hand (because `summclust` is unavailable or the specification
     uses multi-way FEs or weights), re-estimate the absorbed FEs and controls inside
     every leave-one-cluster-out iteration — never demean or partial out non-cluster
     FEs once on the full sample before the loop, which leaks the omitted cluster into
     the fixed effects and corrupts the leave-out variance. The jackknife emits a
     *variance*, which the battery carries downstream: SE ratios against the paper's
     CV1, VtF/tF inputs, the quantify-inference rule. Its β̂^(g) leave-out distribution
     shows which cluster carries the estimate. The CV1→CV3 gap is the leverage finding.
  3. **Restricted wild bootstrap, second, led by WCR-S** (`boottest …, jk noci` followed
     immediately by `assert !missing(r(p))`; R/Python `bootstrap_type = "31"`).
     `boottest` prints a confidence set by default for a single hypothesis, and its `jk`
     residual adds an `(M_{gg}^{-1} − I)X_g t₁` term that vanishes only at a null of
     zero, so `noci` is mandatory (`check_inference.py` F9) and any non-zero null or
     confidence/Anderson–Rubin set must be inverted by transforming the outcome
     (`y − b₀·x` or `y − b₀·endog`) and testing zero over a grid (`boottest …, ar`
     runs an unrestricted bootstrap DGP and fails `check_inference.py` F8 unless tagged
     `AR-boottest-robustness` as a companion row). Because `boottest` exits with
     `_rc = 0` and `r(p) = .` when it refuses a model (e.g. multiple or interacted
     absorbed FEs after `reghdfe`), every Stata `boottest` call must be followed by
     `assert !missing(r(p))` (`check_inference.py` F10); when `boottest` refuses a
     multi-way or interacted FE specification, collapse each interacted FE pair into a
     single group id (`egen fe_ab = group(a b)`), verify the point estimate is
     identical, and re-run, or fall back to CV3/randomization. Always also run WCR-C
     and report its p beside WCR-S (MNW advise computing both whenever CV1 and CV3
     differ, and the cost is one more call); it is never cited alone as the result.
     WCR-C and unrestricted (WCU) calls are tagged `WCR-C-robustness` / `WCU-robustness`
     in the code. Name the variant, the weights and B ≥ 9999 every time a bootstrap
     number is cited ("WCR-S p .03", never "WCR p .03"). Log its known failure modes
     as pathology evidence: coarse p-value granularity at small G (support bounded by
     2^G Rademacher / 6^G Webb draws), `boottest` non-attachment to the estimator,
     unbounded inversion, and under-rejection with few treated clusters.
  4. **One or few treated clusters, or few effective shocks: randomization inference**
     over the actual assignment. It outranks every bootstrap.
  5. **Where CV3, WCR-S, WCR-C and randomization disagree, the disagreement is the
     finding.**
     Report the spread. Never pick the most favourable p-value for either side.
  6. **Size checks must model the dependence that matters.** A simulation that draws
     errors independently across clusters cannot certify a test when units in
     different clusters share a treatment source. A shift-share design is the standard
     case: commuting zones with the same industry mix are dependent across states.
     Such a simulation is no size evidence there (see the shift-share module's
     placebo-shock rejection table).

  For IV coefficients under a weak first stage, tF/VtF confidence sets (conditioned on
  F̂, and r̂ for VtF) go honestly unbounded instead of printing a discounted p-value.
  An unbounded set is reported as "uninformative at this cluster count", not smoothed
  over.
- **Estimator-specific small-sample artifacts.** Check whether the
  estimator's standard errors are known to misbehave at this N — for
  example, quantile-regression standard errors at small N — and substitute
  or supplement with resampling or exact methods where a validated
  implementation exists. Specifically: `statsmodels` `quantreg` SEs are
  sparsity-based and unreliable at small N under a saturated or
  near-degenerate design (they can come out *smaller* than OLS — a fake
  strengthening); for a median/L1 check, fit the full specification in a
  second toolchain (R `quantreg::rq`, using `method = "sfn"` for sparse
  fixed effects, or `fequantreg` / `qregpd`), or report `BLOCKED` if
  high-dimensional fixed effects cannot be absorbed in L1 — never
  FWL-partial by OLS before an L1 fit (the Frisch–Waugh–Lovell theorem
  holds for L2/OLS, not L1/quantile regression). Never quote a full-design
  quantile-reg t at small N without an independent-implementation check.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record EVERY power and design-validity threat in the module report's `## Leads for later stages` (folded into the `code-and-data` report) for `claims` as it appears, whether or not the
result is a null — the MDE-versus-plausible-effect comparison is the
central input to the informative-null branch decision, and it is this
skill's job to compute it, not `claims`' job to wish for it.
