# STCM v0.5 — Receipt Store and Conflict Resolution Policy

## Status

This document defines the next boundary after STCM v0.4 sequential receipt lineage passed green.

v0.4 proved that a transition cannot become a valid next receipt basis merely by closing locally. It must also bind to the correct prior receipt and avoid stale, superseded, missing, malformed, or conflicting lineage posture.

v0.5 asks the next operational question:

```text
Where does lineage truth come from, and how is conflict resolved without deleting history?
```

The v0.4 lineage layer accepts `chain_head` and `known_successors` as supplied facts. v0.5 must define the governed source of those facts.

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

## Receipt store boundary

The receipt store should be treated as a governed index over receipt facts, not as a free-form database.

At minimum it must answer:

```text
get_receipt(receipt_id)
get_chain_head(chain_id)
get_successors(prior_receipt_id)
is_superseded(receipt_id)
get_conflicts(prior_receipt_id)
get_resolution(conflict_id)
```

These operations do not decide closure by themselves. They provide the facts that the lineage layer uses before closure.

---

## Minimal receipt record

A v0.5 receipt record should preserve at least:

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

The store may later add signatures, authority records, external proof references, and cross-repository portability metadata, but the first boundary should keep the record small enough to test.

---

## Store-derived lineage

v0.5 should stop relying only on caller-supplied `chain_head` and `known_successors` fixtures.

Instead, the harness should prove:

```text
receipt_store -> chain_head
receipt_store -> known_successors
receipt_store -> supersession facts
receipt_store -> conflict facts
```

Then the lineage gate should evaluate using facts retrieved from the store.

The transition may still present a claimed prior receipt, but the store decides whether that claim matches the governed chain state.

---

## Conflict policy boundary

Conflict is not merge.

A conflict occurs when more than one plausible successor claims the same prior receipt at the same sequence position, or when receipt identity/hash facts disagree.

A conflict policy must decide posture, not erase evidence.

The first v0.5 policy should support these states:

```text
OPEN
RESOLVED_ACCEPT_ONE
RESOLVED_SUPERSEDE_ALL_BUT_ONE
RESOLVED_REJECT_ALL
ESCALATED
```

Conflict resolution must never delete the losing receipts. It changes whether they are valid as future continuation bases.

---

## Supersession policy boundary

Supersession is not deletion.

A superseded receipt remains historically valid for the time at which it closed. It is no longer current for future continuation.

The store must preserve both facts:

```text
valid_as_closed: true
current_basis: false
superseded_by: <receipt_id>
```

This allows audit history to remain intact while preventing stale continuation.

---

## Required v0.5 fixtures

The first v0.5 harness should prove at least these cases.

### 1. Store returns current head

Given a chain with receipts `R1 -> R2 -> R3`, the store returns `R3` as the current head.

Expected result:

```text
store verdict: HEAD_FOUND
lineage may evaluate against R3
```

### 2. Store detects stale prior

A transition claims `R2` while the store head is `R3`.

Expected result:

```text
store-derived lineage: STALE
closure blocked
```

### 3. Store detects competing successors

Two receipts claim the same prior receipt and same sequence index.

Expected result:

```text
conflict status: OPEN
lineage verdict: CONFLICT
closure blocked
```

### 4. Store resolves conflict by accepting one successor

A conflict exists, and policy accepts one receipt as the current continuation.

Expected result:

```text
accepted receipt becomes current basis
rejected competing receipts remain historical but not current
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
lineage verdict: STALE or CONFLICT
closure blocked
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

## Harness order after v0.5

The intended order becomes:

```text
scope/routing
-> node execution
-> merge/composition
-> receipt store lookup
-> lineage binding
-> conflict policy check
-> closure predicate
-> next receipt basis
-> receipt store update
```

The store lookup and conflict policy check must occur before closure can establish a new next basis.

The store update must occur only after closure succeeds.

---

## What green should mean in v0.5

A green v0.5 run should mean:

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

## What v0.5 should not prove yet

A green v0.5 run does not need to prove:

- distributed consensus across remote stores;
- cryptographic proof beyond deterministic fixture hashes;
- cross-repository portability;
- external authority adjudication;
- numeric entropy;
- human governance council policy;
- permanent storage implementation.

Those remain later boundaries.

---

## Version boundary statement

STCM v0.5 establishes that lineage truth must come from a governed receipt store, not merely from transition-provided claims. The store preserves history, identifies heads and successors, detects conflicts, supports supersession without deletion, and prevents rejected, stale, missing, or conflicting receipts from becoming future continuation bases.
