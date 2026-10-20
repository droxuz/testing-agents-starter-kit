# Report: Group C

## 1. Team

Andrew Nong 219661537
Ethan Constantin 220287447
Matthew Magagna 219804921
Peyton Hislop 217342957

## 2. Final configuration

Strategy in `student/final.yaml`: separate



## 3. Prompts and tools

These are the default prompts and tools provided in the starter kit:

| Part | Mode | What it does | Why it is there |
|---|---|---|---|
| `student/prompts/blackbox.yaml` | blackbox | Directs the model to write pytest tests from the specification alone. | Initial black-box test generation without implementation bias. |
| `student/prompts/whitebox.yaml` | whitebox | Directs the model to cover missed lines and branches in `solution.py`. | Closes coverage gaps identified after black-box testing. |
| `student/tools/blackbox/list_constraints` | blackbox | Regex parser that lists numeric inequalities and boundary values from `SPEC.md`. | Helps the agent identify numeric range bounds. |
| `student/tools/shared/check_tests` | shared | Statically analyzes `tests/` for syntax errors, missing assertions, and forbidden AST imports. | Guards against syntax failures and evaluator file rejection. |
| `student/tools/whitebox/coverage_report` | whitebox | Runs `pytest-cov` and outputs uncovered line numbers and missed branches. | Informs the white-box agent of remaining coverage deficits. |
| `student/tools/whitebox/run_tests` | whitebox | Runs pytest against `solution.py` with short tracebacks. | Verifies that white-box tests pass on the reference code. |

## 4. Results on the development problems

The table below records the full evaluation from the initial baseline run on all 61 development problems (`runs/my-final/final/evaluation.json`):

| Metric | Starter baseline | Your final configuration |
|---|---|---|
| Bug detection rate | 0.7248 | TBD |
| Hard-mutant score | 0.8284 | TBD |
| Path coverage | 0.9862 | TBD |
| Oracle precision | 0.9102 | TBD |
| Branch coverage | 0.9902 | TBD |
| Tokens per problem | 203456 | TBD |
| Cost for all problems (USD) | 1.3031 | TBD |

## 5. What you tried

| Change | Bug detection | Hard-mutant score | Path coverage | Kept? |
|---|---|---|---|---|
| Starter baseline execution (`separate` strategy on 61 dev problems) | 0.7248 | 0.8284 | 0.9862 | yes |
| TBD | TBD | TBD | TBD | TBD |
| TBD | TBD | TBD | TBD | TBD |

## 6. Design questions

1. Which part of your design improved bug detection the most, and how do you know?

TBD

2. How does your agent decide on expected values in black-box mode, and how did you reduce wrong ones?

TBD

3. What does the white-box side of your agent add over the black-box side? With the separate strategy, use the evaluator's "black-box tests alone" numbers. With the combined strategy, compare against a run of your black-box prompt and tools on their own.

TBD

4. How does your agent decide which tests to keep within the call budget?

TBD

5. Describe two problems where your agent still does badly, and why, using their trajectories.

TBD
