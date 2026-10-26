# DiD and event-study methods: estimand adjudication, pre-trend evidence, and inference

Source-audited crib for the DiD/event-study battery. One decision spine:
what does the reported coefficient average, what evidence does the pre-trend
display carry, and what inference does the cluster structure support.

**Sources audited (all source PDFs not distributed with the skill unless noted):**
- Roth, "Pretest with Caution: Event-Study Estimates after Testing for
  Parallel Trends," *AER: Insights* 4(3) (2022), 305–322 — published.
- Rambachan & Roth, "A More Credible Approach to Parallel Trends,"
  *Review of Economic Studies* 90(5) (2023), 2555–2591 — published.
- Roth & Sant'Anna, "When Is Parallel Trends Sensitive to Functional Form?"
  *Econometrica* 91(2) (2023), 737–747 — published.
- Callaway & Sant'Anna, "Difference-in-Differences with Multiple Time
  Periods," *Journal of Econometrics* 225(2) (2021), 200–230 — published.
- Sun & Abraham, "Estimating Dynamic Treatment Effects in Event Studies with
  Heterogeneous Treatment Effects," *Journal of Econometrics* 225(2) (2021),
  175–199 — published.
- Conley & Taber, "Inference with 'Difference in Differences' with a Small
  Number of Policy Changes," *Review of Economics and Statistics* 93(1)
  (2011), 113–125 — published.
- de Chaisemartin & D'Haultfœuille, "Two-Way Fixed Effects Estimators with
  Heterogeneous Treatment Effects," *American Economic Review* 110(9)
  (2020), 2964–2996 — published.
- Goodman-Bacon, "Difference-in-Differences with Variation in Treatment
  Timing," *Journal of Econometrics* 225(2) (2021), 254–277 — published.

Verification status: **source-audited 2026-09-22**. Page cites are to the
printed folios above; interior claims carry section numbers.

Use in this battery: `did-event-study-diagnostics` (estimand adjudication,
pre-test power, HonestDiD breakdown, Conley–Taber routing) and the
design-matrix DiD records.

## 1. First question: what is β̂ averaging?

Before any robustness comparison, name the estimand the paper's estimator
actually delivers — this is the estimand adjudication the module gates on.

- **Goodman-Bacon 2021** (Theorem 1, pp. 256–258): with variation in
  treatment timing, the TWFE DD coefficient is a weighted average of *all
  possible 2×2 DD comparisons* between timing groups — early-treated vs
  later-treated, later-treated vs *already-treated* (the "forbidden"
  comparisons where a treated unit acts as control), and each vs
  never-treated. Weights are proportional to group sizes and the variance
  of the treatment dummy; `bacondecomp` prints the table. Negative weights
  arise only when effects change over time within a group (p. 255).
- **de Chaisemartin & D'Haultfœuille 2020** (Theorem 1, pp. 2967–2968):
  under common trends the TWFE coefficient equals a weighted sum of
  cell-level ATEs, weights W_g,t summing to 1 but **possibly negative** —
  because already-treated cells enter as controls. With heterogeneous
  effects the aggregate can bear the opposite sign to every cell-level
  effect. Diagnostic: report the share and sum of negative weights
  (`twowayfeweights`). Remedy: their DID_M estimator (`did_multiplegt`),
  which averages only cells whose treatment actually changes.
- **Sun & Abraham 2021** (§§2–3): in a staggered event-study TWFE with
  leads and lags, the coefficient on relative-time indicator μ_ℓ is a
  linear combination of cohort-specific effects from ℓ *and from other
  relative periods* — contamination across leads and lags. The weights
  come from an auxiliary regression depending only on the cohort
  distribution (`eventstudyweights` prints them). Fix: the
  interaction-weighted (IW) estimator with never- or last-treated cohorts
  as controls.
- **Callaway & Sant'Anna 2021** (§§2–4): the clean building block is the
  group-time ATT(g,t) — the effect at time t on units first treated at g —
  point-identified under PT + no anticipation; estimate by outcome
  regression, IPW, or doubly-robust; then aggregate deliberately
  (the aggregation scheme is application-specific, not automatic).
  Control-group choice is part of the estimand: never-treated is safest;
  not-yet-treated buys data at the price of assuming later-treated units
  have no anticipatory response while serving as controls.

**Rule for the review:** a TWFE-vs-robust-estimator comparison is only
meaningful after the estimand is named. If TWFE is invalidated (negative
weights dominant, forbidden comparisons large), mark its row
`validity = invalid` in `results.csv`, naming the convention in the row's
`notes` (which comparisons, what weight) — do not average it into a "the
effect is roughly X" range. If the paper's claim needs a different
aggregate than CS's natural one (e.g. a per-calendar-year effect), state
the weighting explicitly.

## 2. What a pre-trend plot/tests actually show — Roth 2022

Two limits (abstract, p. 305):

- **Power**: conventional pre-trends tests can have low power against
  violations that would meaningfully bias the estimate — non-rejection is
  consistent with economically important non-parallel trends.
- **Selection**: conditioning on *passing* the pretest distorts the
  post-treatment estimates — the draws that survive are a selected sample,
  so pretesting can exacerbate the bias it was meant to screen.

Review consequences: (a) "pre-trends not rejected" is not evidence of
parallel trends unless the test's power against the relevant violation
magnitude is computed; (b) a paper that reports estimates *only* after a
passed pretest has a conditional-on-selection inference problem; (c) in
staggered designs the lead-coefficient "pretest" is additionally
contaminated by post-treatment effects from other relative periods
(Sun–Abraham §2) — so an event-study's clean-looking leads do not
establish PT even at face value.

