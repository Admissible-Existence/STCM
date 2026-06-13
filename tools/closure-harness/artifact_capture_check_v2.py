#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

sat_path = Path("reports/stcm_v0_6_portability_saturation.json")
status_path = Path("reports/stcm_v0_6_artifact_capture_status.json")

expected = {
    "stage": "stcm_v0_6_portability_saturation",
    "boundary": "stcm_v0_6",
    "row_count": 25600,
    "unexpected": 0,
    "saturated": True,
    "boundary_status": "validated_draft_candidate",
}

status_path.parent.mkdir(parents=True, exist_ok=True)

if not sat_path.exists():
    status = {
        "stage": "stcm_v0_6_artifact_capture_check",
        "status": "missing_saturation_report",
        "validated": False,
        "expected_report": str(sat_path),
        "expected": expected,
    }
    status_path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n")
    print(json.dumps(status, indent=2, sort_keys=True))
    raise SystemExit(1)

report = json.loads(sat_path.read_text())
mismatches = {}
for key, want in expected.items():
    got = report.get(key)
    if got != want:
        mismatches[key] = {"expected": want, "got": got}

validated = not mismatches
status = {
    "stage": "stcm_v0_6_artifact_capture_check",
    "status": "validated_draft_candidate" if validated else "artifact_mismatch",
    "validated": validated,
    "saturation_report": str(sat_path),
    "capture_status_report": str(status_path),
    "expected": expected,
    "mismatches": mismatches,
}
status_path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n")
print(json.dumps(status, indent=2, sort_keys=True))
raise SystemExit(0 if validated else 1)
