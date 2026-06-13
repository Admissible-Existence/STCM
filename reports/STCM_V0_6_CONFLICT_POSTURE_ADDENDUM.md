# STCM v0.6 Conflict Posture Addendum

## Status

```text
boundary: stcm_v0_6
addendum_status: executable_predicate_surface_updated
```

## Purpose

This addendum records the conflict-posture refinement added to the STCM v0.6 portable receipt authority predicate.

The executable predicate no longer treats conflict as a boolean.

It now evaluates declared conflict posture before deposit, hidden dependency, lineage, and authority posture.

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

## Positive conflict postures

```text
none
non_blocking
resolved_accepted
```

## Blocking conflict outcomes

```text
CONFLICT_OPEN
CONFLICT_UNDER_REVIEW
CONFLICT_RESOLUTION_REJECTED
CONFLICT_SUPERSEDED_BY_RESOLUTION
CONFLICT_EXTERNAL_UNRESOLVED
```

## Updated fixture surface

```text
2 source states
2 target states
5 receipt postures
8 conflict postures
5 deposit postures
2 hidden dependency states
2 lineage states
8 authority postures

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
A receipt can be current, depositable, lineage-continuous, and authority-valid, but still inadmissible if conflict posture is unresolved, rejected, under review, or otherwise blocking.
```
