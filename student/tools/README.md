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

## Optional execution and behavioral diagnostics

These five commands are independent additions for white-box/combined mode. No
prompt YAML is changed to require them. As with every executable tool, the harness
automatically includes their `--help` text in the available-tools description.
They do not call one another's CLI or use evaluator/hidden bug or mutant data.
All support `--json`; execution tools accept `--method NAME` when inference from
SPEC or the sole public `Solution` method is ambiguous.

| Command | Purpose | Default bound |
|---|---|---|
| `oracle_report` | Execute tests; show failing IDs, pytest details, exceptions, and observed reference returns without rewriting assertions | 20 seconds |
| `call_budget_report` | Count actual target entries, by test and file, with an ordered budget projection | 50 calls allowed; 20-second execution |
| `fault_targets` | Suggest source-based arithmetic, update, indexing, initialization, ordering, loop-state, and modulo fault hypotheses | 10 targets |
| `case_probe` | Execute an explicitly supplied JSON candidate set; report results, input changes, and line-transition arcs | 12 candidates; 20 seconds |
| `mutation_probe` | Run tests on locally generated arithmetic, constant, comparison, update, selection, Boolean, and loop-exit mutations | 12 mutants; 4 seconds per suite; 60 seconds overall |

Examples, run from the task workspace:

```bash
oracle_report
call_budget_report --budget 50
fault_targets --method solve --limit 8
case_probe candidates.json --method solve
mutation_probe --method solve --limit 8 --line 12
```

Replace `solve` and line numbers with the actual target. None of these invocations
requires another tool to run first. Runtime tools execute only `tests/test_*.py`,
with external pytest plugins, pytest configuration discovery, and conftest loading
disabled. Inline test fixtures and parametrization work. Temporary request/report
files are confined to the task folder and removed after execution or a timeout.
Tests and the reference source are not rewritten. Private `_runtime.py` and
`_mutations.py` are shared implementation modules, not agent-visible commands.

`call_budget_report` counts loops, helper calls, parametrized invocations, fixture
setup/teardown, and calls made while tests are imported. Recursive target entries
are counted too. The displayed budget boundary uses all observed calls in collection
order; it is not an exact reproduction of evaluator validity/flakiness filtering or
partial-test handling. A failing/skipped path can hide calls that would run after
repair, so rerun after edits. Repeated input previews are hints, not automatic
deduplication: repetition may intentionally test state. Reference module import
itself precedes instrumentation; target calls made inside that module at import
time are not counted. This is separate from target calls in test-module imports,
which are counted.

`oracle_report` diagnoses failures in both test files but never edits either one.
Reference-based observations belong only in white-box/combined mode; they must not
be exposed to black-box generation. Unsupported assertions remain ordinary pytest
assertions: a diagnostic does not silently rewrite them or establish SPEC validity.

`case_probe` accepts a JSON list, for example:

```json
[
  {"label": "tie", "args": [[2, 2]], "kwargs": {}, "expected": 4},
  {"label": "unequal", "args": [[2, 5]], "kwargs": {}}
]
```

Use cases valid for the actual task; the example is only a schema. `expected` is
optional and compared using Python equality. Arguments/results must be compatible
with this JSON interface; arbitrary custom object construction is not supported.
Fresh argument data and a fresh `Solution()` are used per case unless
`--reuse-instance` explicitly requests a sequence on one instance. Module globals
still persist within a probe. Constructors must take no required arguments.
The maximum is 32 candidates and 100 KB of JSON. Output previews are bounded, so
input-change detection can miss changes outside a preview. Coverage arcs are
observed transitions, not a percentage or MC/DC coverage. Arc novelty compares
earlier candidates, not baseline tests; equal arcs do not establish redundant cases.

`mutation_probe` first requires two matching passing reference executions with
observed target calls. It then executes fresh in-memory source variants in isolated
subprocesses. Only the selected declared method (including nested definitions) is
mutated, not arbitrary helper methods. Mutants are generated deterministically and
interleaved across available mutation families; `--line` can focus a source site.
Import/collection failures, timeouts, changed test collections, and other ambiguous
outcomes are reported separately rather than counted as kills. Two baseline runs
are an instability check, not proof of nonflakiness. Equivalent mutants may survive;
the bounded local sample is not the evaluator's mutation or hard-mutant score.
No report from hidden evaluation is read by these tools.
