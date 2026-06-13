# STCM v0.5 — Receipt Store and Conflict Resolution Policy

## Status

This document records the green operational boundary after STCM v0.5 receipt store and conflict policy fixtures passed.

v0.4 proved that a transition cannot become a valid next receipt basis merely by closing locally. It must also bind to the correct prior receipt and avoid stale, superseded, missing, malformed, or conflicting lineage posture.

v0.5 answers the next operational question:

```text
Where does lineage truth come from, and how is conflict resolved without deleting history?
```

The v0.4 lineage layer accepted `chain_head` and `known_successors` as supplied facts. v0.5 derives those facts from a governed receipt store.

---

## Core claim

A receipt chain cannot rely only on the transition that presents a prior receipt. The system must maintain a receipt store that can answer:

- what receipt is the current chain head;
- which receipts claim a given prior receipt;
- whether a receipt has been superseded;
- whether two successors conflict;
- whether a conflict has been resolved by policy;
- whether historical receipts remain valid-as-closed even after supersession.

The receipt store is not merely storage. It is the authority surface for lineage facts.

---

## Implemented harness order

The current closure harness now evaluates eight layers:

1. Node layer — each Prime Node tested in isolation.
2. Composed layer — transition -> PN outputs -> conservation record -> closure.
3. Routing layer — ignore / reroute / escalate front-gate behavior.
4. Routed-hop layer — source reroutes -> recognized owner activates -> destination closes or governed non-closes.
5. Merge layer — multi-node outputs merge into a coherent transition receipt only when required conditions hold.
6. Lineage layer — prior -> current -> next continuity gate.
7. Store layer — governed receipt store + conflict policy pipeline.
8. Closure layer — direct closure-predicate regression.

The v0.5 store pipeline executes this order:

```text
receipt store lookup
-> lineage binding
-> conflict policy check
-> closure predicate
-> next receipt basis
-> receipt store update candidate
```

The store lookup and conflict policy check occur before closure can establish a new next basis.

The store update candidate is produced only after closure succeeds.

---

## Receipt store boundary

The receipt store is implemented as an append-only governed index over receipt facts.

It answers:

```text
get_receipt(receipt_id)
get_chain_head(chain_id)
get_successors(prior_receipt_id)
is_superseded(receipt_id)
get_conflicts(prior_receipt_id)
get_resolution(conflict_id)
```

These operations do not decide closure by themselves. They provide the facts that the lineage and conflict-policy checks use before closure.

The store has no delete operation.

---

## Implemented receipt record

The v0.5 receipt record preserves at least:

```text
receipt.id
receipt.hash
receipt.chain_id
receipt.sequence_index
receipt.previous_receipt_id
receipt.previous_receipt_hash
receipt.state
receipt.closed
receipt.closed_at
receipt.superseded_by
receipt.conflict_id
receipt.resolution_status
receipt.source_transition_id
receipt.conservation_record_hash
```

It also exposes derived posture:

```text
valid_as_closed
current_basis
```

A receipt is current basis only when it is closed, not superseded, not rejected by conflict policy, and not under an open conflict.

---

## Store-derived lineage

v0.5 stops relying only on caller-supplied `chain_head` and `known_successors` fixtures.

The implemented pipeline derives:

```text
receipt_store -> chain_head
receipt_store -> known_successors
receipt_store -> supersession facts
receipt_store -> conflict facts
```

The transition may still present a claimed prior receipt, but the store resolves that claim into store-authoritative receipt facts before lineage is evaluated.

The transition can no longer assert its own lineage truth.

---

## Conflict policy boundary

Conflict is not merge.

A conflict occurs when more than one plausible successor claims the same prior receipt at the same sequence position, or when receipt identity/hash facts disagree.

The implemented conflict states are:

```text
OPEN
RESOLVED_ACCEPT_ONE
RESOLVED_SUPERSEDE_ALL_BUT_ONE
RESOLVED_REJECT_ALL
ESCALATED
```

An open conflict blocks closure.

A resolved conflict can accept one continuation without deleting the other receipts.

Rejected or superseded receipts remain queryable, but they cannot serve as current future-continuation bases.

---

## Supersession policy boundary

Supersession is not deletion.

A superseded receipt remains historically valid for the time at which it closed. It is no longer current for future continuation.

The store preserves both facts:

```text
valid_as_closed: true
current_basis: false
superseded_by: <receipt_id>
```

This allows audit history to remain intact while preventing stale continuation.

---

## Implemented v0.5 fixtures

The green store layer proves these cases.

### 1. Store returns current head

Given a chain with receipts `R1 -> R2 -> R3`, the store returns `R3` as the current head and permits a valid successor to close.

Expected result:

```text
store head: R3
lineage verdict: BOUND
closure may proceed
```

### 2. Store detects stale prior

A transition claims `R2` while the store head is `R3`.

Expected result:

```text
store-derived lineage: STALE
closure blocked
```

### 3. Store detects competing successors

Two receipts claim the same prior receipt and same sequence index under an open conflict.

Expected result:

```text
conflict status: OPEN
closure blocked
```

### 4. Store resolves conflict by accepting one successor

A conflict exists, and policy accepts one receipt as the current continuation.

Expected result:

```text
accepted receipt becomes current basis
rejected competing receipt remains historical but not current
```

### 5. Store supersedes old receipt without deleting it

A receipt is superseded by a later receipt.

Expected result:

```text
old receipt valid_as_closed=true
old receipt current_basis=false
new receipt may become head
```

### 6. Rejected receipt cannot serve as prior

A transition claims a receipt rejected by conflict policy as its prior basis.

Expected result:

```text
closure blocked
rejected prior cannot serve as current basis
```

### 7. Missing store receipt blocks continuation

A transition claims a prior receipt id that is not found in the store.

Expected result:

```text
lineage verdict: MISSING_PRIOR
closure blocked
```

### 8. Store preserves audit history

After supersession or conflict resolution, all involved receipts remain queryable.

Expected result:

```text
history preserved
future continuation restricted
```

---

## What green means in v0.5

A green v0.5 run means:

- chain head is derived from the receipt store;
- known successors are derived from the receipt store;
- stale priors are detected from store facts;
- competing successors are detected as conflict;
- open conflict blocks closure;
- conflict resolution can accept one continuation without deleting others;
- supersession preserves historical validity while blocking future continuation;
- rejected or superseded receipts cannot serve as current prior basis;
- missing store receipts block continuation;
- successful closure can produce a store-update candidate for the next receipt basis.

---

## What v0.5 does not prove yet

A green v0.5 run does not yet prove:

- distributed consensus across remote stores;
- cryptographic proof beyond deterministic fixture hashes;
- cross-repository portability;
- external authority adjudication;
- numeric entropy;
- human governance council policy;
- permanent storage implementation.

Those remain later boundaries.

---

## Next boundary

The next clean boundary is portability.

v0.5 proves that the store is the authority surface inside this harness. The next question is whether that store-derived admissibility posture can remain valid when receipts move across repositories, projects, or authority domains.

The likely v0.6 boundary is:

```text
STCM v0.6 — Portable Receipt Authority and Cross-Repo Continuity
```

---

## Version boundary statement

STCM v0.5 establishes that lineage truth must come from a governed receipt store, not merely from transition-provided claims. The store preserves history, identifies heads and successors, detects conflicts, supports supersession without deletion, and prevents rejected, stale, missing, or conflicting receipts from becoming future continuation bases.

This is the first executable boundary for store-derived lineage truth and governed conflict posture.
