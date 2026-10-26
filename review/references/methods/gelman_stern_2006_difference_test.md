# The difference between "significant" and "not significant" — Gelman & Stern (2006)

Working distillation of Andrew Gelman & Hal Stern, "The Difference
Between 'Significant' and 'Not Significant' is not Itself Statistically
Significant," *The American Statistician* 60(4): 328–331,
doi:10.1198/000313006X152649. Verified against the published article
(Taylor & Francis typeset, journal furniture on page 1; source PDF not
distributed).

## The rule

A contrast between "statistically significant" and "not significant"
across two groups, periods, or specifications is not itself evidence of
a difference. Significance is a threshold on each estimate's own noise;
the difference between the two estimates has its own standard error and
must be tested directly.

Canonical example (§2, p. 328): two independent studies report 25 ± 10
and 10 ± 10. The first is significant at the 1% level, the second not at
all — but the estimated difference is 15 with SE √(10² + 10²) = 14,
"not even close to being statistically significant." The paper adds a
third study (2.5 ± 1.0): each estimate is different from zero or not on
its own, yet pooling information beats comparing threshold verdicts.

## Uses in the review skill

- `code-and-data` (MANDATORY direct difference test):
  any "the effect holds for A but not B" prose — subgroup, period,
  gender, region, regime — must be verified by a test of A − B
  (interaction term or difference of estimates with its own interval),
  never by comparing two significance verdicts. A heterogeneity claim
  resting on the contrast of two stars is `UNRESOLVED` until the
  difference is tested.
- Reading caveat for the difference test (no separate interaction-MDE run is
  required; the design-matrix MDE row applies when the "not in B" null carries
  weight): the test of the difference
  carries roughly twice the SE of the main effect at roughly half the
  plausible size — hence the ~16× sample heuristic (Gelman's 2018-03-15
  blog post, "You need 16 times the sample size to estimate an
  interaction than to estimate a main effect"; the arithmetic: the
  interaction's variance is 4× the main effect's — 2× from differencing
  four cell means instead of two, 2× from the halved cell size — and the
  other 4× comes from the interaction being half the size).
