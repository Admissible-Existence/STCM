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
  prime_nodes.py           # PN-001..PN-006 pure functions
  node_fixtures.py         # per-node isolation fixtures
  compose.py               # six-node output merger into conservation record
  composed_fixtures.py     # end-to-end transition fixtures
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

## Next-pass hooks (logged GAPs become work items)

- `low:multi_node_merge` — Open Q#11: merging multi-node receipts into one transition receipt.
- Add fixtures as PN-001..006 expand, each PN contributing one closure condition.
