---
name: ai-sweep
description: >-
  Sweep a piece of writing for machine-register prose AND for exposed
  plumbing — stock AI filler ('it is worth noting', 'delve', evaluative
  adverbs), rhetorical scaffolding, fact-free sentences, and
  deliberation leak (self-narrating verification, tours of rejected
  alternatives, pre-empted objections, process autopsies, stale
  hedging, trivial-derivation apparatus). Two layers: a mechanical tell
  pass plus a model-scored scan (the passage scanner, PASSAGE_SCANNER), resolved by
  a judgment pass that edits in place. Use whenever the operator
  asks to "sweep for AI language", "de-AI this", "check the register",
  "check for plumbing", "did I leave my working showing", "is this
  defensive", or runs a pre-publication hygiene pass on anything going
  to a reader — a post, chapter, appendix, report, README, email — or
  to net AI tells over the rendered fields of a structured file. LOOK
  IN THE FOOTNOTES AND FIGURE/TABLE NOTES — that is where plumbing
  hides. Report plus worklist resolved by an in-place judgment pass —
  the sweep writes no sidecar files; register items the pass may
  rewrite (facts preserved), plumbing items the operator rules on —
  never a silent cut (unattended, they are reported, not cut). It judges
  how the prose reads and whose activity it narrates; it does not check
  facts, quotations, numbers or attribution.
---

# AI-language sweep

Born as the review-digest prose gate: model-drafted text kept its
facts but read as generated even with a style guide written into the
brief. It also runs on its own, over any prose going to a reader.
Register and deliberation leak are swept together because they are the
same cold-eyed pass over a finished draft.

## What it does not do

The sweep judges how the prose reads and whose activity it narrates.
It does not check facts, quotations, numbers or attribution against
their sources, and it does not judge the argument or the evidence: a
sentence can pass the sweep and be false. Pair it with a fact-check
where facts matter.

## Two fault classes, two tests

- **Register** — machine voice: stock filler, evaluative adverbs,
  rhetorical scaffolding, sentences about the document itself. The test
  is how the sentences *sound*.
- **Plumbing** — deliberation leak: internal show-your-working that
  leaked into the deliverable. The test is *whose activity is the
  subject* — a finding or reader-facing fact is a keeper; us, our
  analysis, our checking, our worry is plumbing. A plain declarative
  sentence can still be plumbing; that is why a phrase net alone does
  not do this job.

## The seven forms of plumbing

1. **Restatement apparatus** — a footnote or parenthetical that explains
   a trivial derivation or reconciles two numbers a competent reader
   reconciles unaided. Write the number, cite the source, stop.
2. **Rejected alternatives** — "we considered X but…", "an alternative
   specification would…", "one could instead…". The reader needs the
   choice made, not the tour of the ones dropped.
3. **Pre-empted objections** — "it might be objected that…", "this is
   not to say…", "we are not claiming…". Answering a referee who is not
   in the room.
4. **Interim hedging** — qualifiers that were live only while a result
   was uncertain. Once it settled, the hedge is stale plumbing.
5. **Bug / process autopsy** — "after correcting an error in…", "an
   earlier version had…". The reader gets the correct number, not its
   bug history.
6. **Method worry narrated** — "there is a concern that…", "we were
   careful to…". Reassurance about our own diligence.
7. **Self-narrating verification** — "we checked / verified / confirmed",
   "as we show", multi-locator citations that exist only to prove we
   looked.

## The law

Every sentence delivers a fact. No scaffolding, no self-credentialing,
no evaluative filler, no sentences about the document itself — and no
sentences whose subject is our deliberation. This is the negative side
of a plain-prose discipline. Voice mechanics — em-dash
austerity, sentence length, connective placement — surface as notes,
not fails: they calibrate on the operator's byline register and a swept
document may not be that voice.

## Running it

```sh
python3 <this-skill>/scripts/ai_sweep.py FILE
```

Three layers over the reader-facing prose:

1. **Mechanical tells** — a regex net over every rendered line: the
   stock phrases (FAIL) plus the plumbing phrase net (`plumb` —
   hypothesis tier, never a hard fail). Non-failing notes: em-dash
   lines, unquoted sentences over 30 words of prose.
2. **Register scan** — the passage scanner chunks the file into passages; each
   gets an `ai_register` score (0–3), a `fact_free_sentences` judgment,
   and a `deliberation_leak` probability against `--questions`
   (default `scripts/prose-questions.json`). Register score ≥
   `--threshold` (1.5) is a worklist FAIL; ≥ `--watch` (1.0) a note;
   `deliberation_leak` ≥ `--plumb` (0.5) a plumbing hypothesis. The
   scanner is optional and operator-configured: `PASSAGE_SCANNER` names an
   executable taking `<scanner> scan FILE --questions BATTERY --output DIR
   --chunk-chars N --overlap N`, and nothing else is looked up. Without it — or on
   `--mechanical-only` — the sweep is mechanical-tells only, prints
   INCOMPLETE, and exits nonzero: a mechanical-only pass is never the
   full gate and the judgment pass still must run.
3. **The read** — the flags are hypotheses. READ THE FOOTNOTES AND
   FIGURE/TABLE NOTES IN FULL, EVERY ONE — that is where plumbing
   hides; the mechanical pre-pass cannot see a footnote that politely
   reconciles two numbers. For plumbing especially, the subject test is
   applied on the read, not by regex.

Scoping flags:

