# Spurious Regressions in Space and Time: A Comparative Diagnostic Protocol

**Version 0.1, 22 July 2026.** This is a source-audited working guide, not a
claim that one automatic procedure has been validated for every temporal or
spatial design.

## Bottom line

Time and space share the same danger: two persistent objects can line up even
when their innovations or generating mechanisms are unrelated. Ordinary
levels regression can then mistake a shared low-frequency realization for
stable covariation. A large coefficient, conventional significance, and high
in-sample fit can all be products of persistence.

The mature time-series response has four distinct parts: diagnose integration,
test whether a stationary cointegrating relation licenses levels, ask whether
the coefficient survives quasi-differencing, and use dynamics, holdouts, and
calibrated power to decide what the data can distinguish. Space now has direct
analogues of the first three parts, but not the same breadth of tests or
finite-sample evidence.

The central comparison is therefore:

> **Time has a mature, varied cointegration apparatus; space has a direct but
> much newer, narrower, and less well-powered analogue.**

Müller and Watson (2024) explicitly provide both a confidence-set construction
for a spatial cointegrating vector and a residual-based spatial analogue of
the Engle--Granger test. Spatial cointegration is not an empty metaphor. What
space lacks is the temporal menu of system, reversed-null, break-robust, and
mixed-I(0)/I(1) procedures, together with a large body of comparative evidence.

Nor is there a universal spatial equivalent of the ARDL bounds test. “Always
transform” is a useful sensitivity strategy on tested smooth covariance
families, not a generally valid escape from classification. Both the new
temporal and spatial profile batteries fail when many observations are really
only a few common regimes.

## What kind of warrant supports each claim?

The guide keeps four kinds of evidence separate:

- **[L] Literature:** a published theoretical or methodological result.
- **[A] Application:** a number reproduced or checked against an application
  script and its finished output.
- **[MC-T] Temporal battery:** a frozen 4,800-run, `T=61` battery plus a
  5,000-repetition targeted six-regime run (receipts not distributed with
  the skill).
- **[MC-S] Spatial battery:** the b--h spatial Monte Carlos summarized in
  the spatial-application guide and its companion pilot battery, including a
  targeted 2,000-repetition G325 heavy-tail run.

An operating characteristic in one battery is not a theorem about another
design. A method can fail a simulated class without proving that a particular
published coefficient is false. Conversely, a coefficient can survive one
repair without being certified as causal.

## The correspondence

| Role | Time | Space |
|---|---|---|
| Persistent object | Unit-root or local-to-unit series | Spatial-unit-root or strongly persistent field |
| Spurious-regression result | Independent I(1) series can yield nonstandard OLS coefficients, fit, and tests [L] | Independent spatial I(1) fields can do the same [L] |
| Variable diagnostics | ADF/PP versus KPSS; break tests | Müller--Watson LFUR/LFST I(1)/I(0) tests |
| Levels escape hatch | Temporal cointegration | Spatial cointegration: LFUR residual test and LFST inversion [L] |
| Descriptive fingerprint | High $R^2$, low Durbin--Watson | High fit with persistent residual map; Moran's I is descriptive |
| Continuous correction path | Prais--Winsten: $\rho=0$ levels, $\rho\to1$ differences | Half-life GLS: $h\to0$ levels, $h\to\infty$ LBM-GLS |
| Weak-dependence inference | HAC after a valid stationary transformation | SCPC or other spatial HAR after a valid transformation |
| Mixed-I(0)/I(1) long-run test | ARDL/ECM bounds, excluding I(2) | No comparably broad validated analogue |
| Independent challenge | Frozen forecast/backcast; persistence-matched noise | Matched spatial placebo; regional estimates; documented assignment-law test |
| Shared hard case | Few breaks or common time regimes masquerading as many dates | Few regions or common blocks masquerading as many places |

Standard-error correction and coefficient correction are not the same thing.
Newey--West, Conley, clustering, and SCPC change uncertainty estimates under
their respective conditions. Prais--Winsten, first differences, and LBM-GLS
change the estimating equation. When persistence creates the apparent
coefficient, a standard-error correction alone need not cure the problem.

## The protocol at a glance

