"""routing_fixtures.py — Routing front-gate fixtures (STCM §14, §15, §16).

Tests route_gate directly across the three scope-match degrees:

  NONE  -> IGNORE   (no hash overlap)
  MATCH -> None     (node proceeds to its own logic)
  TOUCH -> REROUTE  (another node owns it, route equation holds) or
           ESCALATE (route equation fails / no target)

route_possible = hash_match AND receipt_sufficient AND transition_allowed (§16)
"""

from __future__ import annotations
from prime_nodes import route_gate, Engagement


def _t(hashes, complete=True, allows=True):
    return {
        "hashes": {"object": hashes} if isinstance(hashes, str) else
                  {f"h{i}": h for i, h in enumerate(hashes)},
        "incoming_receipts": {"complete": complete},
        "transition_rule": {"allows": allows},
    }


# A node that activates on h_self and recognizes h_other as PN-OTHER's job.
SCOPE = {"hashes": ["h_self"], "routes_to": {"h_other": "PN-OTHER"}}


def routing_fixtures() -> list[dict]:
    fx: list[dict] = []

    # NONE -> IGNORE: hash hits neither activation nor routes_to.
    fx.append(dict(name="route_ignore_none", stage="route:ignore",
                   call=lambda: route_gate("PN-X", _t("h_unrelated"), SCOPE),
                   expect=Engagement.IGNORE))

    # MATCH -> None: caller proceeds to node's own logic.
    fx.append(dict(name="route_match_proceeds", stage="route:match",
                   call=lambda: route_gate("PN-X", _t("h_self"), SCOPE),
                   expect=None))

    # TOUCH + equation holds -> REROUTE to the recognized owner.
    fx.append(dict(name="route_reroute", stage="route:reroute",
                   call=lambda: route_gate("PN-X", _t("h_other"), SCOPE),
                   expect=Engagement.REROUTE, expect_route_to="PN-OTHER"))

    # TOUCH but receipt insufficient -> ESCALATE (equation fails).
    fx.append(dict(name="route_escalate_insufficient_receipt",
                   stage="route:escalate_receipt",
                   call=lambda: route_gate("PN-X", _t("h_other", complete=False),
                                           SCOPE),
                   expect=Engagement.ESCALATE,
                   expect_reason="ROUTE_EQUATION_FAILED"))

    # TOUCH but transition not allowed -> ESCALATE.
    fx.append(dict(name="route_escalate_not_allowed",
                   stage="route:escalate_rule",
                   call=lambda: route_gate("PN-X", _t("h_other", allows=False),
                                           SCOPE),
                   expect=Engagement.ESCALATE,
                   expect_reason="ROUTE_EQUATION_FAILED"))

    # TOUCH but no route target declared -> ESCALATE (no governed path).
    scope_no_target = {"hashes": ["h_self"], "routes_to": {"h_other": None}}
    fx.append(dict(name="route_escalate_no_target",
                   stage="route:escalate_no_target",
                   call=lambda: route_gate("PN-X", _t("h_other"), scope_no_target),
                   expect=Engagement.ESCALATE,
                   expect_reason="NO_ROUTE_TARGET"))

    return fx
