---
name: shift-share-diagnostics
description: >-
  Diagnostics for shift-share and exposure-weighted designs, including
  designs the paper does not label shift-share: Rotemberg-weight
  concentration, effective number of shocks, decomposition identity,
  placebo-shock rejection, and shock-level inference. Invoke from
  `code-and-data` whenever any regressor or instrument is an
  exposure-weighted sum of shocks.
---

# Shift-share diagnostics

Answer the shock-level question with shock-level tools. The trigger is
structural, not nominal: ANY regressor or instrument built as an
exposure-weighted sum of shocks is a latent shift-share design, whether or
not the paper uses the words — and a paper can pass every unit-exclusion
and clustering check while its identification rests on two shocks, which
only the shock-level diagnostics can reveal.

`NOT_APPLICABLE` when no target regressor has the exposure-weighted-sum
structure — record that the structure was checked for, since the unlabelled
case is the one that escapes.

The source-audited cribs behind this module:
`../../references/methods/shift_share/gpss_2020_bartik_instrument.md`
(Rotemberg weights, the decomposition identity, shares-vs-shocks framing),
`../../references/methods/shift_share/bhj_2022_quasi_experimental_ssiv.md` (shock
exogeneity, incomplete shares, the Col 1→2→3 walk),
`../../references/methods/shift_share/akm_2019_shift_share_inference.md` (AKM/AKM0
shock-level inference and its validity conditions), and
`../../references/methods/shift_share/borusyak_hull_2020_nonrandom_exposure.md`
(non-random exposure and recentering).
The textbook-level overview of the whole program is Borusyak, Hull &
Jaravel (2025), "A Practical Guide to Shift-Share Instruments," *Journal
of Economic Perspectives* 39(1): 181–204; cribbed at
`../../references/methods/shift_share/bhj_2025_practical_guide.md` —
its two checklist columns (shifts margin / shares margin) supply the
tailored-shares, share-vintage, and combination-sensitivity checks
below.

## Core checks

- **Rotemberg-weight concentration**, computed on the exact estimation
  sample — not the full dataset, and not the sample of a different column.
  Which shocks carry the estimate, and how concentrated are the weights?
- **Effective number of shocks.** The inverse Herfindahl of the shocks'
  average exposure weights, 1/Σ_k s̄_k² (BHJ 2022 Table 1; BHJ 2025) —
  not of the Rotemberg weights: an estimate with thousands of nominal
  shocks and an effective number under ten is identified off a handful
  of comparisons.
- **Decomposition identity verified on the estimation file.** Confirm the
  weighted combination of just-identified estimates reproduces the reported
  coefficient; a failure means the sample, weights, or specification differ
  from what the decomposition assumes.
- **Adjudicate the identifying margin — and route the verdict through it.**
  What varies across units, what varies across shocks: then state, with the
  reason, which margin the design's strongest defense claims as exogenous —
  the shares (the exposure geography or settlement pattern, the
  Goldsmith-Pinkham / Card reading) or the shocks (the aggregate shifters,
  the BHJ reading). This is a judgment the report must defend, not a
  default: an enclave/origin-share instrument is defended on shares, a
  lottery-style shifter on shocks. The margin decides which tests are
  verdict-bearing. Share exogeneity is falsified by share-level evidence —
  location-level balance, and negative controls / pre-trends of the outcome
  on the exposure geography (an instrument that predicts the pre-period
  outcome fails share exogeneity directly). The shock margin fails on
  shock-level balance (exogeneity) or on few effective shocks (the
  many-shocks law of large numbers); concentration does not falsify
  exogeneity, it breaks the many-shocks condition — and shock-level SEs are
  themselves unreliable when the effective number of shocks is small, so
  report it as a limit. Results on the *other* margin rebut only what the paper itself
  claims — run them when the paper claims them (a shock-level placebo is a
  shock-level claim on the paper), but label them rebuttals, never "the
  diagnostic this design calls for". When the margin is genuinely arguable
  the headline must not silently rest on one choice; when both margins
  fail, say so in both directions — "the shares are not exogenous AND the
  shocks are few and concentrated" is strictly stronger than a verdict that
  routes through one contested margin.
