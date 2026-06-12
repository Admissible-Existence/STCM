"""lineage.py — Sequential receipt lineage (STCM v0.4).

Adds continuity posture to the conservation record. A transition that claims
continuity must bind to the CORRECT prior receipt before closure may proceed:

    receipt(t0) -> transition(t1) -> receipt(t1) -> transition(t2)

Lineage verdicts (distinct from closure verdicts; they FEED closure):

    BOUND           prior is closed, current, not superseded, id+hash match
    MISSING_PRIOR   transition claims continuity but no prior is present
    MALFORMED_PRIOR prior exists but is missing required lineage fields
    CONFLICT        id matches but hash mismatches, OR competing successors
    STALE           prior is not the current head of the chain
    SUPERSEDED      prior explicitly points to a later replacement

Order (v0.4): scope/routing -> nodes -> merge/compose -> LINEAGE -> closure.
If lineage != BOUND, closure must not return CLOSED.

Two inviolable principles enforced here:
  * Supersession is NOT deletion: a superseded receipt remains valid-as-closed;
    it is only invalid as the basis for a NEW successor. History is preserved.
  * Conflict is NOT merge: two competing successors from the same prior are
    never silently merged; the verdict is CONFLICT (governed non-closure).
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class LineageVerdict(str, Enum):
    BOUND = "BOUND"
    MISSING_PRIOR = "MISSING_PRIOR"
    MALFORMED_PRIOR = "MALFORMED_PRIOR"
    CONFLICT = "CONFLICT"
    STALE = "STALE"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class LineageResult:
    verdict: LineageVerdict
    reason_code: str
    detail: str | None = None

    @property
    def bound(self) -> bool:
        return self.verdict is LineageVerdict.BOUND


# Fields a prior receipt MUST carry to be evaluable as a lineage basis.
_REQUIRED_PRIOR_FIELDS = ("id", "hash", "sequence_index", "closed")


def evaluate_lineage(transition: dict,
                     chain_head: dict | None = None,
                     known_successors: list[dict] | None = None) -> LineageResult:
    """Evaluate continuity posture for a transition claiming a prior receipt.

    transition expects:
        claimed_prior_receipt_id, claimed_prior_receipt_hash, sequence_index,
        and an embedded 'prior_receipt' object (the receipt as the transition
        presents it). In a real system the prior would be fetched from the store;
        here it is supplied on the transition (v0.4 is posture, not storage).
    chain_head: the receipt the store considers the CURRENT head of this chain.
    known_successors: receipts already claiming the same prior (conflict check).
    """
    claimed_id = transition.get("claimed_prior_receipt_id")
    claimed_hash = transition.get("claimed_prior_receipt_hash")
    prior = transition.get("prior_receipt")

    # --- genesis: a transition may legitimately claim NO prior (chain start) ---
    if claimed_id is None and prior is None:
        if transition.get("is_genesis") is True:
            return LineageResult(LineageVerdict.BOUND, "GENESIS_NO_PRIOR")
        return LineageResult(LineageVerdict.MISSING_PRIOR,
                             "NO_PRIOR_CLAIMED_NOT_GENESIS",
                             "transition claims continuity but names no prior")

    # --- missing: claims a prior id but the prior object is absent ---
    if prior is None:
        return LineageResult(LineageVerdict.MISSING_PRIOR, "PRIOR_ABSENT",
                             f"claimed {claimed_id} but no prior_receipt present")

    # --- malformed: prior present but missing required lineage fields ---
    missing = [f for f in _REQUIRED_PRIOR_FIELDS if prior.get(f) is None]
    if missing:
        return LineageResult(LineageVerdict.MALFORMED_PRIOR, "PRIOR_MISSING_FIELDS",
                             f"prior missing fields: {missing}")

    # --- conflict (identity): id matches but hash does not ---
    if prior.get("id") != claimed_id:
        return LineageResult(LineageVerdict.CONFLICT, "PRIOR_ID_MISMATCH",
                             f"prior.id={prior.get('id')} claimed={claimed_id}")
    if prior.get("hash") != claimed_hash:
        return LineageResult(LineageVerdict.CONFLICT, "PRIOR_HASH_MISMATCH",
                             "claimed prior hash does not match prior receipt hash")

    # --- prior must itself be closed to serve as a basis ---
    if prior.get("closed") is not True:
        return LineageResult(LineageVerdict.MALFORMED_PRIOR, "PRIOR_NOT_CLOSED",
                             "prior receipt is not closed; cannot be a basis")

    # --- superseded: prior explicitly points to a replacement ---
    # History-preserving: the prior is NOT deleted; it is simply not current.
    if prior.get("superseded_by") is not None:
        return LineageResult(LineageVerdict.SUPERSEDED, "PRIOR_SUPERSEDED",
                             f"prior superseded_by {prior.get('superseded_by')} "
                             "(prior remains valid-as-closed, not current)")

    # --- stale: prior is not the current head of the chain ---
    if chain_head is not None:
        head_id = chain_head.get("id")
        if head_id is not None and head_id != prior.get("id"):
            return LineageResult(LineageVerdict.STALE, "PRIOR_NOT_HEAD",
                                 f"head={head_id} but prior={prior.get('id')}")
        # sequence must advance by exactly one from the head.
        head_seq = chain_head.get("sequence_index")
        t_seq = transition.get("sequence_index")
        if (head_seq is not None and t_seq is not None
                and t_seq != head_seq + 1):
            return LineageResult(LineageVerdict.STALE, "SEQUENCE_NOT_CONTIGUOUS",
                                 f"head_seq={head_seq} transition_seq={t_seq}")

    # --- conflict (competing successors): another receipt already claims this
    # prior at the same sequence index. Never silently merged. ---
    if known_successors:
        t_seq = transition.get("sequence_index")
        competitors = [
            s for s in known_successors
            if s.get("previous_receipt_id") == prior.get("id")
            and s.get("sequence_index") == t_seq
            and s.get("id") != transition.get("result_receipt_id")
        ]
        if competitors:
            ids = [s.get("id") for s in competitors]
            return LineageResult(LineageVerdict.CONFLICT, "COMPETING_SUCCESSORS",
                                 f"competing successors from same prior: {ids}")

    return LineageResult(LineageVerdict.BOUND, "LINEAGE_BOUND")
