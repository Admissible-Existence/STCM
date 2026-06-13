# STCM v0.7 Cross-Repo Adoption Handshake

## Purpose

STCM v0.7 defines the receiving-repo handshake for a portable receipt.

STCM v0.6 answers whether a receipt is portable or reboundable.

STCM v0.7 answers what the receiving repo does with that receipt.

## Boundary

```text
boundary: stcm_v0_7
status: draft
role: receiving_repo_adoption_handshake
```

## Inputs

```text
source_receipt_present
receiver_declared
portable_status
conflict_blocking
receiver_decision
```

## Outcomes

```text
ADOPTED
REBOUND
QUARANTINED
REJECTED
INSUFFICIENT_DECLARATION
AUTHORITY_MISMATCH
CONFLICT_BLOCKED
```

## Rule order

```text
1. Missing source receipt or receiver declaration -> INSUFFICIENT_DECLARATION
2. Invalid portable authority -> AUTHORITY_MISMATCH
3. Blocking conflict -> CONFLICT_BLOCKED
4. Receiver reject -> REJECTED
5. Receiver quarantine -> QUARANTINED
6. Receiver rebind -> REBOUND
7. Receiver adopt with portable authority -> ADOPTED
8. Otherwise -> AUTHORITY_MISMATCH
```

## Non-effects

```text
may_claim_final_cross_repo_validity: false
may_auto_open_receiver_repo: false
may_bypass_receiver_declaration: false
```
