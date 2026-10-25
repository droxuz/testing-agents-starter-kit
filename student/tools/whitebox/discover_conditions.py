#!/usr/bin/env python3
"""Discover expressions, local guards and structural reach hints; no execution.
Columns are zero-based UTF-8 offsets. Flags are conservative, not proofs.
"""
import argparse
import ast
import copy
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Reach:
    text: str
    lineno: int
    column: int
    outcome: object = None

    @classmethod
    def test(cls, expression, outcome):
        return cls(ast.unparse(expression), expression.lineno,
                   expression.col_offset, outcome)

    def short(self):
        if self.outcome is None:
            return self.text
        return f'L{self.lineno}:{self.column}={"T" if self.outcome else "F"}'


@dataclass
class Decision:
    test: ast.AST
    kind: str
    function: str
    owner_lineno: int
    reached_if: tuple = ()
    notes: tuple = ()
    unreachable: bool = False

    @property
    def lineno(self):
        return self.test.lineno

    @property
    def col_offset(self):
        return self.test.col_offset

    @property
    def end_lineno(self):
        return getattr(self.test, 'end_lineno', self.lineno)

    @property
    def end_col_offset(self):
        return getattr(self.test, 'end_col_offset', self.col_offset)

    @property
    def target_id(self):
        return f'{self.function}@{self.lineno}:{self.col_offset}'


@dataclass
class Atom:
    node: ast.AST
    guard: str
    potential_effects: bool
    may_raise: bool
    repeat_of: object = None
    equivalent_to: object = None
    normalized_key: str = ''
    shared_operands: tuple = ()


@dataclass
class Analysis:
    structure: str
    atoms: list
    aliases: dict = field(default_factory=dict)

    @property
    def rows(self):
        return [(ast.unparse(atom.node), atom.guard) for atom in self.atoms]

    def display_node(self, node):
        """Clone syntax for display; never mutate or evaluate source expressions."""
        aliases = self.aliases

        def clone(part):
            if id(part) in aliases:
                return ast.copy_location(ast.Name(id=aliases[id(part)][0], ctx=ast.Load()), part)
            result = copy.copy(part)
            for name, value in ast.iter_fields(part):
                if isinstance(value, ast.AST):
                    setattr(result, name, clone(value))
                elif isinstance(value, list):
                    setattr(result, name, [clone(item) if isinstance(item, ast.AST) else item
                                          for item in value])
            return result
        return clone(node)


def format_logic(text):
    return ast.unparse(ast.parse(text, mode='eval').body)


def guarded_by(guard, requirement):
    return f'({guard}) and ({requirement})' if guard else requirement


def risks(nodes):
    parts = [part for node in nodes for part in ast.walk(node)]
    effects = any(isinstance(part, (ast.NamedExpr, ast.Call, ast.Await,
                                   ast.Yield, ast.YieldFrom, ast.Attribute, ast.Subscript))
                  for part in parts)
    raises = any(isinstance(part, (ast.Call, ast.Await, ast.Yield, ast.YieldFrom,
                                  ast.Subscript, ast.Attribute))
                 or isinstance(part, ast.BinOp) and isinstance(part.op, (ast.Div, ast.FloorDiv, ast.Mod))
                 for part in parts)
    return effects, raises


def normalized_key(node):
    """A scalar-equivalence hint, not a general symbolic simplifier."""
    reverse = {ast.Lt: ast.Gt, ast.LtE: ast.GtE, ast.Gt: ast.Lt,
               ast.GtE: ast.LtE, ast.Eq: ast.Eq, ast.NotEq: ast.NotEq}
    result = node
    if isinstance(node, ast.Compare) and len(node.ops) == 1:
        left, right, op = node.left, node.comparators[0], type(node.ops[0])
        try:
            value = ast.literal_eval(left)
        except (ValueError, TypeError, SyntaxError, RecursionError):
            value = object()
        if isinstance(right, ast.Name) and type(value) in (int, float, str, bool, type(None)) and op in reverse:
            result = ast.Compare(left=right, ops=[reverse[op]()], comparators=[left])
    return ast.dump(result, include_attributes=False)


