"""store_pipeline.py — v0.5 pipeline: store -> lineage -> conflict -> closure -> update.

Implements the v0.5 order:
    receipt store lookup
    -> lineage binding (reusing v0.4 evaluate_lineage)
    -> conflict policy check
    -> closure predicate
    -> next receipt basis
    -> receipt store update (ONLY after closure succeeds)

The transition presents a claimed prior; the STORE supplies the authoritative
chain_head and known_successors. The transition can no longer assert its own
lineage truth.
"""

from __future__ import annotations
from dataclasses import dataclass

from receipt_store import ReceiptStore, Receipt, Conflict, ConflictStatus
from lineage import evaluate_lineage, LineageResult, LineageVerdict
from closure import evaluate_closure, ClosureResult, Verdict


def _receipt_to_prior_dict(r: Receipt | None) -> dict | None:
    if r is None:
        return None
    return {"id": r.id, "hash": r.hash, "sequence_index": r.sequence_index,
            "closed": r.closed, "superseded_by": r.superseded_by,
            "state": r.state}


@dataclass(frozen=True)
class PipelineResult:
    store_head_id: str | None
    lineage: LineageResult
    conflict_status: str | None
    closure: ClosureResult | None
    closed: bool
    store_update_candidate: dict | None   # produced only on successful closure
    final_reason: str


def run_pipeline(transition: dict, record: dict, policy: dict,
                 store: ReceiptStore, chain_id: str) -> PipelineResult:
    # --- store lookup: authoritative head + successors ---
    head = store.get_chain_head(chain_id)
    claimed_prior_id = transition.get("claimed_prior_receipt_id")

    # Resolve the claimed prior FROM THE STORE (not from the transition's copy).
    store_prior = (store.get_receipt(claimed_prior_id)
                   if claimed_prior_id else None)
    successors = (store.get_successors(claimed_prior_id)
                  if claimed_prior_id else [])

    # Build a transition view whose prior_receipt is the STORE's record, so the
    # store's facts (not the transition's claim) drive lineage.
    store_transition = dict(transition)
    store_transition["prior_receipt"] = _receipt_to_prior_dict(store_prior)
    known_successors = [
        {"id": s.id, "previous_receipt_id": s.previous_receipt_id,
         "sequence_index": s.sequence_index}
        for s in successors
    ]

    # --- lineage binding (store-derived) ---
    lin = evaluate_lineage(
        store_transition,
        chain_head=_receipt_to_prior_dict(head),
        known_successors=known_successors)

    # --- conflict policy check ---
    conflict_status = None
    if claimed_prior_id:
        conflicts = store.get_conflicts(claimed_prior_id)
        # An OPEN conflict on the claimed prior blocks closure.
        open_conflicts = [c for c in conflicts
                          if c.status is ConflictStatus.OPEN]
        if open_conflicts:
            conflict_status = ConflictStatus.OPEN.value
        elif conflicts:
            conflict_status = conflicts[0].status.value

    # A rejected/superseded prior cannot serve as basis (store-authoritative),
    # even if the transition's own copy looked fine.
    if store_prior is not None and not store_prior.current_basis and lin.bound:
        lin = LineageResult(LineageVerdict.STALE, "PRIOR_NOT_CURRENT_BASIS",
                            "store: prior is superseded or rejected")

    # --- gate: lineage must bind AND no open conflict, before closure ---
    if not lin.bound:
        return PipelineResult(
            head.id if head else None, lin, conflict_status, None, False,
            None, f"LINEAGE_{lin.verdict.value}")
    if conflict_status == ConflictStatus.OPEN.value:
        return PipelineResult(
            head.id if head else None, lin, conflict_status, None, False,
            None, "CONFLICT_OPEN")

    # --- closure predicate ---
    clo = evaluate_closure(record, policy)
    if clo.verdict is not Verdict.CLOSED:
        return PipelineResult(
            head.id if head else None, lin, conflict_status, clo, False,
            None, clo.reason_code)

    # --- store-update candidate (only after successful closure) ---
    rr = record.get("result", {})
    update = {
        "id": rr.get("receipt_id"),
        "chain_id": chain_id,
        "sequence_index": transition.get("sequence_index"),
        "previous_receipt_id": claimed_prior_id,
        "previous_receipt_hash": transition.get("claimed_prior_receipt_hash"),
        "state": rr.get("resulting_state"),
        "closed": True,
        "source_transition_id": transition.get("transition_id"),
    }
    return PipelineResult(
        head.id if head else None, lin, conflict_status, clo, True,
        update, "CLOSED")
