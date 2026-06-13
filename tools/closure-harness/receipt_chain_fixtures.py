from __future__ import annotations


def base_chain(**overrides):
    chain = {
        "chain_id": "chain-001",
        "source_repo": "source/repo",
        "source_receipt_id": "src-001",
        "source_boundary": "stcm_v0_6",
        "receiver_decision_receipt_id": "rdr-001",
        "receiving_repo": "receiver/repo",
        "receiving_boundary": "stcm_v0_7",
        "next_receipt_id": "next-001",
        "next_receipt_boundary": "stcm_v0_8",
        "chain_outcome": "CHAIN_ACCEPTED",
        "chain_continuous": True,
        "reason": "Chain accepted.",
        "timestamp": "2026-01-01T00:00:00Z",
    }
    chain.update(overrides)
    return chain


def build_chain_fixtures():
    yield {"name": "valid_accepted_chain", "receiver_outcome": "ADOPTED", "chain": base_chain(), "expect_valid": True}
    yield {"name": "valid_rebound_chain", "receiver_outcome": "REBOUND", "chain": base_chain(chain_outcome="CHAIN_REBOUND_REQUIRED"), "expect_valid": True}
    yield {"name": "valid_quarantined_chain", "receiver_outcome": "QUARANTINED", "chain": base_chain(chain_outcome="CHAIN_QUARANTINED"), "expect_valid": True}
    yield {"name": "valid_rejected_chain", "receiver_outcome": "REJECTED", "chain": base_chain(chain_outcome="CHAIN_REJECTED"), "expect_valid": True}
    yield {"name": "missing_source_receipt", "receiver_outcome": "ADOPTED", "chain": base_chain(source_receipt_id=""), "expect_valid": False}
    yield {"name": "missing_receiver_decision_receipt", "receiver_outcome": "ADOPTED", "chain": base_chain(receiver_decision_receipt_id=""), "expect_valid": False}
    yield {"name": "missing_next_receipt", "receiver_outcome": "ADOPTED", "chain": base_chain(next_receipt_id=""), "expect_valid": False}
    yield {"name": "outcome_mismatch", "receiver_outcome": "ADOPTED", "chain": base_chain(chain_outcome="CHAIN_REJECTED"), "expect_valid": False}
    yield {"name": "chain_not_continuous", "receiver_outcome": "ADOPTED", "chain": base_chain(chain_continuous=False), "expect_valid": False}