| Stage | Question | Required output |
|---|---|---|
| 0 | What is the estimand, sample, ordering or geometry, and effective information count? | Frozen analysis record and runnability status |
| 1 | Which outcomes, regressors, and residuals are persistent? | Opposite-null diagnostic table; no binary verdict from non-rejection |
| 2 | Does a stationary linear combination license the levels relation? | Cointegration evidence, its power, and the supported scope |
| 3 | Does the levels fit have the classic descriptive fingerprint? | Fit and residual-persistence statistics and plots |
| 4 | Does the coefficient survive a continuous persistence correction? | Full coefficient path, point row, persistence set, and protected interval |
| 5 | Does the maintained covariance family fit well enough to use that interval? | Adequacy record and, where possible, an off-family fallback |
| 6 | Do mixed-order or external challenges agree? | Bounds/holdout/placebo/regional/design-based results as applicable |
| 7 | Were decisive non-rejections capable of rejecting? | Data-calibrated size and power |
| 8 | What exactly can be concluded? | Five separate reporting outputs, never one omnibus verdict |

## Stage 0: freeze the analysis and count information honestly

Before looking at a repair, record:

1. the exact outcome, focal coefficient, controls, deterministic terms,
   complete-case rule, and units;
2. the time ordering and spacing, or the coordinate system and distance rule;
3. the identifying and exogeneity assumptions needed to interpret the focal
   coefficient;
4. the hypothesized direction and a minimum substantively important effect
   $\delta$, justified independently of the repaired estimate;
5. all known breaks, regimes, borders, sampling clusters, and treatment-
   assignment units; and
6. the published coefficient, standard error, inference rule, and software
   settings to be reproduced before any alternative is run.

The number of rows is not necessarily the information count. Sixty-one annual
observations generated by six common regimes are closer to six independent
pieces of variation than to sixty-one. The spatial equivalent is hundreds of
towns whose treatment and disturbance both vary mainly across a dozen regions.
This is pseudoreplication, not merely “high autocorrelation.” [MC-T, MC-S]

Assign one runnability status:

- **within calibrated range**: no known feature puts the application outside
  the procedure's tested or theoretical scope;
- **calibration uncertain**: available evidence does not resolve scope; or
- **outside calibrated range**: a named feature, such as few regimes, strong
  anisotropy, or an unmodelled heavy-tail process, matches a known failure.

There is no validated universal numerical gate for this judgment. Inspect the
series or maps, residuals, data construction, and known grouping structure.
Do not turn a low-powered pre-test into a licence to proceed.

## Stage 1: diagnose persistence on one fixed sample

### Time

Run ADF and Phillips--Perron tests, whose null is a unit root, together with a
KPSS test whose null is level or trend stationarity. Test levels and first
differences. A defensible I(1) classification needs evidence that the level is
nonstationary and the first difference is stationary. Use deterministic terms
that match the claim and add a break-unit-root test, such as Zivot--Andrews,
when one break is plausible. Report lag or bandwidth selection, critical
values, and break dates. [L]

Interpret the evidence rather than forcing a label:

| Unit-root-null tests | Stationarity-null test | Reading |
|---|---|---|
| Reject | Do not reject | Evidence for stationarity under the stated deterministics |
| Do not reject | Reject | Convergent evidence for nonstationarity |
| Both reject or both fail to reject | Disagreement | Unresolved; investigate breaks, nonlinearities, fractional persistence, and tuning choices |

### Space

Run the Müller--Watson I(0) and I(1) tests on the outcome, focal regressor,
other spatially varying regressors, and provisional levels residuals, using
one complete-case sample and recorded coordinates. In the BBV Stata
implementation, record `q`, Monte Carlo draws, and seeds. A reported `p=.05`
is a non-rejection when the rule is `p<.05`. [L, MC-S]

The tested outcome-plus-regressor router treats a clean levels branch as:

- outcome: do not reject I(0) and reject I(1); and
- focal regressor: no I(1) stamp, where a stamp means reject I(0) and do not
  reject I(1).

All other cases trigger the persistent/uncertain branch in the existing
spatial guide. This is a routing rule, not proof that a field literally has a
unit root. It should not be interpreted substantively for a binary treatment:
the focal-regressor stamp fired in 50.0--72.5% of tested binary nulls. [MC-S]

