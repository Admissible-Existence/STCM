"""run_closure_harness.py - Saturation runner (dispatcher task entry point).

Nine test layers, all decidable, none watching a checkmark:

  1. NODE layer        - each PN tested in isolation
  2. COMPOSED layer    - transition -> 6 nodes -> record -> closure verdict
  3. ROUTING layer     - front-gate ignore / reroute / escalate behavior
  4. ROUTED-HOP layer  - source reroutes -> destination closes or refuses
  5. MERGE layer       - multi-node outputs -> coherent receipt -> closure
  6. LINEAGE layer     - prior -> current -> next receipt continuity gate
  7. STORE layer       - governed receipt store + conflict policy pipeline
  8. PORTABILITY layer - draft v0.6 cross-repo receipt authority cases
  9. CLOSURE layer     - closure predicate regression

Reports a coverage matrix per layer. Terminal states:
  SATISFIED / PROVEN_UNSATISFIABLE / GAP

Exit 0 = saturated. Exit 1 = unexpected result.
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
from lineage_fixtures import lineage_fixtures
from lineage_gate import gated_close
from store_fixtures import store_fixtures
from store_pipeline import run_pipeline
from portability import PortabilityInput, evaluate_portability
from portability_fixtures import build_rows as portability_rows

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


def run_lineage_layer(policy):
    results, unexpected = [], 0
    for fx in lineage_fixtures():
        gr = gated_close(fx["record"], policy, fx["transition"],
                         chain_head=fx.get("chain_head"),
                         known_successors=fx.get("known_successors"))
        lin_ok = gr.lineage.verdict == fx["expect_lineage"]
        closed_ok = gr.closed == fx["expect_closed"]
        ok = lin_ok and closed_ok
        unexpected += 0 if ok else 1
        results.append({"fixture": fx["name"], "stage": fx["stage"],
                        "lineage": gr.lineage.verdict.value,
                        "lineage_reason": gr.lineage.reason_code,
                        "closed": gr.closed, "final_reason": gr.final_reason,
                        "match": ok})
    return results, unexpected


def run_store_layer(policy):
    results, unexpected = [], 0
    for fx in store_fixtures():
        store = fx["store"]
        pr = run_pipeline(fx["transition"], fx["record"], policy,
                          store, fx["chain_id"])
        ok = True
        notes = []

        if "expect_head" in fx:
            ok = ok and pr.store_head_id == fx["expect_head"]
        if "expect_lineage" in fx:
            ok = ok and pr.lineage.verdict.value == fx["expect_lineage"]
        if "expect_conflict" in fx:
            ok = ok and pr.conflict_status == fx["expect_conflict"]
        if "expect_closed" in fx:
            ok = ok and pr.closed == fx["expect_closed"]

        if "check_supersede" in fx:
            r = store.get_receipt(fx["check_supersede"])
            cond = r.valid_as_closed and not r.current_basis
            ok = ok and cond
            notes.append(f"{r.id} valid_as_closed={r.valid_as_closed} "
                         f"current_basis={r.current_basis}")
        if "check_resolution" in fx:
            acc, rej = fx["check_resolution"]
            ra, rr = store.get_receipt(acc), store.get_receipt(rej)
            cond = (ra.resolution_status == "accepted"
                    and rr.resolution_status == "rejected"
                    and rr.valid_as_closed)
            ok = ok and cond
            notes.append(f"accepted={ra.resolution_status} "
                         f"rejected={rr.resolution_status}")
        if "check_history" in fx:
            present = {r.id for r in store.all_receipts()}
            cond = all(rid in present for rid in fx["check_history"])
            ok = ok and cond
            notes.append(f"all_present={cond}")

        unexpected += 0 if ok else 1
        results.append({"fixture": fx["name"], "stage": fx["stage"],
                        "head": pr.store_head_id,
                        "lineage": pr.lineage.verdict.value,
                        "conflict": pr.conflict_status, "closed": pr.closed,
                        "final_reason": pr.final_reason,
                        "update": pr.store_update_candidate is not None,
                        "notes": "; ".join(notes), "match": ok})
    return results, unexpected


def run_portability_layer():
    results, unexpected = [], 0
    for i, row in enumerate(portability_rows()):
        inp = PortabilityInput(**{
            "source_declared": row["source_declared"],
            "target_declared": row["target_declared"],
            "receipt_posture": row["receipt_posture"],
            "conflict_open": row["conflict_open"],
            "deposit_posture": row["deposit_posture"],
            "hidden_dependency": row["hidden_dependency"],
            "lineage_continuous": row["lineage_continuous"],
            "authority_posture": row["authority_posture"],
        })
        decision = evaluate_portability(inp)
        ok = decision.outcome == row["expected"]
        unexpected += 0 if ok else 1
        results.append({"fixture": f"portability_{i:04d}",
                        "stage": decision.outcome,
                        "expected": row["expected"],
                        "got": decision.outcome,
                        "portable_candidate": decision.portable_candidate,
                        "cross_repo_valid": decision.cross_repo_valid,
                        "reason": decision.reason,
                        "boundary": row["boundary"],
                        "boundary_status": row["boundary_status"],
                        "match": ok})
    return results, unexpected


def main() -> int:
    policy = yaml.safe_load(POLICY_PATH.read_text())
    node_res, node_unexp = run_node_layer()
    comp_res, comp_unexp = run_composed_layer(policy)
    route_res, route_unexp = run_routing_layer()
    hop_res, hop_unexp = run_hop_layer(policy)
    merge_res, merge_unexp = run_merge_layer(policy)
    lin_res, lin_unexp = run_lineage_layer(policy)
    store_res, store_unexp = run_store_layer(policy)
    port_res, port_unexp = run_portability_layer()
    clos_res, clos_unexp = run_closure_layer(policy)
    total_unexp = (node_unexp + comp_unexp + route_unexp + hop_unexp
                   + merge_unexp + lin_unexp + store_unexp + port_unexp
                   + clos_unexp)

    node_matrix = matrix_from(node_res, lambda r: r["got"] == "BIND")
    comp_matrix = matrix_from(comp_res, lambda r: r["verdict"] == "CLOSED")
    route_matrix = matrix_from(
        route_res, lambda r: r["got"] in ("PROCEED", "REROUTE"))
    hop_matrix = matrix_from(
        hop_res, lambda r: r["routed"] and r["matched"] and r["closed"])
    merge_matrix = matrix_from(merge_res, lambda r: r["coherent"] is True)
    lin_matrix = matrix_from(lin_res, lambda r: r["lineage"] == "BOUND" and r["closed"])
    store_matrix = matrix_from(store_res, lambda r: r["closed"] is True)
    port_matrix = matrix_from(port_res, lambda r: r["portable_candidate"] is True)
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
            "lineage": {"run": len(lin_res), "unexpected": lin_unexp,
                        "matrix": dict(sorted(lin_matrix.items())), "details": lin_res},
            "store": {"run": len(store_res), "unexpected": store_unexp,
                      "matrix": dict(sorted(store_matrix.items())), "details": store_res},
            "portability": {"run": len(port_res), "unexpected": port_unexp,
                            "matrix": dict(sorted(port_matrix.items())), "details": port_res},
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
    dump("LINEAGE LAYER (prior->current->next continuity, v0.4)", lin_matrix, lin_unexp)
    dump("STORE LAYER (governed receipt store + conflict policy, v0.5)", store_matrix, store_unexp)
    dump("PORTABILITY LAYER (draft portable receipt authority, v0.6)", port_matrix, port_unexp)
    dump("CLOSURE LAYER (predicate regression)", clos_matrix, clos_unexp)
    print(f"\n  TOTAL unexpected: {total_unexp} "
          f"({'SATURATED' if total_unexp == 0 else 'FAILURES PRESENT'})", file=sys.stderr)
    return 1 if total_unexp else 0


if __name__ == "__main__":
    raise SystemExit(main())
