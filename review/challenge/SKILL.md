---
name: challenge
description: >-
  Fourth review stage, run by a fresh agent: test the review's evidence in both
  directions — where the review errs against the authors and where it errs in their
  favour — rebuild it from the pristine deposit and the printed page, and rule on
  each element: STANDS, STANDS WITH CHANGES, WRONG or ADD, with proposed wording and
  every adverse result the stage's own scripts produced. Rules on evidence, never on
  severity.
---

# Challenge

You test the review's evidence, not its tone, and you rule on evidence, never on
severity: the verdict stage decides what the surviving evidence establishes. Reviews
built to find fault err against the authors: in the first ten such tests every review
had errors, nearly all against them, and three headline verdicts were wrong. A stage
built only to defend the authors errs the other way: when it removed invalid attacks,
valid ones went with them, and estimators the review's own logs showed to be
uninformative were written up as identified. Argue the authors' case, then the reader's, and rule on the evidence.
STANDS on a sound finding is as useful a ruling as WRONG on a bad one.

## Inputs (filled in by the orchestrator)

- **Evidence under test:** every claim-ledger row, verbatim, with its holds, kernel,
  status, and the findings and evidence paths it rests on in both directions — what
  the review counted against the claim and what it counted for it (where the ledger
  has one undirected evidence column, sort it into the two directions yourself); every finding in
  the stage and module reports; and every calculation the review built itself that a
  finding rests on.
- **Packet:** {job root}: the published article, its appendix, and the pristine
  `04_replication_*/`.
- **Work folder:** `work/challenge/`, holding scripts `s1…`, each with a log of the
  same name. A large run is split by group of result families, one agent per group,
  each writing `review/challenge-REPORT-<group>.md`.

## Rules

1. **YOU MAY READ THE REVIEW'S SCRIPTS AND LOGS TO SEE WHAT IT DID. YOU MAY NEVER RUN
   ITS SCRIPTS, OR CITE ITS `results.csv`, LOGS OR DERIVED DATA AS EVIDENCE.**
   Re-running a flawed regression reproduces the flaw. Build every number from the
   pristine deposit and the printed page, and reproduce the paper's anchor cell before
   any variant.
2. **A finding you did not rebuild stays in force.** A ruling may weaken a row only on
   evidence you rebuilt. List every finding on the row that you did not rebuild, in
   either direction, under (d); it carries into the verdict stage unchanged. Removing an
   invalid argument against the paper does not remove the valid ones beside it.
3. Every number in your report cites `script:line` in your own log or a printed page
   and cell. A ruling with neither is not a ruling. The `review` rules bind you
   (`../SKILL.md`, especially 4, 6 and 8).
4. Check each PDF's title page before citing it; cite printed page numbers.

## Where reviews err against the authors

Test every element for each of these:

- **A wrong design treated as the honest test**: a variant the design's literature
  rules out, such as a shift-share shock leave-out or residualised variant without the
  exposure-sum control (for a leave-out, the sum of the remaining shares — with
  complete shares, the dropped shock's share). Find the correct
  version; the authors have often printed it. Reproduce it from the deposit before
  it rescues the claim; the wrong-design finding falls either way.
- **Our repair changing their result**: run the unmodified deposit and diff.
- **A test with no power read as a refutation**: simulate it under the paper's own
  estimate. If it would seldom reject when the paper is right, its non-rejection is
  no evidence. If it cannot reject any value, it is degenerate. A correction of the
  paper's own estimate (rule 8's definition) is not such a test: low power does not
  restore support the correction removed. A variant relabelled a correction is.
- **An uninformative estimate read as a null**: an interval that contains both zero
  and the paper's estimate refutes nothing. "Fails", "collapses" or "does not survive"
  needs an estimate that excludes the paper's. A claim whose evidence is uninformative
  is stated as not established. That is the finding, not a softer one, because the
  burden is the paper's. Say what the data cannot say, plainly, with the interval.
- **An attack on a claim the paper does not make**: find every quoted claim on the
  printed page and read the whole sentence for qualifiers ("In our model", "of
  final goods"). A quote that is not on the page, or a significance claim the paper
  never makes, is no target.
- **A choice the paper states and justifies, counted as a failure.** A stated
  justification answers an omission charge; it does not end the argument, and a
  review that rebuts the justification itself stands.
- **The authors' own disclosure presented as our discovery**: credit them.

## Where reviews err in the authors' favour

Test every element for each of these:

- **Evidence for the claim held to a lower bar than evidence against it.** Rule 8
  binds both directions. A first stage called strong, an estimate called precise, a
  result called robust, or a test the paper "survives" must hold at the inference
  level the design's literature requires (the shock level for shift-share, the level
  of the identifying variation for clustering), and the test must have been able to
  fail.
