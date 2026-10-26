# Simulation and resampling harness

Engineering rules for Monte Carlo calibration runs, bootstrap/placebo
resampling, and null-distribution construction. The battery decides WHAT to
simulate; this file is HOW to simulate without artifacts masquerading as
findings. Most rules below exist because live runs have violated them.

## Gate the generator, not just the outcome

Before interpreting any MC result, validate the DGP **independent of the
real-data anchor**: at N=1 simulate every required component (summands,
blocks, marginal tests, FE columns, spatial structure) and confirm real-valued
non-degenerate draws; check simulated-vs-observed location, spread, and tail
behaviour. A simulator whose components are NaN/Inf from the first draw will
still produce a "significant" anchor comparison — the degeneracy IS the
explanation. Also calibrate the simulator's parameters *from* the observed
series' own dependence (each unit's residual autocorrelation, cluster-level
correlation), never only from a benchmark paper's defaults, and label any
surviving benchmark-derived parameter as such.

## QR-stable, not crossprod-naive

Inside a resampling loop, never use `solve(crossprod(X))` — it fails
intermittently on mildly ill-conditioned draws and a `tryCatch` →
`MASS::ginv` fallback silently mixes regression definitions across
replications. Use `qr.coef(qr(X), y)`; report and drop rank-deficient draws.
Same for covariance estimates: `vcov(fit)` from the fitted object, not a
hand-rolled `sigma2 * solve(X'X)`. A garbage component's random sign
injection can produce an *under-rejection* at the null that mimics a
conservative test.

## Resample the data the paper's estimator actually sees

Extract the estimation frame from inside the fitted call
(`model.frame(fit)`, `fit$model`, the do-file's kept sample), not the raw
file. A constructed frame missing even one derived column produces
coefficients near zero across all replications and reads as total model
failure — it is missing-data mechanical failure. If you cannot recover the
exact frame, say so and bound the exercise.

## Finiteness and sanity gates on every reported distribution

- A bootstrap p that is an exact floor value — `1/(reps+1)` like .0002 — can
  be a floor because ALL resampled statistics were NaN. Count finite resamples
  and require a minimum share before reporting a bootstrap distribution at
  all; a resample-share bar that counts never-tested replicates as
  "supporting the null" manufactures a pass.
- After assembly, gate EVERY reported distribution: verify finite mean/SD and
  min<max before calling a result. If the SD is 0, `e()` scalars went missing,
  or the drawn value is identical across seeds when the draws are random (not
  exact enumeration), the harness failed — do not
  report its numbers.
- Per-replication failures and null-distribution degeneracy are different
  verdicts — label them separately.
- For permutation/randomization inference, compute the p against the
  ACTUAL permutation distribution with the test's own formula — a printed
  reference p (e.g. Moran's from a canned `moran.mc`) can be computed by a
  different formula that never moves; reproducing the formula is the finding.
- For randomization-inference tables, check the number of randomizations the
  paper reports (e.g. 1,000) against the feasible support (`2^K` sign
  combinations / `C(N,k)` subsets) — a count exceeding the support is a
  reporting problem where the paper presents the draws as distinct or reports
  a p finer than 1/support.

## Incremental output and real seeds

Write every estimator's coefficient/SE/p to a results file **inside the
loop** — `quietly { estimates ... ; file write }` or `postfile` — not via a
parallel-collection mechanism or log-scrape; a "converged run" with no file
output gives the MC nothing to summarize. Use distinct real seeds per run —
`set.seed(sim)` at minimum; better, a hash of the replicate index — and
verify the drawn quantity actually varies across seeds. A zero-SD draw is a
frozen RNG. Record nrep, seed(s), platform, and BLAS flavour.

## Normalize coefficient names before selecting

Stata's `_b[1.treat#c.control]` reads an interaction directly; the
names that differ are the column names in `e(b)`, which carry base and
omitted markers (`0b.treat`, `0b.treat#co.control`, `o.x`). Normalize
names (`regexr`, stripping `b`/`o` markers) before matching a column
across commands or across a simulation grid, or a postfile collects from
the wrong element.

## resample-weighted tests (wbs)

For Rademacher/wild resampling of an estimator: retain `reldist::wtd.quantile`
or an explicit quantile specification rather than hand-rolling a mid-quantile
definition inside the simulation — a hand-rolled type may not be the
documented one and shifts small-sample cutoffs.

## Reporting

Report per-arm and overall: N converged of K, finite-stat share, drawn-value
SD (frozen-RNG check), the p distribution across replications (not just the
headline), and which replications were dropped and why. The file's job is to
let a reader distinguish "the test rejects" from "the harness produced
garbage."
