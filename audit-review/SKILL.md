---
name: audit-review
description: >-
  Mechanical audit-and-fix pass over a completed `review` run. Checks (a)
  completeness — every stage ran, and every printed equation, table, figure,
  headline claim and deposited script was covered — and (b) mechanical errors —
  scripts re-run clean, paper numbers match print, reproduced numbers come from the
  right row, anomalies reach the claims they bear on, every number traces to a log.
  Rates no claim: a correction that a claim-ledger row or the bottom line rests on
  goes back to the review's verdict stage. Declares the evidence handoff for the
  digest. Use after a review, or to bring an old run up to the current spec.
metadata:
  version: "0.9.3"
---

# Audit a review

Check a completed `review` run for **completeness** and **mechanical errors**, fix
what fails, and leave the run's own reports correct. The audit decides nothing about
what the evidence establishes: whether a claim holds is the review's verdict stage's
call, and the audit routes any correction that bears on it back there (step 4). The product is the corrected reports — not
a report about the audit. Corrections go into the run's own files; the audit's
scripts and logs go under `work/audit/`. The only new files the audit writes
elsewhere are:

- `CHANGELOG.md` — the corrections list (the only file that says old → new);
- `coverage.csv` (generated) and `coverage-na.csv` (your not-applicable rulings);
- `spec-drift.csv` (generated, with your dispositions) and, where it declares
  superseded scripts, `inference-superseded.csv`;
- `HANDOFF.md` (+ the generated `HANDOFF.manifest.json`) — the evidence the digest
  may cite.

