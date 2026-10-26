# Design and check matrix

Use this matrix to select checks. “Core” means mandatory whenever the design
permits it. “Conditional” means mandatory when the stated feature is present.

## Cross-design core

| Check | Applies when | Minimum record |
|---|---|---|
| Published anchor | Always | Version, table cell, estimate, N, inference, executed artifact |
| Assignment/dependence level | Observations share treatment or shocks | Level, cluster count, size distribution, rationale |
| Collapse test (point estimate) | A load-bearing regressor or instrument is constant within a coarser unit than the rows carry it — assigned, measured, or imputed at that coarser level | Collapse mode (average / drop-to-source), genuine-unit count vs nominal N, coefficient (and first-stage F for IV) before and after, and what the movement means — see the collapse-test record |
| Leave-unit/group-out | Independent units or natural groups exist | Full coefficient range and influential omissions |
| Functional form | Transform or nonlinear coding is load-bearing | Original and defensible alternative forms |
| Sample/scope | Inclusion rules or components may drive result | Named subsets, sample counts, estimate movement |
| Multiple testing | A family of outcomes/specifications supports one claim | Family definition, raw and adjusted inference |
| Negative control/placebo | A causally inert analogue can be justified | Rationale established before result |
| Magnitude / significance / variance | Each substantive empirical family; formal/model families use their own records | (a) **Practical magnitude** — effect in outcome units with baseline (always), plus the practical-significance measures the design supports: a realistic-dose counterfactual and a standardized effect size (Cohen's d / partial correlation / β·SD(x)/SD(ε)) computed at the level the regressor varies, per the practical-significance record — ES index formulas and conventions in `methods/cohen_1988_effect_sizes.md`; (b) design-appropriate inference for that estimate, including multiplicity where a family supports one claim; (c) Shapley values (LMG / dominance / relative-importance) for shares of variance actually explained when an R²-style decomposition is possible, per the decomposition record; `NOT_APPLICABLE` with reason when impossible. Never report (b) alone. The standardized effect size is a magnitude measure, not a variance-share proxy — never substitute partial R², semi-partial R², nested/incremental ΔR², or η² for (c); those are not Shapley shares and are not a PROXY for them. |
| Minimum detectable effect | A null or near-null carries interpretive weight; also record when MDE evidence appears during any check | MDE at conventional power against plausible effect sizes (power machinery in `methods/cohen_1988_effect_sizes.md`); hand design-validity threats to `claims` whether or not the result is a null |
| Omitted-variable sensitivity | A causal claim rests on selection-on-observables (controls) or on IV exogeneity/exclusion | Robustness value and partial R² of the treatment (or instrument); benchmark against named observed covariates; the confounder strength needed to overturn the claim — see the OVB-sensitivity record. Applies to OLS-with-controls and IV; `NOT_APPLICABLE` when the design identifies without a selection-on-observables or exogenous-instrument assumption |
| Variable semantics | Always, before quoting or correcting any number | Labels, generated columns, filters, and the file the live code actually loads |

## Design-specific requirements

### Instrumental variables

Core:

- first-stage coefficient and strength with design-consistent inference;
- reduced form;
- weak-instrument-robust confidence set or test;
- cluster count at the assignment or instrument-variation level;
- sensitivity to plausible controls and influential groups.

Conditional:

- overidentification diagnostics when multiple instruments exist;
- monotonicity and treatment-margin discussion for LATE claims;
- spatial dependence when the instrument is geographically smooth;
- omitted-variable-bias sensitivity for the exclusion restriction and
  instrument exogeneity: how strong an unobserved confounder of the instrument
  would have to be to overturn the finding — see the OVB-sensitivity record.

Do not treat a large non-robust first-stage statistic as proof of identification.
Strength and exclusion are separate. First-stage strength does not defend
exogeneity; run the OVB-sensitivity check on the exclusion restriction whenever
the identifying story rests on an assumed-as-good-as-random instrument.
Weak-IV critical-value sources: `methods/stock_yogo_2002_weak_instruments.md`
(i.i.d. case; bias vs size tables) and
`methods/montiel_olea_pflueger_2013_weak_iv.md` (effective F under
robust/clustered/HAC errors).

### Regression discontinuity

Core:

- local linear fit at a data-driven bandwidth (`rdrobust` / `rdbwselect`);
  conventional point estimate at hMSE with the RBC interval at hMSE and hCER —
  never conventional inference at a selector bandwidth;
- bandwidth and order sensitivity over hCER, hMSE, 2·hCER, 2·hMSE and p = 1, 2;
- density test — `rddensity`, Robust row, effective N and density estimates per
  side; binomial test in the smallest window when mass points are few;
- manipulation-robust bounds (Gerard–Rokkanen–Rothe breakdown) for every
  load-bearing estimate where one-sided manipulation is possible;
- predetermined covariates and placebo outcomes through the headline's
  procedure at each variable's own bandwidth, plus at the headline bandwidth as
  a labelled supplement;
- placebo cutoffs on each side using one side's observations, bandwidth
  reselected at each;
- donut at several small radii with the bandwidth reselected;
- RD plot with data-driven bins and the local fit inside the estimation window,
  not the default global polynomial alone;
- package versions recorded for every RD package run.

Conditional:

- covariate-adjusted headline: predetermined, balanced, additive covariates,
  bandwidth reselected with them, adjusted–unadjusted gap decomposed;
- fuzzy RDD: first stage with F ≥ 20 or fall back to ITT, single-bandwidth
  ratio with RBC, falsification on assignment, complier estimand;
- regression kink design — see the regression-kink record;
- discrete running variable or local-experiment reading — mass-point count
  decides the route; see the local-randomization RD record; EHW against
  running-variable-clustered SEs;
- boundary-discontinuity designs, including pooled distance-to-border and
  contiguous-pair regressions — see the boundary-discontinuity record;
- multiple cutoffs, cumulative cutoffs, multi-candidate elections, or
  non-geographic multiple scores — cutoff-specific estimates and pooling
  weights (`rdmc`), boundary-point plus pooled distance estimates for two
  scores (`rdms`);
- extrapolation claims away from the cutoff — see the RD extrapolation record;
- heterogeneous RD effects: RBC intervals per subgroup and for the difference
  (`rdhte`), never two subgroup intervals compared by eye;
- RD-specific minimum detectable effect (`rdmde`, `rdpower`) at the paper's
  specification when a null or small RD result is load-bearing;
- geographic/spatial dependence for the paper's pooled border regression.

### Difference-in-differences and event studies

Core:

- adoption/timing inventory;
- estimator valid for the observed timing structure;
- event-time coefficient path with uncertainty, with Roth pre-test power and the
  HonestDiD breakdown M̄ (a non-rejected pre-trend is not validation);
- in-sample placebo cutoff: with more than two pre-treatment dates, the headline
  spec re-run on the pre-period alone with the cutoff moved inside it
  (`did-event-study-diagnostics`);
- alternative comparison groups;
- cluster level aligned with treatment assignment;
- anticipation and terminal-period sensitivity.

Conditional:

- heterogeneous-effect decomposition with staggered adoption;
- balanced-panel check when composition changes over event time;
- spillover checks when untreated units may be exposed.

### Panel models without a treatment event

Core:

- unit and time dependence;
- serial-correlation-robust inference;
- unit/group leave-outs — with the sign of `b_full − b_drop` checked before
  any "one unit drives it" claim (a deletion that strengthens the estimate
  is not fragility);
- balance, attrition, and timing-path checks;
- sensitivity to fixed-effect structure.

### Time-series and trending-levels designs

Trigger: any headline or mechanism result regresses one **trending or highly
persistent time-indexed series** on another (aggregate GDP, prices, wages, skill
premia, money, population, national ratios, indices, market-integration price
gaps), or a structural/calibrated model is fitted to such trending aggregates over
time. Fires alongside `panel-diagnostics` for a dynamic panel and alongside
`cross-sectional-diagnostics` for a market-access design that also carries a price
series over time. It does NOT fire for a pure spatial cross-section, geographic
RDD, or a DiD/event study whose regressor of interest is a binary treatment — that
is a *spatial* or *panel-serial-correlation* problem, handled by the spatial
record and `panel-diagnostics`, not here. The temporal and spatial spurious-
regression problems are analogues but distinct; the spatial battery
(Müller–Watson's spatial unit-root and spurious-regression tests in the
Becker–Boll–Voth SPUR port, and SCPC) never substitutes for this one.

The full temporal protocol — opposite-null order classification, the
cointegration menu, the Prais–Winsten/first-difference survival path, ARDL
bounds, holdout validation, calibrated power, and the synthesis standard —
is `methods/spurious_regressions_guide.md`; the space–time
correspondence and spatial analogues are in
`methods/spurious_space_time_unified_guide.md`.

Core:

- integration order on each series in levels and first differences, by
  **opposite-null** tests (ADF/PP with H0 = unit root, and KPSS with H0 =
  stationarity), deterministics matched to the claim; test differences to exclude
  I(2); classify the *evidence*, not the series;
- an endogenous-break unit-root test (Zivot–Andrews) with the selected date and
  break-valid critical values;
- cointegration when outcome and regressor(s) are I(1): a residual test
  (Engle–Granger and/or Phillips–Ouliaris) **with response-surface critical
  values matched to the number of stochastic regressors and the deterministic
  case — never ordinary ADF/KPSS tables**, a system test (Johansen trace with
  reported VAR order/deterministic case/rank), and a **reversed-null** test (Shin
  on Stock–Watson DOLS residuals with Shin's own critical values);
- the R²-vs-Durbin–Watson (Granger–Newbold) fingerprint for every levels spec;
- coefficient survival under iterative Prais–Winsten (report ρ̂ and before/after
  coefficient, SE, DW) and under first differences with Newey–West HAC SEs;
- an order-agnostic ARDL/ECM bounds test (Pesaran–Shin–Smith), counting all regressors in the tested levels relationship in k (including I(0), excluding the lagged dependent variable and deterministics) and matching the deterministic case;
- out-of-sample validation on a frozen training window (holdout RMSE and R²_OOS).

Conditional:

- break-robust cointegration (Gregory–Hansen / Maki) when a regime shift in the
  long-run relation is plausible;
- persistence-matched **noise-regressor placebos** where the design allows —
  how often does an unrelated series with matched length, missingness, drift,
  volatility, and persistence reproduce the published coefficient/*t*/R²;
- **calibrated size-and-power Monte Carlo — mandatory at short T (T ≲ 40) before
  any non-rejection is cited**: no-cointegration tests can have near-zero power at
  short T (an underpowered non-rejection is no evidence); Shin is not uniformly
  conservative — undersized at short T with weak persistence, oversized at high
  residual persistence — so weigh a rejection only against the size Monte Carlo
  at the data's own ρ̂; Engle–Granger without trend
  is oversized on drifting series; fitted residuals are not stationary by construction; residual-based tests require critical values accounting for estimation and, where relevant, selection; under cross-sectional
  dependence use Pesaran CIPS, not first-generation panel unit-root tests.

The decision rests on **convergence across differently-identified evidence**, not
on any single I(0)/I(1) classification and never on a high in-sample R² — see the
time-series synthesis record below.

### Randomized experiments

Core:

- assignment and analysis-unit match;
- attrition and missingness;
- prespecified outcome family and multiplicity adjustment;
- intent-to-treat estimate;
- randomization inference when feasible.

Conditional:

- treatment-on-treated or IV analysis for noncompliance;
- interference/spillover analysis when treatment can cross units.

### Cross-sectional observational studies

Core:

- functional form and common support;
- influence and leave-region/group-out;
- dependence structure, including geography;
- collapse test on the point estimate when a load-bearing regressor is constant within coarser units;
- transparent covariate sensitivity;
- negative controls where substantively justified.

### Shift-share and exposure-weighted designs

Trigger: any regressor or instrument built as an exposure-weighted sum of
shocks — including designs the paper does not label as shift-share. Regroup
them as latent shift-share designs; unit-level robustness checks do NOT answer
shock-level concentration.

Core:

- **identifying-margin adjudication** — name which margin (exogenous shares
  vs exogenous shocks) the design's strongest defense claims, defend the
  choice, and route verdict-bearing tests to it; tests on the other margin
  are recorded with `row_role = rebuttal`;
- Rotemberg-weight concentration computed on the exact estimation sample;
- effective number of shocks;
- verification of the decomposition identity on the estimation file;
- separation of exposure level from identifying shock variation;
- placebo-shock rejection.

Conditional:

- shock-level (AKM0-style) inference when shocks are few or concentrated;
- null-imposed shock-level score test;
- **share-margin rows** (required when the adjudication claims share
  exogeneity): a negative control or pre-trend loading the instrument on a
  pre-period outcome; share-level balance or covariate predictability of the
  exposure; a constant-shock placebo where feasible — share exogeneity fails
  on evidence about the shares, not on shock-level inference;
- unit-exclusion robustness — run it, but never report it as the answer to
  shock concentration.

Source-audited cribs:
`methods/shift_share/gpss_2020_bartik_instrument.md` (Rotemberg
weights, decomposition),
`methods/shift_share/bhj_2022_quasi_experimental_ssiv.md` (shock
exogeneity, incomplete-shares and period-interaction controls),
`methods/shift_share/akm_2019_shift_share_inference.md`
(AKM/AKM0),
`methods/shift_share/borusyak_hull_2020_nonrandom_exposure.md`
(recentering).

### Synthetic control and synthetic difference-in-differences

Core:

- pre-period length adequate for the chosen inference procedure, with the
  consequence routed (short T0 → penalized/augmented estimator plus
  placebo-resolution limits);
- placebo-unit effect distribution and the treated unit's rank within it —
  ranked on the post/pre RMSPE ratio over a pre-fit-screened pool, with J
  and the smallest attainable p reported (a resolution-limited grid is
  "uninformative," not a null);
- weight diagnostics: sparse, extreme, or degenerate weights, plus donor
  leave-one-out and placebo-pool contamination screening;
- terminal-period sensitivity;
- alternative-estimator refit (augmented SC / SDID / generalized SC) and
  conformal inference beside the placebo rank;

- model-based prediction interval (`scpi`) beside the placebo rank, with the
  weight constraint stated and varied (simplex / lasso / ridge / ols).

Conditional:

- lagged-outcome covariates: check whether they collapse the weights onto the
  outcome path, making the fit mechanical;
- in-time (backdated) placebo treatments;
- staggered adoption or multiple treated units via `scdataMulti` (`scpi`).

### Scale-sensitive transforms and count outcomes

Trigger: `ln(1+x)`, asinh, counts, rates, per-capita scaling, floors, or
ratios over weak denominators, in the outcome or a load-bearing regressor.

Core:

- unit-rescaling sweep inside the log/asinh — if the estimate moves with the
  measurement units, the transform is doing the work (why it moves, what the
  sweep measures, and the alternative estimands:
  `methods/chen_roth_2024_logs_with_zeros.md`);
- count model (Poisson or negative binomial) on the full sample, compared with
  the transformed specification and its implicit sample;
- count versus per-capita specification where population scales the outcome;
- difference or probability statements in place of unstable ratios;
- placebo and robustness checks run in the SAME corrected specification as the
  main effect, not in a convenient alternate framework.

Conditional:

- bootstrap-through-the-model for long-run, net-present-value, or other
  quantities derived by pushing the estimate through further modeling.

### Controls, samples, and denominators that define the estimand

Trigger: a control horse race, a mediator control, an aggregate attribution
claim, a subset restriction, or covariates built from the same source as the
regressor.

Core:

- time-invariant covariates under fixed effects entered as
  covariate-by-period where the claim requires their effect to vary;
- coefficient shrinkage distinguished from standard-error inflation when a
  control "kills" a result — with the causal model (confounder / mediator /
  collider / confounded mediator) named per Cinelli–Forney–Pearl before any
  prescription, and the reference specification named;
- mediator controls built from the treatment machinery identified and
  removed — unless the mediator is itself confounded, in which case both
  specifications are biased;
- multi-treatment contamination screen (GPHK) where treatments horse-race in
  one regression;
- same-source covariates checked for near-duplication and scale or no-data
  artifacts, with the residualised correlation and provenance diff reported;
- treated shares and always-treated shares computed from the regression
  sample, not taken from the text;
- aggregate-denominator claims checked for a sign-homogeneous, transportable
  denominator (an ATE can hide constant, fanned or sign-reversing effects:
  `methods/gelman_hullman_kennedy_2024_causal_quartets.md`).

Conditional:

- saturated group-by-period fixed effects or a sample restriction in place of
  single-group dummies, where the question demands it.

### Small samples and minimum detectable effects

Core:

- minimum detectable effect at conventional power against the claimed and
  plausible effect sizes — underpowered does not mean refuted, and a null
  from an underpowered design is uninformative; hand every design-validity
  threat (power, identification, isolation, measurement, discriminating
  power) to `claims` as it appears, not only when the result is a null;
- lean or bivariate re-tests when saturated controls overfit a small sample;
- estimator-specific small-sample standard-error artifacts (for example,
  quantile-regression standard errors at small N).

### Formal theory and quantitative models

Trigger: a target result whose truth rests on a **proof** (theorem,
proposition, lemma, derivation, closed-form claim) or whose magnitude comes
out of a **calibrated/simulated model**. Routes to `theory-diagnostics` and
`quantitative-model-diagnostics` respectively; both fire on a hybrid result
that is proved *and* calibrated, and either fires alongside the empirical
checks when an estimate inherits its meaning from the model. A kill here is a
construction — a counterexample, a simulation, a re-derivation, a sensitivity
sweep — never an assertion.

Formal-theory core (`theory-diagnostics`):

- re-derivation of each load-bearing result from the paper's own primitives;
- counterexample construction — an object meeting every hypothesis and
  violating the conclusion;
- weaker-statement check — same quantifiers, domain, inequality strength,
  existence-vs-uniqueness, mode of convergence, notion of solution;
- assumption stress test — each stated assumption's use and sufficiency, and
  the hunt for the missing/stronger-property-drift assumption;
- cited-result misuse — invoked theorems whose hypotheses are unmet or that
  deliver a weaker/converse conclusion than the proof uses;
- definition grounding to each symbol's explicit defining equation, run as a
  separated defender step before any verdict (the anti-strawman guard).

Formal-theory conditional:

- numerical simulation of the paper's model to adjudicate an
  "invalid method / it collapses" claim, with code checked against definitions and assumptions and the conclusion restricted to what its quantifiers allow;
- fabricated-grounding guard when a defence rests on "the paper states X" —
  the sentence must be locatable in the paper text.

Quantitative-model core (`quantitative-model-diagnostics`):

- free-parameter inventory (externally calibrated / internally set to targets
  / assumed with no anchor), and the headline's dependence on each;
- calibration-sensitivity sweep across defensible parameter ranges, reporting
  the headline quantity's range in the paper's units;
- targeted vs non-targeted moments — fit on moments the calibration did not
  target, since targeted moments match by construction;
- mechanism attribution — shut each channel off in turn and report its share
  of the headline (the model analog of variance decomposition);
- solve-the-stated-model check — the code implements the written model
  (equations, parameters, targets, closure), and the numerical solution is an
  actual solution at the calibrated point (convergence, residual/Euler errors,
  grid sensitivity, existence/uniqueness where claimed).

Quantitative-model conditional:

- closure/functional-form sensitivity when the form is a choice theory did not
  force;
- bootstrap-through-the-model for long-run/NPV/welfare quantities derived by
  pushing an estimate through further machinery;
- external/out-of-sample implication where the model implies a checkable fact
  outside its calibration sample.

Premises (`whimsical-assumptions-diagnostics`), whenever a conclusion is
derived from a model:

- inventory of stated, structural, closure, exclusion and bridge premises,
  each grounded in a quotation or the equation that embodies it;
- critical-assumption test — one realistic relaxation per premise, rebuilt
  and run, effect in the paper's units;
- warrant grade from a source measuring the same quantity (the paper's own
  evidence first), never from priors;
- signed exclusions against any "bound" wording; built-in conclusions;
  the bridge from model to policy claim;
- WHIMSICAL only when critical and unwarranted are both shown.

Do not force the magnitude/significance/variance triple onto a theorem — it is
estimate-shaped and meaningless for a proof. A structural model *estimated* on
data with standard errors keeps the empirical inference and identification
checks; one fitted to trending aggregates over time also triggers
`time-series-diagnostics` (minimizing fit residuals does not guarantee stationarity or establish a long-run relation).

### Variable semantics and live-data gate

Before quoting or correcting any number, verify variable and value labels,
generated-column semantics, subset filters, and the file the live code
actually loads. A label mismatch or hidden build-step transformation is a
battery finding when it changes a tested result; otherwise record it as a
lead for the data audit in `code-and-data`.

## Magnitude, significance, and variance decomposition record

Run this for each substantive result family, not as an afterthought.
**Statistical significance is not practical significance**: a coefficient can
be estimated precisely and still be trivial in the world. A celebrated
precisely-estimated reduced form is the type case — p < 0.001, yet small
relative to the noise the model leaves unexplained. Report three dimensions, never significance alone:

1. **Practical magnitude** — how big the effect is in the world. The
   outcome-units anchor is mandatory; add the measures the design supports and
   mark the rest `NOT_APPLICABLE` with a reason. This is a menu keyed to the
   design, not a mechanical computation of all four:
   - **Outcome units, against a baseline** *(always)* — the effect in units a
     reader can picture, against the base rate or mean (an elasticity when the
     specification is log-log).
   - **Realistic-dose counterfactual** *(whenever the treatment has an observed
     real-world range)* — plug in the *actual* change in the regressor, not a
     textbook one-unit or one-SD move, and compare the implied outcome change
     to a meaningful yardstick: the outcome's own SD across units, or its total
     observed change over the period. This most directly answers "did it
     matter." *Worked instance (a transfer-response design):* the average rise
     in the exposure per worker was a few thousand dollars; at the
     coefficient this implies a per-worker effect of only a few percent of
     the cross-unit SD — a rounding error on the noise. **Guardrail:** a within-FE / relative design identifies only
     relative effects; do not scale its coefficient into a national or
     aggregate total (the missing-intercept problem). Flag the ceiling rather
     than fake the number.
   - **Standardized effect size** *(when the outcome scale is not itself
     interpretable, or for comparison across specs or papers)*. Report it in the
     currency the regressor makes natural. For a **continuous** regressor, label the partial correlation separately from β·SD(X)/SD(ε); state whether X is raw or residualized and how residual SD is scaled. For a **binary** regressor, β/SD(ε) is a residual-SD-standardized contrast; identify when it is the conventional unadjusted Cohen's d based on pooled within-group SD, and use an explicit degrees-of-freedom correction for Hedges' g. The familiar r = d/√(d²+4) conversion assumes balanced groups and compatible population scaling; unequal groups, finite-sample SD conventions, or covariate adjustment need the corresponding adjustment. Do not use it as a universal partial-correlation conversion.

     **GATE — compute at the level the regressor varies, and at the level the
     claim is about where that is finer; report both and say which the claim
     needs.** When observations are finer than the level treatment varies
     at (individual respondents under a group-level treatment), idiosyncratic
     noise inflates SD(ε) and flatters a "the effect is trivial" story, which a
     defender reverses in one sentence. Worked case: a standardized effect reads as
     small at the individual level but several-fold larger at the group
     level where the treatment lives. Compute it where the treatment lives
     before citing it.
   - **Benchmark** *(when a comparator exists)* — the effect beside an
     established driver in the same model, or the same effect in the prior
     literature. Practical significance is comparative.
2. **Statistical significance** under design-appropriate inference for that
   cell (and the multiplicity-adjusted figure when the cell sits in a
   published family).
3. **Share of variance explained** whenever an R²-style decomposition is
   possible: **Shapley values** (LMG / dominance analysis / relative-
   importance) for the focal regressor and the major control blocks. Skip
   only when the estimator or design makes the decomposition impossible;
   mark `NOT_APPLICABLE` and state why.

**Keep magnitude and variance allocation distinct.** Let X̃ and Ỹ be residuals after projecting X and Y on the same controls, using the same sample and weights. The partial correlation is r = cor(X̃,Ỹ), and partial R² = r² for a single added regressor. With a common sum-of-squares scaling for X̃ and full-model residual ε, f = β·SD(X̃)/SD(ε) satisfies r = f/√(1+f²), not r = f. Different degrees-of-freedom conventions require adjustment. β·SD(raw X)/SD(ε) is yet another standardized coefficient. Report exactly which was computed; none satisfies the separate Shapley/LMG requirement. A unit-SD regressor does not make f equal √(partial R²).

**FORBIDDEN substitutes for this dimension [CRITICAL].** Do not report
partial R², semi-partial R², nested/incremental ΔR² (R²_full − R²_reduced),
or η² / partial-η² as "share of variance explained." Those measure unique
contribution conditional on the other covariates already in the model; they
are not Shapley shares and are not an acceptable PROXY when a packaged LMG
run is unavailable. If the decomposition exists but no Shapley/LMG run can be made, mark `NOT_RUN` with the
reason (the module stays `INTERIM` only while a packaged run is feasible) — do
not fill the cell with a one-order R² increment.
(Partial R² belongs in the OVB-sensitivity record below, not here.)

A large significant coefficient that explains almost none of the outcome is
a different finding from one that dominates the variance — record both. For
the variance decomposition specifically, record:

- method: Shapley / LMG / dominance (name the algorithm and software —
  `relaimpo`, `domir`, `shapley2`, or a hand-coded LMG in another environment);
  never a one-order partial or nested R² labelled as a share;
- block definitions and the rationale — blocks are chosen by the question,
  and an undifferentiated "other controls" block that hides sensitivity is
  not acceptable;
- fixed-effect handling: fixed effects included as blocks, or the
  within/two-way-FE decomposition, stated explicitly;
- shares reported against a named variance denominator (Shapley values sum to the corresponding R²). Residualizing on FE gives within shares; convert to original-total units with SST_within/SST_original on the same sample and weights, accounting separately for FE. Any
  share-of-explained-variance figure labelled explicitly as "of the R² the
  model explains";
- weights: when the paper estimates with weights, do not trust a packaged
  decomposition to handle them — validate against a hand-coded weighted
  decomposition and record the reconciliation;
- software, version, and seed where resampling is involved.

Track the decomposition separately from the coefficient: which units drive
the coefficient and which drive a published magnitude or contribution share
are different questions with different answers.

## Few-cluster implementation record

Do not reduce “wild bootstrap” to a command name. Record:

- number of clusters and cluster-size distribution — nominal G AND the
  partial-leverage effective count G* (Carter et al. 2017; ρ = 0 iff the
  spec carries cluster fixed effects);
- statistic and null hypothesis;
- the variant: WCR-S (`boottest …, jk noci` followed by `assert !missing(r(p))`; R `bootstrap_type = "31"`) is the only
  primary bootstrap. WCR-C (plain `boottest`, tagged `WCR-C-robustness`) is always reported beside it,
  never alone; WCU (unrestricted, tagged `WCU-robustness`) is a robustness row.
  Both are tagged in the code. The bootstrap itself ranks below the CV3 jackknife, and
  below randomization inference when treated clusters or effective shocks are few
  (rule 9, small-n module);
- weight distribution;
- repetitions or exact enumeration;
- random seed;
- finite-sample adjustment;
- p-value and interval construction;
- software and version;
- validation against a test case or independent implementation.

The appropriate method depends on cluster count, balance, leverage, and
estimator. If no validated implementation is available, mark the check
`NOT_RUN` and the module `INTERIM`.

## Collapse-test record

Clustering, wild bootstrap, and randomization inference repair the *standard
error*; they never touch the *point estimate*, which they read off the same
pooled fit as naive OLS. That is sufficient only when the non-independence
lives in the error term, orthogonal to the regressor — the random-effects
case where OLS is already unbiased and precision is the whole disease (Moulton
1990). When the regressor or instrument is itself constant within a coarser
unit than the rows carry it — assigned, measured, or imputed at that coarser
level — the pooled coefficient is a *row-weighted* estimate, and an honestly
clustered interval sits around that row-weighted number. Whether that is *the
wrong number* depends on the case, and the two must not be conflated. For
**genuine rows** carrying a coarse attribute (each row a real observation),
the row-weighted number is a valid estimate for a defined estimand: collapsing
to the coarser unit while **retaining the original weights and controls**
reproduces it — the coefficient exactly when every regressor, controls included,
is constant within the coarse unit (approximately otherwise), and the clustered SE
up to the CV1 small-sample factor (compare under CV0 or rescale) —
so the pooled estimate is not an artifact, and equal-weight/no-adjustment collapses
are *named specification sensitivities with different estimands*, not
corrections. Two readings still make the equal-weight fit more than a
sensitivity. If the claim is a common effect, both weightings estimate the same
slope, so a gap large relative to its sampling error is evidence that the effect
is not common, and the claim must then say which average it means. And when the
residual intraclass correlation within the coarse unit is high, a unit's extra
rows add almost no information about that slope, so the equal-weight fit is the
more precise estimate of it; report that correlation beside the two fits. For **donor-substituted, fabricated, or imputed copies**, a copy
carries zero independent information, so the row-weighting genuinely is wrong
and drop-to-source is a correction. The point-estimate counterpart to the
assignment-level clustering check is therefore to **collapse to the genuine
independent units** — after first confirming, for the genuine-rows case, that
the estimand-preserving (original-weight) collapse reproduces the pooled fit.

Trigger: a load-bearing regressor or instrument takes fewer distinct values
than its row count because one coarse value is spread across many rows — an
aggregate regressor merged onto micro units (intraclass correlation ≈ 1), a
coarse-resolution variable, or donor-substituted / interpolated / imputed
values.

Two modes, always named (never let "collapse" default to averaging):

- **average** — for genuine replicates of a real unit (subsamples of one
  assignment): one row per unit, the unit mean. First run the
  **estimand-preserving** collapse (retain original row-count/analytical
  weights and controls) to confirm it reproduces the pooled coefficient and
  clustered SE (the coefficient exactly only when all regressors, controls
  included, are constant within the unit — a row-varying control makes the
  match approximate; the SE up to the CV1 small-sample factor); the equal-weight unit mean is then a distinct target, reported
  as a sensitivity, not a correction, unless the equal-weight estimand is
  argued to be the right one.
- **drop-to-source** — for donor-substituted, fabricated, or imputed values;
  a copy carries zero independent information, so its correct weight is zero:
  keep only the sourced rows.

Record:

- which mode and why (replicate subsample → average; imputed/donor copy →
  drop-to-source);
- the genuine-unit count versus the nominal N;
- the coefficient before and after collapse, and — for an instrument — the
  first-stage F before and after;
- what the movement means, read off the variable's role. For a **regressor**
  on genuine rows, confirm the estimand-preserving (original-weight) collapse
  reproduces the pooled fit, then read equal-weight movement as one-vote-per-
  unit *re-weighting* toward a different estimand, not proof the pooled number
  is wrong — *worked instance*: about a dozen genuine values of a historical
  regressor spread across ~40 country rows; equal-weight collapse roughly
  halves the OLS coefficient, so the estimate depends on whether
  the claim needs a per-country or a row-weighted target — state which, do not
  assume. (Donor/imputed copies are the separate drop-to-source case, where
  the movement *is* a correction.) An **instrument** whose first-stage F collapses has lost
  identification, and the 2SLS estimate bends toward OLS under the weak
  instrument — *worked instance*: a donor-substituted instrument with most
  country values filled from a sourced minority; drop-to-source halves
  the first-stage F into the weak-instrument zone.

State the finding in plain terms — the pooled estimate row-weights the genuine
values by their replicate counts; giving each unit one vote (Hurlbert 1984)
changes it to a different, equally-defined estimand, and the review's job is to
say which estimand the paper's claim needs, not to assume one-vote-per-unit is
automatically correct. Do **not** re-describe it as informative cluster size,
`Cov(n,β)/n̄`, effective-sample weighting, or a within-cluster-resampling
correction: those port the critique back into the standard-error apparatus it
is aimed at, and miss that the re-weighting changes the estimate, not the variance.
This check is the estimate-side complement of the few-cluster record (the
inference side); where the dependence is in the regressor, run both.

## Spatial implementation record

For every spatially exposed result, keep five manifest rows. Conley/HAC and SCPC are required; the spatial-lag/SLX refit, Kelly and CKK are additionally required for smooth or interpolated regressors/instruments. Other rows need an explicit NOT_APPLICABLE rationale. Required work the review can still do and has not makes the family INTERIM; a row blocked because the authors never deposited its inputs (no coordinates) is BLOCKED and the result unverifiable as published (rule 7 of the review skill), not INTERIM. Neither is scientific falsification.

Record the sample, coordinate source, projection and units, distance metric, original coefficient and interval, residual diagnostics and reference procedure, region leave-outs, and a substantively justified spatial scale grid. A token short cutoff does not address longer-range dependence.

| Procedure | Required record | Interpretation |
|---|---|---|
| Conley/HAC | Kernel, cutoff grid and units, finite-sample convention, estimate and interval at each cutoff | Baseline dependence-robust inference under its assumptions; strong dependence can cause undercoverage. A Conley-only run does not complete this battery. |
| Müller–Watson SCPC | Model/transform, correlation model and avc grid (e.g. 0.03/0.10/0.25, with rationale), coordinate metric, interval and implementation | Assumption-indexed inference. Assess validity and plausible bounds; loss of significance at one bound does not prove no effect, spuriousness, or failure of causal identification. Do not automatically privilege an unsupported bound. |
| Spatial-lag/SLX refit | Spatial weights (contiguity or distance band, cutoff and units, row standardization), the lagged terms added (WX of the focal regressor; WY if SAR), own-unit coefficient beside the published one, spillover coefficient, interval under the same HAC record | Tests whether the published point estimate is spillover-inflated — the coefficient side Conley and SCPC leave untouched. A shrunken own-unit coefficient is a magnitude finding even when inference holds; a stable one does not by itself rule out spillovers through a channel the weights omit. |
| Kelly matched-noise placebo | Estimated noise structure, basis choice, simulation count/seed, actual statistic and placebo distribution, clustering and numerical options, Monte Carlo uncertainty | Tests whether the specified matched-noise process can mimic the association. Its validity depends on that process and implementation; it is not a universal causal test. |
| Conley–Kelly–Kozbur pre-whitening | Basis/knots, actual rank, selected PCs and selection curve, residual degrees of freedom, identifying variation before/after, coefficient/SE/interval, HAC support and bandwidth record | The WP26/11 method targets inference with spatial basis functions whose population coefficients are zero under the model. Finite-sample chance correlation can remove identifying variation. Coefficient movement is sensitivity evidence, not by itself proof of confounding; a stable coefficient is not proof that confounding is absent. |

Read disagreements against the paper's claim. Separate coefficient movement from SE inflation, investigate model validity and retained identifying variation, and compare intervals to substantively meaningful effects. All applicable checks must be run; their significance indicators are not a conjunction of necessary causal conditions. A supported confounding mechanism or valid counterexample can overturn a causal claim; an imprecise estimate may instead limit what can be asserted. Report the strongest supportable conclusion, including inconclusive evidence when appropriate.

For interpolated surfaces also assess residual variogram range, a justified GLS/SEM refit, regional influence, and sensitivity to projection. The CKK Condition 6 concerns the support of the basis actually used: quantile knots are not uniformly spaced, and PC mixtures can have much wider support than individual splines. Use the geometry and same distance units as HAC; document whether the theoretical condition is established or the implementation is an empirical sensitivity exercise. See `software-examples.md` for interfaces and support metadata; the source-audited space–time protocol behind the SCPC/SPUR and half-life-GLS machinery is `methods/spurious_space_time_unified_guide.md`.

### Spatial field lessons (folded from the research-memory battery)

- **The three test families answer different questions — never net them into one verdict.** Conley/HAC repairs *standard errors* under spatial error correlation and leaves the point estimate untouched; it is the weakest element and says nothing about confounding or spuriousness. Kelly matched-noise placebos test whether the regressor is distinguishable from noise with the *same* spatial autocorrelation structure (and are ill-posed when the "treatment" is itself geography — collinear with the spline basis — which is itself a finding about a geography instrument). Müller–Watson/SPUR tests spatial unit roots and spurious regression. "Survives Conley but fails SPUR" is coherent — consistent with spuriousness, not diagnostic of it (an underpowered cointegration test fits the same pattern) — and not a battery conflict. Report each element's verdict on its own question.
- **Do not predict the direction of the Conley correction.** Negatively correlated scores (x̃_i·ε̂_i, the partialled regressor times the residual) at the cutoff scale *tighten* the SE; Conley has strengthened t-stats in multiple audits, and the sign can flip across cutoffs within one paper. Report the whole cutoff profile, not one number. Mechanism: the Conley variance is a quadratic form in the scores, and the OLS FOC (Σg_i = 0) drives it toward zero as the cutoff approaches the domain — near the domain size the matrix goes non-positive-definite and `acreg` returns nothing, so a reported large-cutoff SE is built from the most-distant, highest-leverage pairs and is unstable, not "conservative." Consistency also needs cutoff/domain → 0, so a cutoff that is a large fraction of the study region is invalid on its own terms. A spatial SE *below* the White SE at a cutoff near the domain scale is the FOC artifact, not a passed correction; at short cutoffs, show the score-correlation sign (x̃·ε̂, not ε̂ alone) before reading it either way.
- **Cluster demeaning is itself a transform.** Regressing the fields on group FE, then finding the residuals stationary, is what MW's spatial transforms are designed to produce — it is not evidence the underlying regression is non-spurious. Run SPUR on the RAW within-group data; check sign stability of the relationship across groups; read an LBM-GLS collapse as persistence sensitivity, not proof of spuriousness (collapse does not show the structural effect is zero); and route per the unified guide's tested router, on the outcome's I(0)/I(1) tests AND the focal regressor's I(1) stamp — not on the dependent variable alone. A single SPUR verdict is low-power corroboration, never a standalone knockout — the decisive standard is a calibrated independent-fields Monte Carlo.
- **Attribution:** the I(0)/I(1) spatial tests are Müller–Watson's (2024, *Econometrica*); Becker–Boll–Voth (2026, *Stata Journal*) ported them as the SPUR package and contributed the flowchart/router. Credit the port as a port.
- **Interpolated/constructed regressors (the acute Kelly case).** When the regressor is an interpolated surface (IDW, kriging, smoothed raster), the spatial autocorrelation voiding the published SEs is partly *manufactured by construction*: run residual Moran's I with a permutation p-value (say outright if the classical SEs are invalid), the empirical variogram's practical range vs the domain (no sill in-domain ⇒ non-stationary ⇒ spurious zone; distrust auto-fitted ranges — Cressie weighting can manufacture a false GLS kill, trust the range the points reach), a constructive spatial-error/GLS refit (report coefficient survival separately from star survival), a smoothness-matched noise placebo at the same source points and power, and a region-dummy + leave-one-REGION-out check — a between-region contrast labelled a treatment effect collapses when the dummy absorbs it, and leverage spanning several clusters is invisible to single-cluster LOO. If the grid was built in a distorting projection (Mercator), re-run the whole battery in an equidistant/equal-area projection — cell counts and coordinates change, the verdict should not.
- **Smooth/continental fields fail on the unprobed dimension.** When the treatment is a smooth field over many units × periods, the dependence the published SEs miss is usually cross-sectional WITHIN a period (one continental shock hits every unit), not the within-unit serial correlation the authors cluster on. Cluster two-way (spatial unit AND time) and report it; sweep the Conley cutoff out to the field's true correlation range, not the authors' cutoff; leave-one-REGION/country-out, not just one cluster.
- **Binary treatments need Moran-matched placebos.** Conley–Kelly leaves the spatial-noise placebo blank for binary treatments; build it: draw Gaussian random fields at the unit locations, threshold top-k to the treated count, run each fake treatment through the outcome's ORIGINAL estimator (Poisson as Poisson — adapt the correction to the model). Calibrate the nugget by bisection until thresholded draws' mean Moran's I (same W as the diagnostics) matches the real treatment's, in every regression sample — that acceptance test is mandatory; a binary indicator's total sill must be ≤ p(1−p).
- **"Conley–Kelly inference" names two different statistics.** The BCH-with-basis regression (spatial basis + few-cluster sandwich) fails size on smooth treatments (false rejection .15–.27 at nominal 5%, worse with more clusters); the Ibragimov–Müller per-cluster t-test is honest (.03–.07) and well powered. Before quoting or relying on a CK-flavoured number, establish WHICH statistic it is — a run reporting IM output under a BCH label misstates the test.

## Local-randomization RD record

Trigger: a running variable with few distinct mass points near the cutoff,
or a paper that reads its design as a local experiment or reports
randomization inference. Record:

- the estimand of every number: θ, the average effect in the window (state
  the window), or τ, the effect at the cutoff; with a discrete score, say that
  any statement about τ rests on extrapolation from the adjacent mass points;
- distinct mass points inside the window on each side, and observations per
  point;
- the window-selection rule: balance statistic, the predetermined covariates
  used, α* (default 0.15; below 0.10 is unsupported), minimum observations per
  side, step (by observations or by length), Fisherian or approximate
  balance p-values, and the resulting window on each side — or, with a
  discrete score, the adjacent-mass-point start and each enlargement; a window
  taken from an MSE or CER selector is not a local-randomization window;
- observations inside the window on each side;
- the manipulation test: binomial p-value for the counts in the chosen and the
  smallest window, the assignment probability q (normally 1/2), and the tool
  (`rdwinselect` or `rddensity`'s binomial output);
- covariates and placebo outcomes tested in the window, including covariates
  not used to select it;
- the test statistic, the randomization mechanism (fixed margins, or Bernoulli
  with the unit probabilities passed), repetitions or exact enumeration, the
  seed, and the outcome model (p = 0, or the polynomial and its defence);
- the Fisherian p-value for the sharp null and the large-sample p-value for
  the average effect, each labelled, and any interval with the effect model it
  inverts;
- sensitivity in windows inside the chosen one (wider windows only as stress
  tests), and, where an unobserved confounder of assignment inside the window
  is the threat, `rdrbounds` (Γ grid, window, statistic, and the Γ at which the
  upper-bound p-value crosses the test level) — it bounds the sharp-null
  p-value, not the effect;
- for a paper that clusters by the running variable: EHW standard errors beside
  the clustered ones, and any Kolesár–Rothe interval with its curvature bound.

Report the local-randomization estimate and the continuity-based estimate
together, each with its estimand. With a continuous score, disagreement points
to a failed exclusion restriction in the window and the continuity result
stands; with few mass points the order reverses. A discrete running variable
that only ever appears with a wide-bandwidth continuity fit is an unexamined
identification claim, not a robust one. This record does NOT fire on a
genuinely continuous, densely sampled score that the paper does not read as
a local experiment; mark it `NOT_APPLICABLE` and say so.

## Boundary-discontinuity record

Trigger: an RD whose score is a two-dimensional location or distance to a
border, including pooled distance-to-border regressions and contiguous-pair
comparisons. **Incomplete without a WBATE.** Pointwise BATEC alone does not
clear this record.

Record (all required unless marked optional):

- the paper's pooled specification classified by the Cattaneo–Titiunik–Yu
  taxonomy: treatment × polynomial interaction, segment fixed effects,
  bandwidth source, inference;
- **estimand_id** for every reported number, named by estimator and weights —
  at least `rd2d_WBATE_density_location` and `rd2d_BATEC_point`, plus
  `rd2d_WBATE_equal_location`, `rd2d_WBATE_density_distance` and `rd2d_LBATE`
  where run; never mix a pooled distance RD and a WBATE in one "survives"
  sentence;
- the score: location-based bivariate `(x, y)` via `rd2d`, and/or
  distance-based via `rd2d.distance` (N×J signed distances to each evaluation
  point); coordinate projection and distance metric (chordal or geodetic, never
  Euclidean on raw latitude/longitude);
- the evaluation points: construction rule (arc-length spacing), the border's
  kinks and corners included, points restricted to where both sides have data;
  path to the points file; one grid refinement showing stability;
- bandwidths (pointwise `mserd` or integrated `imserd`), kernel, VCE / cluster
  level, `fitmethod` (joint by default), whether paper controls/FE enter the
  boundary fit — and if they do, the fit without them beside it;
- **WBATE**: weights (density-type, proportional to observations near each
  grid point, as the comparison for the paper's pooled estimate — the pooled
  limit is density-weighted for the local difference in means and the
  treatment-interacted specifications, not necessarily for a common-coefficient
  regression with segment fixed effects; equal weights as a second average), conventional and RBC estimates, RBC SE/p and CI; path
  to the `summary()` artifact;
- **BATEC**: point estimate, SE and pointwise interval at each point, **plus**
  a uniform confidence band. Empty bands leave the check BLOCKED with command
  proof, and the stage INTERIM while an untried repair remains;
- **LBATE** (optional unless a largest-effect claim is made): estimate and CI;
- treated and control effective sample sizes and minimum distances at each
  point; thin-support segments trimmed with the estimand relabelled;
- kinks: for distance-based estimates within a bandwidth of a kink or corner,
  the location-based refit and the kink-option refit;
- compound treatment: the other administrative borders overlaid, the segments
  where they coincide, and the response (restriction, placebo outcomes, or a
  relabelled compound estimand);
- covariate balance along the border: covariate BATEC with uniform band and
  covariate WBATE;
- whether coordinates are shared centroids (mass points);
- heterogeneity across boundary points, judged on the uniform band and
  reported *as* heterogeneity — never as a substitute for the WBATE;
- optional: interference — re-estimate after dropping units nearest the border
  on both sides where spillovers are plausible.

A pooled nearest-distance RD estimates a density-weighted average of the
boundary effect curve; it cannot show where along the border the effect or the
imbalance sits, and the pointwise curve alone leaves the paper's pooled claim
with no aggregate to answer it. Report both (leading with the WBATE is this
battery's convention). Manifest row for the boundary check may be `done` only
if a WBATE row exists in the results CSV / report. Where the design is
genuinely one-dimensional, mark this record `NOT_APPLICABLE`.

## Regression-kink record

Trigger: identification from a change in the slope of a policy rule in an
assignment variable, or any `deriv = 1` estimate or ratio of slope changes.
Record:

- the policy rule reconstructed from the statute, the slope change used as the
  denominator, whether the rule's level also jumps at the kink, and (fuzzy)
  the share of observations exactly on the schedule;
- density and covariate tests for both a jump and a slope change at the kink;
  any visible bunching;
- the order × selector grid (p = 1 and p = 2; default, unregularised and, for
  fuzzy kinks, ratio-targeted selectors), each cell with the conventional
  estimate and RBC interval, and the first stage likewise for fuzzy kinks;
- the placebo-kink test: support, number of placebo kinks (≥ 100), placebos
  dropped because their window contains a real kink, the share significant
  under the paper's own inference, and the two-sided permutation p-value;
- the scale applied to `deriv = 1` output, and `p` set explicitly;
- for a load-bearing null, the detection rate of a meaningful kink from the
  placebo distribution.

## RD extrapolation record

Trigger: a claim about the RD effect for units away from the cutoff. Record:

- the claim, quoted, and the population it names;
- the extrapolation assumption the paper states (or "none stated");
- for the multi-cutoff constant-bias method: the target group and score range
  between cutoffs, the direction of extrapolation, both falsification tests
  with their power, whether cutoff groups differ by period or place, and RBC
  inference including the covariance between the high-cutoff fits;
- the verdict: estimated, assumed (unsupported), or outside the method's reach
  (beyond the highest or below the lowest cutoff, or a population never exposed
  to a cutoff).

## OVB-sensitivity record

Trigger: a causal claim resting on selection-on-observables (a control set) or
on IV exogeneity/exclusion. Record:

- the estimator the sensitivity is computed on (OLS with the paper's controls;
  the IV / Anderson–Rubin fit for an instrument), the treatment or instrument
  coefficient, its standard error, and residual degrees of freedom;
- the robustness value at the relevant threshold, and the extreme robustness
  value where an unobserved confounder is allowed to explain all residual
  outcome variation;
- the partial R² of the treatment (or instrument) with the outcome (this is
  Cinelli–Hazlett sensitivity input — it is NOT the variance-explained
  dimension above, and must not be copied into that cell);
- benchmark bounds against named observed covariates — the multiple of a named
  covariate's strength a confounder would need to overturn the claim;
- for IV, whether the sensitivity is to violations of instrument exogeneity or
  exclusion, stated explicitly.

A robustness value near what a single named observed covariate already explains
is a different finding from one no plausible confounder could reach; report
which. A robustness value is NOT a verdict — it quantifies how much unobserved
confounding the claim can absorb, not whether such confounding exists. Report it
beside its benchmark, never as a bare number. Source-audited cribs:
`methods/cinelli_hazlett_2020_sensitivity.md` (RV formulas,
extreme-scenario bounds, benchmarking) and
`methods/oster_2013_unobservable_selection.md` (the δ/Rmax
coefficient-stability parametrization — WP rule Rmax = min(2.2·R̃, 1); the
published JBES 2019 version's convention is 1.3·R̃).

## Time-series synthesis record

Trigger: `time-series-diagnostics` fired. Do not count test statistics as
independent votes when they reuse the same residuals or impose the same
assumptions. Organise the verdict around distinct identifying information:

| Evidence class | Question it answers |
|---|---|
| Opposite-null unit-root tests (ADF/PP vs KPSS, + Zivot–Andrews) | Is each series stationary, integrated, or unresolved? |
| Residual + system + reversed-null + break cointegration tests | Is any stable long-run combination supported? |
| R² beside Durbin–Watson | Does the levels fit show the Granger–Newbold fingerprint? |
| Prais–Winsten and first differences | Does the coefficient survive removal of persistence? |
| ARDL/ECM bounds test | Is a levels relation supported without an exact I(0)/I(1) call? |
| Holdout + noise placebos | Does it work beyond its own data; can matched noise reproduce it? |
| Calibrated Monte Carlo | Which rejections/non-rejections are informative at this T? |

A defensible finding of a long-run relationship rests on these converging:
stationary residuals or positive cointegration evidence, a bounds F above its
upper ($I(1)$) bound and the bounds t on the lagged-level coefficient more
negative than its upper ($I(1)$) bound ($t < t_U < 0$; PSS 2001; t-bounds in Cases I, III, V only),
stable corrected estimates, and acceptable holdout performance.
An element without power at this T (per the Monte Carlo) limits the finding
rather than defeating it, provided at least one powered element supports it; the
holdout is never waived. When these disagree,
report the disagreement — a high in-sample R² never resolves it, and a single
non-rejection never carries the conclusion. Record the integration order of every
load-bearing series explicitly; a `time-series-diagnostics-REPORT.md` that reaches
COMPLETE without one is a critical failure (see the module's GATE).

