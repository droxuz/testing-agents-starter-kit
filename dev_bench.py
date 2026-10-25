#!/usr/bin/env python3
"""dev_bench.py: Rapid-iteration benchmark runner for testing agent development.

By default, runs the standardized 4-problem core suite (~1.5-2m total across 4 workers):
    - lcb-3610: Sliding window / heap frequency (7 bugs, 1 hard mutant, 15 lines)
    - lcb-3612: Monotonicity / binary search (7 bugs, 9 hard mutants, 14 lines)
    - lcb-3686: Prefix array / beautiful splits (8 bugs, 11 hard mutants, 17 lines)
    - lcb-3594: Hash map / sum outliers (6 bugs, 3 hard mutants, 21 lines)
    Total testbed: 28 bugs, 24 hard mutants across 4 distinct algorithmic domains.

Usage:
    python dev_bench.py
    python dev_bench.py --run exp1-feature --notes "Feature hypothesis"
    python dev_bench.py --canary     # Ultra-fast 1-problem check (~20s)
    python dev_bench.py --extended   # 8-problem full extended suite (~3-4m)
    python dev_bench.py --only lcb-3610
"""

import argparse
import datetime
import json
import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# Ignore OpenRouter cost-tracking discrepancies
os.environ["MSWEA_COST_TRACKING"] = "ignore_errors"

REPO_ROOT = Path(__file__).resolve().parent
LOG_FILE = REPO_ROOT / "EXPERIMENTS.md"
RUNS_DIR = REPO_ROOT / "runs"
SEEDS_DIR = REPO_ROOT / "seeds" / "blackbox"

# Ultra-fast canary problem for quick tool/prompt syntax validation
CANARY_PROBLEM = ["lcb-3566"]

# Standard 4-problem core suite (28 bugs, 24 hard mutants, zero reasoning traps)
CORE_PROBLEMS = [
    "lcb-3610",  # Sliding window / frequency ties (7 bugs, 1 hard mutant, 15 lines)
    "lcb-3612",  # Monotonicity / binary search (7 bugs, 9 hard mutants, 14 lines)
    "lcb-3686",  # Prefix array / beautiful splits (8 bugs, 11 hard mutants, 17 lines)
    "lcb-3594",  # Hash map / sum outliers (6 bugs, 3 hard mutants, 21 lines)
]

# 8-problem extended suite (56 bugs, 72 hard mutants)
EXTENDED_PROBLEMS = [
    *CORE_PROBLEMS,
    "lcb-3566",  # String simulation / state machine (5 bugs, 0 hard mutants, 12 lines)
    "lcb-3654",  # Dynamic programming / array sum ops (8 bugs, 15 hard mutants, 32 lines)
    "lcb-3607",  # Greedy / number theory (7 bugs, 9 hard mutants, 23 lines)
    "lcb-3690",  # Binary search on answer / flips (8 bugs, 24 hard mutants, 26 lines)
]

_active_child_process: subprocess.Popen | None = None


def kill_active_process() -> None:
    global _active_child_process
    if _active_child_process is None:
        return
    proc = _active_child_process
    _active_child_process = None
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True, timeout=5)
        else:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def handle_interrupt(signum=None, frame=None) -> None:
    kill_active_process()
    print("\n\n[dev_bench] Interrupted by user (Ctrl+C). Aborting immediately.\n", file=sys.stderr)
    sys.exit(130)


signal.signal(signal.SIGINT, handle_interrupt)
if hasattr(signal, "SIGBREAK"):
    signal.signal(signal.SIGBREAK, handle_interrupt)
if hasattr(signal, "SIGTERM"):
    signal.signal(signal.SIGTERM, handle_interrupt)


def check_api_key() -> None:
    load_dotenv(REPO_ROOT / ".env")
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key or key.startswith("sk-or-...") or "your-key" in key.lower():
        print("\n [ERROR] OPENROUTER_API_KEY is not configured in .env!\n", file=sys.stderr)
        sys.exit(1)


