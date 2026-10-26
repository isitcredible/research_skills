---
name: review
description: >-
  Review and replication of an academic paper. Reads the paper and its
  version history, audits the code against the text, executes the replication
  package, audits how the data were built, challenges every finding in a fresh
  context, and records what the evidence establishes claim by claim. Use when asked
  to review a paper, audit a draft, or start a replication.
metadata:
  version: "0.9.1"
---

# Review

Establish what the paper's evidence supports. The strongest form the critique takes
is *"the data and analysis do not provide good evidence for the claim"* — assert the
evidential gap, never the opposite claim; asserting the negation is the same
overclaim the review exists to catch. A full investigation that finds no fault is a
valid outcome, reported as survival.

The review establishes what is true; it rates nothing. Each claim is recorded as
holding, holding only in narrower form, or not established, with what survives. How
much a finding matters to a reader is decided when the digest is written.

## Rules that bind every stage

1. **The printed article is the record.** Check every PDF's title page (journal
   volume/DOI = published; series name + number = working paper; "Online Appendix" =
   OA). Every claim and number resolves to the published article and appendix,
   never to a working paper's values.
2. **Coverage is a list, not an impression.** The formula map, ledgers, manifest and
   claim ledger are the record of what was checked. "I looked carefully" is not.
3. **Every reported number traces to a saved script and its log** in the job tree,
   and each script is re-run clean before its number is cited.
4. **Every number, quote and page attributed to the paper is pinned to the printed
   cell or page** (`Table 3 col 2, p. 2246`) and checked against the page image —
   never against the package's output, a draft, or memory.
   A quote keeps its qualifying clause ("In our model", "of final goods"); dropping
   one attacks a claim the paper does not make. Numbers compared as like for like
   share specification, sample and clustering level; a comparison across them says
   what differs and draws no conclusion that needs them to match.
5. **A blocked stage still reads the print.** A result that cannot be re-estimated
   still has its printed cells checked; a printed null under the paper's preferred
   estimator is a finding that needs no code.
6. **A calculation the review builds itself is unvalidated until checked** — a
   corrected variant, a new control, a split, a recode, a resample. Where code
   ships, build it as a copy of the shipped code with only the defective lines
   changed (re-deriving from raw inputs silently drops the shipped sample rules).
   A defect in shipped data is repaired the same way: copy the shipped tree, change
   only the defective cells, run the shipped code unmodified, and save the data diff
   as the variant's patch.
   Always save a moments file (mean, sd, min, max, N of the corrected object and
   the outcome, before and after), and list every result family that uses it when
   it is shared (its `consumers:` line; see the code-and-data stage).
   A repair made only to get the authors' code to run is held to the same rule: run
   the unmodified code first and diff every output it produces; a repair that moves
   a number beyond the reproduction tolerance, or off the printed cell where the
   unmodified code cannot run, is a variant, never the deposit's result.
7. **Status words mean what they say.** `COMPLETE` = every applicable check ran and
   its output was inspected. `INTERIM` = required work the review can still do is
   unfinished (name it) — including a stage the harness cannot spawn and a source
   awaiting the operator's access. Work whose materials the authors never deposited
   is recorded *unverifiable as published*, a finding, not left `INTERIM`. A cited
   source still unobtainable after every acquisition tier, operator access
   included, is recorded `unverified-here` — a limit on the review, not a finding
   against the paper.
   `BLOCKED` = nothing can be anchored (give the exact evidence). Status rolls up:
   one `INTERIM` check makes its stage `INTERIM`, and one `INTERIM` stage report or
   claim-ledger row makes the run `INTERIM`.
