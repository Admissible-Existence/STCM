from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdoptionInput:
    source_receipt_present: bool
    receiver_declared: bool
    portable_status: str
    conflict_blocking: bool
    receiver_decision: str


@dataclass(frozen=True)
class AdoptionDecision:
    outcome: str
    adopted: bool
    reason: str
    boundary: str = "stcm_v0_7"
    boundary_status: str = "draft"


def evaluate_adoption(inp: AdoptionInput) -> AdoptionDecision:
    if not inp.source_receipt_present or not inp.receiver_declared:
        return AdoptionDecision(
            outcome="INSUFFICIENT_DECLARATION",
            adopted=False,
            reason="Source receipt and receiver declaration are required.",
        )

    if inp.portable_status not in {"portable", "reboundable"}:
        return AdoptionDecision(
            outcome="AUTHORITY_MISMATCH",
            adopted=False,
            reason="Portable authority is not acceptable to the receiver.",
        )

    if inp.conflict_blocking:
        return AdoptionDecision(
            outcome="CONFLICT_BLOCKED",
            adopted=False,
            reason="Blocking conflict prevents receiver adoption.",
        )

    if inp.receiver_decision == "reject":
        return AdoptionDecision(
            outcome="REJECTED",
            adopted=False,
            reason="Receiver rejected the portable receipt.",
        )

    if inp.receiver_decision == "quarantine":
        return AdoptionDecision(
            outcome="QUARANTINED",
            adopted=False,
            reason="Receiver quarantined the portable receipt for review.",
        )

    if inp.receiver_decision == "rebind":
        return AdoptionDecision(
            outcome="REBOUND",
            adopted=False,
            reason="Receiver requires local authority rebound.",
        )

    if inp.receiver_decision == "adopt" and inp.portable_status == "portable":
        return AdoptionDecision(
            outcome="ADOPTED",
            adopted=True,
            reason="Receiver adopted the portable receipt.",
        )

    return AdoptionDecision(
        outcome="AUTHORITY_MISMATCH",
        adopted=False,
        reason="Receiver decision is not compatible with portable authority.",
    )
