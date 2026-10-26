# Report: Group C

## 1. Team

Andrew Nong 219661537
Ethan Constantin 220287447
Matthew Magagna 219804921
Peyton Hislop 217342957

## 2. Final configuration

Strategy in `student/final.yaml`: `separate`

We run a two-stage sequential testing pipeline:
1. **Black-box stage**: Read the specification and signature without implementation access; derive answers from requirements; run constraint and static checks; write `test_blackbox.py`.
2. **White-box stage**: Inspect the provided correct implementation and inherited tests, then execute our trace-guided workflow:
   - **Phase 1 (Candidate generation)**: Propose legal inputs targeting boundaries, ties, competing choices, and state changes.
   - **Phase 2 (Execution and selection)**: Run `select_candidates`, checking known constraints and repeated outputs, then rank execution diversity against inherited tests.
   - **Phase 3 (Oracle export)**: Export selected inputs as literal assertions in `test_whitebox.py`, preserving inherited tests and implementation.
   - **Phase 4 (Validation and submission)**: Run static checks and pytest on the new file, then submit. If inherited calls exhaust the budget, preserve them and submit without extra tests.

We retain the assigned Qwen3.5 9B model and unchanged settings. Tools are offline; none calls another model or accesses hidden bug/mutant implementations. Only `student/` contains our submitted agent changes.

## 3. Prompts and tools

| Part | Mode | What it does | Why it is there |
|---|---|---|---|
| `student/prompts/blackbox.yaml` | blackbox | Requests partitions, boundaries, constraint review, and valid assertions. | Encourages specification-based tests and rechecking answers after input edits. |
| `student/tools/blackbox/list_constraints` | blackbox | Extracts supported strict integer bounds, comparison chains, and dependent constraints. | Avoids forbidden boundary suggestions; reports unsupported rules. |
| `student/tools/blackbox/check_inputs` | blackbox | Checks supported literal arguments, lengths, relationships, and row fields. | Rejects known input violations; UNKNOWN remains unverified. |
| `student/tools/blackbox/check_tests` | blackbox | Flags assertion-method misuse, conflicting literal answers, and static budget risks; delegates shared checks. | Detects specific input-independent test mistakes. |
| `student/prompts/whitebox.yaml` | whitebox | Directs candidate generation, selection, validation, and budget-exhaustion submission. | Makes implementation-guided refinement reproducible. |
| `student/tools/whitebox/select_candidates` | whitebox | Reserves inherited calls, ranks candidates, and exports fixed expected values. | Uses execution diversity within the remaining budget. |
| `student/tools/whitebox/_trace_worker.py` | whitebox | Bounded subprocess measurement, repeated candidate execution, and constraint checking. | Supports selection while limiting expensive exploration. |
| Shared `check_tests`; white-box `run_tests`, `coverage_report` | shared / whitebox | Existing static, execution, and coverage checks. | Validate suites; the prompt checks new tests directly with pytest. |

Selection prioritizes unseen execution edges, ordered line traces, edge-count buckets, and output diversity. These are heuristics: structural novelty does not guarantee bug detection. Subprocess and trace-event limits bound tool execution. Repeated execution checks stability, not every possible source of flakiness.

## 4. Results on the development problems

Sources: starter `runs/my-final/final/evaluation.json`; final `runs/matthew-final-v3/final/evaluation.json`. Both evaluate all 61 development problems without a mutant cap.

| Metric | Starter baseline | Your final configuration |
|---|---:|---:|
| Bug detection rate | 0.7248 | 0.7744 |
| Bugs detected | 251/350 | 268/350 |
| Hard-mutant score | 0.8284 | 0.8650 |
| Hard mutants detected | 185/240 | 186/240 |
| Path coverage | 0.9862 | 0.9951 |
| Oracle precision | 0.9102 | 0.9307 |
| Branch coverage | 0.9902 | 0.9932 |
| Mutation score | 0.9429 | 0.9662 |
| Tokens per problem | 203,456 | 189,919 |
| Reported cost, USD | 1.303078 | 1.212363 |
| Wrong-oracle labels | 230 | 189 |
| Valid tests | 2,331 | 2,540 |
| Rejected files | 5 | 0 |
| Over-budget tests | 316 | 0 |
| Duplicate-test smells | 65 | 17 |
| Missing-assertion smells | 0 | 1 |

Both runs report zero flaky tests, warnings, and problems without valid tests. Rates are evaluator averages across problems, not pooled kill fractions. Tokens per problem are rounded from evaluator totals.

