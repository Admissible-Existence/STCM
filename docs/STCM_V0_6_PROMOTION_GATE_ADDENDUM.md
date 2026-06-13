# STCM v0.6 Promotion Gate Addendum

## Status

```text
boundary: stcm_v0_6
record_status: pending_artifact_confirmation
promotion_gate: reports/stcm_v0_6_promotion_gate.yaml
```

## Purpose

This addendum records the promotion gate for STCM v0.6 without changing the current validation status.

The promotion gate defines the transition from `pending_artifact_confirmation` to `validated_draft_candidate`.

## Required reports

```text
reports/stcm_v0_6_portability_saturation.json
reports/stcm_v0_6_artifact_capture_status.json
```

## Required promotion evidence

```text
row_count: 102400
unexpected: 0
saturated: true
boundary_status: validated_draft_candidate
artifact_capture_validated: true
```

## Non-effects

```text
may_claim_final_cross_repo_validity: false
may_open_all_repositories_to_factory: false
may_bypass_target_declaration: false
```

## Source commits

```text
artifact_capture_check.py: 03b0001c22893db52b9258ac8f25dd2534632c63
task_registry.yaml: 50038db2e0239ec6c4feab3defebd94a80dd8352
promotion_gate.yaml: 47d8540b64c0a1e450b92c36df547668a5118658
validation_record: e516595408bad32425298a8ce4ef044613e7df11
```
