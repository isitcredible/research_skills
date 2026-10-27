# Changelog

What each release of the review skills (`review`, `audit-review`, `review-digest`)
changed, newest first. The three skills share one version. Each entry names its rows
in `review/spec-changes.csv`, which records every requirement change in full.

Below 1.0 any release may change what the skills require of a run.

## 0.9.2 — 2026-10-27

- Model routing is guidance, not fixed assignments: fit it to the models, prices and
  harness available. *Agents and cost* in `review/SKILL.md` now names three rough
  kinds of task: mechanical (checkable by looking, so a cheaper model can do it),
  analysis (stage and module reports, the scripts a review writes, the provisional
  claim ledger, the coordinator) and verdict (the challenge and verdict stages, where
  the strongest available model buys most for least). With two models, analysis and
  verdict share the stronger; the challenge agent runs on a model at least as strong
  as the one that wrote what it tests. The section gives examples for a single model,
  Claude, OpenAI and a lead-and-worker harness. What a run produces is unchanged.

Spec row: R534 (process).

## 0.9.1 — 2026-10-26

- The independent-literature check now applies to every paper, not only to historical
  claims. Its sources depend on the kind of proposition: an estimated effect is
  checked against meta-analyses, replications and comments, working papers and
  preprints, registries, and other designs on the same population; a historical claim
  against repositories, archives and monographs. A meta-analysis that pools the target
  paper or its data does not count as independent. Each work consulted records whether
  it has been replicated, corrected or retracted, and independence is judged by data,
  sample, sources and design.
- `review/references/historiography-protocol.md` is renamed
  `review/references/literature-protocol.md`.

Spec row: R533.

## 0.9.0 — 2026-10-26

First public release: `review`, `audit-review` and `review-digest`, with `ai-sweep`
nested in `review-digest/ai-sweep/` as the engine of the digest's prose gate.
Changes from the last pre-release version:

- `python3` in every command means a Python 3.10+ interpreter with the packages the
  README lists; a virtual environment's interpreter is fine.
- A subagent the harness bars from writing files returns its report as text, and the
  coordinator saves it unchanged.
- Diagnostic modules: a module that does not apply writes a one-line
  `NOT_APPLICABLE` report; a module that fires runs as its own agent, writes its own
  report and appends to the shared ledgers under a lock.
- The code-and-data stage runs its gates only once the fired modules have reported.
- Clearer record formats for the robustness-claim scan, the claim ledger (now with a
  template in `review/assets/`), the challenge's two-direction evidence sort, and the
  ordering of findings in the verdict.
- `audit-review` initialises a repository in a job folder that has none, and sorts
  every erratum it routes back by the same test of whether it changes a verdict.
- `review-digest`: a slip that leaves every conclusion unchanged is routed but does
  not block the digest; staleness is judged by the manifest's file hashes (dates are
  only a hint); the fact sweep flags a number stated more precisely than its source.

Spec rows: R522–R532.