Branch-specific nominal inference is not post-selection-valid merely because
each branch is valid in isolation. Every diagnostic, tuning choice, routing
decision, and fallback must be reproduced inside the end-to-end calibration
described in Stage 7.

Moran's I is useful description, not a branch selector. Its value depends on
the weight matrix, row standardization, islands, and permutation scheme.

## Stage 2: test the levels escape hatch

### Time: a mature battery

If the outcome and stochastic regressors are I(1), a proposed long-run levels
relation requires a stationary residual combination. Use complementary tests:

- Engle--Granger residual ADF with MacKinnon cointegration critical values;
- Phillips--Ouliaris residual tests;
- Johansen trace tests for system rank, with explicit lag and deterministic
  specifications;
- Shin's DOLS-residual test, which reverses the null to cointegration and uses
  Shin's critical values rather than ordinary KPSS values; and
- Gregory--Hansen or Maki tests when the cointegrating relation may break.

No one non-rejection establishes anything. At short $T$, simulate size and
power using the actual deterministic case, lag selection, and critical values.
The conclusion should state which alternatives the tests could distinguish.
[L] Positive cointegration evidence licenses a long-run levels parameter; it
does not license the original conventional OLS standard error. Estimate and
infer the long-run relation with a method whose endogeneity and serial-
correlation conditions fit the design, such as DOLS, FMOLS, a correctly
specified ECM, or the appropriate system estimator.

### Space: a direct but narrower analogue

Müller and Watson define a spatially cointegrated $p$-vector $x_l$ by the
existence of a vector $\beta_0$ for which $\beta_0'x_l$ is spatial I(0), while
other nonproportional combinations are spatial I(1). They give two practical
constructions in Remarks 4.1--4.2 (pp. 1675--1676). [L]

First, an asymptotic confidence set for $\beta_0$ collects the candidate
vectors $b$ for which the LFST stationarity test does not reject I(0) when
applied to $b'x_l$. This is the spatial analogue of inverting stationarity
tests for a temporal cointegrating vector.

Second, for $y_l=x_l'\beta+u_l$, form low-frequency residual projections that
are orthogonal to the realized design, $Z_X=R_X'Y=R_X'u$. Applying the LFUR
statistic to $Z_X$ gives an asymptotic test of the null of **no spatial
cointegration**, explicitly described by Müller and Watson as the spatial
analogue of the Engle--Granger residual test. Under the no-cointegration null,
the required asymptotic independence of $u$ and $X$ follows in their canonical
model.

This licenses a spatial cointegration branch in principle. It does not create
the following methods, which remain absent or immature:

- a comparably established spatial system-rank apparatus;
- a broad finite-sample record for residual LFST as the reversed-null
  cointegration diagnostic;
- general break- or border-robust spatial cointegration procedures;
- a spatial ARDL-style bounds test; or
- a well-powered automatic router proven to preserve cointegrated relations.

In one 200-repetition cointegration design, the MW residual test detected the
relation in 73% of repetitions, while an outcome-only flowchart sent 31.5% to
the differencing branch and another 26.5% to its indeterminate branch; the
strict residual I(0)-and-I(1) certification rate was 72%. [MC-S] That is
meaningful power, but far from a licence to equate non-rejection with no
cointegration. Pointwise exact 95% binomial intervals are `.663--.790`,
`.251--.384`, and `.652--.781`, respectively; 200 repetitions provide pilot
calibration, not precise operating characteristics.

Report the spatial relation as **supported**, **not supported**, or
**uninformative at the calibrated alternatives**. Do not say that persistence
automatically invalidates levels, and do not use an underpowered residual test
as an automatic licence to transform away the relation.

## Stage 3: show the descriptive fingerprint

For time-series levels regressions, place adjusted $R^2$ beside

$$
DW=\frac{\sum_{t=2}^T(\hat u_t-\hat u_{t-1})^2}
         {\sum_{t=1}^T\hat u_t^2}.
$$

Under a simple AR(1) approximation, $DW\simeq2(1-\hat\rho)$. The
Granger--Newbold rule $R^2>DW$ is a warning, not a test. [L]

For space, show the outcome, focal regressor, and residual maps, together with
pre-specified Moran or low-frequency summaries. High fit plus a smooth
residual field is the visual analogue, but there is no universal
“$R^2>$ Moran's I” threshold. The matrix and permutation scheme determine the
number, so use it descriptively.

