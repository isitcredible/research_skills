# Software examples

These are implementation illustrations, not definitions of the checks. Confirm
syntax against the installed version, inspect the returned objects, and validate
the result on the reproduced anchor or a known test case.

**Find the estimand the estimator was built to produce — do not stop at the
default printout.** A specialized package usually exists to report a specific
quantity the ordinary output does not surface: `rd2d` reports a weighted
boundary average treatment effect, not just a per-point curve; `sensemakr`
reports a robustness value, not just a coefficient; `rwolf` reports a
dependence-adjusted p-value, not just the raw one. When a check hands off to a
named package, read enough of its method reference to know which returned object
is the quantity the reader needs, and extract THAT. Pasting the console default
and moving on is how the load-bearing number goes missing.

## Find the original application first

Infer the application from the package:

| Evidence | Likely application |
|---|---|
| `.do`, `.ado`, `.dta`, `.ster`, `.gph` | Stata |
| `.R`, `.Rmd`, `.Rproj`, `renv.lock` | R |
| `.m`, `.mat`, MATLAB project files | MATLAB |
| `.sas`, `.sas7bdat` | SAS |
| `.py`, notebooks, environment files | Python |
| `.jl`, `Project.toml`, `Manifest.toml` | Julia |

Confirm with the readme, launch scripts, logs, and saved output. Mixed-language
packages may require more than one application.

Search the local machine — beyond `PATH` — before translating. Examples:

```sh
type -a stata-mp stata-se stata 2>/dev/null
type -a R Rscript matlab python3 julia 2>/dev/null
```

On macOS, do not assume `stata`, `stata-mp`, or `matlab` are on the system `$PATH`. You must actively search for the installed application bundles and explicitly construct the path to the executable inside the `.app/Contents/MacOS/` directory. (Note that Stata is often installed in a subfolder like `/Applications/StataNow/StataSE.app`):

```sh
# 1. Find the application bundle
mdfind "kMDItemFSName == 'Stata*'c"
mdfind "kMDItemFSName == 'MATLAB*'c"
find /Applications ~/Applications -maxdepth 2 -name "Stata*.app" -o -name "MATLAB*.app" 2>/dev/null

# 2. Construct the explicit path and execute.
# Look inside the .app/Contents/MacOS/ directory for the CLI binary (e.g. stata-mp, stata-se, or MATLAB).
/Applications/StataNow/StataSE.app/Contents/MacOS/stata-se -b do script.do
/Applications/MATLAB_R2023b.app/Contents/MacOS/MATLAB -batch "run('script.m')"
```

On Windows PowerShell, inspect commands and common installation roots:

```powershell
Get-Command StataMP-64.exe, StataSE-64.exe, Stata-64.exe -ErrorAction SilentlyContinue
Get-ChildItem 'C:\Program Files' -Directory -Filter 'Stata*' -ErrorAction SilentlyContinue
```

Also inspect shell configuration, environment modules, package managers,
containers, and project-specific launch scripts. Record every location checked,
the selected executable, its version and edition, and license/access status.

Do not install or activate software without authorization. If the application
exists but the sandbox blocks execution, request permission to run the exact
executable. Use translation only after the native search is exhausted and
logged.

## Stata

### Assignment-level clustered inference

```stata
regress outcome treatment controls, vce(cluster assignment_id)
tab assignment_id
```

For fixed effects or IV, retain the authors' estimator where possible and change
only the inference level in the first pass.

### Few effective clusters (or few effective shocks): what to run, in this order

**YOUR DEFAULT IS WRONG HERE.** The reflex answer to "few clusters" is "wild cluster
bootstrap", and the reflex command is plain `boottest`. Plain `boottest` is WCR-C
(ordinary restricted residuals, CV1 t-statistic). When one cluster or one shock carries
most of the variation (G* of a handful, whatever the nominal G), its draws mostly
re-sign that one cluster, so its p-value can be far too small or far too large. Do not
quote it as the few-cluster answer. `../scripts/check_inference.py` fails any `boottest`
call without `jk`.

1. **Diagnose.** Compute partial leverages and G* for the coefficient (`summclust` in
   Stata does it, along with the delete-one-cluster estimates and CV3; or implement it
   directly, see `methods/mackinnon_nielsen_webb_2023_few_clusters.md`). Name the
   top-leverage clusters.
2. **Lead with the cluster jackknife (CV3)** and its delete-one-cluster estimates. Re-fit
   every control and every non-cluster FE in each leave-out. Report CV1 beside it: the
   CV1→CV3 gap is the leverage finding.

   ```stata
   * varlist: outcome, coefficient of interest, then the controls
   summclust y treatment controls, cluster(state) fevar(year) jackknife gstar table
   ```

3. **The restricted wild bootstrap, second, led by WCR-S:** `jk` jackknifes the
   bootstrap DGP (MacKinnon, Nielsen and Webb 2023).

   ```stata
   boottest treatment = 0, jk noci weight(webb) reps(9999) seed(20260723)   // WCR-S
   assert !missing(r(p))
   ```

   **`jk` is WCR-S only for a test of zero, and `noci` + `assert !missing(r(p))` are
   mandatory (`check_inference.py` F9/F10).** `boottest` 4.5.3 prints a confidence set
   by default for a single hypothesis (`noci` suppresses it) and adds an `X_g·t1` term
   to the jackknifed residual that vanishes only when the null value is 0, so
   `boottest x = b0, jk` with b0 ≠ 0, and any interval it inverts, is not MNW's WCR-S.
   Furthermore, `boottest …, ar` sets its bootstrap DGP to the model constraints only
   (`SetR(*pR1)`), running an unrestricted wild bootstrap even though its header prints
   "null imposed" (`check_inference.py` F8 fails any `boottest …, ar` without
   `AR-boottest-robustness`). For a nonzero null, or a confidence or Anderson–Rubin
   set, transform the outcome (`y − b0·x`, or `y − b0·endog` for AR), test the
   coefficient against 0 with `jk noci` at each grid point, and bisect the boundaries
   with a large B. Report p-values at zero from `jk noci`; never report boottest's own
   `jk` or `ar` interval as the primary set.

   R / Python: `fwildclusterboot::boottest(..., bootstrap_type = "31")`, or
   `wildboottest(..., bootstrap_type = "31")`. Unrestricted (`nonull`) and plain WCR-C
   are never cited alone as the result. Tag the call with the comment `WCU-robustness` or
   `WCR-C-robustness`. Always run WCR-C and report it beside WCR-S (MNW: compute
   both). Record the variant, the
   weights, B and the seed beside every bootstrap number, and name the variant every
   time the result is cited ("WCR-S p .03", never "WCR p .03").
4. **One or few treated clusters, or a shift-share design with few effective shocks:
   randomization inference** over the actual assignment (clusters, or the shocks across
   industries), with the permuted statistic named (studentized and raw). In a shift-share
   design the unit is the shock, not the region: a region-clustered test of any kind is
   not the few-shocks answer.
5. **IV with a weak or leverage-dependent first stage:** tF/VtF or a null-imposed AR set,
   built on the inputs above (CV3, or WCR-S for the AR form).

