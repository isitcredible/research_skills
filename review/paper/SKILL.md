---
name: paper
description: >-
  First review stage, no code: the paper's version history (what moved between
  drafts and print), the printed-table consistency pass (do the printed cells
  support the prose?), and the research-design critique (identification,
  confounders, controls).
---

# Paper

Read the paper as an argument before touching code. Three questions: what changed
between drafts and print; do the printed numbers already contradict the prose; does
the design measure what the claim needs? No code runs in this stage.

## 1. Version history

Papers change between drafts and print: coefficients move, samples are redrawn,
robustness checks appear, vanish or are reframed. Record what moved. A change is a
**lead, not a motive**: pre-submission search, referee demands or concealment each
need documentary evidence (correspondence, a dated referee report, an explicit
statement).

- Run `pdfinfo` and read the title page of every draft; record its date and status.
  Search for earlier versions (SSRN history, series pages, author sites and CVs, RePEc,
  Scholar, Wayback) and record the searches. The newest working paper may be the
  accepted manuscript — comparing only it with print misses earlier movement.
- Compare **every adjacent pair of dated versions**, then earliest → published. A
  transition with no surviving draft on one side is `UNOBSERVABLE`, never "minimal".
- A pre-analysis plan or registry entry is a dated version: compare primary outcome,
  estimand, sample and exclusions (`../references/methods/olken_2015_preanalysis.md`).
  An undisclosed departure is a finding; no registration is not.
- A published comment and reply are a version pair too.

Write `analysis/paper/drift-table.md`: for each result found in an adjacent pair,
before → after (coefficient, SE, stars, N, sample, specification) with page locations
in both documents, classified as **coefficient moved** (with % change), **significance
flipped**, **sample/specification changed**, **exhibit deleted/added/demoted**, or
**claim reframed** (point → range, causal verb hardened, hedge dropped, abstract not
updated after a number moved). Read load-bearing signs off the page image —
`pdftotext` drops minus signs.

Look specifically for: an adverse check deleted before print; a weak or null cell
the prose calls "in line with"; a main-text result moved to the appendix where it
points the other way; an appendix check the text cites that is broken or missing; a
check decaying toward null by print while the claim it supports stays unqualified.

A defect present in every version is a research-design finding, not drift. A rescaling
or renaming is not a moved effect until the underlying quantity is confirmed. Never
report a working-paper number as the paper's result; a drift claim resting on a
version not on disk is `unverified-here`, naming the missing draft.

## 2. Printed-table consistency

Walk every headline, mechanism and robustness table in the published article and
appendix (page image for load-bearing signs). Findings:

- columns in one table that disagree (sign flips, nulls beside "robust" cells, the
  paper's preferred estimator already null);
- prose asserting significance, a range, or robustness that the printed cells do not
  support;
- sibling tables telling opposite stories; a range that is non-zero only by averaging
  contradictory columns.

**Robustness claims.** Every sentence of the form "results are robust / similar /
unchanged / not sensitive to X" is a testable claim about a cited table. For each,
open the table, check *every outcome the sentence covers*, and classify it
`SUPPORTED` / `QUALIFIED` / `CONTRADICTED` / `UNRESOLVED` in
`analysis/paper/robustness-claims.csv` (`claim, page, cited_exhibit,
outcomes_covered, classification, evidence`). A scan that finds no such sentence is
one row classified `NONE_FOUND`, its `evidence` naming the search stems; a
header-only file cannot be told from a skipped scan. A blanket claim backed by a
check run on a subset is a scope claim — pass it to `code-and-data` as a lead.

Test the version-history leads against the published cells. This section appears in
the report even when clean; a later blocked stage does not excuse skipping it.

## 3. Research design

- **Identification.** Name the design (DiD, RDD, IV, experiment, cross-section,
  structural model) and its core assumptions, and whether the paper defends or merely
  assumes each. A placebo or balance test counts only if it would detect the violation
  it is meant to test; "no significant imbalance" is a failure to reject, not
  confirmation (equivalence testing —
  `../references/methods/eggers_tunon_dafoe_2024_placebo_tests.md`).
- **Logic gaps.** Does the design test the theoretical claim, or a weaker neighbour
  of it? Name the most damaging omitted variables and alternative stories. A regressor
  built from the outcome's own correlates or consequences has a built-in association.
  Inclusion rules that bind differently across compared units confound the estimate
  with selection.
- **Controls.** An added control can bias as badly as an omitted one
  (Cinelli–Forney–Pearl). Classify suspects: mediator or descendant of treatment
  (over-control), pre-treatment collider (M-bias — "pre-treatment" is no safe harbour),
  near-instrument (bias amplification), descendant of the outcome (selection). Where
  the causal diagram cannot settle it, Cinelli–Hazlett sensitivity is the honest tool.
  Pass each suspect to `code-and-data` (is it in the code? re-estimate without it).
- **Theory and hybrid papers.** Do the assumptions hold up; does the informal story
  match what the formal result establishes; does the theorem support the abstract's
  claim? Re-derivations, counterexamples and simulations belong to
  `../modules/theory-diagnostics/` in the next stage — pass leads there. Pass the
  premises the abstract and policy claims rest on to
  `../modules/whimsical-assumptions-diagnostics/`.

Structural problems only: no comments on typos, style or code mechanics.

## Output

`review/paper-REPORT.md` from `../assets/report-template.md`, with findings `P1, P2, …`
grouped under version history, printed-table consistency and research design (bold
labels; finding blocks keep the template's `###` heads), most important first within
each, and the gravest named in Status; the two
artifacts above; and leads for `code-and-data` (checks to run, controls to drop,
deleted diagnostics to restore, subsets to verify) and for `claims` (reframed or
demoted claims).
