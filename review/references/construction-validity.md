# Construction-validity — design-specific checks

Reference for the challenge stage's checks on calculations the review built itself (the protocol
lives in `../challenge/SKILL.md`); this file carries the checks for the two construction families that most often hide
deterministic defects: stochastic procedures and rates over executions. A construction bug
reproduces cleanly on every re-run — these checks exist because re-execution cannot see it.

## Stochastic procedures — resampling, permutation, simulated assignment

The question every check answers: **do the generated draws follow the experiment's assignment
distribution?** Not "do the draws look like the data" — the test's inference rests on
*off-observed* assignments, the configurations the data never showed.

- **Assignment and resampling units.** What was randomized, at which levels, and does the draw
  permute or resample *at* those levels? A three-level design (cluster on/off, sub-arm at an
  intermediate level, an arm at the unit level) needs draws that move each level at its own
  level. Drawing observation rows within policy groups resamples at a finer level than any
  randomization level and silently destroys within-unit dependence.
- **Eligibility and support.** When a permutation changes which units are eligible, do
  newly-eligible units receive draws from the correct operative arm distribution? A generator
  that retains each unit's *original* arm vector when eligibility moves can never create a
  treated observation where the experiment would have — it shrinks the treated support by
  construction. Enumerate the support: which values can a moved unit take under the generator,
  versus under the experiment.
- **Strata.** Permutations stay within the design's strata (within-district, within-cluster).
  A draw that crosses stratum boundaries produces assignments the experiment never allowed.
- **Hierarchy.** Moves must respect nesting — a lower-level arm draw stays inside its parent
  unit; resampled parents carry their children.
- **Join multiplicity.** Draws assembled by joining resampled keys back to observation rows
  must not fan out or collapse: count joined rows per draw against the original unit count. A
  unit–cell pair sample joined back on the unit alone over-represents units spanning several
  cells — the draws are not the claimed whole-unit resamples.
- **Statistic and tail.** Name the statistic (re-selection of a winner? the point estimate?)
  and the tail (upper-tail share, a percentile, a two-sided p) and verify the code computes
  *that* tail: an upper-tail share saved into a variable named for a percentile is a different
  quantity.

**Inspect generated draws independently of the reported p-value.** Dump a handful of permuted or
resampled assignment vectors and check them by eye against the design: newly-eligible units
carry operative arms, stratum sizes preserved, nothing outside the support. The generator's
output is the test; the p-value is downstream of it.

**Observed-data agreement is a control, not validity.** An anchor that reproduces or an arm
reconstruction matching observed data checks plumbing — the code reads the right files and
applies the same transform to the same inputs. It says nothing about draws the data never
showed. Both failure modes have shipped: generators that reproduce their anchor on every re-run
while structurally unable to produce a valid counterfactual draw.

## Rates over executions — completion, abort, exclusion shares across a fleet

A "success rate" over a fleet of runs is a claim about a denominator and a classification, not
just a count.

- **Define the categories operationally before counting:** completed / failed / excluded /
  timed-out — by what rule, recorded where? A rate whose categories were never defined cannot
  be checked and should not be reported.
- **Verify the definitions against actual executions.** Open draws from *each* category,
  including every exclusion class. An excluded draw that completes under the original reporting
  logic is a misclassification, not an abort — the count then describes the reporting filter,
  not the executions.
- **An unresolved timeout is not a machine artifact by default.** A non-terminating loop (an
  elimination routine that never satisfies its stopping test) reports as a timeout and is a
  property of the pipeline being measured — classify it only after reading what it was doing
  when it stopped.
- **A flag in the data is not an execution outcome by default.** A `mapped=FALSE`-style flag
  records a reporting event; check what the original code actually did with such rows before
  counting them as failures — language-level behaviors (vector recycling, coercion) can carry
  flagged rows through to completion.
- **Check rows are not draws.** Instrumentation rows (original-data refits recorded for control)
  are excluded by their marker, never silently pooled into success or failure tallies — and
  their exclusion must itself be verified, not assumed from the schema.

## Paper-attributed constructions — "the paper's own X" must be the paper's own X

A reviewer-authored construction presented as the paper's specification, column, or test object
carries a second validity burden beyond its own correctness: it must *be* the object it names.

- **Resolve the attribution against both primary objects before building on it.** The printed
  equation or method text AND the deposited code block that implements it — quoted, with page and
  `file:line` citations in the inventory row. The two disagreeing is itself a finding (record
  which the construction follows and why); either one unread is an unverified attribution.
- **Output resemblance is not specification evidence.** A reconstruction whose output drifts like
  the printed table's shares a shape, not a regressor list — the printed column's controls, fixed
  effects, and weights are read from the code, never inferred from what the output looks like.
  (An audit inferred a printed table's regressor list from its output shape,
  missed the fixed effects sitting in the deposited code block, and built the remediation the
  verdict rested on against a spec the authors never ran.)
