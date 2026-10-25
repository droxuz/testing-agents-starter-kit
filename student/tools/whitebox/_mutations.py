"""Small deterministic AST mutation candidates generated only from the task source."""
import ast
import copy
import hashlib
from collections import defaultdict


def candidates(source, method, limit=12, line=None):
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Solution')
    function = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == method)
    specifications = []

    def add(node, category, replacement):
        if line is None or node.lineno == line:
            specifications.append((node, category, replacement))

    binary = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Add,
              ast.FloorDiv: ast.Mult, ast.Div: ast.Mult, ast.Mod: ast.Add,
              ast.LShift: ast.RShift, ast.RShift: ast.LShift, ast.BitAnd: ast.BitOr,
              ast.BitOr: ast.BitAnd, ast.BitXor: ast.BitOr}
    comparisons = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE,
                   ast.GtE: ast.Gt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
                   ast.In: ast.NotIn, ast.NotIn: ast.In}
    for node in ast.walk(function):
        if isinstance(node, ast.Constant) and type(node.value) is int and abs(node.value) <= 10**18:
            for delta in (-1, 1):
                add(node, 'constant', ast.Constant(value=node.value + delta))
        elif isinstance(node, ast.BinOp) and type(node.op) in binary:
            replacement = copy.deepcopy(node)
            replacement.op = binary[type(node.op)]()
            add(node, 'arithmetic', replacement)
            if isinstance(node.op, ast.Mod):
                add(node, 'remove-modulo', copy.deepcopy(node.left))
        elif isinstance(node, ast.AugAssign) and type(node.op) in binary:
            replacement = copy.deepcopy(node)
            replacement.op = binary[type(node.op)]()
            add(node, 'update', replacement)
        elif isinstance(node, ast.Compare):
            for index, operator in enumerate(node.ops):
                if type(operator) in comparisons:
                    replacement = copy.deepcopy(node)
                    replacement.ops[index] = comparisons[type(operator)]()
                    add(node, 'comparison', replacement)
        elif isinstance(node, ast.BoolOp):
            replacement = copy.deepcopy(node)
            replacement.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
            add(node, 'boolean', replacement)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {'min', 'max'}:
            replacement = copy.deepcopy(node)
            replacement.func.id = 'min' if node.func.id == 'max' else 'max'
            add(node, 'selection', replacement)
        elif isinstance(node, ast.Continue):
            add(node, 'loop-exit', ast.Break())

    grouped = defaultdict(list)
    for specification in sorted(specifications, key=lambda s: (s[0].lineno, s[0].col_offset, s[1])):
        grouped[specification[1]].append(specification)
    order = []
    while any(grouped.values()):
        for category in sorted(grouped):
            if grouped[category]:
                order.append(grouped[category].pop(0))

    mutants, seen = [], set()
    for original, category, replacement in order:
        key = (type(original), original.lineno, original.col_offset)

        class Replace(ast.NodeTransformer):
            def generic_visit(self, node):
                if hasattr(node, 'lineno') and (type(node), node.lineno, node.col_offset) == key:
                    return ast.copy_location(copy.deepcopy(replacement), node)
                return super().generic_visit(node)

        changed = ast.fix_missing_locations(Replace().visit(copy.deepcopy(tree)))
        text = ast.unparse(changed) + '\n'
        identity = hashlib.sha256(text.encode()).hexdigest()[:12]
        if identity in seen:
            continue
        seen.add(identity)
        try:
            compile(text, 'solution.py', 'exec')
        except SyntaxError:
            continue
        mutants.append({'id': identity, 'line': original.lineno, 'column': original.col_offset,
                        'category': category, 'before': ast.unparse(original)[:160],
                        'after': ast.unparse(replacement)[:160], 'source': text})
        if len(mutants) >= limit:
            break
    return mutants