The final evaluation used 60 saved white-box results; `lcb-3654` stalled and was interrupted, leaving its black-box suite. Eight black-box tasks produced no file, but white-box generated suites for them. API accounting failures and interrupted usage can make reported cost incomplete. These are single stochastic runs with different generated black-box tests, not an isolated causal comparison of the selector alone.

## 5. What we tried

Arrows compare starter and experimental outputs on matching problem sets. Detection columns below show kill counts; path coverage shows evaluator averages. All numbers come from saved evaluator JSON.

| Change | Bug detection | Hard-mutant score | Path coverage | Kept? |
|---|---:|---:|---:|---|
| Expanded black-box prompt; five problems | 13/27 → 12/27 | 1/7 → 1/7 | 95.29% → 95.29% | No |
| Focused white-box prompt; three problems | 13/19 → 12/19 | 1/1 → 0/1 | 100% → 100% | No |
| Trace v3; eight additional problems | 25/45 → 31/45 | 5/12 → 7/12 | 84.87% → 100% | Yes |

The first experiment (`bb-starter-subset-r2` versus `bb-prompt-v1-subset-r2`) reduced oracle precision from 96.39% to 89.39% while increasing tokens. More instructions did not reliably improve reasoning.

The second (`wb-starter-pilot-r1` versus `wb-focused-pilot-r1`) reduced duplicate smells but lost detections. Better-looking suites and complete coverage were insufficient.

The third (`wb-starter-validation8-r1` versus `wb-trace-v3-validation8-r1`) introduced no additional wrong answers beyond inherited failures. Each configuration suffered an API failure on a different problem. Excluding both affected problems leaves 19/34 versus 24/34 bugs, with hard mutants tied at 2/7. We therefore do not attribute the raw hard-mutant gain solely to design. V3 also regressed on `lcb-3587`: 8/8 to 5/8 bugs.

Earlier trace versions mishandled matrix arguments and allowed handwritten fallback after budget exhaustion. V3 clarified keyword arguments, corrected external-entry accounting, and added explicit STOP behavior. Local checks and replay against four saved workspaces verified counting; a subsequent model run respected STOP.

## 6. Design questions

1. Which part of your design improved bug detection the most, and how do you know?

Trace-guided selection with executable oracle generation supplied the strongest evidence. The additional eight-problem comparison improved detection despite excluding API-affected pairs, and the full configuration found 17 additional bugs. More candidate tests and better budget use are confounders; we did not isolate each feature through ablation.

2. How does your agent decide on expected values in black-box mode, and how did you reduce wrong ones?

The model derives exact answers from requirements and small manually reasoned cases. The harness removes worked examples in black-box mode. Constraint and assertion checks catch supported invalid inputs, contradictions, and invocation mistakes; they cannot prove semantic correctness. Expected answers must be recalculated after input changes. We did not establish a reliable standalone black-box detection improvement.

3. What does the white-box side of your agent add over the black-box side? With the separate strategy, use

It executes the provided correct implementation during generation and exports its outputs as literals. Submitted tests never compute answers from the implementation dynamically. On the 53 final-run problems with black-box output, the evaluator reports black-box alone detecting 179/307 bugs; the final suites detect 239/307 on those same problems: 60 additional detections. The overall 268/350 result includes eight problems without black-box files, so subtracting 179 directly would be misleading.

4. How does your agent decide which tests to keep within the call budget?

Black-box has 25 calls; the final suite has 50. The selector reserves observed inherited external entries, including constructors and externally entered helpers. Internal recursion contributes traces but does not consume another external entry. It filters duplicate inputs and greedily selects candidates whose measured costs fit. If inherited calls exhaust the budget, it exports nothing and instructs submission without changing inherited tests. Black-box static call warnings are estimates, not runtime guarantees.

5. Describe two problems where your agent still does badly, and why, using their trajectories.

`lcb-3629` detected 0/5 bugs despite 100% path coverage. Its white-box trajectory repeatedly exceeded the candidate-count limit before truncating to 80; two expensive candidates exceeded the trace-event limit. The exported 50 valid tests missed all realistic bugs. This suggests insufficient semantic/large-transformation diversity; without inspecting hidden defects, we cannot identify the precise missing fault triggers.

`lcb-3627` detected 2/6 bugs and 2/9 hard mutants. The trajectory proposed 47 grid inputs, rejected three, and selected 39 beyond inherited tests. All selected tests passed, but the suite reached only 83.33% branch coverage. Ranking reported no new edges for its leading candidates. The pool did not adequately distinguish remaining pathfinding behavior; full path-goal coverage did not imply complete branch coverage or strong fault detection.
