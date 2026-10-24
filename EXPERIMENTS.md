# Agent Development & Experiment Log

This file tracks rapid-iteration benchmark runs on the standardized 8-problem development subset.
Formal final milestones across all 61 problems should still be recorded in [REPORT.md].

Run `.venv\Scripts\python dev_bench.py --mode whitebox --run exp0-baseline --notes "Starter kit whitebox baseline on 8-problem benchmark"` To run the dev bench for whitebox and have it automatically recorded here.

---

## 1. Standardized 8-Problem Dev Benchmark
The benchmark runs 8 problems in parallel across 8 workers, taking ~2.5–3 minutes total:

| Problem ID | Problem Domain & Focus | Bugs | Hard Mutants | Sol. Lines | Primary Challenge |
|---|---|:---:|:---:|:---:|---|
| **`lcb-3610`** | Sliding window / heap frequency | **7** | 1 | 15 | Window sizes ($k=1, k=n$) and frequency collision ordering. |
| **`lcb-3607`** | Greedy / Number theory / Prime ops | **7** | **9** | 23 | Non-decreasing sequence transitions, off-by-one division. |
| **`lcb-3594`** | Hash map / array arithmetic | **6** | 3 | 21 | Zero sums, negative outliers, identical duplicate values. |
| **`lcb-3566`** | String simulation / State machine | **5** | 0 | 12 | State transitions, string boundaries, termination conditions. |
| **`lcb-3686`** | Prefix arrays / beautiful splits | **8** | **11** | 17 | Partitioning logic, prefix match boundaries, off-by-one indices. |
| **`lcb-3654`** | Dynamic programming / array sum ops | **8** | **15** | 32 | Complex state transitions, division/reduction ordering, knapsack bounds. |
| **`lcb-3612`** | Monotonicity / binary search | **7** | **9** | 14 | Strictly increasing subarray detection, boundary interval checks. |
| **`lcb-3690`** | Binary search on answer / string flips | **8** | **24** | 26 | Maximum substring of identical characters, parity of flips. |
| **Totals** | **Comprehensive Algorithmic Testbed** | **56 bugs** | **72 mutants** | — | **56 realistic bugs, 72 subtle mutants across 8 distinct domains.** |

---

## 2. Experiments & Run History

*(New runs executed via `python dev_bench.py` will append here automatically).*
