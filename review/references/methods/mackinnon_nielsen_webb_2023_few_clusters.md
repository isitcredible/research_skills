# Few and unequal clusters: partial leverage, CV3, and tF/VtF confidence sets

Source-audited distillation of the MacKinnon–Nielsen–Webb cluster-jackknife
program and of the Lee–McCrary–Moreira–Porter(-Yap) tF/VtF procedures.

**Sources audited (all source PDFs not distributed with the skill):**
- MNW, "Cluster-robust inference: A guide to empirical practice,"
  *Journal of Econometrics* 232 (2023), 272–299 — published, verified.
- MNW, "Fast and reliable jackknife and bootstrap methods for cluster-robust
  inference," *Journal of Applied Econometrics* 38 (2023), 671–694 —
  published, verified. (Guide cites it as "MacKinnon et al. 2022a/2022b".)
- Lee, McCrary, Moreira & Porter, "Valid t-ratio Inference for IV," *AER*
  112(10) (2022), 3260–3290 — **NBER WP 29124 audited; published version
  pending**. Cite by section, not printed page, until the AER lands.
- Lee, McCrary, Moreira, Porter & Yap, "What to do when you can't use '1.96'
  Confidence Intervals for IV," NBER WP 31893 (2023) — no published version
  exists; WP is the version of record.
- MNW, "Cluster-robust inference: A practitioner's guide with `summclust`,"
  *Stata Journal* 23(4) (2023), 574–602 — published; the `summclust`
  implementation reference.
- Hansen, "Jackknife Standard Errors for Clustered Regression," *Review of
  Economic Studies* (2026, published) — on-disk version dated Sept 2025;
  cribbed separately at `hansen_2026_jackknife_se.md`.

Verification status: **source-audited 2026-09-22**; Hansen and the Stata
Journal companion added 2026-09-28. Printed-page cites below are to the
published JoE/JAE articles; the two Lee et al. sources are WPs and are cited
by section only.

Use in this battery:

1. **small-n / iv-diagnostics few-cluster rows** — report G* and CV3; route
   weak-IV coefficients through tF/VtF rather than quoting a WCB p-value.
2. **shift-share-diagnostics** — the same diagnostics at the shock-cluster
   level, where a dominant shock is the same disease as a dominant cluster.
3. **Auditing a paper's cluster count** — a nominal G of 40–60 with severe
   leverage imbalance is not "enough clusters"; report the effective count.

## 1. Nominal G is the wrong denominator: leverage and G*

Two diagnostics, both from the guide §3.4/§7:

- **Cluster leverage** L_g: the cluster analog of observation leverage —
  L_g = tr(H_g) where H_g = X_g(XᵀX)⁻¹X_gᵀ is the per-cluster block of the
  hat matrix (guide eq. 19, ~p. 281). A cluster is high-leverage when it
  carries a large share of the regressor information.
- **Partial leverage** for coefficient j: L_gj = x̃_gjᵀx̃_gj / x̃_jᵀx̃_j,
  where x̃_j is the regressor residualised on all other regressors (guide
  eq. 39, pp. 290–291). Partial leverages sum to 1 across clusters — they are
  the share of residualised regressor variation located in each cluster.

The **effective number of clusters** G*_j is Carter, Schnepel & Steiger's
(2017) measure (guide pp. 290–291). It is parameterised by ρ, the assumed
intra-cluster correlation of the disturbances under an equi-correlated model:

- **ρ = 0 is the right choice when the regression contains cluster fixed
  effects** — cluster FEs already absorb intra-cluster correlation, and ρ ≠ 0
  with cluster FEs can produce numerical instability. **ρ = 1 is the
  worst-case choice** appropriate when there are no cluster FEs.
- At ρ = 0, G*_j(0) is a monotone-decreasing function of the squared
  coefficient of variation of the partial leverages — equivalently the
  inverse Herfindahl, G*(0) = G / (1 + CV²(L_•j)) = 1/Σ_g L_gj².

So: fifty-one states where one state carries 70–80% of the residualised
regressor behave like G* ≈ 1–2 clusters, and every cluster-robust procedure
inherits that — the nominal count is a courtesy number. Report G* beside G
whenever clustering is debated, at the correct ρ for the FE structure.
(This formalises, and replaces, the "variance-meat share" heuristic: the meat
share of the largest cluster is its partial leverage.)

