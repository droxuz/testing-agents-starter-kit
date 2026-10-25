"""Offline checks: python -m unittest discover -s student/tools/whitebox -p _test_mutation_report.py"""
import ast
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).with_name("mutation_report").resolve()
BOUNDARY = """class Solution:
    def f(self, x):
        if x <= 4:
            return 1
        return 0
"""


class MutationReportTests(unittest.TestCase):
    def task(self, source, blackbox, whitebox=""):
        temporary = tempfile.TemporaryDirectory(prefix=".mutation-test-", dir=Path.cwd())
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "tests").mkdir()
        (root / "solution.py").write_text(source, encoding="utf-8")
        (root / "tests/test_blackbox.py").write_text(blackbox, encoding="utf-8")
        if whitebox:
            (root / "tests/test_whitebox.py").write_text(whitebox, encoding="utf-8")
        return root

    def invoke(self, root, *args):
        result = subprocess.run(
            [sys.executable, str(TOOL), *args], cwd=root, capture_output=True,
            text=True, timeout=45,
        )
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_boundary_survivor_then_verified_kill(self):
        root = self.task(BOUNDARY, """from solution import Solution
def test_existing():
    assert Solution().f(1) == 1
    assert Solution().f(5) == 0
""")
        source = (root / "solution.py").read_bytes()
        blackbox = (root / "tests/test_blackbox.py").read_bytes()
        _, before = self.invoke(root, "--limit", "2")
        self.assertEqual(before["baseline"]["calls"], 2)
        self.assertEqual(before["remaining"][0]["id"], "M1")
        self.assertEqual(before["remaining"][0]["status"], "survived")
        self.assertIn("M2", before["killed"])
        _, focused = self.invoke(root, "--offset", "1", "--limit", "1")
        self.assertEqual(focused["killed"], ["M2"])
        (root / "tests/test_whitebox.py").write_text(
            "from solution import Solution\n"
            "def test_boundary():\n    assert Solution().f(4) == 1\n",
            encoding="utf-8",
        )
        _, after = self.invoke(root, "--limit", "2")
        self.assertEqual(set(after["killed"]), {"M1", "M2"})
        self.assertEqual((root / "solution.py").read_bytes(), source)
        self.assertEqual((root / "tests/test_blackbox.py").read_bytes(), blackbox)
        self.assertFalse(list(root.glob(".mutation-*")))

    def test_original_failures_never_create_kills(self):
        root = self.task("class Solution:\n    def f(self, x):\n        return x + 1\n",
                         "from solution import Solution\n"
                         "def test_wrong():\n    assert Solution().f(2) == 99\n")
        _, report = self.invoke(root)
        self.assertEqual(report["baseline"]["failed_count"], 1)
        self.assertEqual(report["baseline"]["eligible_tests"], 0)
        self.assertEqual(report["killed"], [])
        self.assertEqual(report["sampled"], 0)

    def test_actual_call_budget_includes_loops_and_parametrization(self):
        root = self.task(
            "class Solution:\n    def f(self, x):\n        return x + 1\n",
            """import pytest
from solution import Solution
@pytest.mark.parametrize("x", [0, 1, 2])
def test_parameter(x):
    assert Solution().f(x) == x + 1
""", """from solution import Solution
def test_loop():
    for x in range(3):
        assert Solution().f(x) == x + 1
""")
        code, report = self.invoke(root, "--limit", "0", "--max-calls", "4")
        self.assertEqual(code, 1)
        self.assertEqual(report["baseline"]["calls"], 6)
        self.assertTrue(report["baseline"]["over_budget"])
        self.assertEqual(report["baseline"]["tests_over_budget"], 1)
        self.assertEqual(report["baseline"]["eligible_tests"], 3)

    def test_failed_tests_spend_budget_before_valid_tests(self):
        root = self.task(
            "class Solution:\n    def f(self, x):\n        return x + 1\n",
            "from solution import Solution\n"
            "def test_wrong():\n    assert Solution().f(2) == 99\n",
            "from solution import Solution\n"
            "def test_valid():\n    assert Solution().f(2) == 3\n",
        )
        _, report = self.invoke(root, "--max-calls", "1")
        self.assertEqual(report["baseline"]["eligible_tests"], 0)
        self.assertEqual(report["baseline"]["tests_over_budget"], 1)
        self.assertEqual(report["killed"], [])

    def test_timeout_is_inconclusive(self):
        root = self.task("""class Solution:
    def f(self, x):
        while x <= 1:
            x += 1
        return x
""", "from solution import Solution\n"
     "def test_one():\n    assert Solution().f(1) == 2\n")
        _, report = self.invoke(root, "--line", "3", "--limit", "2", "--timeout", "1.5")
        survivor = next(row for row in report["remaining"] if row["id"] == "M2")
        self.assertEqual(survivor["status"], "timeout")
        self.assertNotIn("M2", report["killed"])

    def test_collection_error_does_not_measure_mutants(self):
        root = self.task(BOUNDARY, "def test_broken(\n")
        code, report = self.invoke(root)
        self.assertEqual(code, 1)
        self.assertIn("original run error", report["error"])
        self.assertNotIn("killed", report)

    def test_internal_recursion_counts_as_one_external_call(self):
        root = self.task("""class Solution:
    def f(self, x):
        return 0 if x == 0 else self.f(x - 1) + 1
""", "from solution import Solution\n"
     "def test_recursive():\n    assert Solution().f(3) == 3\n")
        _, report = self.invoke(root, "--limit", "0")
        self.assertEqual(report["baseline"]["calls"], 1)

    def test_mutation_restores_tree_and_ids(self):
        namespace = runpy.run_path(str(TOOL))
        tree = ast.parse(BOUNDARY)
        original = ast.dump(tree)
        choices = list(namespace["candidates"](tree))
        for _, node, index, replacement in choices:
            before, after, mutated = namespace["change"](tree, node, index, replacement)
            self.assertNotEqual(before, after)
            ast.parse(mutated)
            self.assertEqual(ast.dump(tree), original)
        self.assertEqual([c[0] for c in choices],
                         [c[0] for c in namespace["candidates"](tree)])

    def test_help_needs_no_task_files(self):
        with tempfile.TemporaryDirectory(prefix=".mutation-help-", dir=Path.cwd()) as root:
            result = subprocess.run([sys.executable, str(TOOL), "--help"], cwd=root,
                                    capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--limit", result.stdout)


if __name__ == "__main__":
    unittest.main()
