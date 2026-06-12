"""lineage_fixtures.py — Sequential receipt lineage fixtures (STCM v0.4).

Proves the six required v0.4 cases plus genesis and the
lineage-succeeds-but-closure-still-fails case (lineage permits, does not
guarantee, closure).
"""

from __future__ import annotations
import copy

from lineage import LineageVerdict
from closure import Verdict


def _closable_record(level=3, tier="medium"):
    """A conservation record that WOULD close on its own merits."""
    return {
        "transition_id": "T-400",
        "transition_type": "bind_and_advance",
        "risk_tier": tier,
        "incoming_receipts": {"complete": True, "completeness_level": level},
        "evidence": {"status": "bound"},
        "authority": {"status": "bound"},
        "phase_parameter": {"phase_change_type": "none"},
        "entropy": {"surplus_transition_entropy": None},
        "result": {"decision": "ALLOW", "resulting_state": "BOUND",
                   "receipt_id": "R-400", "coherence_preserved": True},
    }


def _prior(id="R-300", h="hash-300", seq=4, closed=True, superseded_by=None):
    return {"id": id, "hash": h, "sequence_index": seq,
            "closed": closed, "superseded_by": superseded_by,
            "state": "BOUND"}


def _transition(prior=None, claimed_id="R-300", claimed_hash="hash-300",
                seq=5, genesis=False):
    return {
        "claimed_prior_receipt_id": claimed_id,
        "claimed_prior_receipt_hash": claimed_hash,
        "sequence_index": seq,
        "prior_receipt": prior,
        "is_genesis": genesis,
        "result_receipt_id": "R-400",
    }


def lineage_fixtures() -> list[dict]:
    fx: list[dict] = []

    # 1. Prior binds: exact id+hash, closed, current head, contiguous seq.
    fx.append(dict(name="lin_bound", stage="lineage:bound",
                   record=_closable_record(),
                   transition=_transition(prior=_prior()),
                   chain_head=_prior(),
                   expect_lineage=LineageVerdict.BOUND,
                   expect_closed=True))

    # 2. Missing prior: claims continuity, no prior object present.
    fx.append(dict(name="lin_missing", stage="lineage:missing",
                   record=_closable_record(),
                   transition=_transition(prior=None),
                   chain_head=_prior(),
                   expect_lineage=LineageVerdict.MISSING_PRIOR,
                   expect_closed=False))

    # 3. Hash mismatch: right id, wrong hash -> CONFLICT.
    fx.append(dict(name="lin_hash_mismatch", stage="lineage:hash_conflict",
                   record=_closable_record(),
                   transition=_transition(prior=_prior(),
                                          claimed_hash="WRONG-hash"),
                   chain_head=_prior(),
                   expect_lineage=LineageVerdict.CONFLICT,
                   expect_closed=False))

    # 4. Stale: binds to an old receipt that isn't the current head.
    fx.append(dict(name="lin_stale", stage="lineage:stale",
                   record=_closable_record(),
                   transition=_transition(prior=_prior(id="R-200", h="hash-200",
                                                       seq=2),
                                          claimed_id="R-200",
                                          claimed_hash="hash-200", seq=3),
                   chain_head=_prior(id="R-300", h="hash-300", seq=4),
                   expect_lineage=LineageVerdict.STALE,
                   expect_closed=False))

    # 5. Superseded: prior points to a later replacement (history preserved).
    fx.append(dict(name="lin_superseded", stage="lineage:superseded",
                   record=_closable_record(),
                   transition=_transition(prior=_prior(superseded_by="R-350")),
                   chain_head=_prior(superseded_by="R-350"),
                   expect_lineage=LineageVerdict.SUPERSEDED,
                   expect_closed=False))

    # 6. Competing successors: another receipt already claims this prior@seq.
    competitor = {"id": "R-399", "previous_receipt_id": "R-300",
                  "sequence_index": 5}
    fx.append(dict(name="lin_conflict_competing", stage="lineage:competing",
                   record=_closable_record(),
                   transition=_transition(prior=_prior()),
                   chain_head=_prior(),
                   known_successors=[competitor],
                   expect_lineage=LineageVerdict.CONFLICT,
                   expect_closed=False))

    # 7. Genesis: legitimately no prior.
    fx.append(dict(name="lin_genesis", stage="lineage:genesis",
                   record=_closable_record(),
                   transition=_transition(prior=None, claimed_id=None,
                                          claimed_hash=None, genesis=True),
                   chain_head=None,
                   expect_lineage=LineageVerdict.BOUND,
                   expect_closed=True))

    # 8. Malformed prior: present but missing required fields.
    bad_prior = {"id": "R-300", "hash": "hash-300"}  # no seq / closed
    fx.append(dict(name="lin_malformed", stage="lineage:malformed",
                   record=_closable_record(),
                   transition=_transition(prior=bad_prior),
                   chain_head=_prior(),
                   expect_lineage=LineageVerdict.MALFORMED_PRIOR,
                   expect_closed=False))

    # 9. Lineage BOUND but closure still fails (low completeness for tier).
    #    Proves lineage permits but does not guarantee closure.
    weak = _closable_record(level=1, tier="high")  # high tier needs level 5
    fx.append(dict(name="lin_bound_closure_fails",
                   stage="lineage:bound_closure_fails",
                   record=weak,
                   transition=_transition(prior=_prior()),
                   chain_head=_prior(),
                   expect_lineage=LineageVerdict.BOUND,
                   expect_closed=False))

    return fx
