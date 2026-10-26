# Publication bias: identification and correction — Andrews & Kasy (2019)

Working distillation of Isaiah Andrews and Maximilian Kasy,
"Identification of and Correction for Publication Bias", *American
Economic Review* 109(8) (2019): 2766–2794. The source PDFs (not distributed with the skill):
`Andrews_Kasy_2019_PublicationBias_AER.pdf` (NBER WP 23298) **and**
`..._published.pdf` (the published AER article) — quote
the published version.

## The results

1. **Nonparametric identification of the publication-probability
   function** (§3): from systematic-replication data (paired
   original/replication estimates on the same protocol) or from
   meta-study data (estimates + SEs across studies), the conditional
   probability of publication given the study's results is identified
   up to scale — no parametric selection model needed. Symmetry
   violations in the original-vs-replication joint distribution, or
   the failure of high-variance estimates to be noisier versions of
   low-variance ones, identify selectivity.
2. **Corrected inference** (§4): median-unbiased estimators and valid
   confidence sets for each study's own parameter under known
   selectivity (the NBER WP 23298 adds Bonferroni-corrected CIs for an
   estimated selection model; the published version does not).
3. **The magnitudes are field-specific** (§III): on the Camerer et al.
   (lab experimental economics) and Open Science Collaboration
   (psychology) replication data, results significant at 5% are **over
   30× more likely to be published** than insignificant results; in the
   minimum-wage meta-study, negative significant estimates are **about
   3×** more likely to be published (pp. 2767–2768).

## Why the battery needs it

The skill had machinery for *within-paper* fragility but nothing for
the *population* selection problem: the estimate under review survived
a publication filter that prefers significance — ~30:1 in lab
replication data, ~3:1 in the minimum-wage literature. This is the
formal backing for "the published estimate is biased upward" as a
methodological prior rather than a rhetorical suspicion, and for the
meta-study trick of comparing a paper's z-score to its field's
selection function.

## Review use

- `claims`: the claim-calibration stage — is the headline estimate
  inside the region where selectivity operates (p < 0.05 on the nose)?
  A marginal-significance headline in a field with no registered
  reports is drawn from a heavily selected distribution.
- Across studies only: the meta-study route needs independent studies'
  estimates and SEs (Θ* independent of Σ* across latent studies, §II.B,
  p. 2774). One paper's specification table is not a mini meta-study —
  its z-scores cluster around the baseline by construction — so do not
  run it there.
- Pairs with `elliott_kudrin_wuthrich_2022_phacking.md`: A&K identify
  the *selection* side (which results get published); EKW identify the
  *production* side (which results get produced) — together they cover
  both margins of the publication filter.
