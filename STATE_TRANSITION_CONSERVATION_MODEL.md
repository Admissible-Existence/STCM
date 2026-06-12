# State Transition Conservation Model

**Status:** v0.1 foundational theory  
**Ecosystem:** StegVerse  
**Scope:** Prime Nodes, Transition Table, Core-Lite, CGE, RTG, MR, DC, receipt-bound governance  
**Purpose:** Define a measurable conservation model for governed state transitions across node-based StegVerse systems.

---

## Assumptions

This document captures the current theory layer before implementation.

It assumes:

1. StegVerse state transitions are governed by a Transition Table.
2. Prime Nodes are bounded governance actors, not unrestricted autonomous agents.
3. Every state transition is conditioned by receipts from prior state transitions.
4. Evaluation occurs through mathematically evaluable terms at a specific moment.
5. Hashes are cheap, concise, and suitable for first-pass routing and activation.
6. Nodes should remain dormant unless a transition matches their declared hash scope.
7. Compute preservation is a governance property, not merely an optimization.
8. A transition is not coherent unless its conservation record can close.

---

## Definition of Done

This v0.1 model is considered complete when it defines:

1. What a state transition is.
2. What a Prime Node is.
3. How receipts condition transitions.
4. How hash-scoped activation works.
5. How routing emerges from non-ignorance.
6. How compute is preserved.
7. How phase changes are modeled.
8. How transition entropy is accounted for.
9. How conservation records close.
10. What should be implemented next.

---

# 1. Core Claim

A governed system does not merely move from one state to another.

It must account for what was received, activated, ignored, consumed, preserved, released, refused, routed, transformed, and receipted during that movement.

The central model is:

```text
state transition
= incoming receipt relationship
+ hash posture
+ active node set
+ ignored node set
+ phase parameter
+ transition entropy
+ authority binding
+ evidence binding
+ moment-bound value comparison
+ resulting receipt
```

A transition becomes coherent only when this relationship can be closed into a conservation record.

---

# 2. State Transition Conservation Principle

```text
A governed system preserves coherence by ensuring that every state transition accounts for its receipt relationships, active node set, ignored node set, phase parameter, entropy change, authority binding, evidence binding, compute load, and resulting receipt.

Nothing participates silently, and nothing becomes authoritative without a receipt-bound transition path.
```

In short:

```text
Every state transition must close its conservation record before it can become the receipt basis for the next state transition.
```

---

# 3. Receipt-Relational State Transition Principle

Every state transition is the relationship of incoming receipts from one or more previous state transitions.

The transition may require:

```text
receipt existence only
some receipts
required receipts
sufficient receipts
complete receipt chain
complete receipt content validation
complete receipt chain with authority/evidence/runtime revalidation
```

Not every transition requires the same receipt completeness.

Low-risk transitions may require only receipt existence.

High-risk or irreversible transitions may require complete receipt chains, authority revalidation, evidence revalidation, quorum, and runtime checks.

## Receipt Completeness Range

```text
0. No receipt
1. Receipt existence only
2. Some receipts
3. Required receipts
4. Sufficient receipts
5. Complete receipts
6. Complete receipts with content verification
7. Complete receipts with authority/evidence/runtime revalidation
```

## Principle

```text
No valid transition without the required receipt relationship.
```

---

# 4. Prime Nodes

A Prime Node is a bounded governance actor.

It is not defined first by intelligence.

It is defined by:

```text
mission
authority
inputs
outputs
hash scope
transition function
receipt requirements
refusal conditions
metrics
escalation path
```

Prime Nodes should be built in accordance with the Transition Table.

The first Prime Nodes should be Transition Prime Nodes.

---

# 5. Initial Transition Prime Nodes

The first nodes should represent the minimum operational skeleton of governed transition.

```text
PN-001 — State Observation Node
PN-002 — Evidence Binding Node
PN-003 — Authority Binding Node
PN-004 — Transition Validation Node
PN-005 — Refusal / Block Node
PN-006 — Receipt / Continuity Node
```

## PN-001 — State Observation Node

Observes and classifies the current state before a transition is considered.

It answers:

```text
What state is the object, actor, claim, repo, bundle, node, or decision currently in?
```

It does not decide whether the transition is valid.

## PN-002 — Evidence Binding Node

Determines whether the proposed transition has required evidence attached.

It answers:

```text
What evidence supports this transition?
Is the evidence current?
Is the evidence admissible?
Is the evidence sufficient?
Is the evidence bound to the object being transitioned?
```

## PN-003 — Authority Binding Node

