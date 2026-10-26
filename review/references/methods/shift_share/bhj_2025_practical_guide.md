# A Practical Guide to Shift-Share Instruments — Borusyak, Hull & Jaravel (2025)

Working distillation of Kirill Borusyak, Peter Hull and Xavier Jaravel,
"A Practical Guide to Shift-Share Instruments," *Journal of Economic
Perspectives* 39(1) (2025): 181–204 — the published article (DOI
10.1257/jep.20231370). The PDF (`Borusyak_2025_PracticalGuide.pdf`, not distributed with the skill);
printed page = PDF page + 180 (PDF p.1 = printed p. 181).
All cites below are to the printed page.

Use in this battery:

1. **The margin-adjudication row** of `shift-share-diagnostics` — the
   guide is the current canonical statement of which identifying margin
   a shift-share design can claim, and the "non-starter" conditions for
   each (§§1–2).
2. **The share-vintage and tailored-shares checks** — guidance on when
   lagging/constructing shares actually helps, which none of the four
   source cribs state as decision rules (§3).
3. **The shares-margin sensitivity battery** — overidentification, the
   visual-IV plot, and the many-weak-IV estimators to demand when a
   design pools share instruments (§4).
4. **Shift-level descriptives and clustering of correlated shifts** —
   the effective-number-of-shifts diagnostic stated as a reporting
   requirement, including its shift-cluster extension (§5).

## 1. The two paths and their non-starters (pp. 185–189, 203)

Two distinct routes to exogeneity of z_i = Σ_k s_ik g_k, summarized in
their Table 2 (p. 190):

- **Many exogenous shifts** (BHJ 2022 / AKM 2019): the shifts are
  as-if-randomly assigned and affect outcomes only through the
  treatment. Requires *many* shifts — a handful of shifts cannot support
  a law of large numbers regardless of unit count (fn 1, p. 187) — and
  complete shares (else the instrument loads on the share sum itself;
  control S_i = Σ_k s_ik, p. 191).
- **Exogenous shares** (GPSS 2020): each share satisfies a
  parallel-trends-type condition — units more vs less exposed to k would
  have trended the same absent the treatment. The instrument pools K
  one-at-a-time share instruments; the shifts only set the weights
  (pp. 188–189).

Non-starters: too few shifts kills the shifts margin; **generic shares
kill the shares margin** — shares measuring a unit's exposure to many
types of shocks (e.g. local industrial composition) cannot be defended
as exogenous instruments for one specific treatment, because any
unobserved shock loading on the same shares violates parallel trends
(pp. 188, 196–197). Shares must be "tailored" to the treatment —
capturing exposure to the shocks that move x_i and little else.

## 2. The shifts checklist (pp. 189–195)

1. **Name the idealized shift-level experiment** and the confounders it
   is meant to escape — a design that cannot describe the lottery is
   not identified from shifts.
2. **Bridge observed-to-ideal shifts with controls at the right level.**
   Shift-level confounders q_k enter the unit-level regression as their
   exposure-weighted aggregate Σ_k s_ik q_k (not as unit-level controls);
   unit-level confounders enter directly (pp. 190–191).
3. **Incomplete shares → control S_i** — and in panels, S_i × period:
   the canonical fix is the period-interacted base share *in the
   period shares are measured* (lagged like the shares themselves)
   (pp. 195–196; the BHJ 2022 Col 1→2→3 walk).
4. **Lag shares to the *start of the natural experiment*** (p. 191):
   with serially correlated shifts, lag to the first period of the
   sequence — or extract unpredictable innovations. Lagging further than
   needed costs power; lagging too little lets shifts contaminate
   shares. Lagging does NOT address dynamic effects of past shifts on
   current outcomes (Jaeger, Ruist & Stuhler 2018; OA A.1).
5. **Report shift-level descriptives**: the distribution of g_k and its
   exposure-weighted version, and the **effective number of shifts** —
   inverse Herfindahl of the importance weights s̄_k = (1/N)Σ_i s_ik.
   If shifts correlate within shift-clusters, compute the Herfindahl at
   the cluster level — many correlated shifts are not many shifts
   (fn 6, p. 192).
6. **Balance tests on both levels**: instrument on unit-level
   predetermineds incl. lagged outcome (pretrends); *shifts* on
   shift-level proxies for confounders (pp. 192–193).
7. **Exposure-robust inference**: AKM variance, or the equivalent
   shift-level 2SLS — same coefficient as the unit-level regression,
   weighted by s̄_k, valid SEs estimated at the level shifts are
   assigned (`ssaggregate` automates the outcome/treatment transforms;
   accommodates shift clustering, spatial dependence, serial
   correlation, and a shift-level first-stage F) (pp. 193–194, fn 7).
   Sensitivity: alternative control sets (different conditional
   quasi-randomness assumptions) and unit-level importance weights.

