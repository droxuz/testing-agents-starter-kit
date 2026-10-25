#!/usr/bin/env python3
"""Plan abstract unique-cause MC/DC pairs with AST guards and integer BVA hints.
Rows A/E=assumed/evaluated; -=skipped. Check SPEC, coupling and reachability.
Does not execute source, solve inputs, derive oracles or measure coverage.
"""
import argparse
import ast
import itertools
from pathlib import Path

from discover_conditions import conditions, format_logic
from boundary_values import compact_hint, literal, UNKNOWN


def evaluate(node, values):
    """Evaluate only the generated Boolean structure, recording short circuits."""
    trace = ['-'] * len(values)

    def visit(part):
        if isinstance(part, ast.Name):
            index = int(part.id[1:]) - 1
            result = values[index]
            trace[index] = 'T' if result else 'F'
            return result
        if isinstance(part, ast.UnaryOp) and isinstance(part.op, ast.Not):
            return not visit(part.operand)
        if isinstance(part, ast.BoolOp):
            for child in part.values:
                result = visit(child)
                if isinstance(part.op, ast.And) and not result:
                    return False
                if isinstance(part.op, ast.Or) and result:
                    return True
            return result
        raise ValueError('Unsupported Boolean structure')

    return visit(node), ''.join(trace)


def plan(structure, rows):
    """Greedily reuse rows; other assumed conditions stay fixed in each pair."""
    expression = ast.parse(structure, mode='eval').body
    fixed = {}
    repeated = {}
    seen = {}
    for index, (text, _) in enumerate(rows):
        atom = ast.parse(text, mode='eval').body
        value = UNKNOWN if any(isinstance(part, ast.Call) for part in ast.walk(atom)) else literal(atom)
        if value is not UNKNOWN:
            fixed[index] = bool(value)
        if text in seen:
            repeated[index] = seen[text]
            repeated[seen[text]] = index
        else:
            seen[text] = index
    model = {}
    for bits in itertools.product([False, True], repeat=len(rows)):
        if all(bits[index] == value for index, value in fixed.items()):
            model[bits] = evaluate(expression, bits)
    selected = set()
    pairs = {}
    notes = {}
    for index in range(len(rows)):
        if index in fixed:
            notes[index] = 'fixed ' + ('T' if fixed[index] else 'F')
            continue
        if index in repeated:
            notes[index] = f'manual: repeats C{repeated[index] + 1}'
            continue
        candidates = []
        for first, (outcome, trace) in model.items():
            if first[index]:
                continue
            second = first[:index] + (True,) + first[index + 1:]
            if (second in model and outcome != model[second][0]
                    and trace[index] != '-' and model[second][1][index] != '-'):
                candidates.append((first, second))
        if not candidates:
            notes[index] = 'no abstract independence pair'
            continue
        pair = min(candidates, key=lambda pair: (
            len(set(pair) - selected), pair[0], pair[1]))
        selected.update(pair)
        pairs[index] = pair
    if not selected and model:
        selected.add(next(iter(model)))
    return model, sorted(selected), pairs, notes


def bitstring(values):
    return ''.join('T' if value else 'F' for value in values)


def clipped(text, limit=240):
    return text if len(text) <= limit else text[:limit - 3] + '...'


def report(node, rows, structure, verbose=False):
    model, selected, pairs, notes = plan(structure, rows)
    print(f'L{node.lineno}: {format_logic(structure)}')
    if verbose:
        print('Source: ' + ast.unparse(node.test))
    for index, (text, guard) in enumerate(rows):
        guard = format_logic(guard) if guard else 'always'
        hint = compact_hint(text)
        if not verbose:
            text, hint = clipped(text), clipped(hint)
        print(f'C{index + 1}: {text} | guard={guard} | {hint}')
    labels = {bits: f'R{i}' for i, bits in enumerate(selected, 1)}
    for bits in selected:
        outcome, trace = model[bits]
        print(f'{labels[bits]}: {bitstring(bits)}/{trace} -> {"T" if outcome else "F"}')
    if pairs:
        print('pairs: ' + '; '.join(
            f'C{i + 1}={labels[first]}/{labels[second]}'
            for i, (first, second) in pairs.items()))
    for index, note in notes.items():
        print(f'C{index + 1}: {note}')
    # Common variables can couple conditions; no domain/constraint solver is used.
    uses = {}
    for index, (text, _) in enumerate(rows):
        names = {part.id for part in ast.walk(ast.parse(text, mode='eval'))
                 if isinstance(part, ast.Name) and part.id not in {'len', 'abs', 'min', 'max'}}
        for name in names:
            uses.setdefault(name, set()).add(index + 1)
    coupled = sorted(name for name, indices in uses.items() if len(indices) > 1)
    if coupled:
        print('check shared variables: ' + clipped(','.join(coupled)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?', default='solution.py')
    parser.add_argument('--line', type=int, help='decision source line; includes simple decisions')
    parser.add_argument('--limit', type=int, default=3, help='max compound decisions (1-30; default 3)')
    parser.add_argument('--max-atoms', type=int, default=6, help='enumeration bound (1-8; default 6)')
    parser.add_argument('--verbose', action='store_true', help='full expressions and source')
    args = parser.parse_args()
    if not 1 <= args.limit <= 30 or not 1 <= args.max_atoms <= 8:
        parser.error('--limit must be 1-30 and --max-atoms 1-8')
    if args.line is not None and args.line < 1:
        parser.error('--line must be positive')
    path = Path(args.source).resolve()
    if not path.is_relative_to(Path.cwd().resolve()):
        parser.error('source must be inside the current task folder')
    try:
        if path.stat().st_size > 200_000:
            parser.error('source must not exceed 200 KB')
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        decisions = sorted((node for node in ast.walk(tree)
                            if isinstance(node, (ast.If, ast.While, ast.IfExp))
                            and (args.line is None or node.lineno == args.line)),
                           key=lambda node: (node.lineno, node.col_offset))
        targets = []
        for node in decisions:
            rows = []
            structure = conditions(node.test, rows)
            if len(rows) > 1 or args.line is not None:
                targets.append((node, rows, structure))
        if not targets:
            print('No matching compound decisions; use coverage_report or --line.')
            return
        print('Abstract unique-cause targets. Rows A/E=assumed/evaluated; -=skipped.')
        print('Check SPEC/reachability; solve inputs and oracles. Integer BVA assumes integers.')
        for index, (node, rows, structure) in enumerate(targets[:args.limit]):
            if index:
                print()
            if len(rows) > args.max_atoms:
                print(f'L{node.lineno}: {len(rows)} conditions; exceeds --max-atoms {args.max_atoms}.')
                continue
            report(node, rows, structure, args.verbose)
        if len(targets) > args.limit:
            print(f'+{len(targets) - args.limit} decisions; use --line/--limit.')
    except (OSError, SyntaxError, UnicodeError, RecursionError, ValueError) as error:
        parser.exit(1, f'Cannot plan targets: {error}\n')


if __name__ == '__main__':
    main()
