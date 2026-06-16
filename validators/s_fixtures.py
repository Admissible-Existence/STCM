"""Fixtures for STCM Wave 1 bootstrap validation."""

BASE = {
    "record_id": "s-001",
    "repo": "Admissible-Existence/STCM",
    "boundary": "stcm_core_lite_v0_1",
    "readme_present": True,
    "task_registry_present": True,
    "existing_harness_present": True,
    "closure_surface_present": True,
    "status": "READY",
    "ready": True,
    "reason": "bootstrap surface present",
    "timestamp": "2026-06-16T00:00:00Z",
}


def with_changes(**changes):
    item = dict(BASE)
    item.update(changes)
    return item


FIXTURES = [
    {"id": "case_ready", "expected": "READY", "record": with_changes()},
    {"id": "case_no_readme", "expected": "INCOMPLETE", "record": with_changes(readme_present=False, status="INCOMPLETE", ready=False, reason="readme missing")},
    {"id": "case_no_registry", "expected": "INCOMPLETE", "record": with_changes(task_registry_present=False, status="INCOMPLETE", ready=False, reason="registry missing")},
    {"id": "case_no_harness", "expected": "INCOMPLETE", "record": with_changes(existing_harness_present=False, status="INCOMPLETE", ready=False, reason="harness missing")},
    {"id": "case_no_surface", "expected": "INCOMPLETE", "record": with_changes(closure_surface_present=False, status="INCOMPLETE", ready=False, reason="surface missing")},
    {"id": "case_blocked", "expected": "BLOCKED", "record": with_changes(status="READY", ready=False, reason="ready flag false")},
]