- **Construction algebra before test selection.** Derive the instrument's
  *residualised* form under the actual FE/control structure. After unit
  and period effects are partialled out, an exposure-weighted instrument
  often reduces to a mechanical function of observables (products or
  deviations of unit size and shock aggregates) whose loading on
  predetermineds is algebraic, not coincidence — a share built from
  predicted origins can be, after partialling, a unit-size measure
  times a shock deviation. Write the algebra down in the module report: it tells
  you which balance tests are actually binding and which the
  construction guarantees will fail.
- **Share vintage and tailoring (BHJ 2025).** Fixed-at-baseline and
  time-updated shares are different instruments answering different
  assumptions — updated shares can reimport the endogeneity the
  instrument exists to escape (shocks moving shares after the
  experiment starts). A lagged-share construction helps only if it cuts
  cov(share, ε) by more than it cuts cov(share, x); demand that
  argument, not the mere fact of lagging. On the shares margin, check
  tailoring: shares measuring general exposure to *many* shock types
  (industrial composition, generic pull factors) are a non-starter —
  share exogeneity needs shares tailored to the shocks that move this
  treatment.
- **Placebo-shock rejection: centring AND rejection rates.** Replace the shocks with
  permuted or irrelevant series pushed through the same exposure weights (≥ 1,000
  draws; permute within the class the shocks are exchangeable in, and report all
  shocks and the narrower class side by side). Report two things:
  - **Centring.** Placebo coefficients centred off zero mean the design detects
    exposure structure, not the shocks. Centred coefficients do not by themselves
    clear exposure bias; recentering (Borusyak–Hull) does.
  - **Rejection rates, in a section headed `Placebo-shock rejection rates`.** For
    every unit-level test the run cites anywhere (CV1, CV3, WCR-S, AR or Conley at
    the region or state level, and the paper's own), give the share of placebo draws
    it calls significant at nominal 5%. Also give the randomization p of the actual
    statistic, raw and studentized, and the share of extreme draws in which the
    top-weight shock lands on the top-weight industry.
  - **What the rates mean.** A unit-level test that rejects more than 10% of
    placebo draws is an inference failure (AKM/AKM0). Its p-values are not evidence
    for or against any claim in this run, however good its size looked in a
    simulation with independent clusters. Nominal state clustering is not a defence:
    units with the same shares are dependent across states. `../../scripts/check_inference.py`
    F4 fails a shift-share run without this section or without the randomization
    (permutation) p of the actual statistic inside it.
- **Shock-level balance and falsification** — under Borusyak–Hull–Jaravel
  the validity rests on *shock* exogeneity, so regress the shocks on
  shock-level confounders; a location-level balance table answers the
  Goldsmith-Pinkham shares question, a different design.
- **The Col 1 → 2 → 3 walk (BHJ Table 4) with exposure-robust,
  shock-clustered SEs.** Col 2 controls the correct sum of shares
  underlying the instrument (the incomplete-shares fix — usually harmless);
  Col 3 additionally controls the period-interacted share = within-period
  isolation, the consequential correction (it halved the coefficient in
  the canonical application). The
  cheap correction moving nothing says nothing about the expensive one —
  run the whole walk. First run the complete-shares check (shares' row-sum
  = 1): it decides whether the incomplete-shares correction applies at all.
- **Constant-shock placebo.** Set every shock to a constant: the instrument
  collapses to the pure share/exposure measure. If the result survives, the
  shocks were decorative and it is an exposure design — which must then
  clear *share*-exogeneity, usually where it fails. The tell: thin,
  concentrated, or noisy shocks yet a strong, precise first stage means the
  share geography is carrying the identification.
- **Non-random exposure** — when shares are geographically clustered,
  Borusyak & Hull (2023) recentering is the tool: the expected instrument
  μ is the average instrument over permuted or counterfactual shocks
  pushed through the fixed shares. Audit whether the permutation class
  matches the shock assignment process (all permutations only for
  exchangeable shocks; within-cluster or matched-group otherwise).

## Conditional checks

- **Shock-level (AKM0-style) inference** — when shocks are few or the
  weights concentrated: unit-level clustering understates uncertainty when
  the effective shocks are scarce. Predicted or estimated shares are signed
  and break `ssaggregate` (r(402), negative weights) — fall back to the
  null-imposed score aggregation (signed-share-safe) or a manual
  share-weighted shock collapse restricted to positive-weight cells.
- **Null-imposed shock-level score test** — alongside, when the shock-level
  asymptotics are themselves doubtful.
- **Shock-level jackknife (CV3) and G\*** — when the effective number of
  shocks is small or one shock dominates. These are the shocks-as-clusters
  version of the few-clusters check in the small-n module.
  - *Estimate.* Write the regression in its shock-level form (BHJ 2022
    Prop. 1): partial the controls at the unit level, then aggregate
    outcome and treatment to shocks with the average exposure weights.
    Include a shock-level intercept and the exposure-sum control, then
    confirm that this reproduces the unit-level coefficient.
  - *Report CV3 twice:*
    - delete one shock at a time;
    - delete one shock cluster at a time (broad sector, or whatever level
      the shocks co-move at).

    **How a shock is deleted.** Delete shock k by adding its share S_k (for
    a cluster, every member's share; in stacked designs, in every period)
    as a unit-level control and re-fitting the whole estimator: every
    control, the intercept and the first stage. This is CV3's
    re-fit-everything rule (MNW 2023 eq. 15). It is also the companion
    unit-level control that BHJ 2022 Prop. 5 requires for a shock-level
    deletion; row deletion in the shock-level form with S_k added to the
    unit controls is the same estimator. Do NOT drop the shock's row from a
    shock-level regression whose controls were partialled once on the full
    sample. That leaves the deleted shift in the leave-out denominator
    through the other rows, and when one shock is large the jackknife is
    wrong in either direction. In the Robots review it inflated a pretrend
    SE sixfold (1.53 against .253) and moved p-values across .05 both ways
    (stacked employment .0009 against .085; an IV .0045 against .94). The
    many-small-shocks asymptotics that license row deletion do not cover a
    dominant shock. **Validation, required:** the leave-top-shock-out
    estimate must equal the unit-level regression with that shock's share
    controlled; assert it before reporting any jackknife.
    Use t with K−2 (shocks) or G−1 (clusters) degrees of freedom.
  - *Report G\*.* Compute it from the partial leverages of the demeaned
    shocks, at both levels, with the top-leverage shocks named.
  - *Cross-check and contrast.* The shock-level CV1 should match the AKM
    standard error. The unit-level HC1/HC3 numbers are a contrast only.
  - *Validity.* A specification without the exposure-sum control is not
    valid at the shock level when shares are incomplete. Report it at the
    unit level only, never as a jackknife row.
  - *Reading.* The jackknife emits a variance, which AKM0 and randomization
    do not. Report it beside them; it is not a replacement
    (`../../scripts/check_inference.py` F12 fails a shift-share report without
    a shock-level jackknife row or `Shock-level jackknife: not applicable —
    <reason>`). A CV1→CV3 gap is itself the leverage finding (see
    `../../references/methods/mackinnon_nielsen_webb_2023_few_clusters.md`
    and `../../references/methods/hansen_2026_jackknife_se.md`).
- **Unit-exclusion robustness** — run it, but NEVER report it as the answer
  to shock concentration. Dropping units one at a time cannot discover that
  the shocks are few; a "drop the top-exposure regions" check leaves the
  concentrated shock spread across every unit's share untouched. The
  shock-level leave-out is a different operation: drop shock $k$, control the
  deleted shock's share $S_k$ (equivalently $S_{-k} = S - S_k$ when $S$ is in
  the regression), and re-estimate the unit-level IV in each leave-out step.
- **Read a capped |t| as uninformative, not as zero.** With one dominant
  shock the self-normalised null-imposed score is capped near |t|≈1, so the
  test cannot reject and the accepted set spans the grid. Report "the design
  is uninformative at shock level" — never "the effect is zero." When
  permutation and studentized versions diverge, the permutation p on |β|
  (not |t|) is the honest corroboration.
- **Audit the authors' own alternative-SE roster, not its label.** A table
  of "robust SEs" often omits the null-imposed members: a "BHJ" row that is
  only baseline exposure-robust, "AKM" rows with no AKM0. Fast tell without
  the code: a symmetric Wald CI (point ± 1.96×SE matching the printed
  interval) cannot be a test-inversion set. And an `se=Inf` with reversed CI
  endpoints is an unbounded *complement* set — never relay it as "zero
  excluded." "The authors already ran BHJ/AKM" does not close the inference
  question; the omitted null-imposed members can also *strengthen* the
  authors' case — do not pre-frame the battery as a kill.
- **Anti-dose-response tell.** If extending the sample through years of
  *faster* treatment growth shrinks the per-unit coefficient, the estimate
  behaves like a fixed event divided by a growing denominator — check
  window-extension attenuation.
- **Placebo/simulation fidelity audit — when the paper runs its own
  placebos.** Verify the placebo DGP matches the actual shock structure:
  same level of shock aggregation (origin vs origin×region), same
  instrument construction off the draws, same fixed-share geography. A
  placebo drawn at a coarser shock level than the design uses tests a
  different, easier-to-pass design; decompose the placebo draws'
  variance share by level to show which component the authors' placebos
  actually exercised. A favorable placebo rejection rate on a
  mis-specified placebo DGP is evidence about the placebo, not the
  design.
- **Non-common shocks → index at the variation level, cluster at the
  shared component.** When shocks vary at origin×destination×period but
  share an origin component, the shock index is the fine level and the
  clustering level is the coarse one — and the effective-shock count is
  computed on the shares that carry the weights, not on nominal shock
  cells. A "thousands of shocks" claim where one origin contributes
  ~all of instrument variance is the same disease as one dominant
  cluster (see `../../references/methods/mackinnon_nielsen_webb_2023_few_clusters.md`).
- **Shares-margin combination sensitivity (BHJ 2025).** When the margin
  adjudication lands on shares, the design pools many share instruments
  and the pooling is the author's choice: run the Sargan–Hansen overID
  on the individual share instruments; the visual-IV reduced-form vs
  first-stage ray plot; per-share β̂_k against first-stage F on the
  high-Rotemberg shares; and, when the share count is large, a
  many-weak-IV-robust estimator (JIVE, LIML, heteroskedasticity-robust
  Fuller, MBTSLS). Under homogeneous effects a failure means share
  exogeneity fails; under heterogeneous effects it may be an
  interpretation problem (correlated share instruments do not generally
  yield a complier average — Mogstad–Torgovitsky–Walters). Say which
  reading applies.
- **Renormalised "share form" is a different instrument.** When the
  paper offers a nonnegative share-form renormalisation of signed or
  estimated shares (shift the min, divide by the total), run the
  diagnostics on it separately — a placebo that passes on the share form
  does not cover the estimated-share baseline, and vice versa.

## Report back

Lead with what each check found and what it costs the claim, not a row for
every check. Still account for coverage: say what you ran, what was
`NOT_APPLICABLE` and why, and what was blocked (exact file, command, error). Record the which-shocks-carry-it answer in the module report's `## Leads for later stages` (folded into the `code-and-data` report) for `claims`: a story about broad
structural change identified off two shocks is a different, narrower claim,
and naming the shocks that carry it is story evidence of the first order.
The margin adjudication goes in the module report and `## Leads for later stages` too — which margin
was claimed, why, and which reported results are verdict-bearing versus
rebuttals — so `claims` does not quote a rebuttal-stage number as the
design's required test.
