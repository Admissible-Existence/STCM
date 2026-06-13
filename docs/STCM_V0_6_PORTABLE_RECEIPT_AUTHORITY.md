# STCM v0.6 — Portable Receipt Authority

## Status

Draft boundary.

This document begins STCM v0.6 by defining two portability vectors surfaced by AE Validation Factory:

```text
1. Hidden dependency refusal
2. Authority rebind
```

STCM v0.6 is not yet a completed portability proof.

It defines the boundary conditions under which cross-repository receipt continuity may become admissible.

---

## Purpose

STCM v0.6 extends the State Transition Conservation Model from local receipt conservation into cross-repository receipt continuity.

The central question is:

```text
When may a receipt generated under one repository boundary be accepted as valid basis for a transition in another repository boundary?
```

The answer cannot be based on platform visibility alone.

A receipt is portable only if the authority, lineage, conflict posture, deposit posture, and current basis can be evaluated from declared records.

---

## Core claim

```text
A cross-repo transition is admissible only when the accepting repository can independently evaluate the receipt basis, authority basis, lineage basis, and conflict posture of the incoming receipt.
```

If any basis depends on undeclared state, local-only authority, stale receipts, unresolved conflict, or undeclared deposit posture, the transition must not be treated as cross-repo valid.

---

## Definitions

### Source repository

The repository that emits or holds the receipt being offered across a repository boundary.

### Target repository

The repository that is asked to accept the receipt as basis for a transition, validation record, report, or next action.

### Portable receipt

A receipt whose required basis can be evaluated outside its source repository boundary.

### Local-only receipt

A receipt whose meaning depends on state, authority, policy, or context that exists only inside the source repository boundary.

### Hidden dependency

A dependency required for validation that is not declared in the receipt, target declaration, authority declaration, deposit policy, or lineage record.

### Authority rebind

The act of re-establishing authority in the accepting repository before an incoming receipt is allowed to become current basis for a target transition.

---

## Boundary vector 1 — Hidden dependency refusal

A receipt must be refused as portable if its validity depends on any undeclared dependency.

Examples:

```text
undeclared platform condition
undocumented repository rule
repo-local state not bound to the receipt
approval not represented by receipt
external result not preserved as evidence
```

### Rule

```text
If a required validation dependency is not declared and receipt-bound, the cross-repo transition must refuse portability.
```

### Refusal outcome

```text
HIDDEN_DEPENDENCY
```

### Consequence

The target repository may still record that an incoming object was observed.

It may not treat the object as portable authority or current basis.

---

## Boundary vector 2 — Authority rebind

A receipt may carry evidence from a source repository, but it does not automatically carry authority into the target repository.

The target repository must decide what authority must be re-established locally.

### Rule

```text
A portable receipt may become current basis in a target repository only after required authority is rebound under the target repository's declared authority posture.
```

### Rebind classes

```text
source-bound
  Authority exists only in the source repository.

evidence-portable
  Evidence may travel, but authority must be re-established.

authority-portable
  Authority may travel because it is explicitly receipt-bound and target-accepted.

refused
  Authority cannot be evaluated or accepted by the target repository.
```

### Refusal outcome

```text
AUTHORITY_NOT_PORTABLE
```

### Pending acceptance outcome

```text
PORTABLE_PENDING_BOUNDARY
```

This means the positive path is visible but not yet proven complete.

---

## Cross-repo admissibility predicate draft

Let:

```text
R  = incoming receipt
S  = source repository
T  = target repository
A  = authority basis
L  = lineage basis
C  = conflict posture
D  = deposit posture
H  = hidden dependency set
```

A receipt may be considered portability-eligible only if:

```text
S is declared
T is declared
R exists
R is current
C is closed or non-blocking
D allows incoming deposit or reference
H is empty
A is portable or successfully rebound in T
L remains continuous across S -> T
```

If any required element fails, the receipt is not cross-repo valid.

---

## Initial outcome map

```text
SOURCE_NOT_DECLARED
TARGET_NOT_DECLARED
MISSING_RECEIPT
RECEIPT_NOT_CURRENT
CONFLICT_OPEN
DEPOSIT_NOT_ALLOWED
HIDDEN_DEPENDENCY
AUTHORITY_NOT_PORTABLE
PORTABLE_PENDING_BOUNDARY
```

---

## Relationship to AE Validation Factory

AE Validation Factory may generate portability matrices and vector recommendations for STCM v0.6.

Those reports are discovery aids.

They do not prove cross-repo validity until this boundary is completed, fixture-backed, and replayed against declared targets.

---

## Completion requirements

STCM v0.6 is not complete until the following exist:

```text
portable receipt authority rule
authority rebind rule
hidden dependency refusal rule
cross-repo conflict posture rule
current-basis rule
deposit acceptance rule
lineage continuity rule
fixture matrix
closure harness layer
saturation report
validation record
```

---

## Boundary statement

STCM v0.6 does not open every repository to the factory.

It defines the conditions under which any repository may become eligible for governed cross-repo validation.
