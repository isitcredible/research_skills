# Shift-share inference: the AKM standard errors — Adão, Kolesár & Morales (2019)

Working distillation of Rodrigo Adão, Michal Kolesár and Eduardo Morales,
"Shift-Share Designs: Theory and Inference," *Quarterly Journal of
Economics* 134(4) (2019): 1949–2010 — the published article (DOI
10.1093/qje/qjz025), not a working paper. Verified against the
published PDF (not distributed; a JSTOR copy whose PDF p.1 is the cover);
printed page = PDF page + 1947 (PDF p.2 = printed p. 1949). The companion R package
vignette is `ShiftShareSE_Rpackage_AKM_AKM0.pdf` (not distributed); the Stata
implementation is `ssaggregate` (SSC). All cites are to the printed page.

Use in this battery:

1. **The shock-level-inference rows** of `shift-share-diagnostics` —
   why unit-level clustering cannot fix a shift-share regression, and
   what AKM/AKM0 compute instead (§§1–3).
2. **Auditing a paper's "we already ran AKM" roster** — AKM vs AKM0 are
   different objects (Wald vs null-imposed inversion) with different
   finite-sample behaviour (§3).
3. **When the procedures themselves are doubtful** — the three validity
   conditions (§4), which is when the null-imposed score test in the
   skill takes over.

## 1. The placebo finding (§II, Table I, pp. 1955–1959)

A canonical industry-shock × regional-exposure design on US local
labor-market outcomes; the industry shocks are
replaced by *random* draws pushed through the actual exposure shares —
30,000 placebo samples. Nominal 5% tests of H0: β = 0 reject far too
often; e.g. for the CZ employment rate (Table I, Panel A, "Employed")
the rejection rate is **48.5%** with Eicker–Huber–White SEs and
**38.1%** with SEs clustered on state, and for employment in
manufacturing **55.7%** and **44.8%** (Table I, cols 5–6, p. 1957;
across the six outcomes, robust rates run 23.2–55.7%, clustered
16.8–44.8%; the abstract's "up to 55%"). Remark 1 (p. 1958):
traditional inference methods yield confidence intervals that are too
short.

## 2. Why (§§III–IV.A, pp. 1959–1975)

The shift-share regressor varies at the **sector level**: regions with
similar specialization share the same effective regressor, so their
residuals are correlated. Clustering regions by geography (state)
corrects only geographic correlation; the correlation that matters runs
through shared sectoral exposure — a clustering dimension the data hide
unless you aggregate the scores by sector.

The AKM variance estimator (their eq. 20, p. 1972), for the regression
Y_i = X_iβ + ε_i with X_i = Σ_s w_is X_s:

  V̂_AKM(β̂) = [ Σ_s X_s² R̂_s² ] / ( Σ_i X_i² )²,   R̂_s = Σ_i w_is ε̂_i.

R̂_s aggregates residuals to the sector level through the exposure
weights. With concentrated sectors (each region specializes in one
sector) this *reduces exactly to* a cluster-robust variance with clusters
= specialization sectors — the rule of thumb "cluster at the level the
regressor varies" made literal (p. 1973). The general form allows
arbitrary correlation of shocks within *clusters of sectors* and requires
independence only across those clusters (§IV.B).

## 3. AKM vs AKM0 (Remarks 5–6, pp. 1980–1981; §VI, Table II, pp. 1992–1994)

- **AKM** — the standard error of Remark 5: a Wald CI from V̂_AKM.
- **AKM0** — the confidence interval of Remark 6, obtained by inverting a
  test that imposes the null; its "effective standard error" (CI length ÷
  2·1.96) depends on the hypothesized β, so it is reported as a CI, not a
  pointwise SE.

Placebo rejection rates at nominal 5% (Table II, pp. 1993–1994): AKM
7.5–9.1%; **AKM0 4.3–4.5%** — near-exact. The two are asymptotically
equivalent; the gap is finite-sample size control, and imposing the null
helps (p. 1994). A reviewer seeing only "AKM" in a robustness table
should check which procedure and what CI construction.

The methods paper's trade-shock application (§VII.A, pp. 2000–2004): AKM
confidence intervals for the employment effects are wider than
state-clustered or robust CIs (the AKM0 CI much wider), but the
qualitative conclusions "remain valid at usual significance levels"
(p. 2003). For the inverse labor-supply elasticity (§VII.B) the AKM and
AKM0 CIs are "very similar to the state-clustered CI" with the Bartik IV
and "only moderately wider" with the trade-shock IV (p. 2006).

## 4. Validity conditions (§VI.B, pp. 1994–1995)

The procedures are valid in large samples only if:

(i) the number of sectors → ∞;
(ii) all sectors are asymptotically "small" (the largest sector cluster
    is asymptotically negligible — the "largest cluster" condition);
(iii) sectoral shocks are independent across sectors (clusters).

Given (i)–(iii) they remain valid under (iv) any distribution of the
sectoral shifters and (v) arbitrary correlation structure of the
regression residuals. Condition (ii) is where a dominant industry (e.g.
one sector carrying most of the weight) breaks the asymptotics — exactly
the case the battery's Rotemberg-concentration check is looking for, and
where the null-imposed score diagnostic in the skill is the fallback.

## Reviewer checklist

- Any exposure-weighted regressor → unit-level SEs (robust *or*
  geographic-cluster) are presumptively too short; quote the placebo
  rates, not intuition.
- Compute AKM and AKM0 (`ShiftShareSE` in R; `ssaggregate` in Stata) at
  the sector/shock level on the estimation file; report the CI, the
  effective SE, and which procedure produced it.
- If a paper's "AKM" row is only a Wald SE and the concentrated-shock
  case is live, run the null-imposed member too — it can move either way.
- Few effective sectors or a dominant one → conditions (i)–(ii) fail:
  say the AKM asymptotics are doubtful and report the uninformative-test
  result honestly (see the skill's capped-|t| discussion).
- Inference correction, not point-estimate correction: AKM/AKM0 change
  the uncertainty statement, never the β̂. For what the estimate is, see
  `gpss_2020_bartik_instrument.md`; for exogeneity of the shocks, see
  `bhj_2022_quasi_experimental_ssiv.md`.
