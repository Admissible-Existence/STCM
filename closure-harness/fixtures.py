from __future__ import annotations


def records() -> list[dict]:
    return [
        {"transition_id":"PN-001","stage":"low:single_record_closure","expected":"CLOSED","basis":"complete single-node record","node_receipts":[{"receipt_id":"r1"}]},
        {"transition_id":"PN-002","stage":"low:missing_basis","expected":"CLOSED","basis":None,"node_receipts":[{"receipt_id":"r2"}]},
        {"transition_id":"PN-003","stage":"medium:current_authority","expected":"CLOSED","basis":"authority-bound record","authority_current":True,"node_receipts":[{"receipt_id":"r3"}]},
        {"transition_id":"PN-004","stage":"medium:expired_authority","expected":"CLOSED","basis":"expired authority must fail","authority_current":False,"node_receipts":[{"receipt_id":"r4"}]},
        {"transition_id":"PN-005","stage":"high:multi_node_merge","expected":"CLOSED","basis":"distinction-preserving merge","authority_current":True,"consent_resolved":True,"commit_time_reconstruction":True,"node_receipts":[{"receipt_id":"r5a"},{"receipt_id":"r5b"}],"merge_proof":{"preserves_distinctions":True,"source_receipt_ids":["r5a","r5b"]}},
        {"transition_id":"PN-006","stage":"high:invalid_multi_node_merge","expected":"CLOSED","basis":"merge proof mismatch must fail","authority_current":True,"consent_resolved":True,"commit_time_reconstruction":True,"node_receipts":[{"receipt_id":"r6a"},{"receipt_id":"r6b"}],"merge_proof":{"preserves_distinctions":True,"source_receipt_ids":["r6a"]}},
    ]
