# Causal quartets — Gelman, Hullman & Kennedy (2024)

Working distillation of Andrew Gelman, Jessica Hullman & Lauren
Kennedy, "Causal Quartets: Different Ways to Attain the Same Average
Treatment Effect," *The American Statistician* 78(3): 267–272,
doi:10.1080/00031305.2023.2267597, distilled from the published
article. The paper is often cited as 2023 (online-first); the issue
citation is 2024.

## The content

An Anscombe-style demonstration for causal inference: two quartets —
sets of four plots with the *same* average treatment effect but very
different patterns of individual-level heterogeneity. The first quartet
varies effects unpredictably across units; the second makes effect
variation predictable from a covariate.

The review-relevant consequences the paper draws:

- An ATE alone tells you almost nothing about who benefits or by how
  much — the same number can hide constant effects, fan-shaped
  heterogeneity, or sign reversals across subgroups.
- "The average effect is often much smaller than anticipated" — the
  headline ATE reported from a selected subpopulation or a convenient
  denominator is typically larger than the population quantity the
  prose implies.
- Heterogeneity is the default, not the exception: a "no effect"
  subgroup claim needs the same direct-difference machinery as a
  positive one.

## Uses in the review skill

- `claims` stage, the supportable story's *who*: an ATE carried by one
  subpopulation does not support a population-level story; the quartet
  shows that the ATE underdetermines the pattern the claim needs.
- `code-and-data` data audit, subgroup-to-aggregate adding-up: subgroup
  effects that cannot compose the reported aggregate are a data problem,
  not a heterogeneity finding.
- Design-matrix transportability rows (treated-share or denominator
  claims): the estimand's population is a property of the design, and
  the ATE label conceals it.
