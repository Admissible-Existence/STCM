# Closure Harness — Dispatcher Task

**Task ID:** `closure-harness`
**Invoked by:** stable Core-Lite dispatcher (`core-lite-intake.yml`) — NOT a new workflow.
**Purpose:** Decide conservation-record closure (STCM §25) as a computed predicate.
Replaces “upload files → run workflow → check green checkmark ×1000” with a local
saturation run that terminates on a real coverage condition.

## What it does

Runs every transition fixture once and asserts its expected verdict. Reports a
coverage matrix with three terminal states per completeness stage:

|Mark |State               |Meaning                                                  |
|-----|--------------------|---------------------------------------------------------|
|`[*]`|SATISFIED           |a positive fixture closed the stage                      |
|`[-]`|PROVEN_UNSATISFIABLE|a negative fixture correctly refused/blocked, with reason|
|`[ ]`|GAP                 |no fixture exercises this stage — logged, non-fatal      |

## Current harness layers

1. **Node layer** — each PN is tested in isolation.
2. **Composed layer** — transition -> PN outputs -> conservation record -> closure.
3. **Routing layer** — ignore / reroute / escalate front-gate behavior.
4. **Routed-hop layer** — source reroutes -> recognized owner activates -> destination closes or governed non-closes.
5. **Merge layer** — multi-node outputs form a coherent merged receipt only when required nodes are present, non-refused, and non-colliding.
6. **Closure layer** — direct closure-predicate regression over hand-built records.

## Exit contract

- `0` — every fixture matched its expected verdict (passing negatives count as success). Run is SATURATED.
- `1` — one or more UNEXPECTED verdicts (a real regression). GAPs never cause exit 1.

## Files (all data/scripts — zero new workflow files)

```text
closure-harness/
  CLOSURE_HARNESS.md       # this file
  KEEP                     # directory marker for mobile-safe archives
  closure.py               # decidable closure predicate, dead-basis guarded
  completeness_policy.yaml # risk-tier -> required fields/level
  fixtures.py              # direct closure-predicate regression fixtures
  prime_nodes.py           # PN-001..PN-006 pure functions + routing front-gate
  node_fixtures.py         # per-node isolation fixtures
  compose.py               # six-node output merger into conservation record
  composed_fixtures.py     # end-to-end transition fixtures
  routing_fixtures.py      # ignore / reroute / escalate fixtures
  routed_hop.py            # source-to-destination routed-hop integration
  hop_fixtures.py          # routed-hop integration fixtures
  merge.py                 # multi-node coherent-recognition merge
  merge_fixtures.py        # merge/coherence fixtures
  run_closure_harness.py   # saturation runner / task entry point
```

The dispatcher task descriptor lives in:

```text
tools/task_registry.yaml
```

## Dead-basis guarantee

`closure.py` NEVER returns CLOSED when a required field is null. A green result
traces to an actual satisfied condition and names the field/reason on failure.
Entropy fields are advisory and never gate closure until numerically defined (Open Q#6).

## Current documented boundary

The current green/documented boundary is:

```text
STCM v0.3 — Routing, Routed-Hop, and Multi-Node Merge
```

See:

```text
docs/STCM_V0_3_ROUTED_HOP_AND_MERGE.md
```

## Next-pass hooks

- Sequential receipt lineage — receipt(t0) -> transition(t1) -> receipt(t1) -> transition(t2).
- Stale receipt refusal.
- Superseded receipt handling.
- Competing receipt-chain conflict detection.
- Keep transition entropy advisory until lineage is proven.
