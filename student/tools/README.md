# Tools

Your agent has one way to act: the `bash` tool that mini-swe-agent gives the model. Every tool
you build is a command line program the agent runs through bash. That is the only way to give the
agent new abilities. MCP servers and extra function-calling tools are not supported.

## Folders

- `blackbox/`: tools available in black-box mode
- `whitebox/`: tools available in white-box mode
- `combined/`: tools available in combined mode, which also sees the black-box and white-box tools
- `shared/`: tools available in every mode

If two visible folders contain a tool with the same name, the mode's own folder wins.

## Rules for a tool

1. It is an executable file (`chmod +x`) with a shebang line, for example `#!/usr/bin/env python3`.
2. `toolname --help` prints a short description and usage. The harness puts this text into the
   prompt automatically, so this is how the agent learns about your tool.
3. It runs inside the task folder. It may read `SPEC.md`, `solution.py` and `tests/`.
4. It must not call any LLM or any network service. All model calls go through the agent.
5. It may only use the Python standard library and the packages in `pyproject.toml`.
6. It must finish within the command timeout in `settings.yaml` and print compact output.
7. In black-box mode it must not try to get at the real implementation.

## Examples included

- `shared/check_tests`: checks syntax, collection and missing assertions without running tests.
- `blackbox/list_constraints`: lists numeric constraints from the spec with boundary values.
- `whitebox/run_tests`: runs the tests against `solution.py`.
- `whitebox/coverage_report`: shows missed lines and branches.

## Independent white-box analysis commands

Run these commands from the task workspace. Each reads the source directly; no
previous report or intermediate file is required. They share parsing functions
internally, but do not launch one another's CLI or run a test-generation pipeline.

| Command | Use when | Default report limit |
|---|---|---|
| `discover_conditions.py` | Locate expression targets, atoms, guards, and structural reach hints | 8 expressions |
| `boundary_values.py` | Request boundary and truth-value hints for a simple or compound expression | 4 expressions |
| `mcdc_targets.py` | Request abstract unique-cause independence pairs | 3 compound expressions |

All three accept `--line N`, `--line N --column K`, or `--target 'ID'`, as well as
`--limit` and `--verbose`. IDs include function, line, and zero-based UTF-8 column.
An explicit MC/DC target may also be a single condition. Quote target IDs in shell
commands. `--max-atoms` bounds MC/DC enumeration (default 6, maximum 8).

For example, once a useful source line is known, call just the relevant command:

```bash
boundary_values.py --line 12
mcdc_targets.py --line 12
```

These are alternative requests, not a required sequence. MC/DC already includes
guard and boundary hints; request separate discovery/BVA output only when it adds
information. The older `bva_report` remains available as a quick comparison scan.

The reports do not execute source, solve inputs, derive expected outputs, measure
coverage, or establish bug detection. Reach requirements are evaluation snapshots,
not a complete control/dataflow proof. Repeated or scalar-equivalent conditions and
shared variables may make abstract pairs infeasible. Potential-effect/exception
flags are nonexhaustive. Validate concrete inputs and results against the contract,
then use the execution/coverage tools. Python `and`/`or` can return operands rather
than booleans; chained-comparison aliases represent shared, once-evaluated values.

Run the analysis regression checks from the repository root with:

```bash
python -m unittest discover -s student/tools/whitebox/_tests -p 'test_*.py'
```

## Runtime call counting and local mutation probing

Two independent runtime commands are retained for white-box/combined mode. Both
accept `--method NAME`, `--timeout SECONDS`, and `--json`. They read task source and
tests only; neither uses hidden bug/mutant data or launches another tool's CLI.

| Command | Purpose | Default bound |
|---|---|---|
| `call_budget_report` | Execute tests and count actual target entries, by test/file, with an ordered budget projection | 50-call allowance; 20 seconds |
| `mutation_probe` | Test locally generated source variants after two passing reference runs | 12 variants; 4 seconds per suite; 60 seconds overall |

Run from the task workspace, replacing `solve` with the target method:

```bash
call_budget_report --method solve --budget 50
mutation_probe --method solve --limit 6 --test-timeout 3 --timeout 30
```

`call_budget_report` includes parameters, loops, helper calls, fixture setup/teardown,
test-module import calls, and recursive target entries. It reports observed calls,
remaining allowance, and cumulative test boundaries. Exit 1 can mean a failing suite
or an exceeded budget; inspect the report. Failed/skipped paths may hide calls, so
rerun after repairs. Counts precede evaluator validity/flakiness filtering and are a
diagnostic projection, not an exact reproduction of evaluator partial-test handling.
Calls during reference-module initialization precede instrumentation and are not
counted. Repeated input previews are hints, not proof of redundant tests.

`mutation_probe` requires two passing reference-suite executions with observed
calls and matching test IDs/outcomes/counts. If preserved baseline tests fail, skip
the probe instead of changing them. It generates deterministic, interleaved AST
variants of the selected method (including nested definitions), executes each in a
fresh subprocess, and leaves source/tests unchanged. `--line N` focuses a source
site; `--limit` is 1-30, `--test-timeout` is 0.1-20 seconds, and `--timeout` is
0.1-100 seconds. Timeouts, invalid runs, changed collections, and inconclusive runs
are distinct from kills. Equivalent mutants may survive; the local sample is not
the evaluator's mutation or hard-mutant score. Two matching reference runs are an
instability check, not proof of nonflakiness.

The shorter white-box prompt prioritizes an early validated test batch, limits
coverage refinement, requires final actual call counting, and makes mutation probing
optional after a passing full suite. Static tools remain independently selectable;
there is no required discovery/BVA/MC/DC/mutation chain. For ordinary failure
diagnosis use `run_tests`; `fix_oracles` remains an optional, limited equality fixer
whose edits require review and subsequent execution.

Private `_runtime.py` provides suite execution, target-call recording, method
selection, and bounded diagnostics; `_mutations.py` generates mutation candidates.
Neither is an agent-visible command. Workers collect only direct `tests/test_*.py`
files, disable external pytest plugins/configuration and conftest loading, and
support inline fixtures and parametrization. Temporary request/report files stay
inside the task folder and are cleaned up on completion/timeout. There is no
candidate-JSON execution interface.
