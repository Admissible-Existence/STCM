"""compose.py — Compose the six PN outputs into a conservation record.

Runs PN-001..006 in dependency order over a single transition + scope, then
assembles the conservation record that closure.py evaluates. The record is now
PRODUCED by the nodes, not hand-written — so a field can only be present if a
node actually bound it. This is the dead-basis guarantee at the node layer:
no node binding => no field => closure cannot close on it.

Returns (record, node_outputs). If every node IGNOREs (out of scope), returns
(None, outputs) — a strictly ignored transition produces NO record at all
(STCM §13: non-matching transitions are not receipted).
"""

from __future__ import annotations
from typing import Any

from prime_nodes import (
    Engagement, NodeOutput,
    pn001_observe, pn002_bind_evidence, pn003_bind_authority,
    pn004_validate, pn005_refusal, pn006_receipt,
)


def _set(record: dict, dotted: str, value: Any) -> None:
    cur = record
    parts = dotted.split(".")
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value


def compose_record(transition: dict, scope: dict) -> tuple[dict | None, list[NodeOutput]]:
    obs = pn001_observe(transition, scope)
    ev = pn002_bind_evidence(transition, scope)
    au = pn003_bind_authority(transition, scope)
    dec = pn004_validate(transition, scope, ev, au, obs)
    upstream = [obs, ev, au, dec]
    refusal = pn005_refusal(transition, scope, upstream)
    rcpt = pn006_receipt(transition, scope, dec)

    outputs = [obs, ev, au, dec, refusal, rcpt]

    # Strict non-engagement: if nothing matched scope, produce no record.
    if all(o.engagement is Engagement.IGNORE for o in outputs):
        return None, outputs

    # Assemble the record from BOUND contributions only.
    record: dict = {
        "transition_id": transition.get("transition_id"),
        "transition_type": transition.get("transition_type"),
        "risk_tier": transition.get("risk_tier"),
        # incoming_receipts is carried from the transition (PN layer does not
        # forge receipt completeness; it is an input the chain supplies).
        "incoming_receipts": transition.get("incoming_receipts", {}),
        "entropy": transition.get("entropy", {}),  # advisory, never gates
        "result": {},
    }

    for o in outputs:
        if o.engagement is Engagement.BIND and o.field_path is not None:
            _set(record, o.field_path, o.value)

    # PN-004 binds result.decision; if it refused, surface its fail value too so
    # closure sees a concrete non-ALLOW decision rather than a null.
    if dec.engagement is Engagement.REFUSE:
        _set(record, "result.decision", dec.value)

    # phase_parameter passthrough (PN layer does not synthesize phase changes).
    if "phase_parameter" in transition:
        record["phase_parameter"] = transition["phase_parameter"]

    # resulting_state: observed -> proposed when allowed; observed when refused.
    if dec.value == "ALLOW" and transition.get("proposed_next_state") is not None:
        _set(record, "result.resulting_state", transition["proposed_next_state"])
    elif obs.engagement is Engagement.BIND:
        _set(record, "result.resulting_state", obs.value)

    # coherence_preserved: true only on a clean ALLOW with a receipt bound.
    coherent = (dec.value == "ALLOW"
                and rcpt.engagement is Engagement.BIND
                and refusal.value in (None,))
    _set(record, "result.coherence_preserved", bool(coherent))

    return record, outputs