8. **A test counted for or against the paper must be able to count.** Before a test
   the review runs or reads counts against a claim — or for it: a first stage called
   strong, an estimate called precise or robust, a check the claim "survives" —
   record three checks beside it. Evidence for the paper meets the same bar as
   evidence against it: a test that could not fail supports nothing, and strength or
   precision is stated at the inference level the design's literature requires,
   naming that level. A
   mismatch between print, prose and code is not a test and needs no power or
   specification check; it is checked against the paper's own disclosures and
   errata, and counts against a claim only once its effect on the printed cell has
   been run, where the code runs.
   - **Power against the paper's own estimate** (simulate where no formula exists).
     A test that would seldom reject were the paper right says nothing by not
     rejecting; a degenerate test says nothing at all. A null, ours or the paper's,
     is informative only for the range it excludes, never "exactly zero". An
     estimator whose weak-identification-robust set is unbounded measures no
     magnitude: it neither supports the paper's size nor refutes it. Write such a
     result as what the data cannot say, with its numbers: "the data cannot say
     whether X; the estimate is b, interval [l, u], which contains both zero and the
     paper's figure". Never a double negative ("cannot be distinguished from zero,
     and is not refuted"), and never a "not refuted" tag on a finding. This
     governs tests of the claim, not corrections of the paper's own estimate: under
     corrected inference or the paper's documented method, the claim keeps only the
     support the corrected estimate gives it, whatever the power. A correction is
     only the paper's own estimand under the inference the design's literature
     requires (it passes the next check), the paper's printed method implemented
     as written, or a repair of a defect in the paper's own construction (a code
     bug, a value mis-transcribed from the stated source) that leaves its stated
     sample rule, controls and estimand unchanged; any other change of sample,
     control, construction or estimand is a test.
   - **The specification the design's literature requires** (a shift-share
     shock leave-out keeps the exposure-sum control, recomputed on the remaining
     shares — with complete shares, the dropped shock's share; `shift-share-diagnostics`). A mis-specified test is the
     review's error, whatever it returns. Departing from the convention is
     legitimate only when a construction shows its premise fails in this design,
     with the conventional version reported beside it.
   - **What the paper already did.** A check it ran, or a choice it states and
     justifies, is engaged on its terms: rebut the check, or show the alternative at
     least as defensible in light of the stated justification; never count it as an
     omission. Its printed version of a test is evidence once it reproduces from the
     deposit; where the deposit cannot run it, it is unverified but still read on
     its printed terms. One that does not reproduce, or whose code does not do what
     the text says, is itself a finding.

9. **Few clusters or few shocks: jackknife first, WCR-S leads, randomization for
   shift-share.** THE WILD CLUSTER BOOTSTRAP IS NOT THE DEFAULT ANSWER TO FEW CLUSTERS,
   and plain `boottest` (WCR-C) is not how to run it. That is the training reflex, and
   it has put wrong p-values into the headline of finished runs.
   - When G* is small, lead with CV3 (re-fitting every control and non-cluster FE inside
     each leave-out; never partial out FEs once on the full sample).
   - The restricted bootstrap is second, with WCR-S (`boottest …, jk noci` at a null of
     zero, followed immediately by `assert !missing(r(p))` because a refused model
     returns `_rc = 0` and `r(p) = .`) as the cited variant. `boottest …, jk` is WCR-S
     only at zero, and `boottest` prints a confidence set by default for one hypothesis,
     so `noci` is mandatory; for a non-zero null or an Anderson–Rubin set, transform the
     outcome (`y − b₀·x` or `y − b₀·endog`) and test zero over a grid (`boottest …, ar`
     does not impose the null in its bootstrap DGP and fails the gate unless tagged
     `AR-boottest-robustness`). WCR-C is always run and reported beside WCR-S
     (MacKinnon–Nielsen–Webb advise computing both whenever CV1 and CV3 differ), never
     alone; their disagreement is part of the spread.
   - Few treated clusters or few effective shocks go to randomization inference and, in
     shift-share designs, the delete-one-shock jackknife (CV3).
   - Cite every bootstrap number with its variant.
   - In a shift-share design, report how often each unit-level test rejects placebo
     shocks (alongside the randomization p of the actual statistic and the shock-level
     jackknife) before any of its p-values counts.

   See the small-n and shift-share modules. `scripts/check_inference.py` must pass.