`boottest` may not attach to every estimator or absorbed fixed-effect configuration
(e.g. multiple or interacted absorbed FEs after `reghdfe`), and when it refuses it prints
a message but exits with `_rc = 0` and `r(p) = .` — always follow `boottest` with
`assert !missing(r(p))`. If it refuses an interacted FE specification, collapse each
interacted FE pair into a single group id (`egen fe_ab = group(a b)`), verify the point
estimate is unchanged, and re-run; otherwise use the jackknife or randomization and
record the substitution.

- **G\* by hand**: each cluster's partial leverage (its share of the residualised
  regressor's sum of squares), then `G* = 1 / Σ L_g²`.
- **CV3 by hand**: for each cluster g, re-estimate the full specification on the
  complement, *re-estimating absorbed fixed effects*, and form
  `((G−1)/G) Σ (b_(g) − b)²`. The FE re-estimation is mandatory.
- **tF / VtF**: grid the null value and invert. An unbounded set is the correct answer,
  not a bug.

### DiD robust estimators and pre-trend honesty

```stata
* Callaway–Sant'Anna (name the estimand and control group); long2 gives the
* common (universal) reference period HonestDiD needs
csdid y controls, ivar(unit) time(t) gvar(first_treated) method(dripw) long2
estat event, window(-5 4) estore(cs)   // estat simple for overall ATT
* Rambachan–Roth HonestDiD sensitivity on the stored event-study object
estimates restore cs
matrix list e(b)   // read positions: Pre_avg Post_avg Tm5..Tm2 Tp0..Tp4
honestdid, pre(3/6) post(7/11) mvec(0.5(0.5)2)   // breakdown M-bar
* Sun–Abraham / event-study interaction (control_cohort() is required per
* the package documentation; not run here)
eventstudyinteract y leads lags, vce(cluster unit) absorb(unit time) ///
    cohort(g) control_cohort(never_treated)
```

`pre()`/`post()` are positions in `e(b)`, not event times: read them from
`matrix list e(b)` for the window actually stored. After
`eventstudyinteract`, pass `b()` and `vcov()` to `honestdid` explicitly.

`pretrends` (R) computes the Roth pre-test power analysis from the
coefficient covariance of an event-study path. `did_imputation` (BJS) is the
imputation route; `did_multiplegt_dyn` covers non-absorbing treatment. State
which estimand and control-group convention each uses — they differ.

### Shift-share aggregation

```stata
* Shares are non-negative exposures summing to ~1
* Wide shares in memory (share101, share102, ... for shock ids 101, 102, ...):
ssaggregate y x [aw=w], n(shock_id) s(share)
* Long shares in a separate file indexed by location_id x shock_id:
ssaggregate y x [aw=w], n(shock_id) s(share) l(location_id) sfilename(shares.dta)
* controls() takes quoted sets, one per transformed copy:
*   controls("c1" "c1 c2")
```

`ssaggregate` requires non-negative shares — predicted shares are
signed and will fail or silently misbehave; the fallback is score aggregation
(sum the share-weighted shocks by hand) or a positive-weight collapse,
recorded as a documented substitution. For shock-level inference, the AKM variance on the
share-weighted shock collapse is asymptotic in the number of shocks: with few effective
shocks or one dominant shock it over-rejects (it can reject a true null a quarter of the
time or more). There, lead with the shock-level jackknife (delete one shock, and delete
one shock cluster) and randomization over the shocks, and keep AKM/AKM0 as the paper's
own number to be compared with them; `ivreghdfe` (not plain
`ivreg2`) is the vehicle when fixed effects are absorbed — name the command
used, the two print different auxiliary statistics.

A simple shared-treatment illustration is:

```stata
rwolf outcome1 outcome2 outcome3, indepvar(treatment) ///
    controls(control1 control2) reps(9999) seed(20260723)
```

Current `rwolf`/`rwolf2` syntax is more flexible than this illustration. Define
the family first and inspect which model, clustering, resampling, and null
options the installed command actually applies.

### Weak-instrument statistics (`ivreg2` and `weakivtest`)

`ivreg2`'s `e(widstat)` returns **Cragg–Donald** without a `vce` option and
**Kleibergen–Paap rk Wald F** under `robust`/`cluster()`/`bw()` — under a
clustered run it prints both, so read the printed label, not memory, before
naming the statistic in prose, and state which run a quoted F comes from when
table and prose replicate different commands. For the Montiel Olea–Pflueger
effective F (`weakivtest` after `ivreg2`), if the model absorbs fixed effects
via `ivreghdfe` and `weakivtest` refuses the post-estimation state, partial out
the absorbed fixed effects and exogenous controls from `y`, `x`, and `z` via
`reghdfe …, absorb(…) resid` and run `ivreg2` + `weakivtest` on the residuals
(or compute `F_eff` directly from the residualised first-stage regression).
`e()` may hold NO Anderson–Rubin
scalars: `di e(arfp)` can return missing silently rather than erroring — use
`weakiv` (`weakiv ivreg2 y (x = z), cluster(g) null(0)`, then `e(ar_p)`) for an
independent AR route. The reduced-form Wald F and `weakiv`'s LM chi2 are
different statistics and need not agree; with few clusters the
tie-breaker is the few-cluster machinery — CV3-based statistics first,
the restricted wild bootstrap second — not the asymptotic label.

### Leave-one-group-out

```stata
levelsof region_id, local(regions)
foreach r of local regions {
    quietly regress outcome treatment controls if region_id != `r', ///
        vce(cluster assignment_id)
    display "LOO,region_id,`r'," _b[treatment] "," _se[treatment] "," e(N)
}
```

Preserve the original sample rule inside each iteration and save results to a
table rather than relying on console history.

## R

### Cluster-robust covariance

Use the model class's supported clustered-covariance method, and verify its
small-sample and degrees-of-freedom conventions. For example, many `fixest`
models accept a cluster formula at estimation or summary time:

```r
fit <- fixest::feols(outcome ~ treatment + controls | fixed_effect,
                    data = d, cluster = ~assignment_id)
```

### Wild-cluster bootstrap (second instrument; WCR-S leads)

Read "Few effective clusters" in the Stata section first: lead with CV3 and G*. In R the
restricted wild bootstrap is run as WCR-S (`bootstrap_type = "31"`: jackknifed residuals in
the DGP, CV1 statistic; MacKinnon, Nielsen and Webb's "WCR31"). The package default
(`"fnw11"`) is WCR-C: always run it beside WCR-S, tag it
`WCR-C-robustness`, and never cite it alone.

```r
set.seed(20260723)
dqrng::dqset.seed(20260723)
boot <- fwildclusterboot::boottest(
  fit,
  clustid = "assignment_id",
  param = "treatment",
  B = 9999,
  type = "webb",
  impose_null = TRUE,
  bootstrap_type = "31"   # WCR-S
)
```

Package availability and argument names vary by version and installation source. The
current R implementation uses a separate `dqrng` seed for Webb weights under its default
engine. Confirm the installed documentation and record the engine, the bootstrap type
(WCR-S), and whether the null is imposed. Python: `wildboottest(model, param=...,
cluster=..., B=9999, bootstrap_type="31")`.

### Holm correction

```r
adjusted <- p.adjust(unadjusted_p_values, method = "holm")
```

Holm requires the full, predeclared family of raw p-values. It does not reproduce
a dependence-aware Romano–Wolf resampling scheme.

### Local-randomization RD

For a running variable with few mass points near the cutoff, or a paper that
reads its design as a local experiment, `rdlocrand` runs finite-sample
randomization inference in a window around the cutoff. Use version 3.0 or
later: 1.1 and 2.0 select windows with an indexing bug.

```r
library(rdlocrand)
# Z holds predetermined covariates used to pick the window by balance.
# wobs = observations added per side at each step; small steps avoid
# stepping past the largest balanced window.
win <- rdwinselect(R, Z, wobs = 2, seed = 20260803)   # default level 0.15
str(win)                                              # check the window fields
wl <- win$w_left; wr <- win$w_right
stopifnot(is.numeric(wl), is.numeric(wr))             # never fall back to the full range
grid <- seq(-20, 20, by = 0.25)
ri <- rdrandinf(Y, R, wl = wl, wr = wr, seed = 20260803,
                ci = c(0.05, grid))                   # alpha, then an effect grid wide enough not to truncate
