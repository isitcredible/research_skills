# research_skills

Agent skills developed by The Catalogue of Errors Ltd
([isitcredible.com](https://isitcredible.com)). Each top-level folder is one skill.
More will be added; for now the repository holds three, which together review a
research paper.

| Skill | What it does |
| --- | --- |
| `review` | Reviews a research paper against its evidence and records, claim by claim, what that evidence establishes. |
| `audit-review` | Audits a finished review mechanically and corrects it. |
| `review-digest` | Turns the audited review into a ranked issue list for human evaluators. |

## The review skills

Given a published article, its appendix and its replication package, `review` reads
the paper and its earlier drafts, audits the code against the text, re-runs the
deposit, challenges every finding in a fresh context, and records what the evidence
establishes, claim by claim. `audit-review` then checks the review, and
`review-digest` turns the audited result into a ranked issue list.

Version 0.9, the first public release. Below 1.0 the requirements may still change;
[`CHANGELOG.md`](CHANGELOG.md) summarises each release and `review/spec-changes.csv`
records every change by version. The three skills share one
version, recorded in each `SKILL.md`'s frontmatter; `audit-review` reads
`review/spec-changes.csv` to list what an older run was never asked to do.

### What each skill does

| Skill | What it does |
| --- | --- |
| `review` | The review itself, in five stages. `paper`: version history, printed-table consistency, research design. `code-and-data`: code against text, reproduction, data audit, fragility battery. `claims`: the claim ledger. `challenge`: a fresh agent rebuilds the evidence from the untouched deposit and tests it in both directions. `verdict`: one fresh agent decides, claim by claim, what the evidence establishes, and writes `SYNTHESIS.md`. Fifteen diagnostic modules (IV, DiD and event studies, RDD, shift-share, few clusters, spatial and time-series dependence, and others) fire where the design calls for them. |
| `audit-review` | A mechanical audit of a finished review: completeness, re-runs, the print, the right log rows, propagation, traceability. It corrects the reports in place, sends any correction a claim rests on back to the verdict stage, and writes `HANDOFF.md`, the evidence the digest may cite. It rates no claim. |
| `review-digest` | Compiles the audited review into `ISSUES.md` and a self-contained `DIGEST.html`, behind gates for coverage, facts, fairness and prose register. Its prose gate runs the engine of `ai-sweep`, a skill nested inside it (`review-digest/ai-sweep/`) that also works on its own, sweeping any prose for machine-register filler and exposed working. |

### What the review records

The review establishes what is true and rates nothing. Each load-bearing claim of the
paper is recorded with:

- **centrality**: `headline`, `supporting` or `peripheral`, read from where the claim
  sits in the paper;
- **holds**: `holds` (as printed), `narrower` (the claim's point stands only in a
  narrower form, stated as the kernel), or `not established` (its evidence does not
  deliver it). "Not established" is the finding: the burden is the paper's, and the
  review never writes "refuted" unless an estimate excludes the claim;
- **kernel** and **not established**: what the evidence supports, and what the claim
  asserts beyond it;
- **status**: `settled`, `INTERIM`, `untested`, `unverifiable` (the authors never
  deposited the materials) or `unverified-here` (a source the review could not
  obtain).

Severity is assigned only in the digest, as a reading aid: a default from each issue's
claims (not established on a headline or supporting claim is High, and so on down),
from which the digest may depart with a stated reason. The digest orders its issues by
the logic of the case, not by severity.

### Installation

The skills change often, so install them from a clone of this repository and link
them into your agent's skills directory. An update is then one `git pull`. Set
`SKILLS_DIR` to the directory your agent reads skills from:

```
git clone https://github.com/isitcredible/research_skills.git ~/research_skills
ln -s ~/research_skills/review ~/research_skills/audit-review ~/research_skills/review-digest "$SKILLS_DIR"/
```

The three skills must sit **side by side** in the skills directory:

```
skills/
├── review/
├── audit-review/
└── review-digest/
```

The layout matters: `audit-review` and `review-digest` call the `review` skill's
scripts by name. To use `ai-sweep` on its own as well, link
`review-digest/ai-sweep/` into the same directory. If your agent does not follow
symbolic links, copy the folders instead and copy them again after each update.

### Updating

```
git -C ~/research_skills pull
```

[`CHANGELOG.md`](CHANGELOG.md) lists what each release changed. Update between runs,
not in the middle of one: each run records the suite version it was made under, and
`audit-review` reads `review/spec-changes.csv` to list what an older run was never
asked to do. To hold a project at one release, check out its tag in the clone
(`git -C ~/research_skills checkout v0.9.1`); `git -C ~/research_skills checkout main`
returns to the latest.

### Requirements

- Python 3.10 or later. Python packages: `mistune` (the digest renderer) and `pytest`
  (the gate test suites). Everything else uses the standard library. Where the skills
  write `python3`, they mean a Python 3.10+ interpreter with these packages installed,
  which may not be the interpreter the operating system provides: a virtual
  environment's interpreter is fine, used in place of `python3` throughout.
- Poppler's `pdftotext` and `pdfinfo` on `PATH` (the paper extracts and the
  printed-surface checks).
- Whatever the replication package needs: Stata, R or Python, with the packages its
  code loads. Few-cluster inference uses `boottest` in Stata and `fwildclusterboot` or
  `wildboottest` in R and Python; spatial pre-whitening uses R
  (`review/assets/prewhiten.R`).
- An agent harness that can start fresh subagents. The challenge stage and the verdict
  stage must run in contexts that never saw the work they test; without that the run
  is marked `INTERIM`. The digest's fact, coverage and final checks should also run in
  fresh contexts.

Optional: a typed-judgment passage scanner. When the environment variable
`PASSAGE_SCANNER` names one, the digest's fairness gate and `ai-sweep`'s register scan
use it. When it is unset, both gates run as a recorded manual pass. The scanner is any
executable called as `<scanner> scan FILE --questions BATTERY --output DIR
--chunk-chars N --overlap N` that splits FILE into passages, answers the battery's
questions for each, and writes `manifest.json` (the passages), `summary.json`
(completion and coverage) and one file per passage under `judgments/`, each holding
`response.answers` keyed by question. The full contract is in the docstrings of
`review-digest/scripts/check_fairness.py` and
`review-digest/ai-sweep/scripts/ai_sweep.py`.

### Running a review

1. Put the paper in a job folder: the published article, its online appendix, any
   working papers, and the unzipped replication package (the `review` skill's intake
   section gives the file names).
2. Ask the agent to review the paper. The run writes its stage reports, ledgers and
   `SYNTHESIS.md`, and gates itself with `review/scripts/check_manifest.py` and
   `review/scripts/check_inference.py`.
3. Ask the agent to audit the review (`audit-review`). The audit corrects the reports,
   re-runs the verdict stage on anything a claim rests on, and writes `HANDOFF.md`,
   hash-bound by `review-digest`'s `build_manifest.py`.
4. Ask the agent for the digest (`review-digest`). `render_digest.py --finalize`
   refuses until every gate passes on the current ledger, every cited input still
   matches its handoff hash, and no upstream error the digest found is still open.

A long run is resumable: each stage writes its state to `PROGRESS.md` at the job root.

### What the statuses mean

- **Run status** (each stage report and `SYNTHESIS.md`): `COMPLETE` means every
  applicable check ran and its output was read. `INTERIM` means work the review can
  still do is unfinished, and it is named: a live computation, a source awaiting
  access, a stage that could not be started in a fresh context. `BLOCKED` means nothing
  could be anchored, with the exact evidence.
- **Claim status**: `unverifiable` is a finding about the paper (the authors never
  deposited the materials); `unverified-here` is a limit on the review (a source it
  could not obtain).
- **Replication** (the `SYNTHESIS.md` header, set by the audit) rates the review's own
  evidence, never the paper: `TRUSTWORTHY` (every load-bearing script re-ran clean and
  matches the reports and the print), `UNSOUND` (one still fails or disagrees after
  correction), `OPEN` (anything else, including data the authors did not deposit).
- **Digest**: `render_digest.py` writes a preview at any time; `--finalize` writes the
  final digest only when the review is `COMPLETE`, the handoff is current, every gate
  has passed on the exact ledger revision, and no upstream error the digest found is
  still open.

### Limits

- A full review of a published paper is long: many agents, several hours of compute
  and model time. The skills split the work into bounded agents, but they do not make
  it cheap.
- One agent decides the verdict. Two runs on the same evidence can differ at the
  margin, mostly on whether a claim is `narrower` or `not established`.
- Without a passage scanner, the fairness and prose gates are manual passes, recorded
  as such.
- What the review cannot run (undeposited data, unobtainable sources) is recorded,
  never guessed: a review of a paper with proprietary data will mark much of it
  unverifiable.
- Some procedures are named in Stata or R terms (a Stata command, an R package), and
  some R or Python packages may be missing on your system or fail on edge cases (a
  model with a single regressor, a handful of distinct values, a degenerate fit). The
  skills then require the procedure to be hand-coded from its definition and the
  substitution stated in the report.

### Tests

Each skill's `scripts/tests/` folder holds its tests. Run them from the repository
root; `-p no:cacheprovider` keeps pytest from leaving a cache folder inside the
skills:

```
python3 -m pytest -q -p no:cacheprovider review/scripts/tests review/assets/tests audit-review/scripts/tests review-digest/scripts/tests review-digest/ai-sweep/scripts/tests
```

## Licence

MIT. Copyright (c) 2026 The Catalogue of Errors Ltd ([isitcredible.com](https://isitcredible.com)).