Determines whether the actor or system has authority to request or perform the transition.

It answers:

```text
Who is requesting the transition?
What authority is claimed?
Is that authority current?
Is that authority scoped to this action?
Is that authority portable?
Is there a hidden platform dependency?
```

## PN-004 — Transition Validation Node

Validates whether the movement from current state to proposed next state is allowed.

It checks:

```text
current_state
proposed_next_state
transition_rule
evidence_status
authority_status
risk_status
runtime_status
receipt_posture
```

## PN-005 — Refusal / Block Node

Produces governed refusal when a transition is invalid, unsupported, unauthorized, unsafe, premature, stale, malformed, or incoherent.

Refusal is not failure.

Refusal is a governed state.

## PN-006 — Receipt / Continuity Node

Records the transition result and preserves continuity.

It prepares clean receipt-bound records for:

```text
DC = Data Continuation
MR = Master Records
```

---

# 6. Finite Node Capacity Principle

Every Prime Node has finite governed capacity.

This capacity includes:

```text
observation load
evidence load
authority load
transition load
refusal load
receipt load
escalation load
runtime load
ambiguity load
risk load
```

A node is overloaded when it can no longer preserve governed distinction.

It can fail by:

```text
misclassifying state
missing evidence
treating evidence as authority
treating recommendation as execution
failing to refuse
delaying receipts
producing ambiguous outputs
collapsing runtime validity into prior validity
```

---

# 7. Mathematical Necessity of Expansion

Node expansion is not merely mathematically justified.

It is mathematically necessary once a node exceeds its exact coherent capability threshold.

```text
If Lg <= Cg:
    node remains coherent

If Lg > Cg:
    node must replicate, specialize, reroute, refuse, escalate, pause, evolve, devolve, or dissolve

If Lg > Cg and no structural response occurs:
    instability begins

If instability persists:
    transition coherence fails
```

Where:

```text
Lg = governed load
Cg = governed coherent capacity
```

## Prime Node Expansion Law

```text
A Prime Node may operate coherently only within its finite governed capacity.

When governed load exceeds that capacity, expansion becomes mathematically necessary.

The system must create additional node capacity through replication, specialization, routing, refusal, escalation, evolution, devolution, or dissolution.

If it does not, the transition geometry destabilizes and the system becomes incoherent.
```

---

# 8. Phase Change as a Transition Parameter

A phase change is not the whole state transition.

A phase change is one measurable parameter of a state transition.

Every transition contains a phase posture, whether or not the phase visibly changes at human resolution.

At sharper observational resolution, the same transition may decompose into smaller transitions, each with its own measurable phase parameter.

## Phase Change Parameter Principle

```text
Every state transition contains a measurable phase-change parameter.

This parameter describes whether the transitioning object, node, actor, claim, system, or state remains in the same phase, evolves, devolves, dissolves, replicates, specializes, or otherwise changes structural posture during the transition.
```

---

# 9. Evolve, Devolve, Dissolve

Prime Nodes can undergo phase movements.

These are structural terms, not moral terms.

```text
EVOLVE
DEVOLVE
DISSOLVE
```

## Evolve

```text
Evolve decreases filled node parameters and requires additional transition entropy.
```

Evolution means the node carries fewer internal parameters by relying on a more capable surrounding transition geometry.

It reduces internal clutter but increases dependency on routing, binding, receipt continuity, authority separation, and transition validation.

## Devolve

```text
Devolve increases node positions by no more than the initial total parameters, releasing surplus transition entropy.
```

Devolution does not mean regress.

In this model, devolve means to unpack a dense node into additional explicit node positions, bounded by the node’s initial total parameter count.

If:

```text
P0 = initial total node parameters
N = resulting node positions
```

Then:

```text
N <= P0
```

Devolution converts hidden internal complexity into visible node geometry.

## Dissolve

```text
Dissolve releases surplus transition entropy.
```

A node dissolves when its function no longer needs to remain as a distinct active node position.

Dissolution must be receipted.

A dissolved node must not remain as implied authority.

---

# 10. Transition Entropy

Transition entropy represents unresolved transition potential required to support state change, reconfiguration, branching, adaptation, decomposition, or closure.

Surplus transition entropy is released when complexity is unpacked, reduced, retired, dissolved, or made explicit.

## Entropy Accounting Rule

```text
Transition entropy must be accounted for during every node phase change.
```

Every evolve, devolve, or dissolve movement changes the transition geometry.

Therefore, every movement requires a receipt.

---

# 11. Moment-Bound Evaluation Principle