ri$p.value      # Fisherian p, sharp null (NA for p > 0 polynomial fits in 3.0)
ri$asy.pvalue   # large-sample p, average-effect null
ri$ci           # inverts sharp nulls under a constant additive effect
stopifnot(ri$ci[1] > min(grid), ri$ci[2] < max(grid)) # guard against CI clamping to grid boundary
# Bernoulli assignment: pass a length-N vector of unit probabilities
# (1/2 inside the window, NA outside); fixed margins is the default.
# Sensitivity in windows inside the selected one, effect grid around the estimate:
rdsensitivity(Y, R, wlist = seq(wr / 2, wr, length.out = 5),
              tlist = seq(-10, 10, 1) + ri$obs.stat, seed = 20260803)
# Hidden bias inside the window (bounds the sharp-null p-value, not the effect):
rdrbounds(Y, R, expgamma = c(1.5, 2, 2.5, 3), wlist = seq(wr / 2, wr, length.out = 5),
          fmpval = TRUE, seed = 20260803)
```

Check that the observation counts `rdrandinf` prints match the window. Report
the randomization results beside the continuity-based estimate, each labelled
with its estimand: θ, the average effect in the window, against τ, the effect
at the cutoff. `rdrbounds` defaults to the rank-sum statistic, not the
difference in means. Record the seed, the statistic and the mechanism.

### Boundary discontinuity design

For a geographic boundary or a two-dimensional score, `rd2d` (Cattaneo,
Titiunik, and Yu) estimates the boundary effect curve and aggregates of it:

- **BATEC** — the boundary effect *curve*: one estimate per evaluation point,
  with pointwise intervals and a uniform confidence band over the whole curve.
  Claims about where the effect is present or larger are judged on the band.
- **WBATE** — a *weighted boundary average treatment effect*. A pooled
  distance-to-border local difference in means (or a treatment-interacted
  pooled regression) targets the density-weighted average of the curve, so
  the like-for-like WBATE weights each grid point by the observations near
  it; equal weights give a different average. A common-coefficient regression
  with segment fixed effects has its own implicit weights.
- **LBATE** — the *largest* boundary average effect, for a "the effect is
  biggest where…" claim.

Location-based `rd2d` and distance-based `rd2d.distance` target the same
curve with different estimators; distance-based estimates near a kink or
corner of the border carry first-order bias, so a gap between the two is a
diagnostic, not a second estimand.

```r
library(rd2d)
# Project coordinates first (Euclidean distance on raw lat/lon is wrong).
# X: bivariate score (two columns); assignment: 0/1;
# b: J x 2 evaluation points spaced by arc length, including the border's
#    kinks and corners, only where both sides have data.
est <- rd2d(Y, X, assignment, b, params.cov = "main",
            vce = "hc1", cluster = clusterid)    # rd2d: with cluster, vce must be hc0/hc1
m <- est$main                                    # per point: estimate.p, ci, h01..h12, N.Co, N.Tr
w_dens <- m$N.Co + m$N.Tr                        # density-type weights (normalised internally)
ss <- summary(est, output = "main", WBATE = w_dens, LBATE = TRUE, cbands = "main")
ss$tables$main    # per-point BATEC rows, then WBATE and LBATE rows
ss$cbands$main    # uniform band; empty unless cbands= is passed
summary(est, output = "main", WBATE = rep(1, nrow(b)))   # equal-weight WBATE, labelled as such
# summary() stops with an error if params.cov was not stored at fit time.
# The WBATE interval is centred on the bias-corrected aggregate: the printed
# point can lie outside it. Quote both as printed.
#
# Covariate balance along the border at each covariate's own bandwidths,
# then at the outcome's as a labelled supplement:
#   rd2d(Z1, X, assignment, b, params.cov = "main")
#   rd2d(Z1, X, assignment, b, h = as.matrix(m[, c("h01","h02","h11","h12")]))
#
# Distance-based fit: D must be N x J signed distances to EACH evaluation point
# in b (NOT one nearest-boundary distance recycled J times, which runs silently).
# Non-negative = treated side. cbands = TRUE is the default and stores the
# covariance; bandwidth columns are h0, h1. Set the kink options on a kinked border.
#   est_d <- rd2d.distance(Y, D, b = b, vce = "hc1", cluster = clusterid)
#   summary(est_d, output = "main", WBATE = w_dens, cbands = "main")
# rdbw2d / rdbw2d.distance expose bandwidth selection; plot() draws the curve
# with its band; vcov() returns the stored covariance for custom aggregates.
```

**`rd2d` is not a heterogeneity plot.** Completing the boundary record means:
(1) a WBATE with stated weights and RBC inference, the aggregate set against
the paper's pooled border effect; (2) the BATEC curve with a uniform band;
(3) LBATE only if a largest-effect claim is at stake. A report that leads with
the min/max of `estimate.p` and never prints a WBATE row has not finished the
check. A hand average of `estimate.p` reproduces the equal-weight point but
has no valid standard error; never report it. If the band is missing, repair
it or record BLOCKED with command proof; the stage stays INTERIM only while an
untried repair remains.

### Omitted-variable-bias sensitivity (Cinelli–Hazlett robustness values)

`sensemakr` computes the robustness value — how strong an unobserved confounder
would have to be, benchmarked against named observed covariates, to overturn a
selection-on-observables claim:

```r
library(sensemakr)
fit <- lm(y ~ d + x1 + x2, data = df)
s <- sensemakr(fit, treatment = "d", benchmark_covariates = "x1", kd = 1)
robustness_value(fit, covariates = "d")   # defaults to q = 1, alpha = 0.05 (RV_qa: 95% CI to zero; alpha = 1 for point null)
sensitivity_stats(fit, treatment = "d")   # rv_q, rv_qa, r2yd.x
ovb_minimal_reporting(s)                   # the standard reporting table
```

`sensemakr` has methods for `lm` and `fixest`; confirm which the installed
version supports. For instrumental variables, `iv.sensemakr` runs the same
framework on the instrument's exogeneity and exclusion:

```r
library(iv.sensemakr)
# x MUST be a numeric matrix WITH column names; iv_fit errors on an unnamed
# matrix (a colname-assignment bug), so pass, e.g.,
#   x <- matrix(cbind(x1, x2), ncol = 2, dimnames = list(NULL, c("x1", "x2")))
ivf <- iv_fit(y = y, d = d, z = z, x = x)
sensemakr(ivf)
sensitivity_stats(ivf)   # rv_qa, and xrv_qa (extreme robustness value)
```

A robustness value is not a verdict: it states how strong unobserved confounding
— of the treatment, or of the instrument — would have to be to move the estimate
to the null. Report it beside the observed-covariate benchmark, never alone.

## Python

### Cluster-robust covariance

For a supported `statsmodels` result:

```python
clustered = fitted.get_robustcov_results(
    cov_type="cluster",
    groups=data["assignment_id"],
    use_correction=True,
    df_correction=True,
)
```

Inspect the installed version's handling of degrees of freedom and model class.

### Holm correction

```python
from statsmodels.stats.multitest import multipletests

