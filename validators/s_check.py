#!/usr/bin/env python3

import json
from pathlib import Path
from s_fixtures import FIXTURES

REPORT = Path('reports/s_check.json')
FLAGS = ['readme_present', 'task_registry_present', 'existing_harness_present', 'closure_surface_present']


def classify(r):
    if not isinstance(r.get('ready'), bool):
        return 'BLOCKED'
    if any(not isinstance(r.get(f), bool) for f in FLAGS):
        return 'BLOCKED'
    ok = all(r[f] for f in FLAGS)
    if ok and r.get('status') == 'READY' and r.get('ready'):
        return 'READY'
    if (not ok) and r.get('status') == 'INCOMPLETE' and not r.get('ready'):
        return 'INCOMPLETE'
    return 'BLOCKED'


def main():
    rows = []
    unexpected = 0
    for item in FIXTURES:
        actual = classify(item['record'])
        expected = item['expected']
        ok = actual == expected
        rows.append({'id': item['id'], 'expected': expected, 'actual': actual, 'ok': ok})
        if not ok:
            unexpected += 1
    report = {'stage': 's_check', 'boundary': 'stcm_core_lite_v0_1', 'row_count': len(rows), 'unexpected': unexpected, 'saturated': unexpected == 0, 'rows': rows}
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report['saturated'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
