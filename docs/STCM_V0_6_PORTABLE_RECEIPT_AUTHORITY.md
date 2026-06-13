# STCM v0.6 — Portable Receipt Authority

## Status

Draft boundary.

This document begins STCM v0.6 by defining portability vectors surfaced by AE Validation Factory:

```text
1. Hidden dependency refusal
2. Authority posture and rebind
3. Cross-repo lineage continuity
4. Deposit posture
5. Receipt posture
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

A receipt is portable only if the authority, lineage, conflict posture, deposit posture, receipt posture, and current basis can be evaluated from declared records.

---

## Core claim

```text
A cross-repo transition is admissible only when the accepting repository can independently evaluate the receipt basis, authority basis, lineage basis, deposit posture, receipt posture, and conflict posture of the incoming receipt.
```

If any basis depends on undeclared state, local-only authority, stale receipts, superseded receipts, missing receipts, conflict-linked receipts, unresolved conflict, broken lineage, technical-only access, expired authority, scope mismatch, or undeclared deposit posture, the transition must not be treated as cross-repo valid.

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

### Cross-repo lineage continuity

The condition in which the receipt lineage remains continuous when a receipt crosses from source repository to target repository.

### Deposit posture

The declared acceptance posture of the target repository for incoming receipts, validation records, or references.

### Receipt posture

The status of the incoming receipt as current, missing, stale, superseded, or conflict-linked.

### Authority posture

The status of the authority attached to, implied by, or required for the incoming receipt.

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

## Boundary vector 2 — Authority posture and rebind

A receipt may carry evidence from a source repository, but it does not automatically carry authority into the target repository.

The target repository must decide what authority must be re-established locally.

### Rule

```text
A portable receipt may become current basis in a target repository only when its authority posture is portable, rebound, or target-accepted within scope.
```

### Authority posture classes

```text
source_bound
  Authority exists only in the source repository.

evidence_only
  Evidence may travel, but no authority travels with it.

delegated
  Authority has been delegated but still requires target-side rebind.

rebound
  Authority has been re-established in the target repository.

portable_signed
  Authority is explicitly signed, receipt-bound, and target-accepted.

expired
  Authority existed but is no longer valid.

scope_mismatch
  Authority does not cover the target transition scope.

refused
  Authority cannot be evaluated or accepted by the target repository.
```

### Refusal outcomes

```text
AUTHORITY_NOT_PORTABLE
AUTHORITY_EXPIRED
AUTHORITY_SCOPE_MISMATCH
AUTHORITY_REBIND_REQUIRED
```

### Pending acceptance outcome

```text
PORTABLE_PENDING_BOUNDARY
```

This means the positive path is visible but not yet proven complete.

---

## Boundary vector 3 — Cross-repo lineage continuity

A receipt cannot become portable current basis if the accepting repository cannot evaluate continuity from the source receipt chain to the target receipt chain.

### Rule

```text
If receipt lineage does not remain continuous across the source-to-target repository boundary, the target repository must refuse portability.
```

### Refusal outcome

```text
LINEAGE_NOT_CONTINUOUS
```

### Consequence

The incoming receipt may be stored as observed evidence.

It may not become current basis for a target transition.

---

## Boundary vector 4 — Deposit posture

Technical write access is not the same thing as admissible deposit authority.

A target repository must declare whether incoming records may be accepted, referenced, refused, or treated as technical-only access.

### Deposit posture classes

```text
declared_accept
  Incoming validation records may be deposited under declared policy.

declared_reference_only
  Incoming records may be referenced, but not made current basis.

missing_policy
  No target deposit policy is declared.

refuses_external
  Target policy refuses external validation records.

technical_only
  A technical write path exists, but admissible deposit authority is not declared.
```

### Refusal outcomes

```text
DEPOSIT_NOT_ALLOWED
TECHNICAL_ACCESS_NOT_AUTHORITY
```

### Reference-only outcome

```text
REFERENCE_ONLY_PENDING_BOUNDARY
```

---

## Boundary vector 5 — Receipt posture

An incoming receipt must be evaluated by posture before it can be considered portable.

### Receipt posture classes

```text
current
  Receipt is eligible for current-basis evaluation.

missing
  No receipt exists to evaluate.

stale
  Receipt exists but is not current.

superseded
  Receipt has been replaced by a later receipt.

conflict_linked
  Receipt is linked to unresolved or blocking conflict posture.
```

### Refusal outcomes

```text
MISSING_RECEIPT
RECEIPT_STALE
RECEIPT_SUPERSEDED
RECEIPT_CONFLICT_LINKED
```

---

## Cross-repo admissibility predicate draft

Let:

```text
R  = incoming receipt
S  = source repository
T  = target repository
A  = authority posture
L  = lineage basis
C  = conflict posture
D  = deposit posture
P  = receipt posture
H  = hidden dependency set
```

A receipt may be considered portability-eligible only if:

```text
S is declared
T is declared
R exists
P is current
C is closed or non-blocking
D allows incoming deposit or reference
H is empty
L remains continuous across S -> T
A is rebound or portable-signed
```

If any required element fails, the receipt is not cross-repo valid.

---

## Initial outcome map

```text
SOURCE_NOT_DECLARED
TARGET_NOT_DECLARED
MISSING_RECEIPT
RECEIPT_STALE
RECEIPT_SUPERSEDED
RECEIPT_CONFLICT_LINKED
CONFLICT_OPEN
DEPOSIT_NOT_ALLOWED
TECHNICAL_ACCESS_NOT_AUTHORITY
HIDDEN_DEPENDENCY
LINEAGE_NOT_CONTINUOUS
AUTHORITY_NOT_PORTABLE
AUTHORITY_EXPIRED
AUTHORITY_SCOPE_MISMATCH
AUTHORITY_REBIND_REQUIRED
REFERENCE_ONLY_PENDING_BOUNDARY
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
