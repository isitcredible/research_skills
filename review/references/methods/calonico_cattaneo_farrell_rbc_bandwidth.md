# Robust bias-corrected RD inference and bandwidth choice — Calonico, Cattaneo, Farrell & Titiunik (2014–2022)

Distillation of five sources, all audited in their published versions:
Calonico, Cattaneo & Titiunik (CCT), "Robust Nonparametric Confidence
Intervals for Regression-Discontinuity Designs," *Econometrica* 82(6) (2014),
2295–2326; Calonico, Cattaneo & Farrell (CCF 2018), "On the Effect of Bias
Estimation on Coverage Accuracy in Nonparametric Inference," *Journal of the
American Statistical Association* 113 (2018), 767–779; Calonico, Cattaneo &
Farrell (CCF 2020), "Optimal Bandwidth Choice for Robust Bias-Corrected
Inference in Regression Discontinuity Designs," *Econometrics Journal* 23(2)
(2020), 192–210; Calonico, Cattaneo & Farrell (CCF 2022), "Coverage Error
Optimal Confidence Intervals for Local Polynomial Regression," *Bernoulli*
28(4) (2022), 2998–3022; and Calonico, Cattaneo, Farrell & Titiunik (CCFT
2017), "rdrobust: Software for Regression-Discontinuity Designs," *Stata
Journal* 17(2) (2017), 372–404, which documents the 2016 release of the
package. The supplemental appendices, which hold the exact variance and
bandwidth formulas, were not audited. Source PDFs (not distributed with the
skill): `Calonico_Cattaneo_Titiunik_2014_RobustRDD_Econometrica.pdf`,
`Calonico_Cattaneo_Farrell_2018_BiasCorrectionCoverage_JASA.pdf`,
`Calonico_Cattaneo_Farrell_2020_OptimalBandwidthRBC_EctJ.pdf`,
`Calonico_Cattaneo_Farrell_2022_CoverageErrorOptimalCI_Bernoulli.pdf`,
`Calonico_Cattaneo_Farrell_Titiunik_2017_rdrobust_StataJ.pdf`.

Verification status: source-audited 2026-10-15.

Use in this battery: `rdd-diagnostics` core checks "Which row carries the
verdict" and "Bandwidth and order sensitivity", the conditional bullets on
clustering and on backing out an unstated bandwidth, and the fuzzy and kink variants; companion to
`rdd_methods_guide.md` §1 and `kolesar_rothe_2018_discrete_rdd.md`.

## 1. Setting and estimand

- Estimand: the average effect at the cutoff in sharp RD, its derivative jump
  in sharp kink RD (up to a known scale factor), and the ratios of these in
  fuzzy and fuzzy kink RD (CCT §§2–3, pp. 2298, 2305–2308).
- The running variable must be continuously distributed near the cutoff.
  CCT Remark 1 (p. 2299): with many mass points the results may still be a
  good approximation; with few mass points they do not apply without further
  assumptions, and other approaches (local randomization) may be more
  appropriate.
- Point estimation is local polynomial of order p on each side; p = 1 is the
  preferred order (CCFT 2017, p. 376; CCF 2020, p. 195, citing poor behaviour
  of higher-order fits near boundaries). For the kink design CCT prefer a
  local quadratic over a local linear fit for boundary-bias reasons (§3.1,
  p. 2305); CCF 2022 treats p − ν odd as the standard case (p. 3002).
- Fuzzy designs are bias-corrected through the first-order linearization of
  the ratio, not by correcting numerator and denominator separately (CCT
  p. 2308); Theorem 3 assumes a non-zero first-stage jump.

## 2. Why conventional intervals at MSE-optimal bandwidths undercover

- The MSE-optimal bandwidth balances squared bias against variance, so
  h_MSE ∝ n^(−1/(2p+3)) and the leading bias stays first order in the
  t-statistic. The conventional interval needs a bandwidth small enough that
  nh^(2p+3) → 0, which h_MSE violates by construction (CCT pp. 2296,
  2300–2301; CCF 2020 p. 196). CCT's abstract describes MSE-optimal
  bandwidths as "by construction not valid for conventional confidence
  intervals" while valid for the robust approach (p. 2295).
