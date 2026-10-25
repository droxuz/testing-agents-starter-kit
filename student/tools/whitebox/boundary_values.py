#!/usr/bin/env python3
"""Static BVA/guards. +/-1 assumes integers; check SPEC and reachability.
C truth precedes NOT. Targets are internal values; no measured coverage.
"""
import argparse
import ast
import operator
import re
from pathlib import Path

from discover_conditions import (analyze, parser_for, source_targets,
                                 print_target, print_atom)


OPS = {ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt,
       ast.GtE: operator.ge, ast.Eq: operator.eq, ast.NotEq: operator.ne}
REVERSE = {ast.Lt: ast.Gt, ast.LtE: ast.GtE, ast.Gt: ast.Lt,
           ast.GtE: ast.LtE, ast.Eq: ast.Eq, ast.NotEq: ast.NotEq}
UNKNOWN = object()


def literal(node):
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, RecursionError):
        return UNKNOWN


def boundary_hint(text):
    node = ast.parse(text, mode="eval").body if isinstance(text, str) else text
    if not isinstance(node, ast.Compare) or len(node.ops) != 1:
        return "seek truthy and falsy cases; no numeric boundary inferred"
    left, right, op = node.left, node.comparators[0], type(node.ops[0])
    if op in (ast.In, ast.NotIn):
        return "try a member and a nonmember; empty/nonempty container if valid"
    if op in (ast.Is, ast.IsNot):
        return "try the same object and a different object; respect allowed types"
    if op not in OPS:
        return "seek true and false cases using the specification"
    a, b = literal(left), literal(right)
    if a is not UNKNOWN and b is UNKNOWN:
        left, right, a, b, op = right, left, b, a, REVERSE[op]
    quantity = ast.unparse(left)
    if a is not UNKNOWN and b is not UNKNOWN:
        return "literal-only comparison; check whether both outcomes are feasible"
    if type(b) is int:
        values = [b - 1, b, b + 1]
        # A length cannot be negative. Other SPEC constraints remain the LLM's job.
        if (isinstance(left, ast.Call) and isinstance(left.func, ast.Name)
                and left.func.id == "len"):
            values = [value for value in values if value >= 0]
        cases = ", ".join(f"{value}=>{'T' if OPS[op](value, b) else 'F'}"
                          for value in values)
        return f"integer targets for {quantity}: {cases}"
    if type(b) is float:
        return f"for {quantity}: below {b!r}, at {b!r}, above {b!r}; choose a suitable numeric step"
    if b is not UNKNOWN:
        if op in (ast.Eq, ast.NotEq):
            return f"for {quantity}: {b!r} and a different specification-valid value"
        return "nonnumeric comparison; choose valid values on each side of the ordering"
    boundary = ast.unparse(right)
    return (f"if integer-valued, target {quantity} around ({boundary}): "
            f"({boundary}) - 1, ({boundary}), ({boundary}) + 1; "
            "hold boundary expression stable")


def compact_hint(text):
    hint = boundary_hint(text)
    if hint.startswith("integer targets for "):
        quantity, cases = hint.removeprefix("integer targets for ").rsplit(": ", 1)
        cases = re.sub(r"(-?\d+)=>([TF])", r"\1(\2)", cases).replace(", ", ",")
        return f"{quantity}: {cases}"
    short = {
        "seek truthy and falsy cases; no numeric boundary inferred": "truthy/falsy",
        "try a member and a nonmember; empty/nonempty container if valid": "member/nonmember; empty/nonempty if valid",
        "try the same object and a different object; respect allowed types": "same/different object; valid types",
        "seek true and false cases using the specification": "T/F per SPEC",
        "literal-only comparison; check whether both outcomes are feasible": "literal-only; check feasibility",
        "nonnumeric comparison; choose valid values on each side of the ordering": "nonnumeric: valid values on each side",
    }
    if hint in short:
        return short[hint]
    if hint.startswith("if integer-valued, target "):
        return "int " + hint.removeprefix("if integer-valued, target ").removesuffix("; hold boundary expression stable") + "; keep boundary stable"
    if hint.startswith("for "):
        return hint.removeprefix("for ").replace("; choose a suitable numeric step", "; choose step").replace(" and a different specification-valid value", "/different valid value")
    return hint


def brief(text, limit=200):
    return text if len(text) <= limit else text[:limit - 3] + "..."


def main():
    parser = parser_for(__doc__, 4)
    args = parser.parse_args()
    try:
        targets = source_targets(parser, args)
        for index, target in enumerate(targets[:args.limit]):
            if index:
                print()
            result = analyze(target.test)
            print_target(target, result, args.verbose)
            atoms = result.atoms if args.verbose else result.atoms[:8]
            for number, atom in enumerate(atoms, 1):
                display = result.display_node(atom.node)
                hint = boundary_hint(display) if args.verbose else compact_hint(display)
                print_atom(number, atom, result, hint, args.verbose)
            if len(atoms) < len(result.atoms):
                print(f'+{len(result.atoms) - len(atoms)} atoms; use --verbose.')
        if not targets:
            print('No matching expressions.')
        if len(targets) > args.limit:
            print(f'+{len(targets) - args.limit} targets; use --target/--line/--limit.')
        if args.verbose:
            print('Targets are internal values, not solved inputs. Reach hints are structural, not proven paths.')
    except (OSError, SyntaxError, UnicodeError, RecursionError, ValueError) as error:
        parser.exit(1, f'Cannot analyze expressions: {error}\n')


if __name__ == "__main__":
    main()
