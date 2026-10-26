---
name: claims
description: >-
  Third review stage: work up from the surviving estimates to the narrowest story
  each can carry, test that story, and build the claim ledger — one row per
  load-bearing claim recording how central it is, whether it holds, what survives
  and what is not established, and the strongest defence. The ledger records what is
  true; it rates nothing.
---

# Claims

A coefficient is not a finding. Work up from each surviving estimate to the story it
can genuinely carry, then test the story — a result can pass every robustness check
and still support only a story that cannot be true.

## Start from the artifacts

Read `analysis/code-and-data/results.csv` and `review/code-and-data-REPORT.md` — the
files, never a remembered coefficient. Screen every row:

- `validity` not `clean` → evidence that the procedure is uninformative here, never a
  test outcome: an uninformative result says nothing against the claim and rescues
  nothing for it. `unvalidated` rows cannot carry a verdict yet.
- `row_role = rebuttal` → answers the paper's own selected number, not the test the
  design requires; if it holds, it cannot settle the claim. If it fails (the number
  does not reproduce, or loses support under corrected inference), it counts against.
  Check the labels, not just the field: a re-run of the selected estimate is a
  rebuttal however it is tagged.
- A margin whose only direct tests are invalid or unrun is a ledger row ("not testable
  under this design"), never a silent pass.
- Scope assumptions in the earlier reports carry into every row that relies on them;
  find them all, and if one was overturned, re-derive or flag what depended on it.

## The work

1. **Decompose what drives the estimate** — functional form, sample and scope, between
   vs within variation, influential observations, timing, placebos, construction
   seams — in `analysis/claims/driver-matrix.csv` (template
   `../assets/driver-matrix.csv`). Pure theory: use the attacker–defender–judge record
   from `theory-diagnostics`; hybrids need both the estimate and the theory outcome.
   A conclusion resting on a WHIMSICAL premise (`assumption-ledger.csv`) supports only
   the ledger's minimal repair.
2. **State the supportable story** — who, what exposure, what mechanism, when, how big
   (outcome units plus the three dimensions: magnitude, significance, variance share),
   against what counterfactual, over what scope. Do not import the abstract's causal
   nouns where the estimate supports only a contrast. An average effect does not say
   who carries it: one carried by a subpopulation does not support a population-wide
   story (`../references/methods/gelman_hullman_kennedy_2024_causal_quartets.md`). A
   hypothesis never stated precisely enough to fail was never tested.
3. **Test it** (`../references/claim-test-matrix.md`):
   - printed-table contradictions and version-history leads from `paper`;
   - each mechanism link — existence, direction, timing, magnitude — and the
     load-bearing cases checked in the data; a mechanism read off effect
     heterogeneity needs its two exclusion assumptions named and an outcome that
     is not a non-affine transform of the theory's construct, and absent
     heterogeneity rules out no channel
     (`../references/methods/fu_slough_2026_hte_mechanisms.md`);
   - design validity: identifying variation, isolation, measurement, power;
   - **the specialist literature — reading the works is the check**
     (`../references/historiography-protocol.md`); another paper drawing on the same
     sources is context, not corroboration;
   - claims that reach the conclusion by a bank shot, or label a mechanical
     consequence as a finding;
   - the **piranha check**: a large general claim about a heavily studied outcome
     competes with every other large claim
     (`../references/methods/tosh_etal_2025_piranha.md`);
   - the **selection filter**: published estimates are selected on significance, and
     a headline just above the threshold is where selection operates
     (`andrews_kasy_2019_publication_bias.md`, `elliott_kudrin_wuthrich_2022_phacking.md`,
     `simonsohn_simmons_nelson_2020_spec_curve.md` in `../references/methods/`).
   Label each failure verification or reanalysis.
4. **Try to overturn your own verdict**, in whichever direction it runs: for each
   headline claim, run one defensible challenge that could reverse the row — a test
   the claim could fail where the row says it holds, or the authors' strongest
   specification where the row says it fails — and record the result.

## The claim ledger

Go through the title, abstract, introduction and conclusion sentence by sentence. One
row per load-bearing claim, in `review/claims-REPORT.md` and
`analysis/claims/claim-ledger.csv` (template `../assets/claim-ledger.csv`):

`claim_id | claim (verbatim) | page | centrality | holds | kernel | not_established | strongest_defence | defence_tested | status | evidence`

One sentence becomes several rows when its claim holds at one inference level and
has no valid test at another; each row quotes the sentence.

The ledger records what the evidence establishes. It carries no severity: how much a
finding matters to a reader is decided when the digest is written.

- **`centrality`** — where the claim sits in the paper, read from the print:
  - `headline` — the title, the abstract, or a finding the introduction or conclusion
    states as the paper's contribution;
  - `supporting` — a result a headline rests on: an estimate, test, robustness check,
    replication or mechanism claim in the results;
  - `peripheral` — an implication, policy prescription, interpretation or framing
    the paper does not test.
- **`holds`** — one of:
  - `holds` — the claim stands as printed; any gap is disclosure or a nuance that
    changes no reader's conclusion;
  - `narrower` — the claim's point stands, but only in a narrower scope, size,
    precision, population or sample than printed, and the paper does not flag it;
  - `not established` — the claim's point is not established by its evidence: the
    comparison was never made; the claimed scope has no evidence; a specification
    the authors avoided, at least as defensible, removes it; a stated robustness
    claim is contradicted by the cited cells; the magnitude cannot be separated from
    a mechanical or confounded channel, or is not measured (the estimator that
    delivers it has an unbounded weak-identification-robust set, or no significant
    first stage at the design's inference level); a plausible, evidenced confounder
    removes a causal claim; or the evidence is uninformative. This is the finding,
    not a softer one, because the burden is the paper's; it is never written
    "refuted".
- **`kernel`** — what the evidence does support, stated as what it is (for
  `not established`, the weaker statement that survives, or "none").
  **`not established`** — what the claim asserts beyond the kernel. Both are written
  so a reader can quote them.
- **`status`** — `settled`, `INTERIM` (a feasible decisive test is unrun), `untested`
  (no valid direct test exists), `unverifiable` (the authors never deposited the
  materials) or `unverified-here` (a cited source the review could not obtain — a
  limit on the review, reported as a caveat, never a finding).
- **Strongest defence** — the best case the authors could make. Testable but not yet
  run → the row is `INTERIM`, in either direction. A defence that cannot be tested
  shields nothing when it rests on materials the authors did not deposit (code,
  data, instruments, records) or on a printed statement the deposited data
  contradict: the missing materials, or the contradiction, are their own finding, and
  the row is decided on the evidence that exists. Any other untestable defence that
  the print supports and that would account for the evidence is recorded beside the
  row and keeps it from `not established` on the evidence it explains. A defence
  tested and failed is recorded as failed.
- **An attribution lost in some samples is lost there.** Where a finding removes
  support for an attribution the paper makes in some of its samples (a contrast
  credited to the treatment where the arms differed in procedure, say), the claims
  resting on those samples are `not established` for that attribution, even where
  other samples still carry the headline. The headline claim is decided on the
  samples that remain, and the row says which they are.
- **A conjecture the paper hedges claims only plausibility.** A sentence the paper
  itself presents as conjecture, hypothesis or speculation ("may", "we speculate", "one
  possible explanation"), and does not elsewhere state or use as a finding, claims only
  that the proposition is plausible. Record it `holds` unless evidence contradicts it,
  including the paper's own results; the kernel says it is a conjecture the paper does
  not test. Where the paper elsewhere states the same proposition as established — in
  the abstract or conclusion, or as the premise of a later result — that sentence is its
  own row, judged as stated. A hedge in wording only, a "may" on a result the paper then
  builds on, does not count.
- **Guard both directions.** Reproducibility, transparency and good faith are not
  evidence for a claim; equally, do not inflate a narrower-but-true claim into one
  not established. A defence that accounts for the evidence resolves the attack or
  narrows it.

## Output

`review/claims-REPORT.md` from `../assets/report-template.md`: findings `L1, L2, …`,
then the supportable story per result family, the claim ledger table (with `Centrality`
and `Holds` columns — later tools read them) and the claim-test matrix. New data anomalies or statistical requests go back to
`code-and-data`; once its corrections land, refresh the affected rows before
synthesis.
