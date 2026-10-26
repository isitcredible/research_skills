# Covariate adjustment in RD — Calonico, Cattaneo, Farrell & Titiunik (2019)

Working distillation of Sebastian Calonico, Matias D. Cattaneo, Max H.
Farrell and Rocío Titiunik, "Regression Discontinuity Designs Using
Covariates," *Review of Economics and Statistics* 101(3) (July 2019):
442–451, doi:10.1162/rest_a_00760. Version audited: the published article
(journal furniture on p. 442; received October 2016, accepted May 2018).
The "Just Accepted MS" dated 29 May 2018 carries the same main text and
Table 1 numbers and was used only as a cross-check; quote the published
pages. The online supplemental appendix (fuzzy, kink and clustered
formulas, polynomial order p > 1, full simulations) was **not** audited:
anything this crib attributes to "the supplement" is the article's own
pointer, not a reading of it. Source PDFs (not distributed with the skill):
`Calonico_Cattaneo_Farrell_Titiunik_2019_RDCovariates_ReStat.pdf` and
`Calonico_Cattaneo_Farrell_Titiunik_2019_RDCovariates_ReStat_accepted_ms.pdf`.
Cross-references, both published: Cattaneo, Idrobo & Titiunik, *A Practical
Introduction to Regression Discontinuity Designs: Foundations* (Cambridge
Elements, 2020), §4.4.1 pp. 69–74 and §5 pp. 80–84 ("CIT 2020"); Calonico,
Cattaneo, Farrell & Titiunik, "rdrobust: Software for Regression
Discontinuity Designs," *Stata Journal* 17(2) (2017): 372–404 ("CCFT 2017").

Verification status: source-audited 2026-10-15 (main text only; supplement
not audited).

Use in this battery:

1. `rdd-diagnostics` — any headline RD estimate that includes controls,
   fixed effects or other covariates in the local regression.
2. `rdd-diagnostics` **Predetermined covariates and placebo outcomes** — the
   covariate-balance condition is what makes the adjusted estimate target
   the standard RD effect, not only a falsification test.
3. The exact finite-sample decomposition (§6) for diagnosing why an
   adjusted estimate moved.

## 1. Setting and estimand (§II, p. 444)

Sharp RD with a continuous score X (density continuous and bounded away
from zero, Assumption SRD(a), p. 445), cutoff normalised to 0, parameter
τ = E[Y(1) − Y(0) | X = 0]. Covariates have potential values,
Z = Z(0)(1 − T) + Z(1)T, so a covariate *can* be moved by treatment; the
framework asks only that the treatment have no mean effect on Z at the
cutoff (p. 443). The paper treats sharp, local-linear designs in the text;
fuzzy, kink and p > 1 are in the supplement (p. 444).

Five ways practitioners add Z to the local linear fit are compared
(eqs. 2–6, p. 444): (2) τ̃, Z entered once with a common coefficient —
the recommended "covariate-adjusted RD estimator"; (3) τ̌, Z interacted
with treatment, equivalent to separate regressions on each side; (4)
common demeaning; (5) common demeaning plus interaction; (6) side-specific
demeaning plus interaction. Covariates enter additively and linearly in
parameters, but this is a local linear *projection*, not an assumption
about E[Y | X, Z] (pp. 443, 445). Z may hold power expansions,
interactions and transformations of the original covariates, and
"including fixed effects or other discrete variables" (p. 445).

## 2. What τ̃ estimates (Lemma 1, pp. 445–446)

τ̃ converges to τ − (μZ+ − μZ−)′γY, where μZ± are the covariate means at
the cutoff on each side and γY is a pooled best-linear-projection
coefficient at the cutoff. So the adjusted estimator targets the standard
RD effect plus a bias term equal to the RD effect on the covariates,
τZ = μZ+ − μZ−, times γY. Sufficient condition: τZ = 0 — no discontinuity
in covariate means at the cutoff. This is weaker than equal marginal
distributions of Z(0) and Z(1) near the cutoff (p. 446). The same balance
condition is the usual covariate "placebo" test (p. 443). For kink
designs a further condition is needed: the first derivatives of the
covariate regressions must also match at the cutoff (p. 446; details in
the supplement). All of Theorem 1–2 is derived "assuming throughout" that
μZ+ = μZ− (p. 446).

Inference, not the source's words: a covariate affected by treatment,
or any covariate that jumps at the cutoff, makes τ̃ estimate
τ − τZ′γY, a different object from the unadjusted τ̂. Whether the bias
term is small depends on γY, which no test of τZ alone reveals.

