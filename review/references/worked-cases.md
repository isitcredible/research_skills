# Worked review cases

These examples illustrate the linked procedures. Details are stylized — they
are composite cases, not any one review's record. For a new review, verify its
own version-locked source cells and implementation; an earlier case does not
determine a new finding.

## Observed version changes

*Case: a top-5 article's online appendix grew from a handful of cited tables
in the working paper (none printed) to over twenty. The IV table drops the
WP's weak-instrument-robust intervals — under which a headline estimate had
crossed zero — and adds an overidentification test reporting p = 0.00 for the
flagship outcome, which the text does not mention while saying the IV
estimates "confirm the OLS estimates." The instrument specification and the
reported first-stage F also changed several-fold. Those are observed changes
and a published-text lead; the version sequence alone does not identify their
cause.*

## Version-specific cells

*Case: an appendix trend coefficient was marginally significant in the working
paper and plainly insignificant in print — same row, moved cell. A pipeline
built on the WP reported a "contradiction" the published paper doesn't
support.*

## Completing a reported robustness grid

*Case: the same article's robustness batteries — additional-covariate and
alternative-instrument grids reported for one headline outcome only — re-run
for the two other headline outcomes: one fails the covariate battery, and the
other collapses under the very controls the text cites as "robust". Only the
first outcome survives — and its IV fails the added overidentification test.*

## Construction findings must carry measured effects — and the direction can surprise

*Case: a validation table. The validation outcome is capped at its top bin and
filled from a different denominator where the target denominator is missing:
two in five estimation cells censored, several imputed. The finding sat in the
construction ledger as a defect bearing on the table. The audit's
quantification re-ran the table four ways: printed coefficient (marginal);
uncapped (roughly tripled, significant); uncapped and unfilled (tripled, more
significant); capped and unfilled (≈ printed). Decomposition: the cap does all
the work (the fill is immaterial), and the direction is attenuation —
top-coding the outcome folds the most extreme units onto the boundary and
flattens the gradient. The defect *understated* the paper's own validation
association threefold: it is still a defect — the printed coefficient is not
the constructed quantity — but it does not damage the paper in the direction
the finding implied. Two durable lessons: (a) the effect run is what
classifies the finding, so log → hypothesize → *run* → then write; (b) which
side of the equation the constructed variable sits on suggests the direction,
and the run decides it —
a censored/imputed outcome attenuates toward zero, the same construction in a
regressor degrades it, in a control it leaves confounding unabsorbed.*

## Corrected-construction variants: patch the shipped builder, never re-derive the estimand

*Case: a construction defect in a shared intermediate variable — a back-cast
formula coded without two terms the printed equation carries — feeding both a
headline outcome and a downstream shock estimate. The review's "printed-formula
variant" regenerated the corrected quantity by formula on every row of an
extract, then collapsed: rows the defect never touched were re-imputed too, so
industries with no defect-borne cells acquired a different estimand (total
window growth where the outcome should be an annualized rate). The reported
corrected headline was an order of magnitude off and insignificant — the
opposite substantive read of the faithful propagation (higher, still
significant). The audit later re-ran the downstream leg correctly — patching
the defective line inside a clone, `replace … if <defect-condition>` — and
reproduced an earlier independent review's number to four decimals, but quoted
the review's buggy headline artifact uncorrected. Two lessons: (a) the shipped
code's gating condition is part of the construction — re-derivation on an
extract silently drops it; patch the builder and let the pipeline carry the
correction; (b) a variant artifact is a re-implementation claim — audit checks
must validate the producing script (does it gate where the original gates?)
not merely confirm the number traces to a file. A cheap tripwire: compare the
variant's outcome moments against baseline — a regression intercept 40× the
outcome's documented mean means the variant, not the paper, is the suspect.*

## Challenge cases — inference and construction validity

Real failures in review-built tests and calculations, kept for the challenge stage. The rule is in `../challenge/SKILL.md`; each case shows what breaking it looked like.

### Inference validity

- The named modes are all committed examples: a CI including zero written as "refutes"; an "exact correction" for a threshold-sensitive proxy; a fabrication charge on an error with no intent evidence; a blanket-survival verdict the honest resolution did not support. Each flattered the critique's thesis.

### Construction validity

- **The missing-frame kill.** A headline "collapse to ~0 under a pretreatment control" was produced by computing pre-period means off the event-time variable — missing for never-treated units — silently dropping the controls' covariates. Every re-run reproduced the artifact. Re-authored on the matched-cohort frame, the effect stood strongly significant.
- **Generator passes its own anchor.** A permutation generator that kept original control units at zero treatment when eligibility moved reproduced its anchor anyway — and every re-run reproduced the defect. Anchor agreement proves nothing about off-observed assignments.
- **Ratified in-context.** A repaired resampling scheme shipped through an earlier audit validated inside the context that authored the fix — the anchor reproduced on every re-run.

### Direction errors

- **The understated defect.** An outcome capped at its top bin on two in five cells was filed as a defect bearing on a headline table; the audit's own rerun showed uncapping *tripled* the printed coefficient — the defect understated the paper's own validation association threefold. The effect run is what classifies the finding.

### Corrected-variant propagation

A review's "printed-formula variant" regenerated a corrected back-cast on every row of an extract instead of patching the shipped builder — a case-gating condition on the shipped code was dropped, so untouched cells acquired a different estimand. The variant was marked `executed` on one of two named consumers; the other leg shipped no artifact. The audit validated the variant's *provenance* (the number traced to a file) but not its *construction* — and quoted the buggy artifact into the verdict while correctly executing the other leg itself. The corrected number was off by an order of magnitude and wrong-signed in implication; the outcome-moment contradiction (a regression intercept ~40× the outcome's documented mean) was visible inside the same report.
