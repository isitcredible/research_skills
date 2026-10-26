---
name: whimsical-assumptions-diagnostics
description: >-
  Diagnostics for the premises of a model-based conclusion: the assumptions a
  theorem, a calibrated number, a model-interpreted estimate or a policy
  prescription stands on. Inventories the load-bearing assumptions (stated,
  structural, closure, exclusion, bridge), grades each one's empirical
  warrant from sources, and relaxes each in a realistic direction to see
  whether the conclusion survives. Invoke from `code-and-data` whenever a
  load-bearing conclusion — qualitative, quantitative or prescriptive — is
  derived from a model. A whimsical assumption is CRITICAL and UNWARRANTED
  at once; unrealism alone is never a finding.
---

# Whimsical-assumptions diagnostics

`theory-diagnostics` asks whether the conclusion follows from the premises.
`quantitative-model-diagnostics` asks whether the number survives other
parameter values. Neither asks whether the premises deserve belief. Every
model is unrealistic, so "the model is unrealistic" says nothing. The useful
question is narrower: **which unrealism does the conclusion rest on, and is
there any evidence for it?**

Three ideas set the standard. Leamer's *whimsy*: an inference is only as
credible as the assumptions it needs, and an assumption chosen for convenience
carries no evidential weight. Rodrik's *critical assumption*: an assumption is
critical when relaxing it in a realistic direction changes the conclusion
substantively. Pfleiderer's *chameleon*: a model whose conclusions are carried
into real-world claims or policy without its assumptions first passing a
realism filter.

**WHIMSICAL = CRITICAL and UNWARRANTED, each shown separately.**
- CRITICAL: a construction shows the conclusion flips sign, or moves beyond
  the range the paper states, under a realistic relaxation; or the conclusion
  is true by construction once the assumption is granted (BUILT_IN).
- UNWARRANTED: the warrant grade is CONTRADICTED, UNANCHORED or CONVENIENCE,
  or CONTESTED with the evidence spanning the region where the conclusion
  flips.

**FRAGILE = unwarranted, and critical only beyond a threshold no source
reaches.** The warrant leg is shown, but nothing sizes the margin that would
break the conclusion, so the construction can only report where it breaks.
A CONTESTED grade qualifies only when no source places the margin on the
conclusion's safe side of the threshold. A threshold of zero (the headline
already sits at the edge of its stated range, so any force in one direction
crosses it) is a bound-check matter for check 4, not a FRAGILE row.
FRAGILE is a finding, reported beside the WHIMSICAL ones: the conclusion
holds only if an unmeasured quantity stays on one side of a stated line.

An unrealistic assumption that is inert is a SURVIVAL, reported as such: the
conclusion is robust to it. A critical assumption with good evidence behind it
is a SURVIVAL too.

Trigger: any load-bearing conclusion derived from a model — a proved result,
a calibrated or simulated number, an estimate whose meaning comes from a model
(a regressor named for a model object, a "share explained by X" read through a
model), or a policy prescription. `NOT_APPLICABLE` when every conclusion is a
reduced-form contrast with no model reading; write a one-line stub naming the
estimates.

Boundaries. Proof validity belongs to `theory-diagnostics`; consume its
rulings and do not re-attack proofs. Parameter-value sweeps belong to
`quantitative-model-diagnostics`; cite its ranges, do not re-run them. The
identifying assumptions of estimates (exclusion restrictions, parallel
trends, shock exogeneity) belong to the empirical modules. This module owns
the structural premises: functional forms, closures, what is exogenous, what
is left out, and the premises that carry a model's result to the world.

**Value or premise?** Decide this before building anything. A relaxation that
only changes a number (an elasticity, a cost saving, a weight, a share) is a
value dispute: cite the `quantitative-model-diagnostics` sweep, and if the
sweep is missing, hand it there. A row is in scope when the relaxation changes
a functional form, a closure, what the model includes, or how a measure maps
onto a model object. A value the paper fixes by assumption that decides a
conclusion's *sign* is recorded here only as the threshold at which the sign
flips (effect `THRESHOLD`, the sweep cited): FRAGILE if its warrant fails,
otherwise INERT or CRITICAL_WARRANTED; never WHIMSICAL on its own. Before
building anything, check the paper's robustness tables and appendix: a
relaxation the paper already ran is read from its table, not rebuilt; save
that page's text under `work/whimsy/` and cite it as the artifact.

## The four failures this module exists to prevent

