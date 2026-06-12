"""lineage_gate.py — Enforce the v0.4 order: lineage BEFORE closure.

    scope/routing -> nodes -> merge/compose -> LINEAGE -> closure -> next basis

If lineage != BOUND, closure must not return CLOSED. This module makes that
ordering a single callable so no caller can accidentally close a record whose
lineage failed.
"""

from __future__ import annotations
from dataclasses import dataclass

from lineage import evaluate_lineage, LineageResult, LineageVerdict
from closure import evaluate_closure, ClosureResult, Verdict


@dataclass(frozen=True)
class GatedResult:
    lineage: LineageResult
    closure: ClosureResult | None   # None when lineage blocked closure
    closed: bool

    @property
    def final_reason(self) -> str:
        if not self.lineage.bound:
            return f"LINEAGE_{self.lineage.verdict.value}"
        return self.closure.reason_code if self.closure else "NO_CLOSURE_RUN"


def gated_close(record: dict, policy: dict,
                transition: dict,
                chain_head: dict | None = None,
                known_successors: list[dict] | None = None) -> GatedResult:
    lin = evaluate_lineage(transition, chain_head, known_successors)
    if not lin.bound:
        # Governed non-closure: lineage failure short-circuits closure.
        return GatedResult(lin, None, closed=False)
    clo = evaluate_closure(record, policy)
    return GatedResult(lin, clo, closed=clo.verdict is Verdict.CLOSED)
