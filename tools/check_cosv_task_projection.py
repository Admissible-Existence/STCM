#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
rec=json.loads((ROOT/"data/cosv/task-vectors/STCM-RELATIONAL-GOVERNANCE-MATH-ALIGNMENT-001.json").read_text())
bind=json.loads((ROOT/"integration/state-manifold-governance-binding.json").read_text())
row=idx["tasks"][0]
m=rec["exact_metrics"]
assert idx["profile"]=="task.v1" and idx["width"]==14 and idx["authority_effect"]=="NONE"
assert row["task_id"]=="STCM-RELATIONAL-GOVERNANCE-MATH-ALIGNMENT-001"
assert rec["vector"]==row["vector"]=="40000000101000"
assert m["lifecycle"]=="CLAIMED_INTEGRATION"
assert m["blocker_count"]==1
assert bind["source"]["goal_id"]=="AE-AUTO-0011"
assert bind["source"]["validation_state"]=="PENDING_MACHINE_OWNED_TERMINAL_DERIVATION"
assert bind["status"]=="BOUND_PENDING_EXACT_TERMINAL_AE_MATH"
assert m["evidence_complete"] is False
assert m["activated"] is False and m["propagated"] is False
assert idx["coverage"]["repository_active_task_surface_audit_complete"] is True
assert idx["coverage"]["repository_vector_present_claimed"] is False
print("STCM_COSV_PROJECTION_PASS tasks=1 blockers=1 repository_vector_present=false")
