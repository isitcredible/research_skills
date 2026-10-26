# When to cluster, and why — Abadie, Athey, Imbens & Wooldridge (2023)

Working distillation of Alberto Abadie, Susan Athey, Guido W. Imbens and
Jeffrey M. Wooldridge, "When Should You Adjust Standard Errors for
Clustering?", *Quarterly Journal of Economics* 138(1) (2023): 1–35. The
source PDFs (not distributed with the skill): `AAIW_2023_Clustering_QJE.pdf` (NBER WP 24003, Nov
2017) **and** `AAIW_2023_Clustering_QJE_published.pdf` (the published
QJE article) — quote the published version.

Use in this battery:

1. **The whether-to-cluster question** — the skill has dense machinery on
   *how* to cluster (MNW, CGM, DK); this is the missing *whether/when*
   frame: clustering is a design problem, not a residual-correlation test
   (§§1–4).
2. **The finite-population correction** — conventional clustered SEs can
   be severely *inflated* when the sample holds a large share of the
   population of clusters and effects are heterogeneous across clusters
   (p. 17); the corrections (CCV, TSCB) further need assignment that varies
   within clusters (§§III–IV).

## 1. The two sources of variance (§§2–3)

Clustered standard errors adjust for two distinct components, and the
"correlated residuals" intuition conflates them:

- **Sampling component**: clusters in the population that are not in the
  sample. Clustering is a sampling-design correction only when sampling
  is two-stage (sample clusters, then units within them). If the data
  contain (nearly) all clusters — all US counties, all years — this
  component vanishes.
- **Design component**: correlated treatment *assignment* within
  clusters. If assignment is cluster-level (a state-level policy), the
  effective sample is the number of clusters, whatever the residual
  correlation looks like. This is why observational DiD needs cluster
  adjustment and a completely randomized unit-level experiment does not.

Two corollaries that kill common folk rules: (i) nonzero within-cluster
residual correlation does *not* imply clustering is required — the
design may carry no cluster-level assignment; (ii) "no harm in
clustering anyway" is false — the clustered variance estimator is
strictly less efficient when unnecessary, and the adjustment is not
all-or-nothing: the correct variance interpolates via the share of
population clusters sampled and the cluster-level assignment
correlation.

## 2. The finite-population correction (§§III–IV)

Conventional clustered SEs assume the sampled clusters are a negligible
share of the cluster population. When the sample covers a large fraction
(all 50 states; every year in the panel) *and* average effects vary
across clusters, conventional clustered SEs can be **severely inflated**
("the cluster variance is heavily biased if the fraction of the sampled
clusters is large and there is substantial variation in the
cluster-specific treatment effects", p. 17). The corrected estimators
(CCV, TSCB) need assignment that varies within clusters, with enough
treated and control units per cluster; with cluster-level assignment
"there is no improvement from using the CCV variance and the TSCB
variance estimator is not applicable" (§VII, p. 32), and the rule is
"With clustered assignment, one should cluster the standard errors at
the level of the assignment" (§VII, p. 33); the conclusion restates it —
without clustered sampling, "standard errors should be clustered at the
treatment assignment level" (§VIII, p. 33). Review use: a census of
clusters with within-cluster assignment and heterogeneous effects may be
over-corrected by clustering — CCV/TSCB are the fix; a state-level
policy on all 50 states may still have conservative clustered SEs, but
no correction applies (p. 32) — cluster at the state. A paper clustering
"because residuals correlate" on a census of clusters hasn't thought
about what the SE is for.

## 3. What this means for the battery

- The clustering question is answered from the **design** (how clusters
  entered the sample, how treatment was assigned), never from a residual
  correlation test. "The residuals correlate within states" is not a
  reason to cluster; "treatment was assigned at state level" is.
- Pair with `mackinnon_nielsen_webb_2023_few_clusters.md`: AAIW says
  *whether* and at what level; MNW says *how many effective clusters the
  chosen level really has* — the two are complementary, and a design can
  fail at either stage (cluster at the right level but have G* ≈ 2).
- `experiment-diagnostics`: in a unit-randomized trial, clustering the
  SEs is a choice with a cost, not a default — check which component the
  design actually carries.
