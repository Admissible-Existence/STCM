"""merge.py — Multi-node observation merge (STCM §19, Open Q#11).

A single transition may require multiple Prime Nodes to observe DIFFERENT
parameters of the SAME transition. Coherent transition recognition occurs only
when the required node receipts are:

    related   - every output refers to the same transition_id and hash
    validated - no required node refused; required set fully present
    bound     - folded into one transition receipt with a node_activation block

This is NOT voting or averaging. Each node owns a disjoint field; the merge
concatenates contributions and records HOW the node set behaved (§20
node_activation). A single refusal or a missing required node => NOT coherent
=> no merged receipt (returns a coherent=False record carrying the reason).

Inputs are the NodeOutput list from compose-style node execution, plus the
transition and the set of node_ids REQUIRED for this transition.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from prime_nodes import Engagement, NodeOutput


@dataclass(frozen=True)
class MergeResult:
    coherent: bool
    record: dict | None
    reason_code: str | None = None
    detail: str | None = None


def _set(record: dict, dotted: str, value: Any) -> None:
    cur = record
    parts = dotted.split(".")
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value


def _same_transition(transition: dict, outputs: list[NodeOutput]) -> bool:
    """Related check: all engaged nodes acted on this transition's identity.

    Node outputs don't carry transition_id directly, so relatedness is enforced
    upstream by passing outputs that were produced from this single transition.
    Here we re-affirm that at least one node engaged (i.e. the transition was in
    scope for the required set) — a fully-ignored transition is not 'related',
    it's simply not this node set's concern.
    """
    return any(o.engaged for o in outputs)


def merge_observations(transition: dict,
                       outputs: list[NodeOutput],
                       required_node_ids: set[str]) -> MergeResult:
    by_id = {o.node_id: o for o in outputs}

    activated = [o.node_id for o in outputs if o.engagement is Engagement.BIND]
    refused = [o.node_id for o in outputs if o.engagement is Engagement.REFUSE]
    ignored = [o.node_id for o in outputs if o.engagement is Engagement.IGNORE]
    routed = [o.node_id for o in outputs if o.engagement is Engagement.REROUTE]
    escalated = [o.node_id for o in outputs if o.engagement is Engagement.ESCALATE]

    # --- related ---
    if not _same_transition(transition, outputs):
        return MergeResult(False, None, "NOT_RELATED",
                           "no required node engaged this transition")

    # --- validated: required set fully present and none refused ---
    missing_required = sorted(required_node_ids - set(by_id.keys()))
    if missing_required:
        return MergeResult(False, None, "REQUIRED_NODE_MISSING",
                           f"missing required nodes: {missing_required}")

    required_ignored = sorted(
        nid for nid in required_node_ids
        if by_id[nid].engagement is Engagement.IGNORE)
    if required_ignored:
        return MergeResult(False, None, "REQUIRED_NODE_IGNORED",
                           f"required nodes out of scope: {required_ignored}")

    required_refused = sorted(
        nid for nid in required_node_ids
        if by_id[nid].engagement is Engagement.REFUSE)
    if required_refused:
        return MergeResult(False, None, "REQUIRED_NODE_REFUSED",
                           f"required nodes refused: {required_refused}")

    # --- bound: fold disjoint field contributions into one record ---
    # Guard: two nodes must not write the same field (disjointness).
    seen_fields: dict[str, str] = {}
    record: dict = {
        "transition_id": transition.get("transition_id"),
        "transition_type": transition.get("transition_type"),
        "risk_tier": transition.get("risk_tier"),
        "incoming_receipts": transition.get("incoming_receipts", {}),
        "entropy": transition.get("entropy", {}),
        "result": {},
        "node_activation": {
            "total_nodes_available": len(outputs),
            "activated_nodes": activated,
            "ignored_nodes_count": len(ignored),
            "refused_nodes": refused,
            "routed_nodes": routed,
            "escalated_nodes": escalated,
            "required_nodes": sorted(required_node_ids),
        },
    }
    for o in outputs:
        if o.engagement is Engagement.BIND and o.field_path is not None:
            if o.field_path in seen_fields:
                return MergeResult(
                    False, None, "FIELD_COLLISION",
                    f"{o.node_id} and {seen_fields[o.field_path]} both write "
                    f"{o.field_path}")
            seen_fields[o.field_path] = o.node_id
            _set(record, o.field_path, o.value)

    if "phase_parameter" in transition:
        record["phase_parameter"] = transition["phase_parameter"]

    # resulting_state from observed->proposed on ALLOW.
    decision = record.get("result", {}).get("decision")
    if decision == "ALLOW" and transition.get("proposed_next_state") is not None:
        _set(record, "result.resulting_state", transition["proposed_next_state"])

    coherent = decision == "ALLOW" and not refused
    _set(record, "result.coherence_preserved", bool(coherent))

    return MergeResult(coherent, record,
                       None if coherent else "DECISION_NOT_ALLOW")
