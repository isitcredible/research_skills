# The triple difference estimator — Olden & Møen (2022)

Working distillation of Andreas Olden and Jarle Møen, "The Triple
Difference Estimator", *Econometrics Journal* 25(3) (2022): 531–553.
The source PDF (not distributed with the skill) is the **published article**
(`Olden_Moen_2022_TripleDifference_EctJ.pdf`).

## The result — stated precisely (Summary + §5)

DDD is computable as the difference between two DiD estimators, but
does **not** require two parallel-trend assumptions for a causal
interpretation: *"the difference between two biased
difference-in-differences estimators will be unbiased as long as the
bias is the same in both estimators"* — the bias is differenced out —
and that equality requires **only one parallel trend assumption, in
ratios**: a parallel trend on the *differential* between the two
categories, not on the two outcomes separately. Equivalently (§6):
DDD can be viewed as a DiD using the **ratio between two categories**
as the outcome — and choosing between DDD and DiD-on-a-ratio turns on
assumptions a DDD does not in general need. Their survey of
top-journal usage: the identifying assumptions are "neither formally
derived nor generally agreed on" — most DDD applications run on
intuition.

## Why the battery needs it

The DiD module had the staggered/functional-form literature but nothing
on DDD — a ubiquitous specification (group × post × eligibility
margin) that reviewers evaluate with the wrong intuitions, *in both
directions*: (a) a DDD is not "DiD but weaker" — the sole purpose of
the second differencing is to remove the first DiD's bias, so DDD can
be *stronger*; (b) but the cancellation needs the bias to be *the same
in both estimators* — a DDD is fragile precisely where the violation
differs across the third margin (their "no other factors generating a
difference in differential trends" — the common-acceleration
condition, §5).

## Review use

- `did-event-study-diagnostics`: when a DDD appears, ask (i) which
  single ratio-parallel-trend is load-bearing — the differential
  between categories must trend in parallel, not each outcome; (ii) is
  the equal-bias condition defensible — would the selection/violation
  differ across the third margin? A "three differences so it's robust"
  claim without (ii) is the intuition-level argument O&M document as
  the field's default.
- `code-and-data`: check whether the reported DDD is the O&M estimand —
  the fully-interacted model — or a stacked/two-way-FE approximation,
  and whether the SEs treat the differenced structure correctly.