- The coverage error of the conventional interval at h_MSE does not shrink to
  zero (CCF 2020 p. 200, item 1; CCF 2022 pp. 3004–3005). Cross-validation
  and IK-type plug-in selectors share the problem (CCT p. 2301).
- How bad in simulation: CCT Table I (pp. 2316–2317), nominal 95%,
  nearest-neighbour SEs, Model 2: conventional coverage 30.3% at the IK
  bandwidth and 87.3% at the CCT bandwidth, against 89.5% and 93.2% for the
  robust interval. CCF 2020 Table 2 (p. 206): 88.7% conventional versus 93.7%
  robust at the estimated MSE bandwidth. The distortion depends on curvature
  near the cutoff; it is not a fixed amount.
- The same applies to the CE-optimal bandwidth: it is too large for the
  conventional interval, which keeps a first-order coverage distortion there
  (CCF 2020 p. 200, item 3).
- Bootstrapping the conventional estimator does not help, because the
  bootstrap distribution is centred on its biased expectation (CCT Remark 6,
  p. 2304).

## 3. What robust bias correction does

Three intervals, which `rdrobust` labels Conventional, Bias-corrected and
Robust:

| Interval | Centre | Standard error | Valid at h_MSE? |
|---|---|---|---|
| Conventional | τ̂(h) | conventional, V̂(h) | no |
| Bias-corrected (traditional) | τ̂(h) − h^(p+1)B̂(b) | conventional, V̂(h) | only as h/b → 0; poor in finite samples |
| Robust bias-corrected (RBC) | τ̂(h) − h^(p+1)B̂(b) | V̂_bc(h, b), includes bias-estimate variability and its covariance with τ̂ | yes |

- The bias estimate uses a local polynomial of order q = p + 1 with pilot
  bandwidth b (CCT p. 2302; CCF 2020 p. 197). Traditional bias correction
  re-centres but keeps the conventional SE; its justification needs
  h/b → 0, which never holds in a finite sample (CCT p. 2302). RBC
  re-centres and re-scales: Theorem 1 (p. 2303) allows ρ = h/b → ρ ∈ [0, ∞].
- The RBC interval is centred on the bias-corrected estimate, not on τ̂(h)
  (CCT p. 2303; CCF 2020 p. 197). Its variance V_bc estimates the variance of
  the bias-corrected estimator, not of τ̂(h) (CCF 2020 p. 197).
- ρ = 1 (b = h, same kernel) makes the bias-corrected estimator numerically
  identical to the local polynomial of order p + 1 at bandwidth h, with
  matching variance. "Linear point estimate, local-quadratic interval at the
  linear MSE bandwidth" is therefore RBC with ρ = 1 (CCT Remark 7,
  pp. 2304–2305). CCF 2018 recommends ρ = 1 as an automatic choice
  (p. 773); CCF 2020 gives three options — ρ = 1, a data-free ρ* that
  minimizes interval length (0.850 for triangular kernel, p = 1; 1 for the
  uniform kernel; Table 1, p. 201), or ρ̂ = ĥ_MSE / b̂_MSE (p. 202).
  MSE-optimal h and b imply ρ_n → 0 asymptotically (CCT Remark 12, p. 2311).
- Studentization must be fixed-n (pre-asymptotic): an asymptotic variance
  formula adds coverage error, especially at boundary points such as the RD
  cutoff (CCF 2018 pp. 768, 774; CCF 2022 p. 3003).
- Length: the robust interval has the larger variance constant, so in small
  samples it can be longer than the conventional interval; with bandwidths
  chosen for correct coverage it is shorter for n large enough (CCT Remark 5,
  p. 2304; CCF 2020 §3.2, pp. 200–201). At one common h it is always the
  longer of the two (Cattaneo, Idrobo & Titiunik 2020, p. 65).