At the moment of evaluation, the system compares bounded values.

These values may be:

```text
hashes
booleans
counts
thresholds
timestamps
state labels
receipt IDs
authority flags
evidence bindings
entropy scores
phase parameters
risk classes
transition paths
```

## Principle

```text
A governed state transition is evaluated by comparing the required transition values against the observed transition values at a specific moment.

The transition result is valid only for the evaluated moment unless revalidated.
```

The system asks:

```text
At time t, do the observed values satisfy the required values for this transition?
```

If yes, the transition may proceed.

If no, the transition must refuse, pause, escalate, devolve, dissolve, reconfigure, or remain incomplete.

---

# 12. Hash-Scoped Node Execution

Hashes are cheap and concise.

A node should not interpret meaning first.

A node should execute on a declared hash range, hash class, or hash posture first.

## Hash-Scoped Node Execution Principle

```text
A Prime Node executes only within a declared hash scope.

Its hash scope defines the object hashes, receipt hashes, transition hashes, authority hashes, evidence hashes, policy hashes, and registry bindings it may evaluate.

Inputs outside that scope must be ignored, refused, rerouted, or escalated according to where failure occurs.

This preserves coherence while minimizing compute cost through cheap comparison before expensive interpretation.
```

---

# 13. Strict Hash-Match Non-Engagement

The stronger rule is that most transitions can be strictly ignored until the first match.

## Strict Hash-Match Non-Engagement Principle

```text
A Prime Node must not evaluate an incoming transition unless the transition first matches the node’s declared hash scope.

Non-matching transitions are ignored rather than refused, routed, interpreted, or receipted.

This prevents unnecessary computation and prevents the receipt space from being polluted by irrelevant non-actions.
```

The default node behavior is not refusal.

The default behavior is ignore.

Refusal occurs only when a node is addressed, matched, required, or activated but cannot proceed.

---

# 14. Ignore, Reroute, Refuse

These are distinct.

## Ignore

```text
This transition is outside my hash scope.
I do not engage.
No receipt required.
```

## Reroute

```text
This transition touched my scope enough to know another node is responsible.
Receipt may be required.
```

## Refuse

```text
This transition is within my scope, but required values are missing, invalid, stale, unauthorized, unsafe, or incoherent.
Receipt required.
```

---

# 15. Hash-Synergistic Routing

Routing does not occur because every node decides where data should go.

Routing occurs because data is ignored by incompatible nodes and activated only by compatible nodes.

## Hash-Synergistic Routing Principle

```text
Routing occurs when incoming data is ignored by all incompatible nodes and activated only by nodes whose declared hash scope matches the data’s receipt, transition, authority, evidence, policy, or state posture.

The data can only move in directions where it is not ignored, not refused, and not blocked by the Transition Table.
```

The data can only go certain directions.

---

# 16. Non-Ignored Path Principle

```text
A data object, receipt, claim, transition, or authority packet may only route through nodes that do not ignore its hash posture.

If no node activates, the data has no governed path.

If one node activates, the route is singular.

If multiple nodes activate, the route branches only along Transition Table-permitted paths.
```

## Routing Cases

```text
0 matches  → no governed route
1 match    → singular governed route
2+ matches → governed branch / distributed observation
```

## Routing Equation

```text
route_possible = hash_match AND receipt_sufficient AND transition_allowed
```

If any part fails, the system ignores, refuses, blocks, reroutes, escalates, or pauses depending on where failure occurs.

---

# 17. Selective Activation Compute Principle

The smaller the active routing set becomes, the more of the system remains available for unrelated transitions.

## Principle

```text
When a transition activates only the subset of nodes whose hash scope matches the data posture, all non-matching nodes remain computationally available.

A smaller set of possible directions preserves system-wide compute capacity while allowing the matched transition path to proceed with bounded resources.
```

Short form:

```text
Every ignored path is preserved capacity.
```

Another short form:

```text
Every node that ignores a transition remains available for another transition.
```

---

# 18. Compute Conservation

For a transition:

```text
C_total = C_active + C_available + C_released + C_blocked
```

Where:

```text
C_total     = total system compute/governance capacity
C_active    = capacity consumed by nodes that activate
C_available = capacity preserved by ignored nodes
C_released  = capacity or entropy released by devolution/dissolution
C_blocked   = load prevented from entering invalid paths
```

Compute cost should scale with activated nodes, not total nodes.

```text
compute cost ∝ activated nodes
not total nodes
```

---

# 19. Multi-Node Observation

A state transition may require several nodes in order to be observed.

