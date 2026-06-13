"""store_fixtures.py — Receipt store + conflict policy fixtures (STCM v0.5).

Each fixture builds a real ReceiptStore state, then runs the full v0.5 pipeline
(store -> lineage -> conflict -> closure -> update) against it. Proves the eight
required v0.5 cases plus the store's append-only/history-preserving guarantee.
"""

from __future__ import annotations

from receipt_store import ReceiptStore, Receipt, Conflict, ConflictStatus


CHAIN = "chain-A"


def _r(id, seq, prev=None, prev_hash=None, closed=True, superseded_by=None,
       resolution_status=None):
    return Receipt(
        id=id, hash=f"hash-{id}", chain_id=CHAIN, sequence_index=seq,
        previous_receipt_id=prev, previous_receipt_hash=prev_hash,
        state="BOUND", closed=closed, closed_at="2026-06-01T00:00:00Z",
        superseded_by=superseded_by, resolution_status=resolution_status)


def _closable_record(level=3, tier="medium", rid="R-NEW", state="BOUND"):
    return {
        "transition_id": "T-NEW",
        "transition_type": "bind_and_advance",
        "risk_tier": tier,
        "incoming_receipts": {"complete": True, "completeness_level": level},
        "evidence": {"status": "bound"},
        "authority": {"status": "bound"},
        "phase_parameter": {"phase_change_type": "none"},
        "entropy": {"surplus_transition_entropy": None},
        "result": {"decision": "ALLOW", "resulting_state": state,
                   "receipt_id": rid, "coherence_preserved": True},
    }


def _transition(claimed_id, claimed_hash, seq):
    return {
        "transition_id": "T-NEW",
        "claimed_prior_receipt_id": claimed_id,
        "claimed_prior_receipt_hash": claimed_hash,
        "sequence_index": seq,
        "is_genesis": False,
        "result_receipt_id": "R-NEW",
    }


def _linear_store():
    """R1 -> R2 -> R3, R3 is head."""
    s = ReceiptStore()
    s.put(_r("R1", 1))
    s.put(_r("R2", 2, prev="R1", prev_hash="hash-R1"))
    s.put(_r("R3", 3, prev="R2", prev_hash="hash-R2"))
    return s


def store_fixtures() -> list[dict]:
    fx: list[dict] = []

    # 1. Store returns current head (R3) and a valid successor closes.
    s1 = _linear_store()
    fx.append(dict(
        name="store_head_found", stage="store:head_found",
        store=s1, chain_id=CHAIN,
        transition=_transition("R3", "hash-R3", 4),
        record=_closable_record(rid="R4"),
        expect_head="R3", expect_lineage="BOUND", expect_closed=True))

    # 2. Store detects stale prior (claims R2 while head is R3).
    s2 = _linear_store()
    fx.append(dict(
        name="store_stale", stage="store:stale",
        store=s2, chain_id=CHAIN,
        transition=_transition("R2", "hash-R2", 3),
        record=_closable_record(rid="R3b"),
        expect_head="R3", expect_lineage="STALE", expect_closed=False))

    # 3. Store detects competing successors -> OPEN conflict -> CONFLICT.
    s3 = _linear_store()
    # Two successors already claim R3 at seq 4.
    s3.put(_r("R4a", 4, prev="R3", prev_hash="hash-R3"))
    s3.put(_r("R4b", 4, prev="R3", prev_hash="hash-R3"))
    s3.register_conflict(Conflict("C1", "R3", 4, ["R4a", "R4b"],
                                  status=ConflictStatus.OPEN))
    fx.append(dict(
        name="store_competing", stage="store:competing",
        store=s3, chain_id=CHAIN,
        transition=_transition("R3", "hash-R3", 4),
        record=_closable_record(rid="R4c"),
        expect_head="R3", expect_conflict="OPEN", expect_closed=False))

    # 4. Conflict resolved by accepting one successor.
    s4 = _linear_store()
    s4.put(_r("R4a", 4, prev="R3", prev_hash="hash-R3"))
    s4.put(_r("R4b", 4, prev="R3", prev_hash="hash-R3"))
    s4.register_conflict(Conflict("C1", "R3", 4, ["R4a", "R4b"]))
    s4.resolve_conflict("C1", ConflictStatus.RESOLVED_ACCEPT_ONE,
                        accepted_receipt_id="R4a")
    fx.append(dict(
        name="store_conflict_resolved", stage="store:resolved",
        store=s4, chain_id=CHAIN,
        check_resolution=("R4a", "R4b"),  # accepted, rejected
        transition=_transition("R4a", "hash-R4a", 5),
        record=_closable_record(rid="R5"),
        expect_lineage="BOUND", expect_closed=True))

    # 5. Supersession without deletion.
    s5 = _linear_store()
    s5.put(_r("R3prime", 3, prev="R2", prev_hash="hash-R2"))
    s5.supersede("R3", "R3prime")  # R3 superseded by R3prime
    fx.append(dict(
        name="store_supersede", stage="store:supersede",
        store=s5, chain_id=CHAIN,
        check_supersede="R3",  # must remain valid_as_closed, not current
        transition=_transition("R3prime", "hash-R3prime", 4),
        record=_closable_record(rid="R4"),
        expect_lineage="BOUND", expect_closed=True))

    # 6. Rejected receipt cannot serve as prior.
    s6 = _linear_store()
    s6.put(_r("R4a", 4, prev="R3", prev_hash="hash-R3"))
    s6.put(_r("R4b", 4, prev="R3", prev_hash="hash-R3"))
    s6.register_conflict(Conflict("C1", "R3", 4, ["R4a", "R4b"]))
    s6.resolve_conflict("C1", ConflictStatus.RESOLVED_SUPERSEDE_ALL_BUT_ONE,
                        accepted_receipt_id="R4a")
    # Transition tries to build on the REJECTED R4b.
    fx.append(dict(
        name="store_rejected_prior", stage="store:rejected_prior",
        store=s6, chain_id=CHAIN,
        transition=_transition("R4b", "hash-R4b", 5),
        record=_closable_record(rid="R5"),
        expect_closed=False))  # STALE or CONFLICT

    # 7. Missing store receipt blocks continuation.
    s7 = _linear_store()
    fx.append(dict(
        name="store_missing", stage="store:missing",
        store=s7, chain_id=CHAIN,
        transition=_transition("R-NONEXISTENT", "hash-X", 4),
        record=_closable_record(rid="R4"),
        expect_lineage="MISSING_PRIOR", expect_closed=False))

    # 8. Audit history preserved after supersession + resolution.
    s8 = _linear_store()
    s8.put(_r("R3prime", 3, prev="R2", prev_hash="hash-R2"))
    s8.supersede("R3", "R3prime")
    fx.append(dict(
        name="store_history_preserved", stage="store:history",
        store=s8, chain_id=CHAIN,
        check_history=["R1", "R2", "R3", "R3prime"],  # all still queryable
        transition=_transition("R3prime", "hash-R3prime", 4),
        record=_closable_record(rid="R4"),
        expect_lineage="BOUND", expect_closed=True))

    return fx
