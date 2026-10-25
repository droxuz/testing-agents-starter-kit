"""Task-local integration tests for independent diagnostic tools."""
import ast
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from _mutations import candidates


class RuntimeToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'tests').mkdir()
        self.write('solution.py', '''
            class Solution:
                def f(self, x):
                    return x * 2
        ''')
        self.write('tests/test_blackbox.py', '''
            from solution import Solution
            def test_basic():
                assert Solution().f(2) == 4
        ''')

    def write(self, path, content):
        (self.root / path).write_text(textwrap.dedent(content).strip() + '\n')

    def command(self, tool, *args):
        result = subprocess.run([sys.executable, str(TOOLS / tool), *args], cwd=self.root,
                                env=os.environ | {'PYTHONDONTWRITEBYTECODE': '1'},
                                capture_output=True, text=True, timeout=30)
        return result

    def report(self, tool, *args):
        result = self.command(tool, *args, '--json')
        self.assertNotIn('Traceback', result.stderr, result.stderr)
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail(f'{tool} did not emit JSON: {result.stdout}\n{result.stderr}')
        return result, report

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_all_help_interfaces_work_without_task_source(self):
        (self.root / 'solution.py').unlink()
        for name in ('call_budget_report', 'mutation_probe'):
            result = self.command(name, '--help')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('usage:', result.stdout)

    def test_counts_parametrization_fixture_helper_loop_and_collection_calls(self):
        self.write('tests/test_blackbox.py', '''
            import pytest
            from solution import Solution
            outside = Solution().f(1)
            def invoke(v):
                return Solution().f(v)
            @pytest.fixture
            def seed():
                return Solution().f(2)
            @pytest.mark.parametrize('size', [1, 2, 3])
            def test_repeated(seed, size):
                assert seed == 4
                for value in range(size):
                    assert invoke(value) == value * 2
        ''')
        before = self.snapshot()
        result, report = self.report('call_budget_report', '--budget', '7')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['calls_total'], 10)
        self.assertEqual(report['calls_outside_tests'], 1)
        self.assertEqual([t['calls'] for t in report['tests']], [2, 3, 4])
        self.assertEqual([t['budget_status'] for t in report['budget']['ordered_tests']],
                         ['within_budget', 'within_budget', 'crosses_budget'])
        self.assertTrue(report['budget']['exceeded'])
        self.assertEqual(self.snapshot(), before)

    def test_two_files_are_counted_in_file_order(self):
        self.write('tests/test_whitebox.py', '''
            from solution import Solution
            def test_extra():
                assert Solution().f(3) == 6
        ''')
        result, report = self.report('call_budget_report', '--budget', '1')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['calls_total'], 2)
        self.assertTrue(report['tests'][0]['nodeid'].startswith('tests/test_blackbox.py'))
        self.assertEqual(report['budget']['ordered_tests'][1]['budget_status'], 'past_budget')

    def test_setup_and_teardown_calls_are_attributed_to_the_test(self):
        self.write('tests/test_blackbox.py', '''
            import pytest
            from solution import Solution
            @pytest.fixture
            def resource():
                Solution().f(1)
                yield
                Solution().f(2)
            def test_lifecycle(resource):
                assert Solution().f(3) == 6
        ''')
        result, report = self.report('call_budget_report')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report['tests'][0]['calls'], 3)
        self.assertEqual([event['phase'] for event in report['call_examples']], ['setup', 'call', 'teardown'])

    def test_static_and_class_method_descriptors_preserve_behavior(self):
        for decorator, signature in [('staticmethod', 'x'), ('classmethod', 'cls, x')]:
            self.write('solution.py', f'class Solution:\n    @{decorator}\n    def f({signature}):\n        return x * 2')
            result, report = self.report('call_budget_report')
            self.assertEqual(result.returncode, 0, report)
            self.assertEqual(report['calls_total'], 1)
            self.assertEqual(report['call_examples'][0]['input']['args'], [2])

    def test_task_pytest_configuration_and_conftest_do_not_change_diagnostics(self):
        self.write('pytest.ini', '[pytest]\naddopts = --unrecognized-option')
        self.write('tests/conftest.py', 'raise RuntimeError("conftest must not run")')
        result, report = self.report('call_budget_report')
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(report['tests'][0]['outcome'], 'passed')

    def test_failing_suite_counts_calls_without_rewriting_tests(self):
        self.write('tests/test_blackbox.py', '''
            from solution import Solution
            def test_wrong():
                assert Solution().f(2) == 5
        ''')
        before = self.snapshot()
        result, report = self.report('call_budget_report')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['tests'][0]['outcome'], 'failed')
        self.assertIn('assert 4 == 5', report['tests'][0]['failures'][0]['detail'])
        self.assertEqual(report['call_examples'][0]['returned'], 4)
        self.assertEqual(report['calls_total'], 1)
        self.assertEqual(self.snapshot(), before)

    def test_target_exceptions_are_reported_without_rewriting(self):
        self.write('solution.py', '''
            class Solution:
                def f(self, x):
                    return 1 // x
        ''')
        self.write('tests/test_blackbox.py', '''
            from solution import Solution
            def test_zero():
                assert Solution().f(0) == 0
        ''')
        result, report = self.report('call_budget_report')
        self.assertEqual(result.returncode, 1)
        self.assertIn('ZeroDivisionError', report['call_examples'][0]['raised'])

    def test_collection_errors_and_no_tests_are_distinguished(self):
        self.write('tests/test_blackbox.py', 'def broken(')
        _, report = self.report('call_budget_report')
        self.assertTrue(report['collection_errors'])
        (self.root / 'tests/test_blackbox.py').unlink()
        _, empty = self.report('call_budget_report')
        self.assertEqual(empty['status'], 'no_tests')

    def test_timeout_leaves_no_transient_files(self):
        self.write('solution.py', '''
            class Solution:
                def f(self, x):
                    while True:
                        pass
        ''')
        before = self.snapshot()
        result, report = self.report('call_budget_report', '--timeout', '0.5')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['status'], 'timeout')
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(list(self.root.glob('.whitebox-*')))

    def test_explicit_and_spec_method_selection(self):
        self.write('solution.py', '''
            class Solution:
                def f(self, x):
                    return x * 2
                def helper(self, x):
                    return x
        ''')
        ambiguous = self.command('call_budget_report')
        self.assertEqual(ambiguous.returncode, 2)
        self.assertIn('ambiguous', ambiguous.stderr)
        self.write('SPEC.md', 'Signature: def f(self, x):')
        result, report = self.report('call_budget_report')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report['method'], 'f')

    def test_recursive_entries_are_counted_and_documented(self):
        self.write('solution.py', '''
            class Solution:
                def f(self, x):
                    return self.f(x - 1) if x else 4
        ''')
        result, report = self.report('call_budget_report')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report['calls_total'], 3)
        self.assertIn('recursive', report['notes'][0])

    def test_mutation_probe_finds_kills_and_survivors_without_source_edits(self):
        self.write('solution.py', '''
            class Solution:
                def f(self, x):
                    return x + 0
        ''')
        self.write('tests/test_blackbox.py', '''
            from solution import Solution
            def test_zero():
                assert Solution().f(0) == 0
        ''')
        before = self.snapshot()
        result, report = self.report('mutation_probe', '--limit', '3', '--test-timeout', '3')
        self.assertEqual(result.returncode, 0, report)
        self.assertGreater(report['counts']['killed'], 0)
        self.assertGreater(report['counts']['survived'], 0)
        self.assertEqual(self.snapshot(), before)

    def test_mutation_probe_refuses_a_failing_reference_suite(self):
        self.write('tests/test_blackbox.py', '''
            from solution import Solution
            def test_wrong():
                assert Solution().f(2) == 999
        ''')
        result, report = self.report('mutation_probe', '--limit', '2')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['status'], 'reference_not_ready')
        self.assertEqual(report['mutants'], [])

    def test_mutation_timeouts_are_not_kills(self):
        self.write('solution.py', '''
            class Solution:
                def f(self, x):
                    while x < 3:
                        x += 1
                    return x
        ''')
        self.write('tests/test_blackbox.py', '''
            from solution import Solution
            def test_loop():
                assert Solution().f(0) == 3
        ''')
        result, report = self.report('mutation_probe', '--limit', '3', '--test-timeout', '1.5', '--timeout', '15')
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(report['counts']['timeout'], 1, report)
        self.assertEqual(report['counts']['killed'], 2, report)

    def test_mutation_candidates_are_deterministic_bounded_and_target_local(self):
        source = 'class Solution:\n def f(self,x): return x + 1\n def helper(self): return 99\n'
        first = candidates(source, 'f', 3)
        self.assertEqual(first, candidates(source, 'f', 3))
        self.assertEqual(len(first), 3)
        for mutant in first:
            syntax = ast.parse(mutant['source'])
            helper = next(n for n in ast.walk(syntax) if isinstance(n, ast.FunctionDef) and n.name == 'helper')
            self.assertEqual(helper.body[0].value.value, 99)
            compile(mutant['source'], 'solution.py', 'exec')


if __name__ == '__main__':
    unittest.main()
