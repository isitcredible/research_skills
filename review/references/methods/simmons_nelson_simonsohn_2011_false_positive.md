# False-positive psychology — Simmons, Nelson & Simonsohn (2011)

Working distillation of Joseph P. Simmons, Leif D. Nelson & Uri
Simonsohn, "False-Positive Psychology: Undisclosed Flexibility in Data
Collection and Analysis Allows Presenting Anything as Significant,"
*Psychological Science* 22(11): 1359–1366,
doi:10.1177/0956797611417632. Verified against the published article
(journal furniture on page 1; source PDF not distributed).

## The simulation result (Table 1, p. 1361)

15,000 simulated datasets, null true, two-condition design with 20
observations per cell. Four researcher degrees of freedom tested alone
and combined: choice among dependent variables, optional stopping (20
then +10), covariate inclusion (gender main effect and interaction), and
condition subsetting. Combining all four lifts the false-positive rate
to **81.5% / 60.7% / 21.5%** at the p < .1 / .05 / .01 columns
respectively — at the conventional 5% level, a researcher exercising all
four flexibilities is more likely to find a false positive than not.

The demonstration experiment: with the four flexibilities exploited, the
authors "showed" that listening to "When I'm Sixty-Four" makes people
younger — a significant result the compliant reporting version then
reveals as artifact.

## The disclosure remedy (pp. 1363–1365)

Six requirements for authors plus four guidelines for reviewers. The
"21-word solution" ("We report how we determined our sample size, all
data exclusions (if any), all manipulations, and all measures in the
study") is the authors' later one-sentence distillation (Simmons, Nelson
& Simonsohn 2012), not part of this paper. The review-side use: the
absence of these disclosures is itself a flag, and a checklist of where
undisclosed flexibility could live.

## Uses in the review skill

- `experiment-diagnostics` design-stage forking paths: the analysis-side
  version of the same selection machinery; SNS give the quantitative
  cost of combined flexibility.
- `paper` PAP item: the disclosure checklist is the baseline a
  PAP or methods section should clear; a PAP that omits sample-size
  determination, exclusions, or the full outcome list leaves the
  flexibility in place.
- `code-and-data` data audit — discretionary-choice sweep: each of the four DFs maps to
  a coding choice the audit enumerates.