def analyze(expression):
    atoms, aliases = [], {}

    def append(node, guard, evaluated_nodes=None):
        effects, raises = risks([node] if evaluated_nodes is None else evaluated_nodes)
        atoms.append(Atom(node, guard, effects, raises))
        return f'C{len(atoms)}'

    def visit(node, guard=''):
        if isinstance(node, ast.BoolOp):
            parts = []
            for child in node.values:
                part = visit(child, guard)
                parts.append(part)
                requirement = part if isinstance(node.op, ast.And) else f'not ({part})'
                guard = guarded_by(guard, requirement)
            operator = ' and ' if isinstance(node.op, ast.And) else ' or '
            return '(' + operator.join(parts) + ')'
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return f'not ({visit(node.operand, guard)})'
        if isinstance(node, ast.Compare):
            operands = [node.left, *node.comparators]
            for middle in operands[1:-1]:
                if id(middle) not in aliases:
                    aliases[id(middle)] = (f'V{len(aliases) + 1}', middle)
            parts = []
            for index, operator in enumerate(node.ops):
                pair = ast.copy_location(ast.Compare(left=operands[index], ops=[operator],
                                                     comparators=[operands[index + 1]]), node)
                # Later comparisons reuse the previously computed left operand.
                evaluated = operands[index:index + 2] if index == 0 else [operands[index + 1]]
                part = append(pair, guard, evaluated)
                parts.append(part)
                guard = guarded_by(guard, part)
            return '(' + ' and '.join(parts) + ')' if len(parts) > 1 else parts[0]
        return append(node, guard)

    structure = visit(expression)
    texts, keys = {}, {}
    for index, atom in enumerate(atoms, 1):
        text = ast.unparse(atom.node)
        atom.normalized_key = normalized_key(atom.node)
        atom.shared_operands = tuple(dict.fromkeys(aliases[id(part)][0] for part in ast.walk(atom.node) if id(part) in aliases))
        if text in texts:
            atom.repeat_of = texts[text]
        elif atom.normalized_key in keys:
            atom.equivalent_to = keys[atom.normalized_key]
        texts.setdefault(text, index)
        keys.setdefault(atom.normalized_key, index)
    return Analysis(structure, atoms, aliases)


def conditions(node, rows, guard=''):
    """Compatibility API: original condition text plus local evaluation guards."""
    result = analyze(node)
    for text, local_guard in result.rows:
        rows.append((text, guarded_by(guard, local_guard) if guard and local_guard else guard or local_guard))
    return result.structure