No single node is required to observe the entire transition unless explicitly assigned.

The transition becomes coherent only when required node receipts are related, validated, and bound into a transition receipt.

## Multi-Node Observation Principle

```text
A state transition may require multiple Prime Nodes to observe different parameters of the same transition.

Coherent transition recognition occurs when the required node receipts are related, validated, and bound into a transition receipt.
```

---

# 20. State Transition Conservation Record

A transition conservation record should capture the following fields.

```yaml
state_transition_conservation:
  transition_id: null
  evaluated_at: null

  state:
    before: null
    after: null

  incoming_receipts:
    relationship_type: null
    required_posture: null
    received: []
    missing: []
    complete: false

  node_activation:
    total_nodes_available: 0
    activated_nodes: []
    ignored_nodes_count: 0
    refused_nodes: []
    routed_nodes: []
    escalated_nodes: []

  hash_scope:
    matched_hashes: []
    unmatched_hashes: []
    first_match: null
    activation_scope: null

  compute_conservation:
    estimated_total_capacity: null
    estimated_active_cost: null
    estimated_preserved_capacity: null
    estimated_released_capacity: null

  phase_parameter:
    phase_change_type: none
    phase_before: null
    phase_after: null

  entropy:
    transition_entropy_required: null
    transition_entropy_released: null
    surplus_transition_entropy: null

  authority:
    required: []
    bound: []
    status: null

  evidence:
    required: []
    bound: []
    status: null

  result:
    decision: null
    resulting_state: null
    receipt_id: null
    coherence_preserved: true
```

---

# 21. Transition Contract Schema

A reusable transition contract may look like this:

```yaml
transition_contract:
  object_id: null
  object_type: null

  current_state: null
  proposed_next_state: null

  transition_id: null
  transition_type: null

  actor:
    id: null
    type: null
    declared_authority: null

  incoming_receipts:
    required_posture: null
    receipt_hashes: []
    receipt_classes: []
    completeness_level: null

  hash_posture:
    object_hash: null
    object_hash_class: null
    transition_hash: null
    transition_hash_class: null
    authority_hashes: []
    evidence_hashes: []
    policy_hashes: []
    registry_status: null

  node_observation:
    required_nodes: []
    activated_nodes: []
    ignored_nodes_count: 0

  evidence:
    required: []
    provided: []
    status: unbound

  authority:
    required: []
    provided: []
    status: unbound

  phase_parameter:
    phase_before: null
    phase_after: null
    phase_change_type: none

  entropy:
    transition_entropy_required: null
    transition_entropy_released: null
    surplus_transition_entropy: null

  validation:
    status: pending
    result: null
    reason_codes: []

  output:
    resulting_state: null
    receipt_required: true
    receipt_id: null
```

---

# 22. Node Hash Contract Schema

Each node should declare what it is allowed to activate on.

```yaml
node_hash_contract:
  node_id: PN-002
  node_role: evidence_binding

  default_state: dormant

  executable_hash_scope:
    object_hash_classes:
      - repo_bundle
      - evidence_packet
      - source_manifest

    receipt_hash_classes:
      - state_observation_receipt
      - intake_receipt
      - source_binding_receipt

    transition_hash_classes:
      - submitted_to_evidence_bound
      - evidence_bound_to_review_pending

    authority_hash_classes: []

    evidence_hash_classes:
      - source_manifest_hash
      - evidence_packet_hash

    policy_hash_classes:
      - evidence_policy_hash

  no_match:
    action: IGNORE
    receipt_required: false
    compute_level: none

  match:
    action: ACTIVATE
    compute_level: minimal_header_comparison

  in_scope_valid:
    action: EVALUATE
    compute_level: bounded_value_comparison

  in_scope_invalid:
    action: REFUSE
    receipt_required: true

  out_of_scope_but_known:
    action: REROUTE
    receipt_required: true

  unknown_or_ambiguous:
    action: ESCALATE
    receipt_required: true
```

---

# 23. Routing Evaluation Schema

```yaml
routing_evaluation:
  data_posture:
    object_hash: null
    object_hash_class: null
    receipt_hashes: []
    transition_hash: null
    transition_hash_class: null
    authority_hashes: []
    evidence_hashes: []
    policy_hashes: []

  node_response:
    no_scope_match:
      action: IGNORE
      receipt_required: false

    scope_match:
      action: ACTIVATE
      receipt_required: maybe

    scope_match_but_invalid:
      action: REFUSE
      receipt_required: true

    scope_match_but_other_node_required:
      action: ROUTE
      receipt_required: true

    scope_match_but_observation_incomplete:
      action: ESCALATE
      receipt_required: true

    scope_match_and_valid:
      action: EVALUATE_OR_BIND
      receipt_required: true
```