## Stage 4: trace the coefficient from levels to the persistence boundary

### Time: the Prais--Winsten path

Under the maintained AR(1) disturbance

$$u_t=\rho u_{t-1}+\varepsilon_t,$$

Prais--Winsten jointly transforms the outcome and every design column. At
$\rho=0$ it is the levels regression. As $\rho\to1$, observations after the
first become first differences and the first observation receives vanishing
weight. Report the entire path of the focal coefficient and interval, not only
the fitted $\hat\rho$ row.

The new temporal pilot adds a REML profile set for $\rho$. It unions 97.5%
conditional coefficient intervals over a 97.5% profile-likelihood set, giving
a Bonferroni-protected nominal 95% interval under the maintained Gaussian AR(1)
family. The frozen battery has an intercept and one focal regressor; its
coverage is not automatic evidence for a many-control or dynamic application.
At `T=61`, 400 repetitions per cell give: [MC-T]

| Design class | Point-PW result | Protected profile result | Pointwise exact 95% MC interval span (point; protected) |
|---|---:|---:|---:|
| Four stationary/I(1)/drifted-I(1)/LTU nulls | size .0525--.0900 | size .0075--.0175 | size [.0328,.1224]; [.0015,.0357] |
| Three cointegration cells, $\beta=.25$ | coverage .9300--.9350; power .4875--.7925 | coverage .9850--.9925; power .2675--.4125 | coverage [.9004,.9571]; [.9676,.9985]; power [.4375,.8312]; [.2247,.4625] |

These 400-repetition cells are pilot calibration. The exact intervals, not
decimal differences inside them, determine how finely the rates can be read.

The Bonferroni logic is simple. Let $R$ be a confidence set for the true
persistence parameter $\theta_0$, and let $C(\theta_0)$ be a coefficient
interval valid at that parameter. If

$$
P(\theta_0\in R)\ge 1-\alpha_1
\quad\text{and}\quad
P\{\beta_0\in C(\theta_0)\}\ge 1-\alpha_2,
$$

then, without requiring independence,

$$
P\!\left\{\beta_0\in\bigcup_{\theta\in R}C(\theta)\right\}
\ge 1-\alpha_1-\alpha_2.
$$

Here $\alpha_1=\alpha_2=.025$. The guarantee is only as finite-sample-valid as
the persistence set and the conditional intervals themselves; profile-
likelihood calibration is approximate, which is why the Monte Carlo coverage
record remains necessary.

The protected interval solves the persistence-uncertainty problem
conservatively. It does not establish cointegration, validate AR(1), or preserve
power for free. Nor does it correct regressor--innovation endogeneity; the path
is a survival diagnostic unless the maintained GLS model is substantively
credible.

### Space: the half-life path

Let $D$ be pairwise distance divided by the sample maximum and maintain

$$R_h(i,j)=\exp\{-\log(2)D(i,j)/h\}.$$

Jointly whiten the outcome and full design, including the intercept, with a
scaled $R_h^{-1/2}$. As $h\to0$, the regression converges to levels. As
$h\to\infty$, its contrast-space limit is demeaned LBM-GLS. REML supplies a
point $\hat h$; a protected union carries a profile set for $h$. [MC-S]

On the 682-observation cross-country fixture with 47 country fixed
effects: [A, MC-S]

| Row | Half-life | Coefficient | C-SCPC p-value or interval |
|---|---:|---:|---:|
| Levels | 0 endpoint | .176640 | p=.0031 |
| REML spatial FGLS | .003854 | .150185 | p=.0113 |
| SPUR residual set, upper endpoint | .031273 | .092935 | p=.2734 |
| LBM-GLS | infinite endpoint | .088908 | p=.3143 |
| Bonferroni profile union | model-based set | — | $[.0249,.2714]$ |

The maintained exponential model says the coefficient survives. The broader
SPUR residual-half-life sensitivity spans significant and insignificant rows.
Those answer different questions: the SPUR set treats generated residuals as
observed and is descriptive; the profile union propagates range uncertainty
inside a narrower parametric covariance family.

Across eight frozen spatial cointegration cells, the protected union covers
.960--1.000. Across eight exact-I(1), I(1)-error/I(0)-treatment,
multivariate-I(1), and LTU2 null cells, it rejects .0125--.0325. [MC-S]

