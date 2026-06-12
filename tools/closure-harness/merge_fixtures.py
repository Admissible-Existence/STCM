"""merge_fixtures.py — Multi-node merge fixtures (STCM §19, Open Q#11).

Proves coherent transition recognition and every way it can fail to cohere.
Each fixture runs the six nodes over one transition, then merges with a declared
required-node set, asserting the expected coherence outcome.
"""

from __future__ import annotations
import copy

from compose import compose_record   # reuse node execution
from prime_nodes import (
    pn001_observe, pn002_bind_evidence, pn003_bind_authority,
    pn004_validate, pn005_refusal, pn006_receipt,
)

IN_SCOPE = {"hashes": ["h_obj_1"]}
OUT_OF_SCOPE = {"hashes": ["h_none"]}

# The minimum required set for a coherent ALLOW: observation + evidence +
# authority + validation + receipt. PN-005 (refusal) is always run but is only
# "required" in the sense that its absence of refusal is checked via the others.
REQUIRED = {"PN-001", "PN-002", "PN-003", "PN-004", "PN-006"}


def _full_transition(tier="medium", level=3):
    return {
        "transition_id": "T-200",
        "transition_type": "bind_and_advance",
        "risk_tier": tier,
        "hashes": {"object": "h_obj_1"},
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
        "proposed_receipt_id": "R-200",
    }


def _run_nodes(transition, scope, partial_scope_for=None):
    """Run the six nodes and return the output list (same order as compose).

    partial_scope_for: optional {node_id: scope} overrides, so a single required
    node can be placed out of scope to exercise partial-scope merge failures.
    """
    ps = partial_scope_for or {}

    def sc(node_id):
        return ps.get(node_id, scope)

    obs = pn001_observe(transition, sc("PN-001"))
    ev = pn002_bind_evidence(transition, sc("PN-002"))
    au = pn003_bind_authority(transition, sc("PN-003"))
    dec = pn004_validate(transition, sc("PN-004"), ev, au, obs)
    refusal = pn005_refusal(transition, sc("PN-005"), [obs, ev, au, dec])
    rcpt = pn006_receipt(transition, sc("PN-006"), dec)
    return [obs, ev, au, dec, refusal, rcpt]


def merge_fixtures() -> list[dict]:
    fx: list[dict] = []

    # Coherent: all required nodes bound, decision ALLOW.
    t_ok = _full_transition()
    fx.append(dict(name="merge_coherent", stage="merge:coherent",
                   transition=t_ok, scope=IN_SCOPE, required=REQUIRED,
                   expect_coherent=True))

    # Not related: transition entirely out of scope -> all ignore. The merge
    # diagnoses this as NOT_RELATED (per §13 it isn't this node set's concern at
    # all), which is distinct from a partial-scope miss below.
    fx.append(dict(name="merge_not_related", stage="merge:not_related",
                   transition=_full_transition(), scope=OUT_OF_SCOPE,
                   required=REQUIRED, expect_coherent=False,
                   expect_reason="NOT_RELATED"))

    # Partial scope: some nodes engage, but a REQUIRED node is out of scope.
    # PN-006 is given a scope it can't match while the rest match -> the merge
    # detects a required node ignored (genuinely different from NOT_RELATED).
    t_partial = _full_transition()
    fx.append(dict(name="merge_required_ignored", stage="merge:required_ignored",
                   transition=t_partial, scope=IN_SCOPE,
                   required=REQUIRED, expect_coherent=False,
                   expect_reason="REQUIRED_NODE_IGNORED",
                   partial_scope_for={"PN-006": OUT_OF_SCOPE}))

    # Required node refused: bad authority -> PN-003 refuses.
    t_bad_au = copy.deepcopy(_full_transition())
    t_bad_au["authority"]["current"] = False
    fx.append(dict(name="merge_required_refused", stage="merge:required_refused",
                   transition=t_bad_au, scope=IN_SCOPE, required=REQUIRED,
                   expect_coherent=False, expect_reason="REQUIRED_NODE_REFUSED"))

    # Required node missing from the output set entirely.
    t_missing = _full_transition()
    fx.append(dict(name="merge_required_missing", stage="merge:required_missing",
                   transition=t_missing, scope=IN_SCOPE,
                   required=REQUIRED | {"PN-999"},  # a node that never runs
                   expect_coherent=False, expect_reason="REQUIRED_NODE_MISSING"))

    return fx