## 3. Specifications that fail (p. 446)

- **Treatment-interacted covariates (τ̌, separate side regressions with
  controls).** Consistent for τ only if μZ+γY+ = μZ−γY−, which in
  practice needs γY+ = γY− on top of balance. The paper calls the gap a
  misinterpretation of the interaction term.
- **Demeaning.** Common demeaning (4) behaves like τ̃; (5) acquires a new
  probability limit involving a recentring; side-specific demeaning (6)
  behaves like the unadjusted τ̂ and needs no balance. But all three use
  local averages of Z, equivalent to uniform-kernel regressions, so they
  have slower convergence rates, new misspecification biases and extra
  asymptotic variability relative to τ̃, so inference based on them is badly
  distorted (p. 446). Simple demeaning also fails in other RD designs
  (p. 446).
- Conclusion (p. 446): τ̃ needs the weakest assumption and avoids the
  demeaning problems; it is the one advocated.

## 4. Covariates cannot rescue identification (pp. 443, 450)

The framework is for precision, as with pre-treatment covariates in
experiments (p. 443). Using covariates to fix a design whose potential
outcomes may be discontinuous needs parametric assumptions or a redefined
parameter; adjusting for imbalanced covariates to "restore identification
is not possible without functional form" assumptions (p. 443). CIT 2020
p. 69 states the same rule for practice: covariates used to augment the
analysis must be balanced at the cutoff, and imbalance in important
predetermined covariates makes the continuity assumption implausible;
p. 71: post-treatment or imbalanced covariates change the parameter
being estimated.

## 5. Efficiency (pp. 447–448, 450)

The asymptotic variance ratio Vτ̃/Vτ̂ compares V[Y(t) − Z(t)′γY | X = 0]
with V[Y(t) | X = 0], summed over sides (p. 447). No general ranking
exists, because γY need not equal either side's own projection
coefficient (p. 448). Gains are guaranteed in the special case
γY = γY− = γY+: when the covariates' effect on outcomes near the cutoff is
roughly the same for treated and control units, including them "may lead
to efficiency gains" (p. 448). This parallels Freedman (2008) and Lin
(2013) for experiments. MSE can also fall (same rate), but the authors
still recommend the **unadjusted τ̂ at its own MSE-optimal bandwidth as
the benchmark point estimator**, because it rests on minimal identifying
assumptions; covariates are added to gain precision relative to it
(p. 448). Simulations (p. 450): gains grow with the residual
outcome–covariate correlation; an irrelevant covariate hardly changes
results.

## 6. Bandwidth selection and RBC inference change with covariates (pp. 446–449)

- **Exact decomposition.** "We rely on the following representation
  (valid for each n)" (p. 446): τ̃(h) = τ̂(h) − τ̂Z(h)′γ̃Y(h), where
  τ̂Z(h) is the vector of standard RD estimates with each covariate as the
  outcome, at the same h, kernel and order. At a common bandwidth, the
  movement from adjustment equals τ̂Z(h)′γ̃Y(h), exactly.
- **MSE and bandwidth.** The covariate-adjusted bias and variance
  constants differ from the no-covariate ones, so the MSE-optimal
  bandwidth, the bias correction and the standard errors all differ under
  adjustment (Theorem 1 and p. 447). Local linear MSE-optimal
  hτ̃ = [Vτ̃ / (4 n Bτ̃²)]^(1/5) (p. 447); the rate is unaffected by d
  because Z is not smoothed over. One-sided, sum and regularised variants
  are in the supplement (p. 447).
- **RBC.** τ̃bc(h, b) = τ̃(h) − h²B̃τ̃(b), with a local quadratic bias
  estimate; b = h is allowed and has optimality properties (p. 448). The
  studentising variance accounts for the bias estimate's variability; the
  feasible versions are nearest-neighbour (NN) or plug-in-residual (PR),
  each covering heteroskedasticity and clustering (p. 448).
- **Theorem 2 (p. 449).** Asymptotic normality of the RBC t-statistic
  requires τZ = 0, nh⁷ → 0 and lim h/b < ∞; it holds at the MSE-optimal
  bandwidth, which conventional inference does not.
- **CER bandwidth.** h̃CER = n^(−1/20) × h̃τ̃ for the local linear case
  (p. 449).
- **Clustering.** Results carry over with each unit in one of G clusters
  and G → ∞, Gh → ∞ (p. 449).
