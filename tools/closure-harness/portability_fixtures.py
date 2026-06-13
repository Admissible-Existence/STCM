#!/usr/bin/env python3
"""portability_fixtures.py - STCM v0.6 fixture family.

Covers the first two v0.6 vectors:
- hidden dependency refusal
- authority rebind
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


DIMENSIONS = {
    "source_declared": [True, False],
    "target_declared": [True, False],
    "receipt_current": [True, False],
    "conflict_open": [True, False],
    "deposit_allowed": [True, False],
    "hidden_dependency": [True, False],
    "authority_class": ["source_bound", "evidence_portable", "authority_portable", "refused"],
    "authority_rebound": [True, False],
}


def expected(row: dict) -> str:
    if not row["source_declared"]:
        return "SOURCE_NOT_DECLARED"
    if not row["target_declared"]:
        return "TARGET_NOT_DECLARED"
    if not row["receipt_current"]:
        return "RECEIPT_NOT_CURRENT"
    if row["conflict_open"]:
        return "CONFLICT_OPEN"
    if not row["deposit_allowed"]:
        return "DEPOSIT_NOT_ALLOWED"
    if row["hidden_dependency"]:
        return "HIDDEN_DEPENDENCY"
    if row["authority_class"] == "refused":
        return "AUTHORITY_NOT_PORTABLE"
    if row["authority_class"] == "source_bound":
        return "AUTHORITY_NOT_PORTABLE"
    if row["authority_class"] == "evidence_portable" and not row["authority_rebound"]:
        return "AUTHORITY_REBIND_REQUIRED"
    if row["authority_class"] == "authority_portable":
        return "PORTABLE_PENDING_BOUNDARY"
    if row["authority_class"] == "evidence_portable" and row["authority_rebound"]:
        return "PORTABLE_PENDING_BOUNDARY"
    return "UNCLASSIFIED"


def build_rows() -> list[dict]:
    keys = list(DIMENSIONS)
    rows = []
    for values in itertools.product(*(DIMENSIONS[k] for k in keys)):
        row = dict(zip(keys, values))
        row["expected"] = expected(row)
        row["boundary"] = "stcm_v0_6"
        row["boundary_status"] = "draft"
        rows.append(row)
    return rows


def main() -> int:
    rows = build_rows()
    report = {
        "stage": "stcm_v0_6_portability_fixtures",
        "boundary": "stcm_v0_6",
        "boundary_status": "draft",
        "row_count": len(rows),
        "rows": rows,
    }
    out_dir = Path("reports")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "stcm_v0_6_portability_fixtures.json"
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in report if k != "rows"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
