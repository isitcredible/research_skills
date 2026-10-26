---
name: time-series-diagnostics
description: >-
  Diagnostics for regressions on trending or highly persistent time series:
  unit-root order (opposite-null), cointegration (residual, system, reversed-null,
  break-robust), the Granger–Newbold R²-vs-Durbin–Watson fingerprint, Prais–Winsten
  and first-difference coefficient survival, an order-agnostic ARDL/ECM bounds test,
  out-of-sample validation, and calibrated size/power. Invoke from `code-and-data`
  whenever a headline or mechanism result regresses one time-indexed level on another.
---

# Time-series diagnostics

A levels regression of one trending or highly persistent series on another can
produce a large, precise coefficient, a high R², and conventional significance
even when the series are unrelated. Independent persistent processes drift
together for long stretches; OLS mistakes the common drift for a relationship
and the residual stays near a unit root (Granger–Newbold 1974; Phillips 1986).
A deterministic trend does not remove a stochastic one, and a near-perfect
in-sample fit is a *product* of a spurious regression, not evidence against it.
Drift does not rescue it either: two I(1) series WITH drift produce a nonsense
regression in which OLS converges to the *ratio of the drifts* (Entorf 1997) —
a stable coefficient equal to the trend ratio is the *mechanism* of the
spuriousness, not an escape from it, and a stable γ across subsamples does
not discriminate — a cointegrated relation is stable too. The levels-residual
Durbin–Watson is a screen, not a discriminator: it goes to 0 under
spuriousness asymptotically, but at short T a slowly adjusting cointegrated
relation also leaves a low DW — cointegration tests with correct critical
values decide; a first-difference R² near zero is
consistent with spuriousness, not proof of it; high levels R²
and a huge t are produced ~always by unrelated series and discriminate
nothing.

Your job is to establish whether the reported levels relationship is a genuine
long-run equilibrium (the series are cointegrated) or an artefact of shared
persistence — and to reach that verdict from **convergence across tests with
different identifying information**, never from a single unit-root classification.

## Trigger

Fire this module when any target result family regresses **time-series levels on
time-series levels** and the series trend or are highly persistent — aggregate
GDP, prices, wages, skill premia, money, population, national ratios, indices,
market-integration price gaps, or any structural/calibrated model fitted to
trending aggregates over time. It fires **alongside** other modules: a dynamic
panel of GDP over time is both `panel-diagnostics` (cross-unit dependence) and
this module (within-unit persistence); a market-access design with a price
series over time is both `cross-sectional-diagnostics` and this.

Do NOT fire it for a pure spatial cross-section, a geographic RDD, or a
DiD/event study with no aggregate time-series relationship in levels — those
carry a *spatial* dependence problem, handled by the spatial implementation
record, not this one. The two spurious-regression problems are analogues but
distinct: Müller–Watson's spatial tests (the Becker–Boll–Voth SPUR port, and
SCPC) are the **spatial** battery, never a substitute for the temporal one here.

The full source-audited protocol this module compresses is
`../../references/methods/spurious_regressions_guide.md`; the space–time
correspondence and the spatial analogues are in
`../../references/methods/spurious_space_time_unified_guide.md`.

## Decision rule

Treat the levels regression as **unvalidated** until the integration order of the
outcome, each stochastic regressor, and the regression residual has been
established, and the cointegration question answered. If outcome and regressor(s)
are I(1), the levels coefficient has a coherent long-run reading **only if** the
residual is I(0) — i.e. they are cointegrated. Cointegration is the escape hatch;
without it the right model is normally in differences and the levels *t*, SE, and
R² do not mean what they appear to.

**No conclusion may rest on a unit-root or cointegration test failing to reject
its null.** These tests have low power at the sample lengths economic history
supplies. Non-rejection of a unit root is not proof of one; non-rejection of
no-cointegration is not proof of no long-run relation. The strongest diagnosis
does not depend on any single I(0)/I(1) call.

## Core checks

Preserve the paper's exact sample, transforms, deterministic terms, break dates,
and lag conventions before touching anything. Plot every series and the levels
residual. **Record irregular spacing and missing years** — annual unit-root
methods require a genuinely consecutive series, not benchmark observations
treated as adjacent (a common economic-history failure).