- Practice: CIT 2020 pp. 72–73 show the covariate-adjusted MSE bandwidth
  differing from the unadjusted one (14.409 vs 17.239) and note that the
  adjusted estimate would differ even at a common bandwidth because the
  fitted coefficients change. Software: `covs` in `rdrobust` and
  `rdbwselect` (CCFT 2017 p. 383; R usage `covs = Z`, CIT 2020 pp. 72–73).
  Balance can be tested by running `rdrobust` with each covariate as the
  outcome (CCFT 2017 p. 376).

## 7. Fixed effects and many covariates

What the source says: any regressors are allowed, including fixed effects
and discrete variables (p. 445), and the convergence rate does not depend
on d (p. 447). What it does not say: nothing on d growing with n,
high-dimensional controls, fixed effects whose number grows with the
sample, or how many observations per fixed-effect cell the window needs.
Z is a fixed-dimension vector in the theory (p. 444).

Inference, not the source's words: (i) the balance condition in Lemma 1
applies to every column of Z, so for a set of fixed-effect indicators it
requires the group shares to be continuous at the cutoff; (ii) Assumption
SRD(d) requires V[(Y, Z′)′ | X = x] to be invertible near the cutoff, so
fixed-effect cells empty or constant near the cutoff violate it; (iii) a
paper with many fixed effects inside a narrow bandwidth sits outside the
asymptotics the article proves.

## 8. Empirical illustration (Table 1, pp. 449–450)

Head Start (Ludwig & Miller 2007), nine 1960 census covariates,
triangular kernel, NN variance. Unadjusted −2.41; adjusted at the
unadjusted bandwidths −2.51; adjusted at covariate-adjusted bandwidths
−2.47. Robust CI length falls 8.25% and 9.76%; h moves from 6.81 to 6.98.
Placebo tests on the covariates found no RD effects. The authors read
stable point estimates as what predetermined covariates should produce:
"including covariates does not substantially" alter the estimates
(p. 450). CIT 2020 p. 74 states the same benefit: shorter intervals with
the point estimate roughly unchanged.

## Review use

- **Trigger.** Any RD result whose local regression includes controls,
  fixed effects, lagged outcomes or other covariates — including a
  hand-rolled `reg y T x T#x controls if abs(x) < h`.
- **Classify each covariate.** Measured before assignment and impossible
  for the treatment to move? If a covariate is measured after the
  assignment date or plausibly responds to treatment, the adjusted
  estimate targets τ − τZ′γY, not τ (Lemma 1); the result must rest on the
  unadjusted estimate.
- **Classify the specification.** Common coefficient (τ̃) is the
  supported form. Covariates interacted with treatment, separate side
  regressions with controls, or demeaned covariates (§3) are flagged: the
  first needs equal side coefficients; the demeaning forms carry invalid
  inference.
- **Compute.** (a) the unadjusted RBC benchmark at its own MSE-optimal h;
  (b) the adjusted RBC estimate with covariate-adjusted bandwidth
  selection (`covs` in both `rdbwselect` and `rdrobust`); (c) the adjusted
  estimate at the unadjusted h, to separate the bandwidth change from the
  adjustment; (d) τ̂Z(h) for each covariate at that common h, with its RBC
  p-value, and γ̃Y(h). The (c) − benchmark gap equals −τ̂Z(h)′γ̃Y(h)
  exactly; report which covariates carry it.
- **When the estimate moves materially.** The source gives no numerical
  threshold. Inference: compare the shift with the unadjusted standard
  error. A shift traced to covariates with nonzero τ̂Z(h) is evidence of
  covariate imbalance at the cutoff — a design-validity problem (CIT 2020
  p. 69) — not a better-controlled estimate. A shift traced to the
  bandwidth change alone is a specification-sensitivity finding. Either
  way the adjusted number does not displace the unadjusted benchmark
  (p. 448).
- **Significance only after adjustment.** If the unadjusted RBC interval
  covers zero and only the adjusted one excludes it, the claim rests on
  the efficiency argument, which is valid only under balance; demand the
  balance tests for every covariate used, and state which covariates
  produced the precision gain.
- **Bandwidth and inference.** An adjusted estimate at a bandwidth chosen
  without covariates, or with conventional standard errors, is not the
  covariate-adjusted RBC procedure of Theorem 2; re-run it. With
  clustering, count clusters with observations inside [−h, h]: the theory
  needs G and Gh large (p. 449).
- **Fixed effects.** Allowed, but state that the result's validity needs
  continuous group shares at the cutoff (inference, §7) and test the
  indicators' balance like any covariate.
- **Kink designs.** Adjustment also needs balance in covariate slopes
  (p. 446); test the covariates' kinks, not only their levels.
