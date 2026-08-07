# STCM Whole-Repository Theory Map

Goal: `STCM-MATHEMATICAL-COMPLETENESS-002`

This adapter maps the existing `docs/STATE_TRANSITION_CONSERVATION_MODEL.md` into the organization-standard formal declaration, derivation, proof-candidate, and falsification surfaces. It does not replace the source theory, closure harness, dispatcher, or hosted validation evidence.

## Theory chain

1. A governed transition relates a prior state, incoming receipts, observed values, authority/evidence bindings, active and inactive node sets, phase/entropy posture, compute allocation, and a resulting receipt.
2. Receipt relationships and hash scope determine whether a node may participate.
3. Finite governed capacity bounds coherent node operation.
4. Hash-scope matching, receipt sufficiency, and transition permission jointly define route possibility.
5. Selective activation partitions transition-specific capacity into active, available, released, and blocked terms.
6. All required terms must close into a conservation record before the result can become the receipt basis for a subsequent governed transition.
7. Every result is moment-bound unless its required predicates are revalidated later.

## Canonical source anchors

- `docs/STATE_TRANSITION_CONSERVATION_MODEL.md` — foundational theory and equations.
- `closure-harness/completeness_policy.yaml` — bounded closure policy.
- `closure-harness/closure.py` — executable bounded closure predicate.
- `closure-harness/fixtures.py` — PN-001..PN-006 fixtures.
- `closure-harness/run_closure_harness.py` — deterministic closure runner.
- `reports/stcm-deterministic-validation-receipt.json` — bounded deterministic evidence.
- `.github/workflows/stcm-build.yml` — hosted regression validation.

## Standard formal layer

- `formalism/principle-registry.yaml` declares six source principles already present in the STCM theory.
- `formalism/dependency-graph.yaml` records how receipt relationships, hash scope, moment-bound values, capacity, routing, compute accounting, and conservation closure depend on one another.
- `formalism/proof-candidates.yaml` registers six bounded proof candidates. All remain `candidate_not_proven`.

## Mathematics layer

`docs/MATHEMATICAL_NOTATION.md` restates and derives the key STCM equations without adding a new source model: load/capacity threshold behavior, hash-scoped activation, route conjunction, compute partition, conservation closure, and time-indexed validity.

## Falsification layer

`docs/FALSIFICATION_AND_LIMITS.md` gives a concrete counterexample condition for every proof candidate and states the limits of bounded fixture saturation.

## Authority boundary

Mathematical completeness means the repository has an explicit, traceable, falsifiable formal model and proof candidates. It does not mean the candidates are proved, does not make SATURATED universal, and does not create execution, standing, publication, release, certification, AE-admissibility, or master-record authority.
