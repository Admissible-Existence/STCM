#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from closure import decide  # noqa: E402
from fixtures import records  # noqa: E402


def expected_ok(record: dict, verdict: dict) -> bool:
    expected = record.get("expected")
    if expected == "CLOSED":
        if record.get("basis") in (None, ""):
            return verdict["verdict"] == "PROVEN_UNSATISFIABLE"
        return verdict["verdict"] == "SATISFIED"
    if expected == "BLOCKED":
        return verdict["verdict"] == "PROVEN_UNSATISFIABLE"
    return False


def main() -> int:
    results = []
    ok = True
    for record in records():
        verdict = decide(record)
        matched = expected_ok(record, verdict)
        ok = ok and matched
        results.append({
            "transition_id": record.get("transition_id"),
            "stage": record.get("stage"),
            "expected": record.get("expected"),
            "verdict": verdict,
            "matched": matched,
        })
    report = {
        "task_id": "closure-harness",
        "total": len(results),
        "matched": sum(1 for item in results if item["matched"]),
        "unexpected": sum(1 for item in results if not item["matched"]),
        "saturated": ok,
        "results": results,
    }
    out = ROOT / "dist" / "closure-harness-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
