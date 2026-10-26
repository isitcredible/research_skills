# Claim-test matrix

Create one row for every material proposition in the supportable story, as a table
in `review/claims-REPORT.md`.

| Field | Meaning |
|---|---|
| claim_id | Stable identifier |
| proposition | One falsifiable statement |
| role | exposure, mechanism link, timing, magnitude, counterfactual, design validity, framing |
| empirical/formal evidence | Exact specification and artifact, or theorem/proof locus and construction |
| case evidence | Named case and verified data value, where applicable |
| independent source | Identified work and page/section |
| independence | independent, partly independent, dependent, unknown |
| result | supports, contradicts, qualifies, not addressed, blocked |
| effect on story | Exact clause retained, narrowed, replaced, or removed |
| status / defense | the claim-ledger status (settled · INTERIM · untested · unverifiable · unverified-here); material defense and its evidentiary result |

## Mechanism chains

Split `X → A → B → Y` into at least:

1. `X → A`
2. `A → B`
3. `B → Y`
4. timing alignment across the chain
5. capacity sufficient for the reported magnitude

A reduced-form association between `X` and `Y` does not fill the intermediate
rows.

## Driver statements

Scope every driver statement to:

- data version;
- sample;
- outcome;
- transform;
- specification;
- inference method.

“The result is the transform” requires a crossed comparison sufficient to
separate data-version and transform effects.

## Framing comparison

Extract the paper's claim from each relevant location rather than paraphrasing
the paper as one undifferentiated headline. A paper can be careful in the table
note and expansive in the abstract; that difference is part of the result.
