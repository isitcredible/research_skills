# Good and bad controls: the 18-model catalog — Cinelli, Forney & Pearl (2024)

Working distillation of Carlos Cinelli, Andrew Forney and Judea Pearl,
"A Crash Course in Good and Bad Controls," *Sociological Methods &
Research* 53(3) (2024): 1071–1104 — the published article (DOI
10.1177/00491241221099552), not a working paper. Verified against the
published PDF (not distributed);
printed page = PDF page + 1071 (PDF p.1 = printed p. 1072). All cites
are to the printed page.

Use in this battery:

1. **The bad-control checks in `controls-samples-diagnostics`** — the
   model-by-model classification behind the M-bias / amplification /
   overcontrol / collider rows (§§1–2).
2. **Adjudicating "pre-treatment so it's safe" and "post-treatment so
   it's bad" claims** — both are false heuristics; the catalog gives the
   counterexamples (§3).

## 1. The classification standard (§2, pp. 1074–1076)

"Good control" = bias reduction; "bad control" = bias increase;
"neutral" = no asymptotic bias change (may still help or hurt
precision). Controlling for Z is a good control iff conditioning on it
leaves X and Y d-separated on all non-causal paths *and* leaves the
causal path untouched — i.e. the decision requires a causal model of
how Z sits relative to treatment and outcome. **Whether Z is measured
pre- or post-treatment is neither necessary nor sufficient** for the
classification (p. 1075) — the two folklore rules both fail in the
catalog.

## 2. The 18 models (§§3–4, pp. 1076–1082)

**Good controls — block a back-door:**

- **Models 1–3**: Z is a common cause (the textbook confounder), or not
  a common cause but still blocks the back-door path — e.g. Z a cause of
  X's parent or of Y's parent on the path (Figs. 1a–c).
- **Models 4–6**: same structures *with an unobserved confounder U
  present* — conditioning on Z still blocks the back-door even though
  U remains uncontrolled (Figs. 2a–c).

**Bad controls:**

- **Model 7 — M-bias** (pre-treatment!): Z is a common effect of
  unobserved causes of X and Y; conditioning on the collider opens the
  path X ← U1 → Z ← U2 → Y (Fig. 3). The canonical "pre-treatment is
  safe" counterexample (pp. 1077–1078).
- **Model 10 — bias amplification** (pre-treatment!): Z predicts X but
  has no path to Y except through an unobserved confounder U;
  conditioning on Z strips exogenous X-variation and *amplifies* the
  bias from U (Fig. 7, p. 1079). Near-instruments are the practical
  instance.
- **Models 11–12 — overcontrol**: Z is a mediator on the causal path
  (conditioning blocks the effect itself) or a descendant/proxy of the
  mediator (partial blocking) (Figs. 8a–b). Variant Fig. 9: when X's
  effect on Z has its own confounder, adjusting for Z can be
  appropriate — model detail matters.
- **Models 16–17 — selection/collider bias**: conditioning on Z (a
  descendant of X and of Y's causes, or a common effect of X and Y)
  opens colliding paths — classic selection bias; the military-records
  and prison-records examples (Figs. 12a–b, pp. 1081–1082).
- **Model 18 — case-control bias**: Z a descendant of the *outcome*
  (e.g. sampled on Y, or caused by Y); conditioning on a descendant of
  the collider Y biases the ACE — special case: under a true null
  effect, adjusting for Z is still valid for *testing* zero (p. 1082).

**Neutral controls:**

- **Model 8** — Z affects Y only: neutral for bias, *good* for
  precision (outcome-side control).
- **Model 9** — Z affects X only: neutral for bias, *bad* for precision
  — soaks up treatment variation (and becomes Model 10's amplifier if
  unobserved confounding exists).
- **Model 13** — Z a cause (not effect) of the mediator: neutral, may
  help precision — looks like Model 12 but the arrow direction saves it.
- **Models 14–15** — post-treatment Z caused by X only: neutral for
  bias, *bad* for precision (reduces X's variation); in Model 15 with
  selection on W (data conditioned on W = w), controlling Z can recover
  the effect by blocking the colliding path — a post-treatment control
  that helps (pp. 1080–1081).

## 3. The review-usable rules (pp. 1075–1082)

- The question is never "is Z a confounder" in the abstract — it is
  what conditioning on Z does to the paths between *this* X and *this*
  Y under the paper's causal structure.
- "Pre-treatment" fails both ways: Models 7 and 10 are pre-treatment
  bad controls; "post-treatment" fails too: Models 14–15 are
  post-treatment neutrals, and Model 15 is post-treatment *helpful*
  under selection.
- Precision ordering among valid controls: outcome-side (Model 8)
  helps; treatment-side (Model 9) hurts and is one unobserved
  confounder away from amplification (Model 10).
- The operational test the battery runs — remove the suspect control
  and watch which way β̂ moves — is the empirical complement; the
  classification tells you which removal to demand.

## Reviewer checklist

- For every contested control, name which catalog model the paper's
  causal structure implies; if the paper has no causal model, that is
  the finding.
- Flag "robust to kitchen-sink controls" where the added set contains
  plausible mediators (11–12), colliders (16–18), or strong
  treatment-predictors (10) — the robustness check can be manufacturing
  the bias.
- Single-group/single-unit dummies and post-outcome sample
  restrictions get the collider treatment (16–18) until the structure
  clears them.
- Report removals with direction: which way β̂ moves is evidence about
  what the control was doing; the catalog says which movement to expect.
