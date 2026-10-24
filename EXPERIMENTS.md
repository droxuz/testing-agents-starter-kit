# Agent Development & Experiment Log

This file tracks rapid-iteration benchmark runs on the standardized development subset.
Formal final milestones across all 61 problems should still be recorded in [REPORT.md](REPORT.md).

---

## ⚡ Command Cheatsheet & Workflow Quick-Reference

### 1. Establish the Golden Baseline (Run Once)
Seeds black-box tests and records the initial starter kit metrics:
```bash
python dev_bench.py --run exp0-baseline --notes "Starter kit baseline"
```

### 2. Test a Feature / Prompt Improvement (Standard Workflow)
Isolates your white-box feature against the fixed black-box seed without stochastic noise:
```bash
python dev_bench.py --mode whitebox --run exp1-<feature> --skip-seed --notes "Added boundary value prompting"
```

### 3. Ultra-Fast Canary Check (~15s on single problem)
Quickly test if your tool or prompt works without syntax errors before a full run:
```bash
python dev_bench.py --mode whitebox --run test-canary --only lcb-3566 --skip-seed
```

### 4. Milestone Verification (Full 8-problem extended suite, ~2.5m)
Verify your changes generalize across all 8 problem domains before committing:
```bash
python dev_bench.py --extended --run exp1-<feature>-extended --notes "Extended suite verification"
```

### 5. Check Grading Rule Compliance
Ensure only allowed files inside `student/` were modified and tools meet requirements:
```bash
python -m testagent.submission student
```

---

## 📋 Benchmark Problem Suites

### Core 4-Problem Suite (Default, fast & robust, ~1–2m across 4 workers)
Focused rapid-iteration testbed: **28 realistic bugs, 24 subtle mutants**. Zero reasoning traps.

| Problem ID | Problem Domain & Focus | Bugs | Hard Mutants | Sol. Lines | Primary Challenge |
|---|---|:---:|:---:|:---:|---|
| **`lcb-3610`** | Sliding window / heap frequency | **7** | 1 | 15 | Window sizes ($k=1, k=n$) and frequency collision ordering. |
| **`lcb-3612`** | Monotonicity / binary search | **7** | **9** | 14 | Strictly increasing subarray detection, boundary interval checks. |
| **`lcb-3686`** | Prefix arrays / beautiful splits | **8** | **11** | 17 | Partitioning logic, prefix match boundaries, off-by-one indices. |
| **`lcb-3594`** | Hash map / array arithmetic | **6** | 3 | 21 | Zero sums, negative outliers, identical duplicate values. |

### Extended 8-Problem Suite (`--extended`, ~3m across 8 workers)
Broader validation testbed: **56 realistic bugs, 72 subtle mutants**.

| Problem ID | Problem Domain & Focus | Bugs | Hard Mutants | Sol. Lines | Primary Challenge |
|---|---|:---:|:---:|:---:|---|
| **`lcb-3566`** | String simulation / State machine | **5** | 0 | 12 | State transitions, string boundaries, termination conditions. |
| **`lcb-3654`** | Dynamic programming / array sum ops | **8** | **15** | 32 | Complex state transitions, division/reduction ordering, knapsack bounds. |
| **`lcb-3607`** | Greedy / Number theory / Prime ops | **7** | **9** | 23 | Non-decreasing sequence transitions, off-by-one division. |
| **`lcb-3690`** | Binary search on answer / string flips | **8** | **24** | 26 | Maximum substring of identical characters, parity of flips. |

---

## 🔬 Experiments & Run History

*(New runs executed via python dev_bench.py will append here automatically).
