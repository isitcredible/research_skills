# Jackknife standard errors for clustered regression — Hansen (2026)

Working distillation of Bruce E. Hansen, "Jackknife Standard Errors for
Clustered Regression," *Review of Economic Studies* (2026, published).
The version audited is the author's version dated **September 2025**
(`Hansen_2026_JackknifeSE_Clustered_ReStud.pdf`, not distributed with the skill) — cite by theorem/
section, verify page numbers against the published version before
quoting.

Use in this battery:

1. **The CV1-vs-jackknife row** of the few-clusters analysis — the
   replacement case for conventional CRVE, not just its finite-sample
   correction (§§1–3).
2. **The invertibility caveat** — what makes a jackknife estimator
   robust to cluster-level regressors, single treated clusters, and
   sparse dummies, and where conventional delete-one estimators (incl.
   Stata's default) still fail (§4).
3. **The Satterthwaite dof** for jackknife t-ratios (§5).

## 1. The failure of conventional estimators (§1, abstract)

Under standard conditions, conventional HC/CRVE variance estimators can
be *fully* downward biased — worst-case bias is the whole variance —
and the resulting confidence intervals have **worst-case coverage
probability zero** even under normal errors. This is a worst-case
result, not a typical-case claim: it binds under arbitrary cluster
sizes, leverage, and within-cluster correlation — precisely the
configuration a few-dominant-clusters design produces.

## 2. The jackknife fix (Thm 1 and following)

Hansen's modified jackknife variance estimator is **conservative: its
expectation is never below the exact variance** — never downward
biased — under the same broad conditions: arbitrary cluster sizes,
regressor leverage, within-cluster correlation, heteroskedasticity,
fixed effects, single treated clusters, and delete-cluster
invertibility failures. Under cluster-dependent normality plus a
stronger rank condition, the worst-case coverage of the jackknife
interval is bounded by the **Cauchy distribution** (uniformly over
regressor/covariance configurations), against zero for the CRVE
interval.

## 3. What this changes in the battery's advice

MNW 2023 (`mackinnon_nielsen_webb_2023_few_clusters.md`) recommends CV3
and jackknife inference on finite-sample grounds; Hansen supplies the
stronger statement — the conventional CRVE is not merely imprecise but
has *full* worst-case downward bias, so a jackknife variance is the
defensible default under concentrated cluster leverage, not a
robustness garnish. The practical ordering stays: report CV3 (or the
modified jackknife) alongside CV1, re-run G*/leverage diagnostics, and
read a large CV1→CV3 gap as the design's actual precision.

## 4. The invertibility caveat — the load-bearing technicality

For the jackknife to inherit the never-downward-biased property, the
formula must be modified so that **delete-cluster regressions that fail
to invert do not cause the cluster to be discarded**. Existing ad-hoc
modifications — including Stata's `vce(jackknife, mse)` ≈ Hansen's
V̂4, which drops non-invertible deletes — can still be downward biased
and are not covered by the guarantee. When the design has
cluster-level-only regressors (cluster FE, one treated cluster, sparse
interactions), the specific estimator variant is decisive: name which
jackknife was run and whether it handles non-invertible deletes.
(MNW's generalized delete-one family has the same property; Hansen's
contribution is showing the guarantee depends on it.)

## 5. Degrees of freedom

A Satterthwaite-type dof adjustment to the jackknife t-ratio (extending
Bell–McCaffrey 2002, Imbens–Kolesár 2016, Young 2016, Pustejovsky–
Tipton 2018) improves finite-sample coverage; scalar parameters only,
no joint tests. Recommended as the default for CIs/p-values over the
student t.

## Reviewer checklist

- Few/unequal clusters + CV1 SEs → treat the CRVE as potentially fully
  downward-biased; demand the jackknife/CV3 number and the G*/leverage
  table (MNW crib for implementation).
- Verify the jackknife variant: cluster-dropping implementations are
  not guaranteed conservative under invertibility failures — check for
  cluster-level-only regressors first.
- Implementation note for the IIG-style combination: CV3/jackknife
  variance estimates feed directly into VtF/tF weak-IV inference — compute
  the 2×2 jackknife covariance matrix $\hat{\Sigma}_{\text{jack}}$ of the
  first-stage and reduced-form coefficients $(\hat{\pi}, \hat{\delta})$ from
  the same delete-one-cluster pairs and pass $(\hat{F}_{\text{jack}},
  \hat{r}_{\text{jack}})$ to the VtF critical-value function (`vtf.ado` is
  hard-wired to CR1/HC1 variable inputs and does not accept supplied SEs;
  any `vtf` call must be tagged `VtF-CR1-robustness`). The few-cluster and
  weak-IV problems stack rather than cancel.

## DiD application: Hansen (2025, JAE)

Hansen, "Standard Errors for Difference-in-Difference Regression,"
*Journal of Applied Econometrics* 40 (2025): 291–309 (published;
`Hansen_2025_DiD_StandardErrors_JAE.pdf`). Recommends the jackknife SE
plus an adjusted interval θ̂ ± (t_K quantile / a)·ŝ_jack, with K and a from
the Bell–McCaffrey reference model (eq. 13). Simulations (§5): CV1
undercovers in every design, worse as treated/untreated cluster counts grow
more unequal, as effect heterogeneity grows, and as G grows under that
asymmetry (worst case 61% baseline; 36% with unequal treated-cluster sizes);
the cluster bootstrap is similar (63%); wild bootstrap fails under large
heterogeneity (69%); Bell–McCaffrey and the adjusted jackknife are best
(worst cases 90% and 91%). With one treated cluster the jackknife
remains conservative (100% coverage; Hansen 2024, cited in §1). Implementation: the author's `jregress`
(Stata, R). Replications: Card–Krueger (1994), Bailey (2010), MacKinnon–Webb
(2020), Rao (2019).