rejected, adjusted, _, _ = multipletests(
    unadjusted_p_values,
    alpha=0.05,
    method="holm",
)
```

Do not present Holm as Romano–Wolf: it controls the family-wise error rate by a
different procedure and does not exploit dependence through resampling.

## Spatial dependence

### Müller–Watson SCPC and spatial unit roots (SPUR)

Müller–Watson spatial-correlation-robust inference (SCPC) and their spatial unit-root and spurious-regression tests (Müller–Watson 2024, *Econometrica*), as ported to Stata by Becker–Boll–Voth (2026, *Stata Journal*) in the SPUR package.

**Stata:** Use the community `spur` and `scpc` commands.
```stata
* SPUR expects coordinate variables named s_1 (lat) and s_2 (lon); use latlong for spherical distances
rename lat s_1
rename lon s_2
spur y x controls, latlong
```
Note: `scpc` requires the preceding estimation to be run with `robust` or `cluster()` (without a sandwich VCE Stata does not store `e(V_modelbased)` and `scpc` aborts with `e(V_modelbased) missing; aborting`), while running `scpc` on the LBM-GLS transformed model from `spurtransform` gives contrast-space SCPC (C-SCPC, the $h \to \infty$ benchmark).

**R:** Interfaces checked with `spuR` 0.1.2 and `scpcR` 0.1.3. Record installed versions and consult their [spuR reference](https://spatial-spur.github.io/spuR/reference/) and [scpcR reference](https://spatial-spur.github.io/scpcR/reference/) when they differ. Use a common complete-case sample. Coordinates are column names in `d`, not an unnamed positional matrix.
```r
fmla <- y ~ x + z
fit <- lm(fmla, data = d)
scpc_res <- scpcR::scpc(fit, data = d, lon = "lon", lat = "lat", avc = 0.03)
# Repeat SCPC over the justified avc grid and save each result.
res <- spuR::spur(fmla, data = d, lon = "lon", lat = "lat",
                  q = 15L, nrep = 100000L, seed = 42L, avc = 0.03)