### How to read coefficient survival

- Survival under a well-supported covariance model says the result is not an
  artefact of choosing the levels endpoint within that model.
- Collapse toward zero says the levels result is persistence-sensitive; it
  does not prove the structural effect is zero.
- A path spanning both signs or both significance states reports uncertainty;
  the point persistence estimate must not suppress it.
- A transformed regression does not itself prove or disprove a long-run
  equilibrium. Cointegration and coefficient survival answer different
  questions.

## Stage 5: test covariance-family adequacy and route failures honestly

A confidence set for one persistence parameter cannot represent uncertainty
about the entire covariance family.

One conservative bridge is available when two procedures target the same
parameter under different covariance classes. If
$C_A=[L_A,U_A]$ and $C_B=[L_B,U_B]$ are their 95% intervals, report the
**model-class convex envelope**

$$
E=\operatorname{conv}(C_A\cup C_B)
 =[\min(L_A,L_B),\max(U_A,U_B)].
$$

For every DGP in the claimed combined model classes, at least one constituent must
target the same $\beta_0$ and possess its advertised coverage. Because $E$
contains each constituent, $P(\beta_0\in E)\ge .95$ whenever that condition
holds. No multiplicity adjustment is required for this containment argument.
The envelope includes zero when the procedures disagree in sign and excludes
it only when both intervals exclude zero in the same direction. This is not a
model-selection rule and deliberately sacrifices power. Under slope
heterogeneity, GLS, differencing, and spatial whitening can estimate different
weighted-average parameters; in that case an envelope of the reported slopes
has no common-parameter coverage interpretation.

### Time adequacy record

Inspect residual ACF/PACF, periodogram or low-frequency energy, dated breaks,
changing variance, tails, and the number of substantively independent regimes.
The temporal battery's off-family null results are: [MC-T]

| Error family | Point PW | Protected | FD+NW(2) | Convex envelope | Exact 95% MC interval, envelope |
|---|---:|---:|---:|---:|---:|
| ARMA(1,1) | .0450 | .0075 | .0525 | .0075 | [.0015,.0218] |
| AR(1), t3 innovations | .0775 | .0100 | .0700 | .0100 | [.0027,.0254] |
| AR(1), changing innovation variance | .0875 | .0150 | .0675 | .0150 | [.0055,.0324] |
| AR(1) plus omitted level break | .2575 | .0075 | .0575 | .0025 | [.0001,.0138] |
| Six common temporal regimes | .6600 | .5950 | .3375 | .3350 | [.2889,.3836] |

The protected procedure absorbs the tested break by widening toward the
persistence boundary, but it cannot control few-regime pseudoreplication.
Neither can short-bandwidth Newey--West after differencing.

The model-class convex envelope has null size `.0025--.0175` outside the common-
regime cell and `.9875--.9925` coverage in the three cointegration cells, but
its cointegration power is only `.2650--.3075`. It also fails the six-regime
null because both constituents fail there.

If AR(1) is inadequate, model known dynamics and breaks explicitly. First
differences plus HAC are a fallback only when the differenced residuals are
weakly dependent and there are enough effective time units. With a few common
regimes, use inference whose independent units are those regimes, a justified
fixed-$b$/HAR procedure, more data across regimes, or report that calibrated
inference is unavailable. The targeted 5,000-repetition follow-up confirms
the six-regime result. The protected profile rejects `.6028` (exact 95% MC
interval `[.5891,.6164]`), FD+NW(2) `.3256` (`[.3126,.3388]`), and their
convex envelope `.3194` (`[.3065,.3325]`). CR2/Satterthwaite clustered by the
known regimes rejects `.0258` (`[.0216,.0306]`); a t test on six balanced
regime means rejects `.0436` (`[.0381,.0496]`), and exact permutation across
those means rejects `.0432` (`[.0377,.0492]`). This controls rejection in that
tested DGP because the six regimes are genuinely independent by construction.
It does not create an automatic way to discover independent regimes in an
application. [MC-T]

### Spatial adequacy record

Inspect directional variograms or correlograms, borders and block structure,
tail behaviour, changing spatial variance, and the assignment level. Again,
no automatic adequacy detector has been validated.

