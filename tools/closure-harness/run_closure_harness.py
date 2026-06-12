"""run_closure_harness.py — Saturation runner (dispatcher task entry point).

Three test layers, all decidable, none watching a checkmark:

  1. NODE layer    — each PN tested in isolation (IGNORE/BIND/REFUSE outcomes)
  2. COMPOSED layer — full transition -> 6 nodes -> record -> closure verdict
  3. CLOSURE layer  — the closure predicate over hand-built records (regression)

Reports a coverage matrix per layer. Terminal states:
  SATISFIED / PROVEN_UNSATISFIABLE / GAP  (GAP logged, non-fatal)

Exit 0 = saturated (all fixtures matched expectations). Exit 1 = unexpected result.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

import yaml

from closure import evaluate_closure, Verdict
from fixtures import all_fixtures
from node_fixtures import node_fixtures
from composed_fixtures import composed_fixtures
from compose import compose_record

POLICY_PATH = Path(__file__).parent / "completeness_policy.yaml"


def run_node_layer():
    results, unexpected = [], 0
    for fx in node_fixtures():
        out = fx["call"]()
        ok = out.engagement == fx["expect"]
        unexpected += 0 if ok else 1
        results.append({"fixture": fx["name"], "node": fx["node"],
                        "expected": fx["expect"].value,
                        "got": out.engagement.value,
                        "reason": out.reason_code, "match": ok})
    return results, unexpected


def run_composed_layer(policy):
    results, unexpected = [], 0
    for fx in composed_fixtures():
        record, outputs = compose_record(fx["transition"], fx["scope"])
        produced = record is not None
        rec_ok = produced == fx["expect_record"]
        if not produced:
            verdict_ok = fx["expect_verdict"] is None
            got_v = None
        else:
            res = evaluate_closure(record, policy)
            got_v = res.verdict.value
            if "expect_verdict_in" in fx:
                verdict_ok = res.verdict in fx["expect_verdict_in"]
            else:
                verdict_ok = res.verdict == fx["expect_verdict"]
        ok = rec_ok and verdict_ok
        unexpected += 0 if ok else 1
        results.append({"fixture": fx["name"], "stage": fx["stage"],
                        "record_produced": produced,
                        "verdict": got_v, "match": ok})
    return results, unexpected


def run_closure_layer(policy):
    results, unexpected = [], 0
    for fx in all_fixtures():
        res = evaluate_closure(fx["record"], policy)
        ok = res.verdict == fx["expect"]
        unexpected += 0 if ok else 1
        results.append({"fixture": fx["name"], "stage": fx["stage"],
                        "expected": fx["expect"].value, "got": res.verdict.value,
                        "reason": res.reason_code, "match": ok})
    return results, unexpected


def matrix_from(results, ok_is_satisfied_when):
    state = {}
    for r in results:
        stage = r.get("stage") or r.get("node") or r["fixture"]
        if not r["match"]:
            continue
        if ok_is_satisfied_when(r):
            state[stage] = "SATISFIED"
        else:
            state.setdefault(stage, "PROVEN_UNSATISFIABLE")
    return state


def main() -> int:
    policy = yaml.safe_load(POLICY_PATH.read_text())
    node_res, node_unexp = run_node_layer()
    comp_res, comp_unexp = run_composed_layer(policy)
    clos_res, clos_unexp = run_closure_layer(policy)
    total_unexp = node_unexp + comp_unexp + clos_unexp

    node_matrix = matrix_from(node_res, lambda r: r["got"] == "BIND")
    comp_matrix = matrix_from(comp_res, lambda r: r["verdict"] == "CLOSED")
    clos_matrix = matrix_from(clos_res, lambda r: r["got"] == "CLOSED")

    report = {
        "layers": {
            "node": {"run": len(node_res), "unexpected": node_unexp,
                     "matrix": dict(sorted(node_matrix.items())), "details": node_res},
            "composed": {"run": len(comp_res), "unexpected": comp_unexp,
                         "matrix": dict(sorted(comp_matrix.items())), "details": comp_res},
            "closure": {"run": len(clos_res), "unexpected": clos_unexp,
                        "matrix": dict(sorted(clos_matrix.items())), "details": clos_res},
        },
        "total_unexpected": total_unexp,
        "saturated": total_unexp == 0,
    }
    print(json.dumps(report, indent=2))

    def dump(title, matrix, unexp):
        print(f"\n=== {title} ===", file=sys.stderr)
        for stage, st in sorted(matrix.items()):
            mark = {"SATISFIED": "[*]", "PROVEN_UNSATISFIABLE": "[-]", "GAP": "[ ]"}[st]
            print(f"  {mark} {stage:40s} {st}", file=sys.stderr)
        print(f"  unexpected: {unexp}", file=sys.stderr)

    dump("NODE LAYER (each PN in isolation)", node_matrix, node_unexp)
    dump("COMPOSED LAYER (transition -> 6 nodes -> closure)", comp_matrix, comp_unexp)
    dump("CLOSURE LAYER (predicate regression)", clos_matrix, clos_unexp)
    print(f"\n  TOTAL unexpected: {total_unexp} "
          f"({'SATURATED' if total_unexp == 0 else 'FAILURES PRESENT'})", file=sys.stderr)
    return 1 if total_unexp else 0


if __name__ == "__main__":
    raise SystemExit(main())