def _ends(block):
    for node in block:
        if isinstance(node, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
            return True
        if isinstance(node, ast.If) and _ends(node.body) and _ends(node.orelse):
            return True
    return False


def _has_local_exit(node, loop_depth=0):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
        return False
    if isinstance(node, (ast.Return, ast.Raise)):
        return True
    if isinstance(node, (ast.Break, ast.Continue)):
        return loop_depth == 0
    if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
        loop_depth += 1
    return any(_has_local_exit(child, loop_depth) for child in ast.iter_child_nodes(node))


def _continuation_requirements(node):
    """Necessary snapshots for a simple if/elif chain to fall through."""
    left, right = _ends(node.body), _ends(node.orelse)
    if left and not right:
        requirements = (Reach.test(node.test, False),)
        if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            requirements += _continuation_requirements(node.orelse[0])
        return requirements
    if right and not left:
        return (Reach.test(node.test, True),)
    return ()


class Discovery:
    """Lexical contexts plus simple early exits; not a complete CFG/dataflow solver."""
    def __init__(self):
        self.targets = []
        self.seen = set()

    def add(self, expression, kind, scope, reach, notes, unreachable, owner=None):
        if id(expression) not in self.seen:
            self.seen.add(id(expression))
            self.targets.append(Decision(expression, kind, '.'.join(scope) or '<module>',
                                         getattr(owner, 'lineno', expression.lineno),
                                         reach, notes, unreachable))

    def expr(self, node, scope, reach=(), notes=(), unreachable=False, kind='value', covered=False):
        if node is None:
            return
        if isinstance(node, ast.BoolOp):
            if not covered:
                self.add(node, kind, scope, reach, notes, unreachable)
            for child in node.values:
                self.expr(child, scope, reach, notes, unreachable, kind, True)
                reach += (Reach.test(child, isinstance(node.op, ast.And)),)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            if not covered:
                self.add(node, kind, scope, reach, notes, unreachable)
            self.expr(node.operand, scope, reach, notes, unreachable, kind, True)
        elif isinstance(node, ast.Compare):
            if not covered:
                self.add(node, kind, scope, reach, notes, unreachable)
            operands = [node.left, *node.comparators]
            self.expr(operands[0], scope, reach, notes, unreachable)
            for index, operand in enumerate(operands[1:]):
                self.expr(operand, scope, reach, notes, unreachable)
                pair = ast.copy_location(ast.Compare(left=operands[index], ops=[node.ops[index]],
                                                     comparators=[operand]), node)
                reach += (Reach.test(pair, True),)
        elif isinstance(node, ast.IfExp):
            self.add(node.test, 'ifexp', scope, reach, notes, unreachable, node)
            self.expr(node.test, scope, reach, notes, unreachable, covered=True)
            self.expr(node.body, scope, reach + (Reach.test(node.test, True),), notes, unreachable, kind)
            self.expr(node.orelse, scope, reach + (Reach.test(node.test, False),), notes, unreachable, kind)
        elif isinstance(node, ast.Lambda):
            for default in [*node.args.defaults, *node.args.kw_defaults]:
                self.expr(default, scope, reach, notes, unreachable)
            label = f'<lambda@{node.lineno}:{node.col_offset}>'
            self.expr(node.body, scope + (label,), (), ('invocation context unknown',), False, 'return')
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            lazy = ('lazy comprehension',) if isinstance(node, ast.GeneratorExp) else ()
            for generator in node.generators:
                self.expr(generator.iter, scope, reach, notes, unreachable)
                reach += (Reach(f'iter@{generator.iter.lineno}:{generator.iter.col_offset}:item',
                                generator.iter.lineno, generator.iter.col_offset),)
                for test in generator.ifs:
                    self.add(test, 'comp-if', scope, reach, notes + lazy, unreachable)
                    self.expr(test, scope, reach, notes + lazy, unreachable, covered=True)
                    reach += (Reach.test(test, True),)
            values = [node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]
            for value in values:
                self.expr(value, scope, reach, notes + lazy, unreachable)
        else:
            # Opaque atoms (calls, operands, containers...) may contain their own BoolOps.
            for child in ast.iter_child_nodes(node):
                self.expr(child, scope, reach, notes, unreachable)

    def block(self, statements, scope=(), reach=(), notes=(), unreachable=False):
        for node in statements:
            self.statement(node, scope, reach, notes, unreachable)
            if isinstance(node, ast.Assert):
                reach += (Reach.test(node.test, True),)
            elif isinstance(node, ast.If):
                left, right = _ends(node.body), _ends(node.orelse)
                if left and right:
                    unreachable = True
                elif left or right:
                    reach += _continuation_requirements(node)
                elif _has_local_exit(node):
                    notes += (f'partial prior exit at L{node.lineno}',)
            elif isinstance(node, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
                unreachable = True

    def statement(self, node, scope, reach, notes, unreachable):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for decorator in node.decorator_list:
                self.expr(decorator, scope, reach, notes, unreachable)
            if hasattr(node, 'args'):
                for default in [*node.args.defaults, *node.args.kw_defaults]:
                    self.expr(default, scope, reach, notes, unreachable)
                self.block(node.body, scope + (node.name,), (), ('invocation context unknown',))
            else:
                for base in node.bases:
                    self.expr(base, scope, reach, notes, unreachable)
                self.block(node.body, scope + (node.name,), reach, notes, unreachable)
        elif isinstance(node, (ast.If, ast.While)):
            kind = 'if' if isinstance(node, ast.If) else 'while'
            self.add(node.test, kind, scope, reach, notes, unreachable, node)
            self.expr(node.test, scope, reach, notes, unreachable, covered=True)
            self.block(node.body, scope, reach + (Reach.test(node.test, True),), notes, unreachable)
            self.block(node.orelse, scope, reach + (Reach.test(node.test, False),), notes, unreachable)
        elif isinstance(node, ast.Assert):
            self.add(node.test, 'assert', scope, reach, notes, unreachable, node)
            self.expr(node.test, scope, reach, notes, unreachable, covered=True)
            self.expr(node.msg, scope, reach + (Reach.test(node.test, False),), notes, unreachable)
        elif isinstance(node, ast.Return):
            boolean_value = isinstance(node.value, (ast.BoolOp, ast.Compare)) or (isinstance(node.value, ast.UnaryOp) and isinstance(node.value.op, ast.Not))
            if boolean_value:
                self.add(node.value, 'return', scope, reach, notes, unreachable, node)
            self.expr(node.value, scope, reach, notes, unreachable, 'return', boolean_value)
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            self.expr(node.iter, scope, reach, notes, unreachable)
            item = Reach(f'for@{node.lineno}:item', node.lineno, node.col_offset)
            self.block(node.body, scope, reach + (item,), notes, unreachable)
            normal = Reach(f'for@{node.lineno}:normal-exit', node.lineno, node.col_offset)
            self.block(node.orelse, scope, reach + (normal,), notes, unreachable)
        elif isinstance(node, ast.Match):
            self.expr(node.subject, scope, reach, notes, unreachable)
            for index, case in enumerate(node.cases, 1):
                matched = Reach(f'match@{node.lineno}:case{index}:pattern', node.lineno, node.col_offset)
                context = reach + (matched,)
                if index > 1:
                    context += (Reach(f'match@{node.lineno}:prior-cases-missed', node.lineno, node.col_offset),)
                if case.guard is not None:
                    self.add(case.guard, 'match-guard', scope, context, notes, unreachable)
                    self.expr(case.guard, scope, context, notes, unreachable, covered=True)
                    context += (Reach.test(case.guard, True),)
                self.block(case.body, scope, context, notes, unreachable)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                self.expr(item.context_expr, scope, reach, notes, unreachable)
            self.block(node.body, scope, reach, notes, unreachable)
        elif isinstance(node, ast.Try) or hasattr(ast, 'TryStar') and isinstance(node, ast.TryStar):
            self.block(node.body, scope, reach, notes + ('try path; exceptions unresolved',), unreachable)
            for handler in node.handlers:
                self.expr(handler.type, scope, reach, notes, unreachable)
                self.block(handler.body, scope, reach, notes + ('exception-handler path',), unreachable)
            self.block(node.orelse, scope, reach, notes + ('try normal-completion path',), unreachable)
            self.block(node.finalbody, scope, reach, notes + ('finally path',), unreachable)
        else:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.stmt):
                    self.statement(child, scope, reach, notes, unreachable)
                else:
                    self.expr(child, scope, reach, notes, unreachable)


def discover(tree):
    visitor = Discovery()
    visitor.block(tree.body)
    return sorted(visitor.targets, key=lambda item: (item.lineno, item.col_offset, item.kind))


def parser_for(description, limit):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('source', nargs='?', default='solution.py')
    parser.add_argument('--line', type=int, help='expression or statement line')
    parser.add_argument('--column', type=int, help='zero-based UTF-8 column; requires --line')
    parser.add_argument('--target', help='exact target ID, e.g. f@12:7')
    parser.add_argument('--limit', type=int, default=limit, help=f'max targets 1-30; default {limit}')
    parser.add_argument('--verbose', action='store_true', help='full expressions and metadata')
    return parser


def source_targets(parser, args):
    if not 1 <= args.limit <= 30:
        parser.error('--limit must be 1-30')
    if args.line is not None and args.line < 1:
        parser.error('--line must be positive')
    if args.column is not None and (args.column < 0 or args.line is None):
        parser.error('--column must be nonnegative and used with --line')
    if args.target and (args.line is not None or args.column is not None):
        parser.error('use --target or --line/--column')
    path = Path(args.source).resolve()
    if not path.is_relative_to(Path.cwd().resolve()):
        parser.error('source must be inside the current task folder')
    if path.stat().st_size > 200_000:
        parser.error('source must not exceed 200 KB')
    targets = discover(ast.parse(path.read_text(encoding='utf-8-sig')))
    return [target for target in targets
            if (args.line is None or args.line in (target.lineno, target.owner_lineno))
            and (args.column is None or target.col_offset == args.column)
            and (not args.target or target.target_id == args.target)]


def brief(text, limit=240):
    return text if len(text) <= limit else text[:limit - 3] + '...'


def print_target(target, analysis, verbose=False):
    print(f'{target.target_id} [{target.kind}]: {format_logic(analysis.structure)}')
    if target.reached_if:
        print('reached_if~ ' + ' & '.join(requirement.short() for requirement in target.reached_if))
    if target.unreachable:
        print('unreachable: prior unconditional exit in this block')
    if target.notes:
        visible = [note for note in target.notes if note != 'invocation context unknown']
        if visible:
            print('context~ ' + '; '.join(dict.fromkeys(visible)))
    if target.kind in ('return', 'value') and isinstance(target.test, ast.BoolOp):
        print('operand-valued: assert the SPEC return, not decision T/F')
    for name, original in analysis.aliases.values():
        text = ast.unparse(original)
        print(f'{name}={text if verbose else brief(text)} [shared once when reached]')
    if verbose:
        print(f'source={ast.unparse(target.test)}')
        print(f'location={target.function}:{target.lineno}:{target.col_offset}-{target.end_lineno}:{target.end_col_offset}')
        for requirement in target.reached_if:
            if requirement.outcome is not None:
                print(f'  {requirement.short()}: {requirement.text}')
        if target.notes:
            print('context notes: ' + '; '.join(dict.fromkeys(target.notes)))


def print_atom(index, atom, analysis, hint=None, verbose=False):
    text = ast.unparse(analysis.display_node(atom.node))
    guard = format_logic(atom.guard) if atom.guard else 'always'
    fields = [f'C{index}: {text if verbose else brief(text)}', f'guard={guard}']
    flags = []
    if atom.potential_effects:
        flags.append('potential_effects')
    if atom.may_raise:
        flags.append('may_raise')
    if flags:
        fields.append('flags=' + ','.join(flags))
    if atom.repeat_of:
        fields.append(f'repeat=C{atom.repeat_of}')
    elif atom.equivalent_to:
        fields.append(f'scalar-equiv~C{atom.equivalent_to}')
    if hint:
        fields.append(hint if verbose else brief(hint, 300))
    print(' | '.join(fields))
    if verbose:
        print('  normalized_key=' + atom.normalized_key)


def main():
    parser = parser_for(__doc__, 8)
    args = parser.parse_args()
    try:
        targets = source_targets(parser, args)
        for index, target in enumerate(targets[:args.limit]):
            if index:
                print()
            result = analyze(target.test)
            print_target(target, result, args.verbose)
            for number, atom in enumerate(result.atoms, 1):
                print_atom(number, atom, result, verbose=args.verbose)
        if not targets:
            print('No matching expressions.')
        if len(targets) > args.limit:
            print(f'+{len(targets) - args.limit} targets; use --target/--line/--limit.')
        if args.verbose:
            print('Reach hints are snapshots, not solved paths. Flags are nonexhaustive; absence is not proof of safety.')
    except (OSError, SyntaxError, UnicodeError, RecursionError, ValueError) as error:
        parser.exit(1, f'Cannot discover expressions: {error}\n')


if __name__ == '__main__':
    main()
