from __future__ import annotations

from dataclasses import dataclass

from adoption import AdoptionInput, evaluate_adoption

REQUIRED_FIELDS = {
    "receipt_id",
    "source_repo",
    "source_receipt_id",
    "source_boundary",
    "receiving_repo",
    "receiving_boundary",
    "receiver_declared",
    "portable_status",
    "conflict_blocking",
    "receiver_decision",
    "outcome",
    "adopted",
    "reason",
    "timestamp",
}


@dataclass(frozen=True)
class ReceiptValidation:
    valid: bool
    reason: str


def validate_receiver_decision_receipt(receipt: dict) -> ReceiptValidation:
    missing = sorted(REQUIRED_FIELDS - set(receipt.keys()))
    if missing:
        return ReceiptValidation(False, "missing_fields:" + ",".join(missing))

    if receipt["receiving_boundary"] != "stcm_v0_7":
        return ReceiptValidation(False, "wrong_receiving_boundary")

    inp = AdoptionInput(
        source_receipt_present=bool(receipt["source_receipt_id"]),
        receiver_declared=bool(receipt["receiver_declared"]),
        portable_status=receipt["portable_status"],
        conflict_blocking=bool(receipt["conflict_blocking"]),
        receiver_decision=receipt["receiver_decision"],
    )
    decision = evaluate_adoption(inp)

    if receipt["outcome"] != decision.outcome:
        return ReceiptValidation(False, "outcome_mismatch")

    if bool(receipt["adopted"]) != decision.adopted:
        return ReceiptValidation(False, "adopted_mismatch")

    return ReceiptValidation(True, "valid_receiver_decision_receipt")
