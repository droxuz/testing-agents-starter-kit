"""Internal pytest process for mutation_report; not an agent tool."""
import json
import sys
from pathlib import Path

import pytest

target = str(Path("solution.py").resolve())


class Results:
    def __init__(self):
        self.current = None
        self.calls = {}
        self.outcomes = {}
        self.order = []
        self.collection_error = False

    def profile(self, frame, event, arg):
        if event != "call" or frame.f_code.co_filename != target or frame.f_code.co_name == "<module>":
            return
        caller = frame.f_back
        if caller is None or caller.f_code.co_filename != target:
            self.calls[self.current] = self.calls.get(self.current, 0) + 1

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        self.current = item.nodeid
        self.order.append(item.nodeid)

    def pytest_runtest_logfinish(self, nodeid, location):
        self.current = None

    def pytest_runtest_logreport(self, report):
        if report.failed:
            self.outcomes[report.nodeid] = "failed"
        elif report.skipped:
            self.outcomes.setdefault(report.nodeid, "skipped")
        elif report.when == "call" and report.passed:
            self.outcomes.setdefault(report.nodeid, "passed")

    def pytest_collectreport(self, report):
        self.collection_error |= report.failed


results = Results()
selection = json.loads(Path("_selection.json").read_text())
sys.path.insert(0, str(Path.cwd()))
sys.setprofile(results.profile)
code = 3
try:
    code = pytest.main(
        ["-q", "--tb=no", "--no-header", "-p", "no:cacheprovider", "-c", "pytest.ini",
         *(selection or ["tests"])],
        plugins=[results],
    )
finally:
    sys.setprofile(None)
    Path("_outcomes.json").write_text(json.dumps({
        "exit_code": int(code),
        "collection_error": results.collection_error,
        "outside_calls": results.calls.get(None, 0),
        "tests": [{"id": node, "status": results.outcomes.get(node, "error"),
                   "calls": results.calls.get(node, 0)} for node in results.order],
    }))