10. **Name the substance, never a bare locator or ID.** Every report, `SYNTHESIS.md`,
    and message to the operator is written for a reader who does not hold the paper's
    table of contents, the stage reports, the cribs, or this skill's section numbers in
    memory. Name what you are referring to in words — "the wage simulation (Section 3.6,
    p. 48)", "the microcredit application (Section 7.3, p. 35)" — never a bare section
    number ("§7.3", "the §3.6 results", "matches §3.4"), a review-internal section
    ("Stage 1 §2", "CALIBRATION §4a", "crib §2"), or a bare claim or finding ID
    ("CL08", "C14") as a noun. A section number, page, or ID may follow in parentheses
    as a locator after the thing has been named, never stand in for it.

## Intake

Rename the packet files at the job root so they sort first:

```
01_paper_<authors>_<year>_<journal>.pdf
02_online_appendix_<authors>_<year>.pdf
03_working_paper_<authors>_<year>_<series>_v<n>_<yyyy-mm>.pdf   # every dated draft the paper stage's search finds
04_replication_<authors>_<year>/                                # unzipped, never edited
lit/<Author>_<Year>_<ShortTitle>.pdf                            # other papers
```

- **Required: the published article and its online appendix** whenever the paper has
  or cites one (search for "online appendix", "supplemental materials", and A1/S1
  tables missing from the main PDF). A missing article or appendix stops the run:
  tell the operator what is on disk (unattended — no operator available to answer: write `BLOCKED — MISSING: <file>` in
  `00_INTAKE.md` and end). An appendix the paper cites but never published
  (established by search) does not stop the run: record it, and treat results
  resting on it as unverifiable as published.
- **No published version exists** (established by searching RePEc, SSRN, author sites
  and Wayback): the newest dated working paper is the version of record. Say so in
  `00_INTAKE.md`.
- **A missing or partial replication package does not stop the run.** Record
  `Deposit: partial` or `Deposit: none` with what the deposit actually contains, run
  the bounded acquisition pass (`references/source-protocol.md`), and run
  everything that needs no code. A claim whose materials were never deposited is
  *unverifiable as published* — a finding, not a gap.
- **When a package ships**, run
  `python3 <review skill>/assets/deposit_inventory.py 04_replication_*/ --out review/deposit-inventory.json`
  first. Classify each file by the content the script probes, never by its filename.
- Write `AGENTS.md` at the job root (heading, objective, packet list) and `00_INTAKE.md` (inventory, deposit status, version of
  record, and `Suite version: <x>` copied from this skill's `metadata.version`, so a
  later audit knows which requirements the run was given). `review/extracts/` holds the pdftotext dumps of the packet and of every
  `lit/` work the review quotes — later quote checks read only these.

## Job tree

```
<job>/
├── 00_INTAKE.md · AGENTS.md · PROGRESS.md · packet files · original archives ·
│                  inference-superseded.csv (only where scripts are declared superseded)
├── review/            paper-REPORT.md · code-and-data-REPORT.md · claims-REPORT.md · challenge-REPORT.md ·
│   │                  deposit-inventory.json
│   └── extracts/      pdftotext dumps of the packet and of every quoted source
├── analysis/
│   ├── paper/         drift-table.md · robustness-claims.csv
│   ├── code-and-data/ formula-map.csv · feasibility-matrix.csv · construction-ledger.md ·
│   │                  battery-manifest.csv · results.csv · source-coverage.csv ·
│   │                  data-findings.csv · module-walk.md · <module>-REPORT.md
│   └── claims/        driver-matrix.csv · claim-ledger.csv
├── work/              pkg/ (working copy of the deposit) · scripts/ · logs/ · results/ · challenge/
└── SYNTHESIS.md       the verdict stage's deliverable (ISSUES.md + DIGEST.html land here later)
```

