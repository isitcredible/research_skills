---
name: review-digest
description: >-
  Compile a completed `review` run into the evaluator-facing issue ledger (`ISSUES.md`)
  and render it as a self-contained HTML digest — a ranked, categorized issue list for
  human evaluators. Use when asked to "make the reviewer digest", "write the issues
  file", "render the review", or produce an evaluator-facing version of a review.
metadata:
  version: "0.9.1"
---

# Review digest

Turns a `review` run's output into the artifacts evaluators read:

- **`ISSUES.md`** — the normalized issue ledger (authored here, gated here).
- **`DIGEST.html`** — rendered mechanically from the ledger, never hand-written.
- **`ERRATA.md`** — the defect ledger for upstream artifacts (internal).

Two rules shape everything: **extraction, not re-adjudication** — whether each claim
holds, what survives, evidence status, and what counts as a finding come from
`SYNTHESIS.md` and stage reports as they stand (no silent promote/merge/drop — a
finding that looks wrong is an `audit`-class errata item, not an in-place fix); and
**the digest's subject is the paper, never the review's process** — no rendered sentence reports what was suspected, checked,
corrected, or discarded; instrument names, review artifacts (reports, ledgers, logs,
scripts the review wrote), review-internal section references, and row-IDs never
render (provenance lives in `sources:`) — a deposit file or a file the paper names may
render, as part of the evidence; and a paper
section is named by its substance ("the wage simulation (Section 3.6, p. 48)"), never
by a bare section number ("the §3.6 simulation", "in §7.3"). Because the upstream
register is adversarial, the
compile runs a fairness pass (no motive/intent framing without documentary evidence)
and a prose pass (no machine register) before the ledger finalizes.

**Severity is assigned here, as a reading aid.** The review records what is true and
rates nothing. Each issue's severity tag tells the reader where to look first; it is
derived from the truth ledger by the default below, and the compiler may depart from
the default only with a stated reason (see "Severity").

**The failures-only rule** (binds all rendered prose): no sentence reports that a
verification or reproduction check *succeeded* — success is the baseline, not a
finding. State the bare fact; a *failed* check is a fact about the paper or deposit.
A claim the review could not test, or whose materials were never deposited, is a
failed check: it is always stated, so silence about a result means it reproduced. A
source the review itself could not obtain (`unverified-here`) is a Caveat about the
review's reach, never an issue against the paper.

## Steps

Commands run from the job root — the folder holding `SYNTHESIS.md`, where `ISSUES.md`,
`HANDOFF.md`, `ERRATA.md` and the ruling files live (not its `review/` subfolder); every
script resolves paths against the folder of the ledger or handoff it is given. `scripts/`
is this skill's directory. The renderer needs the `mistune` Python package. The prose
gate uses the engine of the `ai-sweep` skill nested in this one (`ai-sweep/`). The fairness gate's passage scanner is
optional and operator-configured: `PASSAGE_SCANNER` names its executable, and nothing
else is looked up. When the engine or the scanner is absent the gate's manual pass is
the gate, recorded, never skipped: `FAIRNESS.md` and `ISSUES.keeps.md` are then always
written, each carrying `gate: manual pass — <date> — sha256:<first-12>`, keeps or not.

0. **Staleness check** — a `HANDOFF.manifest.json` is the declared evidence set, and
   staleness is judged by its hashes: an accepted input that no longer matches is
   stale. Mtime order (ISSUES < SYNTHESIS < stage reports < newer result files) is a
   hint only — an audit legitimately re-runs scripts and corrects reports after
   SYNTHESIS. CHANGELOG entries postdating artifacts, uncited newer evidence →
   `ERRATA.md`. `DIGEST.html` carries build metadata;
   `python3 scripts/render_digest.py ISSUES.md --stale-check` reports CURRENT/STALE
   (before the first render it prints `NO DIGEST`, as expected). `sources:` must
   resolve inside the manifest's set. Stale evidence (an upstream artifact older than what it summarizes, or an
   accepted input changed since the handoff, on which `--finalize` refuses) stops the
   digest short of final: report it for the run's owner to route back to
   `audit-review`. An INTERIM run is not stale: it compiles and renders as a preview,
   never final. Skill-owned files
   (`ISSUES.md`, `DIGEST.html`) regenerate freely; other skills' files are never
   deleted or regenerated — a *defect* goes to Errata, staleness is reported.

