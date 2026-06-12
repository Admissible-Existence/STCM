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
from merge_fixtures import merge_fixtures, _run_nodes
from merge import merge_observations
from routing_fixtures import routing_fixtures
from routed_hop import route_and_close
from hop_fixtures import hop_fixtures

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


def run_merge_layer(policy):
    """Multi-node merge: nodes -> merge -> (if coherent) closure (STCM §19)."""
    results, unexpected = [], 0
    for fx in merge_fixtures():
        outputs = _run_nodes(fx["transition"], fx["scope"],
                             fx.get("partial_scope_for"))
        mr = merge_observations(fx["transition"], outputs, fx["required"])
        coh_ok = mr.coherent == fx["expect_coherent"]
        reason_ok = True
        closure_v = None
        if not mr.coherent and "expect_reason" in fx:
            reason_ok = mr.reason_code == fx["expect_reason"]
        if mr.coherent:
            # A coherent merge MUST yield a closable record.
            res = evaluate_closure(mr.record, policy)
            closure_v = res.verdict.value
            reason_ok = res.verdict is Verdict.CLOSED
        ok = coh_ok and reason_ok
        unexpected += 0 if ok else 1
        results.append({"fixture": fx["name"], "stage": fx["stage"],
                        "coherent": mr.coherent, "reason": mr.reason_code,
                        "closure": closure_v, "match": ok})
    return results, unexpected


def run_routing_layer():
    """Routing front-gate: ignore / reroute / escalate (STCM §14-16)."""
    results, unexpected = [], 0
    for fx in routing_fixtures():
        out = fx["call"]()
        got = None if out is None else out.engagement
        ok = got == fx["expect"]
        if ok and out is not None and "expect_route_to" in fx:
            ok = out.route_to == fx["expect_route_to"]
        if ok and out is not None and "expect_reason" in fx:
            ok = out.reason_code == fx["expect_reason"]
        unexpected += 0 if ok else 1
        results.append({"fixture": fx["name"], "stage": fx["stage"],
                        "got": got.value if got else "PROCEED",
                        "route_to": getattr(out, "route_to", None) if out else None,
                        "reason": getattr(out, "reason_code", None) if out else None,
                        "match": ok})
    return results, unexpected


def run_hop_layer(policy):
    """Routed-hop integration: source reroutes -> dest closes (STCM §15-16)."""
    results, unexpected = [], 0
    for fx in hop_fixtures():
        hr = route_and_close(
            fx["transition"], fx["source_id"], fx["source_scope"],
            fx["dest_id"], fx["dest_scope"], policy)
        ok = (hr.routed == fx["expect_routed"]
              and hr.destination_matched == fx["expect_matched"]
              and hr.closed == fx["expect_closed"])
        if ok and "expect_reason" in fx:
            ok = hr.reason_code == fx["expect_reason"]
        unexpected += 0 if ok else 1
        results.append({"fixture": fx["name"], "stage": fx["stage"],
                        "routed": hr.routed, "matched": hr.destination_matched,
                        "closed": hr.closed, "verdict": hr.verdict,
                        "reason": hr.reason_code, "match": ok})
    return results, unexpected


def main() -> int:
    policy = yaml.safe_load(POLICY_PATH.read_text())
    node_res, node_unexp = run_node_layer()
    comp_res, comp_unexp = run_composed_layer(policy)
    route_res, route_unexp = run_routing_layer()
    hop_res, hop_unexp = run_hop_layer(policy)
    merge_res, merge_unexp = run_merge_layer(policy)
    clos_res, clos_unexp = run_closure_layer(policy)
    total_unexp = (node_unexp + comp_unexp + route_unexp + hop_unexp
                   + merge_unexp + clos_unexp)

    node_matrix = matrix_from(node_res, lambda r: r["got"] == "BIND")
    comp_matrix = matrix_from(comp_res, lambda r: r["verdict"] == "CLOSED")
    route_matrix = matrix_from(
        route_res, lambda r: r["got"] in ("PROCEED", "REROUTE"))
    hop_matrix = matrix_from(
        hop_res, lambda r: r["routed"] and r["matched"] and r["closed"])
    merge_matrix = matrix_from(merge_res, lambda r: r["coherent"] is True)
    clos_matrix = matrix_from(clos_res, lambda r: r["got"] == "CLOSED")

    report = {
        "layers": {
            "node": {"run": len(node_res), "unexpected": node_unexp,
                     "matrix": dict(sorted(node_matrix.items())), "details": node_res},
            "composed": {"run": len(comp_res), "unexpected": comp_unexp,
                         "matrix": dict(sorted(comp_matrix.items())), "details": comp_res},
            "routing": {"run": len(route_res), "unexpected": route_unexp,
                        "matrix": dict(sorted(route_matrix.items())), "details": route_res},
            "routed_hop": {"run": len(hop_res), "unexpected": hop_unexp,
                           "matrix": dict(sorted(hop_matrix.items())), "details": hop_res},
            "merge": {"run": len(merge_res), "unexpected": merge_unexp,
                      "matrix": dict(sorted(merge_matrix.items())), "details": merge_res},
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
    dump("ROUTING LAYER (ignore / reroute / escalate)", route_matrix, route_unexp)
    dump("ROUTED-HOP LAYER (source reroutes -> dest closes)", hop_matrix, hop_unexp)
    dump("MERGE LAYER (multi-node -> coherent receipt -> closure)", merge_matrix, merge_unexp)
    dump("CLOSURE LAYER (predicate regression)", clos_matrix, clos_unexp)
    print(f"\n  TOTAL unexpected: {total_unexp} "
          f"({'SATURATED' if total_unexp == 0 else 'FAILURES PRESENT'})", file=sys.stderr)
    return 1 if total_unexp else 0


if __name__ == "__main__":
    raise SystemExit(main())
