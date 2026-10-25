#!/usr/bin/env python3
"""Static guards for reached decisions. C truth precedes NOT."""
import argparse
import ast
from pathlib import Path


def format_logic(text):
    return ast.unparse(ast.parse(text, mode="eval").body)


def guarded_by(guard, requirement):
    return f"({guard}) and ({requirement})" if guard else requirement


def conditions(node, rows, guard=""):
    """Append condition occurrences and return their Boolean structure."""
    if isinstance(node, ast.BoolOp):
        parts = []
        for child in node.values:
            part = conditions(child, rows, guard)
            parts.append(part)
            requirement = part if isinstance(node.op, ast.And) else f"not ({part})"
            guard = guarded_by(guard, requirement)
        operator = " and " if isinstance(node.op, ast.And) else " or "
        return "(" + operator.join(parts) + ")"
    elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return f"not ({conditions(node.operand, rows, guard)})"
    elif isinstance(node, ast.Compare):
        operands = [node.left, *node.comparators]
        parts = []
        for i, symbol in enumerate(node.ops):
            comparison = ast.Compare(left=operands[i], ops=[symbol],
                                     comparators=[operands[i + 1]])
            rows.append((ast.unparse(comparison), guard))
            part = f"C{len(rows)}"
            parts.append(part)
            guard = guarded_by(guard, part)
        return "(" + " and ".join(parts) + ")" if len(parts) > 1 else parts[0]
    else:
        rows.append((ast.unparse(node), guard))
        return f"C{len(rows)}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", default="solution.py")
    parser.add_argument("--limit", type=int, default=8, help="max decisions; default 8")
    parser.add_argument("--line", type=int, help="source line")
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
    except (OSError, SyntaxError, UnicodeError, RecursionError) as error:
        parser.exit(1, f"Cannot read source: {error}\n")

    decisions = sorted(
        (node for node in ast.walk(tree)
         if isinstance(node, (ast.If, ast.While, ast.IfExp))
         and (args.line is None or node.lineno == args.line)),
        key=lambda node: (node.lineno, node.col_offset),
    )
    if args.verbose:
        print("Static discovery. Guards assume the decision is reached without exceptions.")
        print("C labels precede enclosing NOT; outcomes mean truthy/falsy.")
    for index, node in enumerate(decisions[:args.limit]):
        rows = []
        structure = conditions(node.test, rows)
        if args.verbose:
            print(f"\nLine {node.lineno}: {ast.unparse(node.test)}")
            print(f"  Structure: {structure}")
        else:
            if index:
                print()
            print(f"L{node.lineno}: {format_logic(structure)}")
        for i, (text, guard) in enumerate(rows, 1):
            if args.verbose:
                print(f"  C{i}: {text} [evaluated if {guard or 'always'}]")
            else:
                guard = format_logic(guard) if guard else "always"
                print(f"C{i}: {text} | guard={guard}")
    if not decisions:
        print("No matching decisions.")
    if len(decisions) > args.limit:
        print(f"+{len(decisions) - args.limit} decisions; use --line/--limit.")
    if args.verbose:
        print("\nCheck SPEC.md. No feasibility or coverage is established.")



if __name__ == "__main__":
    main()