Corrected reports must read as if they were right first time: every sentence makes
sense to a reader who never saw the earlier draft, and without the paper's table of
contents, the stage reports, or this skill open beside it — name the substance ("the
wage simulation (Section 3.6, p. 48)"), never a bare section number ("§7.3", "the §3.6
results", "§6", "§4a") or a bare claim or finding ID ("CL08", "C14") as a noun, in the
reports, `CHANGELOG.md` open/operator items, or messages to the operator.

## Ground rules

- The run's logs, manifest and SYNTHESIS are what you are checking, not evidence that
  it is right. Presume nothing is verified until you have checked it yourself.
- A number that reproduces is not thereby correct: re-running a script says nothing
  about whether it matches print, comes from the right row, supports the inference, or
  whether the calculation itself is sound. A bug in a review-built calculation
  reproduces perfectly every time.
- A fix produces evidence. Never edit a report to say PASS.
- A FAIL is either the review's error (fix it) or correct work showing the *paper*
  fails (keep it). Never fix away a true finding.
- Your own repairs get the same checks as the run's.
- The checklist is the `review` skill at the version the run records
  (`Suite version:` in `00_INTAKE.md`). For a run in use, that means the current
  skill, with `check_spec_drift.py` listing what the run was never asked to do. A
  run frozen for a corpus or a release test is audited against its own tagged
  snapshot, and is upgraded to the current skill only when the operator asks.
  Record the version you audit against (the `metadata.version` in its frontmatter)
  in `CHANGELOG.md`. A run in the old six-stage layout is
  audited against the current spec; read its six stage reports as the first three stages
  (version-diff + research-design = paper; spec-accuracy + fragility-battery +
  data-audit = code-and-data; check-story = claims) and pass its ledger paths to the
  scripts explicitly. A run made under v0.6.2–v0.7.x holds stress reports,
  re-derivations and adjudications, and a claim ledger with severities instead of
  `holds`: read its stress reports as challenge reports (ignoring their proposed
  ratings), have the claims stage add `centrality` and `holds` to every ledger row,
  list the re-derivations, adjudications and stress checks as `superseded` in
  `HANDOFF.md`, and run the verdict stage fresh.
- **Agents and cost.** Size, route and run every worker by the `review` skill's
  *Agents and cost* section. Every audit task is mechanical: re-runs, print checks,
  row checks, coverage, propagation, artifact completion. The one judgement task, a
  verdict re-run (step 4), is the review's verdict stage, run by its own rules on the
  verdict model; so is any stage or module the completeness check finds missing.
- **Back up with the repository, never with copies.** Commit the job tree before
  applying corrections, so the diff is the record; never copy files or trees as
  backups. A job folder that is not a repository gets `git init` (local, no remote)
  first.
- **Re-runs.** Commit, re-run in place, and read drift with `git diff`. Never re-run
  in place a script that appends rows to a shared ledger: run it in a copy of the
  tree, or rebuild the ledger from its builder script, and say which.
- Unattended (no operator available to answer), resolve every pause by rule: keep
  the evidence, record the call and the reason, continue. A live process the audit
  did not start (another session's job) makes the audit `INTERIM`: audit what exists
  and defer the rest. Re-runs the audit starts itself never make it `INTERIM`. Run a long one in the background, do the other work meanwhile, and collect it
  before handoff. A re-run that cannot finish in the session is reported with its
  measured runtime and the command that completes it, not used to stop early.

## 1. Completeness — was everything covered?

Each miss is a FAIL, and the fix is to do the missing work (derive the row, run the
check), not to note it.

- **Stages.** The four stage reports and `SYNTHESIS.md` exist with their required
  sections, and each stage's required artifacts exist and are substantive: drift table
  and robustness-claims ledger (paper); formula map, feasibility matrix, construction
  ledger, manifest, `results.csv`, data-audit statuses (`source-coverage.csv`) and
  `data-findings.csv`, the module-dispatch walk and a
  report for every fired module (code-and-data); driver matrix and claim ledger, with `centrality` and `holds` for every row (claims); challenge reports covering every claim-ledger row, every stage finding and every review-built calculation, in both directions, with their counts (challenge; a run without them gets the stage now); a `SYNTHESIS.md` written by the verdict stage, with every section that stage requires, including the design-level findings, the estimator table and the counts (verdict). Run
  `python3 <review skill>/scripts/check_manifest.py --root <job>`. Each stage
  ran its documented steps, not a one-off substitute. Run
  `python3 <review skill>/scripts/check_inference.py --root <job>` too. A failure is
  a FAIL like any other: re-run the bootstrap as WCR-S (`boottest …, jk noci` at zero
  with `assert !missing(r(p))`; non-zero nulls and Anderson–Rubin sets inverted over a
  grid on the transformed outcome `y − b₀·x` / `y − b₀·endog`, F8–F10), lead the row
  with CV3 (re-estimating FEs inside each leave-out), add the placebo-shock rejection
  table with the randomization p and the shock-level jackknife (F4/F12), compute VtF on
  jackknife inputs and the Montiel Olea–Pflueger effective F for every IV cell
  (F6/F7/F13), re-run HonestDiD on universal-base event studies (`csdid, long2` /
  `base_period = "universal"` with positive `e(b)` positions, F11), and restate every
  claim-ledger row whose inference changes. Never tag a call as robustness just to pass
  the gate. Historical scripts that a new battery recomputes may be listed in
  `inference-superseded.csv` (path, reason, replaced_by). Once listed, no report may
  cite their bootstrap as the result.
- **Spec drift.** A report that exists may still predate a requirement. Run
  `python3 <audit-review skill>/scripts/check_spec_drift.py --root <job> --write`
  (add `--run-date YYYY-MM-DD` when `00_INTAKE.md` records no `Suite version:`).
  It lists every requirement in the review skill's `spec-changes.csv` added since the
  run's version, or, for a run older than that history, a full re-walk of every stage
  and module. Do each item and record `done: <artifact path>`, or rule it
  `na: <reason>` (e.g. the module never fired); then run it without `--write` until it
  exits 0 (it prints `PASS`).
- **The printed paper.** Run
  `python3 <audit-review skill>/scripts/check_coverage.py --root <job>` (it finds
  `01_*.pdf` and `02_*.pdf` under the root; it fails when it can read no printed
  surface, or no deposit inventory unless `00_INTAKE.md` records `Deposit: none`).
  It lists every equation (numbered and lettered), table and figure. It fails an
  equation with no formula-map row and a table or figure with no row or mention; a
  table or figure carried only by prose WARNs — confirm it has a row. Fix by deriving the row, or rule it not applicable with a reason in
  `coverage-na.csv` (`ref,reason`). A printed equation missing from the formula map is
  the canonical miss. The script sees only tagged equations: check every untagged
  display equation against the formula map by hand.
- **The deposit.** The same script fails every code file in
  `review/deposit-inventory.json` that no report, ledger or log mentions, and lists
  unmentioned data files. Every script was either read or run, or is ruled out with a
  reason.
- **The claims.** Re-read the abstract, introduction and conclusion yourself. Every
  claim sentence maps to a claim-ledger row; a missing claim gets its row.
- **Gaps.** Every `BLOCKED`, `NOT_RUN`, "infeasible" or "not in the deposit" claim
  carries its evidence: the exact file, command and error, or a saved listing (the
  script fails deposit-absence claims without a `listing:` path). A gap that is
  feasible and verdict-bearing is run now. A diagnosis with no attempt is a FAIL.
- **Version.** The critique rests on the published article. A working-paper number
  standing in for the published value, or a "contradiction" that exists only inside a
  working paper, is a FAIL that voids the finding. Drift between dated versions, and a
  working paper that is the version of record, are exempt.

## 2. Mechanical errors — do the reports match the scripts, the logs and the print?

Work through the load-bearing findings first; a wrong finding is not rescued by tidy
process. Cases of each failure: `references/audit-cases.md`. Whether a test
could count, and whether a calculation the review built is valid, are the challenge
stage's checks, not the audit's.

a. **Re-run** the scripts the findings rest on. A script that errors or prints a
   different number is a FAIL as serious as a wrong result; on any mismatch, widen the
   re-run.
b. **Print check.** Every number, quote and page attributed to the paper matches the
   printed article — open the printed cell, never the review's own output. A claim
   that "the paper's specification is X" is checked against the printed equation *and*
   the code at `file:line`. A wrong baseline voids every comparison made against it.
   A mismatch between print, prose and code is checked against the paper's own
   disclosures and errata before it is recorded.
c. **Row check.** Each reproduced number comes from the script and log row that
   computes *that claim's* quantity — same sample, estimator and standard errors. A real
   number on the wrong row is as serious as an invented one. Check that report tables do
   not carry blank or missing p-values swallowed from refused `boottest` calls, that
   local-randomization RD confidence intervals (`rdrandinf` `ci()` / `rdsensitivity`
   `tlist()`) do not equal `min(grid)` or `max(grid)` (silent grid truncation), that
   residual cointegration tests (Engle–Granger, Phillips–Ouliaris) use MacKinnon
   response-surface critical values (`urca:::.urcval`) rather than raw `ur.df` /
   `punitroot` unit-root tables, and that variance-explained numbers reported as
   Shapley/LMG are order-averaged LMG shares and never raw nested $\Delta R^2 =
   R^2_{\text{full}} - R^2_{\text{without}}$, partial $R^2$, or $\eta^2$.
d. **Propagation.** Every logged anomaly states which claims it weakens or voids. A
   failed shared input (generator, denominator, helper) withdraws every finding built
   on it; a corrected one is re-run through *every* result family that uses it. A
   variant of the paper's documented method filed as invalid, instead of reported as a
   measured discrepancy, is the same failure.
e. **Traceability.** Every reported number traces to a script and log in the job tree.

## 3. The corrections list

One item per FAIL in `CHANGELOG.md`: `file · location · old → new`, the new text
written as the finding itself, in final wording. Items are mechanical: a number, quote,
page, path, log row, stale gate line or missing artifact. Mark each `EVIDENCE` (needs
a number or artifact — produce it now, in your own context) or `TEXT` (applied in step
5). An item that could change a claim-ledger row's `holds` or kernel, a design-level
finding, or the bottom line is also marked `→ VERDICT`. A correction that leaves all of
these as they stand — a locator, a quote made verbatim, a number restated to its log, a
miscount within a finding that does not alter its conclusion — is TEXT only, applied in
step 5, including in `SYNTHESIS.md` (step 4 says when). Order by consequence: a wrong baseline poisons everything built on it. Every TEXT item
carries an **instance hunt** — grep every report and SYNTHESIS for the wrong number,
name or phrase (not only the exact old sentence); fixing one copy while the number
survives elsewhere is not a fix. A verbatim quotation of the evidence that was
tested (such as a challenge report's header) stays as it stands; record the
exception in `CHANGELOG.md`. Every fix follows
the run's own rules (saved, re-run clean, re-checked).

**Open items are only what this audit cannot do.** There are two kinds:
- calls only the operator can make;
- work blocked outside the job: code, data or software that was never deposited or
  cannot be installed, or a source still unobtainable after every acquisition tier
  in the `review` skill (recorded there as `unverified-here`). A cited source read only in a non-published copy has not
  exhausted those tiers.

Each open item states the blocker's evidence (file, command and error, or listing),
what was attempted, and what would close it.

Everything else is completeness work, done in this audit and never listed as
open: a missing module report or stub, an unassessed or unclassified ledger row
(robustness claims included), an unrun feasible check, a stage that needs
rebuilding. `check_manifest.py` fails missing module reports and unassessed
robustness claims. An open item that does not meet this bar is a FAIL. Nothing
is forced green.

## 4. Route to the verdict stage

If any item is marked `→ VERDICT`, apply the mechanical items first (step 5), then run
the review's verdict stage once, fresh, on the corrected reports, scoped to the routed
corrections (its section "A re-run after an audit correction"): name the `→ VERDICT`
items and their `CHANGELOG.md` entry in its brief. It re-decides what they bear on and
carries the rest over, listing anything else it changes. Run it unscoped only when the
completeness check added stages or claim rows. A verdict re-run that cannot be started
in a fresh context leaves the audit `INTERIM`, with the routed items listed as open.
Every TEXT item goes in before the re-run, those in `SYNTHESIS.md` included, and the
brief names the `SYNTHESIS.md` ones as applied, so the scoped re-run carries them
over; after an unscoped re-run, re-apply any its new text lacks. Its `SYNTHESIS.md`
replaces the old one; `CHANGELOG.md` records which rows moved and why. The audit
decides no claim. A corrected row goes straight to the verdict stage, never back
through the challenge stage. A row the completeness check adds (a claim sentence the
ledger missed) is new evidence: the claims stage writes it and the challenge stage
tests it, once, before the verdict re-run. An errata item
routed back from `review-digest` is classified by step 3's own test (TEXT, or
`→ VERDICT` where it could change what a claim establishes), not by its
`finding-bearing` flag; a `→ VERDICT` one is handled the same way.

## 5. Apply

Apply every TEXT item yourself, with its instance hunt. Never infer: anything the list
does not cover that could change what a claim establishes is a `→ VERDICT` item. No
narration.

## 6. Sweep

Grep the corrected files for draft residue ("previously stated", "was corrected",
"the audit found", "on re-examination"…) and for bare section numbers ("§3.6", "§7.3",
"§4a") or bare row/finding IDs ("CL08", "C14") used as nouns without naming what they
refer to, and apply the reader test above. The sweep covers what a reader opens:
`SYNTHESIS.md` (except the verdict re-run's `## Counts` record of what changed),
the open items in `CHANGELOG.md`, and messages to the operator — not working files,
stage reports or logs. Anything left becomes TEXT items. The
`SYNTHESIS.md` header line carries the replication status and the verdict stage's
counts, never a one-word verdict on the paper:

`Replication: TRUSTWORTHY | OPEN | UNSOUND · <n> not established / <n> narrower / <n> hold`

`Replication:` rates the review's own evidence, never the paper; the paper's standing
is the counts and the verdict stage's bottom line. Set the word; leave the counts as
the verdict stage wrote them. `TRUSTWORTHY`: every load-bearing
script re-ran clean in this audit and matches the reports and, where the paper prints
the number, the print. `UNSOUND`: a load-bearing script still fails or still
disagrees with the reports after this audit's corrections. `OPEN`: anything else — a
load-bearing check blocked or not re-run, open items, or the audit `INTERIM`.

`CHANGELOG.md` closes with the dated corrections entry and the open items; it is
append-only across audits.

## 7. Handoff

Corrections close only when their consequences land: generated artifacts regenerated
by their scripts, dependent reports updated, any verdict re-run done. Then write
`HANDOFF.md` at the job root, once per audit; a later errata round amends it (new
inputs, status) and rebuilds the manifest:

- `status:` `COMPLETE` (only when `## conflicts` reads `none` and no claim-ledger row
  is `INTERIM`; list only finding-bearing conflicts there) / `INTERIM` /
  `BLOCKED`; a reason goes after a `#`;
- `audit:` the date of this audit's `CHANGELOG.md` entry;
- `## inputs` — every artifact the findings rest on: one file per bullet, as a bare
  path from the job root (a `§locator` or `# note` may follow);
- `## primaries` — the published article and appendix (and `review/extracts/`, which
  the quote check reads), each working paper relied on,
  the deposited code and data (files by hash, a directory by listing);
- `## excluded` — `path | disposition | evidence`, disposition one of `superseded`,
  `withdrawn`, `exploratory`, `unresolved` (bars COMPLETE) or `not-evidence` (e.g.
  `00_INTAKE.md`, `PROGRESS.md`); a stage or module report is an input unless a rebuilt report supersedes it
  (`superseded`, naming the replacement);
- `## conflicts`.

If `ERRATA.md` exists at the job root (routed back from `review-digest` with `FOR-AUDIT-REVIEW` items), verify that every finding-bearing item has been resolved in the reports (by a verdict re-run where step 3's test marks it `→ VERDICT`) and close it with `status: closed` and a `resolution: <CHANGELOG.md entry>` line before re-binding the manifest; `render_digest.py --finalize` refuses to run while any finding-bearing `ERRATA.md` item remains `status: open`.

Run `python3 build_manifest.py HANDOFF.md` (in the `review-digest` skill's `scripts/`) to
hash-bind it. If the handoff cannot honestly be completed, say so in its status.

Be direct: a FAIL softened to a "minor note", a gate forced green, or a mechanical
error left in place because fixing it would move a claim is the rubber stamp in
another form. When everything
the run got wrong is corrected in its own reports, you are done.
