#!/usr/bin/env python3
"""portability_predicate_check.py - saturate STCM v0.6 portability predicates.

This check independently re-evaluates every portability fixture row through
portability.evaluate_portability and compares the result to the fixture's
expected outcome.
"""

from __future__ import annotations

import collections
import json
from pathlib import Path

from portability import PortabilityInput, evaluate_portability
from portability_fixtures import DIMENSIONS, build_rows


DETAIL_PATH = Path("reports/stcm_v0_6_portability_predicate_check.json")
SATURATION_PATH = Path("reports/stcm_v0_6_portability_saturation.json")


def check_rows() -> dict:
    rows = build_rows()
    details = []
    unexpected = 0
    outcome_counts = collections.Counter()

    for i, row in enumerate(rows):
        inp = PortabilityInput(**{k: row[k] for k in DIMENSIONS})
        decision = evaluate_portability(inp)
        expected = row["expected"]
        got = decision.outcome
        ok = got == expected
        unexpected += 0 if ok else 1
        outcome_counts[got] += 1
        details.append({
            "fixture": f"portability_predicate_{i:04d}",
            "expected": expected,
            "got": got,
            "portable_candidate": decision.portable_candidate,
            "cross_repo_valid": decision.cross_repo_valid,
            "reason": decision.reason,
            "match": ok,
        })

    saturated = unexpected == 0
    return {
        "stage": "stcm_v0_6_portability_predicate_check",
        "boundary": "stcm_v0_6",
        "boundary_status": "validated_draft_candidate" if saturated else "draft_gap",
        "rows": len(rows),
        "unexpected": unexpected,
        "saturated": saturated,
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "details": details,
    }


def saturation_record(report: dict) -> dict:
    return {
        "stage": "stcm_v0_6_portability_saturation",
        "boundary": report["boundary"],
        "boundary_status": report["boundary_status"],
        "row_count": report["rows"],
        "unexpected": report["unexpected"],
        "saturated": report["saturated"],
        "outcome_count": len(report["outcome_counts"]),
        "outcome_counts": report["outcome_counts"],
        "detail_report": str(DETAIL_PATH),
    }


def main() -> int:
    report = check_rows()
    record = saturation_record(report)
    Path("reports").mkdir(exist_ok=True)
    DETAIL_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    SATURATION_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if report["saturated"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
