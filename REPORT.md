# Report: Group C

## 1. Team

Andrew Nong 219661537
Ethan Constantin 220287447
Matthew Magagna 219804921
Peyton Hislop 217342957

## 2. Final configuration

Strategy in `student/final.yaml`: `separate`

Our agent has two stages:
1. **Black-box testing**: The agent reads the problem description and function signature. It cannot see the implementation. It chooses inputs, works out expected answers from the requirements, and writes `test_blackbox.py`.
2. **White-box testing**: The agent reads the provided correct implementation and the existing black-box tests. It follows four steps:
   - **Suggest inputs** that test boundaries, equal values, competing choices, and changes during loops.
   - **Run and select inputs** using `select_candidates`. The tool prefers inputs that make the code behave differently from earlier tests.
   - **Write tests** with fixed expected answers taken from the correct implementation's outputs.
   - **Check and submit** the new `test_whitebox.py` file without changing the implementation or black-box tests. If there is no call budget left, submit without adding tests.

We use the assigned Qwen3.5 9B model and unchanged settings. Our tools work offline and make no extra model calls. Submitted agent changes are inside `student/`.

## 3. Prompts and tools

| Part | Mode | What it does | Why it is there |
|---|---|---|---|
| `prompts/blackbox.yaml` | blackbox | Asks for input groups, boundaries, constraint checks, and correct pytest assertions. | Guides testing from the requirements alone. |
| `tools/blackbox/list_constraints` | blackbox | Lists supported input limits and boundary values, including strict inequalities. | Helps avoid inputs outside the allowed range. |
| `tools/blackbox/check_inputs` | blackbox | Checks supported input values, lengths, and relationships between arguments. | Finds known rule violations; marks unsupported checks UNKNOWN. |
| Black-box `check_tests` | blackbox | Finds incorrect assertion methods, different answers for identical inputs, and possible budget overruns; then runs shared checks. | Catches mistakes before submission. |
| `prompts/whitebox.yaml` | whitebox | Directs input generation, selection, checking, and submission. | Gives the agent a clear order of work. |
| `tools/whitebox/select_candidates` | whitebox | Chooses inputs and writes tests within the remaining call budget. | Avoids duplicate inputs and spends calls on different code behavior. |
| `tools/whitebox/_trace_worker.py` | whitebox | Runs inputs twice, records execution, and checks supported constraints. | Supplies expected answers and helps identify changing results. |
| Shared `check_tests`; white-box `run_tests`, `coverage_report` | shared / whitebox | Existing syntax, execution, and coverage checks. | Help validate tests; the new workflow runs pytest directly on the new file. |

The selector first prefers new connections between executed lines. It then considers line order, how often connections execute, and different outputs. These signals guide selection but do not guarantee bug detection. Repeated runs catch some unstable results; timeouts limit expensive exploration.

## 4. Results on the development problems

We compared the saved starter evaluation with our final evaluation for all 61 development problems. The final results are included in the submission as `results/final_evaluation.json`. Neither evaluation capped the number of mutants.

| Metric | Starter baseline | Your final configuration |
|---|---:|---:|
| Bug detection rate | 72.48% | 77.44% |
| Bugs detected | 251/350 | 268/350 |
| Hard-mutant score | 82.84% | 86.50% |
| Hard mutants detected | 185/240 | 186/240 |
| Path coverage | 98.62% | 99.51% |
| Oracle precision | 91.02% | 93.07% |
| Branch coverage | 99.02% | 99.32% |
| Mutation score | 94.29% | 96.62% |
| Tokens per problem | 203,456 | 189,919 |
| Reported cost, USD | 1.303078 | 1.212363 |
| Wrong-oracle labels | 230 | 189 |
| Valid tests | 2,331 | 2,540 |
| Rejected files | 5 | 0 |
| Over-budget tests | 316 | 0 |
| Duplicate-test smells | 65 | 17 |
| Missing-assertion smells | 0 | 1 |

Both runs had zero flaky tests, warnings, and problems without valid tests. Scores average results across problems and can differ from dividing total counts. Tokens per problem are rounded. Oracle precision measures how often generated tests pass on the correct implementation.

The final run saved white-box results for 60 problems. `lcb-3654` stalled, so its black-box tests were evaluated without white-box additions. Eight problems had no black-box file, but white-box produced tests for them. API failures and the interruption mean recorded costs may be incomplete. Model outputs vary between runs, so these results do not prove the same gains will happen every time.