`04_replication_*/` stays untouched; repairs and re-runs happen in `work/pkg/` with
diffs saved. The inference gate (`scripts/check_inference.py`) reads `work/pkg/` as
the authors' code and skips it, so a bootstrap the review adds or re-specifies runs
from `work/scripts/`. All computation lives under `work/` — never `/tmp`.

## Stages

Run in order. Each stage is its own job: open its `SKILL.md` and produce its report
and artifacts. Applicability is decided per result family (`NOT_APPLICABLE` with a
reason), never for the paper as a whole.

1. **`paper/`** — no code. The version history (what moved between drafts), the
   printed-table consistency pass (do the printed cells support the prose?), and the
   research-design critique (identification, confounders, controls).
2. **`code-and-data/`** — the code read against the text (with the formula map), the
   package executed and its anchors reproduced, the data audit, and the fragility
   battery with its design-specific modules.
3. **`claims/`** — the claim ledger: for each load-bearing claim, how central it is,
   whether it holds, what survives and what is not established, and the strongest
   defence. Provisional until the verdict stage.
4. **`challenge/`** — required before any verdict. A fresh agent on the model the
   operator's routing assigns to verdicts, never the context that wrote the stage
   reports (one agent per group of result families where the run is large), gets
   `challenge/SKILL.md`, the packet, and the evidence under test: every claim-ledger
   row verbatim, every finding in the stage and module reports, and every calculation
   the review built itself that a finding rests on, each with its evidence paths in
   both directions. It rebuilds what it tests from the pristine deposit and the
   printed page, and rules on each element in both directions: STANDS, STANDS WITH
   CHANGES, WRONG or ADD. It rules on evidence only. Before a WRONG or STANDS WITH
   CHANGES ruling is relied on, a worker re-runs its load-bearing script and opens
   the page it cites. Without `review/challenge-REPORT*.md` the run is `INTERIM`. A
   run made before this stage existed gets it when it next feeds a publication or is
   next audited.
5. **`verdict/`** — one fresh agent on the verdict model, given `verdict/SKILL.md` and
   the inputs it names, writes `SYNTHESIS.md`: the final claim ledger, the
   design-level findings, the bottom line, the estimator table, the data-integrity
   rung, the findings, and the counts. It never sees the coordinator's reasoning.
   Nothing re-decides after it. Without it the run is `INTERIM`.

## Stage reports