- `--skip-fields 'system_prompt|notes'` — field-name pattern for lines
  that never render. A matching `field: |` / `field: >-` block scalar
  exempts its whole indented block. Sweep only what a reader sees.
- YAML frontmatter and `#` comments in `.yaml/.yml` are exempt without
  flags; fenced code and `<style>`/`<script>` blocks are skipped.
- `--no-plumbing` disables the plumbing axis (review-digest's ledger
  shim uses it — process narration is the ledger's content).
- `--mechanical-only`, `--warn-only`, `--rescan`, `--threshold`,
  `--watch`, `--plumb`, `--chunk-chars`, `--overlap`, `--timeout`,
  `--retries` (per-attempt seconds / extra attempts on the scanner — a
  stalled or incomplete scan fails the gate, never hangs it).
- `--scan-dir` is a CACHE dir the script owns: an `.ai-sweep-owned`
  marker file gates every deletion — a non-empty dir without it is
  never cleared (a fresh owned `scan-N` subfolder is used instead, so a
  content folder passed by mistake survives), and a symlinked dir must
  resolve to one the script created. Default `<file>/.style-scan/`.

## The private-tree boundary

A target under the operator's personal tree never reaches the passage
scanner: the engine detects it and runs mechanical-only, deliberately.
The boundary is `AI_SWEEP_PRIVATE_ROOTS` — a
colon-separated list of absolute paths, resolved like `PATH`. There is no
built-in default: set it for any tree whose text must stay off the scanner.
The judgment read of such a file is then done by hand.

For a structured file, sweep only the fields a reader sees and skip the
rest:

```sh
python3 <this-skill>/scripts/ai_sweep.py page.yaml \
    --skip-fields 'system_prompt|notes'
```

## The judgment pass — two dispositions

- **Register items** the pass disposes in place: rewrite to
  fact-delivering prose — register rewrites preserve every fact
  (numbers, claims, severities do not move; the fix is usually
  deletion — a scaffolding sentence loses nothing when cut) — or keep
  where the flag is a false positive. A keep is a ruling, so it is
  recorded: the exact kept wording in `backticks` (a distinctive
  phrase, not a single word) plus a one-line reason go into
  `<file-stem>.keeps.md` beside the target — one list item per keep,
  `- `phrase` — <reason>`. The sweep reads it: a flagged line or
  passage carrying the recorded phrase clears while the wording
  stands; an entry with no reason clears nothing, and the record binds
  to the text — change the wording and the keep no longer covers it.
- **Plumbing items** the operator rules: report each with location,
  verbatim text, which of the seven forms, and a proposed action —
  CUT, or REWRITE (give the rewrite, finding as subject, in
  `~~strike~~` / `**bold**` markup). Never silent-cut: it is the
  operator's prose and a phrase can be legitimate; a KEEP ruling is
  recorded the same way — `backtick` phrase plus reason in
  `<file-stem>.keeps.md` — and clears while the wording stands.

**Who rules on plumbing items when no operator is present.** When
`review-digest` calls the engine (its prose gate, through its
`scripts/check_style.py`), the digest's own rules decide: the gate runs
with `--no-plumbing`, and the digest's ledger rules govern process
narration. Run on its own with no operator to answer, the sweep reports
every plumbing item — location, verbatim text, form, proposed action —
and leaves the text as it stands: an unattended pass never cuts or
rewrites a plumbing item and never records a KEEP for one. The report
is the deliverable; the operator rules when they read it. Register
items are still disposed in place.

A passage flagged on **two axes at once** — a register note and a
plumb hypothesis — carries two independent signals: give it an
explicit ruling on the read — rewrite or keep — never a slide-through.
(2026-09-29: a maxim-and-application hinge — "a selection needs a
stability argument, and the paper offers one" — scored 1.03 register
+ 0.65 leak and slid through the read unexamined. The construction is
now named in the level-2 criteria of the battery.)

**The keepers line — do not over-cut.** What was done to the data
stays; why we explored, worried, or checked goes. "Water cells were
masked before estimation" is a keeper — the reader needs it to know
what the number is. "We explored a collinearity concern" is plumbing.
And two escape-closers: "it's disclosed, so it's fine" is not a
defence — technically-disclosed plumbing still ships only our workings;
a true derivation's home is the technical appendix or the project
notes, never the deliverable.

Exit 1 while any register fail stands or the register layer never ran;
plumbing hypotheses do not move the exit — they move to the report.
`<file-stem>.keeps.md` is the suppress record: a keep not recorded
there re-flags and fails on the next run — "clean" means rewritten,
consciously flagged, or ruled-and-recorded. The scan is cached while
file and battery stand — `--rescan` after either changes.

## Where it sits

- The engine is canonical here. review-digest's step-3 prose gate calls
  it through its `scripts/check_style.py`, a shim that supplies the
  ledger battery, the ledger's internal-field list, and `--no-plumbing`
  (the ledger narrates the review's process by design — its no-plumbing
  rule is the digest's own read, not this net). This skill lives inside
  review-digest (`review-digest/ai-sweep/`), which finds the engine at
  `ai-sweep/scripts`; to use the sweep on its own, link or copy this
  folder into the skills directory.
- Construction detail the plumbing axis evicts from a deliverable
  belongs in a technical appendix or the project notes: "cut here,
  ensure it lives in the appendix," not delete.
- Tests for the engine's deterministic parts (the mechanical tell pass,
  the keep record, the scanner-missing path) are in `scripts/tests/`:
  `python3 -m pytest -q -p no:cacheprovider scripts/tests` from this
  folder.