Stata: `summclust` (MNW's ado) reports leverages, partial leverages, G*, the
delete-one-cluster estimates β̂^(g), and CV3. A hand implementation is a
residualise-then-sum: partial the regressor on the FE/controls, sum squared
residuals by cluster, normalise to shares, invert the Herfindahl.

## 2. CV1 vs CV3

- **CV1** — the usual cluster-robust sandwich. Downweights nothing; a
  dominant cluster's residuals set the whole variance. MNW's flat assessment:
  CV1 SEs "are often much too small" (JAE conclusion, pp. 692–693).
- **CV3** — the cluster jackknife. Two equivalent forms (guide §2/§3.4):
  the modified-score sandwich (guide eq. 10) and the classic jackknife
  variance built from the G delete-one-cluster coefficient estimates,
  CV3 = ((G−1)/G) Σ_g (β̂^(g) − β̂)(β̂^(g) − β̂)ᵀ (guide eq. 18, ~p. 281).
  The second form is what `summclust` computes and is far faster.

**Fixed-effect subtlety** (JAE paper, §3/§4): in the delete-one-cluster
replications, regressors partialled out beforehand pick up information from
the deleted cluster — so in general everything must be re-fit per
replication. The exception is fixed effects at the clustering level or finer
(e.g. firm FEs with industry clustering): those load only on their own
cluster's observations, and it is not just valid but *essential* to partial
them out — with a cluster-FE dummy among the regressors the M_gg matrices in
the score form are singular (guide §2, p. 275). So: cluster-level-or-finer
FEs partialled out; coarser FEs and all controls re-estimated inside each
leave-out replication. A "jackknife" that holds non-cluster FEs at their
full-sample values is not CV3.

Report both CV1 and CV3 — a large gap between them is itself a
leverage-imbalance finding (in MNW's example, CV3 is 47% larger than CV1 at
G = 70). CV3 + t(G−1) is a reliable default when clusters are well balanced
and the effective count is large (MNW suggest "more than 100"); it can
under-reject (JAE conclusion).

**The stronger statement — Hansen (2026)** (full crib at
`hansen_2026_jackknife_se.md`): conventional HC/CRVE estimators have *full*
worst-case downward bias and worst-case CI coverage of **zero**, while the
modified jackknife variance is never downward biased and its CI coverage is
Cauchy-bounded — under arbitrary cluster sizes, leverage, within-cluster
correlation, FE, single treated clusters, and delete-cluster invertibility
failures. So a jackknife variance is the defensible *default* under
concentrated leverage, not a robustness garnish. Two catches: (a) the
guarantee requires the delete-cluster modification that does *not* discard
non-invertible leaves — cluster-dropping implementations (Stata's
`vce(jackknife, mse)`) are not covered; (b) Hansen recommends a
Satterthwaite dof for the jackknife t-ratio over student t.

## 3. WCB in the modern toolkit — corrected

The earlier draft of this crib treated WCB as unreliable below a hard
G* ≈ 10 floor. That floor is ours, not MNW's — **they give no threshold**,
and their actual recommendations are subtler (JAE conclusion, pp. 692–693;
guide §5–7):

- MNW recommend **at least one WCR (restricted, null-imposed) bootstrap
  variant almost all the time**, B ≥ 9999, not as a last resort.
- Their single endorsed default is **WCR-S**: a restricted bootstrap whose
  DGP uses jackknife-transformed restricted scores while the test statistic
  uses ordinary CV1 SEs — cheap and their best performer in simulations.
  The classic WCR-C (plain Roodman `boottest`) is the variant the new ones
  "typically perform better than" — in some experiments WCR-S works
  "substantially better" (JAE §8). But "whenever CV1 and CV3 differ
  substantially … it is probably a good idea to compute both WCR-C and
  WCR-S P-values" (§8): WCR-C is the companion, never the sole number.
- **Unrestricted WCU/WCU-S is demoted to a robustness check** — do not quote
  it as the primary inference (JAE conclusion: "we generally do not recommend
  the unrestricted wild cluster bootstrap").
- WCR can yield *exact* inference even at very small G in certain cases
  (Canay, Kamat & Ogburn via the Rademacher–randomisation link; guide ~p.
  289) — though under strong cluster-homogeneity conditions.
- The genuine MNW warning cases: **few treated clusters** (WCR P-values can
  be far too *large* — under-rejection — when only one cluster is treated;
  guide §4.3.2) and severe leverage imbalance. For few-treated-cluster
  settings they point to **randomization inference** over the cluster-level
  treatment assignment (guide §6.2).
- Diagnostics, not thresholds: compute G* and the (partial) leverages; if
  CV1 vs CV3 disagree materially or G* is tiny, the bootstrap variants are
  more reliable — and when methods disagree, run several and report the
  spread.

So the review-side rule changes: do not dismiss a WCB result merely for a
small effective count — ask *which variant* (restricted vs unrestricted,
which score transform, B), check G*/leverage, and treat a large
CV1-vs-CV3-vs-bootstrap spread as the actual finding. A null-imposed
boottest run on an IV spec that returns an unbounded CI is still a pathology
report, not a p-value — the orchestrator quarantine rule applies.

## 4. tF / VtF confidence sets (Lee–McCrary–Moreira–Porter program)

Corrected after source audit — these procedures condition on **first-stage
F**, not on effective-cluster diagnostics:

- **tF** (LMMP 2022): the critical value is a smooth function c(F̂) of the
  first-stage F — equivalently an SE inflation factor — so the set stays
  valid as the instrument weakens, going unbounded rather than spuriously
  tight. Finite 95% sets exist for any F̂ > 1.96² = 3.84; c(F̂) → ∞ as
  F̂ → 3.84⁺. Plain ±1.96 without adjustment requires F̂ > 104.67 for true
  95% coverage (pre-testing at F̂ > 16.38 yields only an 85% interval, WP
  p. 2 and fn. 17 — the Stock–Yogo "10" folklore is far short). tF is robust to heteroskedastic/clustered errors provided the
  same robust variance type is used for first stage and IV. (WP §I–II.)
- **VtF** (LMMPY 2023, version of record = NBER WP 31893): extends tF by
  conditioning on a second statistic — r̂(b₀), the null-imposed correlation
  between structural-equation and first-stage residuals (computed from the
  reduced-form/FS variance-covariance; under clustered errors it is the
  correlation across clusters of within-cluster sums of Zû and Zv̂). The
  critical value c(r̂(b₀), F̂) is then inverted over b₀ to a (possibly
  asymmetric) interval β̂ − k₋·se to β̂ + k₊·se. Practical rule of thumb:
  **F̂ > 10 + 100·|r̂| suffices for ±1.96 at 95%** (WP p. 23); VtF still yields bounded
  sets down to F̂ > 3.84. tF is the r̂-worst-case special case. In their
  89-specification audit of top-five IV papers, VtF intervals were shorter
  than AR in 100% of cases. (WP §I–II.)
- Stata: `vtf.ado` + `vtf95.mmat`/`vtf99.mmat` from Lee's Princeton
  supplement page; tF likewise from SupplementarytF.html.

**Pairing with few-cluster machinery** — legitimate and recommended, but be
precise about what is whose: the VtF *critical values* come from (F̂, r̂);
the *inputs* must use the jackknife variance (CV3 SE and a jackknife
first-stage F, from the jackknife covariance of the reduced-form and
first-stage coefficients) when clusters or shocks are few or unequal. The
review requires this; it is not optional. `vtf.ado` cannot take a jackknife
variance (only `robust`/`cluster()`, i.e. HC1/CR1), so its output is a CR1
companion row and the jackknife set is built by hand (iv-diagnostics,
"VtF on jackknife inputs"; SP-008). An unbounded VtF set at effective-clusters ≈ 1 is the machinery
honestly reporting "uninformative at this cluster count" — report it as
such, never round it to a p-value.

## 5. Reviewer checklist

- Any clustered target: report nominal G **and** effective G* (Carter et al.,
  ρ = 0 iff cluster FEs present) plus the top partial leverages. A paper
  citing "50 states" whose top state carries most of the regressor's
  variation has ~1–2 effective clusters — say so.
- Unequal leverage or small G* → lead with CV3 SEs beside CV1 (gap =
  finding): the jackknife emits a *variance* the battery consumes
  downstream (SE ratios, VtF/tF inputs) plus the β̂^(g) leave-out
  distribution as an influence diagnostic; a bootstrap emits only a
  verdict. WCR-S bootstrap P-values second — with WCR-C always beside them
  (§8 advises both whenever CV1 and CV3 differ) — B ≥ 9999, variant
  and convention named — and its failure modes are reportable pathology,
  not shrugs: coarse p-value granularity at small G (2^G Rademacher /
  6^G Webb support), estimator non-attachment, unbounded inversion,
  few-treated-cluster under-rejection.
- IV coefficients under weak instruments or few clusters → tF/VtF sets with
  clustered/jackknife-robust inputs; record F̂, r̂, and whether the
  F̂ > 10 + 100·|r̂| rule of thumb is met.
- One or few treated clusters → cluster-level randomization inference
  (guide §6.2), not a bootstrap t-test.
- An unbounded CV3/tF/VtF set is an informative result about the design
  ("uninformative at this cluster count/instrument strength"), reported as
  such — never promoted to a significance verdict (orchestrator quarantine).
- Audit a paper's "few clusters" defense the same way: ask for G*, not G —
  and for which bootstrap variant, not just "we wild-bootstrapped".
- Before accepting a finer clustering level as the fix, recompute G* and
  partial leverages *at that level* — a dominant cluster typically migrates
  with the level (a dominant state becomes a dominant metro under finer
  clustering), because what concentrates is regressor variance, not
  geography.
- A 2SLS SE *below* the analogous OLS SE is a CRVE-failure tell, not
  proof: IV adds uncertainty relative to OLS mechanically only under
  homoskedastic SEs on the same sample, so under clustering a smaller
  reported IV SE suggests the clustered variance — not the precision — is
  what moved. Check both under CV3 first (see `iv-diagnostics`).
