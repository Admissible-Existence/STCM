# STCM v0.6 Status

## Boundary

```text
status: draft
boundary: Portable Receipt Authority and Cross-Repo Continuity
```

## Current executable predicate surface

```text
source declaration
target declaration
receipt posture
conflict posture
deposit posture
hidden dependency
lineage continuity
authority posture
```

## Current fixture scale

```text
2 source states
2 target states
5 receipt postures
2 conflict postures
5 deposit postures
2 hidden dependency states
2 lineage states
8 authority postures

2 * 2 * 5 * 2 * 5 * 2 * 2 * 8 = 25600 rows
```

## Current posture classes

### Receipt posture

```text
current
missing
stale
superseded
conflict_linked
```

### Deposit posture

```text
declared_accept
declared_reference_only
missing_policy
refuses_external
technical_only
```

### Authority posture

```text
source_bound
evidence_only
delegated
rebound
portable_signed
expired
scope_mismatch
refused
```

## Positive draft outcomes

```text
PORTABLE_PENDING_BOUNDARY
REFERENCE_ONLY_PENDING_BOUNDARY
```

## Refusal outcomes

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
```

## Current claim boundary

```text
STCM v0.6 is executable and fixture-backed as a draft boundary.
It is not yet a final cross-repo validity claim.
```
