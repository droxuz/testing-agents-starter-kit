#!/usr/bin/env python3
"""dev_bench.py: Rapid-iteration benchmark runner for testing agent development.

By default, runs a fast 4-problem core suite (~45-60s) across 4 workers:
    lcb-3566 (strings), lcb-3610 (sliding window), lcb-3594 (hash maps), lcb-3607 (greedy/primes).

Usage:
    python dev_bench.py
    python dev_bench.py --mode whitebox --run exp0-baseline --notes "Starter kit baseline"
    python dev_bench.py --mode whitebox --run exp1-boundary --notes "Boundary condition prompt"
    python dev_bench.py --extended  # Runs full 8-problem benchmark (~2.5m)
    python dev_bench.py --only lcb-3566
"""

import argparse
import datetime
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# Ignore OpenRouter cost-tracking discrepancies (e.g. upstream provider reporting cost 0)
os.environ["MSWEA_COST_TRACKING"] = "ignore_errors"

# 4-problem fast core suite (~1-2m total): fast, high-yield, no reasoning traps (28 bugs, 24 hard mutants)
CORE_PROBLEMS = [
    "lcb-3610",  # Sliding window / frequency ties (7 bugs, 1 hard mutant, 15 lines)
    "lcb-3612",  # Binary search / increasing subarrays (7 bugs, 9 hard mutants, 20 lines)
    "lcb-3686",  # Prefix array / beautiful splits (8 bugs, 11 hard mutants, 18 lines)
    "lcb-3594",  # Hash map / sum outliers (6 bugs, 3 hard mutants, 21 lines)
]

# Full 8-problem extended suite: 56 bugs, 72 hard mutants
EXTENDED_PROBLEMS = [
    *CORE_PROBLEMS,
    "lcb-3566",  # String simulation / state machine (5 bugs, 0 hard mutants)
    "lcb-3654",  # Dynamic programming / array sum (8 bugs, 15 hard mutants)
    "lcb-3607",  # Greedy / number theory (7 bugs, 9 hard mutants) - slow reasoning model trap
    "lcb-3690",  # Binary search on answer / identical chars (8 bugs, 24 hard mutants)
]

DEFAULT_PROBLEMS = CORE_PROBLEMS
REPO_ROOT = Path(__file__).resolve().parent
LOG_FILE = REPO_ROOT / "EXPERIMENTS.md"
RUNS_DIR = REPO_ROOT / "runs"

_active_child_process: subprocess.Popen | None = None


def kill_active_process() -> None:
    """Forcefully terminates the active child process and its entire process tree."""
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
    """Signal handler for Ctrl+C to abort cleanly without logging to EXPERIMENTS.md."""
    kill_active_process()
    print("\n\n[dev_bench] Interrupted by user (Ctrl+C). Aborting immediately without writing to EXPERIMENTS.md.\n", file=sys.stderr)
    sys.exit(130)


# Register interrupt handlers for clean terminal termination on both Windows and Linux
signal.signal(signal.SIGINT, handle_interrupt)
if hasattr(signal, "SIGBREAK"):
    signal.signal(signal.SIGBREAK, handle_interrupt)
if hasattr(signal, "SIGTERM"):
    signal.signal(signal.SIGTERM, handle_interrupt)


def sync_windows_shims() -> None:
    """Creates Windows shims for CLI tools and enables Windows POSIX compatibility.

    On Linux or macOS, this function returns immediately and has zero effect.
    """
    if sys.platform != "win32":
        return

    scripts_dir = Path(sys.executable).parent
    tools_root = REPO_ROOT / "student" / "tools"

    # Generate .cmd wrappers for extensionless student tools
    for tool_file in tools_root.rglob("*"):
        if tool_file.is_file() and not tool_file.suffix and not tool_file.name.startswith((".", "_")):
            shim = scripts_dir / f"{tool_file.name}.cmd"
            shim.write_text(f'@"{sys.executable}" "{tool_file.resolve()}" %*\n')

    # Generate python3.cmd wrapper for Windows
    python3_shim = scripts_dir / "python3.cmd"
    python3_shim.write_text(f'@"{sys.executable}" %*\n')

    # Install the in-process windows runner patch
    try:
        from testagent import windows_compat
        windows_compat.install()
    except ImportError:
        pass


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
    errors = [p for p in problems if p.get("exit_status", "").startswith("Error:") or p.get("exit_status") == "TokenLimitExceeded"]
    if errors:
        print("\n" + "!" * 72, file=sys.stderr)
        print(f" [WARNING] {len(errors)} problem(s) encountered issues in mode '{mode}':", file=sys.stderr)
        for err in errors[:3]:
            print(f"   * {err['problem_id']}: {err['exit_status']}", file=sys.stderr)
        print("!" * 72 + "\n", file=sys.stderr)
        if len(errors) == len(problems):
            print(f"[dev_bench] All problems failed with errors. Aborting evaluation.", file=sys.stderr)
            sys.exit(1)


