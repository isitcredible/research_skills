# references/methods/

Method crib sheets consumed by the skill's checks — distilled,
page-referenced summaries of the canonical sources. Every file in this
folder and `shift_share/` is listed below.

Core single-source cribs (power, weak IV, sensitivity, functional form,
shift-share):

- `cohen_1988_effect_sizes.md` — the standardized effect-size index the
  test dictates (index, denominator, level of variation stated) and the
  power/MDE machinery behind every "could this design have detected it".
- `stock_yogo_2002_weak_instruments.md` — what the Stock–Yogo critical
  values test (relative bias, size distortion) and why "F > 10" is not
  the rule; i.i.d. errors only.
- `montiel_olea_pflueger_2013_weak_iv.md` — the effective F and its
  critical values for clustered, autocorrelated or heteroskedastic
  errors; auditing a printed "first-stage F > 10".
- `cinelli_hazlett_2020_sensitivity.md` — OVB sensitivity: robustness
  value, partial R², benchmark bounds; the same machinery on an IV
  exclusion restriction.
- `cinelli_forney_pearl_2024_bad_controls.md` — the good/bad-controls
  catalog behind the M-bias, amplification, overcontrol and collider
  checks; why "pre-treatment so it's safe" is a false heuristic.
- `oster_2013_unobservable_selection.md` — δ, Rmax and the bias-adjusted
  β for coefficient-movement-as-robustness claims; **version flag**: the
  WP's Rmax multiplier (2.2) differs from the published 1.3.
- `chen_roth_2024_logs_with_zeros.md` — log-like transforms of
  zero-valued outcomes: what a unit-rescaling sweep shows, and the
  alternative estimands to propose.
- `shift_share/akm_2019_shift_share_inference.md` — why unit-level
  clustering cannot fix a shift-share regression; what AKM/AKM0 compute.
- `shift_share/bhj_2022_quasi_experimental_ssiv.md` — shock exogeneity
  in quasi-experimental shift-share designs; the shock-level
  specification walk.
- `shift_share/borusyak_hull_2020_nonrandom_exposure.md` — non-random
  exposure to exogenous shocks; recentering and shock-counterfactual
  randomization inference.
- `shift_share/gpss_2020_bartik_instrument.md` — Rotemberg-weight
  concentration, the decomposition identity, shares-vs-shocks framing.

Selection, power and inference cribs:

- `gelman_carlin_2014_type_ms.md` — Type S and Type M (exaggeration)
  error rates from a design's power.
- `gelman_stern_2006_difference_test.md` — "significant vs not
  significant" is not a test of a difference; test the contrast.
- `gelman_loken_2013_forking_paths.md` — data-contingent analysis
  choices inflate error rates without any conscious fishing.
- `simmons_nelson_simonsohn_2011_false_positive.md` — undisclosed
  researcher degrees of freedom and the simulated false-positive rates
  they produce.
- `ioannidis_stanley_doucouliagos_2017_power_of_bias.md` — median power
  in economics literatures and the typical exaggeration of reported
  effects.
- `tosh_etal_2025_piranha.md` — many large effects on one outcome
  cannot coexist unless they are dependent.
- `olken_2015_preanalysis.md` — what a pre-analysis plan pins down and
  how to read deviations from it.
- `young_2019_channelling_fisher.md` — randomization tests against
  conventional inference in experiments; the larger loss of
  significance on joint tests.

Spurious-regression guides:

- `spurious_regressions_guide.md` — the temporal protocol: integration
  order, cointegration menu, Prais–Winsten/first-difference survival,
  ARDL bounds, holdouts, calibrated Monte Carlo.
- `spurious_space_time_unified_guide.md` — the space–time
  correspondence as one staged protocol: persistence diagnosis, the
  levels escape hatch, coefficient survival (Prais–Winsten path in time,
  half-life path in space), covariance-family adequacy, calibrated size
  and power, and the five-output report.

Multi-source guides added 2026-09-22 (all source-audited against
the published versions unless flagged in-file):

- `mackinnon_nielsen_webb_2023_few_clusters.md` — few/unequal clusters:
  Carter et al. G*, CV3 jackknife, WCR-S, tF/VtF sets.
