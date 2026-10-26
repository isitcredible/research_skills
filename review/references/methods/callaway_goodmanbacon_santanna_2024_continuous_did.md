# DiD with a continuous treatment — Callaway, Goodman-Bacon & Sant'Anna (2025)

Working distillation of Brantly Callaway, Andrew Goodman-Bacon and
Pedro H. C. Sant'Anna, "Difference-in-Differences with a Continuous
Treatment", *American Economic Review* (forthcoming 2025). The source PDF (not
distributed with the skill) is the **January 2024 author draft**
(`Callaway_GoodmanBacon_SantAnna_2024_ContinuousDiD_arXiv.pdf`) —
published version forthcoming; verify numbering before quoting.

## The core results

Continuous ("dose") treatments — minimum wages, pollution exposure,
spending levels — are common but the binary-DiD toolkit doesn't carry
over (§§2–4):

1. **ATT-type parameters are identified** under a generalized parallel
   trends assumption (as in the binary case), but **comparisons across
   doses are not** — the difference between ATT(d) and ATT(d′) mixes
   the treatment effect with selection into dose, a selection bias
   parallel trends does not rule out. Stronger assumptions are needed
   to interpret the dose-response as causal.
2. **TWFE is hard to interpret even with two periods** (§3, Theorem
   3.4, Jan 2024 draft): as a summary of dose effects the linear TWFE
   coefficient "suffers from at least one of three problems: negative
   weights, selection bias, or non-intuitive weighting schemes" (§4
   opening). Which one depends on the building block: level-effect
   decompositions carry negative weights but no selection bias;
   cross-dose (causal-response, scaled 2×2) decompositions have
   positive weights but mix in selection bias under parallel trends
   alone. No staggering is needed.
3. **Alternative estimators** (§4): non-parametric/semi-parametric
   dose-response estimators that avoid the TWFE contamination; their
   application shows conclusions differ.

## Why the battery needs it

The DiD module covered staggered *binary* timing (Goodman-Bacon,
Callaway–Sant'Anna, Sun–Abraham) and functional form (Roth–Sant'Anna,
McConnell) but had nothing on **dose intensity as the treatment** — a
major share of applied "DiD" (every continuous policy variable). The
selection-into-dose point is the sharpest: a dose-response gradient is
not evidence of causality by itself, because the gradient reflects who
selected how much dose.

## Review use

- `did-event-study-diagnostics`: is the treatment continuous or
  multi-valued? If so, a TWFE dose coefficient is not interpretable as
  an average causal response even in 2×2. Ask for the CGBS estimators
  or a defensible discretization, and for a stated assumption that
  handles selection into dose.
- `shift-share-diagnostics`: shift-share designs are dose designs in
  disguise (county exposure = dose); the same selection-into-dose
  caveat applies to reading the gradient as causal.
- Pairs with `schmidheiny_siegloch_2023_event_studies.md` (which
  generalizes TWFE event studies to multi-valued treatments) — SS for
  the TWFE-side parameterization, CGBS for the causal-interpretation
  limits and alternative estimators.

## Companion: event studies with a staggered dose (AEA P&P 2024)

Callaway, Goodman-Bacon & Sant'Anna, "Event Studies with a Continuous
Treatment," *AEA Papers and Proceedings* 114 (2024): 601–605 (published;
`Callaway_GoodmanBacon_SantAnna_2024_EventStudiesContinuousTreatment_AEAPP.pdf`).
Under no anticipation, staggered adoption and ordinary parallel trends
(Assumption 4), Theorem 1: (i) the event-study ATT averaged over doses is
estimated with binary staggered estimators (Callaway–Sant'Anna, zero-dose
units labelled never-treated); (ii) a dose-band event study, by first
cutting the sample to the band plus zero-dose units; (iii) dose-response
curves averaged over an event-time window, on data balanced in event time.
ACR aggregations need the main paper's stronger assumption. They advise
watching the effective sample size in each dose band.
