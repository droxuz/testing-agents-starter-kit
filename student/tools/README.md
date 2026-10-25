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


## Selective white-box analysis

The white-box prompt explains when to choose a tool, what its output means,
and the next useful action. Tool help supplies detailed flags. There is no
mandatory AST -> BVA -> MC/DC sequence; mcdc_targets.py can reuse AST/BVA internally.

- discover_conditions.py: decision atoms and short-circuit guards.
- boundary_values.py: comparison boundary hints; bva_report offers a broad alternative.
- mcdc_targets.py: abstract independence pairs, not solved inputs or measured MC/DC.
- mutation_report: executed feedback from sampled local operator mutants.
  Start with `mutation_report --limit 6`; focus with `--line N --limit 2`.
  JSON shows killed IDs and remaining changes. Fix original test errors before
  interpreting results; only passing tests within the combined call budget can
  kill mutants. Failed original tests still spend calls. Timeouts, errors, and
  skipped/unexecuted tests are inconclusive. A survivor need not be killable.
  Rerun the same sample after additions; different samples have different denominators.
  Use `mutation_report --limit 0 --max-calls 50` to check executed calls without mutation.

Mutation feedback is a small MuTAP-style adaptation, not a reproduction of the
paper's complete implementation. It uses only disposable copies of task-local
source and tests, without benchmark bugs, benchmark mutants, or harness imports.
It leaves the implementation and inherited tests unchanged. Expected results
come from SPEC or an independently checked oracle; fix_oracles is not automatic.
The legacy check_tests budget is a static estimate; use the executed-call report
to catch loops and parametrization. This tool does not establish oracle correctness,
flakiness, achieved MC/DC, or performance against held-out bugs.

Offline tool checks, without model calls:

```bash
python -m unittest discover -s student/tools/whitebox -p _test_mutation_report.py
python -m testagent.submission student
```
