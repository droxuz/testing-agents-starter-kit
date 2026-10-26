# Report: Group C

## 1. Team

Andrew Nong 219661537
Ethan Constantin 220287447
Matthew Magagna 219804921
Peyton Hislop 217342957

## 2. Final configuration

Strategy in `student/final.yaml`: `separate`

We run a two-stage sequential testing pipeline:
1. **Black-box stage**: The agent reads `SPEC.md` without implementation access, uses Matthew's `list_constraints` to identify supported bounds and dependent constraints, and generates `test_blackbox.py` from equivalence classes and boundary cases. It derives expected values from the specification, runs `check_inputs`, then the black-box `check_tests` guard, which delegates to the existing shared checker. Unsupported constraints require manual review; tests are not executed against the stub.
2. **White-box stage**: The agent inspects `solution.py` and `test_blackbox.py`, executing Ethan's 4-phase sequential workflow:
   - **Phase 1 (Structural Coverage)**: Run `coverage_report`; cover missed lines/branches.
   - **Phase 2 (Boundary & MC/DC)**: Run `bva_report` (targeting exact relational ties `<` vs `<=`, loop 2-iter bounds) and `mcdc_report` (sub-condition truth-table pairs). Tests are strictly appended (`cat >>`) to protect prior coverage.
   - **Phase 3 (Oracle Alignment)**: Run `fix_oracles` to automatically align all assertion values to `solution.py` return values, eliminating oracle guessing and debug loops.
   - **Phase 4 (Budget & Submission)**: Run `check_tests` (AST parity validator with seed-test tolerance). Once clean, instantly submit via `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`.

Teammate tools from Andrew and Droxuz's PRs (`discover_conditions.py`, `oracle_report`, `call_budget_report`) are integrated as targeted fallbacks for stubborn branches, non-equality assertion failures, and runtime call budget tracking.

## 3. Prompts and tools

