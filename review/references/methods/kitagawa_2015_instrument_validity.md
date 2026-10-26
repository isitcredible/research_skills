# A test for instrument validity — Kitagawa (2015)

Working distillation of Toru Kitagawa, "A Test for Instrument
Validity", *Econometrica* 83(5) (2015): 2043–2063. The source PDFs
(not distributed with the skill):
`Kitagawa_2015_InstrumentValidity_Econometrica.pdf` (cemmap WP
CWP34/14) **and** `..._published.pdf` (the published Econometrica
article) — quote the published version.

## What it does

For a binary treatment and discrete instrument in the heterogeneous-
effect (LATE) framework, instrument validity (exogeneity + monotonicity
jointly) has **testable implications** — the complier outcome densities
implied by observed data must be nonnegative (§2–3). Kitagawa's test
inferences this via a variance-weighted Kolmogorov–Smirnov statistic;
rejection means the instrument's identifying assumptions fail, not just
that the first stage is weak. No smoothing parameters needed; handles
discrete and continuous outcomes; covariate extension provided.

## Why the battery needs it

The weak-IV machinery (Stock–Yogo, MOP, tF/VtF) asks *"is the
instrument strong?"* — this is the missing *"is the instrument valid?"*
check for the binary/discrete case. Distinct from overidentification
tests: it works with a single instrument (exactly identified), where
Sargan/Hansen is vacuous. Rejection identifies a violation of the
exclusion/monotonicity compound, which no first-stage F can detect.

**Scope limits to state honestly in review**: requires binary treatment
and discrete instrument as stated. Huber–Mellace and Mourifié–Wan are
alternative tests of the binary/discrete-instrument implications
(Huber–Mellace of a weaker mean-independence version; Mourifié–Wan of
the same condition via conditional moment inequalities, admitting
covariates — both p. 2049), not a continuous-instrument extension; for a
continuous instrument, state the gap.

## Review use

- `iv-diagnostics`: after first-stage strength is established, the
  validity question for binary/discrete IV designs — does the paper
  run or acknowledge a validity check beyond "the instrument is
  plausibly exogenous"? A Kitagawa rejection (or no test where one
  applies) is a finding.
- `experiment-diagnostics`: randomized-encouragement designs with
  noncompliance are the canonical binary-IV case — the test applies
  directly.