- Undersmoothing (a smaller h with the conventional interval) is a valid
  alternative in principle, but RBC's coverage error is never larger and is
  strictly smaller when the regression functions are smoother than the fit
  exploits (CCF 2018 pp. 767–768; CCF 2020 Theorem 3.1, p. 198). Ad hoc
  shrinkage of the MSE bandwidth was "no panacea" in CCF 2018's simulations
  (p. 778).

## 4. The coverage-error-optimal bandwidth

- At a boundary point, which is where the RD estimand sits, the CE-optimal
  bandwidth for the RBC interval has rate n^(−1/(p+3)), smaller than
  h_MSE ∝ n^(−1/(2p+3)) for every p ≥ 1 (CCF 2020 Theorem 3.2, p. 199;
  CCF 2018 p. 776; CCF 2022 p. 3010). The interior-point result that h_MSE is
  already rate-optimal for p = 1 (CCF 2018 p. 776; CCF 2022 pp. 3009–3010)
  does not carry over to the RD cutoff.
- RBC at h_MSE is valid but not CE-optimal; the papers' guidance is that the
  two bandwidths are complementary — h_MSE for the point estimate, h_CE for
  the interval (CCF 2020 p. 193; CCF 2022 pp. 3009–3010 endorse reporting
  the MSE-optimal point estimate with the RBC interval at the same h_MSE).
  CCFT 2017 says CER bandwidths "may be preferable in practice for inference
  purposes" (p. 381).
- Rule-of-thumb implementation: ĥ_CE = n^(−p/((2p+3)(p+3))) × ĥ_MSE. For p = 1
  that is n^(−1/20): a 27% shrink at n = 500 (CCF 2020 p. 202). A
  direct plug-in version also exists (pp. 202–203). The software article
  states the same rescaling for every selector type (CCFT 2017 p. 381).
- A coverage/length trade-off bandwidth (exponent between 1/(5+2p) and
  1/(3+p), researcher-chosen weight) is derived in CCF 2020 §4.3 and CCF
  2022 §4.1; the 2017 software article does not list it as a selector.
- Neither MSE- nor CE-optimal bandwidths may be used to choose a
  local-randomization window: "CE- and MSE-optimal bandwidth choices should
  not be used when the goal is to employ local" randomization (CCF 2020
  p. 194).

## 5. `rdrobust` as documented in the Stata Journal (2017)

- Syntax (p. 382): `c() p() q() deriv() fuzzy(var [sharpbw]) covs() kernel()
  weights() h(hL hR) b(bL bR) rho() scalepar() bwselect() scaleregul() vce()
  level() all`. If ρ is given, only h is selected and b = h/ρ (p. 383). The
  default-run output shows triangular kernel, p = 1, q = 2, mserd, NN
  variance (p. 392).
- Selectors (pp. 380–381, 383): `mserd` (one common MSE bandwidth for the RD
  estimator; default), `msetwo` (separate MSE bandwidths below and above),
  `msesum` (common bandwidth for the sum of the two one-sided estimates,
  which the authors say serves mainly for regularization, p. 380), `msecomb1` =
  min(mserd, msesum), `msecomb2` = side-wise median(msetwo, mserd, msesum);
  `cerrd`, `certwo`, `cersum`, `cercomb1`, `cercomb2` are the CER analogues.
  The authors single out mserd and msetwo for point estimation and cerrd and
  certwo for RBC intervals; the rest serve regularization and sensitivity
  (p. 400).
- In the `rdbwselect, all` illustration (p. 400) every CER selector has the
  same b as its MSE counterpart; only h is rescaled. Check: 17.708 ×
  1297^(−1/20) = 12.37, the printed cerrd value.
- Regularization (the Imbens–Kalyanaraman denominator term) is on by default
  and "always leads to smaller bandwidths"; `scaleregul(0)` removes it
  (p. 400).
