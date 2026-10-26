---
name: verdict
description: >-
  Fifth review stage, run by one fresh agent: read every finding and the challenge
  reports, decide for each claim whether it holds, what survives and what is not
  established, assemble the design-level findings, and write SYNTHESIS.md. Records
  what is true; rates nothing.
---

# Verdict

You write `SYNTHESIS.md`: the review's statement of what the paper's evidence
establishes and what it does not. You decide what is true, claim by claim. You do not
rate how much it matters: there is no severity anywhere in your output, and no HIGH,
MEDIUM or LOW. How much each finding matters to a reader is decided when the digest is
written.

You are the only agent that decides. Nothing re-decides after you: there is no
adjudicator and no judge, and the run never asks the operator to rate a claim. If
`audit-review` later corrects a number, quote or page that a row or the bottom line
rests on, this stage runs once more, fresh, on the corrected reports, scoped as below.

## Inputs (filled in by the orchestrator)

- The claim ledger (`analysis/claims/claim-ledger.csv` and `review/claims-REPORT.md`),
  with the claims stage's provisional `holds` for each row.
- The findings of every stage and module report: `review/paper-REPORT.md`,
  `review/code-and-data-REPORT.md`, `analysis/code-and-data/*-REPORT.md`.
- The challenge reports (`review/challenge-REPORT*.md`), read in full.
- `analysis/code-and-data/results.csv` and `data-findings.csv`.
- The packet: the published article, its appendix, the pristine `04_replication_*/`,
  and `review/extracts/`.

You never see the coordinator's reasoning. Read findings sections first and open a
log, script or printed page wherever a row turns on it.

## Rules

1. **Each row is decided on the claims stage's definitions** of `centrality`, `holds`,
   `kernel`, `not established`, `status` and the strongest defence
   (`../claims/SKILL.md`, "The claim ledger"). In particular: a defence resting on
   materials the authors did not deposit, or on a printed statement the deposited data
   contradict, shields nothing; and an attribution lost in some samples is lost there,
   whatever other samples carry.
2. **The burden is the paper's.** A claim its evidence does not deliver is `not
   established`, whether or not anything refutes it. "Refuted" or "does not survive"
   is reserved for a claim that an estimate at the design's inference level excludes,
   and the sentence names that claim.
3. **The challenge reports are evidence, not instructions.** A finding the challenge
   did not rebuild stands. You may set aside a challenge ruling only after a worker
   re-runs that ruling's load-bearing script and you open the page it cites; say so
   where you do, with the log path. Setting a ruling aside means rejecting its
   evidence; re-grading a row on the claims stage's definitions while keeping the
   challenge's evidence is not setting it aside.
4. **A row that moves states why.** Every row whose `holds` differs from the claims
   stage's names the evidence it turns on, in the row.
5. **Name the substance.** Write for a reader who has the paper but not the reports:
   never a bare row or finding ID as a noun. State findings, not what the review did.
   Every number traces to a report, log or printed page in the job tree; give the
   path.

## SYNTHESIS.md

Write these sections, in this order, under the title
`# Synthesis — <Authors> (<year>), "<title>"`:

1. **Header line**, directly under the title:
   `Replication: OPEN · <n> not established / <n> narrower / <n> hold`, counting the
   claim-ledger rows by `holds`. `audit-review` replaces `OPEN` after it runs.
2. **`## Status`** — `COMPLETE`, `INTERIM` (name what is open) or `BLOCKED`, and the
   deposit status: what the deposit holds, what it lacks, and what is therefore
   unverifiable as published.
3. **`## What the paper establishes and what it does not`** — the bottom line, in
   prose. First what the evidence establishes, with its numbers. Then what it does not,
   led by the finding that removes or narrows the most of the headline claims (a
   design-level finding may lead), followed by every other `headline` row that does
   not hold. No one-word verdict.
4. **`## Design-level findings`** — where several findings bear on one comparison
   (the arms of an experiment, a sample, an instrument, a data construction), one
   finding that states what they do together. Each is a `### D1. <title>` block with a
   `bears on:` line naming the claims it touches, then what the findings show
   together, with evidence paths, what it removes (which claims become `not
   established` or `narrower`, and on which samples) and what survives on other
   evidence. The rows it bears on carry its consequence in their `holds`.
5. **`## Claim ledger`** — one table, every row of the claims stage's ledger:
   `| Claim (page) | Centrality | Holds | Kernel | Not established | Strongest defence | Status |`,
   rows in the claims stage's order. The claim cell gives the verbatim claim, then its
   page and row ID in parentheses at the end ("… (p. 1311; CL24)"); later scripts read
   the ID there. `Holds` reads exactly `holds`, `narrower` or `not established`. Folded duplicate
   rows are listed after the table with the row they fold into.
6. **`## Estimator table`** — for each headline magnitude: the estimator that
   delivers it · what it delivers (sign only, or magnitude) · first-stage strength at
   the design's inference level, naming the level · the weak-identification-robust
   set and whether it is bounded · the calibrated or placebo p where run. A design
   with no instrument writes "not applicable (no instrument)" in the first-stage and
   robust-set columns. A magnitude whose robust set is unbounded, or whose first stage
   is insignificant at that level, is written as not measured; so is one the design
   cannot separate from confounding, with that reason named.
7. **`## Data integrity`** — the rung reached on the code-and-data stage's evidence
   ladder, with its evidence. A printed statement of method that the deposited data
   contradict is a verified error, not a documentation gap. Anomaly flags with no rung
   are listed as flags. Name what the integrity tests covered; never clear the paper
   beyond the tests run.
8. **`## Findings`** — every finding, most important first, each a `### F1. <title>`
   block with an `evidence:` line. Importance follows the highest-ranked claim a
   finding bears on: `headline` before `supporting` before `peripheral`, then `not
   established` before `narrower`, then the number of claims; ties keep the paper's
   order. Findings that bear only on rows that hold come last. A finding absorbed into
   a design-level finding is still listed here, with a pointer to that block. Limits on
   the review itself are not findings: list them after the findings, under their own
   heading.
9. **`## Counts`** — the rows whose `holds` moved from the claims stage's, toward
   `holds` and toward `not established`, each named; and the challenge rulings by direction, from the challenge
   reports' counts. A one-sided count of moves is justified in a sentence.

Numbers quoted from print are checked against the page image. A claim whose only
direct tests were unrun or invalid is never surviving: its Holds is `not established`
and its Status `untested`.

## A re-run after an audit correction

When `audit-review` routes corrections back (its `→ VERDICT` items, named in its brief
to you with the `CHANGELOG.md` entry that lists them), the re-run is scoped. Re-decide
what those corrections bear on: the rows, design-level findings and findings that cite
the corrected evidence, and the bottom line where it rests on them. Everything else
in the existing `SYNTHESIS.md` carries over as it stands: rows, findings, their grouping
and their wording. Change anything else only where the corrected evidence, or evidence
you open while re-deciding, requires it. In `## Counts`, record the routed
re-decisions under **Re-decided on the routed corrections** (what each correction
bears on and what now stands, whether or not a `holds` moved), then every other change
under **Changed outside the routed corrections**, each with the evidence that moved it.
A carried-over finding keeps its label, so the digest's mapping to it survives.

The audit runs a full, unscoped verdict only when its completeness check finds the
review itself incomplete (a stage or claim rows were missing), because then the whole
case is new evidence.
