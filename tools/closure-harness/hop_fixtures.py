"""hop_fixtures.py — Routed-hop integration fixtures (STCM §15-16).

Proves the full hop: a transition rerouted by a source node is picked up and
closed by the recognized owner, plus every way the hop can fail to complete.
"""

from __future__ import annotations
import copy


def _routable_transition(hash_for_dest="h_dest", tier="medium", level=3):
    """A transition whose object hash is owned by the DESTINATION node."""
    return {
        "transition_id": "T-300",
        "transition_type": "bind_and_advance",
        "risk_tier": tier,
        "hashes": {"object": hash_for_dest},
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
        "proposed_receipt_id": "R-300",
    }


# SOURCE recognizes h_dest as DEST's responsibility but does not activate on it.
SOURCE_SCOPE = {"hashes": ["h_src_only"], "routes_to": {"h_dest": "PN-DEST"}}
# DEST activates on h_dest.
DEST_SCOPE = {"hashes": ["h_dest"]}
# A destination that does NOT own h_dest (for broken-route testing).
WRONG_DEST_SCOPE = {"hashes": ["h_other"]}


def hop_fixtures() -> list[dict]:
    fx: list[dict] = []

    # Happy path: source reroutes to DEST, DEST matches and closes.
    fx.append(dict(
        name="hop_success", stage="hop:success",
        transition=_routable_transition(),
        source_id="PN-SRC", source_scope=SOURCE_SCOPE,
        dest_id="PN-DEST", dest_scope=DEST_SCOPE,
        expect_routed=True, expect_matched=True, expect_closed=True))

    # Broken route: source names PN-DEST, but the dest scope doesn't own the hash.
    fx.append(dict(
        name="hop_broken_route", stage="hop:broken",
        transition=_routable_transition(),
        source_id="PN-SRC", source_scope=SOURCE_SCOPE,
        dest_id="PN-DEST", dest_scope=WRONG_DEST_SCOPE,
        expect_routed=True, expect_matched=False, expect_closed=False,
        expect_reason="ROUTE_BROKEN"))

    # Target mismatch: caller expected a different dest than the source named.
    fx.append(dict(
        name="hop_target_mismatch", stage="hop:mismatch",
        transition=_routable_transition(),
        source_id="PN-SRC", source_scope=SOURCE_SCOPE,
        dest_id="PN-OTHER", dest_scope=DEST_SCOPE,
        expect_routed=True, expect_matched=False, expect_closed=False,
        expect_reason="ROUTE_TARGET_MISMATCH"))

    # Source doesn't reroute at all (it matches the hash itself).
    self_owned = _routable_transition(hash_for_dest="h_src_only")
    fx.append(dict(
        name="hop_source_no_reroute", stage="hop:no_reroute",
        transition=self_owned,
        source_id="PN-SRC", source_scope=SOURCE_SCOPE,
        dest_id="PN-DEST", dest_scope=DEST_SCOPE,
        expect_routed=False, expect_matched=False, expect_closed=False))

    # Routed hop where DEST receives but the transition can't close (low level,
    # destructive override). Routing succeeded; closure correctly refused.
    dele = copy.deepcopy(_routable_transition(tier="low", level=1))
    dele["transition_type"] = "delete_file"
    fx.append(dict(
        name="hop_routed_then_blocked", stage="hop:routed_blocked",
        transition=dele,
        source_id="PN-SRC", source_scope=SOURCE_SCOPE,
        dest_id="PN-DEST", dest_scope=DEST_SCOPE,
        expect_routed=True, expect_matched=True, expect_closed=False))

    return fx
