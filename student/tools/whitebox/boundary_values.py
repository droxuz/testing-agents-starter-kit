#!/usr/bin/env python3
"""Static BVA/guards. +/-1 assumes integers; check SPEC and reachability.
C truth precedes NOT. Targets are internal values; no measured coverage.
"""
import argparse
import ast
import operator
import re
from pathlib import Path

from discover_conditions import conditions, format_logic


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
    node = ast.parse(text, mode="eval").body
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", default="solution.py")
    parser.add_argument("--line", type=int, help="decision source line")
    parser.add_argument("--limit", type=int, default=4, help="maximum decisions (1-30; default 4)")
    parser.add_argument("--verbose", action="store_true", help="full report")
    args = parser.parse_args()
    if not 1 <= args.limit <= 30:
        parser.error("--limit must be between 1 and 30")
    if args.line is not None and args.line < 1:
        parser.error("--line must be positive")
    path = Path(args.source).resolve()
    if not path.is_relative_to(Path.cwd().resolve()):
        parser.error("source must be inside the current task folder")
    try:
        if path.stat().st_size > 200_000:
            parser.error("source must not exceed 200 KB")
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        decisions = sorted((node for node in ast.walk(tree)
                            if isinstance(node, (ast.If, ast.While, ast.IfExp))
                            and (args.line is None or node.lineno == args.line)),
                           key=lambda node: (node.lineno, node.col_offset))
        if args.verbose:
            print("Static BVA candidates. Integer +/-1 targets require integer quantities.")
            print("Reach the decision, satisfy evaluation guards, and check SPEC.md.")
        for index, node in enumerate(decisions[:args.limit]):
            rows = []
            structure = conditions(node.test, rows)
            if args.verbose:
                print(f"\nLine {node.lineno}: {ast.unparse(node.test)}")
                print(f"  Structure: {structure}")
            else:
                if index:
                    print()
                print(f"L{node.lineno}: {brief(format_logic(structure))}")
            for i, (text, guard) in enumerate(rows[:8], 1):
                if args.verbose:
                    print(f"  C{i}: {text} | evaluate if {guard or 'always'}")
                    print(f"    {boundary_hint(text)}")
                else:
                    guard = format_logic(guard) if guard else "always"
                    hint = brief(compact_hint(text), 300)
                    print(f"C{i}: {brief(text)} | guard={brief(guard)} | {hint}")
            if len(rows) > 8:
                print(f"+{len(rows) - 8} conditions; inspect L{node.lineno}.")
        if not decisions:
            print("No matching decisions.")
        if len(decisions) > args.limit:
            print(f"+{len(decisions) - args.limit} decisions; use --line/--limit.")
        if args.verbose:
            print("\nEvaluated conditions may still be masked by later operands.")
            print("Targets are internal values, not full inputs or expected outputs.")
            print("No solving, exhaustive combinations, execution or coverage measurement.")
    except (OSError, SyntaxError, UnicodeError, RecursionError) as error:
        parser.exit(1, f"Cannot analyze source: {error}\n")


if __name__ == "__main__":
    main()