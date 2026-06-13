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

    return {
        "stage": "stcm_v0_6_portability_predicate_check",
        "boundary": "stcm_v0_6",
        "boundary_status": "draft",
        "rows": len(rows),
        "unexpected": unexpected,
        "saturated": unexpected == 0,
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "details": details,
    }


def main() -> int:
    report = check_rows()
    Path("reports").mkdir(exist_ok=True)
    Path("reports/stcm_v0_6_portability_predicate_check.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in report if k != "details"}, indent=2, sort_keys=True))
    return 0 if report["saturated"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
