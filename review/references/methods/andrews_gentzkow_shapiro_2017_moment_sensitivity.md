# Moment sensitivity — Andrews, Gentzkow & Shapiro (2017)

Working distillation of Isaiah Andrews, Matthew Gentzkow and Jesse M.
Shapiro, "Measuring the Sensitivity of Parameter Estimates to
Estimation Moments", *Quarterly Journal of Economics* 132(4) (2017):
1553–1592. The source PDF (not distributed with the skill) is an author-copy version
(`AGS_2017_MomentSensitivity_QJE.pdf`) — verify numbering against the
published version before quoting.

## The tool

A local measure of how each estimated parameter depends on each
moment of the data — the Λ matrix ("sensitivity matrix") — computable
at negligible cost even for complex structural estimators (§§2–3). For
estimators where identification is orthogonality between errors and
excluded instruments, Λ is the nonlinear generalization of the **omitted
variables bias formula** (§3): a reader who thinks assumption a₀ fails
in a particular way can translate "how the failure changes the moments"
into "how much the estimate is biased" without re-running the model.

## Why the battery needs it

`quantitative-model-diagnostics` had **zero** methods cribs — the only
module with no formal toolkit. AGS is the standard answer to "which
features of the data drive this structural estimate" (the Heckman/Angrist
critique of opacity). For review: a structural estimate whose key
parameters load heavily on a few disputed moments is fragile in a way
no standard error captures; a paper that doesn't report (or can't
produce) its sensitivity structure is asking the reader to take the
identification on faith.

## Review use

- `quantitative-model-diagnostics`: for any structural/estimated-model
  claim, ask (a) which moments carry the identifying weight — is Λ
  reported or computable? (b) does the estimate rest on a small set of
  moments whose validity is contested? (c) does the paper let a reader
  translate an alternative assumption into a predicted bias? If not,
  the "structural" label is doing rhetorical work the machinery doesn't
  support.
- `theory-diagnostics`: same Λ logic applies to model counterfactuals —
  which calibrated parameters does the headline comparative static
  actually load on?
- This is the structural-side analogue of the Rotemberg weights in
  shift-share: both decompose an opaque estimate into "which inputs
  carry it." The review question is identical — name the load-bearing
  moments and check them.
