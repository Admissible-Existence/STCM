"""receipt_store.py — Governed receipt store (STCM v0.5).

The store is the AUTHORITY SURFACE for lineage facts, not free-form storage.
v0.4 took chain_head and known_successors as caller-supplied fixtures; v0.5
derives them from the store, so a transition can no longer assert its own
lineage truth — it presents a claim, and the store decides whether the claim
matches governed chain state.

INVIOLABLE: the store is APPEND-ONLY. There is no delete operation. Supersession
and conflict resolution flip status flags; they never remove a receipt. This
makes "history preserved" a structural property, not a tested hope:
    valid_as_closed stays true once a receipt closed;
    current_basis is what changes.

Query operations (spec §"Receipt store boundary"):
    get_receipt(receipt_id)
    get_chain_head(chain_id)
    get_successors(prior_receipt_id)
    is_superseded(receipt_id)
    get_conflicts(prior_receipt_id)
    get_resolution(conflict_id)
"""

from __future__ import annotations
from dataclasses import dataclass, field, replace
from enum import Enum


class ConflictStatus(str, Enum):
    OPEN = "OPEN"
    RESOLVED_ACCEPT_ONE = "RESOLVED_ACCEPT_ONE"
    RESOLVED_SUPERSEDE_ALL_BUT_ONE = "RESOLVED_SUPERSEDE_ALL_BUT_ONE"
    RESOLVED_REJECT_ALL = "RESOLVED_REJECT_ALL"
    ESCALATED = "ESCALATED"


@dataclass(frozen=True)
class Receipt:
    id: str
    hash: str
    chain_id: str
    sequence_index: int
    previous_receipt_id: str | None = None
    previous_receipt_hash: str | None = None
    state: str | None = None
    closed: bool = False
    closed_at: str | None = None
    superseded_by: str | None = None
    conflict_id: str | None = None
    resolution_status: str | None = None   # per-receipt outcome (accepted/rejected)
    source_transition_id: str | None = None
    conservation_record_hash: str | None = None

    # Derived, history-preserving facts.
    @property
    def valid_as_closed(self) -> bool:
        return self.closed is True

    @property
    def current_basis(self) -> bool:
        # A receipt is a valid CURRENT basis only if closed, not superseded,
        # and not rejected by conflict policy.
        return (self.closed is True
                and self.superseded_by is None
                and self.resolution_status != "rejected")


@dataclass
class Conflict:
    conflict_id: str
    prior_receipt_id: str
    sequence_index: int
    member_receipt_ids: list[str]
    status: ConflictStatus = ConflictStatus.OPEN
    accepted_receipt_id: str | None = None


class ReceiptStore:
    """Append-only governed index. No delete. Status changes only."""

    def __init__(self) -> None:
        self._receipts: dict[str, Receipt] = {}
        self._conflicts: dict[str, Conflict] = {}

    def _under_open_conflict(self, receipt_id: str) -> bool:
        """True if the receipt is a member of an OPEN (unresolved) conflict.
        Such a receipt cannot serve as a current basis until resolution."""
        r = self._receipts.get(receipt_id)
        if r is None or r.conflict_id is None:
            return False
        c = self._conflicts.get(r.conflict_id)
        return bool(c and c.status is ConflictStatus.OPEN)

    def _is_current_basis(self, r: Receipt) -> bool:
        return r.current_basis and not self._under_open_conflict(r.id)

    # ---- ingest (append-only) ----
    def put(self, receipt: Receipt) -> None:
        if receipt.id in self._receipts:
            raise ValueError(f"receipt {receipt.id} already exists (append-only)")
        self._receipts[receipt.id] = receipt

    # ---- query operations ----
    def get_receipt(self, receipt_id: str) -> Receipt | None:
        return self._receipts.get(receipt_id)

    def get_chain_head(self, chain_id: str) -> Receipt | None:
        """Current head = highest sequence_index in the chain that is a valid
        current basis (closed, not superseded, not rejected)."""
        candidates = [r for r in self._receipts.values()
                      if r.chain_id == chain_id and self._is_current_basis(r)]
        if not candidates:
            return None
        return max(candidates, key=lambda r: r.sequence_index)

    def get_successors(self, prior_receipt_id: str) -> list[Receipt]:
        return [r for r in self._receipts.values()
                if r.previous_receipt_id == prior_receipt_id]

    def is_superseded(self, receipt_id: str) -> bool:
        r = self._receipts.get(receipt_id)
        return bool(r and r.superseded_by is not None)

    def get_conflicts(self, prior_receipt_id: str) -> list[Conflict]:
        return [c for c in self._conflicts.values()
                if c.prior_receipt_id == prior_receipt_id]

    def get_resolution(self, conflict_id: str) -> Conflict | None:
        return self._conflicts.get(conflict_id)

    # ---- status mutations (never deletion) ----
    def supersede(self, old_id: str, new_id: str) -> None:
        """Mark old receipt superseded by new. History preserved: the old
        receipt stays closed/valid_as_closed; only current_basis flips."""
        old = self._receipts[old_id]
        self._receipts[old_id] = replace(old, superseded_by=new_id)

    def register_conflict(self, conflict: Conflict) -> None:
        self._conflicts[conflict.conflict_id] = conflict
        for rid in conflict.member_receipt_ids:
            if rid in self._receipts:
                self._receipts[rid] = replace(self._receipts[rid],
                                              conflict_id=conflict.conflict_id)

    def resolve_conflict(self, conflict_id: str, status: ConflictStatus,
                         accepted_receipt_id: str | None = None) -> None:
        """Resolve a conflict by changing posture. Losing receipts are flagged
        'rejected' (or superseded), NEVER deleted."""
        c = self._conflicts[conflict_id]
        c.status = status
        c.accepted_receipt_id = accepted_receipt_id
        for rid in c.member_receipt_ids:
            r = self._receipts.get(rid)
            if r is None:
                continue
            if status in (ConflictStatus.RESOLVED_ACCEPT_ONE,
                          ConflictStatus.RESOLVED_SUPERSEDE_ALL_BUT_ONE):
                if rid == accepted_receipt_id:
                    self._receipts[rid] = replace(r, resolution_status="accepted")
                else:
                    self._receipts[rid] = replace(
                        r, resolution_status="rejected",
                        superseded_by=(accepted_receipt_id
                                       if status ==
                                       ConflictStatus.RESOLVED_SUPERSEDE_ALL_BUT_ONE
                                       else r.superseded_by))
            elif status == ConflictStatus.RESOLVED_REJECT_ALL:
                self._receipts[rid] = replace(r, resolution_status="rejected")
            elif status == ConflictStatus.ESCALATED:
                self._receipts[rid] = replace(r, resolution_status="escalated")

    # ---- audit: everything ever put is still here ----
    def all_receipts(self) -> list[Receipt]:
        return list(self._receipts.values())
