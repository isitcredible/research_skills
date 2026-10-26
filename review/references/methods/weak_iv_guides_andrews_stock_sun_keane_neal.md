# Weak-IV practical guides — Andrews, Stock & Sun (2019); Keane & Neal (2024)

Working distillation of two survey guides for the weak-instrument
battery. Anno-notation: page/section references are to the audited copies.

- **Andrews, Stock & Sun, "Weak Instruments in Instrumental Variables
  Regression: Theory and Practice", *Annual Review of Economics* 11
  (2019): 727–753** — the published typeset (not distributed with the skill)
  (`Andrews_Stock_Sun_2019_WeakIV_AnnuRev.pdf`). The synthesis survey of the modern weak-IV literature with
  an explicit **nonhomoskedastic emphasis** (heteroskedastic,
  serially-correlated, clustered data — the case that applies in
  practice): first-stage diagnostics matched to the error structure —
  their headline recommendation is the **Montiel Olea–Pflueger
  effective F** for judging strength — and **AR confidence intervals
  "efficient regardless of the strength of the instruments, and so
  should be reported regardless of the value of the first-stage F"**
  (§"Recommendations", verified). Their AER-2014–18 tabulation shows
  reported first-stage F statistics cluster below 50 — weak-IV is the
  norm, not the exception. The skill's
  `mackinnon_nielsen_webb_2023_few_clusters.md` (tF/VtF) and MOP cribs cover the specific
  estimators; ASS is the map of the whole territory and the standard
  cite for "F > 10 is not sufficient."
- **Keane & Neal, "A Practical Guide to Weak Instruments", *Annual
  Review of Economics* 16 (2024): 185–212** — source PDFs (not distributed with the skill):
  `Keane_Neal_2024_WeakInstruments_AnnuRev.pdf` (UNSW working-paper
  version, June 2022 draft) **and**
  `Keane_Neal_2024_WeakInstruments_AnnuRev_published.pdf` (the
  published Annu. Rev. article) — quote the published
  version. Adds the sharpest applied warnings since ASS; the
  load-bearing results below are from the WP text (§§1–5). Companion
  code paper: Keane & Neal (2023), "Instrument strength in IV estimation
  and inference: a guide to theory and practice", *Journal of
  Econometrics* 235(2): 1625–1653.

## What KN adds beyond the F > 10 rule

1. **The contaminated-subsample power asymmetry** (their core applied
   point, §§3–4). 2SLS standard errors tend to be *artificially small*
   in precisely the samples where the 2SLS estimate is most contaminated
   by OLS bias. If OLS bias is positive, the t-test has *inflated power
   to detect false-positive effects* — and the problem "persists even
   if the first-stage F is in the thousands." Operational tell for
   review: an IV estimate that lands near the OLS point estimate with a
   *smaller* standard error is the signature of this failure mode, not
   evidence of IV precision. (Pairs with the IV-SE-below-OLS-SE check
   already in `iv-diagnostics`.)
2. **F thresholds matched to the claim** (§5). F > 10 renders *size
   distortion* modest — nothing more. For "2SLS is reliably better than
   OLS" in the returns-to-education archetype they argue F ≥ 50 is
   needed; Lee et al. (2022) show F > 104.7 to guarantee t-test size at
   the correct 5% rate. Review rule: quote the threshold relative to the
   claim being defended — size control (tF-adjusted), bias relative to
   OLS (10% worst-case → much higher F), or worst-case bias.
3. **AR-type tests as default** (§4). Anderson–Rubin (or CLR where
   available) should be used *in lieu of the t-test even with strong
   instruments*, because the t-test's failure is not monotone in F. A
   review that sees only t/Wald IV output can demand AR CIs whatever the
   first stage says; F-adjusted p-values (tF) are the minimal bar.
4. **Effective-F / matched diagnostics** (ASS; Olea–Pflueger). Report the
   first-stage statistic matched to the variance structure — with one
   endogenous regressor, the Montiel Olea–Pflueger effective F under
   robust/clustered errors (see `montiel_olea_pflueger_2013_weak_iv.md`;
   it equals the robust and Kleibergen–Paap F only when just-identified,
   ASS p. 738), Cragg–Donald under i.i.d. MOP does not cover multiple
   endogenous regressors (ASS fn. 4, p. 739: no analog known); the
   extension there is Lewis–Mertens.

## Where these fit the battery

- `iv-diagnostics`: the SE-precision tell, the claim-matched F
  thresholds, and AR-instead-of-t as the default inference row.
- `shift-share-diagnostics`: BHJ-2025 shares-margin diagnostics sit on
  the same scale — the effective-F convention there (F_eff via
  AKM/AKM0 weighting) is the shift-share instance of "match the
  first-stage statistic to the design."
- The tF/VtF tables themselves are in Lee, McCrary, Moreira & Porter (2022)
  and Lee, McCrary, Moreira, Porter & Yap (2023); the rules used here are in
  `mackinnon_nielsen_webb_2023_few_clusters.md`.
