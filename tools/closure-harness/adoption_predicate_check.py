#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from adoption import AdoptionInput, evaluate_adoption
from adoption_fixtures import build_rows

report_path = Path("reports/stcm_v0_7_adoption_handshake.json")
report_path.parent.mkdir(parents=True, exist_ok=True)

rows = []
unexpected = 0

for i, row in enumerate(build_rows()):
    inp = AdoptionInput(
        source_receipt_present=row["source_receipt_present"],
        receiver_declared=row["receiver_declared"],
        portable_status=row["portable_status"],
        conflict_blocking=row["conflict_blocking"],
        receiver_decision=row["receiver_decision"],
    )
    decision = evaluate_adoption(inp)
    match = decision.outcome == row["expected"]
    unexpected += 0 if match else 1
    rows.append({
        "fixture": f"adoption_{i:03d}",
        "expected": row["expected"],
        "got": decision.outcome,
        "match": match,
        "adopted": decision.adopted,
        "boundary": decision.boundary,
        "boundary_status": decision.boundary_status,
    })

report = {
    "stage": "stcm_v0_7_adoption_handshake",
    "boundary": "stcm_v0_7",
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
