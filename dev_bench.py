#!/usr/bin/env python3
"""dev_bench.py: Single command to run, evaluate, and log the standardized 4-problem benchmark.

Usage:
    python dev_bench.py --mode whitebox --run exp0-baseline --notes "Starter kit baseline"
    python dev_bench.py --mode combined --run exp0-combined --notes "Combined baseline"
    python dev_bench.py --mode both --run exp0-baseline
    python dev_bench.py --eval-only --run exp0-baseline --mode whitebox
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_PROBLEMS = [
    "lcb-3610",  # Sliding window / frequency ties (7 bugs, 1 hard mutant)
    "lcb-3607",  # Greedy / number theory (7 bugs, 9 hard mutants)
    "lcb-3594",  # Hash map / sum outliers (6 bugs, 3 hard mutants)
    "lcb-3566",  # String simulation / state machine (5 bugs, 0 hard mutants)
    "lcb-3686",  # Prefix array / beautiful splits (8 bugs, 11 hard mutants)
    "lcb-3654",  # Dynamic programming / array sum (8 bugs, 15 hard mutants)
    "lcb-3612",  # Binary search / increasing subarrays (7 bugs, 9 hard mutants)
    "lcb-3690",  # Binary search on answer / identical chars (8 bugs, 24 hard mutants)
]
REPO_ROOT = Path(__file__).resolve().parent
LOG_FILE = REPO_ROOT / "EXPERIMENTS.md"
RUNS_DIR = REPO_ROOT / "runs"


def sync_windows_shims() -> None:
    if sys.platform != "win32":
        return
    scripts_dir = Path(sys.executable).parent
    tools_root = REPO_ROOT / "student" / "tools"
    for tool_file in tools_root.rglob("*"):
        if tool_file.is_file() and not tool_file.suffix and not tool_file.name.startswith((".", "_")):
            shim = scripts_dir / f"{tool_file.name}.cmd"
            shim.write_text(f'@"{sys.executable}" "{tool_file.resolve()}" %*\n')


def check_api_key() -> None:
    load_dotenv(REPO_ROOT / ".env")
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key or key == "sk-or-..." or "your-key" in key.lower() or key.startswith("sk-or-..."):
        print("\n" + "!" * 72, file=sys.stderr)
        print(" [ERROR] OPENROUTER_API_KEY is not configured in .env!", file=sys.stderr)
        print(" Please open `.env` in the project root and set your actual key:", file=sys.stderr)
        print("     OPENROUTER_API_KEY=sk-or-v1-abcdef123456...", file=sys.stderr)
        print("!" * 72 + "\n", file=sys.stderr)
        sys.exit(1)


def check_agent_errors(run_name: str, mode: str) -> None:
    usage_file = RUNS_DIR / run_name / mode / "usage.json"
    if not usage_file.exists():
        return
    try:
        data = json.loads(usage_file.read_text())
    except Exception:
        return
    problems = data.get("problems", [])
    errors = [p for p in problems if p.get("exit_status", "").startswith("Error:")]
    if errors:
        print("\n" + "!" * 72, file=sys.stderr)
        print(f" [WARNING] {len(errors)} problem(s) failed in mode '{mode}':", file=sys.stderr)
        for err in errors[:3]:
            print(f"   * {err['problem_id']}: {err['exit_status']}", file=sys.stderr)
        print("!" * 72 + "\n", file=sys.stderr)
        if len(errors) == len(problems):
            print(f"[dev_bench] All problems failed with errors. Aborting evaluation.", file=sys.stderr)
            sys.exit(1)


def run_command(cmd: list[str], description: str) -> None:
    print(f"\n>>> [dev_bench] {description}: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if result.returncode != 0:
        print(f"Error during {description} (exit code {result.returncode})", file=sys.stderr)
        sys.exit(result.returncode)


def extract_results(run_name: str, mode: str) -> dict:
    mode_dir = RUNS_DIR / run_name / mode
    eval_file = mode_dir / "evaluation.json"
    usage_file = mode_dir / "usage.json"

    if not eval_file.exists():
        raise FileNotFoundError(f"Missing evaluation file: {eval_file}")

    eval_data = json.loads(eval_file.read_text())
    usage_data = json.loads(usage_file.read_text()) if usage_file.exists() else {}

    summary = eval_data.get("summary", {})
    totals = usage_data.get("totals", {})
    problems = eval_data.get("problems", [])

    total_bugs_killed = sum(p["suite"]["bugs_killed"] for p in problems)
    total_bugs = sum(p["suite"]["bugs_total"] for p in problems)
    total_hard_killed = sum(p["suite"]["hard_mutants_killed"] for p in problems)
    total_hard = sum(p["suite"]["hard_mutants_total"] for p in problems)
    total_calls_used = sum(p["suite"].get("calls_used", 0) for p in problems)

    return {
        "run_name": run_name,
        "mode": mode,
        "summary": summary,
        "totals": totals,
        "problems": problems,
        "bugs_killed": total_bugs_killed,
        "bugs_total": total_bugs,
        "hard_killed": total_hard_killed,
        "hard_total": total_hard,
        "calls_used": total_calls_used,
        "cost_usd": totals.get("cost_usd", 0.0),
        "total_tokens": totals.get("prompt_tokens", 0) + totals.get("completion_tokens", 0),
    }


def format_markdown_entry(data: dict, notes: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = data["summary"]
    
    bug_rate = f"{summary.get('bug_kill_rate', 0.0) * 100:.1f}% ({data['bugs_killed']}/{data['bugs_total']})"
    hard_score = f"{summary.get('hard_mutation_score', 0.0) * 100:.1f}% ({data['hard_killed']}/{data['hard_total']})"
    path_cov = f"{summary.get('path_coverage', 0.0) * 100:.1f}%" if summary.get("path_coverage") is not None else "N/A"
    branch_cov = f"{summary.get('branch_coverage', 0.0) * 100:.1f}%"
    oracle_prec = f"{summary.get('oracle_precision', 0.0) * 100:.1f}%"

    md = [
        f"\n### Experiment: `{data['run_name']}` ({data['mode']})",
        f"- **Timestamp:** {timestamp}",
        f"- **Notes / Hypothesis:** {notes}",
        f"- **Cost / Tokens:** ${data['cost_usd']:.4f} | {data['total_tokens']:,} tokens",
        f"- **Total Function Calls Used:** {data['calls_used']}",
        "",
        "| Metric | Result | Target / Baseline |",
        "|---|---|---|",
        f"| **Bug Detection Rate** | **{bug_rate}** | Primary Goal |",
        f"| **Hard-Mutant Score** | **{hard_score}** | High-Yield Mutants |",
        f"| **Path Coverage** | {path_cov} | Branch/Path Exhaustion |",
        f"| **Branch Coverage** | {branch_cov} | Structural Coverage |",
        f"| **Oracle Precision** | {oracle_prec} | Test Correctness |",
        "",
        "#### Per-Problem Breakdown",
        "| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |",
        "|---|:---:|:---:|:---:|:---:|:---:|:---:|",
    ]

    for p in data["problems"]:
        s = p["suite"]
        md.append(
            f"| `{p['problem_id']}` | {s.get('tests_valid', 0)} | {s.get('wrong_oracle', 0)} | "
            f"{s.get('bugs_killed', 0)}/{s.get('bugs_total', 0)} | "
            f"{s.get('hard_mutants_killed', 0)}/{s.get('hard_mutants_total', 0)} | "
            f"{s.get('calls_used', 0)} | {s.get('branch_coverage', 0.0) * 100:.1f}% |"
        )

    md.append("\n---\n")
    return "\n".join(md)


def print_console_summary(data: dict) -> None:
    summary = data["summary"]
    print("\n" + "=" * 70)
    print(f" BENCHMARK SUMMARY: {data['run_name']} ({data['mode']})")
    print("=" * 70)
    print(f"  * Bug Detection Rate:   {summary.get('bug_kill_rate', 0.0) * 100:.2f}% ({data['bugs_killed']}/{data['bugs_total']} killed)")
    print(f"  * Hard-Mutant Score:    {summary.get('hard_mutation_score', 0.0) * 100:.2f}% ({data['hard_killed']}/{data['hard_total']} killed)")
    print(f"  * Branch Coverage:      {summary.get('branch_coverage', 0.0) * 100:.2f}%")
    print(f"  * Oracle Precision:     {summary.get('oracle_precision', 0.0) * 100:.2f}%")
    print(f"  * Total Calls Used:     {data['calls_used']}")
    print(f"  * Cost (USD):           ${data['cost_usd']:.4f}")
    print(f"  * Total Tokens:         {data['total_tokens']:,}")
    print("=" * 70)


def run_benchmark(mode: str, run_name: str, problems: list[str], workers: int, notes: str, eval_only: bool) -> None:
    sync_windows_shims()
    python_exe = sys.executable

    if not eval_only:
        check_api_key()
        # In separate mode, whitebox benefits from blackbox tests existing.
        # If running whitebox and blackbox tests don't exist yet, run blackbox first.
        if mode == "whitebox":
            blackbox_exists = all((RUNS_DIR / run_name / "blackbox" / pid / "tests" / "test_blackbox.py").exists() for pid in problems)
            if not blackbox_exists:
                print(f"[dev_bench] Seeding blackbox tests for run '{run_name}'...")
                cmd_bb = [python_exe, "-m", "testagent.run", "--mode", "blackbox", "--run", run_name, "--workers", str(workers), "--only", *problems]
                run_command(cmd_bb, f"Running black-box pre-requisite for {run_name}")
                check_agent_errors(run_name, "blackbox")

        cmd_run = [python_exe, "-m", "testagent.run", "--mode", mode, "--run", run_name, "--workers", str(workers), "--only", *problems]
        run_command(cmd_run, f"Running agent ({mode}) on {len(problems)} benchmark problems")
        check_agent_errors(run_name, mode)

    cmd_eval = [python_exe, "-m", "testagent.evaluate", "--run", run_name, "--mode", mode, "--only", *problems]
    run_command(cmd_eval, f"Evaluating {mode} tests on benchmark problems")

    results = extract_results(run_name, mode)
    print_console_summary(results)

    markdown_entry = format_markdown_entry(results, notes)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(markdown_entry)
    print(f"[dev_bench] Logged results successfully to {LOG_FILE.name}!")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mode", choices=["whitebox", "combined", "both"], default="whitebox", help="Mode to run (default: whitebox)")
    parser.add_argument("--run", default="exp0-baseline", help="Run name identifier (default: exp0-baseline)")
    parser.add_argument("--workers", type=int, default=8, help="Workers for parallel execution (default: 8)")
    parser.add_argument("--only", nargs="*", default=DEFAULT_PROBLEMS, help="Problem IDs to run (default: 8-problem benchmark)")
    parser.add_argument("--notes", default="Development benchmark run", help="Brief hypothesis or notes to append to EXPERIMENTS.md")
    parser.add_argument("--eval-only", action="store_true", help="Only evaluate existing run and log without re-running agent")
    args = parser.parse_args()

    modes = ["whitebox", "combined"] if args.mode == "both" else [args.mode]
    for m in modes:
        run_benchmark(m, args.run, args.only, args.workers, args.notes, args.eval_only)


if __name__ == "__main__":
    main()