# res$tests contains SPUR integration tests; res$fits contains levels and
# transformed fits, including their SCPC results. Label the branches separately.
```
For projected coordinates use `coords_euclidean = c("X", "Y")` instead of lon/lat. SPUR integration diagnostics and SCPC coefficient inference are separate procedures; a failure of one call does not justify silently replacing the other. Record any transformation and its implications for the estimated relationship.

### Kelly (2019) Spatial Noise Placebo

Uses `spatInfer` ([author tutorial](https://morganwkelly.github.io/spatInfer_tutor/tutorial.html)); interfaces checked with 0.1.0. The estimation frame needs coordinate columns named **X and Y**, in a recorded, appropriate spatial coordinate system. The focal regressor comes first in the formula. `optimal_basis` returns a **plot**; read its BIC selection subtitle and record the chosen spline/PC counts, rather than passing that plot to `placebo`.

**R:**
```r
fmla <- y ~ x + z
basis_plot <- spatInfer::optimal_basis(fmla, d, max_splines = 5)
print(basis_plot)  # save this plot; record its selected counts
# This callable runner takes the counts read from that selection record.
run_kelly <- function(d, selected_splines, selected_pcs, n_sim = 1000L) {
  fmla <- y ~ x + z
  set.seed(20260723)
  bch <- spatInfer::placebo(fmla, d, splines = selected_splines,
    pc_num = selected_pcs, nSim = n_sim,
    exact_cholesky = FALSE, Parallel = FALSE)
  set.seed(20260723)
  im <- spatInfer::placebo_im(fmla, d, splines = selected_splines,
    pc_num = selected_pcs, nSim = n_sim,
    exact_cholesky = FALSE, Parallel = FALSE)
  list(bch = bch, im = im)
}
# run_kelly(d, selected_splines = <recorded count>, selected_pcs = <recorded count>)
```
`Parallel = FALSE` avoids headless core-detection problems. The approximate decomposition (`exact_cholesky = FALSE`) is a recorded numerical choice that can help larger runs; assess sensitivity where feasible, rather than claiming a universal size threshold for crashes. BCH and Ibragimov–Müller inference rely on different assumptions. Neither has universally guaranteed size or power: report cluster counts, noise calibration, simulation uncertainty, and the actual method/returned fields, rather than inheriting a printed label. Use production simulation counts for conclusions; a reduced-count smoke run checks the interface only.

### Conley-Kelly-Kozbur (2026) Spatial Pre-Whitening

The helper `../assets/prewhiten.R` selects PCs of a linear tensor spline basis by nearest-neighbour residual correlation, inspired by Section 5 of Conley, Kelly & Kozbur **UCD working paper WP26/11 (2026)**. It does not compute HAC or certify its coverage. The paper's target is inference; finite-sample correlation with the spatial basis can reduce identifying variation. Compare coefficient movement, SE changes, and retained variation; movement alone is not evidence of confounding.

**Geometry and bandwidth:** supply projected planar coordinates in common units for the spline and nearest-neighbour calculations. R `bs(df=...)` uses quantile internal knots ([R documentation](https://stat.ethz.ch/R-manual/R-devel/library/splines/html/bs.html)). The helper returns the actual knot vectors and raw support widths; for degree one, each raw spline spans t[j+2] − t[j]. The tensor support bound combines the two axis widths by Euclidean distance. Uniform-gap approximations are invalid for these knots. Moreover, PC mixtures may span the whole domain: the raw spline bound is **not** an automatic cutoff for the augmented model. Establish the support of the actual basis and use the same metric/units when checking the paper's Condition 6. If the practical PC implementation is not covered by that condition, say so and report empirical sensitivity; do not advertise theorem-guaranteed coverage. Keep projected distances and geodesic HAC units distinct and document their relationship.

**R:** This runner accepts an explicitly chosen kilometre cutoff grid, whose justification and support assessment belong in the report. `d` contains y, x, z, projected X/Y and geographical lon/lat on the same complete-case sample. The helper path is resolved relative to this skill's directory by the caller.
```r
run_ckk <- function(d, prewhiten_path, cutoffs_km) {
  stopifnot(length(cutoffs_km) > 0, all(is.finite(cutoffs_km)), all(cutoffs_km > 0))
  source(prewhiten_path, local = TRUE)
  pw <- spatial_prewhiten(d$y, cbind(d$x, d$z), d[c("X", "Y")])
  aug <- cbind(d, pw$PCs)
  fmla_aug <- reformulate(c("x", "z", colnames(pw$PCs)), response = "y")
  baseline <- fixest::feols(y ~ x + z, data = d)
  fit <- fixest::feols(fmla_aug, data = aug)
  covariances <- lapply(cutoffs_km, function(cutoff) {
    # fixest's Conley kernel is uniform, and vcov_fix = TRUE (default)
    # eigen-repairs a non-PSD matrix: match the paper's kernel (e.g.
    # conleyreg's bartlett) and report when the repair triggers.
    fixest::vcov_conley(fit, lat = "lat", lon = "lon", cutoff = cutoff)
  })
  list(baseline = baseline, augmented = fit, selection = pw,
       cutoffs_km = cutoffs_km, covariances = covariances)
}
```
Save the selection curve, knot/support metadata, ranks and residual degrees of freedom, plus the original and augmented estimates and HAC intervals at each cutoff. The helper caps candidates by realized rank and residual degrees of freedom; this safeguard is an implementation choice to record, not a claim that every returned basis satisfies the paper's asymptotic conditions.

### Spatial implementation gotchas (field notes)

- **`spatInfer` is GitHub-only** (`morganwkelly/spatInfer`), NOT CRAN — pin the
  commit; dated CRAN snapshots in rocker images lack it. `placebo()` is
  stochastic beyond a single `set.seed` — **reset the seed immediately before
  each call**. `Parallel = FALSE` headless (`detectCores()` returns NA under
  sandbox and `mc.cores` is computed inside the function — setting
  `options(mc.cores=)` does not fix it). `exact_cholesky = FALSE` beyond a few
  hundred obs — the exact Cholesky of the full covariance can segfault R with
  no catchable error. `prin_comp`/`generate_clusters` are unexported
  (`spatInfer:::`). At small N (~44) the BCH bootstrap is the noisiest of the
  battery — report the spread across spline/cluster settings and runs; never
  cherry-pick a cell.
- **`conleyreg` (R):** `ncores = 1` is mandatory headless (fixest nthreads=NA
  crash otherwise). It returns a `coeftest` matrix — index `r["x","t value"]`
  directly, not `coef(summary())`. Cross-checkable to 3dp against a hand-rolled
  Bartlett spatial-HAC sandwich and Stata `acreg ..., latitude() longitude()
  dist(km) bartlett spatial`.
- **`acreg` distance convention:** with `latitude()`/`longitude()` it computes
  an asymmetric local approximation — 111·Δlat and 111·cos(origin lat)·Δlon —
  not haversine; mirror it in any reconstruction or the cutoff-edge rows will
  look wrong. Near the domain-size cutoff the covariance goes non-positive-
  definite and `acreg` returns nothing (see the spatial record's FOC note).
- **Cutoff scale:** the Conley cutoff must reach the treatment unit's spatial
  scale — for ancestral-homeland treatments (~200 km) run a ladder to
  500–1000 km, not 100–200 km; for continental fields, out to the field's
  correlation range.
- **Centroids:** use real *signed* centroids — `rnaturalearth` +
  `sf::st_centroid` with `sf_use_s2(FALSE)`; beware sources giving ABSOLUTE
  latitude (useless south of the equator) and integer-rounded centroid files
  (collision risk on low-frequency-cosine procedures).
- **SPUR/SCPC R ports** (`spuR`, `scpcR`, github.com/spatial-spur): verified
  against the Stata `spur` implementation. `scpc()` consumes a
  platform-dependent number of RNG draws — pin `set.seed` immediately before
  every stochastic arm. Residual tests use full-LAPACK eigen on rep-specific
  matrices, so BLAS flavour (Accelerate vs OpenBLAS) shifts a small-nrep MC
  p by ~.01 — run a whole battery on ONE platform. spuR/Stata great-circle
  "distance" is central angle/(2π); km = d·2π·6371.000009. At small N a
  saturated spec over-parameterises `spurtest` — run parsimonious specs; SCPC
  on the raw OLS model can abort (`e(V_modelbased)` missing) — use SCPC on
  the LBM-GLS-transformed model.

## Time-series unit-root and cointegration battery

For `time-series-diagnostics`. The one rule that trips everyone: **cointegration
residual tests use their OWN response-surface critical values (MacKinnon /
Phillips–Ouliaris / Shin), never the ordinary ADF or `ur.kpss` tables** — those
use the wrong reference distribution and can misstate rejection rates. Preserve the paper's sample, spacing,
deterministics, and lags; a non-consecutive "annual" series breaks every method
below.

**R** (`urca`, `tseries`, `dynlm`, `ARDL`, `po.test`):
```r
library(urca); library(tseries); library(ARDL)
# 1. Integration order — opposite nulls, levels and first differences
pmax <- floor(12 * (length(y) / 100)^0.25)   # without lags=, AIC searches only 1 lag
summary(ur.df(y, type = "trend", lags = pmax, selectlags = "AIC"))  # H0: unit root; never tries 0 lags
summary(ur.pp(y, type = "Z-tau", model = "trend"))       # H0: unit root
summary(ur.kpss(y, type = "tau"))                        # H0: trend-stationarity
summary(ur.za(y, model = "both"))                        # one endogenous break
# 2. Cointegration
#   Engle–Granger: fit levels, then ADF the residual with MacKinnon co-int CVs
eg <- lm(y ~ x); e <- resid(eg)
adf_eg <- ur.df(e, type = "none", lags = floor(12 * (length(e) / 100)^0.25),
                selectlags = "AIC")
#     compare to MacKinnon cointegration response surfaces (urca's internal
#     table is MacKinnon 1996), NOT the
#     ur.df printout's unit-root CVs and NOT urca::punitroot (niv = 1, unit-root
#     values). The internal (unexported) urca function gives the p-value:
#     urca:::.urcval(arg = adf_eg@teststat[1], nobs = length(e),
#                    niv = <variables in the cointegrating regression>,
#                    itt = 1, itv = 2, nc = 2)
po.test(cbind(y, x))                                     # Phillips–Ouliaris (tseries)
summary(ca.jo(cbind(y, x), type = "trace", ecdet = "trend", K = 2))  # Johansen
# 3. Order-agnostic bounds (Pesaran–Shin–Smith)
m    <- ardl(y ~ x, data = d, order = c(2, 2))
bt_f <- bounds_f_test(m, case = 3); bt_f                 # F vs I(0)/I(1) bounds
bt_t <- bounds_t_test(m, case = 3); bt_t                 # t vs I(0)/I(1) bounds (Cases 1, 3, 5; t < t_U < 0)
# 4. Prais–Winsten AR(1) FGLS  (report rho, coef before/after, DW)
library(prais); summary(prais_winsten(y ~ x, data = d, index = "year"))
# Durbin–Watson beside R² for every levels spec:
library(lmtest); dwtest(eg)
```
Shin's reversed-null (H0 = cointegration) has no clean CRAN one-liner: estimate
the cointegrating vector by Stock–Watson DOLS (`dynlm` with leads/lags of Δx),
compute a KPSS-type statistic on the DOLS residuals, and compare to **Shin (1994)
critical values** for the number of stochastic regressors — not `ur.kpss` values.
Gregory–Hansen / Maki break-robust cointegration: `gregory.hansen` /
`maki.cointegration` in `github.com/…` community packages, or hand-code with
recomputed CVs.

**Stata:**
```stata
dfuller y, trend lags(2)           // H0: unit root (ADF)
pperron y, trend                   // H0: unit root (Phillips–Perron)
kpss y, trend                      // H0: stationarity (reversed null)
dfgls y                            // ADF-GLS, efficient at short T
zandrews y, break(both)            // one endogenous break
egranger y x, trend                // Engle–Granger (community egranger)
vecrank y x, trend(trend) lags(2)  // Johansen trace rank
ardl y x, lags(2 2) ec             // ARDL/ECM; -estat ectest- for bounds
prais y x, rhotype(regress)        // Prais–Winsten; prints original and
                                   // transformed DW itself (estat dwatson fails)
