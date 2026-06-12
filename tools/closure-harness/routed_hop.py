"""routed_hop.py — Routed transition integration (STCM §15-16).

Proves routing END TO END, not just at the gate. A transition that REROUTEs from
a source node must be picked up by the recognized owner and either close there or
produce a governed non-closure at the destination.

The hop (§16 "if one node activates, the route is singular"):

    1. source node runs route_gate against SOURCE scope -> REROUTE(route_to=DEST)
    2. DEST node runs route_gate against DEST scope
         - DEST must MATCH (it activates on the rerouted hash), else the route is
           broken: the named owner doesn't actually own it -> ROUTE_BROKEN
    3. DEST runs its node logic; the transition is composed + closed at DEST

A valid route therefore requires: source rerouted, destination activated, and the
destination produced a closable (or explicitly non-closable) record. No silent
hops: a reroute whose destination ignores the transition is a broken route, which
is itself a governed, detectable outcome (not a dropped transition).
"""

from __future__ import annotations
from dataclasses import dataclass

from prime_nodes import route_gate, Engagement, ScopeMatch, classify_scope
from compose import compose_record
from closure import evaluate_closure, Verdict


@dataclass(frozen=True)
class HopResult:
    routed: bool                  # source produced a REROUTE
    route_to: str | None          # named destination
    destination_matched: bool     # destination actually activates on the hash
    closed: bool                  # destination produced a CLOSED record
    verdict: str | None           # closure verdict at destination
    reason_code: str | None = None


def route_and_close(transition: dict,
                    source_id: str, source_scope: dict,
                    dest_id: str, dest_scope: dict,
                    policy: dict,
                    required_node_ids=None) -> HopResult:
    # --- hop step 1: source decides ---
    src = route_gate(source_id, transition, source_scope)
    if src is None or src.engagement is not Engagement.REROUTE:
        got = "MATCH/proceed" if src is None else src.engagement.value
        return HopResult(False, None, False, False, None,
                         reason_code=f"SOURCE_DID_NOT_REROUTE:{got}")

    # --- hop step 2: the named owner must actually activate on this hash ---
    if src.route_to != dest_id:
        return HopResult(True, src.route_to, False, False, None,
                         reason_code="ROUTE_TARGET_MISMATCH")

    dmatch, _ = classify_scope(transition, dest_scope)
    if dmatch is not ScopeMatch.MATCH:
        # The named owner doesn't own it -> broken route (governed, detectable).
        return HopResult(True, dest_id, False, False, None,
                         reason_code="ROUTE_BROKEN")

    # --- hop step 3: destination composes + closes the transition ---
    record, _outputs = compose_record(transition, dest_scope)
    if record is None:
        return HopResult(True, dest_id, True, False, None,
                         reason_code="DEST_PRODUCED_NO_RECORD")
    res = evaluate_closure(record, policy)
    return HopResult(True, dest_id, True,
                     res.verdict is Verdict.CLOSED, res.verdict.value,
                     reason_code=None if res.verdict is Verdict.CLOSED
                     else res.reason_code)
