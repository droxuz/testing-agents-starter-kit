"""Offline, self-contained regression checks. Run with Python from any directory.

The leading underscore keeps this file out of agent command discovery.
Synthetic tests are parsed/collected, never deliberately run against a solution.
"""

import ast
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parent
CONSTRAINTS = runpy.run_path(str(TOOLS / 'list_constraints'))
CHECKER = runpy.run_path(str(TOOLS / 'check_tests'))


def run_tool(name, spec, source, *args):
    with tempfile.TemporaryDirectory() as tmp:
        task = Path(tmp)
        (task / 'tests').mkdir()
        (task / 'SPEC.md').write_text(spec)
        (task / 'tests/test_cases.py').write_text(source)
        return subprocess.run([sys.executable, str(TOOLS / name), *args], cwd=task,
                              capture_output=True, text=True, timeout=20)


class ConstraintTests(unittest.TestCase):
    def test_strict_singleton_and_negative(self):
        bounds, _, _, _, conflict = CONSTRAINTS['analyze']('2 < n < 5\n1 <= x <= 1\n10 > y >= -2')
        self.assertFalse(conflict)
        self.assertEqual(bounds['n'], [3, 4])
        self.assertEqual(bounds['x'], [1, 1])
        self.assertEqual(bounds['y'], [-2, 9])

    def test_propagation(self):
        bounds, _, dependent, _, conflict = CONSTRAINTS['analyze']('1 <= l <= r <= 10^9\n1 <= n == a.length <= 5 * 10^4')
        self.assertFalse(conflict)
        self.assertTrue(dependent)
        self.assertEqual(bounds['l'], [1, 10**9])
        self.assertEqual(bounds['r'], [1, 10**9])
        self.assertEqual(bounds['n'], [1, 50000])

    def test_unparsed_and_conflicting(self):
        self.assertTrue(CONSTRAINTS['analyze']('5 <= n < 5')[-1])
        self.assertTrue(CONSTRAINTS['analyze']('0.1 <= p <= 0.9')[3])

    def test_cli_singleton(self):
        r = run_tool('list_constraints', '1 <= x <= 1', '')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('candidates: 1\n', r.stdout)


class InputTests(unittest.TestCase):
    def test_dependent_bounds(self):
        spec = 'Constraints:\n1 <= x <= k <= nums.length\n## Signature\ndef f(self, nums, k, x):\n'
        r = run_tool('check_inputs', spec, 'def test_one():\n assert Solution().f([1,2],1,2)==0\n')
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn('x <= k violated', r.stdout)

    def test_row_fields(self):
        spec = ('Constraints:\nrows[i] = [left, right, weight]\n1 <= left <= right <= 100\n'
                '1 <= weight <= 100\n## Signature\ndef f(self, rows):\n')
        r = run_tool('check_inputs', spec, 'def test_one():\n assert Solution().f([[0,2,0]])==0\n')
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn('left=0 outside', r.stdout)
        self.assertIn('weight=0 outside', r.stdout)

    def test_unknown_mutated_input(self):
        spec = 'Constraints:\n1 <= nums[i] <= 3\n## Signature\ndef f(self, nums):\n'
        r = run_tool('check_inputs', spec, 'def test_one():\n a=[1]\n a.append(0)\n assert Solution().f(a)==0\n')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('unresolved inputs: 1', r.stdout)

    def test_misspelled_constraint_unknown(self):
        spec = 'Constraints:\n1 <= itmes.length <= 10\n## Signature\ndef f(self, items):\n'
        r = run_tool('check_inputs', spec, 'def test_one():\n assert Solution().f([])==0\n')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('unresolved bound checks: 1', r.stdout)


class TestReviewTests(unittest.TestCase):
    def test_assertion_style(self):
        bad = ast.parse('class TestA:\n def test_one(self):\n  self.assertEqual(1,1)\n')
        good = ast.parse('class TestA(unittest.TestCase):\n def test_one(self):\n  self.assertEqual(1,1)\n')
        self.assertEqual(len(list(CHECKER['style_findings'](bad))), 1)
        self.assertEqual(list(CHECKER['style_findings'](good)), [])

    def test_custom_assertion_style(self):
        tree = ast.parse('class TestA:\n def assertEqual(self,a,b):\n  assert a==b\n def test_one(self):\n  self.assertEqual(1,1)\n')
        self.assertEqual(list(CHECKER['style_findings'](tree)), [])

    def test_contradiction_without_module_execution(self):
        source = ('raise RuntimeError("must not execute")\ndef test_a():\n assert Solution().f(1)==2\n'
                  'def test_b():\n sol=Solution()\n result=sol.f(x=1)\n assert result==3\n')
        r = run_tool('check_tests', 'def f(self,x):\n', source)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn('conflicting expected answers', r.stdout)
        self.assertNotIn('RuntimeError', r.stdout)

    def test_stateful_calls_skipped(self):
        tree = ast.parse('def test_one():\n sol=Solution()\n assert sol.f(1)==1\n assert sol.f(1)==2\n')
        self.assertEqual(len(list(CHECKER['literal_answers'](tree, 'f', ['x']))), 1)

    def test_budget_boundary_and_collection_only(self):
        for count in (25, 26):
            source = ('class Solution:\n def f(self,x):\n  raise RuntimeError("test bodies must not run")\n'
                      + ''.join(f'def test_{i}():\n assert Solution().f({i})=={i}\n' for i in range(count)))
            r = run_tool('check_tests', 'def f(self,x):\n', source)
            self.assertEqual(r.returncode, int(count > 25), r.stdout + r.stderr)
            self.assertEqual('BUDGET RISK' in r.stdout, count > 25)
            if count == 25:
                self.assertIn('Collected 25 tests', r.stdout)

    def test_syntax_delegated(self):
        r = run_tool('check_tests', 'def f(self,x):\n', 'def test_bad(:\n pass\n')
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn('syntax error', r.stdout)


if __name__ == '__main__':
    unittest.main()
