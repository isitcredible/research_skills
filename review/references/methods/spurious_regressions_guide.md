# Protocol for Detecting and Diagnosing Spurious Regressions

## Decision rule

Treat a levels regression involving trending or highly persistent series as unvalidated until the time-series properties of the outcome, regressors, and regression residuals have been established.

If the outcome and one or more regressors are I(1), an OLS levels regression has a coherent long-run interpretation only if the relevant linear combination is I(0): the variables must be cointegrated. Cointegration is the escape hatch from spurious regression. Without it, conventional OLS standard errors, *t*-statistics, and goodness-of-fit measures do not have their usual interpretation. The appropriate model is normally in differences, possibly with short-run dynamics.

No conclusion should rest on a unit-root test failing to reject its null. Unit-root and cointegration tests have low power in short samples. Failure to reject a unit root is not proof of a unit root; failure to reject no cointegration is not proof of no cointegration. The evidentiary standard is convergence across:

- tests with opposite null hypotheses;
- break-robust tests;
- an order-agnostic ARDL/ECM bounds test;
- direct correction for residual autocorrelation;
- first-difference estimates; and
- out-of-sample performance and, where feasible, noise-regressor placebos.

The strongest diagnosis does not depend on any single classification of a series as I(0) or I(1).

## 1. Why trending levels regressions are dangerous

Consider

$$
y_t = \alpha + \beta'x_t + d_t'\gamma + u_t,
$$

where $y_t$ is the outcome, $x_t$ contains the regressor or regressors of interest, and $d_t$ contains deterministic terms such as a constant, trend, seasonal indicators, or dated breaks.

Independent persistent processes can drift together for long intervals. In a regression of one independent random walk on another, sample covariance need not settle toward zero as the sample grows. OLS can therefore produce an apparently precise coefficient, a high $R^2$, and conventional significance even though the series are unrelated. The residuals remain highly persistent and the usual OLS asymptotics fail (Granger and Newbold 1974; Phillips 1986).

A deterministic time trend does not remove a stochastic trend. Nor does a near-perfect in-sample fit validate the relation. High $R^2$ is one of the products of a spurious regression, not evidence against it.

