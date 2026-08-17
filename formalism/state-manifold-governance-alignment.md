# STCM State-Manifold Governance Alignment

Canonical mathematical source: `Admissible-Existence/AE:AE-AUTO-0011`.

STCM records moment-bound and receipt-bound relations. It must distinguish four objects:

`S` — observed/reconstructed state,

`C_rho(x,y)` — causal relation established at observation resolution `rho`,

`R` — receipt/evidence that records an observation or governance judgment,

`A_G(tau)` — admissibility judgment for transition `tau` under governor/invariant set `G`.

The receipt relation is evidentiary:

`R => evidence(C_rho(x,y))`

when its evidence is sufficient. The reverse construction

`R => C_rho(x,y)`

is not valid merely because a receipt exists.

## Resolution

If finer observations produce

`x -> z_1 -> ... -> z_n -> y`,

STCM may emit additional moment/receipt relations. When those observations refine the same established causal transition, their coarse projection must preserve the relation `x -> y`. Additional receipts increase observational resolution; they do not retroactively erase the coarse transition.

## Governance coordinate

A governance receipt must bind at least:

- the transition identifier/relation being evaluated;
- the governor or invariant set;
- the disposition;
- the evidence used;
- any explicit dependency, decomposition, lineage, or precedence rule that affected the result.

This prevents an `INADMISSIBLE` higher-order judgment from being confused with nonexistence or first-order impossibility of the transition.

## Time coordinate

A timestamp or epoch records a coordinate/evidence relation. It is authoritative to admissibility only when an explicit governance invariant consumes that coordinate. STCM must not infer causal identity, causal continuity, expiry, or admissibility from elapsed time alone.

## No implicit lineage taint

For receipts over trajectory `tau_1,...,tau_n`, a restricted receipt on `tau_i` does not alter the governance standing of `tau_j` unless a separately identified lineage rule relates them. If lineage taint is intended, the receipt must name the lineage invariant and the ancestry evidence that caused the derived judgment.

## Classification and consequence

A governance receipt that says `DENY` or `FAIL_CLOSED` is classification/decision evidence. Enforcement requires a separately observable causal response transition. STCM should therefore be able to record both the governance disposition and the response transition without conflating the two.

This note is an integration constraint. The full proof obligations remain owned by AE-AUTO-0011 and must be rebound to the terminal validated mathematical version before STCM claims alignment complete.
