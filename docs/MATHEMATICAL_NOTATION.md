# STCM Mathematical Notation and Bounded Derivations

Goal: `STCM-MATHEMATICAL-COMPLETENESS-002`

This file makes equations already present in `docs/STATE_TRANSITION_CONSERVATION_MODEL.md` explicit for organization-wide audit. It derives bounded consequences of the declared model; it does not assert universal proof.

## Conservation closure

Let a governed transition conservation record be represented by

`R_T = (S_before, S_after, receipts, A, I, phi, H, E, C, authority, evidence, R_out)`

where `A` is the active node set, `I` the ignored node set, `phi` the phase posture, `H` the hash-scope posture, `E` transition entropy/accounting, `C` compute/governance capacity accounting, and `R_out` the resulting receipt.

For each transition type let `Req(T)` be its required conservation fields. Define closure predicate

`Close(R_T) := forall q in Req(T), accounted(q)`.

`accounted(q)` means the required field is present and valid, explicitly refused/blocked, or explicitly not applicable under the governing policy; silence is not accounting.

The source theory defines a coherent transition receipt basis only when

`Coherent(T) => Close(R_T)`.

This is the bounded derivation behind `STCM-PC-001`. It is a consequence of STCM's definition of coherence, not a claim that every real-world system must adopt that definition.

## Finite capacity

For Prime Node `n`, let governed load be `L_g(n,t)` and governed coherent capacity be `C_g(n,t)`.

Declared operating condition:

`L_g <= C_g => coherent operation is permitted by the capacity condition`.

If

`L_g > C_g`,

the model requires a structural response from

`{replicate, specialize, reroute, refuse, escalate, pause, evolve, devolve, dissolve}`.

If `L_g > C_g` persists while neither `L_g` decreases nor `C_g` increases and no structural response removes the overload, the capacity premise for coherent operation is violated. This is the bounded threshold derivation for `STCM-PC-002`.

For devolution, with initial parameter count `P_0` and resulting explicit node positions `N`, the source bound is

`N <= P_0`.

## Hash-scoped activation

Let `h(d)` denote the relevant hash posture of incoming data `d` and `H_n` the declared accepted hash scope of node `n`.

Define match predicate

`M(n,d) := [h(d) in H_n]`.

Under strict non-engagement,

`NOT M(n,d) => n not in A(d)`

where `A(d)` is the activated node set for the transition. Therefore the candidate active set satisfies

`A(d) subseteq {n | M(n,d)}`.

Non-matching nodes remain candidates for available capacity instead of consuming transition-specific interpretation cost. This is `STCM-PC-003`.

## Routing predicate

For candidate path step `(n,d)`, define:

- `M(n,d)` = hash-scope match;
- `Q(d)` = required receipt posture is sufficient;
- `T(n,d)` = Transition Table permits the step.

Then the source routing equation is

`RoutePossible(n,d) = M(n,d) AND Q(d) AND T(n,d)`.

For match count `m = |{n : M(n,d)}|`, the source model distinguishes:

`m = 0 -> no governed route`,

`m = 1 -> singular candidate route`,

`m >= 2 -> candidate governed branch`,

subject in every case to receipt sufficiency and Transition Table permission. This is the bounded conjunction derivation for `STCM-PC-004`.

## Compute accounting

For a bounded system capacity at an evaluated moment,

`C_total = C_active + C_available + C_released + C_blocked`.

The terms denote capacity currently used by activated nodes, preserved by inactive/ignored nodes, released by structural change, and prevented from entering invalid paths respectively.

Under the selective activation rule, transition-specific active cost is modeled as a function of activated nodes:

`Cost_T = f(A(d))`,

rather than a function that necessarily activates the entire node population. The source shorthand `compute cost proportional to activated nodes, not total nodes` is a model objective/claim whose falsification conditions are stated separately. This is `STCM-PC-005`.

## Moment-bound validity

Let required values at time `t` be `V_req(t)` and observed values `V_obs(t)`. Define transition predicate

`P_T(t) := [V_obs(t) satisfies V_req(t)]`.

A result established at `t_1` establishes only `P_T(t_1)`. In general,

`P_T(t_1)` does not imply `P_T(t_2)`

unless the values required for the predicate are shown invariant across the interval or are revalidated at `t_2`.

This is `STCM-PC-006` and formalizes the source statement that transition validity is moment-bound unless revalidated.

## Proof maturity

The PN-001..PN-006 closure fixtures and hosted harness provide bounded evidence for the implemented closure predicate. They do not prove the capacity law, routing law, compute relation, or conservation principle universally. All six proof candidates remain `candidate_not_proven`.