- **An analogue is a proxy — label it.** Where the paper's exact object cannot be built
  (restricted data, missing inputs), the construction is a proxy and its sample/weight/estimator
  differences are stated. Prose built on it says "the closest feasible analogue", never "the
  paper's test."
- **The review's own earlier verdict is a claim to re-check, not inherit.** A `code-and-data` spec audit
  that marked the object a match is evidence about the comparison it ran — a later attribution
  contradicting it is an anomaly to propagate, not a verdict to override silently.
- **No packet may describe an unchecked construction as validated.** "Requirements met" applies
  only to constructions the challenge actually rebuilt, at the recorded revision — a construction
  added afterwards carries no inherited validity.

## Derived quantities — a ratio is arithmetic until the counterfactual is stated

A number derived from estimated quantities — a ratio, a share, an upper bound, a decomposition —
carries the validity burden of the inference it serves, not of the arithmetic.

- **A bound or causal share needs its counterfactual on the record:** what trend or level would
  have continued absent the shock, over what horizon, under what functional form, with the
  estimate's uncertainty propagated through the extrapolation. An "at most X%" claim without those
  is a point-estimate ratio — write it as descriptive arithmetic naming its inputs, or build the
  construction that makes it a bound.
- **The uncertainty is part of the quantity.** A pre-trend extrapolated seven years forward
  carries the pre-trend's confidence interval through the extrapolation; a bound computed off the
  point estimate alone understates what the confound could contribute and is a FAIL of the same
  kind as a missing SE.
- **Two estimates that agree are still two objects.** Values matching to several decimals across
  different windows, weights, or samples coincide until shown identical — never "statistically
  identical" on the numbers alone; the claim requires sample, window, weights, and estimator to
  match.

## Packaged-command traps — where default syntax silently computes the wrong statistic

Even when a review calls a standard community package, default options or post-estimation hooks can silently return a different estimator from the one named in prose (`check_inference.py` gates the mechanical signatures):

- **`vtf.ado` vs jackknife VtF:** Stata's `vtf.ado` is hard-wired to CR1/HC1 score covariances (`_vtf_avar`) and takes variable names, not pre-computed jackknife SEs. A few-cluster VtF check must form the $2 \times 2$ jackknife covariance matrix $\hat{\Sigma}_{\text{jack}}$ of $(\hat{\pi}, \hat{\delta})$ from the same delete-one-cluster pairs and pass $(\hat{F}_{\text{jack}}, \hat{r}_{\text{jack}})$ to the VtF critical-value function; any `vtf` call is a CR1 companion tagged `VtF-CR1-robustness`.
- **`boottest` defaults (`jk`, `noci`, `ar`, missing `r(p)`):** Plain `boottest` is WCR-C; `boottest ..., jk` is WCR-S only at a zero null (its CI inversion at $b_0 \ne 0$ adds an $X_g \cdot t_1$ term that is not MNW's WCR-S, so `noci` is mandatory); `boottest ..., ar` runs an unrestricted bootstrap DGP (`SetR(*pR1)`) despite printing "null imposed", so primary AR sets must invert zero-null `jk noci` tests on $y - b_0 d$ over a grid; and a refused `boottest` exits with `_rc = 0` and `r(p) = .`, requiring `assert !missing(r(p))`.
- **`csdid` + `honestdid`:** `csdid` defaults to consecutive-period pre-treatment comparisons (`short`), whereas `honestdid` requires a common (`universal`) baseline (`csdid ..., long2` or R `did::att_gt(..., base_period = "universal")`) and positive column indices in `e(b)` (`pre(a/b) post(c/d)`).
- **Shift-share delete-one-shock jackknife:** Dropping shock $k$ creates missing share $S_k$, so the unit-level IV regression must control $S_k$ (equivalently $S_{-k} = S - S_k$ when $S$ is in the model) and re-estimate in each leave-out step; a pre-built $Z_{-k}$ without controlling $S_k$ or a unit-level cluster jackknife is not the shock-level CV3.
- **Engle–Granger / Phillips–Ouliaris residual ADF:** R's `summary(urca::ur.df(e, ...))` and `urca::punitroot` use `niv = 1` unit-root critical values, which over-reject on fitted cointegration residuals; evaluate `adf_eg@teststat[1]` via `urca:::.urcval(..., niv = m)`.
- **Local-randomization RD (`rdrandinf`) CI grid clamping:** When the default or narrow `ci` grid does not bracket the acceptance region, `rdrandinf` clamps `ri$ci` to `min(grid)` or `max(grid)` without warning; verify `ri$ci[1] > min(grid)` and `ri$ci[2] < max(grid)`.

