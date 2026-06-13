# STCM v0.6 Validation Record

## Status

```text
record_status: pending_artifact_confirmation
boundary: stcm_v0_6
boundary_name: Portable Receipt Authority and Cross-Repo Continuity
```

## Purpose

This record is the formal landing point for the STCM v0.6 portability saturation result.

It must not be treated as a final cross-repo validity claim until the saturation artifact exists and records zero unexpected rows.

## Predicate surface

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

## Fixture scale

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

## Required saturation artifact

```text
reports/stcm_v0_6_portability_saturation.json
```

## Required artifact fields

```text
stage: stcm_v0_6_portability_saturation
boundary: stcm_v0_6
row_count: 102400
unexpected: 0
saturated: true
boundary_status: validated_draft_candidate
```

## Current claim boundary

```text
STCM v0.6 is executable and fixture-backed as a draft boundary.
It becomes a validated draft candidate only after the saturation artifact confirms zero unexpected rows.
It is not a final cross-repo validity claim.
```

## Source code basis

```text
docs/STCM_V0_6_PORTABLE_RECEIPT_AUTHORITY.md
tools/closure-harness/portability.py
tools/closure-harness/portability_fixtures.py
tools/closure-harness/portability_predicate_check.py
tools/closure-harness/run_closure_harness.py
.github/workflows/core-lite-intake.yml
tools/task_registry.yaml
```

## Latest source commits

```text
portable_receipt_authority.md: 0314c3737c213362059f3b451ab822d3ebe059c8
portability.py: 250fc7b9baeeac0bc4315d2a2163e4130643db50
portability_fixtures.py: fbb6cbbcf5127accf1a95dcfe1e03b017650ae9f
run_closure_harness.py: 3b33f1b109241210d057b57216b877a8a0c1de00
core-lite-intake.yml: 08a7ff589f8c556350696c9ac12ad78c0777c0e4
task_registry.yaml: 38e1013cf7daf620455ef8cd15be8b019f4cb756
```
