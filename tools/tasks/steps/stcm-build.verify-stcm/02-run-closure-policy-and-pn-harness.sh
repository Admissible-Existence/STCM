python -m py_compile closure-harness/closure.py closure-harness/fixtures.py closure-harness/run_closure_harness.py
python closure-harness/run_closure_harness.py
python -m json.tool dist/closure-harness-report.json >/dev/null