def seed_blackbox_tests(run_name: str, problems: list[str]) -> None:
    """Instantly seeds pre-existing black-box tests from seeds/blackbox or runs/my-final."""
    target_bb = RUNS_DIR / run_name / "blackbox"
    fallback_bb = RUNS_DIR / "my-final" / "blackbox"

    for pid in problems:
        dst = target_bb / pid / "tests" / "test_blackbox.py"
        if dst.exists():
            continue

        src = SEEDS_DIR / pid / "tests" / "test_blackbox.py"
        if not src.exists():
            src = fallback_bb / pid / "tests" / "test_blackbox.py"

        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)


def run_command(cmd: list[str], description: str) -> None:
    global _active_child_process
    print(f"\n>>> [dev_bench] {description}: {' '.join(cmd)}")
    try:
        kwargs = {}
        if sys.platform != "win32":
            kwargs["start_new_session"] = True
        env = os.environ | {"PYTHONUNBUFFERED": "1", "MSWEA_COST_TRACKING": "ignore_errors"}
        proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, **kwargs)
        _active_child_process = proc
        ret = proc.wait()
        _active_child_process = None
        if ret != 0:
            print(f"Error during {description} (exit code {ret})", file=sys.stderr)
            sys.exit(ret)
    except KeyboardInterrupt:
        handle_interrupt()


def extract_results(run_name: str, mode: str) -> dict:
    mode_dir = RUNS_DIR / run_name / mode
    eval_file = mode_dir / "evaluation.json"
    usage_file = mode_dir / "usage.json"

    if not eval_file.exists():
        raise FileNotFoundError(f"Missing evaluation file: {eval_file}")

    eval_data = json.loads(eval_file.read_text(encoding="utf-8"))
    usage_data = json.loads(usage_file.read_text(encoding="utf-8")) if usage_file.exists() else {}

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
    print("=" * 70 + "\n")


def run_benchmark(mode: str, run_name: str, problems: list[str], workers: int, notes: str, eval_only: bool) -> None:
    python_exe = sys.executable

    if not eval_only:
        check_api_key()
        if mode == "whitebox":
            seed_blackbox_tests(run_name, problems)

        cmd_run = [python_exe, "-u", "-m", "testagent.run", "--mode", mode, "--run", run_name, "--workers", str(workers), "--only", *problems]
        run_command(cmd_run, f"Running agent ({mode}) on {len(problems)} benchmark problem(s) with {workers} worker(s)")

    cmd_eval = [python_exe, "-u", "-m", "testagent.evaluate", "--run", run_name, "--mode", mode, "--only", *problems]
    run_command(cmd_eval, f"Evaluating {mode} tests on benchmark problem(s)")

    results = extract_results(run_name, mode)
    print_console_summary(results)

    markdown_entry = format_markdown_entry(results, notes)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(markdown_entry)
    print(f"[dev_bench] Logged results successfully to {LOG_FILE.name}!")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mode", choices=["whitebox", "blackbox", "combined"], default="whitebox", help="Mode to run (default: whitebox)")
    parser.add_argument("--run", default="exp0-baseline", help="Run identifier (default: exp0-baseline)")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers (default: 4)")
    parser.add_argument("--only", nargs="*", default=None, help="Specific problem IDs to run")
    parser.add_argument("--canary", action="store_true", help="Run single canary problem (~20s)")
    parser.add_argument("--extended", action="store_true", help="Run 8 extended problems")
    parser.add_argument("--notes", default="Development benchmark run", help="Notes to append to EXPERIMENTS.md")
    parser.add_argument("--eval-only", action="store_true", help="Only evaluate existing run without re-running agent")
    args = parser.parse_args()

    if args.only:
        problems = args.only
    elif args.canary:
        problems = CANARY_PROBLEM
    elif args.extended:
        problems = EXTENDED_PROBLEMS
    else:
        problems = CORE_PROBLEMS

    workers = min(args.workers, len(problems))

    try:
        run_benchmark(args.mode, args.run, problems, workers, args.notes, args.eval_only)
    except KeyboardInterrupt:
        handle_interrupt()


if __name__ == "__main__":
    main()
