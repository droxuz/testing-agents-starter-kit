#!/usr/bin/env python3
"""Plan abstract unique-cause MC/DC pairs with AST guards and integer BVA hints.
Rows A/E=assumed/evaluated; -=skipped. Check SPEC, coupling and reachability.
Does not execute source, solve inputs, derive oracles or measure coverage.
"""
import argparse
import ast
import itertools
from pathlib import Path

from discover_conditions import (analyze, parser_for, source_targets,
                                 print_target, print_atom)
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


def report(target, result, verbose=False):
    print_target(target, result, verbose)
    for index, atom in enumerate(result.atoms, 1):
        hint = compact_hint(result.display_node(atom.node))
        print_atom(index, atom, result, hint, verbose)
    if target.unreachable:
        print('No pairs: structurally unreachable after a block exit.')
        return
    model, selected, pairs, notes = plan(result.structure, result.rows)
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
    uses = {}
    for index, atom in enumerate(result.atoms):
        names = {part.id for part in ast.walk(atom.node)
                 if isinstance(part, ast.Name) and part.id not in {'len', 'abs', 'min', 'max'}}
        for name in names:
            uses.setdefault(name, set()).add(index + 1)
    coupled = sorted(name for name, indices in uses.items() if len(indices) > 1)
    if coupled:
        print('check shared variables: ' + clipped(','.join(coupled)))


def main():
    parser = parser_for(__doc__, 3)
    parser.add_argument('--max-atoms', type=int, default=6, help='enumeration bound 1-8; default 6')
    args = parser.parse_args()
    if not 1 <= args.max_atoms <= 8:
        parser.error('--max-atoms must be 1-8')
    try:
        decisions = source_targets(parser, args)
        targets = []
        for target in decisions:
            result = analyze(target.test)
            if len(result.atoms) > 1 or args.line is not None or args.target:
                targets.append((target, result))
        if not targets:
            print('No matching compound expressions; use coverage_report or --line.')
            return
        print('Abstract unique-cause targets. Rows A/E=assumed/evaluated; -=skipped.')
        print('Reach hints are snapshots, not solved paths. Check SPEC/coupling; +/-1 assumes integers.')
        for index, (target, result) in enumerate(targets[:args.limit]):
            if index:
                print()
            if len(result.atoms) > args.max_atoms:
                print(f'{target.target_id}: {len(result.atoms)} atoms; exceeds --max-atoms {args.max_atoms}.')
                continue
            report(target, result, args.verbose)
        if len(targets) > args.limit:
            print(f'+{len(targets) - args.limit} targets; use --target/--line/--limit.')
    except (OSError, SyntaxError, UnicodeError, RecursionError, ValueError) as error:
        parser.exit(1, f'Cannot plan targets: {error}\n')


if __name__ == '__main__':
    main()
