# Levels vs logs in DiD — McConnell (2024)

Working distillation of Brendon McConnell, "Can't See the Forest for the
Logs: On the Perils of Using Difference-in-Differences with a
Log-Dependent Variable," **working paper** (February 2024 version audited:
`McConnell_2024_Forest_Logs_logDD_wp.pdf`, not distributed with the skill; unpublished — cite
by section, verify before quoting numbers).

Use in this battery:

1. **The functional-form row** of `did_event_study_guide.md` — the
   levels-vs-logs DiD estimand distinction and the sign-flip condition
   (§§1–2).
2. **The prescription** — how to pick the transform and what to run when
   the model is multiplicative (§3).

## 1. The two estimands (§§2–3)

A levels DiD identifies the *difference of level differences* — an
additive model of trends. A log-dependent-variable DiD identifies the
*difference of proportional growth rates* — a multiplicative model.
These are different estimands, not the same estimand in different
units: PT in levels means equal additive trends; PT in logs means equal
*growth* trends. One can hold while the other fails, and either
direction of failure is possible.

## 2. The sign-flip condition (§3)

When baseline outcome distributions differ sufficiently between treated
and control groups, the levels and logs DiD estimates can take
**opposite signs**: if the secular trend lifts all outcomes while the
treated group starts far lower, the additive gap can move one way while
the proportional gap moves the other. The paper gives the exact
sufficient condition in terms of the aggregate time effect and the
baseline mean gap. Review use: a headline result whose sign flips
between levels and logs is not "robust to functional form" nor
"uncertain" — it is two different answers to two different questions,
and the scale choice must be argued, not averaged.

## 3. The prescription (§4)

- Choose additive vs multiplicative parallel trends **a priori from the
  economic model** — not by estimating pre-trends in both scales and
  reporting whichever passes. The pretest-first workflow is a researcher
  degree of freedom on the scale axis (the same family of problem as
  Chen–Roth's units dependence and Fitzgerald et al.'s sweet spot).
- If the defensible model is multiplicative, keep the outcome **in
  levels and estimate by PPML** — that preserves a multiplicative
  structure on an untransformed outcome and sidesteps the log-of-zero
  and transform-dependence issues entirely.
- Companion results, not substitutes: Roth & Sant'Anna (2023) show PT
  holds under all strictly monotonic transforms only under a strong CDF
  condition (see the DiD guide §4); Chen & Roth (2024) show the log-like
  estimand is unit-dependent under zeros. McConnell adds: even *without*
  zeros, levels and logs are different estimands that can disagree in
  sign.

## Reviewer checklist

- A DiD on a log-like outcome carries an implicit multiplicative-PT
  claim; demand its defense, or run the sign-check between levels and
  logs and report when they disagree.
- "We also show the specification in levels/logs" is not a robustness
  check of one estimand — it is a second estimand; adjudicate which one
  the paper's claims need.
- A multiplicative-model recommendation should point to PPML-on-levels,
  not to log(Y+c) — and where the design is IV with unit FE, carry the
  Jochmans (2022) caveat (`jochmans_2022_iv_fe_count.md`).
