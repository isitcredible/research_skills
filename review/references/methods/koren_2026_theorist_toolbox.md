# LLM-assisted theory verification — Koren (2026)

Working distillation of Moran Koren, "Theorist Toolbox: Tools for Agent
Based LLM-assisted Economic Theory Research", arXiv:2606.22337v2 (econ.TH,
June 2026), and the companion agent skills the paper operationalizes —
`math-proof`, `codex-math`, `co-math-init`/`co-math-status` — at
github.com/morankor/theorist-toolbox. Audited against the v2 HTML and the
skill sources at master. Status: arXiv draft; the paper's own worked-example
mathematics is explicitly *unverified*, and its findings are demonstrations
on one problem, not measured rates — adopt the techniques on their merits,
not as validated results. Consumed by `../../modules/theory-diagnostics/`;
the paper is production-side (how to *write* theory with a model) — this crib
inverts its writing discipline into audit checks.

## The one-axis finding

Three LLM theory methods differ only on *how the work is verified*: a single
disciplined pass (internal self-check only), an adversarial prover–verifier
pair, and a multi-agent project with a reviewer gate. Observed on the worked
example: the most finished-looking output (the single pass) was the least
verified; the adversarial pair caught three of its own plausible, internally
consistent false claims that a confident single pass would have shipped.
Reading implication: **polish is not rigor** — fluent, referee-ready LaTeX is
essentially free to produce and is uniform across checked and unchecked
claims, so surface finish carries no information about verification. Do not
allocate scrutiny by it.

## The skip-words are the attack surface

`math-proof` bans the rhetorical moves that let a proof skip the steps most
likely to hide an error. Inverted for audit, every occurrence is a named
point to open — each marks a step the author declined to write:

- "it is easy to see", "clearly", "obviously", "it follows trivially",
  "the other case is similar", "by symmetry" (which symmetry? is it exact?)
- several algebraic manipulations fused into one line
- a sign asserted without the derivative or inequality that establishes it;
  one effect declared to "dominate" another with no bound
- inequality direction reversed across a multiplication or reciprocal
  without remark; Jensen's inequality applied in the wrong direction
- a discrete object (integer threshold, count) differentiated as if continuous
- an edge case silently dropped ($x = 0$, a singular matrix, an empty
  configuration, a boundary point)
- cases claimed "analogous" with no explicit substitution mapping the proved
  case onto them
- existence asserted with neither a construction nor a named existence
  theorem whose hypotheses are checked here
- induction that conflates "holds for $n = k$" (hypothesis) with what is
  proved; contradiction proofs that assert "leads to a contradiction"
  without exhibiting the incompatible statements side by side
- shorthand introduced mid-proof without definition

Two discipline rules that invert directly: *mechanistic verifiability* —
a step that cannot be encoded formally without adding an assumption is too
vague, and is where a missing assumption is hiding — and *assembly* — verify
each lemma's hypotheses are satisfied at its call site; a correct lemma
invoked where its conditions fail is as fatal as a gap in the lemma.

## Briefing an adversarial pass (`codex-math`, adapted)

The prompt shape matters more than the checker. "Verify this proof" invites
a pass/fail skim; "prove or disprove — if it fails, find the tightest
sufficient condition or a counterexample in a named region" forces
construction. Explore-framed beats verdict-framed. A delegated attack brief
carries:

1. The exact claim stated formally — quantifiers, domains — not "check the
   concavity" but the proposition itself.
2. Every symbol defined, with its domain and economic meaning; the checker
   does not share your context.
3. What has been tried and where suspicion lies.
4. Specific strategies to attempt, plural — one line of attack failing does
   not settle the claim.
5. The standard of rigor demanded: prove every step; a claimed
   counterexample must give specific parameter values verified numerically;
   no hand-waving.

Effort set by stakes, not apparent difficulty: heaviest scrutiny on unproved
load-bearing claims and counterexample searches, however routine they look.

## Lead, not verdict — and the false-positive taxonomy

Every adversarial finding is a lead requiring triage, never a verdict — in
both directions: "the attacker found nothing" is itself a checkable claim,
not assumed. False-positive classes to discard: flagging standard
conventions as errors; demands for unnecessary generality; over-reading
degenerate cases the hypotheses already exclude; flagging an assumption the
paper states outright as "unjustified"; flagging what the paper addresses
elsewhere. A real catch comes with a concrete counterexample or points to a
specific step that does not follow.

## Numerics as a standing gate

Every claim with computable content is checked numerically or symbolically
against an independent implementation — a Monte Carlo for a distributional
claim, symbolic for an algebraic identity, a gradient check for a derivative
formula, direct equilibrium computation for a solution-concept claim. In
Koren's exercise the most finished-looking output had no numerical check and
was the least trustworthy: a claim audited only by eyeball is under-attacked,
however clean the proof reads.

## The three observed kill-shapes

Errors the adversarial pass caught — each individually plausible and the type
that survives its author's re-reading:

- **In-expectation mistaken for ex-post**: a property claimed in every
  realized sample that holds only on average (the K_{2,2} counterexample —
  one agent's report moving another's adjustment through realized shocks).
- **Cancellation mistaken for a global property**: a cross-partial that
  vanishes at the target read as balance everywhere; the correct negative is
  provable (the mixed derivative does not vanish in general).
- **Sufficient mistaken for necessary**: a special construction (leave-one-
  out) credited with supplying a property (first-moment neutrality) the
  standard estimator already has — what the construction genuinely buys is a
  different property, so the claim is downgraded, not endorsed.
