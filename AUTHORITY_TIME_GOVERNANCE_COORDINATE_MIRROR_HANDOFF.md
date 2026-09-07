# Authority × Time Governance Coordinate Mirror Handoff

```text
task_id: AUTHORITY-TIME-GOVERNANCE-COORDINATE-001
repository: Admissible-Existence/STCM
cross_repo_owner: StegVerse-Labs/.github#1154
local_issue: #5
local_pull_request: #6
branch: fix/authority-time-governance-coordinate
state: SOURCE_AND_VALIDATOR_CORRECTED_EXACT_HEAD_VALIDATION_PENDING
```

This handoff owns only the Authority × Time/STCM receipt-semantic correction. `STCM_MIRROR_HANDOFF.md` retains unrelated STCM ownership.

Canonical primitive:

```text
Governance = Authority × Time
G = (Authority, Time)
Delta-time -/-> Delta-authority
```

Installed correction surfaces:

```text
integration/state-manifold-governance-binding.json
tools/check_cosv_task_projection.py
AUTHORITY_TIME_GOVERNANCE_COORDINATE_MIRROR_HANDOFF.md
```

STCM receipts remain evidence. They may preserve the applicable governance coordinate and transition relationships, but they do not manufacture Authority, Time, or causal transition identity.

The old `time_is_evidence_unless_explicitly_governing` invariant is removed. Time remains a governance coordinate; timestamps/durations are evidence or observations associated with it.

README impact determination: NO CHANGE REQUIRED. The root `README.md` is specifically the Closure Harness dispatcher-task document and does not define STCM governance primitives. Editing it to describe the organization-wide coordinate model would misrepresent that task-local README. The correction is instead discoverable through this mirror handoff and the binding/validator files.

Validation history: STCM Build PASS. Initial COSV projection validation failed only because the checker asserted the superseded binding status. The checker now validates Authority × Time fields and invariants directly. Exact-head rerun remains required.

Remaining: exact-head validation, merge/review gate, terminal AE rebind as separately declared, propagation through `.github#1156`.

This handoff is sufficient for continuation without the originating chat.