## 3. Share vintage and tailoring (pp. 188–189, 196–197)

- **Lagging shares is not a panacea**: it weakens the instrument and
  only helps if it plausibly reduces cov(share, ε) by *more* than it
  reduces cov(share, x) — the paper must argue this, not assert it.
  Requires transitory shocks attracting treatment AND persistent
  share-setting channels (Card 2009 logic, p. 197).
- **Strengthening a shares claim**: replace generic or endogeneity-
  exposed shares with the component arising from specific
  quasi-experiments. The guide's example (Terry, Chaney, Burchardi,
  Tarquinio & Hassan, 2023 WP; AER 2026) builds shares from the timing
  coincidence of historical migration waves and regional growth
  (pp. 196–197). **Reviewer note: the guide cites this construction
  approvingly as a tailored-shares improvement — whether it actually
  delivers exogenous shares is exactly what a review must test (one line of
  critique: shares built from a generic pull component can load
  mechanically on unit size).**
- **Time-updated shares reimport endogeneity**: shares measured after
  the experiment's start can themselves be moved by the shocks — a
  stronger first stage from updated shares can be the contamination
  the instrument exists to avoid (fn 5, p. 191). Run fixed-at-baseline
  and updated versions and diagnose which assumption each relies on.

## 4. The shares checklist (pp. 196–199)

1. **Tailored shares** (non-starter if generic — §1).
2. **Unit-level controls**: e.g. the total initial share controls the
   extensive margin so the instrument leverages only the *composition*
   of exposure (p. 197).
3. **Which shares carry the estimate** — Rotemberg weights
   (`bartik_weight` in Stata/R); non-unique under complete shares — use
   the demeaned-shifts convention (fn 9, p. 198). Concentrate balance
   tests on the high-weight shares.
4. **Balance tests on individual shares**: pre-period outcomes, baseline
   characteristics, contemporaneous placebo outcomes. Pretrends pass
   more easily when shares changed drastically since the pre-period or
   no same-type shocks occurred earlier — a passing pretrend under those
   conditions is weaker evidence than it looks (Jaeger–Ruist–Stuhler
   caveat, p. 198).
5. **Combination sensitivity** — under share exogeneity the model is
   overidentified and the pooling is a researcher's choice (pp. 198–199):
   - Sargan–Hansen overID test on the individual share instruments;
   - **Visual IV**: reduced-form vs first-stage coefficients per share
     should lie on a ray through the origin (Angrist–Pischke plot; the
     shift-share estimate is a weighted regression of the RF on the FS
     coefficients, OA B.2);
   - GPSS scatter: per-share β̂_k vs first-stage F — the high-F,
     high-Rotemberg estimates should agree;
   - Alternative combinations/estimators: top-Rotemberg shares alone;
     and under many shares the many-weak-IV robust estimators — JIVE
     (Angrist–Imbens–Krueger), LIML, heteroskedasticity-robust Fuller
     (Hausman et al. 2012), modified bias-corrected 2SLS (Kolesár et al.
     2015).
   - **Failure interpretation splits on homogeneity**: if effects are
     homogeneous, failed combination tests mean share exogeneity fails;
     with heterogeneous effects the same failure can be interpretation,
     not violation — correlated share instruments do not generally
     deliver a complier average (Mogstad–Torgovitsky–Walters 2021).

## 5. Leave-out and in-sample shifts (p. 199 fn 11, OA A.12)

When the shifts themselves are estimated in-sample (the Bartik-1991
national-growth case), the estimator needs a bias correction — the
leave-out shift-share construction. Whether a leave-out construction
helps depends on what contamination it removes.

## Reviewer checklist

- Adjudicate the margin first; both margins have a named non-starter
  (few shifts / generic shares). A design can fail both.
- Shifts margin: completeness → S_i (×period in panels); shift-level
  descriptives incl. effective shifts at the shift-cluster level;
  balance at both levels; exposure-robust SEs or the equivalent
  shift-level IV with its own first-stage F.
- Shares margin: tailored? which shares carry it (Rotemberg); balance
  on the high-weight shares; combination sensitivity incl. a
  many-weak-IV-robust estimator when K is large; JRS caveat on
  comforting pretrends.
- Share vintage: baseline-fixed vs updated each answer different
  assumptions — demand the reason any update helps identification
  rather than power.
- For the mechanics underneath each item see the source cribs:
  `gpss_2020_bartik_instrument.md`,
  `bhj_2022_quasi_experimental_ssiv.md`,
  `akm_2019_shift_share_inference.md`,
  `borusyak_hull_2020_nonrandom_exposure.md`.
