"""closure.py — Conservation-record closure predicate (STCM §25).

Closure is a DECIDABLE function over a transition conservation record, not an
observed CI result. It returns one of three verdicts with a reason code and the
specific failing field:

    CLOSED      - all required conditions satisfied; may become next receipt basis
    INCOMPLETE  - a required field is null/missing; transition cannot close
    REFUSED     - a required field is present but invalid/stale/unauthorized

DEAD-BASIS GUARD (STCM dead-basis doctrine): this function NEVER returns CLOSED
when a required field is null. A green result must trace to an actual satisfied
condition. Advisory fields (entropy) are recorded but never gate closure until
numerically defined (Open Question #6).
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Verdict(str, Enum):
    CLOSED = "CLOSED"
    INCOMPLETE = "INCOMPLETE"
    REFUSED = "REFUSED"


@dataclass(frozen=True)
class ClosureResult:
    verdict: Verdict
    reason_code: str
    failing_field: str | None = None
    risk_tier: str | None = None
    completeness_level: int | None = None

    @property
    def closed(self) -> bool:
        return self.verdict is Verdict.CLOSED


def _get(record: dict, dotted: str) -> Any:
    """Read a dotted path from a nested dict. Returns _MISSING if absent."""
    cur: Any = record
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return _MISSING
        cur = cur[part]
    return cur


_MISSING = object()


def resolve_risk_tier(record: dict, policy: dict) -> str:
    """Declared tier, overridden to irreversible for forced transition types."""
    ttype = _get(record, "transition_type")
    forced = policy.get("forced_irreversible_transition_types", [])
    if ttype in forced:
        return "irreversible"
    declared = _get(record, "risk_tier")
    if declared is _MISSING or declared not in policy["risk_tiers"]:
        # Unknown tier is treated as irreversible (fail-closed bias).
        return "irreversible"
    return declared


def evaluate_closure(record: dict, policy: dict) -> ClosureResult:
    """Decide closure for one conservation record against the policy table."""
    tier = resolve_risk_tier(record, policy)
    tier_spec = policy["risk_tiers"][tier]
    min_level = tier_spec["min_completeness_level"]

    # 1) Completeness level gate (STCM §3).
    level = _get(record, "incoming_receipts.completeness_level")
    if level is _MISSING or level is None:
        return ClosureResult(Verdict.INCOMPLETE, "RECEIPT_LEVEL_NULL",
                             "incoming_receipts.completeness_level", tier, None)
    if not isinstance(level, int):
        return ClosureResult(Verdict.REFUSED, "RECEIPT_LEVEL_MALFORMED",
                             "incoming_receipts.completeness_level", tier, None)
    if level < min_level:
        return ClosureResult(Verdict.INCOMPLETE, "RECEIPT_LEVEL_BELOW_TIER",
                             "incoming_receipts.completeness_level", tier, level)

    # 2) Mandatory-field presence gate (dead-basis guard: null required -> never CLOSED).
    satisfied_map = policy.get("satisfied_status_values", {})
    for field in tier_spec["required_fields"]:
        val = _get(record, field)
        if val is _MISSING or val is None:
            return ClosureResult(Verdict.INCOMPLETE, "REQUIRED_FIELD_NULL",
                                 field, tier, level)
        # Boolean required fields must be explicitly True.
        if isinstance(val, bool) and val is False:
            return ClosureResult(Verdict.REFUSED, "REQUIRED_FLAG_FALSE",
                                 field, tier, level)
        # Status fields must hold a satisfied value.
        if field in satisfied_map and val not in satisfied_map[field]:
            return ClosureResult(Verdict.REFUSED, "STATUS_NOT_SATISFIED",
                                 field, tier, level)

    # 3) Result decision must affirm coherence.
    decision = _get(record, "result.decision")
    if decision is _MISSING or decision is None:
        return ClosureResult(Verdict.INCOMPLETE, "RESULT_DECISION_NULL",
                             "result.decision", tier, level)
    if decision != "ALLOW":
        # DENY / FAIL_CLOSED from GCAT/BCAT is a valid governed non-closure.
        return ClosureResult(Verdict.REFUSED, "DECISION_NOT_ALLOW",
                             "result.decision", tier, level)

    return ClosureResult(Verdict.CLOSED, "CONSERVATION_RECORD_CLOSED",
                         None, tier, level)
