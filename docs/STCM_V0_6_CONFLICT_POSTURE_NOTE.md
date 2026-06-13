# STCM v0.6 Conflict Posture Note

## Status

```text
boundary: stcm_v0_6
note_status: companion_note
main_document: docs/STCM_V0_6_PORTABLE_RECEIPT_AUTHORITY.md
```

## Purpose

This note records the v0.6 conflict posture refinement as a companion to the main portable receipt authority document.

The executable predicate no longer evaluates conflict as a boolean.

It evaluates declared conflict posture.

## Conflict posture classes

```text
none
non_blocking
open_blocking
under_review
resolved_accepted
resolved_rejected
superseded_by_resolution
unresolved_external
```

## Blocking outcomes

```text
CONFLICT_OPEN
CONFLICT_UNDER_REVIEW
CONFLICT_RESOLUTION_REJECTED
CONFLICT_SUPERSEDED_BY_RESOLUTION
CONFLICT_EXTERNAL_UNRESOLVED
```

## Positive draft conflict postures

```text
none
non_blocking
resolved_accepted
```

## Updated fixture surface

```text
row_count: 102400
```

## Source commits

```text
portability.py: 250fc7b9baeeac0bc4315d2a2163e4130643db50
portability_fixtures.py: fbb6cbbcf5127accf1a95dcfe1e03b017650ae9f
run_closure_harness.py: 3b33f1b109241210d057b57216b877a8a0c1de00
validation_record: 672b5bf6f73acb8acfa084f5e17067b6167e8ee7
```

## Boundary statement

```text
Conflict posture is not visibility.
Conflict posture is a declared admissibility condition.
```
