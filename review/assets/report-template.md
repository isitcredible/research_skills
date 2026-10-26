# [Stage] Report — [Paper Title]

The technical record of what this stage established, findings first. Every claim
resolves to an artifact a reader can re-run or check — a script and log, a row in a
ledger, or a page-referenced printed cell. No narrative of the procedure.

## Status

`COMPLETE`, `INTERIM` (name what is missing) or `BLOCKED` (give the exact evidence),
and one or two sentences on what the stage found and on what evidence. `COMPLETE`
means every applicable check ran and its output was inspected — not that a file
exists. A `PROXY` counts only if it actually covers the requirement and states its
limits.

## Findings

Most important first (within each group, where the stage groups them), one block each.
Stages number findings `P1` (paper), `C1` (code-and-data), `L1` (claims). A module
report uses its own prefix: CTL controls-samples, XS cross-sectional, DID
did-event-study, EXP experiment, IV iv, PAN panel, QM quantitative-model, RDD rdd,
SCL scale-sensitive, SSH shift-share, SN small-n, SC synthetic-control, TH theory,
TS time-series, WA whimsical-assumptions.

### [P1 / C1 / L1 / SN1]. [Title]
bears on: [the claims this finding touches, named]
evidence: [paths to script + log, ledger row, or page/cell]

What is wrong, the printed value against what was found, and its effect on the
result: the headline quantity before and after, in practical magnitude, significance
and (for estimates) variance share; for theory, the consequence for the theorem.
State direction — a defect that understates the paper's estimate is written as
understating. Say so plainly when a correction leaves the result unchanged or
strengthens it. Combined rules are decomposed so the report names which part moves
the result.

A blocked check (exact file, command, error) and a justified `NOT_APPLICABLE` are
recorded here too, so the gap is visible.

## [Sections the stage requires]

Each section the stage's SKILL requires beyond these goes here, between Findings and
Leads — for `claims`, the supportable story per result family, the claim ledger and
the claim-test matrix.

## Leads for later stages

Checks to run, variables to trace, claims to test — each naming its source.

## Scope assumptions

Limits this stage relied on ("the deposit cannot run Table 3", "inputs X are
synthetic"), each with its evidence. A later stage that overturns one re-checks
everything that rested on it.

## Coverage

Papers, data and code examined; which result families this stage reached and which it
left open.
