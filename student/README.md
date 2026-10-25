# Matthew's separate testing-agent handoff

This branch contains the black-box safeguards below and the evaluated **trace-v3
white-box workflow**. `final.yaml` selects `separate`. The assigned model and
`settings.yaml` are unchanged. See the repository's `REPORT.md` for the final
comparison, experiment limitations, and team details.

## White-box integration

Keep these files together:

- `prompts/whitebox.yaml`: candidate generation, selection, validation, and submission workflow.
- `tools/whitebox/select_candidates`: executable command that ranks candidates and exports literal pytest assertions.
- `tools/whitebox/_trace_worker.py`: bounded worker for tracing and repeated candidate execution.
- `tools/whitebox/_test_select_candidates.py`: local synthetic regression checks.
- `tools/blackbox/check_inputs` and `list_constraints`: reused for supported input-constraint checks.

The selector reads only task-local specification, provided implementation, and
inherited tests. It uses no network or extra model calls. It reserves inherited
external calls from the shared 50-call budget and explicitly stops when that
budget is exhausted. Unknown constraints remain unverified. Generated tests
contain fixed expected values; they do not import the worker or candidate JSON.

The final 61-problem evaluation detected 268/350 bugs versus the starter's
251/350, with 186/240 versus 185/240 hard mutants and zero over-budget tests.
One white-box task was interrupted; its black-box tests were evaluated. API
failures and stochastic generation limit causal and cost claims. These are
whole-configuration results, not proof of a standalone black-box improvement.

Raw runs, configuration snapshots, and private journals remain ignored under
`runs/` and are not included in this commit. Ask Matthew for the evaluation
artifacts when assembling `results/` and the final submission ZIP.

The following sections preserve the black-box experiments and their limitations.

## Included changes

| File | Purpose |
|---|---|
| `prompts/blackbox.yaml` | Require constraint extraction and input review; request valid pytest assertion style and static consistency/budget checks. |
| `tools/blackbox/list_constraints` | Correct strict integer bounds and singleton candidates; propagate necessary bounds through comparison chains; display dependent and unsupported rules. |
| `tools/blackbox/check_inputs` | Check supported literal inputs against numeric bounds, lengths, parameter relationships, and generic row-field declarations in the specification. |
| `tools/blackbox/check_tests` | Flag unittest assertions in plain pytest classes, contradictory literal expected answers for matching fresh-instance calls, and possible budget overruns; then delegate to the unchanged shared checker. |

The archived `review_tests` duplicate checker is **not** part of this candidate.
The black-box tools are offline. They never read a real implementation or hidden bug data.
The original shared checker still imports test modules for pytest collection;
its test-body execution behavior is unchanged.

## Limitations and integration

- UNKNOWN means unsupported, not valid. Symbolic arithmetic, dynamic inputs,
  helpers, complex control flow, prose requirements, and misspelled specification
  fields may remain unchecked.
- Input legality and internal consistency do not prove expected-answer correctness.
- Budget warnings count source call sites, not actual runtime calls. Loops,
  parametrization, fixtures, helpers, and collection can change actual usage.
- Contradiction checking only supports selected literal equality assertions on
  fresh instances. Stateful calls and dynamic assertions are skipped.
- The black-box `check_tests` shadows the shared command. It also becomes visible
  in combined mode under the existing harness discovery rules. White-box command
  discovery is unchanged. The team should review this when comparing strategies.
- Keep both `check_inputs` and `list_constraints`: the former reuses the latter's
  parser. Keep the original `tools/shared/check_tests` for delegation.
- Checks never automatically repair tests. After changing an input, the agent
  must re-derive the expected answer.

## Measured evidence

All counts below come from actual saved evaluator output. Run names identify
artifacts retained locally; **raw runs and private journal are not committed**.
Ask Matthew for the evaluation JSON/trajectories if needed for the team report.

Earlier three-problem experiments use `lcb-3502`, `lcb-3562`, `lcb-3610`.
The first three rows below are restricted to those IDs, even when the original
run included additional problems.

