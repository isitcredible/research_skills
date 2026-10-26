# Heterogeneous treatment effects as mechanism tests — Fu & Slough (2026)

Working distillation of Jiawei Fu & Tara Slough, "Heterogeneous Treatment
Effects and Causal Mechanisms," *American Political Science Review* (2026):
1–18, doi:10.1017/S0003055426101580. Verified against the published
article (CUP typeset, APSR journal furniture on page 1; source PDF not distributed). Printed page = PDF page.

## The rule

Using a pretreatment-covariate interaction to claim a mechanism is
identified only under two **exclusion assumptions** on the moderator
X_k (pp. 7–8): (I) X_k does not moderate the treatment's *direct* effect;
(II) X_k does not moderate the indirect effect of any *other* mechanism.
Under both, a difference in CATEs equals the difference in the focal
mechanism's conditional average indirect effect — sufficient *and
generically necessary* (Prop. 1). Note the estimand is a *difference* of
indirect effects, never the indirect effect itself.

The inference is **asymmetric** (Table 2, p. 11):

- **HTEs present** (exclusion holds): the covariate is a mechanism
  detector variable (MDV) → mechanism active for at least one unit
  (Prop. 2). The standard reading survives — but only under exclusion.
- **HTEs absent**: uninformative. Three indistinguishable explanations
  (Prop. 3 + Cor. 1): the covariate is not an MDV (theory misspecified);
  the mechanism is active but homogeneous across units so *no* MDV
  exists; or the mechanism is inert. "No heterogeneity ⇒ mechanism
  ruled out" is invalid outright.
- **Outcome is a non-affine transform** (binning, dichotomization,
  Likert cut-points, log, winsorize): exclusion generically fails —
  the transform breaks additive separability of the mechanism from
  other mechanisms and from outcome predictors (pp. 8–9). HTEs then
  show only that the covariate predicts the outcome (Prop. 4); no
  HTEs is vacuous (Prop. 5).

Canonical artifact (Remark 2, pp. 4–5): binary vote choice is a
threshold transform of continuous utility, so ceiling/floor effects
make partisanship *appear* to moderate the corruption-information
effect although it moderates no mechanism — measurement-generated
heterogeneity. Their Monte Carlo (App. A3.3) is the sharper warning:
at skewed baseline support, a finite sample is *better powered* to
detect the spurious moderator than the real one.

Exclusion is not weaker than sequential ignorability — the two are
logically unordered, so HTE mechanism tests are *not* more agnostic
than mediation analysis (pp. 7–8). Prevalence stakes (Table 1): 56%
of quantitative articles in AJPS/APSR/JoP 2021 report HTEs; 95% of
those interpret them as mechanism evidence; 59% of those put the
mechanism claim in the abstract.

## Reviewer checklist distilled from the guidance (pp. 12–16)

- A mechanism-via-HTE claim must name: the candidate mechanism set,
  the exclusion assumptions per moderator, and the outcome→mechanism
  mapping. Unstated exclusion = unsupported claim, not "agnostic".
- Check the outcome: if it is a non-affine transform of the latent
  quantity the mechanism acts on, the interaction is uninformative
  about the mechanism (still fine for targeting/extrapolation/
  distributional claims — those do not need exclusion).
- Absence-of-HTE prose ("the effect does not vary with X, so channel
  M cannot be at work") gets no support without extra assumptions.
- The only clean fix for the null direction: multiple candidate MDVs
  for one mechanism — a hit on one + a miss on another confirms
  activation and indicts the miss as misspecification.
- Low interaction power (cf. Gelman–Stern crib, the ~16× heuristic)
  compounds the asymmetry: the informative direction is detection,
  so selective reporting loads false "mechanism active" findings
  (their fn. 18). Monotonicity of CATEs alone does not rescue
  mechanism inference (Prop. A7); random-utility recovery of the
  latent outcome or Bayesian CATE-magnitude models are the priced
  alternatives (Table 3).

## Uses in the review skill

- `paper`: the audit template for every "the effect is
  larger where X is high, consistent with mechanism M" sentence —
  demand the two exclusion assumptions by name and check whether the
  outcome is a non-affine transform of the construct the theory
  posits. Pairs with `cinelli_forney_pearl_2024_bad_controls.md`
  (moderator vs mediator vs collider) and
  `chen_roth_2024_logs_with_zeros.md` (the transform changes the
  estimand, not just the scale).
- `code-and-data` (significance contrasts /
  interaction claims): Gelman–Stern asks whether the difference is
  *real*; this crib asks what a real difference *licenses*.
  Constructive stress test: re-run the load-bearing interaction on
  the least-transformed outcome available, or simulate the
  ceiling/floor artifact — an "MDV" interaction that appears only on
  a bounded/dichotomized outcome is pathology evidence, not a
  mechanism finding.
- `claims`: two overclaim directions — presence-overclaim
  (exclusion unstated or transform-induced) and absence-overclaim
  ("rules out" a channel from null heterogeneity). The Table 1
  frequencies quantify how standard the move is.
- Sibling instrument: Blackwell, Ma & Opacic (2024), "Assumption
  Smuggling in Intermediate Outcome Tests" — the same audit for the
  *other* modal mechanism test (treatment effects on intermediate
  outcomes).
