---
name: theory-diagnostics
description: >-
  Diagnostics for formal-theory results — theorems, propositions, proofs,
  derivations, closed-form claims. Re-derives from the paper's own primitives,
  constructs counterexamples, stress-tests the assumptions, and checks that
  each proof delivers exactly what it claims. Invoke from `code-and-data`
  whenever a load-bearing result rests on a proof or derivation rather than an
  estimate. A kill here is a construction, never an assertion.
---

# Theory diagnostics

The empirical modules break a result by running the regression that kills it.
A formal result has no regression: its kill is a **construction** — a concrete
counterexample, a numerical simulation of the paper's own model, or a
re-derivation from the paper's own primitives that lands somewhere other than
the claim. This module is the battery's "run it" ethos applied to a proof.
The object changes; the discipline does not: **you may not call a theorem
false by argument alone.** Build the counterexample, run the simulation, or
carry the derivation through — then report what it shows.

Trigger: any target result whose truth rests on a theorem, proposition, lemma,
proof, derivation, or closed-form claim — including the model section of an
otherwise-empirical (hybrid) paper, where the estimation inherits its meaning
from a model that must itself hold. `NOT_APPLICABLE` when every target result
is an estimate and no formal claim is load-bearing; say so in a one-line stub
naming the estimates and move on. Do not manufacture a proof audit on a paper
that has no theory.

## The one failure this module exists to prevent

"Re-derive it yourself and see if it breaks" is a **strawman generator** the
moment your premise is wrong. Give a symbol a meaning the paper never assigned
it, or attack a step the paper never took, and you can derive a rigorous-looking
contradiction from your own fabrication — and because the fabricated premise is
non-reproducible, a second pass "confirms" it by construction. This is not
hypothetical: it is the exact way a confident, false "the method is
mathematically invalid" kill gets shipped. The structure below is built around
that hazard. Do not collapse it into a single pass.

## Operate in three separated roles — never one context

Run these as **distinct jobs** (separate subagents where the harness supports
them; otherwise separate, dedicated passes each starting from a clean read, and the
module report says which way the roles ran).
The attacker must not rule on its own findings, and the judge must not run a
fresh derivation from memory. Segregation is the mechanism, not decoration.

### 1. Attacker — try to break each load-bearing result

Spend the majority of effort on the core: the theorems, propositions, proofs,
and definitions **are** the paper. A pass whose findings all sit in the
periphery while the core was never seriously attacked is a coverage failure,
not a verdict — but a core that *was* seriously attacked and held is a survived
result, not a missing issue. The construction ledger separates the two:
attacked-and-held is evidence; never-attacked is a hole. For each load-bearing
result:

- **Re-derive from the paper's own stated premises and definitions.** Check
  every skipped step and every "it follows trivially." When the text says an
  expression "is," "corresponds to," or "is the [named object] of" something —
  build that object independently and compare term by term; a constant-factor
  mismatch (the factor-of-2 that nobody re-derives) is a finding. For
  algebraic steps a symbolic check (SymPy/Mathematica simplify–differentiate–
  compare, saved as an artifact) is stronger evidence than an eyeballed
  derivation — use it where the hunt is a skipped step or a factor.
- **Treat the skip-words as the attack surface.** "It is easy to see,"
  "clearly," "obviously," "it follows trivially," "the other case is
  similar," "by symmetry" — each marks a step the author declined to write,
  and each is a named point to open. The characteristic sleights parked
  behind them: several manipulations fused into one line; a sign asserted
  without the derivative or inequality that establishes it; one effect
  declared to "dominate" another with no bound; an inequality direction
  reversed across a multiplication or reciprocal without remark; Jensen
  applied in the wrong direction; a discrete object (an integer threshold, a
  count) differentiated as if continuous; an edge case silently dropped
  (x = 0, a singular matrix, an empty configuration); cases claimed
  "analogous" with no explicit substitution carrying the proved case onto
  them; existence asserted with neither a construction nor a named theorem
  whose hypotheses are checked here.
- **Construct a counterexample.** For each theorem or proposition, actively try
  to build an object that satisfies *every* stated hypothesis and *violates*
  the conclusion — a specific function, sequence, or parameter value. A
  concrete counterexample is the single most powerful refutation available;
  a theorem that survives a serious construction attempt is far stronger
  evidence than one you read and nodded along to.
- **Proof of a weaker statement.** Does the proof establish *exactly* the
  claim, or something weaker — the same quantifiers, domain, strict-vs-weak
  inequality, existence-vs-uniqueness strength, mode of convergence, and notion
  of solution/equilibrium/optimality? A correct proof of a different, weaker
  theorem is a finding even when every line is right.