If $y_t$ and the stochastic elements of $x_t$ are I(1), ask whether there is a vector $(1,-\beta')$ such that

$$
u_t = y_t-\alpha-\beta'x_t-d_t'\gamma
$$

is I(0). If so, the variables are cointegrated and the levels coefficient may describe a long-run equilibrium. If $u_t$ is I(1), the fitted levels relation is spurious. With several I(1) variables, the question concerns the cointegration rank and the particular cointegrating vector, not whether every pair is cointegrated.

Before testing, preserve the paper's exact sample, transformations, deterministic terms, break definitions, and lag conventions. Plot each series and the levels-regression residuals. Record missing years and irregular spacing: annual unit-root methods require a genuinely consecutive annual series, not a sequence of widely separated benchmark observations treated as adjacent.

## 2. Characterize the integration order

Run the tests on each outcome and stochastic regressor in levels and first differences. An I(1) classification requires evidence that the level is nonstationary and the first difference is stationary. The ARDL bounds procedure used later permits a mixture of I(0) and I(1) variables, but not I(2) variables; testing first differences is therefore still necessary to rule out I(2).

Use deterministic terms appropriate to the data-generating claim. A test with only a constant, a test with a constant and trend, and a break test answer different questions. Report the sample, deterministic specification, lag or bandwidth rule, statistic, critical values, inference, and any estimated break date.

### ADF and Phillips-Perron: null of a unit root

The augmented Dickey-Fuller test estimates a unit-root regression with lagged differences to absorb serial correlation. Select the lag order by a declared rule, such as AIC within a pre-specified maximum, and check the resulting residuals. The Phillips-Perron test uses a nonparametric correction for serial correlation and heteroskedasticity rather than adding the same lag structure. Both have:

$$
H_0:\text{unit root}, \qquad H_1:\text{stationarity around the specified deterministic terms}.
$$

A statistic that does not cross the relevant critical value is a non-rejection, not a finding that the series has a unit root.

### KPSS: reversed null of stationarity

The KPSS test reverses the hypotheses:

$$
H_0:\text{level or trend stationarity}, \qquad H_1:\text{unit root}.
$$

Use the level-stationary or trend-stationary version to match the deterministic specification, and state the long-run-variance bandwidth rule. Evidence is materially stronger when ADF and Phillips-Perron fail to reject a unit root while KPSS rejects stationarity. If both sides fail to reject, the sample is uninformative. If both sides reject, investigate breaks, nonlinearities, fractional integration, bandwidth sensitivity, and deterministic-term misspecification rather than choosing the preferred result.

### Zivot-Andrews: one endogenous break

The Zivot-Andrews test allows one break date to be selected from the data. Use the break model that fits the claim: intercept break, trend break, or both. Select the augmentation lag transparently, for example by AIC within a declared maximum. Report both the test statistic and the endogenously selected date.

This test addresses the objection that apparent nonstationarity is a stationary process around one structural break. Rejection can reclassify a series as break-stationary; non-rejection leaves the unit-root hypothesis unresolved. Because the break date is estimated, ordinary Dickey-Fuller critical values are invalid.

### Required interpretation

Classify the evidence, not merely the series:

| Pattern | Interpretation |
|---|---|
| ADF/PP reject; KPSS does not reject | Evidence for stationarity under the stated deterministic specification |
| ADF/PP do not reject; KPSS rejects | Convergent evidence for nonstationarity |
| Opposite-null tests disagree or both fail to reject | Integration order unresolved; do not build the diagnosis on pre-testing |
| Zivot-Andrews rejects when ordinary tests do not | Plausible break-stationarity; report and carry the break into subsequent tests |

## 3. Test for cointegration

Apply several tests because their power, treatment of endogeneity, deterministic terms, and assumptions differ. At least one test should reverse the usual null of no cointegration. Use critical values designed for the specific cointegration statistic. Standard ADF or univariate KPSS tables are not substitutes.

### Engle-Granger residual test

1. Estimate the proposed long-run levels equation, including its constant, trend, and other deterministic terms.
2. Apply an ADF test to the fitted residuals. The residual test regression normally contains no additional constant or trend because the residuals come from the first-stage cointegrating regression.
3. Compare the statistic with MacKinnon response-surface critical values matched to the number of stochastic variables, deterministic specification, and sample size, not standard ADF critical values.

The null is no cointegration (Engle and Granger 1987). Rejecting it supports a stationary residual combination. Non-rejection is not proof of no cointegration, especially in a short sample. The two-step test can be sensitive to which variable is normalized as the dependent variable and to the first-stage dynamics.

### Phillips-Ouliaris residual tests

Add Phillips-Ouliaris $Z_\alpha$ or $Z_t$ tests as semiparametric residual-based checks (Phillips and Ouliaris 1990). Their null is no cointegration. They correct for serial correlation and endogeneity differently from Engle-Granger. Use Phillips-Ouliaris critical values for the fitted deterministic case; neither ordinary ADF nor ordinary normal critical values apply. Agreement between Engle-Granger and Phillips-Ouliaris is more informative than either alone.

### Johansen trace test

Fit a VAR in the levels variables, select its lag order by a declared information criterion within a pre-specified maximum, and translate that choice correctly into the lag parameter used by the Johansen implementation. Specify the deterministic components inside and outside the cointegrating space explicitly.

The trace test proceeds sequentially from

$$
H_0:r=0
$$

to higher ranks. For a proposed single long-run relation, rejection of $r=0$ is the necessary first step. Report the selected VAR order, deterministic case, trace statistics, critical values, and inferred rank (Johansen 1988, 1991). A rank conclusion obtained after searching lag orders or deterministic cases should be labelled accordingly.

### Shin test: reversed null of cointegration

Shin's residual-based test has

$$
H_0:\text{deterministic cointegration}, \qquad H_1:\text{no cointegration}.
$$

Estimate the cointegrating vector by Stock-Watson dynamic OLS, including contemporaneous, lead, and lag terms in first differences as appropriate, then compute the KPSS-type statistic on the DOLS residuals (Shin 1994; Stock and Watson 1993). Use Shin's own critical values for the number of stochastic regressors and the deterministic specification.

Do not use off-the-shelf univariate `ur.kpss` critical values. Those values are larger than the applicable Shin cointegration values in common cases and therefore bias the decision toward failing to reject the null of cointegration. A persuasive no-cointegration diagnosis combines non-rejection by Engle-Granger, Phillips-Ouliaris, or Johansen with rejection of cointegration by Shin.

### Break-robust cointegration

Use Gregory-Hansen tests when one regime shift may occur in the cointegrating relation (Gregory and Hansen 1996). Choose among level shift, level shift with trend, and regime shift according to the substantive relation, and report the endogenously selected break date and the model-specific critical values.

Maki's extension permits an unknown number of breaks (Maki 2012). With one allowed break it can implement a Gregory-Hansen-type exercise; with more breaks it tests a broader claim. Pre-specify the maximum number of breaks that the sample can support. Break flexibility consumes power and can overfit short series, so report all selected dates and the exact break model.

The purpose is diagnostic: if ordinary tests find no cointegration and a break-robust test also finds none, the claim that a genuine long-run relation merely changed at an unknown date has been directly examined rather than assumed.

## 4. Check the Granger-Newbold fingerprint

For every levels specification, report the ordinary $R^2$ or adjusted $R^2$ beside the Durbin-Watson statistic

$$
DW=\frac{\sum_{t=2}^{T}(\hat u_t-\hat u_{t-1})^2}{\sum_{t=1}^{T}\hat u_t^2}.
$$

Under a simple AR(1) approximation, $DW\approx2(1-\hat\rho)$. A value near zero therefore indicates residual persistence near a unit root. The Granger-Newbold rule of thumb is:

$$
R^2>DW \quad\Rightarrow\quad \text{suspect a spurious regression}.
$$

High $R^2$ together with very low $DW$ is the classic fingerprint: the regression tracks the common movement in levels while leaving a near-unit-root residual. It is a screening rule, not a proof. A stationary but dynamically misspecified model can also have serially correlated residuals. Follow it with residual plots and autocorrelation functions, cointegration tests, and corrected estimators.

## 5. Ask whether the result survives treatment of autocorrelation

### Prais-Winsten iterative FGLS

Estimate an AR(1) error process,

$$
u_t=\rho u_{t-1}+\varepsilon_t,
$$

and apply the Prais-Winsten transformation, retaining the transformed first observation (Prais and Winsten 1954). Report:

- the estimated $\hat\rho$;
- the coefficient of interest, standard error, sign, and significance before and after correction;
- the Durbin-Watson statistic before and after correction; and
- convergence and residual diagnostics.

Prais-Winsten asks whether the result survives a standard AR(1) correction without requiring a prior verdict that every series is I(0) or I(1). It does not establish cointegration and should not be used to rescue an invalid levels interpretation. Its diagnostic value lies in coefficient survival.

The connection to differencing is exact in the limit. For $t\ge2$, the transformed equation uses $y_t-\rho y_{t-1}$ and $x_t-\rho x_{t-1}$. As $\rho\rightarrow1$, those quasi-differences become first differences. A fitted $\hat\rho$ near one should therefore make Prais-Winsten estimates approach the first-difference result.

### First-difference regression with HAC inference

If I(1) variables are not cointegrated, estimate the short-run relation in differences:

$$
\Delta y_t=\alpha+\theta'\Delta x_t+\sum_i\phi_i\Delta y_{t-i}+\sum_j\Gamma_j'\Delta x_{t-j}+e_t.
$$

Use a parsimonious, pre-specified lag structure or select it with a declared rule. Report Newey-West heteroskedasticity-and-autocorrelation-consistent standard errors and the bandwidth or lag choice (Newey and West 1987). Newey-West corrects inference for remaining serial correlation and heteroskedasticity; it does not make an invalid levels regression valid.

Compare sign, magnitude, and precision with the levels estimate. A large, precise levels coefficient that becomes small and imprecise in differences, while Prais-Winsten estimates $\rho$ near one and reaches the same result, is strong evidence that the levels coefficient came from persistence rather than a stable relation.

## 6. Use an order-agnostic ARDL/ECM bounds test

Estimate an unrestricted error-correction model:

$$
\Delta y_t=\alpha+\lambda y_{t-1}+\delta'x_{t-1}
+\sum_i\psi_i\Delta y_{t-i}
+\sum_j\Gamma_j'\Delta x_{t-j}
+d_t'\eta+e_t.
$$

The Pesaran-Shin-Smith bounds test evaluates the joint null

$$
H_0:\lambda=0,\;\delta=0,
$$

that no long-run levels relationship exists (Pesaran, Shin, and Smith 2001). Its lower critical value assumes I(0) regressors; its upper value assumes I(1) regressors:

- $F$ below the lower bound: fail to reject the null of no long-run levels relationship;
- $F$ above the upper bound: run the bounds $t$-test on $\lambda$ (PSS 2001's second step, p. 304); support a long-run levels relationship only when $t$ is also beyond (more negative than) its upper ($I(1)$) bound ($t < t_U < 0$) — an $F$ rejection with $t$ inside its bounds leaves a degenerate relation (lagged regressor levels significant, no error correction) open (Cases I, III, V; in Cases II and IV only the F-bounds test exists);
- $F$ between the bounds: inconclusive.

The test is valid when the stochastic regressors are a mixture of I(0) and I(1), so it does not require correct classification of each series. It is not valid with I(2) variables. This is why first-difference unit-root checks remain necessary even though precise I(0)/I(1) classification is not.

Match the critical-value case to the intercept and trend specification. Select ARDL lags transparently, report the chosen order, and test the residuals. In the bounds calculation, $k$ counts every forcing variable in the tested levels/long-run relation — I(0) and I(1) alike, since the bounds bracket the all-I(0) and all-I(1) extremes of that full set (PSS 2001, pp. 299–301); the lagged dependent variable, deterministic trends and one-off break dummies (PSS 2001, p. 307 and fn. 17) do not add to $k$. Under-counting $k$ raises the critical values and manufactures false "no cointegration" verdicts. Use finite-sample or simulated critical values where available and identify them as such.

This test should carry particular weight when conventional unit-root tests are underpowered or disagree. A bounds statistic below the lower bound makes the integration-order dispute moot for the proposed levels relation.

## 7. Validate out of sample

Set a training window without using the holdout outcomes. Estimate the complete specification, including all trend and break terms, on that window. Freeze the coefficients and project into a later forecast window or an earlier backcast window. Do not re-estimate coefficients, choose new breaks, or alter transformations after viewing holdout performance.

Report the holdout root-mean-square error and

$$
R^2_{OOS}=1-
\frac{\sum_{t\in H}(y_t-\hat y_t)^2}
{\sum_{t\in H}(y_t-\bar y_H)^2},
$$

where $H$ is the holdout window and $\bar y_H$ is the holdout-period mean. State whether forecasts are conditional on realized regressor values. A negative $R^2_{OOS}$ means that the fitted model performs worse than the holdout mean.

A stable structural relation should retain its sign, scale, and useful predictive content across a defensible holdout. A spurious levels fit commonly diverges once the training interval ends. This exercise requires no unit-root classification and is therefore immune to the objection that ADF or cointegration tests lack power.

For synthetic-control designs, reserve part of the pre-treatment period for validation or backcasting. Post-treatment fit cannot validate an unobserved counterfactual because the untreated outcome is unavailable. Re-run donor selection and weight estimation using only the training portion; evaluate the frozen synthetic series in the held-out pre-treatment observations. Unit placebos and alternative treatment dates remain separate falsification exercises.

Where the design allows, add noise-regressor placebos. Generate unrelated series with the same sample length, missingness, drift, volatility, and persistence as the regressor of interest; then repeat the entire estimation and selection procedure. Report how often pure noise reproduces the published coefficient sign, *t*-statistic, $R^2$, or in-sample path. A method that routinely extracts the claimed result from unrelated persistent noise has failed a direct calibration test.

## 8. Quantify test power where feasible

This Monte Carlo step strengthens the EJW protocol; it was not part of Francis (2026).

Calibrate simulations to the observed sample rather than quoting generic claims about low power. Preserve:

- sample length, spacing, and missing-data pattern;
- deterministic drift and any plausible breaks;
- innovation variance, cross-correlation, and short-run ARMA dynamics;
- the observed range of persistence, including local-to-unity alternatives; and
- the exact lag-selection, bandwidth, break-search, and critical-value procedures used in the empirical analysis.

Simulate at least four classes of data-generating process: stationary or break-stationary series; independent unit-root series; cointegrated I(1) series with plausible adjustment speeds; and non-cointegrated I(1) series with correlated innovations. For every empirical test, estimate:

1. **Size:** the rejection rate when that test's null is true.
2. **Power:** the rejection rate against substantively plausible alternatives.

Report rejection curves over persistence and error-correction speed rather than one favorable calibration. A non-rejection is informative only if the test had reasonable power against the alternatives that matter. If calibrated power is low, label the non-rejection as empty and rely on opposite-null tests, the bounds test, coefficient survival under Prais-Winsten and differencing, and out-of-sample performance. If empirical size is distorted by the short sample or break search, use simulated critical values or qualify the nominal significance level.

## 9. Synthesis standard

Do not count test statistics as independent votes when they reuse the same residuals or impose the same assumptions. Organize the conclusion around distinct identifying information:

| Evidence class | Question |
|---|---|
| Opposite-null unit-root tests | Are the individual series stationary, integrated, or unresolved? |
| Residual, system, reversed-null, and break cointegration tests | Is any stable long-run combination supported? |
| $R^2$ and Durbin-Watson | Does the levels fit have the Granger-Newbold fingerprint? |
| Prais-Winsten and first differences | Does the coefficient survive removal of persistence? |
| ARDL/ECM bounds test | Is a levels relation supported without exact I(0)/I(1) classification? |
| Holdout and noise placebos | Does the relation work beyond the data that generated it, and can noise reproduce it? |
| Calibrated Monte Carlo | Which rejections and non-rejections are informative at the observed sample size? |

A defensible finding of a long-run relationship requires stationary residuals or positive cointegration evidence, bounds $F$ and $t$ both beyond their upper bounds (Cases I, III, V; in Cases II and IV only the F-bounds test exists), stable corrected estimates, and acceptable holdout performance. If these disagree, report the disagreement. A high in-sample $R^2$ never resolves it.

> ## Worked illustration: Francis (2026), annual data for 1963-2023
>
> This box records the actual statistics produced by `9_Tests.R` and `Replication_Results.txt` (the application's replication script and finished results receipt, not distributed with the skill). It illustrates the protocol; the substantive variables are not part of the general decision rule.
>
> **Integration order.** For the outcome, ADF = -1.18 and Phillips-Perron = -1.40, neither close to the 5 percent critical values (-3.45 and -3.48). KPSS = 0.17, above its 5 percent trend-stationarity critical value of 0.15. Zivot-Andrews = -3.27 and does not reject a unit root; its endogenous break is 1982. For the regressor, ADF = -1.23 and Phillips-Perron = -1.23 do not reject a unit root, while KPSS = 0.36 rejects trend stationarity even at 1 percent (critical value 0.22). Zivot-Andrews is the exception: -6.11 rejects a unit root with a break dated 1981. The break result makes exact I(0)/I(1) classification ambiguous for the regressor rather than invalidating the rest of the diagnosis.
>
> **Cointegration.** The Johansen trace statistic for $r=0$ is 11.71, below the 10 percent critical value of 22.76. AIC selected a VAR order of one, with the implemented minimum of two used for the test. The Engle-Granger residual ADF statistic is -1.11, compared with MacKinnon response-surface critical values of -4.26, -3.63, and -3.34 at 1, 5, and 10 percent. Shin's DOLS-residual statistic is 0.19, above Shin's 1 percent critical value of 0.184, rejecting the reversed null of cointegration. The one-break Gregory-Hansen/Maki statistic is -4.22, short of the 10 percent critical value of -5.28; the endogenous break is 1999. Phillips-Ouliaris was not reported in the EJW analysis and is an addition to the reusable protocol above.
>
> **Granger-Newbold fingerprint.** Across four levels specifications, adjusted $R^2$ values are 0.826, 0.902, 0.938, and 0.901, while Durbin-Watson statistics are 0.112, 0.174, 0.354, and 0.181. Every specification has $R^2>DW$, with a high fit and near-unit-root residual autocorrelation.
>
> **Autocorrelation and differences.** Prais-Winsten estimates $\hat\rho$ of 0.966, 0.933, 0.917, and 0.937. After correction, Durbin-Watson rises to 1.891, 1.901, 1.885, and 1.850. In the trend and break specifications, the regressor coefficients become -0.042 (SE 0.078), -0.039 (0.076), and -0.048 (0.079), all insignificant. The no-trend specification changes sign and is significantly positive, 0.139 (0.041), rather than retaining the hypothesized negative relation. First-difference estimates are likewise small and insignificant: -0.049 (Newey-West SE 0.084) contemporaneously and -0.081 (0.101) with lagged differences; adjusted $R^2$ is -0.011 and -0.004.
>
> **Order-agnostic bounds test.** The four ARDL/ECM bounds statistics are 1.319, 0.914, 0.992, and 0.838. Each is below the 10 percent I(0) lower bound of 3.84. The error-correction coefficients are also insignificant. The result therefore does not depend on deciding whether the break-adjusted regressor is I(0) or I(1).
>
> **Out of sample.** Frozen specifications produce $R^2_{OOS}=-1.83$ for the 1988-2005 forecast, -13.46 for the 1914-1962 backcast, and -43.71 for the 2006-2023 forecast. Each performs worse than the mean of its own holdout period. This evidence is independent of unit-root-test power.
>
> **Diagnosis.** No single non-rejection carries the conclusion. The reversed-null tests, break-robust cointegration test, bounds test, Durbin-Watson fingerprint, Prais-Winsten correction, first differences, and three holdouts all point away from a stable levels relation.

## Reviewer checklist

1. [ ] Plot the outcome, every stochastic regressor, and the levels-regression residuals; verify consecutive timing and transformations.
2. [ ] Reproduce the reported levels regression exactly before changing its time-series treatment.
3. [ ] Report ADF and Phillips-Perron tests with the null of a unit root and declared lag/bandwidth rules.
4. [ ] Report KPSS with the reversed null of level or trend stationarity and the correct deterministic case.
5. [ ] Run Zivot-Andrews or another justified break-unit-root test and report the endogenous break date.
6. [ ] Test first differences to rule out I(2); do not infer I(1) from a level-test non-rejection alone.
7. [ ] Run Engle-Granger with MacKinnon response-surface critical values, not standard ADF tables.
8. [ ] Add Phillips-Ouliaris residual tests with Phillips-Ouliaris critical values.
9. [ ] Run Johansen trace tests with a documented VAR lag rule, deterministic case, and inferred rank.
10. [ ] Run Shin's reversed-null test on DOLS residuals using Shin's critical values, not ordinary KPSS values.
11. [ ] Run Gregory-Hansen or Maki break-robust cointegration tests and report the selected break model and date(s).
12. [ ] Place $R^2$ beside Durbin-Watson for every levels specification; flag $R^2>DW$ as the Granger-Newbold fingerprint.
13. [ ] Re-estimate by iterative Prais-Winsten; report $\hat\rho$, coefficient survival, and Durbin-Watson before and after correction.
14. [ ] Estimate a first-difference model with declared dynamics and Newey-West HAC standard errors.
15. [ ] Run the Pesaran-Shin-Smith ARDL/ECM bounds test; rule out I(2), use the correct deterministic case, and count every forcing variable in the levels relation in $k$ (I(0) and I(1) alike — not the lagged dependent variable or deterministic terms).
16. [ ] Reserve a defensible forecast or backcast window; freeze the model and report holdout error and $R^2_{OOS}$.
17. [ ] For synthetic control, reserve pre-treatment observations for validation and re-estimate weights using the training window only.
18. [ ] Where feasible, run persistence-matched noise-regressor placebos through the complete specification-selection procedure.
19. [ ] Calibrate Monte Carlo size and power to the observed sample, drift, volatility, persistence, breaks, and lag-selection rules; identify this as an extension if it was not in the original analysis.
20. [ ] Base the verdict on convergence across opposite-null, order-agnostic, corrected-estimator, and holdout evidence; never on failure to reject or in-sample fit alone.

## References

Dickey, David A., and Wayne A. Fuller. 1979. "Distribution of the Estimators for Autoregressive Time Series with a Unit Root." *Journal of the American Statistical Association* 74(366): 427-431.

Engle, Robert F., and C. W. J. Granger. 1987. "Co-Integration and Error Correction: Representation, Estimation, and Testing." *Econometrica* 55(2): 251-276.

Francis, Joseph. 2026. "Specification Searching in the Race between Education and Technology." *Econ Journal Watch* 23(1): 4-26.

Granger, C. W. J., and P. Newbold. 1974. "Spurious Regressions in Econometrics." *Journal of Econometrics* 2(2): 111-120.

Gregory, Allan W., and Bruce E. Hansen. 1996. "Residual-Based Tests for Cointegration in Models with Regime Shifts." *Journal of Econometrics* 70(1): 99-126.

Johansen, Søren. 1988. "Statistical Analysis of Cointegration Vectors." *Journal of Economic Dynamics and Control* 12(2-3): 231-254.

Johansen, Søren. 1991. "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models." *Econometrica* 59(6): 1551-1580.

Kwiatkowski, Denis, Peter C. B. Phillips, Peter Schmidt, and Yongcheol Shin. 1992. "Testing the Null Hypothesis of Stationarity against the Alternative of a Unit Root: How Sure Are We That Economic Time Series Have a Unit Root?" *Journal of Econometrics* 54(1-3): 159-178.

MacKinnon, James G. 1991. "Critical Values for Cointegration Tests." In *Long-Run Economic Relationships: Readings in Cointegration*, edited by Robert F. Engle and C. W. J. Granger, 267-276. Oxford: Oxford University Press.

Maki, Daiki. 2012. "Tests for Cointegration Allowing for an Unknown Number of Breaks." *Economic Modelling* 29(5): 2011-2015.

Newey, Whitney K., and Kenneth D. West. 1987. "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." *Econometrica* 55(3): 703-708.

Pesaran, M. Hashem, Yongcheol Shin, and Richard J. Smith. 2001. "Bounds Testing Approaches to the Analysis of Level Relationships." *Journal of Applied Econometrics* 16(3): 289-326.

Phillips, Peter C. B. 1986. "Understanding Spurious Regressions in Econometrics." *Journal of Econometrics* 33(3): 311-340.

Phillips, Peter C. B., and Sam Ouliaris. 1990. "Asymptotic Properties of Residual Based Tests for Cointegration." *Econometrica* 58(1): 165-193.

Phillips, Peter C. B., and Pierre Perron. 1988. "Testing for a Unit Root in Time Series Regression." *Biometrika* 75(2): 335-346.

Prais, S. J., and C. B. Winsten. 1954. "Trend Estimators and Serial Correlation." Cowles Commission Discussion Paper 383.

Shin, Yongcheol. 1994. "A Residual-Based Test of the Null of Cointegration against the Alternative of No Cointegration." *Econometric Theory* 10(1): 91-115.

Stock, James H., and Mark W. Watson. 1993. "A Simple Estimator of Cointegrating Vectors in Higher Order Integrated Systems." *Econometrica* 61(4): 783-820.

Zivot, Eric, and Donald W. K. Andrews. 1992. "Further Evidence on the Great Crash, the Oil-Price Shock, and the Unit-Root Hypothesis." *Journal of Business & Economic Statistics* 10(3): 251-270.