1. **Compile `ISSUES.md`** (format below) from `SYNTHESIS.md`, stage reports, module
   reports and the claim ledger. Numbers and paper-claims
   enter only from stage reports — never paraphrased fresh from the paper. Summary
   counts and Assessment tallies are arithmetic over the ledger.

2. **Fairness gate** — `python3 scripts/check_fairness.py ISSUES.md` (the fairness
   battery `fairness-questions.json`, scored by the passage scanner; `PASSAGE_SCANNER`
   unset → manual whole-ledger pass, recorded — never skipped). Every flagged passage resolves: **keep** only with
   intent-evidence in the corpus (correspondence, dated referee report, explicit
   statement, a documented rejected alternative) — recorded in `FAIRNESS.md` as the
   kept wording in backticks (15+ characters) plus `evidence: <file>:<line>[-<line>]`
   or `evidence: <file> §<section>` (path from the job root, lines that exist), the
   field ending its line or closed by `;`; one line per keep, or a `### ` entry whose
   `evidence:` covers its phrases. A keep missing either leaves the passage flagged;
   a keep clears only the sentence it names. Otherwise **rewrite to the descriptive
   claim** (what was done + measured effect + documentation status; chronology and
   asymmetric choices are correlation, never motive). A rewrite changes only the wording that attributes motive, never the
   finding, its numbers or its severity, and keeps every caveat the original carried.
   Equally, no rewrite clears the paper beyond what upstream established: a sentence
   on integrity states, as facts about the paper's evidence, what the integrity
   evidence covers and what it does not (which records were and were not deposited),
   never a list of the review's checks; and "not shown to change" is never written as
   "does not change".
   Re-run to exit 0.

3. **Prose gate** — `python3 scripts/check_style.py ISSUES.md` — machine-register and
   failures-only sweep over rendered prose. Resolutions: rewrite to fact-delivering
   prose, or record the keep (`ISSUES.keeps.md`, `backticked` phrase + reason).
   Scanner missing/stalled → manual whole-ledger pass, recorded — never skipped.

4. **Fact-check gate** — `python3 scripts/check_facts.py ISSUES.md`: every quoted span
   must resolve in a primary source (the packet extracts, the deposit, cited works —
   never the review's own prose) and every number in the accepted corpus (with
   `HANDOFF.manifest.json`, inside its accepted set; before one exists, anywhere under
   the job root — a preview standard, since `--finalize` requires the manifest). A quote
   with an elision gets a disposition in `ISSUES.facts.md` confirming no negation or
   qualifying clause was dropped. The judgment pass then confirms per hit: same quantity (level vs
   growth, % vs pp, stock vs flow), verbatim or unquoted, no precision upgrades, derived
   numbers name their derivation. Claim-level items the sweep can't see (spec
   attributions, bounds-as-ratios, mechanism claims) get a one-line disposition in
   `ISSUES.facts.md`. Also: **attribution** — external works are named at point of use
   and carry a `## References` entry; a gloss answers to the deposited version.
   **Summary-evidence** — accurate-but-misleading selection is corrected; material
   exceptions travel with the conclusion wherever stated.