1. **Integration order — opposite nulls.** ADF and Phillips–Perron (H0: unit
   root) *and* KPSS (H0: stationarity), on each series in levels and first
   differences, with deterministic terms matched to the claim (constant vs
   constant+trend) — then run the *other* deterministic case as a
   sensitivity: a classification that flips on constant vs constant+trend is
   not established either way and is reported as such. I(1) requires the
   level nonstationary AND the first
   difference stationary — test the difference too, to rule out I(2). Add
   Zivot–Andrews (one endogenous break) to answer the "it's stationary around a
   break" objection; report the selected date and use break-valid critical
   values. Classify the *evidence*, not the series: convergent only when ADF/PP
   fail to reject while KPSS rejects (or vice versa); if both fail to reject, the
   sample is uninformative — say so and lean on the order-agnostic tests below;
   and if both REJECT (no unit root AND no stationarity — the signature of
   breaks, nonlinearity, or fractional integration), the evidence is likewise
   unresolved: investigate breaks/nonlinearity/fractional integration rather
   than choosing a side.

2. **Cointegration — several tests, at least one reversed-null.** Engle–Granger
   and Phillips–Ouliaris residual tests (H0: no cointegration) with **MacKinnon /
   Phillips–Ouliaris response-surface critical values matched to the number of
   stochastic regressors and deterministic case — never ordinary ADF/KPSS
   tables** (in R, `summary(urca::ur.df(e, ...))` and `urca::punitroot` print
   raw unit-root critical values with `niv = 1`, which severely over-reject on
   fitted residuals; evaluate `adf_eg@teststat[1]` against
   `urca:::.urcval(arg = adf_eg@teststat[1], nobs = length(e), niv = m, itt = 1,
   itv = 2, nc = 2)` for the MacKinnon $p$-value or `nc = 1` with
   `arg = c(0.01, 0.05, 0.10)` for critical values, where `m` = outcome +
   stochastic regressors and `itv` = 1/2/3 for none/const/trend, as in
   `../../references/software-examples.md`; `check_inference.py` warns on
   `ur.df()` in cointegration scripts without `.urcval`). Johansen trace for
   system rank (report VAR order, deterministic case, rank). Shin (H0:
   cointegration) on Stock–Watson DOLS residuals with Shin's own critical
   values — a rejection is affirmative no-cointegration evidence only once
   weighed against the size Monte Carlo at the data's own residual ρ̂ (Shin is
   undersized at short T with weak persistence, oversized at high residual
   persistence; step 7). Gregory–Hansen / Maki for a break in the
   cointegrating relation. Agreement across differently-identified tests is the
   evidence; any single one is not.

3. **Granger–Newbold fingerprint.** For every levels spec, report R² beside the
   Durbin–Watson statistic. R² > DW is the classic fingerprint (high fit, near-
   unit-root residual). A screening rule, not a proof — follow with residual
   ACF and the cointegration tests.

4. **Coefficient survival.** Iterative Prais–Winsten (report ρ̂, and the
   coefficient/SE/sign/significance and DW before and after); a ρ̂ near one should
   pull the estimate toward the first-difference result. Report the coefficient
   and interval along the ρ grid (0 → 1), not only the fitted-ρ̂ endpoints — a
   before/after read can hide a non-monotone path and suppresses persistence
   uncertainty; where the maintained AR(1) is defensible, add the profile-union
   protected interval per the unified guide's Stage 4. Then the first-
   difference regression with Newey–West HAC SEs and declared dynamics. A large,
   precise levels coefficient that goes small and imprecise in differences while
   ρ̂→1 is strong evidence the levels result was persistence, not relationship.
   Where a long-run levels coefficient is read off OLS on I(1)/persistent
   regressors — whatever SEs are printed — that long-run inference is invalid:
   recompute with FM-OLS and DOLS (`cointReg::cointRegFM` / `cointRegD`). HAC
   SEs do not rehabilitate it under regressor endogeneity in a cointegrated
   system (for stationary-but-persistent regressors HAC is the fix and FM/DOLS
   is not required — condition on the diagnosed order); White SEs on
   persistent series can understate the long-run severalfold.
   And at high residual persistence BOTH test directions can fail together —
   the no-cointegration test underpowered AND the reversed-null test oversized —
   leaving the battery genuinely UNDETERMINED: report power AND size at the
   data's own estimated residual ρ, and rest the critique on what holds either
   way (e.g. invalid inference) rather than fighting for a "spurious" label.

5. **Order-agnostic bounds.** The Pesaran–Shin–Smith ARDL/ECM bounds test on the
   joint null of no levels relationship. Valid under a *mixture* of I(0)/I(1)
   regressors (not I(2) — hence the difference tests in step 1), so a clean I(0)/I(1) classification is not required. Count in k every regressor in the tested levels relationship, including I(0) regressors; exclude the lagged dependent variable and deterministic terms. Match the critical-value case to the deterministics. An F below the lower bound fails to reject no levels relationship; an F between the bounds is inconclusive. Neither proves absence. Supporting a levels relationship needs the F above its upper ($I(1)$) bound AND the bounds t-test on the lagged-level dependent coefficient more negative than its upper ($I(1)$) bound ($t < t_U < 0$; PSS 2001, §3; the t-bounds exist for Cases I, III and V only — in Cases II and IV the F-bounds test alone applies).

