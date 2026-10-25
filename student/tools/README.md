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