The spatial protected union's off-family null size is .1025 under G722
anisotropy, .2950 and 1.000 under the two regional-block designs, and .0950
under G325 heavy tails. These four failures survive Holm correction. LBM plus
C-SCPC stays near .05 in both block designs, but fails other tested tail or
variance cases. Their model-class convex envelope gives: [MC-S]

| Geometry | Error family | Repetitions | Protected profile | LBM+C-SCPC | Model-class convex envelope | Exact 95% MC interval, envelope |
|---|---|---:|---:|---:|---:|---:|
| G722 | anisotropic | 400 | .1025 | .0500 | .0400 | [.0230,.0641] |
| G722 | regional block | 400 | .2950 | .0525 | .0475 | [.0288,.0732] |
| G722 | heavy-tailed | 400 | .0250 | .0800 | .0150 | [.0055,.0324] |
| G722 | heteroskedastic | 400 | .0250 | .0400 | .0125 | [.0041,.0289] |
| G325 | anisotropic | 400 | .0650 | .0550 | .0350 | [.0193,.0580] |
| G325 | regional block | 400 | 1.0000 | .0500 | .0200 | [.0087,.0390] |
| G325 | heavy-tailed | 2,000 | .0920 | .2565 | .0840 | [.0722,.0970] |
| G325 | heteroskedastic | 400 | .0350 | .1325 | .0275 | [.0138,.0487] |

The envelope also has size `.0050--.0250` in the eight maintained nulls and
coverage `.970--1.000` in the eight cointegration cells. It controls rejection
in the tested block and G722 anisotropy DGPs. The original 400-repetition G325
heavy-tail failure survived Holm correction (`.0875`, adjusted `p=.01765`);
the targeted run passed an exact first-400 identity gate and estimates size at
`.0840` (`[.0722,.0970]`, exact point-null `p=1.03e-10`). Thus the envelope
broadens the calibrated scope without making the procedure covariance-robust.

Use LBM+C-SCPC as an off-family sensitivity where its own scope is defensible.
When treatment varies at a regional or assignment level, cluster or estimate
at that level. An Ibragimov--Müller regional interval requires approximately
independent regional estimates centred on a common target; mechanically drawn
regions do not establish that premise. The existing spatial guide's
named-driver variance procedure is licensed only for its one frozen scenario
class.

For the two block DGPs, where the twelve independent regions are known by
construction, CR2/Satterthwaite clustered at that level has size `.0450` in
G722 and `.0425` in G325; regression on twelve region means has size `.0525`
in both. The matching temporal and spatial result is exact in spirit: moving
inference to the independently varying unit controls rejection in these
tested DGPs; a better row-level covariance parameter does not create more
information. [MC-S]

No end-to-end automatic adequacy-gate-plus-fallback rule has yet passed the
full spatial battery. Until it does, the half-life path is a powerful
sensitivity analysis and a calibrated maintained-family procedure, not a new
universal estimator.

## Stage 6: use mixed-order and external challenges

### ARDL/ECM bounds in time

The Pesaran--Shin--Smith bounds test evaluates the joint null of no levels
relationship in an unrestricted error-correction model. A statistic below the
I(0) lower bound fails to reject; one above the I(1) upper bound supports a
levels relation only with the bounds t-test on the lagged dependent variable
also beyond its upper bound (Cases I, III, V; in Cases II and IV the F-bounds
test alone applies); one between is inconclusive. It permits a mixture of I(0)
and I(1) regressors but not I(2). Match the deterministic case, lag selection,
and number of forcing variables in the levels relation (k counts I(0) and I(1)
regressors alike) to the critical values, and prefer
finite-sample or simulated values where feasible. [L]

This is robust to mixtures of I(0) and I(1) regressors only within its stated
conditions; it is not agnostic to integration order because I(2) variables are
excluded. Prais--Winsten and spatial LBM transformation are not bounds tests
and must not be advertised as equivalent evidence for a long-run relation.

### Holdout and placebo challenges