6. **Out-of-sample.** Freeze the full spec on a training window, project into a
   held-out forecast/backcast window (do not re-estimate). Report holdout RMSE
   and R²_OOS against a **pre-declared benchmark** — and for persistent series
   the benchmark must include a random walk / last observation, not only the
   holdout mean: beating the mean is nearly free under drift, and a levels fit
   that beats the mean but loses to a random walk has reproduced drift, not a
   relation (a Clark–West / Diebold–Mariano comparison is the formal version).
   A stable relation keeps sign, scale, and predictive content; a
   spurious fit diverges once the training interval ends. This needs no unit-root
   classification and so is immune to the low-power objection. Where feasible add
   **persistence-matched noise-regressor placebos**: how often does a series with
   the same length, missingness, drift, volatility, and persistence — but no
   relation — reproduce the published coefficient/*t*/R²?

7. **Calibrated size and power (short samples especially).** Do NOT cite a
   non-rejection as evidence without a Monte Carlo, calibrated to the observed
   sample, showing the test had power against the alternatives that matter. At
   T ≲ 40 this is decisive and non-optional:
   - H0=no-cointegration tests (Engle–Granger, Phillips–Ouliaris) can have near-
     zero power at short T — an underpowered non-rejection is **no evidence**, not
     weak evidence. Run the calibrated power MC before citing one.
   - Shin (H0=cointegration) is not uniformly conservative: undersized at short
     T with weak persistence, oversized at high residual persistence (step 4) —
     weigh a rejection only against the size MC at the data's own ρ̂.
   - Engle–Granger *without* trend is oversized on drifting series (common drift
     masquerades as equilibrium): use trend deterministics and recompute the CVs
     for the actual T.
   - **Account for fitting and selection.** Minimizing in-sample residuals does not make them stationary. Residual-based cointegration tests are legitimate when their critical values account for the fitted relationship. For SCM or other selected/trained models, establish that the reference distribution covers the fitting and selection procedure, or calibrate the entire procedure under the null. A routine ADF on selected fit residuals is not independent validation; report held-out performance too.

   - Johansen trace is erratic at short T (completeness entry, not a load-bearing
     verdict). For panel I(1) under cross-sectional dependence, first-generation
     panel tests (IPS/MW/Hadri) are invalid — all p≈0 while mutually
     contradicting is the CSD signature; use Pesaran CIPS.

Software (R `urca`/`tseries`/`dynlm`/`ARDL`/`urca::ca.jo`; Stata
`dfuller`/`pperron`/`kpss`/`dfgls`/`zandrews`/`vecrank`/`vec`/`ardl`/`egranger`):
see `../../references/software-examples.md`, "Time-series unit-root and cointegration
battery". Definitions and the reporting record: `../../references/design-matrix.md`,
"Time-series and trending-levels designs".

## Report back

Lead with what the battery found and what it costs the claim — is the levels
relationship a cointegrated equilibrium or a shared-persistence artefact? — not a
row per test. Organise the evidence by identifying information, never as
independent votes when tests reuse the same residuals (the synthesis table in the
design-matrix record). Account for coverage: what ran, what was `NOT_APPLICABLE`
and why, what was `BLOCKED` (exact file, command, error). Every reported statistic
traces to a saved script + log in the job tree. Hand `claims` the verdict on
whether the paper is entitled to its long-run / levels language, and the OOS and
noise-placebo results — a story told about a stable long-run relationship that
lives only in-sample is a framing gap.

## GATE

A COMPLETE status on a time-series-exposed family is a **critical failure** if the
integration-order record is missing. Concretely, before this module's row clears:
the outcome and each stochastic regressor have an opposite-null integration-order
call (ADF/PP **and** KPSS); unless every series is established I(0), at least one residual/system
cointegration test **and** one reversed-null (Shin) or order-agnostic (ARDL
bounds) test have been run with correct (not ordinary-ADF) critical values; R²
sits beside DW for every levels spec; and the coefficient's survival under Prais–
Winsten and differencing is reported. A non-rejection cited as evidence without
a calibrated power check does not clear the gate — at any T; at T ≲ 40 the MC
is required regardless of what is claimed. Inspect each required record for the named series/specification, actual statistic, reference distribution, assumptions, interpretation, and a script/log containing the result. A keyword match or a report file alone is not completion. Missing any required record leaves the family **INTERIM, not COMPLETE** — say

which piece is absent.
