#!/usr/bin/env python3
"""artifact_capture_check.py - STCM v0.6 saturation artifact validator.

This task validates the generated v0.6 saturation JSON inside the governed
core-lite-intake workspace. It does not download GitHub artifacts. It checks the
local report emitted by portability_predicate_check.py and writes a compact
machine-readable capture status report.
"""

from __future__ import annotations

import json
from pathlib import Path

SATURATION_PATH = Path("reports/stcm_v0_6_portability_saturation.json")
STATUS_PATH = Path("reports/stcm_v0_6_artifact_capture_status.json")

EXPECTED = {
    "stage": "stcm_v0_6_portability_saturation",
    "boundary": "stcm_v0_6",
    "row_count": 102400,
    "unexpected": 0,
    "saturated": True,
    "boundary_status": "validated_draft_candidate",
}


def main() -> int:
    STATUS_PATH.parent.mkdir(exist_ok=True)

    if not SATURATION_PATH.exists():
        status = {
            "stage": "stcm_v0_6_artifact_capture_check",
            "status": "missing_saturation_report",
            "validated": False,
            "expected_report": str(SATURATION_PATH),
            "expected": EXPECTED,
        }
        STATUS_PATH.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(status, indent=2, sort_keys=True))
        return 1

    report = json.loads(SATURATION_PATH.read_text(encoding="utf-8"))
    mismatches = {}
    for key, expected_value in EXPECTED.items():
        got = report.get(key)
        if got != expected_value:
            mismatches[key] = {"expected": expected_value, "got": got}

    validated = not mismatches
    status = {
        "stage": "stcm_v0_6_artifact_capture_check",
        "status": "validated_draft_candidate" if validated else "artifact_mismatch",
        "validated": validated,
        "saturation_report": str(SATURATION_PATH),
        "capture_status_report": str(STATUS_PATH),
        "expected": EXPECTED,
        "mismatches": mismatches,
    }
    STATUS_PATH.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2, sort_keys=True))
    return 0 if validated else 1


if __name__ == "__main__":
    raise SystemExit(main())
