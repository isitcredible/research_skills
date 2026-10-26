# Inference with a discrete running variable — Kolesár & Rothe (2018)

Working distillation of Michal Kolesár and Christoph Rothe, "Inference
in Regression Discontinuity Designs with a Discrete Running Variable",
*American Economic Review* 108(8) (2018): 2277–2304. The source PDFs
(not distributed with the skill):
`Kolesar_Rothe_2018_DiscreteRDD_AER_published.pdf` (the published
AER article) **and** `Kolesar_Rothe_2018_DiscreteRDD_AER.pdf` (Nov 2017
author draft) — quote the published version. The online appendix (the
lower-bound estimate for K and the proofs) was not audited.

Verification status: source-audited 2026-10-15.

Use in this battery: `rdd-diagnostics` — the discrete-running-variable
row of the local-randomization check and any paper that clusters standard
errors by the running variable. Pairs with `rd_local_randomization_guide.md`
§7 (the Cattaneo group's route for discrete scores).

## The setting

A researcher-chosen window around the cutoff, a local linear (or other
low-order) fit, and inference justified by assuming the specification
bias is negligible (pp. 2277–2278, 2287). With a running variable that
takes few values near the cutoff (age in years, test-score bins, seats
won), the window must be wide enough to contain several support points,
so the bias is not negligible. This is a different problem from a
continuous latent score recorded with rounding, which is measurement
error (p. 2278 n. 2, citing Dong 2015).

## Clustering by the running variable does not fix it

Lee and Card (2008) proposed clustering standard errors by the running
variable (CRV). KR show (§§2–3):

- The Lee–Card random-specification-error model that motivates CRV is a
  heuristic incompatible with i.i.d. sampling (pp. 2288–2289).
- When misspecification is small to moderate and the number of support
  points is small to moderate, CRV standard errors are on average
  *smaller* than the unclustered Eicker–Huber–White (EHW) ones, because of
  a negative few-clusters term; CRV intervals then undercover even under
  correct specification (pp. 2284, 2290–2291). In their CPS placebo study
  CRV coverage of a nominal 95% interval is as low as 58 percent, while
  EHW intervals come much closer to 95 percent (p. 2279).
- In their application, KR's results imply "that any CI with correct
  coverage must be at least as wide as the EHW CI" (p. 2299). Where the EHW
  interval covers zero, a CRV-based significance claim is incorrect.

## The remedies, in order (pp. 2302–2303)

1. **Rich support near the cutoff:** there is no need to treat discrete
   and continuous scores differently. Shrink the window until the bias is
   negligible and use EHW standard errors.
2. **Too few support points for that:** use an honest confidence interval
   with guaranteed coverage under an explicit restriction on the
   conditional expectation function (§4):
   - **BSD** (bounded second derivative): a curvature bound K on the CEF.
     The interval uses a nearest-neighbour variance, the worst-case bias
     attained at μ(x) = ∓(1/2)Kx², and a bandwidth chosen to minimise length
     without losing honesty (pp. 2293–2295). K must come from subject
     knowledge: if the CEF departs by no more than S from a straight line
     over any interval of length 1, K = 8S is reasonable (p. 2295). K
     cannot be bounded above from the data; it can only be bounded below,
     which gives a specification check (p. 2295).
   - **BME** (bounded misspecification error): the specification bias at
     the cutoff is no larger than the largest at any support point in the
     window on that side. It needs many observations per support point and
     is not recommended when cell means are noisy relative to the bias or
     the window holds many support points (pp. 2295, 2297); in their
     Lalive application it is nearly uninformative (p. 2302).
3. Report the bound assumption with the interval. The honest-CI machinery
   is the RD instance of the Armstrong–Kolesár program and is implemented
   in the `RDHonest` package (p. 2280 n. 4).

The Cattaneo group's alternative (Annual Review of Economics 2022,
pp. 840, 842): uniform-in-bias methods such as BSD need a manually set
smoothness constant, which they regard as equivalent to choosing the
bandwidth by hand; with few mass points they make local randomization the
primary analysis (`rd_local_randomization_guide.md` §7). Either route is
defensible; a CRV interval alone is not.

## Review use

- **Trigger:** count the distinct running-variable values within the
  paper's window on each side. A paper that clusters by the running
  variable, or a discrete score with a moderate number of support points,
  fires this row.
- **CRV versus EHW:** recompute EHW standard errors. If significance holds
  only under the CRV interval, the significance claim fails.
- **Remedy check:** with rich support, ask for the narrow-window EHW
  estimate. With sparse support, ask for a BSD interval over a stated range
  of K with its justification, or a local-randomization analysis in the
  smallest window. The absence of a KR interval is not a failure when the
  paper uses local randomization with few mass points.
- **Effective sample:** with a discrete score, the number of support points
  governs CRV behaviour and, for local polynomial fits, the effective
  sample (the latter is the Cattaneo group's point, Extensions pp. 61, 69);
  EHW and BSD inference still use N.
- `small-n-diagnostics`: few support points near the cutoff is a
  small-effective-sample problem in the running-variable dimension.
