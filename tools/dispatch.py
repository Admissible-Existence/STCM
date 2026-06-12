"""dispatch.py — Stable Core-Lite dispatcher.

Reads tools/task_registry.yaml and runs each registered task (or one task if
ONLY_TASK is set). This is invoked by core-lite-intake.yml. Adding a feature
means registering a task, never adding a workflow file.

Exit code: 0 if every run task exited 0 (or task is non-fatal); 1 otherwise.
"""

from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "tools" / "task_registry.yaml"


def main() -> int:
    reg = yaml.safe_load(REGISTRY.read_text())
    only = os.environ.get("ONLY_TASK", "").strip()
    tasks = reg.get("tasks", [])
    if only:
        tasks = [t for t in tasks if t["id"] == only]
        if not tasks:
            print(f"no registered task with id={only!r}", file=sys.stderr)
            return 1

    overall = 0
    for t in tasks:
        entry = ROOT / t["entry"]
        print(f"\n=== dispatching task: {t['id']} ===", file=sys.stderr)
        proc = subprocess.run([sys.executable, str(entry)], cwd=str(ROOT))
        rc = proc.returncode
        fatal = t.get("fail_on_nonzero_exit", True)
        print(f"--- task {t['id']} exit={rc} fatal={fatal} ---", file=sys.stderr)
        if rc != 0 and fatal:
            overall = 1
    return overall


if __name__ == "__main__":
    raise SystemExit(main())