1. **The unrealism catalogue.** Listing every simplification (representative
   agent, CES, closed economy, no frictions) and calling the list a critique.
   This is the cheapest completion, and it is BANNED. A row reading "the
   model assumes X, which is unrealistic" with no relaxation construction and
   no sourced warrant grade is not a finding. Delete it or do the work.
   One construction behind several rows is one finding: merge the rows,
   cross-reference them, and count it once.
2. **The strawman premise.** Charging the paper with an assumption it does not
   make. Every row is grounded: a stated assumption by quotation and page; a
   structural or closure assumption by the equation that embodies it; an
   exclusion by showing the mechanism is absent from the equations, not just
   unmentioned.
3. **The prior as warrant.** Grading an assumption "contradicted" because
   everyone knows it is false. A grade needs a source that measures the same
   quantity, at the same level, under the same definition. If no source is
   found, the grade is UNANCHORED, never CONTRADICTED. The same-quantity test
   applies to the paper's own text and tables too: its own words are the
   strongest source only when they measure the premise's object. A usage
   share is not a displacement share; a firm count is not an adoption rate.
4. **The rigged relaxation.** Replacing an assumption with whatever breaks
   the result. A relaxation must be realistic and minimal: one change, in a
   direction the evidence supports, that a referee in the paper's own field
   would accept as a fair alternative. A relaxation outside the defensible
   range is DISCARDED, however dramatic its effect. A valid relaxation meets
   all of these:
   - **One change, all changes listed.** Write down every way the relaxed
     model differs from the paper's. A switch of units, of definition, or of
     a second premise (full displacement smuggled in beside a rent wedge) is a
     second change.
   - **Sized from a source.** Any number that sets the size of the
     relaxation passes the same-quantity test in failure 3. If no source
     sizes it, report the threshold at which the conclusion flips, never an
     unsized "central case". A sentence from a source's model or theory
     section is not evidence for a size or a direction.
   - **Same units as the conclusion.** Report the effect in the unit the
     conclusion is stated in (per installed robot, not per unit of
     technology shock). A change of units is a second change.
   - **Model-consistent.** The relaxed model keeps the paper's other stated
     premises on the same result. It also uses the model's own term for the
     relaxed channel where the paper, or a paper it borrows from, has one.
     Turning a suppressed term to zero is not a relaxation when the paper
     states a premise about that term's sign. A relaxation that opens a new
     margin (where the new capital's income goes) lists the margin and
     reports the threshold over it.
   - **Intermediate before polar.** For a closure or behavioural margin, use
     the evidence-based middle (partial adjustment, a rising supply curve)
     rather than jumping to the opposite pole. Report the pole only beside it.

## The inventory — five kinds of premise

- **Stated.** What the paper names: numbered assumptions, "we assume",
  "suppose", "for tractability".
- **Structural.** What the functional forms and primitives impose: a single
  elasticity across all pairs, perfect substitution within a unit, a fixed
  ordering of objects, a representative agent, constant returns, a static
  technology.
- **Closure.** What is held fixed and what adjusts: capital or its return,
  labour supply, prices, open or closed, partial or general equilibrium,
  exogenous or endogenous technology. Two closures in one paper are two
  models; record which conclusion uses which.
- **Exclusion.** Mechanisms the model leaves out. Each gets a **sign**: would
  including it raise or lower the headline? Ground the sign in a source or a
  construction, not intuition.
- **Bridge.** Premises the paper needs to carry the model's result to its
  real-world or policy claims that the model itself does not contain: that
  the empirical measure is the model's object; that a planner can observe the
  model's categories before acting; that a policy instrument moves the
  model's parameter, and by how much; that a result about the model's
  economy holds in the one being described.

## The checks — each one a construction

1. **Critical-assumption test.** For each premise with a realistic
   relaxation, rebuild the paper's derivation, simulation or calibration
   with that one change and report the conclusion in the paper's own units.
   Use the deposited code where it exists (the change as a logged patch);
   use a symbolic check (SymPy) for an analytic result. Effect is one of
   `SIGN_FLIP`, `MATERIAL` (outside the paper's stated range or wording),
   `IMMATERIAL`, `BUILT_IN`, `NO_COUNTERPART` (the relaxed or exact model has
   no value at the conclusion's own counterfactual), `THRESHOLD` (the
   conclusion fails beyond a stated value of an unsized margin; the value
   goes in the note), `UNTESTED` (with the reason). Every effect quotes the sentence of the conclusion it moves;
   moving a comparison the paper never states is IMMATERIAL. Effects are
   directional, conclusion by conclusion: a move that strengthens the
   conclusion as stated, or moves a hedged number in the direction its hedge
   already concedes, is IMMATERIAL for that conclusion (a larger job loss
   cuts against "limited" but not against "robots reduce employment").
   "About X" tolerates the range the paper itself attaches to X, including a
   sensitivity table it cites in support of X; else the rounding of its last
   printed digit (0.2 covers 0.15 to 0.25); a fraction in words covers half
   the step to its neighbours ("about two-thirds" covers 0.50 to 0.83). No
   private materiality band. A move whose only
   consequence is crossing the paper's own "bound" belongs to check 4, as one
   finding, not to a row each.
   Where the deposited code differs from the printed model, judge the premise
   against the printed model (the code defect corrected), report the
   shipped-code number in the note, and route the defect to `code-and-data`.
2. **Warrant grading.** Grade each premise `SUPPORTED`, `CONTESTED`,
   `CONTRADICTED`, `UNANCHORED` or `CONVENIENCE` (the paper itself calls it a
   simplification or offers no justification). Cite the source by file and
   page. An assumption contradicted by the paper's own tables, on the same
   quantity (a common coefficient where its own table shows heterogeneity),
   is CONTRADICTED on its own record. Every role saves every web source it
   relies on into `work/whimsy/sources/` with its URL and fetch date, and
   cites the saved copy: a source the judge cannot re-open is not a source. A quotation check
   proves a sentence exists, not what it means; the judge reads each one in
   context.
3. **Consistency.** Two conclusions in the paper resting on incompatible
   premises (an efficiency theorem used for the magnitude, a distortion for
   the welfare loss) is a finding. So is a companion paper by the same
   authors that maintains the opposite premise, when both conclusions are
   carried forward together. Cite the companion's page. A companion's
   *estimate* used as warrant is only as good as that estimate: if the suite
   has reviewed the companion, consume its verdict on that number; if not,
   label it "companion estimate, unverified here". An unverified companion
   estimate can make a premise CONTESTED, never CONTRADICTED, and it cannot
   size a relaxation on its own.
4. **Signed exclusions.** Tabulate every exclusion with its sign on the
   headline. A bound is a net claim. If the paper calls a number a bound and
   its case for it counts only forces on one side, the bound is *not
   demonstrated* (not shown false); say which excluded forces push past it
   and which push the other way. Crossing it one force at a time does not
   test a net bound. If every exclusion pushes the same way, the headline is
   one-sided by construction: say so with the table.
5. **Built-in check.** Is a conclusion that the paper presents as a finding,
   evidence or confirmation actually its own input restated: a measure
   defined through the model, a category defined by its outcome, a result
   imposed by an indexing convention, a number that is an assumed ratio times
   an assumed base? Show the identity. A valid theorem following from its
   stated premises is not BUILT_IN; that is what theorems do. A "match"
   between model and data is BUILT_IN when the model side is an identity of
   an input, even if the data side is measured: the match then tests the
   input, not the model. A built-in conclusion cannot count as evidence for
   its premise.
6. **Bridge audit.** For each real-world or policy claim, list the premises
   needed to reach it from the model. Mark each one as contained in the
   model, supported by cited evidence, or absent. A prescription whose bridge
   has an absent premise is a chameleon claim: the model does not deliver it.

**Judge the conclusion where the paper states it most strongly.** A caveat in
the body does not rescue an abstract, conclusion or policy section that drops
it. Judge the strongest version against its premises, and record the caveat
and where it decays.

## Run it as four separated roles

Separate subagents where the harness allows; otherwise separate passes, each
starting from a clean read, and the module report says which way the roles ran. Never
let one role rule on its own output.

1. **Inventory.** Reads the paper and appendix and fills the ledger's
   grounding, kind and conclusion columns. Covers every conclusion in the
   claim set: each one names the premises it uses. No relaxations, no
   grades, and no pre-assigned legs from sister reports (cite them as
   leads); this role's job is completeness and accurate grounding.
2. **Attacker.** For each row: builds the relaxation and runs it, proposes a
   warrant grade with sources, and does checks 3–6. Writes scripts and logs
   where the stage keeps them (`work/scripts/`, `work/logs/`, names prefixed
   `whim_`); role records and saved sources stay in `work/whimsy/`. Effort goes first to the premises behind the
   abstract's and policy section's claims.
3. **Defender.** Makes the paper's case. For each row it checks the grounding
   is real (the quote exists, the equation says it); finds the best evidence
   *for* the premise; tests the relaxation against every rule in failure 4;
   and checks whether the paper already confines its conclusion to the
   premise. It may re-run a construction, and may build the model-consistent
   or intermediate version the attacker should have built; its logs are part
   of the record and can supply or remove either leg. It issues no verdict.
4. **Judge.** Rules each row `WHIMSICAL`, `CRITICAL_WARRANTED`, `INERT`,
   `DISCARDED` (strawman, rigged relaxation, misread source, out of scope),
   `CONSUMED` (ruled in a sister module), `FRAGILE` (warrant fails; the
   conclusion breaks beyond a threshold no source reaches) or `UNRESOLVED`
   (a leg is missing and no threshold exists; name what would settle it). WHIMSICAL needs both legs shown in the
   record; the judge does not supply a missing leg by running a new
   derivation. Check that every quoted source sentence exists where cited; a
   fabricated grounding sinks the argument that rests on it. Weigh attacker
   and defender constructions alike, by which one implements the paper's
   definitions and meets the relaxation rules. Check each governing
   script's stated settings against its log; a header that claims runs the
   log does not show counts for nothing.
   - **Caveats.** A caveat carried everywhere the conclusion appears,
     abstract included, makes the conclusion conditional: judge the
     conditional. It is WHIMSICAL only if the paper still uses the
     conditional result as evidence for an unconditional claim.
   - **Rows carrying several conclusions.** Rule each conclusion the premise
     is load-bearing for. The row takes the most severe outcome; the note
     gives the outcome for every conclusion, so a finding on a minor
     sentence is never buried under an INERT headline.
   - **Out of scope.** Value disputes, arithmetic, code defects and
     misreporting of the paper's own tables are DISCARDED and routed: name
     the module or stage in the note as "routed to: …".
   - **Already ruled elsewhere.** When the row's critical result is a
     finding another module or stage has already confirmed (a theorem's
     failure in `theory-diagnostics`, a code defect confirmed in
     `code-and-data`), rule CONSUMED, name it ("routed to:
     theory-diagnostics TH-…"), and count it there, not here. DISCARDED is
     for what this module hands off unconfirmed.
   - **Weight of defender evidence.** A defender's model build counts like
     the attacker's. A defender's new regression is a check on what a source
     means: it can remove a leg, not supply one. A direction argument with no
     source carries no weight on the warrant leg.
   For each WHIMSICAL row record the **minimal repair**: the weakest
   restatement of the conclusion that the evidence would support.

## Output

`analysis/code-and-data/assumption-ledger.csv`, one row per premise:

`id | assumption | kind | grounding | conclusions | relaxation | artifact | effect | warrant | warrant_source | ruling | note`

- `kind` ∈ {stated, structural, closure, exclusion, bridge}
- `effect` ∈ {SIGN_FLIP, MATERIAL, IMMATERIAL, BUILT_IN, NO_COUNTERPART,
  THRESHOLD, UNTESTED}; any
  effect other than UNTESTED names its `artifact`: the log(s) holding the
  number, as job-relative paths separated by `;` and nothing else (settings,
  scripts and arrows go in `note`)
- `warrant` ∈ {SUPPORTED, CONTESTED, CONTRADICTED, UNANCHORED, CONVENIENCE};
  every grade except UNANCHORED has a `warrant_source`
- `ruling` ∈ {WHIMSICAL, FRAGILE, CRITICAL_WARRANTED, INERT, DISCARDED,
  CONSUMED, UNRESOLVED}; DISCARDED and CONSUMED rows say "routed to: …" in
  `note`; a FRAGILE row has effect THRESHOLD and an unwarranted grade

`check_manifest.py` enforces these rules.

`analysis/code-and-data/whimsical-assumptions-diagnostics-REPORT.md`. Lead
with the WHIMSICAL rows: the premise, the conclusion it carries, the
construction and its number, the warrant and its source, and the minimal
repair. Next, the FRAGILE rows, each with its threshold, the conclusion it
guards, and the measurement that would settle it. Then the signed-exclusion
table and the bridge audit for each policy claim. Then the survivors, stated plainly: an INERT or CRITICAL_WARRANTED
premise is evidence that the result is sturdier than its simplifications
suggest. Coverage: every conclusion and its premise rows; every UNTESTED or
UNRESOLVED row with what would settle it. Hand each WHIMSICAL row to `claims`
as it appears, because a conclusion resting on a whimsical premise supports
only its minimal repair.
