# RDD methods: the spine of the RD cribs

Source-audited crib for the RDD battery and the index to the other RD cribs.
One decision spine: does the reported interval carry the bandwidth's bias,
and is the running variable's distribution credible.

**Sources distilled here (source PDFs not distributed with the skill):**
- Calonico, Cattaneo & Titiunik, "Robust Nonparametric Confidence
  Intervals for Regression-Discontinuity Designs," *Econometrica* 82(6)
  (2014), 2295–2326 — published (CCT).
- Gerard, Rokkanen & Rothe, "Bounds on Treatment Effects in Regression
  Discontinuity Designs with a Manipulated Running Variable,"
  *Quantitative Economics* 11(3) (2020), 839–870 — published (GRR).

Verification status: **source-audited 2026-10-15** (re-audit of the
2026-09-22 text; §§1–2 corrected).

Use in this battery: `rdd-diagnostics` (RBC inference as headline,
manipulation-robust bounds) and the design-matrix RDD records.

## 0. The RD cribs and what each one governs

| Crib | Governs |
|---|---|
| this file | RBC as the headline; GRR manipulation bounds |
| `calonico_cattaneo_farrell_rbc_bandwidth.md` | which `rdrobust` row carries the verdict; MSE- vs CER-optimal bandwidths; selectors; clustering; recovering hidden quantities from printed output |
| `rd_practice_guide.md` | the authors' falsification battery (covariates, density, placebo cutoffs, donut, bandwidth range); fuzzy RD; RD plots in practice; pre-specified protocols |
| `calonico_etal_2019_rd_covariates.md` | covariate-adjusted RD estimates: what they target, when they fail, the adjusted–unadjusted identity |
| `calonico_cattaneo_titiunik_2015_rd_plots.md` | RD plots: bins, global fits, what a plotted jump is not |
| `cattaneo_jansson_ma_2020_density_test.md` | the `rddensity` manipulation test, its power, mass points, the binomial test |
| `rd_local_randomization_guide.md` | local randomization; window selection; discrete running variables |
| `kolesar_rothe_2018_discrete_rdd.md` | inference with a discrete running variable; why clustering by the score fails |
| `rd_multiple_cutoffs_guide.md` | multiple cutoffs and scores; pooled weights; extrapolation away from the cutoff |
| `rd_boundary_designs_guide.md` | geographic and two-dimensional boundary designs; `rd2d` |
| `calonico_etal_2025_rd_hte.md` | heterogeneous RD effects; `rdhte` (working paper) |
| `cattaneo_titiunik_vazquezbare_2019_rd_power.md` | RD power and minimum detectable effects; `rdpower` |
| `regression_kink_guide.md` | regression kink designs; the placebo-kink permutation test |

## 1. Conventional intervals are biased at the bandwidths in standard use

CCT (abstract, p. 2295; pp. 2296, 2301): the bandwidth selectors in standard
use, including MSE-optimal selectors targeting the *point estimate*, are too
large for valid conventional confidence intervals. At those bandwidths the
point estimate's bias is first order in the t-statistic, so intervals built
from the raw estimate and the conventional SE undercover. In CCT's
simulations (Table I, p. 2316) the conventional interval at the IK
bandwidth covers 30.3% in Model 2, against 89.5% for the robust one.

The fix is the **robust bias-corrected (RBC) construction**: subtract an
estimate of the leading bias and studentize with a *new variance estimator*
that includes the variability of that bias estimate. Traditional bias
correction keeps the conventional SE, which ignores that variability; it is
valid only when h/b → 0 and performs poorly in finite samples (CCT p. 2302).
Undersmoothing is valid in theory but has no rule for how far to shrink
(`calonico_cattaneo_farrell_rbc_bandwidth.md` §3). RBC is valid at the
MSE-optimal bandwidth and applies to sharp, fuzzy and kink designs (CCT §3),
with scope conditions: a continuous running variable (Remark 1, p. 2299); a
non-zero first stage for fuzzy designs (Theorem 3, p. 2308); a local
quadratic for kink designs (p. 2305, and `regression_kink_guide.md`, where
RBC alone is shown not to control size under curvature).

The MSE-optimal bandwidth minimizes the MSE of the *uncorrected* point
estimator; it is not chosen for the RBC interval. The bandwidth optimized
for the RBC interval is the coverage-error-optimal one (`cerrd`/`certwo`),
which is smaller. Both are too large for a conventional interval
(`calonico_cattaneo_farrell_rbc_bandwidth.md` §4).

Review rule (in the module): the headline is the conventional point
estimate with the RBC interval and p-value; the conventional interval is a
diagnostic. The RBC interval is centred on the bias-corrected point — quote
it as printed, never re-centred on the conventional estimate. A
conventional interval or star at an MSE- or CER-optimal (`rdbwselect`)
bandwidth is the discredited combination.

## 2. Manipulation is a share, not a verdict — GRR 2020

**Model and assumptions.** Some units ("manipulators") can move their score
to one side of the cutoff. GRR's model requires: manipulation in one
direction only, called the "only substantial requirement" (p. 841;
Assumption 3(i), p. 843); no manipulator exactly at the cutoff value
(Assumption 3(ii), pp. 843–844); standard RD conditions and a smooth,
positive score density among non-manipulators (Assumptions 1–2, p. 843);
and a continuously distributed running variable (p. 844). Two-sided
bunching, bunching on the cutoff value, and a discrete score are outside
the model.

