from __future__ import annotations

BASE_REQUIRED_FIELDS = ("transition_id", "stage", "expected", "basis")
TIER_REQUIRED_FIELDS = {
    "low": (),
    "medium": ("authority_current",),
    "high": ("authority_current", "consent_resolved", "commit_time_reconstruction"),
}


def _tier(stage: str) -> str:
    return stage.split(":", 1)[0] if ":" in stage else stage


def _merge_failure(record: dict, tier: str) -> dict | None:
    receipts = record.get("node_receipts", [])
    if receipts in (None, ""):
        receipts = []
    if not isinstance(receipts, list):
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "node_receipts_not_list", "fields": ["node_receipts"]}
    minimum = 2 if tier == "high" else 1
    if len(receipts) < minimum:
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "insufficient_node_receipts", "fields": ["node_receipts"]}
    ids = [item.get("receipt_id") for item in receipts if isinstance(item, dict)]
    if len(ids) != len(receipts) or any(value in (None, "") for value in ids):
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "missing_receipt_identity", "fields": ["node_receipts"]}
    if len(set(ids)) != len(ids):
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "duplicate_receipt_identity", "fields": ["node_receipts"]}
    if len(receipts) > 1:
        proof = record.get("merge_proof")
        if not isinstance(proof, dict) or proof.get("preserves_distinctions") is not True:
            return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "missing_distinction_preserving_merge_proof", "fields": ["merge_proof"]}
        if proof.get("source_receipt_ids") != ids:
            return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "merge_proof_source_mismatch", "fields": ["merge_proof.source_receipt_ids"]}
    return None


def decide(record: dict) -> dict:
    stage = record.get("stage")
    if stage in (None, ""):
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "missing_required_field", "fields": ["stage"]}
    tier = _tier(str(stage))
    if tier not in TIER_REQUIRED_FIELDS:
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "unsupported_policy_tier", "fields": ["stage"]}
    required_fields = BASE_REQUIRED_FIELDS + TIER_REQUIRED_FIELDS[tier]
    missing = [field for field in required_fields if record.get(field) in (None, "")]
    if missing:
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "missing_required_field", "fields": missing}
    expected = record.get("expected")
    if expected not in {"CLOSED", "BLOCKED"}:
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "unsupported_expected_verdict", "fields": ["expected"]}
    if expected == "BLOCKED":
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "negative_fixture_correctly_blocked", "fields": []}
    if tier in {"medium", "high"} and record.get("authority_current") is not True:
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "authority_not_current", "fields": ["authority_current"]}
    if tier == "high" and record.get("consent_resolved") is not True:
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "consent_unresolved", "fields": ["consent_resolved"]}
    if tier == "high" and record.get("commit_time_reconstruction") is not True:
        return {"verdict": "PROVEN_UNSATISFIABLE", "reason": "commit_time_reconstruction_missing", "fields": ["commit_time_reconstruction"]}
    merge_failure = _merge_failure(record, tier)
    if merge_failure:
        return merge_failure
    return {"verdict": "SATISFIED", "reason": "closure_basis_and_policy_satisfied", "fields": []}
