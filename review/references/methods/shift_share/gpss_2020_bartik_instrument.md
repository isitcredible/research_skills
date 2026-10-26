# The Bartik instrument: equivalence, Rotemberg weights — Goldsmith-Pinkham, Sorkin & Swift (2020)

Working distillation of Paul Goldsmith-Pinkham, Isaac Sorkin and Henry
Swift, "Bartik Instruments: What, When, Why, and How," *American Economic
Review* 110(8) (2020): 2586–2624 — the published article (DOI
10.1257/aer.20181047), not a working paper. Verified against the
published PDF (not distributed); printed page = PDF page + 2585
(PDF p.1 = printed p. 2586). All cites below are to the printed page.

Use in this battery:

1. **Rotemberg-weight concentration** and the **decomposition identity**
   rows of `shift-share-diagnostics` — the formulas, the sign conventions,
   and what high-weight instruments must be defended against (§§2–4).
2. **The shares-vs-shocks identification framing** — Bartik can be read as
   either shares-as-instruments or shocks-as-exogenous; which reading a
   paper's claims need (§1).
3. **The diagnostic protocol to demand** — top-weight instruments,
   pretrends, over-ID among high-weight industries (§5).

## 1. Two equivalent views of the instrument (§§II–III, pp. 2587–2598)

The Bartik instrument B_l = Σ_k s_lk g_k (industry shares s_lk times
national shocks g_k) is **numerically equivalent** to the GMM estimator
that uses the K industry shares s_k as separate instruments with a
particular weight matrix (their eq. for the equivalence, §II). Two
identification readings follow:

- **Shares-as-instruments view** (the paper's primary lens): each share
  s_k is an instrument; validity = each share uncorrelated with the
  residual. This makes Bartik a many-instrument GMM problem.
- **Shock-exogeneity view** (BHJ 2022's lens, see
  `bhj_2022_quasi_experimental_ssiv.md`): the shocks g_k are
  quasi-randomly assigned and shares may be endogenous.

They are *observationally distinct identifying assumptions*, not two
names for one. Which a claim needs is decided by where the exogeneity
sits; the design-matrix's separation-of-exposure check exists to force
that question.

## 2. The Rotemberg decomposition (§IV, pp. 2598–2603)

Treating each industry share z_k = s_k as a just-identified instrument
yields per-instrument estimates β̂_k = (z_k'y)/(z_k'x). The Bartik/TSLS
estimator is exactly

  β̂_Bartik = Σ_k α̂_k β̂_k,   Σ_k α̂_k = 1,

the Rotemberg (1983) weights α̂_k ∝ ĝ_k·(kth instrument's first-stage
fitted contribution). **Weights sum to one but can be negative**; they
depend on the normalization of the shocks — GPSS report weights after
demeaning the (unweighted) industry shocks, and warn the weights are not
invariant to that convention (pp. 2602–2603 n./online App. E).

Appendix F relation (eq. 6, p. 2601): the relative first-stage
F-statistic on instrument k is proportional to its Rotemberg weight only
if the precision of its first-stage coefficient is proportional to the
instrument's variance; otherwise "the Rotemberg weight and relative
F-statistic will be less strongly related" (p. 2601) — so read both
rather than inferring first-stage strength from the weight.

## 3. Negative weights and interpretation (§IV.C–D, pp. 2601–2605)

- If the β̂_k are mutually similar, negative α̂_k do little damage.
- If the β̂_k are dispersed, negative α̂_k place negative weight on some
  underlying unit-level effects β_l: **the estimand need not be a convex
  average and admits no LATE-like interpretation** (pp. 2604–2605).
- Diagnostic they recommend: split instruments into positive- and
  negative-weight groups; report the share of total |α| that is negative
  and the sum of negative weights; check whether the high-positive-weight
  β̂_k bracket the headline.

## 4. What the application work shows (pp. 2589, 2605–2621)

- In the methods paper's canonical industry-shift application (inverse
  labor-supply elasticity, §VI, pp. 2608–2611; the trade-shock application
  is relegated to online Appendix Section A, p. 2590) the top five
  Rotemberg-weight industries carry over 40% of the positive weight
  (p. 2609), with oil and gas extraction first (p. 2611; also p. 2589),
  and the high-weight set is dominated by a handful of sectors — the headline
  estimate is effectively those comparisons. National industry growth
  rates explain **less than 1%** of the variance in Rotemberg weights:
  weight comes from the share geography × shock covariance, not from the
  shocks' sizes alone (p. 2589).
- In the Card (2009) immigrant-enclave application, the top-weight
  instrument differs by education group — for high-school-equivalent
  workers it is the Mexican-1980-enclave share; for college-equivalent a
  different one — so the "same instrument" is making different
  comparisons for different outcomes (pp. 2614–2618).
- Their Figure (the β̂_k vs α̂_k scatter, code in their posted package):
  points weighted by |α̂_k|, shaded by sign — the picture that shows which
  comparisons the estimate is.

## 5. The reporting protocol GPSS recommend (§V, pp. 2603–2605, 2621–2622)

1. Report the Rotemberg weights on the **estimation sample**; name the
   top positive and top negative weight instruments and say what
   comparison each is.
2. For the high-weight instruments: show β̂_k, first-stage Fs, pretrends,
   and covariate balance *at the industry level*.
3. Overidentification/testing among the high-weight subset, not only the
   full instrument set.
4. Sensitivity to dropping the top-weight industries (a shock-level
   leave-out, not a unit-level one).

## Reviewer checklist

- Compute α̂_k on the exact estimation sample (weights move across
  columns and subsamples); verify Σα̂_k = 1 and that Σα̂_kβ̂_k reproduces
  the printed coefficient.
- Report: top-5 positive and top-5 negative α̂_k with industry names and
  the sum of negative weights. The effective number of shocks is a
  different object: 1/Σ_k s̄_k² over the shocks' average exposure weights
  (BHJ 2022, Table 1), not over the Rotemberg weights.
- Any paper defending "the shocks are exogenous" must still answer for
  the specific high-weight industries — shock exogeneity is claimed
  *on average* over k; the estimate lives in the top few k.
- A symmetric roster of "robust SEs" without the high-weight-instrument
  diagnostics has not answered the Rotemberg question.
- For inference at the shock level see `akm_2019_shift_share_inference.md`;
  for the identification walk (sum-of-shares, period interactions) see
  `bhj_2022_quasi_experimental_ssiv.md`.
