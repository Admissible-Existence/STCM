from __future__ import annotations

REQUIRED_FIELDS = ("transition_id", "stage", "expected", "basis")


def decide(record: dict) -> dict:
    missing = [field for field in REQUIRED_FIELDS if record.get(field) in (None, "")]
    if missing:
        return {
            "verdict": "PROVEN_UNSATISFIABLE",
            "reason": "missing_required_field",
            "fields": missing,
        }
    expected = record.get("expected")
    if expected not in {"CLOSED", "BLOCKED"}:
        return {
            "verdict": "PROVEN_UNSATISFIABLE",
            "reason": "unsupported_expected_verdict",
            "fields": ["expected"],
        }
    if expected == "BLOCKED":
        return {
            "verdict": "PROVEN_UNSATISFIABLE",
            "reason": "negative_fixture_correctly_blocked",
            "fields": [],
        }
    return {
        "verdict": "SATISFIED",
        "reason": "closure_basis_present",
        "fields": [],
    }