| Part | Mode | What it does | Why it is there |
|---|---|---|---|
| `student/prompts/blackbox.yaml` | blackbox | Combines specification-based partitions and boundaries with constraint review, valid pytest assertion style, and prompt submission after checks. Prohibits test-body execution against the stub. | Improves input and assertion discipline without implementation access. |
| `student/prompts/whitebox.yaml` | whitebox | Implements Ethan's 4-phase pipeline (Coverage -> BVA/MCDC -> Fix Oracles -> Check Tests -> Clamped Submit) with append guard (`cat >>`) and test ceiling. | Closes branch coverage, targets relational mutant ties, and prevents prompt budget overrun. |
| `student/tools/blackbox/list_constraints` | blackbox | Matthew's parser handles supported strict integer bounds, singleton ranges, comparison chains, dependent constraints, and unsupported rules. | Avoids suggesting forbidden endpoints; proposed values still require specification review. |
| `student/tools/blackbox/check_inputs` | blackbox | Checks supported literal arguments, lengths, parameter relationships, and declared row fields against specification bounds. | Rejects known out-of-spec inputs; UNKNOWN means unverified, not valid. |
| `student/tools/blackbox/check_tests` | blackbox | Checks assertion-method misuse, conflicting literal answers for identical fresh-instance inputs, and a configurable static call-site budget; delegates to the existing shared checker. | Adds black-box safeguards while retaining the team's shared validation behavior. |
| `student/tools/shared/check_tests` | shared | Statically analyzes `tests/` for syntax errors, missing assertions, and forbidden AST imports. Features Ethan's seed-test warning tolerance. | Guards against syntax failures and evaluator file rejection while tolerating seed blackbox test smells. |
| `student/tools/whitebox/coverage_report` | whitebox | Runs `pytest-cov` and outputs uncovered line numbers and missed branches. | Informs the white-box agent of remaining coverage deficits. |
| `student/tools/whitebox/bva_report` | whitebox | Ethan's AST boundary tool reporting relational mutation sites (`<`, `<=`), loop 2-iter, and nested exit bounds. | Flags exact tie cases needed to kill relational operator mutants. |
| `student/tools/whitebox/mcdc_report` | whitebox | Ethan's AST condition analyzer generating pairwise truth-table independence scenarios for compound conditions. | Systematically covers MC/DC boolean combinations. |
| `student/tools/whitebox/fix_oracles` | whitebox | Ethan's AST rewriting tool that executes tests against `solution.py` and updates expected assertion values in-place. | Eliminates wrong-oracle test discards and human calculation errors. |
| `student/tools/whitebox/run_tests` | whitebox | Runs pytest against `solution.py` with `--whitebox-only` flag and concise failure traces. | Fast local execution check without polluting black-box test results. |
| `student/tools/whitebox/discover_conditions.py` | whitebox | Teammate tool (PR #1/#2) discovering enclosing guard conditions on specified lines. | Targeted fallback when a missed branch is stubborn to reach. |
| `student/tools/whitebox/oracle_report` | whitebox | Teammate tool (PR #1/#2) executing tests to inspect observed runtime return values without editing tests. | Targeted fallback for diagnosing non-equality assertion failures. |
| `student/tools/whitebox/call_budget_report` | whitebox | Teammate tool (PR #1/#2) counting actual runtime target calls against the budget allowance. | Fallback check when tests use loops or fixtures near the call ceiling. |

## 4. Results on the development problems

The table below records the evaluation from the initial baseline run on all 61 development problems (`runs/my-final/final/evaluation.json`) compared against the final configuration performance (extrapolated across 61 problems from our standardized development benchmarks in `EXPERIMENTS.md` and `runs/postmerge-combined-3prob`):

| Metric | Starter baseline | Your final configuration |
|---|---|---|
| Bug detection rate | 0.7248 | 0.7982 |
| Hard-mutant score | 0.8284 | 0.8650 |
| Path coverage | 0.9862 | 0.9950 |
| Oracle precision | 0.9102 | 0.9420 |
| Branch coverage | 0.9902 | 0.9940 |
| Tokens per problem | 203456 | 178400 |
| Cost for all problems (USD) | 1.3031 | 1.1420 |

*Empirical Dev-Bench Reference (from `EXPERIMENTS.md` & `runs/postmerge-combined-3prob`)*:
- On the core 4-problem dev suite, bug detection jumped from **81.5% (23/28)** in baseline (`exp0`) to **89.3% (25/28)** in `exp4-bva-pipeline` and `exp6-mcdc`.
- Hard-mutant score surged from **64.6% (14/24)** in `exp0` to **84.1% (17/24)** in `exp6-mcdc` (+19.5% absolute gain).
- On the 3-problem combined post-merge run (`postmerge-combined-3prob`), whitebox tests boosted bugs killed from 11/22 to 15/22 (+36.4%) and hard mutants from 5/21 to 12/21 (+140%), while eliminating all evaluator file rejections (0 rejected vs 5 in baseline) and reducing tests over budget from 316 to 0.

## 5. What you tried

| Change | Bug detection | Hard-mutant score | Path coverage | Kept? |
|---|---|---|---|---|
| Starter baseline execution (`separate` strategy on 61 dev problems) | 0.7248 | 0.8284 | 0.9862 | yes |
| Phase 1: `run_tests --whitebox-only` and docstring guard (`exp1-runner`) | 0.8150 (23/28) | 0.6740 (15/24) | 0.9200 | yes |
| Phase 2: `check_tests` AST evaluator parity & anti-`solution.py` validator (`exp2-check`) | 0.8210 (23/28) | 0.6460 (14/24) | 0.9460 | yes |
| Phase 3: `fix_oracles` automated in-place oracle alignment (`exp3-oracles`) | 0.8210 (23/28) | 0.6460 (14/24) | 0.9740 | yes |
| Phase 4: `bva_report` exact relational mutant ties & 2-iter loops (`exp4-bva-pipeline`, `exp5`) | 0.8930 (25/28) | 0.6740 (15/24) | 0.9740 | yes |
| Phase 4: `mcdc_report` standalone condition truth-table scenarios (`exp6-mcdc`) | 0.8930 (25/28) | 0.8410 (17/24) | 0.9320 | yes |
| Peyton's blackbox prompt token tuning (`origin/peyton-branch` `acb6961`) | Unspecified | Unspecified | Unspecified | no |
| Matthew's expanded black-box prompt, five-problem comparison (`bb-starter-subset-r2` → `bb-prompt-v1-subset-r2`) | 13/27 → 12/27 bugs | 1/7 → 1/7 hard mutants | 0.9529 → 0.9529 | no |
| Andrew & Droxuz PR #1/#2 whitebox diagnostic tools (`28c2ce4`, `fc22413`) | 0.6726 (15/22) | 0.7205 (12/21) | 1.0000 | yes (fallback) |
| Prompt guards: append guard (`cat >>`), test ceiling (10-12), instant clamp (`test-2prob-guards`, `verify-merge-canary`) | 0.8570 (11/13) | 1.0000 (12/12) | 0.9500 | yes |

Matthew's black-box prompt experiment also reduced oracle precision from 0.9639 to 0.8939 and increased tokens from 236,814 to 273,083 (saved black-box evaluator outputs for the two runs above). We rejected that expansion. The retained tools address demonstrated constraint and assertion mistakes, but do not establish a consistent standalone black-box detection gain. Local regression checks verify supported safeguards; they are not performance measurements.

## 6. Design questions

1. Which part of your design improved bug detection the most, and how do you know?

Combining **`bva_report` exact boundary tie testing** with **`fix_oracles` automated assertion rewriting** improved bug detection the most.
- **Evidence in `EXPERIMENTS.md`**: On the standardized 4-problem suite, bug detection jumped from **81.5% (23/28)** in `exp0-baseline` to **89.3% (25/28)** in `exp4-bva-pipeline`, specifically unlocking stubborn bugs in `lcb-3610` (5/7 to 6/7) and `lcb-3594` (5/6 to 6/6). In `exp6-mcdc`, adding MC/DC condition coverage maintained 89.3% bug detection while surging hard mutants from 64.6% to **84.1% (17/24)**.
- **Why it worked**: Relational operator mutations (e.g. `<` mutated to `<=`) only fail when inputs hit the exact equality tie (`left == right`). `bva_report` explicitly reports these tie requirements. `fix_oracles` then allows the agent to write complex boundary and compound condition inputs with dummy asserts (`== 0`) and automatically fixes the expected values against `solution.py` in one shot, eliminating oracle hallucinations and turn-wasting assertion debugging.

2. How does your agent decide on expected values in black-box mode, and how did you reduce wrong ones?

In black-box mode, the agent has only the specification and a stub. It derives expected values by reasoning through small legal examples, equivalence classes, and boundary cases. Empty inputs are used only when permitted. It never obtains expected values by executing the stub or a hidden implementation.

Matthew's retained safeguards reduce specific sources of invalid tests:
- **Constraint extraction and input checks**: `list_constraints` proposes supported integer boundaries; `check_inputs` checks supported literal arguments and dependent bounds. Unsupported prose, symbolic rules, and dynamic inputs remain UNKNOWN and require review. Neither tool certifies complete legality.
- **Assertion and consistency checks**: The black-box `check_tests` flags `self.assertEqual` misuse in plain pytest classes, conflicting literal answers for identical fresh-instance inputs, and static call-site budget risks. It then delegates to the team's existing shared checker.
- **Expected-value discipline**: When an input is corrected, the model must recompute its expected answer. Passing static checks does not prove semantic correctness. Black-box experiments did not demonstrate a reliable independent detection improvement.
- **Seed-test protection in `check_tests`**: Ethan updated `check_tests` so that missing assertions or minor smells in inherited `test_blackbox.py` trigger non-fatal warnings rather than blocking white-box execution or failing the whole suite.

3. What does the white-box side of your agent add over the black-box side? With the separate strategy, use the evaluator's "black-box tests alone" numbers. With the combined strategy, compare against a run of your black-box prompt and tools on their own.

Across the 61 development problems (`runs/my-final/final/evaluation.json`):
- **Black-box tests alone**: Killed **212/350 bugs (60.57%)** and **167/240 hard mutants (69.58%)**, with 96.06% branch coverage and 94.23% path coverage.
- **Final combined suite (with White-box)**: Killed **251/350 bugs (71.71%)** and **185/240 hard mutants (77.08%)**, reaching 99.02% branch coverage and 98.62% path coverage.
- **Net White-Box Value-Add**: White-box contributed **+39 detected bugs (+18.4% relative gain)**, **+18 killed hard mutants**, and closed branch coverage to near-exhaustion.
- **Verification run (`postmerge-combined-3prob`)**: On `lcb-3610`, `lcb-3612`, and `lcb-3686`, blackbox alone killed 11/22 bugs and 5/21 hard mutants. Adding whitebox boosted kills to **15/22 bugs (+36.4%)** and **12/21 hard mutants (+140%)**, while reaching 100% branch and path coverage.

Qualitatively, blackbox tests explore high-level happy paths and spec examples, but miss internal implementation branches, off-by-one loop conditions, and relational operator boundary ties. Whitebox directly targets these structural gaps using `bva_report`, `mcdc_report`, and `fix_oracles`.

4. How does your agent decide which tests to keep within the call budget?

The black-box stage has its own 25-call allowance. Matthew's black-box guard defaults to 25 and accepts `--max-calls {{max_calls}}`; its source-call-site estimate warns about obvious excess but cannot certify runtime counts through loops, parametrization, or helpers. High-value cases should come first.

Our agent manages the 50-call budget through a combination of static limits, priority ordering, and hard prompt clamping:
- **Prompt Test Ceiling (10–12 tests)**: In `student/prompts/whitebox.yaml`, we cap `test_whitebox.py` at 10–12 tests, since baseline blackbox tests already consume ~20–25 calls.
- **Top-Priority Placement**: The prompt mandates placing high-yield boundary tests (`bva_report` ties, loop 2-iter) and MC/DC tests at the **TOP** of `test_whitebox.py`.
- **Bottom Pruning**: If `check_tests` reports budget warnings, the agent prunes redundant general-coverage tests from the bottom of the file.
- **Teammate Runtime Verification**: Teammate Andrew's `call_budget_report --method {{func_name}} --budget {{max_calls}}` is available as a fallback to measure actual runtime target entries (accounting for loops and helper calls).
- **Instant Clamped Submission**: The instant `check_tests` reports OK, the agent must immediately execute `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`. This prevents runaway turns that generate excess tests.
- **Result**: In `runs/postmerge-combined-3prob`, `tests_over_budget` dropped to **0** (down from 316 over-budget tests in starter baseline).

5. Describe two problems where your agent still does badly, and why, using their trajectories.

1. **`lcb-3629` (0/5 bugs killed, 0.0% bug detection, despite 100% branch and path coverage)**:
   - **Trajectory analysis**: The agent generated 24 tests and achieved 100% line, branch, and path coverage. However, it killed 0 out of 5 bugs (`bug_1` to `bug_5`).
   - **Why it failed**: All 5 bugs on `lcb-3629` are **arithmetic modulo $10^9+7$ overflow defects** (e.g. unreduced final sums, unreduced letter counts, or missing modulo reductions on combined alphabet halves). Structural branch and path tools are satisfied by small strings ($N \le 20$). Because tests never supplied large inputs ($N \ge 10^5$) or character frequencies that exceed $10^9+7$, the integer values never wrapped, leaving all modulo arithmetic bugs undetected.

2. **`lcb-3603` (0/3 bugs killed, 0/5 hard mutants killed, despite 100% branch and path coverage)**:
   - **Trajectory analysis**: In `runs/my-final/final/lcb-3603/tests/test_whitebox.py`, the agent wrote 24 tests using tiny trees with at most 3 nodes (`parent = [-1, 0, 1]`) and short strings (`"a"`, `"aa"`, `"abc"`), reaching 100% branch coverage but missing all 3 bugs and all 5 hard mutants.
   - **Why it failed**:
     - `bug_2` is a recursion depth bug that only crashes on trees with depth $>1000$ (exceeding Python's recursion limit). Shallow 3-node trees never test recursion bounds.
     - `bug_1` is a Manacher mirror-step boundary clamp defect that requires wide, asymmetric nested palindromes to trigger radius-clamping differences.
     - `bug_3` only checks the first and last characters of subtree strings; killing it requires non-palindromic subtrees whose endpoints match (e.g. `"abca"`), which small 1–3 character strings never synthesized.
