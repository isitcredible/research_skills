# What a "failed replication" means — Clemens (2017)

Working distillation of Michael A. Clemens, "The Meaning of Failed
Replications: A Review and Proposal", *Journal of Economic Surveys*
31(1) (2017): 326–342. The source PDFs (not distributed with the skill):
`Clemens_2017_FailedReplications_JES.pdf` (IZA DP 9000) **and**
`..._published.pdf` (the published JES article) — quote
the published version.

## The proposal

"Replication" has no standardized meaning in economics, so a discrepant
replication can signal anything from a legitimate methodological
disagreement to misconduct. Clemens proposes an unambiguous taxonomy
(§2, Table 1, pp. 327–328): a **replication** test estimates parameters
from the same sampling distribution — **verification** (the exact
reported analysis, on the original data or the same sample remeasured)
or **reproduction** (identical methods on a new sample of the same
population); a **robustness** test estimates different parameters —
**reanalysis** (altered code: new specifications, coding, covariates,
SEs) or **extension** (new data on a different population or period,
including dropping influential observations). The two have different
evidentiary weight — a failed replication signals error, chance, or
fraud; a failed robustness test signals that the sampling distribution
changed — and much prominent "replication failure" discourse conflates
them.

## Why the battery needs it

The `code-and-data` stage's data audit and spec checks run both kinds of
check but had no cite for the distinction or its incentive logic. The
taxonomy disciplines the review's own claims: a reviewer who cannot
reproduce the published table on the published data has found a
*verification* failure (narrowly defined, high-confidence); a reviewer
whose *different* specification gives a different answer has found a
*robustness* finding — weaker claim, different remedy. Conflating them
either over- or under-claims the critique.

## Review use

- `code-and-data` / `paper`: when re-running published code,
  keep the two failure modes separate in the writeup — "the code does
  not produce the table" (verification) vs "the table is sensitive to
  specification choice" (reanalysis). Clemens is the cite for why the
  distinction matters to the strength of the claim.
- `claims`: when the review's verdict is reported, a "failed
  replication" phrasing should be reserved for verification failures;
  sensitivity findings are reanalysis disagreements. This is the
  honesty constraint on how hard the review can claim to push.
