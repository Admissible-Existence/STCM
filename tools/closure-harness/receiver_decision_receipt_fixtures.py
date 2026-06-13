from __future__ import annotations


def valid_receipt(**overrides):
    receipt = {
        "receipt_id": "rdr-001",
        "source_repo": "source/repo",
        "source_receipt_id": "src-001",
        "source_boundary": "stcm_v0_6",
        "receiving_repo": "receiver/repo",
        "receiving_boundary": "stcm_v0_7",
        "receiver_declared": True,
        "portable_status": "portable",
        "conflict_blocking": False,
        "receiver_decision": "adopt",
        "outcome": "ADOPTED",
        "adopted": True,
        "reason": "Receiver adopted the portable receipt.",
        "timestamp": "2026-01-01T00:00:00Z",
    }
    receipt.update(overrides)
    return receipt


def build_receipt_fixtures():
    yield {
        "name": "valid_adopted_receipt",
        "receipt": valid_receipt(),
        "expect_valid": True,
    }
    yield {
        "name": "missing_required_field",
        "receipt": {k: v for k, v in valid_receipt().items() if k != "receipt_id"},
        "expect_valid": False,
    }
    yield {
        "name": "wrong_boundary",
        "receipt": valid_receipt(receiving_boundary="stcm_v0_6"),
        "expect_valid": False,
    }
    yield {
        "name": "outcome_mismatch",
        "receipt": valid_receipt(outcome="REJECTED"),
        "expect_valid": False,
    }
    yield {
        "name": "adopted_mismatch",
        "receipt": valid_receipt(adopted=False),
        "expect_valid": False,
    }
    yield {
        "name": "valid_rebound_receipt",
        "receipt": valid_receipt(
            portable_status="reboundable",
            receiver_decision="rebind",
            outcome="REBOUND",
            adopted=False,
            reason="Receiver requires local authority rebound.",
        ),
        "expect_valid": True,
    }
    yield {
        "name": "valid_quarantine_receipt",
        "receipt": valid_receipt(
            receiver_decision="quarantine",
            outcome="QUARANTINED",
            adopted=False,
            reason="Receiver quarantined the portable receipt for review.",
        ),
        "expect_valid": True,
    }
    yield {
        "name": "valid_rejected_receipt",
        "receipt": valid_receipt(
            receiver_decision="reject",
            outcome="REJECTED",
            adopted=False,
            reason="Receiver rejected the portable receipt.",
        ),
        "expect_valid": True,
    }
