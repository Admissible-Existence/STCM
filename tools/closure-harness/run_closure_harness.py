"""run_closure_harness.py — Saturation runner (dispatcher task entry point).

This is the task the stable dispatcher invokes. It does NOT watch a checkmark.
It runs every fixture once, asserts the expected verdict, and reports a coverage
matrix of completeness stages with three terminal states per stage:

    SATISFIED            - a positive fixture closed it
    PROVEN_UNSATISFIABLE - a negative fixture correctly refused/blocked, with reason
    GAP                  - a stage with no fixture exercising it (logged, non-fatal)

Exit codes:
    0  every fixture matched its expected verdict (negatives passing is success)
    1  one or more fixtures produced an UNEXPECTED verdict (a real failure)
GAPs never cause exit 1; they are logged for the next pass.
"""

from __future__ import annotations
import json
import sys
import yaml
from pathlib import Path

from closure import evaluate_closure, Verdict
from fixtures import all_fixtures

POLICY_PATH = Path(__file__).parent / "completeness_policy.yaml"

# Stages we expect coverage for. A declared stage with no fixture => GAP.
EXPECTED_STAGES = {
    "low:satisfied", "medium:satisfied", "high:satisfied", "irreversible:satisfied",
    "high:level_gate", "guard:null_level", "medium:receipt_id",
    "medium:complete_flag", "high:authority", "gate:decision",
    "integrity:delete_override", "integrity:delete_disposed", "advisory:entropy",
    # Intentionally-uncovered stage to demonstrate GAP reporting:
    "low:multi_node_merge",
}


def main() -> int:
    policy = yaml.safe_load(POLICY_PATH.read_text())
    fixtures = all_fixtures()

    results = []
    unexpected = 0
    stage_state: dict[str, str] = {}

    for fx in fixtures:
        res = evaluate_closure(fx["record"], policy)
        ok = res.verdict == fx["expect"]
        if not ok:
            unexpected += 1
        # Classify stage outcome.
        if res.verdict == Verdict.CLOSED and ok:
            stage_state[fx["stage"]] = "SATISFIED"
        elif res.verdict in (Verdict.INCOMPLETE, Verdict.REFUSED) and ok:
            stage_state.setdefault(fx["stage"], "PROVEN_UNSATISFIABLE")
        results.append({
            "fixture": fx["name"], "stage": fx["stage"],
            "expected": fx["expect"].value, "got": res.verdict.value,
            "reason": res.reason_code, "field": res.failing_field,
            "tier": res.risk_tier, "level": res.completeness_level,
            "match": ok,
        })

    gaps = sorted(EXPECTED_STAGES - set(stage_state.keys()))
    for g in gaps:
        stage_state[g] = "GAP"

    report = {
        "fixtures_run": len(fixtures),
        "unexpected_verdicts": unexpected,
        "stage_matrix": dict(sorted(stage_state.items())),
        "gaps_logged": gaps,
        "details": results,
        "saturated": unexpected == 0,
    }
    print(json.dumps(report, indent=2))

    # Human summary
    print("\n=== STAGE COVERAGE MATRIX ===", file=sys.stderr)
    for stage, state in sorted(stage_state.items()):
        mark = {"SATISFIED": "[*]", "PROVEN_UNSATISFIABLE": "[-]", "GAP": "[ ]"}[state]
        print(f"  {mark} {stage:32s} {state}", file=sys.stderr)
    if gaps:
        print(f"\n  {len(gaps)} GAP(s) logged (non-fatal): {gaps}", file=sys.stderr)
    print(f"\n  unexpected verdicts: {unexpected} "
          f"({'SATURATED' if unexpected == 0 else 'FAILURES PRESENT'})",
          file=sys.stderr)

    return 1 if unexpected else 0


if __name__ == "__main__":
    raise SystemExit(main())