- `did_event_study_guide.md` — DiD/event studies: estimand adjudication
  (Goodman-Bacon, dCDH, Sun–Abraham, Callaway–Sant'Anna), pre-test power
  (Roth), HonestDiD bounds (Rambachan–Roth), functional form
  (Roth–Sant'Anna), few treated clusters (Conley–Taber).
- `panel_methods_guide.md` — panels: CGM multiway, Driscoll–Kraay,
  Pesaran CD/CCE, Bai interactive FE, Mundlak margins, Nickell bias,
  Arellano–Bond diagnostics, Griliches–Hausman attenuation, Lee bounds.
- `synthetic_control_guide.md` — SC: ADH fit/placebos, Ferman spec
  searching, Kaul all-lags pathology, BMF augmentation, CWZ conformal,
  SDID.
- `rdd_methods_guide.md` — RDD spine and index of the RD cribs: CCT
  robust bias correction, GRR manipulation bounds (re-audited
  2026-10-15).
- `morgan_rubin_2012_rerandomization.md` — rerandomization/balance.
- `goldsmithpinkham_hull_kolesar_2024_contamination.md` — contamination
  bias; **interim, WP-audited** (published AER pending).
- `gelman_hullman_kennedy_2024_causal_quartets.md` — the same average
  treatment effect from constant, fanned or sign-reversing unit effects: an
  ATE alone does not license a population-wide story.
- `fu_slough_2026_hte_mechanisms.md` — HTE-as-mechanism-test: the two
  exclusion assumptions, the asymmetric inference (present HTE informs,
  absent HTE doesn't), and non-affine outcome transforms as a generator
  of uninformative heterogeneity.

Single-source cribs added 2026-09-28 (all audited; version status noted
in-file):

- `shift_share/bhj_2025_practical_guide.md` — the BHJ JEP checklist as
  decision rules: margin non-starters (few shifts / generic shares),
  share vintage and lagging, shift-level descriptives at the
  shift-cluster level, the shares-margin combination-sensitivity
  battery (overID, visual IV, many-weak-IV estimators).
- `hansen_2026_jackknife_se.md` — the replacement case for conventional
  CRVE: full worst-case downward bias vs the never-downward-biased
  modified jackknife; the no-discard modification under invertibility
  failures; Satterthwaite dof.
- `bellemare_wichman_2020_ihs_elasticities.md` — exact asinh elasticity
  formulas (the asinh–asinh coefficient is an elasticity only at large
  inputs), the min ≥ 10 / ≤ 1/3-zeros data rules, dummy-regressor
  percentage effects.
- `fitzgerald_etal_2026_loglike.md` — 46-paper record of log-like
  non-robustness: the sweet-spot diagnostic (scale as a researcher DF),
  compliance failure with the BW rules, and the harmonized alternatives
  (normalized estimands, Poisson, quantile regression).
- `mcconnell_2024_forest_logs.md` — levels vs logs DiD as different
  estimands (additive vs multiplicative trends), the sign-flip
  condition, the PPML-on-levels prescription.
- `jochmans_2022_iv_fe_count.md` — FE versions of the IV count-data
  estimators are inconsistent under fixed-T; the caveat that travels
  with any FE-IV-Poisson proposal.

Single-source cribs added 2026-10-01 (all-modules frontier audit — a
sweep beyond the trigger set that prompted it; all PDF-backed):

- `abadie_athey_imbens_wooldridge_2023_clustering.md` — clustering is a
  design problem (sampling/assignment), not a residual-correlation test;
  the finite-population correction when the sample is nearly the
  population of clusters.
- `weak_iv_guides_andrews_stock_sun_keane_neal.md` — ASS (2019) +
  Keane–Neal (2024): claim-matched F thresholds, the small-SE-under-
  contamination tell, AR/CLR as default even at strong F.
- `kitagawa_2015_instrument_validity.md` — the testable implications of
  IV validity with one discrete instrument (binary treatment); the
  "is it valid?" check where Sargan is vacuous.
- `kolesar_rothe_2018_discrete_rdd.md` — clustering by a discrete
  running variable does not fix misspecification; EHW as the width floor;
  narrow window first, then honest BSD/BME CIs (re-audited 2026-10-15).
- `pei_pischke_schwandt_2019_left_right.md` — noisy-proxy controls make
  RHS coefficient-stability near-uninformative; the LHS balancing test
  is more powerful.
- `schmidheiny_siegloch_2023_event_studies.md` — endpoint binning as the
  identifying restriction without never-treated; event-study ≡
  distributed-lag.
- `callaway_goodmanbacon_santanna_2024_continuous_did.md` — continuous
  treatments: contaminated TWFE dose coefficients even in 2×2; the
  selection-into-dose caveat on gradients.
- `olden_moen_2022_triple_difference.md` — DDD needs one parallel
  trend, not two — *in ratios*, on the differential between categories;
  the equal-bias cancellation is the assumption to defend.
- `cattaneo_feng_titiunik_2021_sc_intervals.md` — prediction intervals
  on the SC counterfactual; the CI the rank test doesn't supply.
- `eggers_tunon_dafoe_2024_placebo_tests.md` — placebo typology +
  sensitivity requirement; Hartman–Hidalgo equivalence testing (the
  backwards-null fix) in the same crib.
- `andrews_kasy_2019_publication_bias.md` — nonparametric selection
  identification; ~30× publication odds for significant results;
  corrected estimators.
- `elliott_kudrin_wuthrich_2022_phacking.md` — the characterized
  no-p-hacking null; tests with power against spec search where the
  old p-curve tests have none.
- `simonsohn_simmons_nelson_2020_spec_curve.md` — the multiverse +
  joint inference by under-null resampling: three test statistics
  (median effect, significant share, Stouffer mean Z), and the joint
  test self-corrects spec-level false-positive inflation.
- `clemens_2017_failed_replications.md` — verification vs reanalysis;
  what a failed replication may claim.
- `andrews_gentzkow_shapiro_2017_moment_sensitivity.md` — the Λ matrix:
  which moments carry a structural estimate; the nonlinear OVB formula.

RD cribs added 2026-10-15 (the rdpackages literature plus the
regression-kink papers; all source-audited, working papers flagged
in-file):

- `calonico_cattaneo_farrell_rbc_bandwidth.md` — CCT 2014, CCF 2018/
  2020/2022, the rdrobust Stata Journal article: which output row carries
  the verdict, MSE- vs CER-optimal bandwidths, selectors, clustering,
  recovering hidden quantities from printed output.
- `rd_practice_guide.md` — Cattaneo–Idrobo–Titiunik *Foundations* and
  *Extensions*, the Annual Review survey, the protocols comment: the
  falsification battery (covariates at their own bandwidths, one-sided
  placebo cutoffs, donut, small-range bandwidth sensitivity), fuzzy RD,
  what a protocol fixes in advance.
- `calonico_etal_2019_rd_covariates.md` — covariate-adjusted RD: same
  estimand only under balance; the exact adjusted–unadjusted identity;
  specifications that fail.
- `calonico_cattaneo_titiunik_2015_rd_plots.md` — RD plots: bin types and
  numbers, the global fit is not the estimate, how bins make or hide a
  jump.
- `cattaneo_jansson_ma_2020_density_test.md` — `rddensity`: robust row
  only, power and non-rejection, mass points, the binomial test.
- `rd_local_randomization_guide.md` — local randomization: the window
  estimand, window selection, nested-window sensitivity, `rdrbounds`,
  discrete scores.
- `rd_multiple_cutoffs_guide.md` — pooled multi-cutoff weights,
  cumulative cutoffs, multi-score designs, extrapolation away from the
  cutoff, `rdmulti`.
- `rd_boundary_designs_guide.md` — boundary designs: BATEC/WBATE/LBATE,
  kink bias of distance-based estimators, the pooled-specification
  taxonomy, compound treatments, `rd2d` (three of six sources are working
  papers).
- `calonico_etal_2025_rd_hte.md` — heterogeneous RD effects and `rdhte`
  (working paper).
- `cattaneo_titiunik_vazquezbare_2019_rd_power.md` — RD power and MDE;
  `rdpower`/`rdsampsi`/`rdmde`; the observed-power trap.
- `regression_kink_guide.md` — Card–Lee–Pei–Weber 2015 and Ganong–Jäger
  2018: the kink estimand, smoothness tests, order × selector grid, the
  placebo-kink permutation test.

Protocol crib added 2026-09-29:

- `koren_2026_theorist_toolbox.md` — LLM-assisted theory verification
  (arXiv:2606.22337v2 + the theorist-toolbox skills): the skip-words
  attack-surface checklist, briefing an adversarial pass (explore-framed,
  not verdict-framed), lead-not-verdict triage with its false-positive
  taxonomy, numerics as a standing gate, the three observed kill-shapes.
  Source is public (arXiv + GitHub); the paper's own math is
  unverified — techniques adopted on merit.

The source PDFs are **not distributed** — they are published articles or
working papers under their publishers' and authors' copyright. Each crib
records in its first paragraph which version it was verified against
(published vs working paper) and flags where the two differ.

These are the canonical cribs: there is no other copy. A change to one is a
suite change (version bump; a `spec-changes.csv` row if it alters what a run
must do).