## 3. Honest sensitivity — Rambachan & Roth 2023

Replace the binary PT assumption with a bound on the violation δ and
report how the conclusion degrades (§§2–4):

- Write the estimand as β = τ + δ (causal + trend-difference bias); impose
  a restriction class on δ.
- **Δ^RM(M̄) — relative magnitudes** (§2.4.1): each consecutive-period
  change in the post-treatment violation, |δ_{t+1} − δ_t|, bounded by
  M̄ × the largest consecutive-period change in the pre-period.
  Interpretation: "post-treatment confounding shocks at most M̄ times the
  worst observed pre-period shock."
- **Δ^SD(M) — smoothness** (§2.4.3): the second difference of δ bounded by
  M — the trend difference cannot kink by more than M per period.
  FLCIs for Δ^SD(M) have attractive guarantees (§4.1.1).
- **Breakdown value**: M* = min M such that 0 enters the identified set —
  report the M̄/M at which the conclusion breaks, not just the CI at one
  arbitrary bound (§4.3 discussion around identification breakdown).

`HonestDiD` (R/Stata) implements both classes. Review use: a paper's claim
survives only if its breakdown M̄ is large relative to what the pre-trends
and institutional setting suggest; a claim holding only at M̄ < 1 (post
violations *smaller* than observed pre violations) is fragile.

## 4. Functional form is not free — Roth & Sant'Anna 2023

Theorem (abstract, p. 737): parallel trends holds under **all** strictly
monotonic transformations of the outcome iff a stronger PT-type condition
holds for the *CDF* of untreated potential outcomes — satisfied
essentially iff the population partitions into a subgroup where treatment
is effectively randomly assigned and a subgroup where the Y(0)
distribution is stable over time (plus a hybrid case).

So when the paper's PT justification is informal ("log outcomes look
stable"), the claim is implicitly assuming near-random assignment or
distributional stability. Review rule: if the headline transform (levels
vs logs vs asinh — see also `chen_roth_2024_logs_with_zeros.md` for
zero-valued outcomes) is load-bearing, either demand a functional-form-
specific PT justification or run the R-SA test for insensitivity to
transforms. A PT claim that flips sign between levels and logs is not
"specification uncertainty" — it is the absence of the identifying
condition, full stop.

McConnell (2024, `mcconnell_2024_forest_logs.md`) sharpens the level-vs-
log case: a levels DiD identifies an *additive* difference in trends, a
log-DV DiD a difference in *proportional growth rates* — different
estimands that can take opposite signs when baseline outcome
distributions differ enough (he gives the sign-flip condition). His
prescription: choose the functional form from the economic model a
priori, not by pretesting both scales; if the defensible model is
multiplicative, keep the outcome in levels and estimate by PPML rather
than logging. So "we also show it in logs/levels" is not a robustness
check of one estimand — it is a second estimand, and the review must say
which the claim needs.

## 5. Few treated clusters — Conley & Taber 2011

When the policy changes in only a few groups (N1 small) while N0 control
groups are many (pp. 113–115, §§2–3):

- The point estimator is not consistent ("Point estimators … are not
  consistent since N1 and T are fixed", p. 113), and standard
  cluster-robust inference fails: there is no asymptotic normality from
  the treated side; the controls identify only the error distribution.
  The usual "50 clusters" comfort applies to *control* clusters only.
- The C–T procedure: use the empirical distribution of control-group
  coefficient estimates (from estimating the same regression on controls)
  to bound the treated estimate's distribution — a randomization-flavored
  inference at the group level.

Review rule: count treated clusters separately from total clusters. A DiD
with 2 treated states and 48 controls is a 2-cluster problem for
inference — route to C–T or cluster-level randomization inference
(cf. the few-cluster crib §3/§5), not to a wild bootstrap t-test, which
under-rejects exactly in the few-treated-clusters case (MNW guide §4.3.2).

## 6. Non-absorbing and non-binary treatments

The module's absorbing-treatment inventory: if units can exit treatment or
treatment intensity varies (fuzzy), the Goodman-Bacon decomposition no
longer applies — it needs absorbing binary timing. The dCDH weight
decomposition applies to any TWFE regression, not only staggered adoption
(pp. 2965–2966; non-binary and fuzzy cases in their online appendix), so
`twowayfeweights` still runs; the estimators are dCDH's `fuzzydid` /
`did_multiplegt` extensions (dCDH 2020 §III, their 2019 wp extensions) and
Callaway–Sant'Anna's multi-valued/dose extensions. Record whether
treatment is absorbing, reversible, or continuous in the design matrix
before choosing the estimator reference class.

## 7. Reviewer checklist

- Estimand named before any estimator comparison; TWFE decomposition
  (`bacondecomp` / `twowayfeweights`) reported for staggered designs;
  forbidden-comparison share stated.
- Pre-trend evidence graded by power against the bias-relevant violation
  magnitude, not by "not rejected"; conditioning-on-pretest distortion
  noted when results are reported only after passing.
- Staggered event-study leads checked for Sun–Abraham contamination
  (`eventstudyweights` weight table).
- Sensitivity reported over Δ^RM/Δ^SD with a breakdown M̄ — not a single
  HonestDiD interval at an unstated bound.
- Functional-form dependence of PT flagged when levels-vs-logs flips
  conclusions; R-SA test offered.
- Treated-cluster count reported beside total G; C–T/RI routing when
  treated clusters are few (see `mackinnon_nielsen_webb_2023_few_clusters.md`).
- Treatment absorption status recorded; reversible/continuous treatments
  routed to the fuzzy/dose estimators, not the 2×2 decomposition.