In time, freeze the complete model on a pre-declared training window and
forecast or backcast without re-estimating coefficients or break dates. Report
RMSE and define holdout $R^2$ explicitly as
$1-\mathrm{SSE}_{model}/\mathrm{SSE}_{benchmark}$. Pre-declare the benchmark:
the training-period mean, a deterministic trend, a random walk or last
observation, or another domain-specific naive forecast. For highly persistent
series, report performance against a random-walk or last-observation benchmark
as well as any fixed-mean comparison. When reproducing an application, name
and retain its published benchmark before adding alternatives. For synthetic
control, hold out part of the pre-period and refit weights using the training
portion only.

A failed holdout is evidence against stability and predictive content, not by
itself proof of spuriousness. A successful holdout is likewise not proof of
causality when the predictors share persistent drift.

In either domain, generate persistence-matched noise only from a defensible
pre-specified law and rerun the entire selection procedure. A spatial matched
placebo is a model-based stress test, not randomization inference. A
conditional randomization test is exact only when the assignment law is
actually documented and the observed treatment and surrogates are
exchangeable under its null.

Spatial regional agreement is corroboration or warning, not a terminal veto.
Space lacks time's natural past-to-future ordering, so buffered spatial
holdouts answer a less clean interpolation or transport question.

## Stage 7: calibrate size and power to the application

Preserve sample length and geometry, missingness, deterministic terms,
plausible breaks, innovation variance, persistence, treatment shape, controls,
and every tuning or selection step. Run the same complete pipeline on:

- weakly dependent or break-stationary nulls;
- independent unit-root or spatial-unit-root fields;
- cointegrated relations over plausible error persistence and effect sizes;
- local-to-unit boundaries;
- off-family dynamics, tails, variance processes, and regime structures; and
- the actual fixed regressors, locations, or dates where conditioning is part
  of the proposed method.

Report size, coverage, power at the declared $\delta$, interval width, routing
shares, applicability, Monte Carlo uncertainty, seeds, and multiplicity
adjustments. A non-rejection is substantive evidence only against alternatives
the procedure had a reasonable chance to detect.

## Stage 8: report five outputs, not one verdict

1. **Runnability.** Within calibrated range, calibration uncertain, or outside
   calibrated range, with the named reason.
2. **Published-method status.** Compatible with the diagnosed regime,
   unsupported in a matched failure class, not evaluated by the battery, or
   not assessable in calibrated form.
3. **Repaired-result status.** Survives, does not survive, or is uninformative
   at $\delta$, always with the coefficient and interval. “Does not survive”
   means the published claim was not reproduced by this procedure, not that
   the true effect is zero.
4. **Exact-null status.** Report a design-based or conditional-randomization
   null separately, or state that no documented assignment law makes it
   runnable.
5. **Identification status.** State whether the coefficient has a causal or
   structural interpretation under named identifying and exogeneity
   assumptions, is only a descriptive conditional association, or was not
   assessed by this persistence protocol.

Attach the persistence and cointegration evidence as a diagnostic block rather
than collapsing it into those outputs. When methods disagree, report which
assumptions and information distinguish them. Do not count correlated tests as
independent votes.

## Two worked receipts

### Francis (2026), 1963--2023 [A]

The finished EJW replication output verifies the time-series guide's worked
numbers. Across four levels specifications, adjusted $R^2$ is .826--.938 and
Durbin--Watson is .112--.354. Iterative Prais--Winsten estimates
$\hat\rho=.917$--.966. The three trend/break supply coefficients become
-.039 to -.048 with standard errors .076--.079; the no-trend row changes sign
to +.139 (.041). First-difference estimates are -.049 (.084) and -.081
(.101). Four bounds statistics, .838--1.319, are below the reported 10% I(0)
lower bound 3.84. Three frozen holdout $R^2$ values are -1.83, -13.46, and
-43.71.

Those convergent results are application-specific evidence despite low unit-
root-test power. Table 9's Prais--Winsten row is the temporal prototype for the spatial
path. The receipt carries no protected temporal profile for this application,
and the printed Table 9 row cannot stand in for one: a profile interval is
computed from the underlying series, never manufactured from a printed
coefficient and standard error.

### Cross-country spatial fixture [A, MC-S]

The levels coefficient is .1766 (C-SCPC p=.0031), the fitted half-life row is
.1502 (p=.0113), and LBM-GLS is .0889 (p=.3143). The broad descriptive SPUR
half-life envelope spans significant and insignificant results, while the
protected exponential-model union is $[.0249,.2714]$. Taking the convex
envelope with the LBM+C-SCPC interval gives the covariance-model convex envelope
$[-.1017,.2795]$, which includes zero. The precise conclusion is therefore
conditional: survival inside the maintained exponential family, but not
across the two tested covariance classes, with no licence to ignore block,
anisotropic, or tail misspecification.

