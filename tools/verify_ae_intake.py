#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "integration" / "admissible-existence-intake.json"
OUT = ROOT / "dist" / "ae-intake-result.json"
REQUIRED = [
    "Admissible-Existence/RTG",
    "Admissible-Existence/IICT",
    "Admissible-Existence/DC"
]


def main():
    data = json.loads(INTAKE.read_text(encoding="utf-8"))
    sources = data.get("source_repositories", [])
    missing = [item for item in REQUIRED if item not in sources]
    ok = not missing
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"intake_id": data.get("intake_id"), "result": "PASS" if ok else "FAIL", "missing": missing}, indent=2) + "\n", encoding="utf-8")
    if ok:
        print("PASS AE intake")
        return 0
    print("FAIL AE intake", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