## 5. What we tried

Each arrow compares starter and experimental results on the same problems. Detection columns show counts; path coverage shows evaluator averages.

| Change | Bug detection | Hard-mutant score | Path coverage | Kept? |
|---|---:|---:|---:|---|
| Longer black-box prompt; five problems | 13/27 → 12/27 | 1/7 → 1/7 | 95.29% → 95.29% | No |
| More focused white-box prompt; three problems | 13/19 → 12/19 | 1/1 → 0/1 | 100% → 100% | No |
| Trace selector v3; eight additional problems | 25/45 → 31/45 | 5/12 → 7/12 | 84.87% → 100% | Yes |

**Longer black-box prompt:** We added more explicit test-planning instructions. Oracle precision fell from 96.39% to 89.39%, and token use increased. More instructions did not produce better tests. Sources: `bb-starter-subset-r2` and `bb-prompt-v1-subset-r2`.

**Focused white-box prompt:** We asked for specific code risks, fewer repeated checks, and fewer duplicate tests. It reduced duplicate-test smells but found fewer bugs and hard mutants. Complete coverage was not enough. Sources: `wb-starter-pilot-r1` and `wb-focused-pilot-r1`.

**Trace selector v3:** We added measured input selection and tool-generated expected answers. It introduced no new wrong answers in the eight-problem comparison. Each configuration had an API failure on a different problem. Removing both affected problems still gives 19/34 versus 24/34 bugs, but hard mutants tie at 2/7. V3 also did worse on `lcb-3587`: 8/8 became 5/8 bugs. Sources: `wb-starter-validation8-r1` and `wb-trace-v3-validation8-r1`.

Earlier versions passed matrix arguments incorrectly and sometimes added handwritten tests after the budget was exhausted. V3 clarified argument formatting, corrected call counting, and added a STOP instruction. Local tests, saved-workspace replays, and a model run checked these fixes.

## 6. Design questions

1. Which part of your design improved bug detection the most, and how do you know?

The strongest evidence supports the trace selector and its expected-answer generation. It improved detection on eight additional problems, even after excluding API-affected problems. The full final run found 17 more bugs. However, it also generated more tests and used the call budget differently. We did not measure each feature separately.

2. How does your agent decide on expected values in black-box mode, and how did you reduce wrong ones?

The model works through small legal inputs using the requirements. The harness removes worked examples in this mode. Our checks find supported input violations, conflicting answers, and incorrect assertion methods. After changing an input, the model must calculate its answer again. These checks cannot prove an answer is correct, and our experiments did not show a reliable improvement from black-box changes alone.

3. What does the white-box side of your agent add over the black-box side? With the separate strategy, use
   the evaluator's "black-box tests alone" numbers. With the combined strategy, compare against a run of
   your black-box prompt and tools on their own.

White-box uses the correct implementation to calculate answers during test generation. It writes those answers as constants; submitted tests do not calculate their expected answers from the implementation. On the 53 problems with black-box files, black-box alone detected 179/307 bugs. Adding white-box increased this to 239/307: 60 more detections on the same problems. The overall 268/350 includes eight problems without black-box files, so subtracting 179 directly would be misleading.

4. How does your agent decide which tests to keep within the call budget?

Black-box allows 25 calls; the final suite allows 50. The selector counts calls already used by black-box, then adds tests that fit the remaining allowance. It counts entries from outside the implementation, including constructors and helpers; internal recursive calls do not spend extra entries. It removes duplicate inputs and puts its preferred tests first. When no budget remains, it adds nothing. Black-box source-code counts are estimates because loops and helpers can make several runtime calls.

5. Describe two problems where your agent still does badly, and why, using their trajectories.

**`lcb-3629`:** It found 0/5 bugs despite 100% path coverage. The agent repeatedly exceeded the candidate limit before reducing the list to 80. Two expensive inputs exceeded the trace-event limit. The 50 exported tests passed but missed every realistic bug. The cases did not expose faulty behavior. Larger transformation cases may help, but we cannot confirm the exact missing triggers without inspecting hidden defects.

**`lcb-3627`:** It found 2/6 bugs and 2/9 hard mutants. The agent proposed 47 grid inputs; the tool rejected three and selected 39. Those tests passed, but branch coverage was only 83.33%. Leading candidates added no new execution edges. The input pool left some code decisions untested, showing why more tests and full path-goal coverage do not guarantee strong bug detection.