**What is identified.** The manipulation share is *point*-identified from
the density jump at the cutoff, τ = 1 − f(c−)/f(c+) (Lemma 1, p. 846). The
effect for non-manipulating compliers at the cutoff,
Γ = E[Y(1) − Y(0) | X = c, complier, M = 0], is *partially* identified: the
sharp bounds take the worst-case *outcome distribution of the manipulators*
given τ (p. 841). Sharp design: trim the treated-side outcome distribution
at the τ or 1 − τ quantile, as in Lee (2009) (Theorem 1, p. 847). Fuzzy
design: the share splits into treated and untreated manipulators, which are
only partially identified; the bounds optimize over that segment, and four
logical restrictions can reject the model (Theorem 2 and pp. 847–853).
Treating eligibility as the treatment gives sharp-design bounds on the ITT
(p. 860). Behavioural assumptions and predetermined covariates narrow the
bounds (pp. 852–853). Nothing is learned about the manipulators (fn. 6,
p. 845).

**Inference.** The recommended object is the manipulation-robust
confidence interval, built to be valid whatever the true τ (§4.2,
pp. 854–855; Appendix B), not the plug-in bound estimates, which are
non-Gaussian when τ̂ is near zero (p. 855, fn. 12). GRR give no formal theory
for that procedure (fn. 10, p. 853) and none for bandwidth choice (fn. 18,
p. 858). The authors' R and Stata implementation is `rdbounds`
(github.com/francoisgerard/rdbounds; the paper points to it on p. 841 as
software "on the authors' websites"; version 1.01, 2019, described by its
authors as preliminary). The fixed-τ breakdown exercise — the largest τ at which the
interval still excludes zero — is a robustness "check for every RD study"
(p. 856).

**When to run it.** GRR intend the bounds for settings where manipulation
is "conceivable, but not obvious from the data" (abstract, p. 839), whatever
a density test says (pp. 841, 862). This matters because density tests have
low power (`cattaneo_jansson_ma_2020_density_test.md` §5): gating the bounds
on a rejection leaves exactly the underpowered cases unexamined.

**How informative.** It depends on τ and on the outcome's tails. In GRR's
application (τ̂ = 0.064, Table 2, p. 861) the sharp-design bounds on
unemployment duration are [26.4, 38.7] days with 6-month censoring and
widen to [31.4, 80.9] days with 24-month censoring; median-effect bounds
stay at [75, 98] days (p. 860). Quantile bounds are the tool when tails
drive the width (pp. 852, 861).

Review routing (as the module encodes): for every load-bearing RD estimate
where one-sided manipulation is institutionally possible, report τ̂ with its
interval and the breakdown τ*. If the upper confidence limit for τ exceeds
τ*, the result is not robust to manipulation the data cannot rule out. A
"survives" verdict is about Γ, the non-manipulating complier effect, and is
stated as such. Where crossing in both directions is plausible, the bounds
do not apply and the manipulation finding rests on covariate balance.
Sorting that leaves the density continuous is invisible to both the density
test and τ; covariate imbalance is the only evidence of it.

The donut is not a substitute for the bounds. GRR call it an ad hoc fix
that extrapolates to a hypothetical population at the cutoff (fn. 3, p. 840;
fn. 7, p. 845). Its role is the sensitivity test in `rd_practice_guide.md`
§6.4: it answers manipulation only if the manipulators sit inside the
donut radius.

## 3. Discrete and heaped running variables

Routing lives in `rd_local_randomization_guide.md` §7 and
`kolesar_rothe_2018_discrete_rdd.md`. In short: the deciding quantity is the
number of distinct score values (mass points) near the cutoff, not
discreteness as such. With many mass points, continuity methods remain
usable, with an effective sample equal to the number of mass points, and
`rddensity` with its mass-point adjustment is admissible. With few, local
randomization is the primary analysis, the density check is the binomial
test in the smallest window, and continuity estimates rest on
extrapolation between mass points. Heaping of a continuous latent score is
a measurement problem (donut sensitivity), not by itself a reason for local
randomization.

## 4. Reviewer checklist

- Headline = conventional point estimate + RBC interval and p-value at the
  MSE-optimal bandwidth, with the RBC interval at the CER-optimal bandwidth
  beside it; conventional SE/interval demoted to diagnostic.
- Density test: robust row only, effective N and the two density estimates
  per side; non-rejection is weak evidence, never clearance.
- GRR breakdown for every load-bearing estimate where one-sided
  manipulation is possible, not only after a rejection.
- Mass-point count near the cutoff decides the discreteness route.
- Bandwidth sensitivity over a small range (hCER, hMSE, 2·hCER, 2·hMSE);
  judge point-estimate stability and interval overlap, not significance at
  every point.
- Covariate-balance and placebo-cutoff tests use the same *procedure* as the
  headline (local polynomial, RBC), each with its own data-driven
  bandwidth; placebo cutoffs use one side's observations only.
