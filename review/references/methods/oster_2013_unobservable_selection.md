# Selection on observables: δ, Rmax, and the bias-adjusted β — Oster (2013/2019)

Working distillation of Emily Oster, "Unobservable Selection and
Coefficient Stability: Theory and Evidence." This crib was verified
against **the NBER working paper, w19054 (May 2013)**
(`Oster_2013_NBER_w19054_UnobservableSelection.pdf`, not distributed).
**Version flag, read first:** the published version is *Journal of
Business & Economic Statistics* 37(2) (2019): 187–204, and the headline
recommendation changed — the published paper's reporting standard is
δ = 1 with **Rmax = min(1.3·R̃, 1)**; the WP derives the cutoff
Π = 2.2, i.e. **Rmax = min(2.2·R̃, 1)** (§4, pp. 4–5). State which version
a claimed "Oster rule" comes from; the 1.3 multiplier is the published
one, not this document's.

Use in this battery:

1. **Coefficient-movement-as-robustness claims** — the paper's core
   result is that the heuristic is informative *only* under a stated
   proportionality assumption (§1); a review can demand the assumption
   be named.
2. **The OVB-sensitivity record** — δ and Rmax are the alternative
   sensitivity parametrization to Cinelli–Hazlett's partial R² (see
   `cinelli_hazlett_2020_sensitivity.md`); which one a paper reports,
   and with what Rmax bound, is a required field.

## 1. The framework (§§2–3)

Outcome Y = βX + W1 + W2 + ε: X the treatment, W1 the *observed*
controls, W2 the unobserved ones. The coefficient-movement heuristic —
"the estimate barely moved when controls were added" — is informative
about bias only if selection on observables is proportional to
selection on unobservables, with **δ the coefficient of
proportionality** (δ = 1: observables and unobservables equally
important in selection). Two ingredients govern the bias-adjusted
effect:

- **δ̃** — the proportionality after separating measurement error out
  (the WP unpacks δ into δ̃ and an error component, §2); bounded
  plausibly in [0,1].
- **Rmax** — the R² the regression would reach *if the unobservables
  were included*; bounded in [R̃, 1] where R̃ is the controlled R².

Proposition 1: given δ and Rmax, the bias-adjusted coefficient β* is a
closed-form function of the two observed regressions — short (β̊, R̊)
and long (β̃, R̃) — plus σ̂_yy (eq. for β*, §3; the δ = 1 branch reduces
to the familiar linear adjustment β* ≈ β̃ − δ(β̊ − β̃)(Rmax − R̃)/
(R̃ − R̊), the form implemented in `psacalc`/`robomit`). Inputs are
ordinary regression-table objects.

## 2. What justifies δ = 1 and the Rmax bound (§4)

- **Evidence on δ̃** (§4.1): estimating δ̃ for excluded control sets in
  real papers, **83% of values fall in [0,1]** — the empirical basis
  for bounding δ̃ at 1.
- **Evidence on Rmax** (§4.2–4.3): 33 randomized papers (AER/JPE/QJE/
  Econometrica/AEJ:Applied 2008–2013, 76 results) reporting coefficients
  with and without controls. Assuming Rmax = 1 would reject **30% of
  randomized results** — too harsh a standard. The Π value letting 95%
  of randomized results survive is **Π = 2.2** → the WP's recommended
  reporting set: **δ̃ ∈ [0,1], Rmax ∈ [R̃, min(2.2·R̃, 1)]** (the
  published 2019 revision tightens this to 1.3).
- About 40% of non-randomized results are robust even to Rmax = 1; ~65%
  survive the WP's bounding standard (abstract/§4).

## 3. What a review can and cannot demand

- The procedure is a **sensitivity exercise**: it assumes the
  proportional-selection link and a stated Rmax; it does not test
  whether selection on unobservables is actually proportional. A paper
  reporting only "the coefficient was stable" has run nothing.
- The two robustness definitions in the paper — the bias-adjusted β*
  excluding zero (point robustness) and the identified set under the
  δ̃, Rmax bounds excluding zero (set robustness) — give different
  answers; record which was used.
- Complement, don't substitute: Cinelli–Hazlett's RV quantifies the
  confounder strength needed to overturn; Oster's machinery quantifies
  what observed coefficient/R² movement implies about unobserved
  selection. They answer adjacent questions.

## Reviewer checklist

- A "coefficient stability" defense → require the proportional-selection
  assumption be stated, plus the inputs (β̊, R̊, β̃, R̃) and the assumed
  δ, Rmax.
- Quoted "Oster δ" or identified set → record the Rmax bound used and
  whether the paper says 1.3×R̃ (published convention) or 2.2×R̃
  (this WP); a set computed at Rmax = 1 alone is the harsh version that
  rejects 30% of RCTs.
- Software: Stata `psacalc`, R `robomit`; both implement the
  Proposition-1 adjustment.
- Randomized-treatment benchmark in the back of mind: if the method
  would kill a randomized result, the bound is too tight.