5. **Coverage gate** — `python3 scripts/check_ledger_coverage.py ISSUES.md`: every *declared*
   upstream finding (claim-ledger rows that do not hold — `narrower` or `not
   established` — design-level findings, finding blocks in SYNTHESIS and reports,
   untested or unverifiable claims) maps to an issue or gets a disposition in
   `ISSUES.coverage.md`, one line each:
   `` `finding phrase` → issue N ("title words") `` (or `→ issues N ("…"), M ("…")`
   for a row that bears on several issues: it maps to the issues that carry its stated
   not-established reason, and sets each one's default; the quoted words come from the
   issue's title, so a renumbered or retitled ledger re-opens the ruling) · `→ caveats` · `→ avenues` ·
   `— excluded: <reason>` · `— contested: FOR-AUDIT-REVIEW` (a finding you believe
   wrong; blocking). The fresh coverage pass writes these dispositions; the compiler
   may propose, never rule. A dropped finding is added to the ledger by extraction. A
   `headline` or `supporting` row that does not hold is never sent to caveats, avenues
   or exclusion, except as `excluded: superseded twin of issue N`. The gate also
   computes each issue's default severity from the rows mapped to it and lists every
   departure; a departure without a `severity-reason:` FAILs. The denominator is
   declared findings only; a finding upstream never wrote down is `audit-review`'s
   completeness gap.

6. **Render + finalize** — `python3 scripts/render_digest.py ISSUES.md` (preview) then
   `--finalize`,
   which refuses over: no `status: COMPLETE` in the ledger, missing/drifted
   `HANDOFF.manifest.json`, sources outside the accepted set, undeclared report-class
   files, open `finding-bearing` errata, or gates unruled on this ledger revision.
   INTERIM renders as preview only. Report-class = every other `*.md` at the job root
   and every `*-REPORT.md` below it. Apparatus — `ISSUES.md`, `ERRATA.md`, `FAIRNESS.md`,
   `CHANGELOG.md`, `HANDOFF.md`, `HANDOFF.manifest.json`, `ISSUES.keeps.md`,
   `ISSUES.facts.md`, `ISSUES.coverage.md`, `README.md`, `AGENTS.md`, `CLAUDE.md`,
   `STYLE.md`, `MEMORY.md`, `VALIDATION.md`, `00_INTAKE.md`, `PROGRESS.md` — is never
   report-class and never needs declaring; a `not-evidence` exclusion of one (the
   audit's usual `00_INTAKE.md`, `PROGRESS.md`) is accepted and changes nothing.

7. **Verify** — `--stale-check` CURRENT; open `DIGEST.html` (issues in the order the case needs, bodies
   carry substance, no markup corruption); **bottom-line check** — Summary+Assessment
   convey SYNTHESIS's bottom line, "What the paper establishes and what it does not",
   led by the same finding and no softer than it; a different bottom line is
   `FOR-AUDIT-REVIEW`, never a reorder; **reader-gate** — every
   rendered sentence's subject is the finding, not the review's activity.

**Judgment-pass independence:** the fact, coverage, and step-7 verify passes run
fresh-context where the harness dispatches (record `gate: <context> — <date> —
sha256:<first-12>` in `ISSUES.facts.md` / `ISSUES.coverage.md`, where `<first-12>` is
the first 12 hex digits of the sha256 of `ISSUES.md` as gated — any later ledger edit
voids the record; a `fresh-context`
record also names the subagent's saved output file — each fresh agent saves its own
record under `work/digest/`, the file its `gate:` line names; the step-7 verify record
is `work/digest/verify-pass.md`, ending with its `gate:` line), else the operator, else
in-context recorded as the limitation it is — in-context where dispatch existed is a
process violation. Fairness/prose stay
in-context; their keeps are externally checkable.

## Errata — bounded upstream fixes

`ERRATA.md` beside `ISSUES.md`, cumulative, items never deleted:

- **errata** — patched here: mechanical slip, correct value provable in the corpus,
  prose artifact only, touches no finding/severity/ranking/status. Never patch
  `SYNTHESIS.md` or generated artifacts (regenerate via the owning script). Minimal
  `old → new`, logged, + one dated `CHANGELOG.md` line.
- **audit — `FOR-AUDIT-REVIEW`** — re-adjudication: upstream contradictions,
  questions about whether a claim holds or its status, report↔synthesis conflicts
  (the audit routes these to the review's verdict stage). File `file · loc · old → new`
  + conflicting evidence; `SYNTHESIS.md` is never patched.
- **operator — `FOR-OPERATOR`** — preference/scope calls, filed with the decision needed.

Each item is a `### ` block; the gates read two fields (any key case; a list bullet or
bold is tolerated):

```markdown
### E3. Table 2 header mislabels the outcome
status: open          # open | closed
finding-bearing: no   # yes | no
resolution: <CHANGELOG entry>   # on closing, its own line beside status: closed
```

`finding-bearing: yes` only when the item could change a claim row's `holds` or
kernel, a design-level finding, or the bottom line. A slip inside a finding block that
leaves its conclusion unchanged is `finding-bearing: no` — routed `FOR-AUDIT-REVIEW`
where it sits in `SYNTHESIS.md`, but not blocking. An `open` item blocks `--finalize`
unless `finding-bearing: no`. The ledger meanwhile
states only what the corpus supports: a ledger sentence that copied an upstream error
is fixed in the ledger, and the upstream error goes to `ERRATA.md`. Material
evidential limits belong in Assessment
**Caveats** as facts about the deposit or design — never a diary of the audit. This
skill never invokes `audit-review`; the run's owner decides whether to fire it, then
the digest re-runs.

## ISSUES.md format

```markdown
---
paper: <Authors> <year>, "<Short title>" (<Journal>)
verdict: Replication: <TRUSTWORTHY|OPEN|UNSOUND> · <n> not established / <n> narrower / <n> hold   # internal — never rendered; copied from the audited SYNTHESIS header (OPEN before an audit); no one-word verdict on the paper
status: COMPLETE | INTERIM | BLOCKED   # copied from SYNTHESIS.md's status line — never rendered; --finalize needs COMPLETE here and in HANDOFF.md
date: <yyyy-mm-dd>   # internal record, optional
---

## Summary
One orientation paragraph, then **Headline claims under review** — one bullet per
`headline` row of the claim ledger, verbatim or from the ledger (never loose abstract
paraphrase).

## Issues                # required even when empty

### 1. <Issue title>
severity: High|Medium|Low    # assigned here: the default from the rows mapped to this issue (see "Severity"), or a departure with a reason
severity-reason: <one line>  # required only when severity departs from the default — internal, never rendered
category: <Research design|Data & measurement|Statistical inference|Reproducibility|
           Framing & claims|Reporting>
evidence: established|strong|plausible|unresolved   # internal
summary: <optional one line>
sources: <;-separated paths relative to the job root — internal>

Body: 1–4 paragraphs of technical substance — the numbers, printed-vs-found, where the
evidence lives. Code-span notation containing `*` or `_`.

## Assessment
What the issues add up to — the top-ranked finding opens it (what fails, under what
change, what survives), the closing sentence states what it establishes. Then
**Avenues the evidence leaves open** (open questions, never instructions) and
**Caveats** (bounds on what findings establish — omit if none).

## References            # whenever external work is relied on
One Harvard entry per external work used; the reviewed paper needs none; every entry
is cited at point of use.
```

`evidence:` grades the upstream support, not the severity: `established` — read in
print or reproduced from the deposit; `strong` — several independent upstream checks
agree, none decisive alone; `plausible` — an upstream inference consistent with the
record, not tested directly; `unresolved` — the review could not test it (materials
missing, check infeasible).

Ranking is file order, and it follows the logic of the case, not the tag. The issue
carrying the finding that leads SYNTHESIS's bottom line comes first. After it, an
issue comes before the issues that rest on it (a design or data finding before the
claims it undermines); where nothing orders two issues, follow the order in which the
paper makes the claims they bear on. Severity tags need not descend with rank: the tag
says how much an issue matters, the order says how to read the case. `status:`/`evidence:`/`sources:` and front-matter `verdict:`
are internal fields — never rendered (as is `severity-reason:`); `###` titles, each
issue's `severity · category` tag line and `summary:` lines render.

## Severity

A reading aid: the tag tells the reader where to look first. It carries no weight
anywhere else, and it is never an argument about what is true — that is the truth
ledger's job.

**Default.** Each issue takes the most severe default among the claim-ledger rows
mapped to it in `ISSUES.coverage.md`. A design-level finding carries no row of its
own: map the rows it bears on to the issue directly.

| Row's `holds` | `headline` | `supporting` | `peripheral` |
|---|---|---|---|
| `not established` | High | High | Medium |
| `narrower` | Medium | Medium | Low |

An issue mapped to no claim row defaults to Low; a data-integrity finding at rung (3)
undisclosed discretion or above is rated High, with that as its `severity-reason:`.

**Departures.** Write the severity a careful editor would give, and where it differs
from the default add `severity-reason:` in one line, naming the fact that justifies it
(for example: "the narrower kernel is the paper's whole contribution"). The coverage
gate lists every departure; nobody adjudicates them, but a run of departures in one
direction is visible at a glance. The fairness and prose passes never change a
severity.