- **A magnitude carried by an uninformative estimator.** When the
  weak-identification-robust set (Anderson–Rubin, conditional LR, or a null-imposed
  shift-share interval) is unbounded, or the first stage is insignificant at the
  design's level, the estimator measures no magnitude: say so, and say what still
  carries the sign (usually the reduced form). Decode the output: a set printed with
  its lower endpoint above its upper, or with an infinite standard error, is
  unbounded. Never describe such an estimator as "identified by" the units that
  dominate it.
- **Inference borrowed from another table, sample or level**: a bootstrap, permutation
  or robust set cited for one result but run on another.
- **A concession that pairs numbers across specifications, samples or clustering
  levels** ("although at the industry level …") to soften a finding.
- **A result the review produced and did not report**: a placebo, a control, a first
  stage or a leave-out in its logs that cuts against the claim and never reached the
  ledger.
- **A row recorded as holding, or a kernel stated wider, than its evidence allows**,
  and a narrower verdict worded more favourably than the surviving evidence allows.
- **A finding filed where it does least.** A fault that bears on a headline
  comparison recorded only against a minor sentence, or split across rows so that no
  row carries it. Name every claim it bears on.
- **A rescue that carries the same defect.** A claim saved by evidence elsewhere: test
  the rescuing evidence for the fault that sank the original.

## Inference traps, both directions

A descriptive share is not causal importance. "Exact" is not a threshold-sensitive
proxy. A point-estimate ratio is not a bound. Equal numbers are not the same quantity.
Fixing inference is not fixing weighting. One adverse variant chosen from many is not
fragility: report the family and how many of its variants move the result. One
significant result chosen from many specifications, outcomes or subgroups is not
evidence at its nominal p: count the forks the paper or the review walked. An error is
not fabrication: intent needs evidence of intent.

## Calculations the review built itself

For each calculation the review built that a finding rests on — a corrected variant, a
new control, a split, a recode, a resample — write what it must satisfy, from the paper
and the code, before opening the review's scripts and logs for it. The stage reports
may already have told you what the review built; say so in the report. Then rebuild it and mark each
requirement `met` or `failed`. Check for missing data silently shrinking the sample,
over-control on post-treatment variables, screens applied to one side only,
sensitivity to the build, reconciliation with the printed sample and, for resampling or
permutation, draws that follow the experiment's own assignment rules
(`../references/construction-validity.md`). A review-built rescue of the paper gets the
same scrutiny as a kill.

A fault the review missed, in either direction, goes in as ADD.

## Report: `review/challenge-REPORT.md`

If the harness will not let you write files, return the full report text as your
final message; the coordinator saves it unchanged as the report.

- **Header:** the evidence under test (verbatim); the version check; what your
  scripts read.
- **(a) Ruling** for each claim: STANDS, STANDS WITH CHANGES or WRONG, with a few
  sentences on what is wrong in each direction and what the surviving evidence
  supports. No severity and no proposed rating.
- **(b) Element table:** `# | element (verbatim from the review) | direction (against
  / for the authors) | ruling | evidence | proposed wording`. The direction is the way
  the element's content cuts. The ruling is STANDS, STANDS WITH CHANGES, WRONG or ADD. Proposed wording is a draft for the verdict
  stage, not text to paste.
- **(c) The strongest case for the authors and the strongest case against them**,
  point by point, and whether each point succeeds against the row as written and
  against the narrowest charge left.
- **(d) Not rebuilt**: every finding on each row you did not rebuild, in either
  direction. These stand.
- **(e) Adverse results**: every result in your own logs that cuts against the
  authors, cited by `script:line`, whether or not your rulings used it.
- **(f) Not tested**, and why.
- **(g) Count**: element rulings by direction (against / for the authors × STANDS /
  STANDS WITH CHANGES / WRONG / ADD); the claim rulings from (a), on their own line;
  and each review-built calculation with its requirements met and failed.

Report findings only; do not narrate what you did.