## Reviewer checklist

1. [ ] Reproduce the focal levels result before changing anything.
2. [ ] Freeze the estimand, sample, deterministics or coordinates, direction,
   and $\delta$.
3. [ ] State the effective assignment or regime units, not only the row count.
4. [ ] Plot every stochastic variable and the levels residuals.
5. [ ] Run opposite-null persistence tests on outcomes and regressors.
6. [ ] Test residual persistence and the relevant cointegration claim.
7. [ ] Use test-specific critical values, deterministics, lags, seeds, and
   simulation counts.
8. [ ] Report $R^2$ beside Durbin--Watson in time; report spatial residual maps
   and pre-specified descriptive dependence summaries in space.
9. [ ] Report the full $\rho$ or $h$ coefficient path, the point row, the
   persistence set, and any protected union.
10. [ ] Distinguish standard-error correction from transformation of the
    estimating equation.
11. [ ] Audit covariance-family adequacy, including breaks or regions and
    effective independent units.
12. [ ] Where two valid procedures target the same parameter, report their
    model-class convex envelope; do not use it as a family-selection test.
13. [ ] Use ARDL bounds only after excluding I(2) and matching its critical-
    value case; do not invent a spatial analogue.
14. [ ] Add a frozen holdout, matched-noise exercise, regional sensitivity, or
    exact assignment-law test only where its premise is defensible.
15. [ ] Calibrate decisive non-rejections at the actual sample size and design.
16. [ ] Report runnability, published-method status, repaired result, exact
    null, and identification status separately.
17. [ ] Say “not reproduced by this procedure,” not “artifact,” “false,” or
    “zero,” unless other evidence independently licenses that stronger claim.

## Evidence files

The application fixtures and validation receipts are not distributed with
the skill (this file carries the protocol only):

- Temporal source guide: `spurious_regressions_guide.md` (distributed
  with the skill).
- Journal-comment application: replication script and finished results
  receipt.
- Temporal protected-profile battery: pilot README and Monte-Carlo
  summary/verdict receipts, including the exact binomial intervals, the
  model-class convex envelope, and 5,000-repetition effective-unit
  receipts.
- Spatial source protocol application, evidence tags E1–E35; the
  spatial cointegration design notes; and the spatial protected-profile
  battery with its 2,000-repetition G325 heavy-tail follow-up.
- Primary spatial theory: Müller & Watson on spatial unit roots,
  especially Remarks 4.1 and 4.2.

A validation script (not distributed) verifies the frozen receipts and records
environment checksums for the guide, code, and frozen outputs.

## References

Becker, Sascha O., P. David Boll, and Hans-Joachim Voth. 2026. “Testing and
Correcting for Spatial Unit Roots in Regression Analysis.” *Stata Journal*
26(2): 177--202.

Engle, Robert F., and C. W. J. Granger. 1987. “Co-Integration and Error
Correction: Representation, Estimation, and Testing.” *Econometrica* 55(2):
251--276.

Francis, Joseph. 2026. “Specification Searching in the Race between Education
and Technology.” *Econ Journal Watch* 23(1): 4--26.

Granger, C. W. J., and P. Newbold. 1974. “Spurious Regressions in
Econometrics.” *Journal of Econometrics* 2(2): 111--120.

Müller, Ulrich K., and Mark W. Watson. 2024. “Spatial Unit Roots and Spurious
Regression.” *Econometrica* 92(5): 1661--1695.

Pesaran, M. Hashem, Yongcheol Shin, and Richard J. Smith. 2001. “Bounds Testing
Approaches to the Analysis of Level Relationships.” *Journal of Applied
Econometrics* 16(3): 289--326.

Phillips, Peter C. B. 1986. “Understanding Spurious Regressions in
Econometrics.” *Journal of Econometrics* 33(3): 311--340.

Shin, Yongcheol. 1994. “A Residual-Based Test of the Null of Cointegration
against the Alternative of No Cointegration.” *Econometric Theory* 10(1):
91--115.
