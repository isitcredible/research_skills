# LHS vs RHS confounder tests — Pei, Pischke & Schwandt (2019)

Working distillation of Zhuan Pei, Jörn-Steffen Pischke and Hannes
Schwandt, "Poorly Measured Confounders Are More Useful on the Left
Than on the Right", *Journal of Business & Economic Statistics* 37(2)
(2019): 205–216. The source PDFs (not distributed with the skill):
`Pei_Pischke_Schwandt_2019_LeftRight_JBES_published.pdf` (the published
JBES article — note the published DOI is 10.1080/07350015.2018.1462710)
**and** `Pei_Pischke_Schwandt_2019_LeftRight_JBES.pdf` (IZA DP 10647,
March 2017) — quote the published version.

## The result

Two canonical ways to test whether an observed proxy for a confounder
threatens identification:

- **RHS / coefficient-comparison test**: add the proxy as a regressor;
  the identifying assumption "passes" if β̂ on the treatment is stable.
- **LHS / balancing test**: regress the proxy on the treatment; the
  identifying assumption passes if the coefficient is zero.

PPS show the LHS test is **generally more powerful** (§§2–3,
derivations + power calculations). The reason is mechanical: when the
proxy is a noisy measure of the true confounder, attenuation shrinks
the RHS coefficient movement toward zero — stability of β̂ under
control addition is *expected even when the design is confounded*,
because the mismeasured control can't absorb the confounding. The LHS
regression instead asks "does treatment predict the proxy?" — a
direct test of balance that measurement error attenuates in the same
proportion on both sides, so it retains power.

## Why the battery needs it

The "coefficient is stable when controls are added" check is ubiquitous
and treated as strong evidence. PPS shows it is **weak evidence when the
controls are noisy proxies** — which is most of them (industry
dummies for skill, lagged outcomes for the persistent component of
confounding, etc.). The review corollary: an invariant coefficient under
progressive control addition is not informative about identification
unless the added controls measure the confounders *well*.

## Review use

- `controls-samples-diagnostics`: where the paper's identification
  argument leans on coefficient stability under control additions, ask
  whether a balancing test (proxy on LHS) was run or could be. If the
  only evidence is RHS stability with proxies that are plausibly poor
  measures, the stability is near-uninformative.
- `did-event-study-diagnostics` / `iv-diagnostics`: same logic applies
  to conditional parallel trends and instrument-balance checks —
  adding a noisy "pretrend proxy" control and finding β stable is the
  RHS version; testing whether treatment predicts the pretrend *level*
  is the LHS version.
- Distinguish from the Oster (2019) δ-machinery in
  `oster_2013_unobservable_selection.md`: Oster asks "how strong would
  selection on unobservables have to be" (a sensitivity bound); PPS
  asks "does adding the observed proxy even test anything" (a power
  statement). Complementary, not substitutes.
