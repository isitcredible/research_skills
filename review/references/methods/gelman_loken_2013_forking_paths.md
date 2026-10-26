# The garden of forking paths — Gelman & Loken (2013)

Working distillation of Andrew Gelman & Eric Loken, "The garden of
forking paths: Why multiple comparisons can be a problem, even when
there is no 'fishing expedition' or 'p-hacking' and the research
hypothesis was posited ahead of time." Verified against the 14 Nov 2013
manuscript — never published in a journal; cite as an unpublished
manuscript (Columbia University). (Source PDF not distributed.)

## The core claim

Multiple comparisons are a problem even when the researcher ran only
*one* analysis. If the details of the analysis — variable definitions,
conditioning, exclusions, transformations — were chosen contingent on
the data, then the analysis performed is one draw from a large space of
potential analyses, and the nominal p-value ignores that space
(abstract; §1.2). The problem does not require conscious fishing or
even awareness: "it is possible to have multiple potential comparisons
... without the researcher performing any conscious procedure of
fishing or examining multiple p-values" (§1.2).

The corollary for review work: honesty and a posited-ahead-of-time
hypothesis do not defuse forking paths. What matters is whether the
*specific* data-dependent choices were pinned before the data were seen
— which is why a PAP/preregistration is treated as a dated prior version
(`paper`), and why the `code-and-data` data audit asks for the envelope of
defensible codings rather than the coding used.

## Uses in the review skill

- `experiment-diagnostics` "design-stage forking paths": the extension
  of the argument one stage earlier — iterating on conditions,
  instructions, or exclusion rules conditional on pilot results is the
  same selection process operating in the design rather than the
  analysis.
- `paper` PAP/preregistration item: a preregistered plan is the
  dated version against which data-contingent choice is measured.
- `code-and-data` data audit — discretionary-coding checks: the forking paths are the
  *potential* analyses, not the performed ones — which is why the audit
  sweeps the space, not just the reported spec.