---

# 24. Example Transition: Repo Cleanup Bundle

A repo cleanup bundle enters the system.

```yaml
object_type: repo_cleanup_bundle
current_state: SUBMITTED
proposed_next_state: EVIDENCE_BOUND
transition_type: bind_cleanup_evidence
```

PN-001 observes:

```text
Current state: SUBMITTED
```

PN-002 checks:

```text
Evidence exists:
- bundle manifest
- file list
- hash
- declared task
- source path
```

PN-003 checks:

```text
Authority required:
- repo governance authority
- cleanup policy authority
- ingestion authority
```

PN-004 validates:

```text
SUBMITTED -> EVIDENCE_BOUND is valid only if evidence and authority conditions are satisfied.
```

PN-005 refuses if required values are missing.

PN-006 receipts the result.

The transition may close only if the required conservation record is complete.

---

# 25. Closure Rule

The next implementation frontier is closure.

## Conservation Record Closure Rule

```text
A state transition closes when all required incoming receipt relationships, hash-scope matches, node observations, phase parameters, entropy accounting, authority bindings, evidence bindings, compute accounting, value comparisons, and resulting receipt requirements satisfy the Transition Table at the evaluated moment.
```

If the conservation record closes:

```text
transition may become the receipt basis for the next transition
```

If the conservation record does not close:

```text
transition is incomplete, refused, unstable, or incoherent
```

---

# 26. What Should Be Built Next

Do not build the full system yet.

Build the minimum files that allow the model to become testable.

Recommended first structure:

```text
prime-nodes/
  README.md
  registry.yaml

  transition-prime-nodes/
    README.md

    PN-001-state-observation/
      README.md
      node.yaml
      node_hash_contract.yaml
      transition_contract.schema.yaml
      example.receipt.yaml

    PN-002-evidence-binding/
      README.md
      node.yaml
      node_hash_contract.yaml
      transition_contract.schema.yaml
      example.receipt.yaml

    PN-003-authority-binding/
      README.md
      node.yaml
      node_hash_contract.yaml
      transition_contract.schema.yaml
      example.receipt.yaml

    PN-004-transition-validation/
      README.md
      node.yaml
      node_hash_contract.yaml
      transition_contract.schema.yaml
      example.receipt.yaml

    PN-005-refusal-block/
      README.md
      node.yaml
      node_hash_contract.yaml
      transition_contract.schema.yaml
      example.receipt.yaml

    PN-006-receipt-continuity/
      README.md
      node.yaml
      node_hash_contract.yaml
      transition_contract.schema.yaml
      example.receipt.yaml
```

---

# 27. Strategic Bottom Line

The State Transition Conservation Model defines StegVerse state transitions as receipt-conditioned, hash-scoped, node-observed, phase-parameterized, entropy-bearing, value-compared, compute-conserving, and receipt-producing events.

The cleanest statement is:

```text
Every state transition must close its conservation record before it can become the receipt basis for the next state transition.
```

The second cleanest statement is:

```text
Governed routing is the path of permitted non-ignorance.
```

The third cleanest statement is:

```text
Every ignored path is preserved capacity.
```

Together, these define a scalable governance model where the system grows without forcing every node to observe every transition.

StegVerse can therefore expand through Prime Nodes without becoming a noisy multi-agent swarm.

It becomes:

```text
dormant by default
hash-activated
receipt-conditioned
transition-table-bound
compute-conserving
coherence-preserving
```

---

# 28. Open Questions for v0.2

The next document or implementation pass should answer:

1. What exact fields are required for conservation record closure?
2. Which fields are mandatory for low-risk, medium-risk, high-risk, and irreversible transitions?
3. What is the minimum hash registry?
4. How are hash classes assigned?
5. What is the first executable Transition Table subset?
6. What constitutes transition entropy numerically?
7. What are the first node capacity thresholds?
8. What metrics prove compute preservation?
9. When does a node ignore versus reroute?
10. When does a matched node become required?
11. How are multi-node observations merged into one transition receipt?
12. How does MR decide whether a resulting receipt becomes master-record admissible?
13. How does DC preserve continuity across dissolved nodes?
14. How does RTG revalidate moment-bound transitions?
15. How does CGE enforce refusal when conservation closure fails?

---

## End State

This document freezes the v0.1 conceptual layer.

The next step is to create the first file bundle for the six Transition Prime Nodes and their registry.