| Configuration / local run | Bugs caught | Wrong-oracle labels | Over-budget tests | Tokens |
|---|---:|---:|---:|---:|
| Starter: `bb-starter-subset-r1` (three IDs) | 10/19 | 3 | 9 | 237,983 |
| Starter: `bb-starter-subset-r2` (three IDs) | 11/19 | 1 | 0 | 104,114 |
| Repaired constraints + invocation: `bb-constraints-v2-pilot-r1` | 12/19 | 3 | 0 | 268,081 |
| Input checker v1: `bb-input-check-v1-pilot-r1` | 10/19 | 2 | 0 | 201,468 |
| Input checker v1 repeat: `bb-input-check-v1-pilot-r2` | 3/19 | 29 | 0 | 241,971 |
| Assertion-style guard: `bb-input-check-v2-pilot-r1` | 7/19 | 13 | 11 | 202,345 |
| Current candidate: `bb-input-check-v3-smoke-r1` + `bb-input-check-v3-rest2-r1` | 9/19 | 2 | 0 | 245,497 |

The 12/19 constraint-only pilot used 23 illegal interval inputs. It must not be
presented as a specification-compliant improvement. The v1 repeat's 25 failures
on `lcb-3502` were missing `self.assertEqual` methods, not 25 proven arithmetic
mistakes. The evaluator labels runtime failures as wrong oracles too.

Additional five IDs: `lcb-3566`, `lcb-3604`, `lcb-3625`, `lcb-3675`, `lcb-3685`.

| Run | Bugs caught | Hard mutants | Wrong-oracle labels | Over-budget tests | Tokens |
|---|---:|---:|---:|---:|---:|
| Starter: `bb-starter-new5-r1` | 10/24 | 2/5 | 17 | 0 | 239,949 |
| Current candidate: `bb-input-check-v3-new5-r1` | 14/24 | 5/5 | 19 | 1 | 414,192 |

Across eight problems, current candidate totals 23/43 bugs versus composite
starter's 21/43 (starter original-three r2 plus new-five r1). This is confounded:
starter produced no tests on `lcb-3625` after an API accounting error, while the
candidate produced no tests on `lcb-3675` after an API error. Candidate `lcb-3685`
retained usable tests despite an API error later in generation.

On the five problems with valid tests in both configurations, starter catches
18/27 bugs versus candidate's 17/27. This completion-selected comparison is
also descriptive, not an unbiased validation estimate. We have not established
consistent bug-detection gains. These were preliminary black-box experiments; the later full separate run is documented in `REPORT.md`.

### Demonstrated local safeguards

- Constraint extraction previously suggested forbidden endpoints for strict
  inequalities and out-of-range candidates for singleton intervals; these are fixed.
- Input checker feedback caused specific illegal `k > len(s)` and `x > k` cases
  to be corrected in saved agent trajectories.
- Local checks detect all 25 invalid assertion-method calls in the saved plain
  pytest class, and the saved suite with 41 source calls plus conflicting answers.
- Semantic misunderstandings remain the main unresolved limitation. Full coverage
  and successful static review are not sufficient evidence of strong tests.

## Validation and next steps

From the repository root:

```bash
.venv/bin/python -m testagent.submission student
.venv/bin/python student/tools/blackbox/_test_tools.py
.venv/bin/python -m pytest -q
```

For an agent experiment, choose a fresh run name and run `testagent.run` in
black-box mode, followed by `testagent.evaluate` with the same IDs. Do not cap
mutants for report comparisons. Generation uses paid model calls; local tool
checks and evaluation do not. Preserve outputs and configuration for each run.
Recurring API accounting failures need course-approved handling; no model or
settings changes were made to bypass them.

Recommended team decision: compare this candidate with the starter black-box
component in the team's final workflow. Keep negative experiments in the report;
do not claim tool correctness alone improved the main evaluation metrics.
