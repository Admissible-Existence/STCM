from __future__ import annotations

from itertools import product


def build_rows():
    source_receipt_present = [False, True]
    receiver_declared = [False, True]
    portable_status = ["portable", "reboundable", "invalid"]
    conflict_blocking = [False, True]
    receiver_decision = ["adopt", "rebind", "reject", "quarantine"]

    for values in product(
        source_receipt_present,
        receiver_declared,
        portable_status,
        conflict_blocking,
        receiver_decision,
    ):
        src, recv, status, conflict, decision = values

        if not src or not recv:
            expected = "INSUFFICIENT_DECLARATION"
        elif status not in {"portable", "reboundable"}:
            expected = "AUTHORITY_MISMATCH"
        elif conflict:
            expected = "CONFLICT_BLOCKED"
        elif decision == "reject":
            expected = "REJECTED"
        elif decision == "quarantine":
            expected = "QUARANTINED"
        elif decision == "rebind":
            expected = "REBOUND"
        elif decision == "adopt" and status == "portable":
            expected = "ADOPTED"
        else:
            expected = "AUTHORITY_MISMATCH"

        yield {
            "source_receipt_present": src,
            "receiver_declared": recv,
            "portable_status": status,
            "conflict_blocking": conflict,
            "receiver_decision": decision,
            "expected": expected,
        }