- Variance (pp. 378–379, 384): `vce(nn 3)` is the default — a
  nearest-neighbour estimator with at least 3 neighbours; `hc0`–`hc3` use
  plug-in residuals; `nncluster var [J]` and `cluster var` are one-way
  cluster-robust versions. With mass points the NN estimator uses all
  equidistant neighbours, so ties change the SE relative to the 2014 version
  (pp. 379, 388). CCT found plug-in-residual SEs undercover more than NN SEs
  in simulation (p. 2315).
- `kernel(uniform) vce(cluster var)`: "This is the command that produces the
  closest results" to `regress` with clustering; `vce(hc1)` is the
  unclustered analogue (p. 401).
- Printed rows: the default output prints a Conventional row (coefficient,
  SE, z, p, CI) and a Robust row with z, p and CI but no coefficient or SE
  (pp. 392–399). The 2017 article lists `all` in the syntax without
  describing it; Cattaneo, Idrobo & Titiunik (2020, pp. 65–66) show that
  `all` adds the Bias-corrected row and prints the bias-corrected estimate
  and robust SE on the Robust row. Stored results used in the article:
  `e(tau_cl)`, `e(pv_rb)`, `e(ci_l_rb)`, `e(ci_r_rb)`, `e(h_l)`, `e(h_r)`,
  `e(b_l)`, `e(b_r)` (pp. 394, 397).
- Recovering the hidden robust quantities (inference from the printed rows):
  bias-corrected estimate = midpoint of the Robust CI; robust SE = CI
  half-width / 1.96; Robust z = midpoint / SE. On the default Senate run:
  midpoint 7.510, SE 1.743, z 4.31 — matching the printed 4.3095 (p. 392).
- Fuzzy: by default the bandwidth targets the ratio estimator when
  non-compliance is two-sided; otherwise, or with `sharpbw`, it targets the
  intention-to-treat numerator (p. 389). Kink: `deriv(1)`; fuzzy kink:
  `fuzzy() deriv(1)` (pp. 382, 401).
- Covariates enter a joint fit with a common coefficient on both sides; the
  adjusted estimator stays consistent only if the covariates have no jump at
  the cutoff (no derivative jump in kink designs), testable by running
  `rdrobust` with each covariate as outcome (pp. 376, 397). Adding covariates
  changes the bandwidth and, through missing values, the sample (1,297 to
  1,108 observations, pp. 394–396).
- Backward compatibility: `ik`, `cct` and `cv` selectors were removed;
  `mserd` upgrades ik and cct. `rdbwselect` is not backward compatible —
  the same Senate data give h = 17.708 under the 2016 code and 16.794 under
  the 2014 code; the old selector ships as `rdbwselect_2014` (pp. 381,
  388–389, 392–393).
- Not documented in the 2017 article: `masspoints`, `bwcheck`, `bwrestrict`,
  any option added after 2016, and what b defaults to when only h is
  supplied. Check the installed help for these.

## 6. What changes with clustering

- Theory: first-order RBC results extend to clustered sampling when each unit
  belongs to one of G clusters, G → ∞ and Gh → ∞ (CCF 2020 §5.2, p. 204).
  No higher-order (coverage error) result is proved for clustered data.
- Bandwidths: every selector, MSE and CER, is re-computed with the
  cluster-robust variance when a cluster variable is given (CCFT 2017
  pp. 379, 398). In the Senate example, `vce(nncluster state)` moved mserd
  from 17.708 to 17.509 — narrower — and widened the robust CI from
  [4.094, 10.926] to [4.091, 11.046] (p. 398).
- CER rule of thumb under clustering scales by the number of clusters:
  ȟ_CE = G^(−p/((2p+3)(p+3))) × ȟ_MSE, with ȟ_MSE the cluster-aware MSE
  bandwidth (CCF 2020 pp. 204–205). Because G < n the shrink factor is
  milder, so the clustered CER bandwidth is a larger fraction of its MSE
  base than the unclustered one is. The 2017 software article states the CER
  formula with n only (p. 381) and does not say whether the clustered
  implementation uses G. The package code does (package source, not the
  article): with a cluster variable, `rdbwselect` rescales the CER bandwidth
  by the total cluster count in place of n, in every release from 2.2 to
  4.1.1. The MSE base can still move either way when clustering is added.
