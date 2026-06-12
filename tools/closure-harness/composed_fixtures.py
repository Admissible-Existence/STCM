"""composed_fixtures.py — End-to-end: transition -> 6 nodes -> record -> closure.

These prove the WHOLE pipeline: a transition runs through PN-001..006, the record
is composed from node outputs, and closure.py evaluates it. Each fixture asserts
both the composed closure verdict and (where relevant) that an out-of-scope
transition produces NO record at all (strict non-engagement, the re-dispatch fix).
"""

from __future__ import annotations
import copy
from closure import Verdict

IN_SCOPE = {"hashes": ["h_obj_1"]}
OUT_OF_SCOPE = {"hashes": ["h_nothing"]}


def _full_transition(tier="medium", level=3):
    return {
        "transition_id": "T-100",
        "transition_type": "bind_and_advance",
        "risk_tier": tier,
        "hashes": {"object": "h_obj_1", "transition": "h_tx_1"},
        "current_state": "DRAFT",
        "proposed_next_state": "BOUND",
        "transition_rule": {"allows": True},
        "incoming_receipts": {"complete": True, "completeness_level": level},
        "evidence": dict(present=True, current=True, admissible=True,
                         sufficient=True, bound_to_object=True),
        "authority": dict(actor="rige", claimed=True, current=True,
                          scoped_to_action=True, portable=True,
                          hidden_platform_dependency=False),
        "phase_parameter": {"phase_change_type": "none"},
        "entropy": {"surplus_transition_entropy": None},
        "proposed_receipt_id": "R-100",
    }


def composed_fixtures() -> list[dict]:
    fx: list[dict] = []

    fx.append(dict(name="e2e_medium_closes", stage="e2e:medium_close",
                   scope=IN_SCOPE, transition=_full_transition("medium", 3),
                   expect_verdict=Verdict.CLOSED, expect_record=True))

    high = _full_transition("high", 5)
    fx.append(dict(name="e2e_high_closes", stage="e2e:high_close",
                   scope=IN_SCOPE, transition=high,
                   expect_verdict=Verdict.CLOSED, expect_record=True))

    # Out of scope: strict non-engagement -> NO record produced (re-dispatch fix).
    fx.append(dict(name="e2e_out_of_scope_no_record", stage="e2e:ignore",
                   scope=OUT_OF_SCOPE, transition=_full_transition(),
                   expect_verdict=None, expect_record=False))

    # Bad evidence -> PN-002 refuses -> PN-004 FAIL_CLOSED -> closure REFUSED.
    bad_ev = copy.deepcopy(_full_transition("medium", 3))
    bad_ev["evidence"]["bound_to_object"] = False
    # PN-002 refuses -> evidence.status never bound -> closure hits the null-field
    # guard (INCOMPLETE) before the decision gate (REFUSED). Both are governed
    # non-closures; the missing-field guard correctly takes precedence.
    fx.append(dict(name="e2e_unbound_evidence_refused", stage="e2e:evidence_refuse",
                   scope=IN_SCOPE, transition=bad_ev,
                   expect_verdict_in=(Verdict.INCOMPLETE, Verdict.REFUSED),
                   expect_verdict=None, expect_record=True))

    # Destructive without disposition -> PN-006 refuses; also forced irreversible
    # tier in closure -> level too low. Either way: not CLOSED.
    dele = copy.deepcopy(_full_transition("low", 1))
    dele["transition_type"] = "delete_file"
    fx.append(dict(name="e2e_delete_no_disposition_blocked",
                   stage="e2e:delete_blocked",
                   scope=IN_SCOPE, transition=dele,
                   expect_verdict_in=(Verdict.INCOMPLETE, Verdict.REFUSED),
                   expect_record=True))

    # Destructive WITH disposition at full irreversible posture -> CLOSED.
    dele_ok = copy.deepcopy(_full_transition("irreversible", 7))
    dele_ok["transition_type"] = "delete_file"
    dele_ok["proposed_next_state"] = "DISPOSED"
    dele_ok["result"] = {"disposition": "archived->cold, hash recorded"}
    fx.append(dict(name="e2e_delete_with_disposition_closes",
                   stage="e2e:delete_closed",
                   scope=IN_SCOPE, transition=dele_ok,
                   expect_verdict=Verdict.CLOSED, expect_record=True))

    return fx
