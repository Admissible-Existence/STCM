# STCM v0.3 — Routing, Routed-Hop, and Multi-Node Merge

## Status

This document records the first green operational boundary after the closure harness expanded beyond direct closure and composed transition tests.

The v0.3 harness now evaluates six decidable layers:

1. Node layer — each Prime Node tested in isolation.
2. Composed layer — transition -> six nodes -> conservation record -> closure.
3. Routing layer — ignore / reroute / escalate front-gate behavior.
4. Routed-hop layer — source reroutes -> recognized destination owner receives -> destination closes or governed non-closes.
5. Merge layer — multiple node outputs merge into one coherent transition receipt when required conditions hold.
6. Closure layer — direct closure predicate regression over hand-built records.

A green run means every fixture in every layer matched its expected verdict or expected governed non-closure.

A green run does **not** mean the model is complete. It means the current declared conservation boundary is saturated.

---

## Core claim

A transition may become a receipt basis only after it survives the appropriate activation, routing, merge, composition, and closure checks for its declared posture.

In v0.3, this is no longer a prose-only claim. It is tested as a computed harness.

---

## Routing boundary

Routing exists before node evaluation.

A node first classifies a transition against its declared hash scope. The result may be:

- `NONE` — no hash overlap; the node ignores the transition.
- `MATCH` — the node owns the hash and proceeds to its own logic.
- `TOUCH` — the node recognizes that the transition belongs to another declared node.

A `TOUCH` does not automatically become a valid route. The route equation must hold:

```text
route_possible = hash_match AND receipt_sufficient AND transition_allowed
```

When the equation holds and a target exists, the node returns `REROUTE`.

When the equation fails or no governed target exists, the node returns `ESCALATE`.

This prevents touched-but-unresolved transitions from being silently dropped or incorrectly treated as valid movement.

---

## Routed-hop boundary

Routing must be proven end-to-end.

A valid routed hop requires:

1. The source node produces `REROUTE`.
2. The route target matches the expected destination node.
3. The destination node actually activates on the rerouted hash.
4. The destination composes a conservation record.
5. The destination closes or produces a governed non-closure.

A route whose destination ignores the transition is not a harmless miss. It is a broken route and must be observable as a governed outcome.

A routed transition may still fail closure at the destination. That is allowed when the failure is governed, explicit, and reasoned.

---

## Multi-node merge boundary

A single transition may require multiple Prime Nodes to observe different parameters of the same transition.

The merge step is not voting, averaging, or consensus by count.

A coherent merge requires:

- the node outputs are related to the same transition execution context;
- all required nodes are present;
- no required node ignored the transition;
- no required node refused the transition;
- no two nodes write the same conservation-record field;
- bound node outputs can be folded into one transition receipt;
- the resulting record preserves coherence.

If any of those conditions fail, the merge is not coherent and must return a reason code.

The merge layer produces a `node_activation` block that records how the node set behaved.

---

## Node activation record

The `node_activation` block is the first operational receipt of how the node field behaved as a group.

It records:

- total nodes available;
- activated nodes;
- ignored node count;
- refused nodes;
- routed nodes;
- escalated nodes;
- required nodes.

This makes multi-node recognition inspectable instead of hidden behind a single green check.

---

## Closure boundary

Closure remains the final predicate.

A merged or composed record must still satisfy the policy-defined completeness tier and required fields before it may close.

The closure predicate still preserves the dead-basis rule:

```text
required null field -> never CLOSED
```

Closure also remains separate from routing. A route can succeed while destination closure fails.

That distinction is intentional.

---

## What green means in v0.3

A green v0.3 harness run means:

- out-of-scope transitions ignore correctly;
- owned transitions proceed into node logic;
- touched transitions reroute only when the route equation holds;
- unresolved touched transitions escalate instead of disappearing;
- routed hops are checked at source and destination;
- broken routes are detected;
- routed-but-invalid transitions non-close explicitly;
- required multi-node observations merge only when coherent;
- field collisions, missing nodes, ignored required nodes, and refused required nodes block coherent merge;
- coherent merged records can close only through the closure predicate;
- every tested expected failure is a governed non-closure, not an accidental pass.

---

## What green does not mean yet

A green v0.3 run does not prove:

- long sequential receipt lineage across many transitions;
- stale receipt detection;
- superseded receipt handling;
- conflict resolution between two valid-looking receipts;
- runtime revalidation at later time `t+n`;
- numeric transition entropy;
- cross-repository governance portability;
- external authority portability beyond the current fixture model.

Those remain later build targets.

---

## Next build boundary

The next recommended build boundary is sequential receipt lineage.

The model should next prove:

```text
receipt(t0) -> transition(t1) -> receipt(t1) -> transition(t2)
```

The next harness should answer:

- Can a later transition bind to the exact prior receipt?
- Can a stale receipt be refused?
- Can a superseded receipt be recognized without deleting history?
- Can two competing receipt chains be identified as conflict rather than merged silently?

Transition entropy should remain advisory until sequential receipt lineage is proven.

---

## Version boundary statement

STCM v0.3 establishes that a transition can be ignored, routed, node-bound, merged, composed, and closed only when the declared hash scope, routing path, node outputs, receipt posture, merge coherence, and closure policy agree.

This is the first executable boundary for routed multi-node admissible transition recognition.
