# Randomization tests against seemingly significant experiments — Young (2019)

Working distillation of Alwyn Young, "Channelling Fisher: Randomization
Tests and the Statistical Insignificance of Seemingly Significant
Experimental Results," *Quarterly Journal of Economics* 134(2): 557–598.
Verified against the QJE-typeset "forthcoming" version (Nov 2018) from
the author's LSE page — text matches the published article; the
published page numbers apply. (Source PDF not distributed.)

## The results (abstract)

A comprehensive sample of 53 experimental papers from the AEA journals,
re-tested using the experiments' own assignment mechanisms
(randomization inference) rather than conventional asymptotic
inference:

- Tests of **individual** treatment effects: randomization tests find
  **13 to 22 percent fewer** significant results than the authors'
  methods.
- **Joint** tests of the multiple treatment effects appearing together
  in tables: **33 to 49 percent fewer** statistically significant
  results than conventional tests (49% at .01, 33% at .05). These are
  table-level joint tests, not a paper-wide omnibus test.
- Bootstrap and jackknife methods support the randomization results.

The mechanism: conventional and cluster-robust standard errors are
biased downward in the finite samples experiments actually have, and
the significance of any one coefficient is partly selection — the joint
null that treatment affected nothing is the test individual stars were
selected to survive.

## Uses in the review skill

- `experiment-diagnostics` randomization-inference and omnibus-joint-
  null checks: this paper is the source — the skill's `## Source` block
  already cites it. The published-version numbers above are the ones to
  quote (the 2016 working paper reported a different headline — 30–40%
  of equations failing — before the published revision; do not cite the
  WP numbers).
- `experiment-diagnostics` design-stage forking paths: Young's result
  quantifies what analysis-side flexibility costs even in randomized
  designs; the design-stage item extends the same logic to choices made
  before data collection.
