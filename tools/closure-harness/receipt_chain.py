from __future__ import annotations

REQUIRED_FIELDS = {
    "chain_id",
    "source_repo",
    "source_receipt_id",
    "source_boundary",
    "receiver_decision_receipt_id",
    "receiving_repo",
    "receiving_boundary",
    "next_receipt_id",
    "next_receipt_boundary",
    "chain_outcome",
    "chain_continuous",
    "reason",
    "timestamp",
}

ALLOWED_CHAIN_OUTCOMES = {
    "CHAIN_ACCEPTED",
    "CHAIN_REBOUND_REQUIRED",
    "CHAIN_QUARANTINED",
    "CHAIN_REJECTED",
    "CHAIN_BROKEN",
    "CHAIN_CONFLICT_BLOCKED",
}

EXPECTED_BY_RECEIVER_OUTCOME = {
    "ADOPTED": "CHAIN_ACCEPTED",
    "REBOUND": "CHAIN_REBOUND_REQUIRED",
    "QUARANTINED": "CHAIN_QUARANTINED",
    "REJECTED": "CHAIN_REJECTED",
    "CONFLICT_BLOCKED": "CHAIN_CONFLICT_BLOCKED",
}


def validate_receipt_chain(chain: dict, receiver_outcome: str) -> dict:
    missing = sorted(REQUIRED_FIELDS - set(chain.keys()))
    if missing:
        return {"valid": False, "reason": "missing_fields:" + ",".join(missing)}

    if chain["chain_outcome"] not in ALLOWED_CHAIN_OUTCOMES:
        return {"valid": False, "reason": "invalid_chain_outcome"}

    if not chain["source_receipt_id"]:
        return {"valid": False, "reason": "source_receipt_missing"}

    if not chain["receiver_decision_receipt_id"]:
        return {"valid": False, "reason": "receiver_decision_receipt_missing"}

    if not chain["next_receipt_id"]:
        return {"valid": False, "reason": "next_receipt_missing"}

    expected = EXPECTED_BY_RECEIVER_OUTCOME.get(receiver_outcome)
    if expected is None:
        return {"valid": False, "reason": "unsupported_receiver_outcome"}

    if chain["chain_outcome"] != expected:
        return {"valid": False, "reason": "chain_outcome_mismatch"}

    if not bool(chain["chain_continuous"]):
        return {"valid": False, "reason": "chain_not_continuous"}

    return {"valid": True, "reason": "valid_receipt_chain"}