- **Hunt the characteristic kill-shapes.** The errors a fluent proof hides
  best are plausible, internally consistent, and shaped alike: a property
  true *in expectation* claimed *ex post* (one realization's report moving
  another's adjustment, while the mean stays put); a cancellation or
  identity at a point mistaken for a global property (a cross-partial
  vanishing at the target read as balance everywhere — check whether the
  mixed derivative vanishes in general, not just at the evaluation point);
  a sufficient construction mistaken for a necessary one, or credited with
  a property it does not supply (a costly fix claimed necessary for a
  property the baseline object already has — what the fix genuinely buys
  may be a different, weaker property).
- **Assumption stress test.** For each stated assumption: where is it used, and
  is it strong enough for every step that invokes it? Then hunt the *missing*
  assumption — a step that only works if some property holds (continuity,
  compactness, measurability, monotonicity, interiority, boundedness) that is
  never assumed or proved. Watch for stronger-property drift: a proof that
  quietly upgrades measurable to continuous, or pointwise to uniform, midway.
  A step that resists formal statement — one you cannot write down with its
  quantifiers, types, and domains without adding a premise the text lacks —
  is where a missing assumption is hiding.
- **Cited-result misuse.** Where the paper leans on a theorem from the
  literature, check its hypotheses are actually met here and that it delivers
  the *exact* conclusion the proof uses — not a weaker version, not the
  converse, not a stronger variant never established. If a cited result cannot
  be checked from the paper or your own knowledge, flag it as an UNVERIFIED
  dependency rather than assuming it holds. The flag is not cosmetic: a result
  resting on an UNVERIFIED dependency cannot be reported as having survived —
  it is UNRESOLVED, conditional on the named lemma, and the survival sentence
  must name the unverified premise. The same check runs *inside* the proof:
  for each internal lemma, verify its hypotheses hold at every call site —
  a correct lemma invoked where its conditions fail is an assembly error as
  fatal as a gap in the lemma itself.
- **Definition-to-claim correspondence.** For each load-bearing formal object,
  state the field-standard object and whether the paper's definition
  coincides. A theorem can be watertight while a nonstandard definition makes
  the conclusion definitional — every line correct, the claim vacuous.
  Vacuity-by-definition is a finding even when the proof is correct; the
  weaker-statement check does not catch it because the formalized object
  itself is not the object the claim names.
- **Framework foundations.** Variable drift (a symbol that changes meaning
  mid-paper); Bayes-direction confusion (P(A|B) used where P(B|A) is needed —
  derive the posterior from prior and likelihood and compare); unjustified
  independence (a joint density silently factored); asymptotic-treated-as-exact
  (an n→∞ result applied at n=30 with the O(1/n) terms dropped).

Each attacker finding names the result, the exact step or symbol, and — for a
counterexample — the concrete object and the computation that shows the
conclusion fails.

**Briefing a delegated attack.** When the attacker pass runs as a separate
subagent, the brief is the prompt, and its shape matters: "verify this
proof" invites a pass/fail skim, while "prove or disprove the claim — if it
fails, find the tightest sufficient condition or a counterexample in a
named region" forces construction. Give the pass everything it needs to
work without your context: the exact claim stated formally (the proposition
with its quantifiers, not "check the concavity"), every symbol's definition,
domain, and economic meaning, where suspicion lies and what has already been
tried, strategies to attempt (plural — one failed line of attack settles
nothing), and the demanded standard of rigor (prove every step; a claimed
counterexample must give specific parameter values verified numerically; no
hand-waving). Set depth by stakes, not apparent difficulty: the heaviest
scrutiny goes to unproved load-bearing claims and counterexample searches,
however routine they look. And allocate scrutiny independently of surface
finish — fluent, referee-ready prose is free to produce and uniform across
checked and unchecked claims, so a proof that looks finished earns no
discount. Full checklist and worked example:
`../../references/methods/koren_2026_theorist_toolbox.md`.

### 2. Defender — ground the definitions, then rescue what can be rescued

Before any algebra, **ground each symbol in its explicit defining equation and local scope.** Compare discrepant equations and tables after checking units, normalizations, indexing, and whether they refer to the same object. A discrepancy may be a different quantity, an attacker misreading, or a real inconsistency in the paper; establish which from the text and derivation. Neither the attacker nor the defender may settle it by presuming the paper consistent.

Then, for each attacker finding:

- **Check scope.** Does the counterexample violate a condition the paper
  imposed (attacking "suppose n ≥ 3" at n = 1)? The conditions are the result.
- **Simulate where informative.** Implement the disputed model and verify the code against its definitions and assumptions. Code can encode the same misreading as prose. Record the exact parameter/domain case, numerical tolerance, and the proposition being tested. A valid counterexample refutes a universal claim; successful examples do not prove it or invalidate a counterexample elsewhere. A successful example can refute an assertion that the procedure *always* fails. For asymptotic claims, finite-sample behavior alone is not a counterexample to the limit result. Return discrepancies for source-grounded resolution.

- Default to defending; make the paper's case as strongly as it can honestly be
  made. Your most dangerous miss is a defence you skip because you reproduced
  the attacker's mistake yourself.

The defender issues **no verdict**. It outputs, per finding: the grounded
definitions (each with its quoted defining equation and location), whether the
finding's reading of the symbol matches the paper's own, the scope check, and
any simulation with its code and result.

### 3. Judge — rule REAL or false-positive, on the paper as source of truth

Weigh each attacker finding against the defence, with the paper's full text in
hand. Rule **CONFIRMED** (a real error), **DISCARDED** (a demonstrated false positive), or **UNRESOLVED** (the evidence does not settle the dispute). Name the missing derivation, source, or implementation check for an unresolved result.

- **Do not run a competing derivation from memory.** The construction and any
  simulation were already done. If you find yourself deriving an equation
  neither the paper nor the construction wrote, stop — that is exactly how this stage manufactures false
  confirmations (the empirical battery's over-derivation failure, in theory
  form).
- **Check the defence's grounding — and that it is real.** Go to the line the
  defence cites and confirm the symbol's defining equation actually says what
  the defence claims. **A defence that rests on "the paper explicitly states /
  licenses X" holds only if that sentence is genuinely locatable in the paper.**
  Defenders invent verbatim quotes; if the claimed statement is not there, the
  defence has fabricated its grounding — it does not dissolve the finding, so
  rule on the remaining merits.
- **Adjudicate the construction.** Check that the numerical or analytic example implements the paper's definitions, meets every hypothesis, and contradicts the actual conclusion. Do not infer a universal result from successful sampled cases. If the attacker and defender use different objects or domains, resolve that difference from the source or mark the finding UNRESOLVED; numbers alone do not resolve it.

- **Headline vs residual.** Discard a false grand claim but keep a real typo or
  sign error riding inside it. A retracted "the whole method fails" does not
  clear a genuine dropped factor in the same equation.

**Real, not "does it matter."** DISCARD is reserved for false positives —
strawman, attacker misread, out-of-scope counterexample, a demand for
generality the claim does not need, a degenerate case the hypotheses already
exclude, a missing-assumption flag where the paper states the assumption
outright or resolves the point elsewhere (located and checked), or a flag on a
convention the paper announces — an announced assumption or convention that is
inconsistent, vacuous, or excludes the claimed case stays CONFIRMED — or numerical vindication that addresses the exact claim and its quantifiers. A real-but-minor error
(a sign, a dropped factor, an undefined symbol, a wrong quantifier) stays
CONFIRMED; magnitude is not this module's call. Genuine minor issues must reach
the author — over-discarding them is a documented failure mode, not tidiness.
For every CONFIRMED finding record the **minimal repair**: the weakest
modification that restores the claim, or "none found" — the distinction a
referee report most needs.

**Propagate through the dependency graph.** The battery's construction
ledger already records proof dependencies — consume them: a CONFIRMED error
in a lemma stamps "rests on broken X" on every formal result that cites it
and on every empirical family the trigger classifies as model-inheriting.
The module report's `## Leads for later stages` (folded into the `code-and-data` report)
carry the dependents for `claims`, not just the finding.

## Report back

Emit `theory-diagnostics-REPORT.md`. Lead with the confirmed errors and what
each costs the paper's claims — a broken main theorem is a different finding
from a typo in a remark. For every confirmed finding record: the result, the
exact step/symbol, the attacker's construction, the defender's grounding and any
simulation (with the code path and its output), and the judge's ruling with the
paper location it rests on. Account for coverage: which core results you
attacked, which survived a serious counterexample attempt (report survival
plainly — a result that withstands the battery is a strong result, and
fabricating a failure to satisfy the adversarial mandate is itself a failed
check), the numerical coverage — for each load-bearing claim with computable
content, name the check that ran (simulation, symbolic, gradient,
equilibrium computation); a claim audited only by eyeball is under-attacked,
not survived — and any UNVERIFIED cited dependencies. Hand every confirmed error and
every unresolved foundational threat to the module report and to `claims`
as it appears — a false or weaker-than-claimed theorem bears directly on what
story the paper can tell, not only on this module's verdict. Survival is
reported only with a construction ledger — the counterexample candidates
tried and why each failed to satisfy the hypotheses; "survived a serious
attempt" without the ledger is a claim, not a verdict.
