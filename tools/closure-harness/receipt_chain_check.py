#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from receipt_chain import validate_receipt_chain
from receipt_chain_fixtures import build_chain_fixtures

report_path = Path("reports/stcm_v0_8_receipt_chain_check.json")
report_path.parent.mkdir(parents=True, exist_ok=True)

rows = []
unexpected = 0

for fx in build_chain_fixtures():
    result = validate_receipt_chain(fx["chain"], fx["receiver_outcome"])
    match = result["valid"] == fx["expect_valid"]
    unexpected += 0 if match else 1
    rows.append({
        "fixture": fx["name"],
        "expected_valid": fx["expect_valid"],
        "got_valid": result["valid"],
        "reason": result["reason"],
        "match": match,
    })

report = {
    "stage": "stcm_v0_8_receipt_chain_check",
    "boundary": "stcm_v0_8",
    "boundary_status": "draft",
    "row_count": len(rows),
    "unexpected": unexpected,
    "saturated": unexpected == 0,
    "rows": rows,
}

report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
print(json.dumps({
    "stage": report["stage"],
    "boundary": report["boundary"],
    "row_count": report["row_count"],
    "unexpected": report["unexpected"],
    "saturated": report["saturated"],
    "report": str(report_path),
}, indent=2, sort_keys=True))

raise SystemExit(0 if unexpected == 0 else 1)
