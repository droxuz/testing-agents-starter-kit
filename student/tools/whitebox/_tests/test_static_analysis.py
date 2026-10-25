"""Development checks for static guidance; these do not measure bug-detection gains."""
import ast
import itertools
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from boundary_values import UNKNOWN, boundary_hint, literal
from discover_conditions import analyze, conditions, discover
from mcdc_targets import evaluate, plan


def targets(source):
    return discover(ast.parse(textwrap.dedent(source).strip() + '\n'))


class DiscoveryTests(unittest.TestCase):
    def test_guards_preserve_negation_and_short_circuit_order(self):
        result = analyze(ast.parse('not a and (b or c)', mode='eval').body)
        self.assertEqual([text for text, _ in result.rows], ['a', 'b', 'c'])
        self.assertEqual(result.atoms[0].guard, '')
        for a, b in itertools.product((False, True), repeat=2):
            env = {'C1': a, 'C2': b}
            self.assertEqual(bool(eval(result.atoms[1].guard, {}, env)), not a)
            self.assertEqual(bool(eval(result.atoms[2].guard, {}, env)), not a and not b)

    def test_structures_match_python_truth_for_nested_expressions(self):
        expressions = ('a and (b or not c)', 'not (a or b) and c',
                       '(a or b) and (c or d)', 'a < b <= c',
                       'not (a == b) or c', 'a and a', '(a and b) or a')
        for expression in expressions:
            syntax = ast.parse(expression, mode='eval').body
            names = sorted({node.id for node in ast.walk(syntax) if isinstance(node, ast.Name)})
            result = analyze(syntax)
            for bits in itertools.product((False, True), repeat=len(names)):
                env = dict(zip(names, bits))
                values = tuple(bool(eval(text, {}, env)) for text, _ in result.rows)
                actual, _ = evaluate(ast.parse(result.structure, mode='eval').body, values)
                self.assertEqual(actual, bool(eval(expression, {}, env)), (expression, bits))

    def test_chained_operand_is_aliased_once_without_mutating_source(self):
        source = ast.parse('0 < next_value() < 10', mode='eval').body
        original = ast.dump(source, include_attributes=True)
        result = analyze(source)
        self.assertEqual(len(result.aliases), 1)
        self.assertEqual([ast.unparse(result.display_node(atom.node)) for atom in result.atoms],
                         ['0 < V1', 'V1 < 10'])
        self.assertTrue(result.atoms[0].potential_effects)
        self.assertFalse(result.atoms[1].potential_effects)
        self.assertEqual(ast.dump(source, include_attributes=True), original)

    def test_repeated_and_reversed_scalar_conditions_are_flagged(self):
        result = analyze(ast.parse('x > 0 and x > 0 and 0 < x', mode='eval').body)
        self.assertEqual(result.atoms[1].repeat_of, 1)
        self.assertEqual(result.atoms[2].equivalent_to, 1)

    def test_early_return_adds_false_snapshot_for_later_target(self):
        found = targets('''
            def f(x):
                if x < 0:
                    return 0
                if x > 3:
                    return 1
        ''')
        second = next(target for target in found if ast.unparse(target.test) == 'x > 3')
        self.assertEqual([(reach.text, reach.outcome) for reach in second.reached_if],
                         [('x < 0', False)])

    def test_unconditional_exit_marks_later_expression_unreachable(self):
        found = targets('''
            def f(x):
                return x
                if x > 0:
                    pass
        ''')
        self.assertTrue(found[0].unreachable)

    def test_return_comprehension_match_and_nested_contexts_are_discovered(self):
        found = targets('''
            def f(values, x):
                if values:
                    selected = [v for v in values if v > 0]
                match x:
                    case int() if x > 2:
                        pass
                return x > 0 and bool(values)
        ''')
        self.assertTrue({'if', 'comp-if', 'match-guard', 'return'} <= {t.kind for t in found})
        selected = next(t for t in found if t.kind == 'comp-if')
        self.assertTrue(any(r.text == 'values' and r.outcome is True for r in selected.reached_if))
        self.assertTrue(any(r.outcome is None for r in selected.reached_if))

    def test_same_line_targets_have_distinct_identifiers(self):
        found = targets('def f(x):\n    return (x > 0) if x else (x < 0)')
        self.assertEqual(len(found), 3)
        self.assertEqual(len({t.target_id for t in found}), 3)

    def test_legacy_conditions_interface_retains_outer_guard(self):
        rows = []
        structure = conditions(ast.parse('a or b', mode='eval').body, rows, 'outer')
        self.assertEqual(len(rows), 2)
        self.assertIn('C2', structure)
        self.assertEqual(rows[0], ('a', 'outer'))
        self.assertIn('outer', rows[1][1])


