# Event-study binning and TWFE generalization — Schmidheiny & Siegloch (2023)

Working distillation of Kurt Schmidheiny and Sebastian Siegloch, "On
Event Studies and Distributed-Lags in Two-Way Fixed Effects Models:
Identification, Equivalence, and Generalization", *Journal of Applied
Econometrics* 38(5) (2023): 695–713. The source PDFs (not distributed with the skill):
`Schmidheiny_Siegloch_2023_EventStudy_JAE.pdf` (corrected author
version) **and** `..._published.pdf` (the published JAE article) — quote the published version.

## The three results

1. **Binning is a restriction, not a nuisance** (§2–3): pooling the
   tails of the event window (assuming constant effects for leads/lags
   beyond ±k) is what makes dynamic effects identified when there are
   no never-treated units. An unbinned ("fully saturated") event study
   with only treated/already-treated units is **underidentified** — the
   endpoint binning supplies the missing normalization. So "we bin at
   ±10" is an identifying assumption that should be defended (are
   effects really flat beyond 10?), not a footnote.
2. **Event study = distributed lag** (§4): with binned endpoints the
   two parameterizations are numerically identical after correct
   reparametrization. Any claim that one is "more flexible" than the
   other is a specification error, not a feature.
3. **Generalization to multi-valued/signed treatments** (§5): the
   framework extends to treatments that vary in intensity and sign
   (benefit-duration changes, dose variation) — the right baseline for
   the continuous-DiD literature (CGBS) when the treatment is
   multi-valued but still on a TWFE structure.

## Why the battery needs it

The DiD/event-study module had the staggered-timing literature
(Goodman-Bacon, CS, Sun–Abraham) but nothing on the **endpoint
convention** — and underidentified saturated models + unjustified
binning is a common silent failure in event-study figures. Also gives
the "is this TWFE event study even identified without never-treated"
check, which is distinct from the negative-weights problem.

## Review use

- `did-event-study-diagnostics`: for every event-study figure, ask
  (a) is there a never-treated group? if not, what is the binning
  normalization and is it defended? (b) are the binned endpoints
  plotted or suppressed? (c) if multiple event windows overlap
  (multiple events per unit), is the binning consistent across them?
- Pairs with the functional-form rows already added (Roth–Sant'Anna
  monotonic transform, McConnell levels-vs-logs): binning is the
  *time-domain* assumption; functional form is the *outcome-domain*
  one — a robust event study needs both defended.