```

**Short-T discipline (T ≲ 40) — do NOT skip.** Before citing any non-rejection,
run a calibrated size/power Monte Carlo at the actual T (seed once at the top,
report the full grid). No-cointegration tests can have ~1% power at short T — an
underpowered non-rejection is *no evidence*. Shin is not uniformly conservative —
undersized at short T with weak persistence, oversized at high residual
persistence — so weigh a rejection only against the size Monte Carlo at the
data's own ρ̂. Engle–Granger without trend is oversized on drifting
series. Minimizing a fit residual does not guarantee stationarity. Residual-based cointegration tests need critical values that account for fitting and, where applicable, selection; calibrate the full fitting procedure if standard tables do not cover it. Under cross-sectional dependence use Pesaran CIPS
(`xtcips` / `pescadf`), not first-generation `xtunitroot` tests.

## Variance decomposition (Shapley / LMG only)

The variance-explained dimension is Shapley values. Do not substitute
partial R², nested ΔR², or η² — those are different statistics (and partial R²
belongs only in the OVB-sensitivity record).

**Named software.** R's `relaimpo` computes LMG/Shapley shares for linear models:

```r
relaimpo::calc.relimp(fit, type = "lmg", rela = FALSE)
```

`rela = FALSE` reports shares of total variance (they sum to the model R²);
`rela = TRUE` rescales to shares of explained variance — if reported, label it
as such. `domir` generalizes dominance analysis to other model classes and
custom fit statistics, which is one route to grouped/block decompositions.
Stata's community `shapley2` covers the basic case.

**Other environments.** If you are working in Python, Julia, or any stack without
these packages, replicate the LMG/Shapley approach yourself: for each regressor
(or named block), average its incremental R² over all orderings in which it can
enter the model (equivalently, weight each subset S of the other p−1 blocks by |S|! (p−|S|−1)! / p!). An unweighted average over subsets is not generally Shapley/LMG. Record
that you hand-coded the decomposition and reconcile against a known case when
possible. Missing named software is not a license to report partial R², nested
ΔR², or η² as the share.

Packaged decompositions — in any language — often ignore or mishandle analytic
weights and fixed effects: for weighted specifications, hand-code the weighted
decomposition over block subsets and reconcile before reporting; for fixed
effects, either include the FE as an explicit block or decompose the
within-transformed data, and state which you did. Within shares sum to within R². To express them against original total outcome variance, scale by SST_within/SST_original with the same weights and sample, accounting separately for the FE contribution.

If no Shapley/LMG implementation can be run or reimplemented for the estimator,
mark the check `NOT_RUN` — do not invent a PROXY from
`R²_full − R²_without_focal`.

## Regression-discontinuity package suite (Cattaneo et al.)

`rdlocrand` (local randomization) and `rd2d` (boundary designs) are covered
above. The rest of the RD suite — all at `rdpackages.github.io`, with R,
Stata, and Python builds — fills the other checks the RD module mandates. Match
the paper's cutoff, kernel, covariates and clustering; these are
illustrations, not the check. Record `packageVersion()` for every package
run: `rdrobust` 4.0.0 moved the `all`/`detail` switches to `summary()`,
remapped clustered variances and removed `rdbwselect_2014`; 4.1.1 changed
bandwidth-selection defaults. Prebuilt binaries can lag the source release —
check the version after installing. Current `rdpower` and `rdhte` require
`rdrobust` ≥ 4.0.0.

**`rdrobust` — the continuity estimate and which row carries it.** Report
the conventional point estimate at the MSE-optimal bandwidth with the robust
bias-corrected (RBC) interval, plus the RBC interval at the CER-optimal
bandwidth.

```r
library(rdrobust)
f <- rdrobust(y, x, c = 0, kernel = "triangular", p = 1, bwselect = "mserd")
summary(f)              # rdrobust >= 4.0.0: one row = conventional point + robust z/p/CI
summary(f, all = TRUE)  # Conventional / Bias-Corrected / Robust  (<= 3.0.0: rdrobust(..., all = TRUE))
f$coef; f$se; f$pv; f$ci   # rows 1-3 = Conventional, Bias-Corrected, Robust (all versions)
f$bws                      # h and b, left and right
summary(rdrobust(y, x, c = 0, bwselect = "cerrd"))   # RBC interval at the CER-optimal h
rdbwselect(y, x, c = 0, all = TRUE)                  # the ten MSE and CER selectors, one p
# Sensitivity: hCER, hMSE, 2*hCER, 2*hMSE, and p = 2; pass b (or rho) whenever h is set:
h <- f$bws[1, 1]; b <- f$bws[2, 1]
summary(rdrobust(y, x, c = 0, h = 2 * h, b = 2 * b))
# Covariate-adjusted fit (bandwidth and RBC inference re-selected with Z):
summary(rdrobust(y, x, c = 0, covs = Z))
# Balance test for covariate j at its own bandwidth, then at the headline's:
summary(rdrobust(Z[, j], x, c = 0, bwselect = "cerrd"))
summary(rdrobust(Z[, j], x, c = 0, h = h, b = b))
# Clustered: in >= 4.0.0 name the cluster estimator ("cr1", "cr2", "cr3");
# "nn"/"hc0"/"hc1" are remapped to CR1 (<= 3.0.0 used "nn" or "hc1" with cluster=)
summary(rdrobust(y, x, c = 0, cluster = g, vce = "cr1"))
# Fuzzy: one bandwidth for the ratio; first stage first
summary(rdrobust(d, x, c = 0)); summary(rdrobust(y, x, c = 0, fuzzy = d))
# Kink: slope change scaled by the policy slope change; set p explicitly
summary(rdrobust(y, x, c = 0, deriv = 1, p = 2, scalepar = 1 / kink_size))
# A paper's window regression with clustered SEs, at its own h (and b / rho = 1):
summary(rdrobust(y, x, c = 0, h = h_paper, b = b_paper, kernel = "uniform", vce = "cr1", cluster = g))
```
Stata: `rdrobust y x, c(0) p(1) kernel(triangular)` · `rdbwselect y x, all` ·
`rdrobust y x, covs(z1 z2)` · `rdrobust y x, fuzzy(d)` · `rdrobust y x, deriv(1) p(2)`.
`vcov()` on an `rdrobust` fit is diagonal with placeholder zeros; never use it
to test one row against another.

**`rdplot` — the RD plot.** The default line is a *global* order-4 polynomial
over the full support with uniform weights, on evenly spaced
mimicking-variance bins; it is not the local fit behind the estimate.

```r
rdplot(y, x, c = 0)                       # default: ES bins, mimicking-variance count, global quartic
rdplot(y, x, c = 0, binselect = "es")     # IMSE-optimal ES bins: means trace the regression function
rdplot(y, x, c = 0, binselect = "qsmv")   # quantile-spaced bins: also shows where the score is sparse
rdplot(y, x, c = 0, p = 1, h = h, kernel = "triangular",
       subset = abs(x) <= h)              # local linear fit inside the estimation window
