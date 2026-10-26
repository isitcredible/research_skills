# Detecting p-hacking — Elliott, Kudrin & Wüthrich (2022)

Working distillation of Graham Elliott, Nikolay Kudrin and Kaspar
Wüthrich, "Detecting p-Hacking", *Econometrica* 90(2) (2022): 887–906.
The source PDFs (not distributed with the skill): `Elliott_Kudrin_Wuthrich_2022_pHacking_
Econometrica.pdf` (arXiv) **and** `..._published.pdf` (the published
Econometrica article) — quote the published version.

## The results

1. **The null is characterized, not assumed** (§2): they derive the set
   of p-value distributions consistent with no p-hacking under general
   conditions — for t-tests, the p-curve is *completely monotone* with
   bounds on its magnitude and derivatives, a strictly stronger set of
   testable restrictions than the "non-increasing" shape the existing
   p-curve tests assume.
2. **More powerful tests** (§3–4): because the restrictions are
   tighter, their tests detect p-hacking in settings where the older
   tests (which just test non-increasingness) have no power — notably
   *specification search across independent tests*, which produces a
   non-increasing p-curve even under p-hacking, so the Simonsohn-style
   test misses it.
3. **Applied findings** (§5): they reject the no-p-hacking null on two
   large p-value datasets where the standard tests do not.

## Why the battery needs it

The skill's anomaly/integrity checks had no formal detection framework
for specification-search — which is exactly the failure mode a fragility
battery induces in a checked paper and the failure mode a reviewer
should suspect in a paper that survives a narrow band of
specifications. EKW tests run on p-values pooled across many studies
(journals, literatures); they are not a test of one paper's own
specification table, whose z-scores cluster around the baseline
estimate by construction. (EKW's own application handles within-paper
correlation by clustering and by subsampling one p-value per paper,
§5.1, p. 896.)

## Review use

- `claims`: the population-selection row — where the field's pooled
  p-curve violates the EKW restrictions, a marginal headline sits in a
  literature with detected specification search; that is a prior, not
  a finding about this paper.
- Not applicable to one paper's specification table: its z-scores are
  correlated draws around the baseline, so a cluster near the threshold
  is the expected shape, not the EKW signature. Within-paper search is
  priced by the specification sweep, not by these tests.
- Pairs with `andrews_kasy_2019_publication_bias.md`: A&K model which
  results get *published*; EKW detects which results got *produced* by
  searching — both across studies.