- The output prints the number of clusters on each side (50/50 and 48/50 in
  the examples, pp. 398–399).
- Inference (not stated in the sources): because the bandwidth moves when
  the cluster option is added, a clustered and an unclustered SE from two
  default runs are computed on different windows; the comparison isolates
  the variance estimator only at fixed h and b.

## 7. What the sources say not to do

- Do not pair an MSE- or CE-optimal bandwidth with the conventional interval
  (CCT p. 2295; CCF 2020 pp. 196, 200).
- Do not re-centre the robust interval on τ̂(h), and do not form a test from
  τ̂(h) divided by the robust SE: the RBC statistic is (τ̂_bc − τ)/√V̂_bc
  (CCT Theorem 1, p. 2303; CCF 2020 p. 197).
- Do not use asymptotic-variance Studentization (CCF 2018 p. 774; CCF 2022
  p. 3003).
- Do not use MSE or CE bandwidths as local-randomization windows (CCF 2020
  p. 194).
- Do not apply the continuity framework unchanged to a running variable with
  few mass points (CCT Remark 1, p. 2299).

## Review use

- **Which number is the verdict.** Trigger: any `rdrobust`-style table. The
  headline is the conventional point estimate at h_MSE with the Robust row's
  CI and p-value. Stars computed from the Conventional row, or from τ̂(h)
  over the robust SE, are failures: the first is invalid at the bandwidth
  used, the second is not a test any of these papers defines. Cost: the
  significance claim must be re-read from the Robust row; if it is not
  printed, recompute it from the replication files.
- **Recover hidden robust quantities.** When a paper prints only the robust
  CI, compute the bias-corrected centre (midpoint) and robust SE (half-width
  / 1.96); a printed z or p inconsistent with them means the paper mixed
  rows.
- **CER runs.** A point estimate taken from a `cerrd`/`certwo` run is an
  undersmoothed estimate, not the MSE-optimal one; report it as such. The
  expected pattern is a point estimate from mserd/msetwo and an RBC interval
  at the same h_MSE, or at h_CE from a second run. Identify a CER bandwidth
  by its ratio to the MSE bandwidth: n^(−1/20) for p = 1 without clusters,
  with b unchanged.
- **Bandwidth grids.** When re-running at manual h values, pass b (or ρ)
  explicitly and record it; a grid that silently switches ρ is comparing
  different intervals. Report the Robust CI at each grid point, not the
  conventional one.
- **Local quadratic "robustness".** A local-quadratic interval at the
  linear MSE bandwidth is RBC with ρ = 1, not an independent check.
- **Bootstrap or ad hoc undersmoothing** offered as the fix for bias at an
  MSE bandwidth: the bootstrap inherits the bias (CCT Remark 6); ad hoc
  shrinkage carries no coverage guarantee. Ask for the RBC interval.
- **Clustering.** Count clusters on each side inside the window; few
  clusters within h undercut the G → ∞, Gh → ∞ condition and the clustered
  RBC interval. Compare clustered and unclustered SEs at fixed h and b
  before attributing a change to the variance estimator.
- **Replicating a paper's OLS RD.** A window regression with uniform weights
  and clustered SEs maps to `kernel(uniform) vce(cluster)` at the paper's h;
  its Robust row is then the RBC interval for the paper's own specification.
- **Software vintage.** Bandwidths from 2014-era code (`cct`, `ik`, `cv`,
  `rdbwselect_2014`) do not match current `mserd` on identical data. Any
  attempt to reproduce an unstated "optimal bandwidth" must sweep package
  version alongside selector, kernel, p, vce, covariates, regularization and
  fuzzy bandwidth target.
- **Discrete scores.** With few mass points, the RBC machinery is outside its
  assumptions; route to `kolesar_rothe_2018_discrete_rdd.md` and the
  local-randomization record, and never take the local-randomization window
  from an MSE or CER selector.
