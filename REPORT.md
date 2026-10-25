# Report: Group C

## 1. Team

- Andrew Nong — 219661537
- Ethan Constantin — 220287447
- Matthew Magagna — 219804921
- Peyton Hislop — 217342957

## 2. Final configuration

Strategy in `student/final.yaml`: **separate**.

The black-box agent reads the specification and signature, derives expected answers without implementation access, and writes `test_blackbox.py`. The white-box agent reads the provided correct implementation and inherited tests, proposes specification-based candidate inputs, and uses our trace selector to export additional literal assertions into `test_whitebox.py`. It preserves inherited tests and the implementation. The final suite merges both files.

We retain the assigned Qwen3.5 9B model and unchanged settings. Tools are offline; none calls another model or accesses hidden bug/mutant implementations. Only `student/` contains our submitted agent changes.

## 3. Prompts and tools

| Part | Mode | Function and purpose |
|---|---|---|
| `prompts/blackbox.yaml` | Black-box | Requests partitions, boundaries, constraint checks, valid pytest assertions, and rechecking expected answers after input edits. |
| `list_constraints` | Black-box | Extracts supported integer bounds, strict inequalities, dependent constraints, and unsupported rules; avoids suggesting forbidden endpoints. |
| `check_inputs` | Black-box | Checks supported literal arguments, lengths, relationships, and row fields against the specification. Unsupported constraints remain UNKNOWN. |
| Black-box `check_tests` | Black-box | Flags contradictory literal assertions, assertion-method misuse, and possible budget overruns, then delegates to the shared checker. |
| `prompts/whitebox.yaml` | White-box | Requests diverse legal candidates targeting comparisons, ties, competing choices, and state changes; specifies validation and budget-exhaustion submission. |
| `select_candidates` and `_trace_worker.py` | White-box | Measure inherited calls; execute candidates twice; filter known-illegal, duplicate, unstable, or unsupported candidates; rank execution diversity and export fixed expected values. |
| Shared `check_tests`, `run_tests`, `coverage_report` | Shared/white-box | Existing static, execution, and coverage checks. The new workflow validates the new file directly with pytest. |

Selection prioritizes unseen execution edges, ordered line traces, edge-count buckets, and output diversity. These are heuristics: structural novelty does not guarantee bug detection. Subprocess and trace-event limits bound tool execution. Repeated execution checks stability, not every possible source of flakiness.

## 4. Results on the development problems

Sources: starter `runs/my-final/final/evaluation.json`; final `runs/matthew-final-v3/final/evaluation.json`. Both evaluate all 61 development problems without a mutant cap.

| Metric | Starter baseline | Final configuration |
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

Both runs report zero flaky tests, warnings, and problems without valid tests. Rates are evaluator averages across problems, not pooled kill fractions. Tokens per problem are rounded from evaluator totals.

The final evaluation used 60 saved white-box results; `lcb-3654` stalled and was interrupted, leaving its black-box suite. Eight black-box tasks produced no file, but white-box generated suites for them. API accounting failures and interrupted usage can make reported cost incomplete. These are single stochastic runs with different generated black-box tests, not an isolated causal comparison of the selector alone.

## 5. What we tried

Arrows compare unchanged-starter and experimental outputs on matching problem sets. Counts and path coverage come from saved evaluator JSON.

| Change / problem set | Bugs | Hard mutants | Path coverage | Kept? |
|---|---:|---:|---:|---|
| Expanded black-box prompt; five problems | 13/27 → 12/27 | 1/7 → 1/7 | 95.29% → 95.29% | No |
| Focused white-box prompt; three problems | 13/19 → 12/19 | 1/1 → 0/1 | 100% → 100% | No |
| Trace v3; eight additional problems | 25/45 → 31/45 | 5/12 → 7/12 | 84.87% → 100% | Yes |

The first experiment (`bb-starter-subset-r2` versus `bb-prompt-v1-subset-r2`) reduced oracle precision from 96.39% to 89.39% while increasing tokens. More instructions did not reliably improve reasoning.

The second (`wb-starter-pilot-r1` versus `wb-focused-pilot-r1`) reduced duplicate smells but lost detections. Better-looking suites and complete coverage were insufficient.

The third (`wb-starter-validation8-r1` versus `wb-trace-v3-validation8-r1`) introduced no additional wrong answers beyond inherited failures. Each configuration suffered an API failure on a different problem. Excluding both affected problems leaves 19/34 versus 24/34 bugs, with hard mutants tied at 2/7. We therefore do not attribute the raw hard-mutant gain solely to design. V3 also regressed on `lcb-3587`: 8/8 to 5/8 bugs.

Earlier trace versions mishandled matrix arguments and allowed handwritten fallback after budget exhaustion. V3 clarified keyword arguments, corrected external-entry accounting, and added explicit STOP behavior. Local checks and replay against four saved workspaces verified counting; a subsequent model run respected STOP.

## 6. Design questions

**1. What improved detection most?**

Trace-guided selection with executable oracle generation supplied the strongest evidence. The additional eight-problem comparison improved detection despite excluding API-affected pairs, and the full configuration found 17 additional bugs. More candidate tests and better budget use are confounders; we did not isolate each feature through ablation.

**2. How are black-box expected values calculated?**

The model derives exact answers from examples, requirements, and small manually reasoned cases. Constraint and assertion checks catch supported invalid inputs, contradictions, and invocation mistakes; they cannot prove semantic correctness. Expected answers must be recalculated after input changes. We did not establish a reliable standalone black-box detection improvement.

**3. What does white-box add?**

It executes the provided correct implementation during generation and exports its outputs as literals. Submitted tests never compute answers from the implementation dynamically. On the 53 final-run problems with black-box output, the evaluator reports black-box alone detecting 179/307 bugs; the final suites detect 239/307 on those same problems: 60 additional detections. The overall 268/350 result includes eight problems without black-box files, so subtracting 179 directly would be misleading.

**4. How are tests kept within budget?**

Black-box has 25 calls; the final suite has 50. The selector reserves observed inherited external entries, including constructors and externally entered helpers. Internal recursion contributes traces but does not consume another external entry. It filters duplicate inputs and greedily selects candidates whose measured costs fit. If inherited calls exhaust the budget, it exports nothing and instructs submission without changing inherited tests. Black-box static call warnings are estimates, not runtime guarantees.

**5. Where does the final agent perform poorly?**

`lcb-3629` detected 0/5 bugs despite 100% path coverage. Its white-box trajectory repeatedly exceeded the candidate-count limit before truncating to 80; two expensive candidates exceeded the trace-event limit. The exported 50 valid tests missed all realistic bugs. This suggests insufficient semantic/large-transformation diversity; without inspecting hidden defects, we cannot identify the precise missing fault triggers.

`lcb-3627` detected 2/6 bugs and 2/9 hard mutants. The trajectory proposed 47 grid inputs, rejected three, and selected 39 beyond inherited tests. All selected tests passed, but the suite reached only 83.33% branch coverage. Ranking reported no new edges for its leading candidates. The pool did not adequately distinguish remaining pathfinding behavior; full path-goal coverage did not imply complete branch coverage or strong fault detection.
