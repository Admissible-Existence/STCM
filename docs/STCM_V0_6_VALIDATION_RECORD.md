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
2 conflict postures
5 deposit postures
2 hidden dependency states
2 lineage states
8 authority postures

row_count: 25600
```

## Required saturation artifact

```text
reports/stcm_v0_6_portability_saturation.json
```

## Required artifact fields

```text
stage: stcm_v0_6_portability_saturation
boundary: stcm_v0_6
row_count: 25600
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
tools/closure-harness/portability.py
tools/closure-harness/portability_fixtures.py
tools/closure-harness/portability_predicate_check.py
tools/closure-harness/run_closure_harness.py
.github/workflows/stcm-v0-6-portability.yml
```

## Latest source commits

```text
portability.py: a8ee178b6713ec437fbe1921eb3f6e930c2cce14
portability_fixtures.py: 4ca2bfe4d6cc259dfc316a706aff1dfe7ae24a30
portability_predicate_check.py: 71d4f3690d20f0d9b641082e275ff64ad46517df
run_closure_harness.py: af29c59666c4f681ff66c7db01549e2dd9c60bcd
workflow: aacf971454f5e1f9739ffbe52b0ca8e2c4a89fb7
```
