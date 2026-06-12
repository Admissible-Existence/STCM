# STCM v0.4 — Sequential Receipt Lineage

## Status

This document records the green operational boundary after STCM v0.4 lineage fixtures passed.

v0.3 proved that a transition can be ignored, routed, node-bound, merged, composed, and closed only when declared hash scope, routing path, node outputs, receipt posture, merge coherence, and closure policy agree.

v0.4 extends the model from one closed transition to a sequence of receipt-bound transitions.

The core question changes from:

```text
Can this transition close?
```

to:

```text
Can this transition close as the lawful successor of a prior receipt?
```

The v0.4 harness now includes a lineage layer that runs before the closure predicate.

---

## Core claim

A transition is not only judged by its local conservation record. It must also bind to the correct prior receipt when it claims continuity.

A valid receipt chain must preserve:

```text
receipt(t0) -> transition(t1) -> receipt(t1) -> transition(t2)
```

A transition that cannot bind to the correct prior receipt cannot become the next receipt basis, even if its local fields appear otherwise complete.

---

## Implemented harness order

The current closure harness now evaluates seven layers:

1. Node layer — each Prime Node tested in isolation.
2. Composed layer — transition -> PN outputs -> conservation record -> closure.
3. Routing layer — ignore / reroute / escalate front-gate behavior.
4. Routed-hop layer — source reroutes -> recognized owner activates -> destination closes or governed non-closes.
5. Merge layer — multi-node outputs merge into a coherent transition receipt only when required conditions hold.
6. Lineage layer — prior -> current -> next continuity gate.
7. Closure layer — direct closure-predicate regression.

The lineage layer is intentionally placed before closure:

```text
scope/routing
-> node execution
-> merge/composition
-> lineage binding
-> closure predicate
-> next receipt basis
```

If lineage fails, closure is not allowed to return `CLOSED`.

---

## Receipt lineage object

v0.4 introduces a lineage posture, not yet a global storage system.

A lineage check evaluates the relationship between:

- the prior receipt claimed by the transition;
- the current transition attempting to bind to it;
- the next receipt produced by successful closure;
- any known supersession or conflict facts.

The implemented lineage model evaluates at least:

```text
prior_receipt.id
prior_receipt.hash
prior_receipt.sequence_index
prior_receipt.closed
prior_receipt.superseded_by
transition.claimed_prior_receipt_id
transition.claimed_prior_receipt_hash
transition.sequence_index
transition.result_receipt_id
chain_head.id
chain_head.sequence_index
known_successors.previous_receipt_id
known_successors.sequence_index
known_successors.id
```

This does not replace the conservation record. It adds continuity posture before the conservation record may become the next receipt basis.

---

## Implemented lineage verdicts

The v0.4 harness implements explicit lineage verdicts:

```text
BOUND
STALE
SUPERSEDED
CONFLICT
MISSING_PRIOR
MALFORMED_PRIOR
```

These verdicts are not closure verdicts. They feed closure.

A lineage verdict of `BOUND` permits closure evaluation to proceed.

A lineage verdict of `STALE`, `SUPERSEDED`, `CONFLICT`, `MISSING_PRIOR`, or `MALFORMED_PRIOR` forces governed non-closure.

Genesis is also supported: a transition with no prior may bind only when it is explicitly marked as genesis.

---

## Implemented v0.4 fixtures

The green lineage layer proves these cases.

### 1. Prior receipt binds

A transition claims the exact prior receipt id and hash. The prior receipt is closed, current, and not superseded.

Expected result:

```text
lineage verdict: BOUND
closure may proceed
```

### 2. Missing prior receipt

A transition claims continuity but no prior receipt object is present.

Expected result:

```text
lineage verdict: MISSING_PRIOR
closure blocked
```

### 3. Prior receipt hash mismatch

A transition claims the correct prior receipt id but the hash does not match.

Expected result:

```text
lineage verdict: CONFLICT
closure blocked
```

### 4. Stale prior receipt

A transition binds to an old receipt that is not the current head of the chain, or whose sequence does not advance contiguously from the current head.

Expected result:

```text
lineage verdict: STALE
closure blocked
```

### 5. Superseded prior receipt

A transition binds to a receipt that explicitly points to a later replacement.

Expected result:

```text
lineage verdict: SUPERSEDED
closure blocked
```

### 6. Competing receipt chains

Another known successor already claims the same prior receipt at the same sequence index.

Expected result:

```text
lineage verdict: CONFLICT
closure blocked until resolved
```

### 7. Genesis

A transition with no prior may bind only when explicitly marked genesis.

Expected result:

```text
lineage verdict: BOUND
closure may proceed
```

### 8. Malformed prior

A prior receipt is present but lacks required lineage fields.

Expected result:

```text
lineage verdict: MALFORMED_PRIOR
closure blocked
```

### 9. Lineage succeeds but closure still fails

A transition may bind to its prior receipt while still failing closure because the conservation record is not sufficiently complete for its tier.

Expected result:

```text
lineage verdict: BOUND
closure blocked by closure predicate
```

This proves lineage permits closure evaluation but does not guarantee closure.

---

## Closure relationship

Lineage does not replace closure.

If lineage fails, closure must not return `CLOSED`.

If lineage succeeds, closure still may fail for ordinary completeness, authority, evidence, or coherence reasons.

The implemented `lineage_gate` makes this order a single callable so callers cannot accidentally close a record whose lineage failed.

---

## Supersession is not deletion

A superseded receipt must not disappear.

Supersession means the old receipt remains historically valid for the time at which it closed, but it is no longer valid as the current basis for a new successor transition.

The system must preserve both facts:

```text
receipt was valid when closed
receipt is not current for future continuation
```

This is essential for auditability.

---

## Conflict is not merge

Two competing successor receipts must not be silently merged.

A conflict means the system has observed more than one plausible continuation from the same prior basis.

The correct behavior is governed non-closure or escalation until the conflict is resolved by policy.

This prevents ambiguous chains from producing false continuity.

---

## What green means in v0.4

A green v0.4 run means:

- a transition can bind to the exact prior receipt;
- genesis may bind only when explicitly declared;
- a missing prior receipt blocks closure;
- a prior receipt id/hash mismatch blocks closure;
- a stale prior receipt blocks closure;
- a superseded prior receipt blocks closure while preserving history;
- malformed prior receipts block closure;
- competing successor receipts are recognized as conflict;
- lineage failure produces governed non-closure, not accidental closure;
- lineage success permits but does not guarantee final closure.

---

## What v0.4 does not prove yet

A green v0.4 run does not yet prove:

- distributed consensus over remote receipt stores;
- cross-repository authority portability;
- final conflict-resolution policy;
- numeric transition entropy;
- time-decay scoring;
- cryptographic proof beyond fixture hash comparison;
- global state reconstruction after partial data loss.

Those remain later boundaries.

---

## Entropy remains advisory

Transition entropy remains advisory after v0.4.

Entropy can later measure how much transition cost, uncertainty, or state disturbance was absorbed or released, but it should not gate closure until future work defines numeric entropy semantics.

---

## Version boundary statement

STCM v0.4 establishes that a transition cannot become a valid next receipt basis merely by closing locally. It must also bind to the correct prior receipt and avoid stale, superseded, missing, malformed, or conflicting lineage posture.

This is the first executable boundary for sequential receipt continuity.
