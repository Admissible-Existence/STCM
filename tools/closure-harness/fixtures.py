"""fixtures.py — Programmatic transition-record generator.

Instead of uploading files and watching a checkmark, we synthesize conservation
records across the whole spectrum and assert the expected verdict for each.

Each fixture declares:
    name     - human label
    record   - the conservation record (STCM §20 shape, minimal)
    expect   - expected Verdict
    stage    - which completeness stage it exercises (for the coverage matrix)

Negative fixtures (expected INCOMPLETE/REFUSED) are first-class: a stage that
"can't be met" is PROVEN_UNSATISFIABLE via a passing negative test.
"""

from __future__ import annotations
import copy
from closure import Verdict


def _base_record(tier: str = "medium") -> dict:
    """A fully-closing medium-tier record. Other fixtures mutate copies of this."""
    return {
        "transition_id": "T-0001",
        "transition_type": "bind_cleanup_evidence",
        "risk_tier": tier,
        "incoming_receipts": {"complete": True, "completeness_level": 3},
        "evidence": {"status": "bound"},
        "authority": {"status": "bound"},
        "phase_parameter": {"phase_change_type": "none"},
        "entropy": {  # advisory only — must never affect verdict
            "transition_entropy_required": None,
            "transition_entropy_released": None,
            "surplus_transition_entropy": None,
        },
        "result": {
            "decision": "ALLOW",
            "resulting_state": "EVIDENCE_BOUND",
            "receipt_id": "R-0001",
            "coherence_preserved": True,
        },
    }


def _mut(base: dict, path: str, value) -> dict:
    r = copy.deepcopy(base)
    cur = r
    parts = path.split(".")
    for p in parts[:-1]:
        cur = cur[p]
    if value is _DELETE:
        del cur[parts[-1]]
    else:
        cur[parts[-1]] = value
    return r


_DELETE = object()


def all_fixtures() -> list[dict]:
    fx: list[dict] = []

    # --- Positive: each tier closes when fully satisfied ---
    fx.append(dict(name="low_closes", stage="low:satisfied",
                   record=_base_record("low") |
                   {"incoming_receipts": {"complete": True, "completeness_level": 1},
                    "result": {"decision": "ALLOW", "resulting_state": "OBSERVED"}},
                   expect=Verdict.CLOSED))
    fx.append(dict(name="medium_closes", stage="medium:satisfied",
                   record=_base_record("medium"), expect=Verdict.CLOSED))
    high = _mut(_base_record("high"), "incoming_receipts.completeness_level", 5)
    fx.append(dict(name="high_closes", stage="high:satisfied",
                   record=high, expect=Verdict.CLOSED))
    irr = _mut(_base_record("irreversible"), "incoming_receipts.completeness_level", 7)
    fx.append(dict(name="irreversible_closes", stage="irreversible:satisfied",
                   record=irr, expect=Verdict.CLOSED))

    # --- Negative: receipt level below tier => INCOMPLETE (proven unsatisfiable) ---
    fx.append(dict(name="high_level_too_low", stage="high:level_gate",
                   record=_mut(_base_record("high"),
                               "incoming_receipts.completeness_level", 3),
                   expect=Verdict.INCOMPLETE))

    # --- Negative: null required field => INCOMPLETE (dead-basis guard) ---
    fx.append(dict(name="null_receipt_level", stage="guard:null_level",
                   record=_mut(_base_record("medium"),
                               "incoming_receipts.completeness_level", None),
                   expect=Verdict.INCOMPLETE))
    fx.append(dict(name="missing_receipt_id", stage="medium:receipt_id",
                   record=_mut(_base_record("medium"),
                               "result.receipt_id", _DELETE),
                   expect=Verdict.INCOMPLETE))

    # --- Negative: required flag False / status not bound => REFUSED ---
    fx.append(dict(name="receipts_incomplete_flag", stage="medium:complete_flag",
                   record=_mut(_base_record("medium"),
                               "incoming_receipts.complete", False),
                   expect=Verdict.REFUSED))
    fx.append(dict(name="authority_unbound", stage="high:authority",
                   record=_mut(high, "authority.status", "unbound"),
                   expect=Verdict.REFUSED))

    # --- Negative: GCAT/BCAT denied / fail-closed => REFUSED ---
    fx.append(dict(name="decision_deny", stage="gate:decision",
                   record=_mut(_base_record("medium"),
                               "result.decision", "DENY"),
                   expect=Verdict.REFUSED))

    # --- Forced irreversible: deletion can NOT close at low completeness ---
    # Receipt-chain integrity: a delete claiming low tier is overridden to
    # irreversible and must fail to close without level 7. PROVEN_UNSATISFIABLE.
    del_low = _base_record("low")
    del_low["transition_type"] = "delete_file"
    del_low["incoming_receipts"] = {"complete": True, "completeness_level": 1}
    fx.append(dict(name="delete_at_low_blocked", stage="integrity:delete_override",
                   record=del_low, expect=Verdict.INCOMPLETE))

    # Delete CAN close only with full irreversible posture.
    del_ok = _mut(_base_record("irreversible"),
                  "incoming_receipts.completeness_level", 7)
    del_ok["transition_type"] = "delete_file"
    del_ok["result"]["resulting_state"] = "DISPOSED"
    fx.append(dict(name="delete_with_disposition_closes",
                   stage="integrity:delete_disposed",
                   record=del_ok, expect=Verdict.CLOSED))

    # --- Advisory entropy must not affect verdict ---
    ent = _mut(_base_record("medium"),
               "entropy.surplus_transition_entropy", 99.0)
    fx.append(dict(name="entropy_does_not_gate", stage="advisory:entropy",
                   record=ent, expect=Verdict.CLOSED))

    return fx
