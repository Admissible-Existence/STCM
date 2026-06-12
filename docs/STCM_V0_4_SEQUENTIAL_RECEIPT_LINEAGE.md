# STCM v0.4 — Sequential Receipt Lineage

## Status

This document defines the next build boundary after STCM v0.3 routed-hop and multi-node merge saturation.

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

---

## Core claim

A transition is not only judged by its local conservation record. It must also bind to the correct prior receipt when it claims continuity.

A valid receipt chain must preserve:

```text
receipt(t0) -> transition(t1) -> receipt(t1) -> transition(t2)
```

A transition that cannot bind to the correct prior receipt cannot become the next receipt basis, even if its local fields appear otherwise complete.

---

## Receipt lineage object

v0.4 introduces a lineage posture, not yet a global storage system.

A lineage check evaluates the relationship between:

- the prior receipt claimed by the transition;
- the current transition attempting to bind to it;
- the next receipt produced by successful closure;
- any known supersession or conflict facts.

A minimal lineage object should be able to express:

```text
prior_receipt.id
prior_receipt.hash
prior_receipt.state
prior_receipt.sequence_index
prior_receipt.superseded_by
prior_receipt.closed
transition.claimed_prior_receipt_id
transition.claimed_prior_receipt_hash
transition.sequence_index
result.receipt_id
result.receipt_hash
result.previous_receipt_id
result.previous_receipt_hash
```

This does not replace the conservation record. It adds continuity posture to the conservation record.

---

## Lineage verdicts

The v0.4 harness should introduce explicit lineage verdicts:

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

---

## Required v0.4 fixtures

The first v0.4 harness should prove at least these cases.

### 1. Prior receipt binds

A transition claims the exact prior receipt id and hash. The prior receipt is closed, current, and not superseded.

Expected result:

```text
lineage verdict: BOUND
closure may proceed
```

### 2. Missing prior receipt

A transition claims continuity but no prior receipt is present.

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

A transition binds to an old receipt that is not the current head of the chain.

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

Two valid-looking receipts claim to be the next receipt after the same prior receipt.

Expected result:

```text
lineage verdict: CONFLICT
closure blocked until resolved
```

---

## Closure relationship

Lineage does not replace closure.

The correct order is:

```text
scope/routing
-> node execution
-> merge/composition
-> lineage binding
-> closure predicate
-> next receipt basis
```

If lineage fails, closure must not return `CLOSED`.

If lineage succeeds, closure still may fail for ordinary completeness, authority, evidence, or coherence reasons.

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

## What green should mean in v0.4

A green v0.4 run should mean:

- a transition can bind to the exact prior receipt;
- a missing prior receipt blocks closure;
- a prior receipt id/hash mismatch blocks closure;
- a stale prior receipt blocks closure;
- a superseded prior receipt blocks closure while preserving history;
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

Transition entropy should remain advisory until sequential receipt lineage is proven.

Entropy can later measure how much transition cost, uncertainty, or state disturbance was absorbed or released, but it should not gate closure before the system can prove prior -> current -> next continuity.

---

## Version boundary statement

STCM v0.4 establishes that a transition cannot become a valid next receipt basis merely by closing locally. It must also bind to the correct prior receipt and avoid stale, superseded, missing, malformed, or conflicting lineage posture.
