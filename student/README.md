# Testing agent configuration

Our final configuration uses the **separate** strategy in `final.yaml`: black-box
first, followed by trace-guided white-box testing. We use the assigned Qwen3.5 9B
model and unchanged settings. See `REPORT.md` for the complete results,
experiments, and limitations.

## Workflow

1. The black-box agent reads the specification and function signature without
   seeing the implementation. It chooses input groups and boundaries, calculates
   expected answers from the requirements, and writes `test_blackbox.py`.
2. The white-box agent reads the provided correct implementation and existing
   tests, then suggests additional inputs based on the specification and code.
3. `select_candidates` checks supported input rules and runs each candidate
   twice. It prefers new execution edges, different line orders, different
   execution counts, and different outputs. It also removes duplicate inputs.
4. The tool selects cases within the remaining call budget and writes
   `test_whitebox.py` with fixed expected values. The agent checks the file and
   submits without editing the implementation or black-box tests.

The black-box budget is 25 calls. The final suite shares a 50-call budget. The
selector reserves the calls already used by black-box tests, including entries
into constructors and helpers from outside the implementation. Internal
recursion does not consume another external entry. If inherited tests exhaust
the budget, the selector tells the agent to submit without adding tests.

## Files to keep together

| File | Purpose |
|---|---|
| `prompts/blackbox.yaml` | Guides specification-based tests, input review, and valid pytest assertions. |
| `tools/blackbox/list_constraints` | Extracts supported numeric bounds, strict inequalities, and dependent constraints. |
| `tools/blackbox/check_inputs` | Checks supported literal inputs against specification rules; reuses `list_constraints`. |
| `tools/blackbox/check_tests` | Checks assertion-method mistakes, conflicting answers for identical inputs, and static budget risks; then calls the shared checker. |
| `prompts/whitebox.yaml` | Guides candidate generation, selection, validation, and submission. |
| `tools/whitebox/select_candidates` | Selects inputs and exports ordinary pytest tests with fixed expected values. |
| `tools/whitebox/_trace_worker.py` | Runs bounded measurements, repeated executions, and input checks for the selector. |
| `tools/whitebox/_test_select_candidates.py` | Regression checks for selection, counting, export, and budget exhaustion. |
| `tools/blackbox/_test_tools.py` | Regression checks for the black-box safeguards. |
| `tools/shared/check_tests` | Existing syntax, source-access, assertion, and collection checks. |
| `tools/whitebox/run_tests`, `coverage_report` | Existing execution and coverage tools. The prompt validates new tests directly with pytest. |

All custom tools are offline and make no additional model calls. Black-box
tools do not inspect the real implementation. White-box tools use only the
provided implementation, specification, and tests inside the task workspace.
Generated tests do not import scratch candidate files or the selector worker.

## Measured results

The saved starter and final evaluations each cover all 61 development problems,
without limiting the mutant set. These are the results for this configuration,
not the alternative configuration tested later on the team's main branch.

| Metric | Starter | Final |
|---|---:|---:|
| Bugs detected | 251/350 | 268/350 |
| Hard mutants detected | 185/240 | 186/240 |
| Mutation score | 94.29% | 96.62% |
| Oracle precision | 91.02% | 93.07% |
| Branch coverage | 99.02% | 99.32% |
| Path coverage | 98.62% | 99.51% |
| Wrong-oracle labels | 230 | 189 |
| Over-budget tests | 316 | 0 |
| Rejected files | 5 | 0 |
| Duplicate-test smells | 65 | 17 |

One white-box task, `lcb-3654`, was interrupted; its black-box tests were still
evaluated. Eight black-box tasks produced no file, but white-box generated tests
for them. Every final problem had valid tests. API failures and the interruption
mean recorded costs may be incomplete. Results vary between model runs, and the
full-run difference cannot be attributed to the selector alone.

Earlier black-box experiments did not establish a reliable standalone detection
gain. We retained checks for demonstrated input and assertion mistakes, rather
than claiming that those checks prove better test selection. Unsuccessful
experiments are included in `REPORT.md`.

## Limits

- UNKNOWN means unverified. Unsupported prose rules, symbolic expressions,
  dynamic inputs, and some field relationships require manual review.
- Valid inputs and consistent assertions do not prove expected answers correct.
  Black-box answers must be recalculated whenever an input changes.
- Black-box source-call counts are estimates. Loops, fixtures, parametrization,
  and helpers can change the number of calls made during execution.
- Repeated execution catches some changing results, but does not prove that a
  test will always be stable. Fresh instances do not reset every possible state.
- Different traces and full coverage do not guarantee bug detection. Expensive
  candidates can exceed tool time or trace limits.
- The black-box `check_tests` command takes priority over the shared command in
  black-box and combined modes. Our selected strategy is separate.

## Validate and run

From the repository root, these commands perform local checks without model calls:

```bash
.venv/bin/python -m testagent.submission student
.venv/bin/python student/tools/blackbox/_test_tools.py
.venv/bin/python -m unittest discover -s student/tools/whitebox -p '_test_*.py'
.venv/bin/python -m pytest -q
```

To generate and evaluate a new full run, choose an unused run name:

```bash
.venv/bin/python -m testagent.final --run team-final --workers 8
.venv/bin/python -m testagent.evaluate --run team-final --mode final --workers 8
```

Generation uses paid model calls; evaluation is local. Keep the configuration,
report, and results matched. Preserve failed runs and record retries rather than
selecting whichever attempt has the highest score. Do not change the assigned
model or settings to bypass API accounting failures.

Raw runs, private journals, and submission ZIPs are ignored under `runs/` or by
the ZIP ignore rule. They are not included in Git commits. The official packaging
command copies available evaluation and usage JSON into `results/` inside the
submission ZIP and generated tests into `final_tests/`. The evaluated backup and
its packaging script remain available locally; rebuild the ZIP after changing
the report or documentation intended for that package.