plot(f, y, x)                             # rdrobust >= 4.0.0: local fit with conventional bands
```
For binary outcomes the spacings-based bin selectors do not apply; use the
polynomial-based variants and confirm them in the help. Bin confidence
intervals need mimicking-variance or undersmoothed bins.

**`rddensity` — the manipulation test at the cutoff.** Successor to the
McCrary test: no pre-binning, and robust bias-corrected inference valid at
the data-driven bandwidth. Quote the Robust row only.

```r
library(rddensity)
r <- rddensity(X = x, c = 0)    # mass-point adjustment and binomial tests on by default
summary(r)                      # robust T and p, bandwidths, effective N per side, binomial table
r$hat$left; r$hat$right         # density estimates; manipulation share 1 - left/right
2.80 * r$sd_jk$diff             # detectable density jump at 80% power, two-sided 5%
rdplotdensity(r, X = x)
summary(rddensity(X = x, c = 0, fitselect = "restricted"))  # power gain only under its restriction
```
Stata: `rddensity x, c(0)` · `rdbwdensity x, c(0)`.

**`rdbounds` — manipulation-robust bounds (Gerard, Rokkanen and Rothe).**
The authors' implementation, in R and Stata, from
`github.com/francoisgerard/rdbounds` (version 1.01, 2019, described by its
authors as preliminary; not on CRAN). It estimates the manipulation share,
the sharp and fuzzy bounds, and bootstrap confidence intervals, including at
fixed assumed shares for the breakdown exercise. Stata (requires `moremata`):

```stata
net install rdbounds, from(https://raw.githubusercontent.com/francoisgerard/rdbounds/master/Stata/)
rdbounds y x, c(0) treatment(d) bwsx(.2, .5) bwy(.1) orders(1) ///
    kernel(triangular) type(ate) potential_taus(.025 .05 .1 .2) num_bootstraps(500)
```
Read the option list in its help before running (bandwidths for the density
and the outcome are set separately), record the version, and report the
estimated share with its interval, the bounds with their interval, and the
breakdown share.

**`rdpower` — RD power and minimum detectable effect.** For continuity-based
RD estimates; set the paper's own specification, because the defaults
re-select an `mserd` bandwidth with the nearest-neighbour variance, no
covariates and no clustering.

```r
library(rdpower)
rdmde(data = cbind(Y, R), h = h_paper, p = 1, kernel = "triangular",
      covs = Z, vce = "cr1", cluster = g)          # MDE at power beta = 0.8, alpha = 0.05
rdpower(data = cbind(Y, R), tau = tau_A, h = h_paper)  # tau_A fixed from outside the data,
                                                       # never the paper's own estimate
rdsampsi(data = cbind(Y, R), tau = tau_A)          # design-stage sample size
```
`beta` is power, not the type-II error rate. `rdpower` 3.0 passes its own
defaults to `rdrobust` (e.g. `stdvars = FALSE`); set them to match the
estimate you are assessing. Stata: install from rdpackages
(`net install rdpower, from(https://raw.githubusercontent.com/rdpackages/rdpower/main/stata) replace`);
`ssc install rdpower` installs an unrelated power package. The 2019 Stata
Journal article's command is `rdpow`; the current release adds `rdpower`
(a wrapper) and `rdmde`.

**`rdmulti` — multiple cutoffs or multiple scores.** The pooled estimate is a
weighted average of cutoff-specific effects; report the weights and the
cutoff-specific estimates beside it.

```r
library(rdmulti)
out <- rdmc(Y, X, C)     # C = the per-unit cutoff each unit faces
out$W                    # pooling weights
out$B; out$V             # bias-corrected estimates and robust variances: use these for
                         # cross-cutoff tests, not the printed (conventional) Coef.
rdmcplot(Y, X, C)        # binned plot with per-cutoff fits
# Cumulative cutoffs: cvec = the distinct cutoffs, e.g. c(33, 66); restrict each
# cutoff's sample to the range between its neighbours (rangemat); xnorm adds a pooled row.
rdms(Y, X, cvec, rangemat = rng, xnorm = Xnorm)
# The article's pooled route: assign each unit to its nearest cutoff, then rdmc.
# Two scores: boundary points (cvec1[j], cvec2[j]); zvar = treatment indicator.
rdms(Y, X1, cvec1, X2 = X2, zvar = Zvar, C2 = cvec2, xnorm = Xnorm)
```
Passing the per-unit cutoff vector to `rdms` runs silently as one RD per
observation — check `length(cvec)`. `rdms` computes Euclidean distance on its
raw inputs; geographic coordinates go to `rd2d`. Stata: `rdmc y x, cvar(c)` ·
`rdms y x, cvar(cv) range(rl rr)` · `rdms y x1 x2 t, cvar(c1 c2) xnorm(xn)`.

**`rdhte` — heterogeneous RD effects with RBC inference.** Separate subgroup
fits are legitimate; the claim needs an RBC test of the *difference*.

```r
library(rdhte)
zf <- factor(z)                                    # factor: one effect per group;
                                                   # numeric z fits one linear slope
h <- rdhte(y = y, x = x, covs.hte = zf, vce = "cr1", cluster = g)
summary(h)
rdhte_contrast(h, c(-1, 1))      # difference refit at the bandwidth optimal for the contrast
names(h$coef)                    # "zf0" "zf1": the names linfct must use
rdhte_lincom(h, linfct = c("zf1 - zf0 = 0"))   # difference at the per-group bandwidths
rdbwhte(y = y, x = x, covs.hte = zf)           # per-group bandwidths
```
`rdhte` defaults to `vce = "hc3"` (CR1 with a cluster) and to group-specific
bandwidths (`bw.joint = FALSE`); state both. It covers sharp designs only.
`rdhte_contrast` and `rdhte_lincom` give different intervals; name the one
reported.

## Nonparametric functional form (binsreg, nprobust, lpdensity)

For a claim that rests on a functional-form choice — a linear control that could
be nonlinear, a "the relationship is monotone/linear" assertion, a density or
distributional shape — these Cattaneo-group packages replace an eyeballed
scatter with estimation and *inference*.

**`binsreg` — binscatter with valid bands and a parametric-fit test.** The plain
binned scatterplot has no inference; `binsreg` adds confidence bands, and
`binstest` formally tests whether the imposed parametric form (e.g. linearity)
is rejected.

```r
library(binsreg)
binsreg(y, x, w = controls)                       # binscatter + confidence/uniform bands
binstest(y, x, w = controls, testmodelpoly = 1)   # H0: relationship is linear (reject => form matters)
binspwc(y, x, by = group)                         # pairwise comparison of curves across groups
```
Stata: `binsreg y x controls` · `binstest` · `binspwc`.

**`nprobust` — kernel/local-polynomial regression with robust bias-corrected
inference**, for a nonparametric alternative to the paper's parametric
conditional-mean:

```r
library(nprobust)
lprobust(y, x)     # local-polynomial regression over a grid, RBC bands
kdrobust(x)        # kernel density with RBC inference
```

**`lpdensity` — local-polynomial density estimation and inference**, for a
distributional/shape claim about a single variable (boundary-adaptive, unlike a
plain kernel density):

```r
library(lpdensity)
lpdensity(data = x)
```

`lspartition` (partitioning-based series regression with uniform inference) and
`lpcde` (local-polynomial *conditional* density) extend the same
robust-inference approach to spline/wavelet regression and to conditional
distributions; reach for them only when the paper's contribution is that
specific object. `portsort` (portfolio sorting) is finance-specific and normally
`NOT_APPLICABLE` here.

## Synthetic control prediction intervals (scpi)

`scpi` (Cattaneo, Feng, Palomba, and Titiunik) gives a synthetic-control gap a
**model-based prediction interval** — a second, independent inference route to
set beside the placebo-permutation rank the SC module already requires. The two
answer different questions: the placebo rank asks "is the treated gap extreme in
the donor distribution?"; `scpi` asks "given the fit, how much of this gap is
inside the estimator's own uncertainty?". The interval is around the synthetic
counterfactual: a gap that clears the placebo rank while the treated outcome sits
inside the counterfactual's `scpi` interval is not the clean effect the gap plot
suggests.
It also carries the constraint set on the weights (simplex, lasso, ridge, ols,
L1-L2) and, via `scdataMulti`, staggered adoption and multiple treated units.
R, Stata, and Python.

```r
library(scpi)
# 1. Prepare: donor pool, pre/post windows, treated unit.
sc <- scdata(df = d, id.var = "unit", time.var = "year", outcome.var = "y",
             period.pre = pre_years, period.post = post_years,
             unit.tr = treated, unit.co = donors,
             constant = FALSE, cointegrated.data = TRUE)
# constant = FALSE replicates ADH; constant = TRUE adds a free intercept (not
# ADH) — run it only as a labelled sensitivity. State cointegrated.data (default
# FALSE): TRUE models treated and donor series as cointegrated, using first
# differences of the donors when modelling the in-sample residuals u.
# 2. Point estimate under the Abadie simplex (weights >= 0, sum to 1):
est <- scest(data = sc, w.constr = list(name = "simplex"))
summary(est)                                  # donor weights (the degeneracy check)
# 3. Prediction intervals — in-sample (u.*) AND out-of-sample (e.*) uncertainty:
pi <- scpi(data = sc, w.constr = list(name = "simplex"),
           sims = 500, e.method = "gaussian", u.missp = TRUE)
scplot(pi)                                    # gap with prediction bands, not just a line
# Sensitivity: re-run under w.constr = list(name = "lasso") / "ridge" / "ols"
# and report whether the gap survives the weight constraint.
# Staggered / multiple treated units: scdataMulti() -> scest()/scpi() -> scplotMulti().
```
Stata: `scdata` → `scest` → `scpi` → `scplot` (same workflow; confirm the
option names in the installed `.ado` help).

## Primary documentation

- Stata `boottest`: Roodman, Nielsen, MacKinnon, and Webb, “Fast and Wild:
  Bootstrap Inference in Stata Using boottest,” *Stata Journal* 19(1), 2019.
- Stata `rwolf`: Clarke, Romano, and Wolf, “The Romano–Wolf
  Multiple-Hypothesis Correction in Stata,” *Stata Journal* 20(4), 2020.
- R `fwildclusterboot`: package reference site and installed help.
- Python clustered covariance: installed `statsmodels` API documentation.
- R `rdlocrand`: Cattaneo, Titiunik, and Vázquez-Bare, *rdlocrand: Local
  Randomization Methods for RD Designs* (CRAN); method in Cattaneo, Frandsen,
  and Titiunik, “Randomization Inference in the Regression Discontinuity
  Design,” *Journal of Causal Inference*, 2015, and the rdpackages
  documentation.
- R `rd2d`: Cattaneo, Titiunik, and Yu, “rd2d: Causal Inference in Boundary
  Discontinuity Designs” (software article, working paper, 2026); methods in
  Cattaneo, Titiunik, and Yu, “Estimation and Inference in Boundary
  Discontinuity Designs: Distance-Based Methods,” *Journal of Econometrics*
  256, 2026, 106266, and the companion location-based paper (to appear in
  *JASA*).
- `rdrobust`: Calonico, Cattaneo, and Titiunik, “Robust Nonparametric
  Confidence Intervals for Regression-Discontinuity Designs,” *Econometrica*
  82(6), 2014; software in Calonico, Cattaneo, Farrell, and Titiunik, *Stata
  Journal* 17(2), 2017.
- `rddensity`: Cattaneo, Jansson, and Ma, “Simple Local Polynomial Density
  Estimators,” *JASA* 115(531), 2020; manipulation-test software in Cattaneo,
  Jansson, and Ma, *Stata Journal* 18(1), 2018.
- `rdmulti`: Cattaneo, Titiunik, and Vázquez-Bare, “Analysis of Regression
  Discontinuity Designs with Multiple Cutoffs or Multiple Scores,” *Stata
  Journal* 20(4), 2020.
- `rdhte`: Calonico, Cattaneo, Farrell, Palomba, and Titiunik, “Treatment
  Effect Heterogeneity in Regression Discontinuity Designs” (working paper,
  2025); confirm syntax in the installed help.
- `rdpower`: Cattaneo, Titiunik, and Vázquez-Bare, “Power Calculations for
  Regression Discontinuity Designs,” *Stata Journal* 19(1), 2019 (`rdpow`,
  `rdsampsi`; `rdmde` was added in a later release).
- RD plots: Calonico, Cattaneo, and Titiunik, “Optimal Data-Driven Regression
  Discontinuity Plots,” *JASA* 110(512), 2015. Covariate adjustment: Calonico,
  Cattaneo, Farrell, and Titiunik, “Regression Discontinuity Designs Using
  Covariates,” *Review of Economics and Statistics* 101(3), 2019.
  Coverage-error-optimal bandwidths: Calonico, Cattaneo, and Farrell,
  *Econometrics Journal* 23(2), 2020.
- `binsreg`: Cattaneo, Crump, Farrell, and Feng, “On Binscatter,” *American
  Economic Review* 114(5), 2024; software in the companion *Stata Journal*
  article.
- `nprobust`: Calonico, Cattaneo, and Farrell, “nprobust: Nonparametric
  Kernel-Based Estimation and Robust Bias-Corrected Inference,” *R Journal*
  11(2), 2019.
- `lpdensity`: Cattaneo, Jansson, and Ma, “lpdensity: Local Polynomial Density
  Estimation and Inference,” *Journal of Statistical Software* 101(2), 2022.
- `scpi`: Cattaneo, Feng, Palomba, and Titiunik, “Prediction Intervals for
  Synthetic Control Methods,” *JASA* 116(536), 2021: 1865–1880; software and
  staggered-adoption extension in Cattaneo, Feng, Palomba, and Titiunik,
  “scpi: Uncertainty Quantification for Synthetic Control Methods” (rdpackages /
  nppackages); confirm the installed syntax.
- R `sensemakr`: Cinelli and Hazlett, “Making Sense of Sensitivity: Extending
  Omitted Variable Bias,” *Journal of the Royal Statistical Society Series B*
  82(1), 2020; package by Cinelli, Ferwerda, and Hazlett (CRAN).
- R `iv.sensemakr`: Cinelli and Hazlett, *iv.sensemakr: Sensitivity Analysis
  Tool for Instrumental Variable Estimates*; confirm the omitted-variable-bias
  IV method paper and syntax in the installed help.