def run_command(cmd: list[str], description: str) -> None:
    global _active_child_process
    print(f"\n>>> [dev_bench] {description}: {' '.join(cmd)}")
    print(f"[dev_bench] Streaming agent outputs in real-time...\n", flush=True)
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


def run_benchmark(mode: str, run_name: str, problems: list[str], workers: int, notes: str, eval_only: bool, skip_seed: bool = False) -> None:
    sync_windows_shims()
    python_exe = sys.executable

    if not eval_only:
        check_api_key()
        # In separate mode, whitebox benefits from blackbox tests existing.
        if mode == "whitebox":
            target_bb = RUNS_DIR / run_name / "blackbox"
            blackbox_exists = all((target_bb / pid / "tests" / "test_blackbox.py").exists() for pid in problems)

            if not blackbox_exists:
                # Check if a golden baseline exists to inherit fixed blackbox tests from
                baseline_bb = RUNS_DIR / "exp0-baseline" / "blackbox"
                can_inherit = all((baseline_bb / pid / "tests" / "test_blackbox.py").exists() for pid in problems)

                if can_inherit:
                    print(f"[dev_bench] Inheriting seeded black-box tests from 'exp0-baseline' for '{run_name}'...")
                    for pid in problems:
                        src = baseline_bb / pid / "tests" / "test_blackbox.py"
                        dst = target_bb / pid / "tests" / "test_blackbox.py"
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                elif not skip_seed:
                    print(f"[dev_bench] Seeding blackbox tests for run '{run_name}'...")
                    cmd_bb = [python_exe, "-u", "-m", "testagent.run", "--mode", "blackbox", "--run", run_name, "--workers", str(workers), "--only", *problems]
                    run_command(cmd_bb, f"Running black-box pre-requisite for {run_name}")
                    check_agent_errors(run_name, "blackbox")

        cmd_run = [python_exe, "-u", "-m", "testagent.run", "--mode", mode, "--run", run_name, "--workers", str(workers), "--only", *problems]
        run_command(cmd_run, f"Running agent ({mode}) on {len(problems)} benchmark problems")
        check_agent_errors(run_name, mode)

    cmd_eval = [python_exe, "-u", "-m", "testagent.evaluate", "--run", run_name, "--mode", mode, "--only", *problems]
    run_command(cmd_eval, f"Evaluating {mode} tests on benchmark problems")

    results = extract_results(run_name, mode)
    print_console_summary(results)

    markdown_entry = format_markdown_entry(results, notes)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(markdown_entry)
    print(f"[dev_bench] Logged results successfully to {LOG_FILE.name}!")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mode", choices=["whitebox", "blackbox", "combined", "both"], default="whitebox", help="Mode to run (default: whitebox)")
    parser.add_argument("--run", default="exp0-baseline", help="Run name identifier (default: exp0-baseline)")
    parser.add_argument("--workers", type=int, default=None, help="Workers for parallel execution (defaults to number of problems)")
    parser.add_argument("--only", nargs="*", default=None, help="Problem IDs to run (defaults to 4-problem core suite)")
    parser.add_argument("--extended", action="store_true", help="Run full 8-problem benchmark instead of the 4-problem core")
    parser.add_argument("--notes", default="Development benchmark run", help="Brief hypothesis or notes to append to EXPERIMENTS.md")
    parser.add_argument("--eval-only", action="store_true", help="Only evaluate existing run and log without re-running agent")
    parser.add_argument("--skip-seed", action="store_true", help="Skip blackbox seeding when running whitebox mode")
    args = parser.parse_args()

    # Determine problems list
    if args.only:
        problems = args.only
    elif args.extended:
        problems = EXTENDED_PROBLEMS
    else:
        problems = CORE_PROBLEMS

    workers = args.workers if args.workers is not None else len(problems)

    try:
        modes = ["whitebox", "combined"] if args.mode == "both" else [args.mode]
        for m in modes:
            run_benchmark(m, args.run, problems, workers, args.notes, args.eval_only, skip_seed=args.skip_seed)
    except KeyboardInterrupt:
        handle_interrupt()


if __name__ == "__main__":
    main()
