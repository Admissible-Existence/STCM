"""node_fixtures.py — Per-node fixtures: each PN tested in isolation.

Each PN is a pure function, so it is testable without the others. Fixtures here
exercise each node's three engagement outcomes (IGNORE / BIND / REFUSE) and its
specific check failures. This is what makes "stages of completeness" provable at
the node level rather than only end-to-end.
"""

from __future__ import annotations
from prime_nodes import (
    Engagement,
    pn001_observe, pn002_bind_evidence, pn003_bind_authority,
    pn004_validate, pn005_refusal, pn006_receipt, NodeOutput,
)

IN = {"hashes": ["h_obj_1"]}          # scope that matches transitions below
OUT = {"hashes": ["h_unrelated"]}     # scope that matches nothing here


def _t(**kw):
    base = {"hashes": {"object": "h_obj_1"}}
    base.update(kw)
    return base


def good_evidence():
    return dict(present=True, current=True, admissible=True,
                sufficient=True, bound_to_object=True)


def good_authority():
    return dict(actor="rige", claimed=True, current=True,
                scoped_to_action=True, portable=True,
                hidden_platform_dependency=False)


def node_fixtures() -> list[dict]:
    fx: list[dict] = []

    # PN-001
    fx.append(dict(name="pn001_ignore_out_of_scope", node="PN-001",
                   call=lambda: pn001_observe(_t(current_state="A"), OUT),
                   expect=Engagement.IGNORE))
    fx.append(dict(name="pn001_bind", node="PN-001",
                   call=lambda: pn001_observe(_t(current_state="A"), IN),
                   expect=Engagement.BIND))
    fx.append(dict(name="pn001_refuse_no_state", node="PN-001",
                   call=lambda: pn001_observe(_t(), IN),
                   expect=Engagement.REFUSE))

    # PN-002
    fx.append(dict(name="pn002_ignore", node="PN-002",
                   call=lambda: pn002_bind_evidence(_t(evidence=good_evidence()), OUT),
                   expect=Engagement.IGNORE))
    fx.append(dict(name="pn002_bind", node="PN-002",
                   call=lambda: pn002_bind_evidence(_t(evidence=good_evidence()), IN),
                   expect=Engagement.BIND))
    fx.append(dict(name="pn002_refuse_insufficient", node="PN-002",
                   call=lambda: pn002_bind_evidence(
                       _t(evidence={**good_evidence(), "sufficient": False}), IN),
                   expect=Engagement.REFUSE))

    # PN-003
    fx.append(dict(name="pn003_ignore", node="PN-003",
                   call=lambda: pn003_bind_authority(_t(authority=good_authority()), OUT),
                   expect=Engagement.IGNORE))
    fx.append(dict(name="pn003_bind", node="PN-003",
                   call=lambda: pn003_bind_authority(_t(authority=good_authority()), IN),
                   expect=Engagement.BIND))
    fx.append(dict(name="pn003_refuse_hidden_platform", node="PN-003",
                   call=lambda: pn003_bind_authority(
                       _t(authority={**good_authority(),
                                     "hidden_platform_dependency": True}), IN),
                   expect=Engagement.REFUSE))

    # PN-004 (needs upstream outputs)
    obs_ok = pn001_observe(_t(current_state="A"), IN)
    ev_ok = pn002_bind_evidence(_t(evidence=good_evidence()), IN)
    au_ok = pn003_bind_authority(_t(authority=good_authority()), IN)
    au_bad = pn003_bind_authority(
        _t(authority={**good_authority(), "current": False}), IN)

    fx.append(dict(name="pn004_allow", node="PN-004",
                   call=lambda: pn004_validate(
                       _t(transition_rule={"allows": True}, proposed_next_state="B"),
                       IN, ev_ok, au_ok, obs_ok),
                   expect=Engagement.BIND))
    fx.append(dict(name="pn004_failclosed_on_upstream_refusal", node="PN-004",
                   call=lambda: pn004_validate(
                       _t(transition_rule={"allows": True}, proposed_next_state="B"),
                       IN, ev_ok, au_bad, obs_ok),
                   expect=Engagement.REFUSE))
    fx.append(dict(name="pn004_deny_rule", node="PN-004",
                   call=lambda: pn004_validate(
                       _t(transition_rule={"allows": False}, proposed_next_state="B"),
                       IN, ev_ok, au_ok, obs_ok),
                   expect=Engagement.REFUSE))

    # PN-005
    refused = NodeOutput("PN-002", Engagement.REFUSE,
                         reason_code="EVIDENCE_NOT_BOUND")
    fx.append(dict(name="pn005_binds_no_refusal", node="PN-005",
                   call=lambda: pn005_refusal(_t(), IN, [ev_ok, au_ok]),
                   expect=Engagement.BIND))  # value None
    fx.append(dict(name="pn005_binds_refusal_record", node="PN-005",
                   call=lambda: pn005_refusal(_t(), IN, [refused]),
                   expect=Engagement.BIND))  # value has refused=True

    # PN-006
    allow_dec = NodeOutput("PN-004", Engagement.BIND,
                           field_path="result.decision", value="ALLOW")
    fx.append(dict(name="pn006_bind_receipt", node="PN-006",
                   call=lambda: pn006_receipt(
                       _t(proposed_receipt_id="R-1"), IN, allow_dec),
                   expect=Engagement.BIND))
    fx.append(dict(name="pn006_refuse_destructive_no_disposition", node="PN-006",
                   call=lambda: pn006_receipt(
                       _t(transition_type="delete_file",
                          proposed_receipt_id="R-1"), IN, allow_dec),
                   expect=Engagement.REFUSE))
    fx.append(dict(name="pn006_destructive_with_disposition", node="PN-006",
                   call=lambda: pn006_receipt(
                       _t(transition_type="delete_file",
                          proposed_receipt_id="R-1",
                          result={"disposition": "archived->cold, hash recorded"}),
                       IN, allow_dec),
                   expect=Engagement.BIND))

    return fx