Each stage writes `review/<stage>-REPORT.md` from `assets/report-template.md` (challenge uses its own format). The
report is also the handoff to later stages: findings, leads for later stages, and
**scope assumptions** — limits a stage relied on ("the deposit cannot run the main
table", "all inputs are synthetic"). A later stage that overturns a scope assumption
re-checks, or flags, every conclusion that rested on it.

## Progress file

Runs die mid-stage — the machine sleeps, a session ends, a spawn fails — and the next
session cannot tell finished work from abandoned work by looking at the tree.
`PROGRESS.md` at the job root is how it tells. Create it at intake; update it after
every stage and every fired module, and before any long computation starts:

- **Done** — each finished stage or module, with the exact paths of what it wrote.
- **Running** — live computations: command, log path, start time.
- **Decisions** — calls made by rule while unattended, each pointing to the artifact
  that records it.
- **Tried and failed** — every approach abandoned: a package repair that did not
  build, an estimator that would not converge, a source that could not be obtained.
  Say what was tried, the exact error or result, and why it was dropped. Do not
  repeat an approach listed here unless something relevant has changed, and say what.
- **Next** — the one concrete step that resumes the work.

On resumption, read `PROGRESS.md` first, then confirm every path under Done exists
and every process under Running is alive or finished (`ps`, log tail). A Done entry
whose files are missing is not done. `PROGRESS.md` is plumbing: nothing from it goes
into `SYNTHESIS.md`.

## Running it

- Commands run from the job root; `<review skill>` is this skill's directory.
  `python3` in every command, in this skill and its stages, means a Python 3.10+
  interpreter with the packages the README lists — not necessarily the system
  `python3`.
- Dispatch each stage, and each fired diagnostic module, to its own subagent where the
  harness supports it; otherwise run them as serial passes. Check what exists before
  spawning — a module dropped because a spawn failed is a silent gap. Module agents
  follow the code-and-data stage's protocol for separate modules (its Modules check).
  How to size, route and run those agents: *Agents and cost* below.
- One continuous run. The only sanctioned pause is the missing article/appendix stop.
  Unattended, resolve every other question by rule: record the call and the reason in
  the artifact it touches, and continue.
- Size long computations to the machine (sampling, capped repetitions), launch them
  with start/end markers, and before assigning any status check for live processes
  tied to the job (`ps`, log mtimes). Synthesis written over live compute is `INTERIM`.
- Inference charges are quantified: "the SEs are wrong" comes with the re-estimated SE
  ratio and whether significance flips — never from reading code alone. Where the
  data were never deposited, state the design error and the cluster count from the
  print, and give a design effect only at a stated intra-cluster correlation, as a
  sensitivity, labelled unquantified.
- A tight SE covers sampling error only. Where measurement or specification error
  dominates, say what the interval leaves out.
- Worked examples of the procedures: `references/worked-cases.md`. Methods notes:
  `references/methods/`.

## Agents and cost

What a run costs is set by how long each agent lives, not by how much it writes:
every step re-reads the agent's whole context, so one long agent costs several times
what the same work costs split across short ones. None of this rations checking —
every check the stages require still runs.

"The operator's routing" below is whatever the operator or the harness sets for which
model handles which kind of task; where nothing is set, every agent uses the session's
model.

- **Route by kind of task.** *Mechanical* tasks — acquiring and filing sources,
  rendering and reading printed pages for a print check, re-running scripts and
  diffing their logs, building coverage and bookkeeping artifacts, migrating an old
  run's records — go to the model the operator's routing assigns to mechanical
  subagent work. *Judgement* tasks — every stage report and module report, the claim
  ledger, the challenge stage and the verdict stage — go to the model the routing
  assigns to verdicts. A mechanical worker reports what it found (match or mismatch, the number,
  the file); it does not rate a claim or decide what a finding means. Where the
  routing is silent, both kinds go to the session's model.
- **Brief each agent for one bounded job** — a module, a group of result families, an
  acquisition list — that it can finish in well under a hundred tool calls. An agent
  past about eighty calls with work left writes its findings to their files and its
  state to `PROGRESS.md`, and stops; a fresh agent resumes from `PROGRESS.md`.
- **The coordinator stays thin.** The agent that dispatches stages and modules reads
  their reports and the gate outputs, not their logs, scripts or page images. A check
  it needs on a worker's output goes to another worker.
- **A subagent the harness bars from writing files** returns its report text in
  full; the coordinator saves it unchanged at the report's path.
- **Never hold a large context across a wait.** The cache that makes re-reading cheap
  lapses within minutes of idleness, and an agent that blocks on a long computation
  pays to rebuild its whole context afterwards. Size each computation to finish in
  under about four minutes. Run anything longer in the background, with start and end
  markers in its log, and work on something else meanwhile — or record it under
  Running in `PROGRESS.md` and stop, so a fresh agent picks it up from the log. A
  coordinator waiting on subagents does not poll their output.
- **Read results, not dumps.** Everything an agent reads stays in its context for the
  rest of its life. Inspect logs with `tail` and `grep`, tables by the rows and
  columns needed, long files by section; send bulky output to a file and read its
  summary line.
- **Text first, then the page.** Locate quotes and numbers in `review/extracts/`
  first. Where a rule requires the page image, render only the page that carries the
  cell or passage, cropped to the table or paragraph with its headings and notes.
