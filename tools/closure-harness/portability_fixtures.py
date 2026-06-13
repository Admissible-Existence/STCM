#!/usr/bin/env python3
"""portability_fixtures.py - STCM v0.6 fixture family.

Covers early v0.6 portability vectors and derives expected outcomes from
the portability predicate module.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

from portability import PortabilityInput, evaluate_portability


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
    inp = PortabilityInput(**{k: row[k] for k in DIMENSIONS})
    return evaluate_portability(inp).outcome


def build_rows() -> list[dict]:
    keys = list(DIMENSIONS)
    rows = []
    for values in itertools.product(*(DIMENSIONS[k] for k in keys)):
        row = dict(zip(keys, values))
        decision = evaluate_portability(PortabilityInput(**row))
        row["expected"] = decision.outcome
        row["portable_candidate"] = decision.portable_candidate
        row["cross_repo_valid"] = decision.cross_repo_valid
        row["reason"] = decision.reason
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
