# STCM v0.6 Artifact Capture

## Status

```text
record_status: awaiting_manual_artifact_values
boundary: stcm_v0_6
workflow: core-lite-intake
registered_task: stcm-v0-6-portability-predicate
```

## Purpose

The v0.6 executable surface is now governed by the core-lite intake path. The final promotion from draft boundary to validated draft candidate requires the saturation artifact from the green workflow run.

The connector did not expose a workflow run for the checked commit, so these values must be captured from the GitHub Actions UI or artifact download.

## Expected artifact

```text
artifact_name: core-lite-intake-reports
artifact_path: tools/closure-harness/reports/stcm_v0_6_portability_saturation.json
```

## Required saturation fields

```text
stage: stcm_v0_6_portability_saturation
boundary: stcm_v0_6
row_count: 102400
unexpected: 0
saturated: true
boundary_status: validated_draft_candidate
```

## Manual capture fields

```text
run_id: TODO
run_url: TODO
artifact_id: TODO
artifact_name: core-lite-intake-reports
artifact_sha256: TODO
captured_by: TODO
captured_at_utc: TODO
```

## Promotion rule

```text
Only after the artifact confirms row_count=102400, unexpected=0, saturated=true, and boundary_status=validated_draft_candidate may docs/STCM_V0_6_VALIDATION_RECORD.md be promoted from pending_artifact_confirmation to validated_draft_candidate.
```

## Source basis

```text
main_authority_doc: 0314c3737c213362059f3b451ab822d3ebe059c8
validation_record: ee705071e3b1a057f0437f6fcc3223cb94e2bac3
portability.py: 250fc7b9baeeac0bc4315d2a2163e4130643db50
portability_fixtures.py: fbb6cbbcf5127accf1a95dcfe1e03b017650ae9f
run_closure_harness.py: 3b33f1b109241210d057b57216b877a8a0c1de00
core_lite_intake: 08a7ff589f8c556350696c9ac12ad78c0777c0e4
task_registry: 38e1013cf7daf620455ef8cd15be8b019f4cb756
```
