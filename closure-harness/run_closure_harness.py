#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from closure import decide  # noqa: E402
from fixtures import records  # noqa: E402


def expected_ok(record: dict, verdict: dict) -> bool:
    return verdict["verdict"] == record.get("expected_verdict")


def main() -> int:
    results = []
    ok = True
    for record in records():
        verdict = decide(record)
        matched = expected_ok(record, verdict)
        ok = ok and matched
        results.append({"transition_id": record.get("transition_id"), "stage": record.get("stage"), "expected": record.get("expected"), "expected_verdict": record.get("expected_verdict"), "verdict": verdict, "matched": matched})
    report = {"task_id":"closure-harness","policy_id":"stcm-closure-completeness-v2","total":len(results),"matched":sum(1 for item in results if item["matched"]),"unexpected":sum(1 for item in results if not item["matched"]),"saturated":ok,"authority_effect":False,"results":results}
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    out = ROOT / "dist" / "closure-harness-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
