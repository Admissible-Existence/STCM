"""prime_nodes.py — The six Transition Prime Nodes as pure functions (STCM §5).

Each node is a pure function: (transition, scope) -> NodeOutput. A node contributes
exactly ONE field to the conservation record. Nodes do not mutate shared state and
do not call each other except PN-004, which reads the upstream node outputs to
validate (STCM §942 — PN-004 validates evidence_status + authority_status).

Two STCM principles are enforced structurally:

  Hash-scope non-engagement (§12/§13): a node evaluates a transition ONLY if the
  transition's hashes match the node's declared scope. Non-matching transitions
  return engaged=False (IGNORE) — no receipt, no refusal, no compute beyond a
  cheap hash compare. This is the structural fix for the re-dispatch loop:
  out-of-scope / stale-manifest transitions produce nothing.

  Refusal is a governed state (§5 PN-005 / §11): a node that IS matched but cannot
  proceed returns a REFUSED contribution with a reason — not an exception.

A node returns one of three engagement outcomes:
  IGNORE  - out of hash scope; contributes nothing
  BIND    - matched and satisfied; contributes its field value
  REFUSE  - matched but cannot proceed; contributes a refusal reason
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Engagement(str, Enum):
    IGNORE = "IGNORE"
    BIND = "BIND"
    REFUSE = "REFUSE"


@dataclass(frozen=True)
class NodeOutput:
    node_id: str
    engagement: Engagement
    field_path: str | None = None      # the single record field this node fills
    value: Any = None                  # value written when engagement == BIND
    reason_code: str | None = None     # set when engagement == REFUSE
    detail: str | None = None

    @property
    def engaged(self) -> bool:
        return self.engagement is not Engagement.IGNORE


def _in_scope(transition: dict, scope: dict) -> bool:
    """Strict hash-match non-engagement (STCM §13).

    The node's scope declares hash families it may evaluate. A transition is in
    scope iff at least one of its declared hashes is listed in the node's scope.
    Cheap comparison before expensive interpretation (§12).
    """
    t_hashes = set(transition.get("hashes", {}).values())
    scope_hashes = set(scope.get("hashes", []))
    if not scope_hashes:           # empty scope = node engages nothing
        return False
    return bool(t_hashes & scope_hashes)


# --------------------------------------------------------------------------- #
# PN-001 — State Observation Node (§169)
# Observes/classifies current state. Does NOT decide validity.
# Contributes: result.resulting_state is seeded from observed -> proposed later;
# here it fills observed current_state.
# --------------------------------------------------------------------------- #
def pn001_observe(transition: dict, scope: dict) -> NodeOutput:
    if not _in_scope(transition, scope):
        return NodeOutput("PN-001", Engagement.IGNORE)
    current = transition.get("current_state")
    if current is None:
        return NodeOutput("PN-001", Engagement.REFUSE,
                          reason_code="STATE_UNOBSERVABLE",
                          detail="no current_state on transition")
    return NodeOutput("PN-001", Engagement.BIND,
                      field_path="observation.current_state", value=current)


# --------------------------------------------------------------------------- #
# PN-002 — Evidence Binding Node (§181)
# Evidence present, current, admissible, sufficient, bound to object.
# Contributes: evidence.status
# --------------------------------------------------------------------------- #
def pn002_bind_evidence(transition: dict, scope: dict) -> NodeOutput:
    if not _in_scope(transition, scope):
        return NodeOutput("PN-002", Engagement.IGNORE)
    ev = transition.get("evidence") or {}
    checks = {
        "present": bool(ev.get("present")),
        "current": bool(ev.get("current")),
        "admissible": bool(ev.get("admissible")),
        "sufficient": bool(ev.get("sufficient")),
        "bound_to_object": bool(ev.get("bound_to_object")),
    }
    missing = [k for k, ok in checks.items() if not ok]
    if missing:
        return NodeOutput("PN-002", Engagement.REFUSE,
                          field_path="evidence.status",
                          reason_code="EVIDENCE_NOT_BOUND",
                          detail=f"failed: {missing}")
    return NodeOutput("PN-002", Engagement.BIND,
                      field_path="evidence.status", value="bound")


# --------------------------------------------------------------------------- #
# PN-003 — Authority Binding Node (§195)
# Authority present, current, scoped, portable, no hidden platform dependency.
# Contributes: authority.status
# --------------------------------------------------------------------------- #
def pn003_bind_authority(transition: dict, scope: dict) -> NodeOutput:
    if not _in_scope(transition, scope):
        return NodeOutput("PN-003", Engagement.IGNORE)
    au = transition.get("authority") or {}
    checks = {
        "actor_identified": bool(au.get("actor")),
        "authority_claimed": bool(au.get("claimed")),
        "current": bool(au.get("current")),
        "scoped_to_action": bool(au.get("scoped_to_action")),
        "portable": bool(au.get("portable")),
        "no_hidden_platform_dependency": not bool(au.get("hidden_platform_dependency")),
    }
    missing = [k for k, ok in checks.items() if not ok]
    if missing:
        return NodeOutput("PN-003", Engagement.REFUSE,
                          field_path="authority.status",
                          reason_code="AUTHORITY_NOT_BOUND",
                          detail=f"failed: {missing}")
    return NodeOutput("PN-003", Engagement.BIND,
                      field_path="authority.status", value="bound")


# --------------------------------------------------------------------------- #
# PN-004 — Transition Validation Node (§210)
# Reads upstream node outputs + transition rule; emits ALLOW/DENY/FAIL_CLOSED.
# This is the only node that reads other nodes' outputs (§942).
# Contributes: result.decision
# --------------------------------------------------------------------------- #
def pn004_validate(transition: dict, scope: dict,
                   ev_out: NodeOutput, au_out: NodeOutput,
                   obs_out: NodeOutput) -> NodeOutput:
    if not _in_scope(transition, scope):
        return NodeOutput("PN-004", Engagement.IGNORE)

    # If any required upstream node refused, validation fails closed.
    upstream = {"PN-001": obs_out, "PN-002": ev_out, "PN-003": au_out}
    refused = [nid for nid, o in upstream.items()
               if o.engagement is Engagement.REFUSE]
    if refused:
        return NodeOutput("PN-004", Engagement.REFUSE,
                          field_path="result.decision",
                          reason_code="UPSTREAM_REFUSAL",
                          detail=f"refused by {refused}", value="FAIL_CLOSED")

    # Upstream must have BOUND (not merely ignored) for a governed ALLOW.
    not_bound = [nid for nid, o in upstream.items()
                 if o.engagement is not Engagement.BIND]
    if not_bound:
        return NodeOutput("PN-004", Engagement.REFUSE,
                          field_path="result.decision",
                          reason_code="UPSTREAM_NOT_BOUND",
                          detail=f"not bound: {not_bound}", value="FAIL_CLOSED")

    rule = transition.get("transition_rule")
    proposed = transition.get("proposed_next_state")
    if rule is None or proposed is None:
        return NodeOutput("PN-004", Engagement.REFUSE,
                          field_path="result.decision",
                          reason_code="NO_TRANSITION_RULE",
                          detail="missing rule or proposed_next_state",
                          value="DENY")
    if rule.get("allows") is not True:
        return NodeOutput("PN-004", Engagement.REFUSE,
                          field_path="result.decision",
                          reason_code="RULE_DENIES",
                          detail="transition_rule.allows != True", value="DENY")

    return NodeOutput("PN-004", Engagement.BIND,
                      field_path="result.decision", value="ALLOW")


# --------------------------------------------------------------------------- #
# PN-005 — Refusal / Block Node (§227)
# Refusal is a governed state, not a failure. Aggregates any refusal into a
# governed refusal record. Contributes: result.refusal (None when nothing refused).
# --------------------------------------------------------------------------- #
def pn005_refusal(transition: dict, scope: dict,
                  node_outputs: list[NodeOutput]) -> NodeOutput:
    if not _in_scope(transition, scope):
        return NodeOutput("PN-005", Engagement.IGNORE)
    refusals = [
        {"node_id": o.node_id, "reason_code": o.reason_code, "detail": o.detail}
        for o in node_outputs if o.engagement is Engagement.REFUSE
    ]
    if not refusals:
        # Nothing to refuse: PN-005 binds an explicit "no refusal" governed state.
        return NodeOutput("PN-005", Engagement.BIND,
                          field_path="result.refusal", value=None)
    return NodeOutput("PN-005", Engagement.BIND,
                      field_path="result.refusal",
                      value={"refused": True, "by": refusals})


# --------------------------------------------------------------------------- #
# PN-006 — Receipt / Continuity Node (§235)
# Records result, preserves continuity, prepares DC/MR receipt. Forces a
# disposition record for destructive transitions (receipt-chain integrity).
# Contributes: result.receipt_id + result.coherence_preserved + completeness.
# --------------------------------------------------------------------------- #
DESTRUCTIVE = {"delete_file", "dispose_object", "retire_node",
               "dissolve_node", "cleanup_commit"}


def pn006_receipt(transition: dict, scope: dict,
                  decision_out: NodeOutput) -> NodeOutput:
    if not _in_scope(transition, scope):
        return NodeOutput("PN-006", Engagement.IGNORE)

    ttype = transition.get("transition_type")
    decision = decision_out.value

    # A destructive transition with no disposition record breaks the chain.
    if ttype in DESTRUCTIVE:
        disp = (transition.get("result") or {}).get("disposition")
        if not disp:
            return NodeOutput("PN-006", Engagement.REFUSE,
                              field_path="result.receipt_id",
                              reason_code="NO_DISPOSITION_RECORD",
                              detail="destructive transition without disposition")

    if decision != "ALLOW":
        # Still receipt a governed non-allow, but mark it as a refusal receipt.
        return NodeOutput("PN-006", Engagement.BIND,
                          field_path="result.receipt_id",
                          value=transition.get("proposed_receipt_id"),
                          detail="refusal-receipt (decision != ALLOW)")

    rid = transition.get("proposed_receipt_id")
    if not rid:
        return NodeOutput("PN-006", Engagement.REFUSE,
                          field_path="result.receipt_id",
                          reason_code="NO_RECEIPT_ID",
                          detail="cannot continue chain without receipt id")
    return NodeOutput("PN-006", Engagement.BIND,
                      field_path="result.receipt_id", value=rid)
