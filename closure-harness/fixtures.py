from __future__ import annotations


def records() -> list[dict]:
    return [
        {
            "transition_id": "stcm-positive-001",
            "stage": "low:single_record_closure",
            "expected": "CLOSED",
            "basis": "all required fields present",
        },
        {
            "transition_id": "stcm-negative-001",
            "stage": "low:missing_basis",
            "expected": "BLOCKED",
            "basis": "negative fixture should be blocked before closure",
        },
        {
            "transition_id": "stcm-negative-002",
            "stage": "medium:null_basis_guard",
            "expected": "CLOSED",
            "basis": None,
        },
    ]