class BoundaryTests(unittest.TestCase):
    def test_integer_truth_tables_follow_each_comparison_operator(self):
        checks = {'<': (True, False, False), '<=': (True, True, False),
                  '>': (False, False, True), '>=': (False, True, True),
                  '==': (False, True, False), '!=': (True, False, True)}
        for operator, expected in checks.items():
            hint = boundary_hint(f'x {operator} 3')
            self.assertEqual(re.findall(r'(-?\d+)=>([TF])', hint),
                             [(str(value), 'T' if truth else 'F')
                              for value, truth in zip((2, 3, 4), expected)])

    def test_reversed_comparison_and_nonnegative_length(self):
        self.assertEqual(boundary_hint('3 < x'), boundary_hint('x > 3'))
        self.assertNotIn('-1=>', boundary_hint('len(xs) == 0'))
        self.assertIn('0=>T', boundary_hint('len(xs) == 0'))

    def test_float_and_boolean_boundaries_are_not_integer_steps(self):
        self.assertIn('suitable numeric step', boundary_hint('x < 1.5'))
        self.assertNotIn('integer targets', boundary_hint('flag == True'))

    def test_dynamic_membership_and_identity_have_distinct_guidance(self):
        self.assertIn('hold boundary expression stable', boundary_hint('total >= threshold'))
        self.assertIn('member and a nonmember', boundary_hint('x in values'))
        self.assertIn('same object', boundary_hint('x is other'))

    def test_literal_helper_does_not_execute_calls(self):
        self.assertIs(literal(ast.parse('danger()', mode='eval').body), UNKNOWN)


class MCDCTests(unittest.TestCase):
    def test_short_circuit_traces_match_evaluation(self):
        syntax = ast.parse('C1 and (C2 or C3)', mode='eval').body
        for bits, expected in [((False, True, True), (False, 'F--')),
                               ((True, True, False), (True, 'TT-')),
                               ((True, False, True), (True, 'TFT')),
                               ((True, False, False), (False, 'TFF'))]:
            self.assertEqual(evaluate(syntax, bits), expected)

    def test_every_reported_pair_independently_changes_the_abstract_decision(self):
        for text in ('a and b', 'a or b', 'a and (b or c)', 'not (a or b) and c'):
            result = analyze(ast.parse(text, mode='eval').body)
            model, selected, pairs, _ = plan(result.structure, result.rows)
            self.assertEqual(len(pairs), len(result.atoms))
            for index, (first, second) in pairs.items():
                self.assertEqual([i for i in range(len(first)) if first[i] != second[i]], [index])
                self.assertNotEqual(model[first][0], model[second][0])
                self.assertNotEqual(model[first][1][index], '-')
                self.assertNotEqual(model[second][1][index], '-')
                self.assertIn(first, selected)
                self.assertIn(second, selected)

    def test_constant_and_repeated_atoms_are_not_claimed_independent(self):
        for text in ('False and a', 'True or a', 'a and a'):
            result = analyze(ast.parse(text, mode='eval').body)
            _, _, pairs, notes = plan(result.structure, result.rows)
            self.assertFalse(pairs)
            self.assertTrue(notes)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.source = self.workspace / 'solution.py'
        self.source.write_text('raise RuntimeError("source must not execute")\n'
                               'def f(x):\n    return (x > 0) if x else (x < 0)\n')

    def command(self, name, *args):
        return subprocess.run([sys.executable, str(TOOLS / name), *args],
                              cwd=self.workspace, text=True, capture_output=True, timeout=10)

    def test_each_cli_works_standalone_and_never_executes_source(self):
        for name in ('discover_conditions.py', 'boundary_values.py', 'mcdc_targets.py'):
            result = self.command(name, '--line', '3', '--limit', '10')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('f@3:', result.stdout)
            self.assertEqual(list(self.workspace.iterdir()), [self.source])

    def test_help_succeeds_without_source(self):
        self.source.unlink()
        for name in ('discover_conditions.py', 'boundary_values.py', 'mcdc_targets.py'):
            result = self.command(name, '--help')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('--target', result.stdout)

    def test_exact_id_and_column_select_same_expression(self):
        found = targets(self.source.read_text())
        target = next(t for t in found if ast.unparse(t.test) == 'x > 0')
        for name in ('discover_conditions.py', 'boundary_values.py', 'mcdc_targets.py'):
            selected = self.command(name, '--target', target.target_id)
            by_position = self.command(name, '--line', str(target.lineno), '--column', str(target.col_offset))
            self.assertEqual(selected.returncode, 0, selected.stderr)
            self.assertEqual(selected.stdout, by_position.stdout)
            self.assertEqual(sum(line.startswith('f@') for line in selected.stdout.splitlines()), 1)

    def test_invalid_options_and_outside_source_are_rejected(self):
        for name in ('discover_conditions.py', 'boundary_values.py', 'mcdc_targets.py'):
            for args in (('--column', '1'), ('--limit', '0'), ('--line', '0'),
                         ('--target', 'f@3:12', '--line', '3'), (str(TOOLS / name),)):
                result = self.command(name, *args)
                self.assertNotEqual(result.returncode, 0, (name, args))
                self.assertNotIn('Traceback', result.stderr)

    def test_enumeration_is_bounded(self):
        self.source.write_text('def f(a,b,c,d,e,f,g,h,i):\n    return a and b and c and d and e and f and g and h and i\n')
        result = self.command('mcdc_targets.py', '--max-atoms', '8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('exceeds --max-atoms 8', result.stdout)
        rejected = self.command('mcdc_targets.py', '--max-atoms', '9')
        self.assertNotEqual(rejected.returncode, 0)


if __name__ == '__main__':
    unittest.main()
