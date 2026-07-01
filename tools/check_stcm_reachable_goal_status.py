from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "docs" / "STCM_REACHABLE_GOAL_STATUS.md"
required_files = [
    "README.md",
    "closure-harness/task.yaml",
    "closure-harness/closure.py",
    "closure-harness/completeness_policy.yaml",
    "closure-harness/fixtures.py",
    "closure-harness/run_closure_harness.py",
]
required_terms = [
    "repo: STCM",
    "workstream: closure-harness",
    "reachable_goal: local_closure_harness_installed",
    "state: ready",
    "manual_tasks_remaining: false",
    "release_candidate: false",
    "creates_workflow: false",
    "closure_predicate: ready",
    "fixtures: ready",
    "runner: ready",
    "status_record_only: true",
    "creates_authority: false",
    "commits_execution: false",
    "claims_final_cross_repo_validity: false",
]
ok = path.exists() and all((ROOT / rel).exists() for rel in required_files)
if ok:
    text = path.read_text(encoding="utf-8")
    for term in required_terms:
        if term not in text:
            print(f"missing: {term}")
            ok = False
else:
    print("missing STCM status or required closure-harness files")
print("valid: STCM reachable goal status" if ok else "STCM reachable goal status check failed")
raise SystemExit(0 if ok else 1)
