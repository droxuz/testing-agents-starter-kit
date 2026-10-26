# Agent Development & Experiment Log

This file tracks rapid-iteration benchmark runs on the standardized development subset.
Formal final milestones across all 61 problems should still be recorded in [REPORT.md](REPORT.md).

---

## ⚡ Command Cheatsheet & Workflow Quick-Reference

### 1. Standard Dev Iteration (Default: 4 Core Problems, ~1.5–2m across 4 workers)
Runs the standardized 4-problem core suite (`lcb-3610`, `lcb-3612`, `lcb-3686`, `lcb-3594`) using instant pre-seeded black-box tests:
```bash
python dev_bench.py --run exp1-<feature> --notes "Added boundary value prompting"
```

### 2. Ultra-Fast Canary Check (~20s on single problem)
Quickly test if your tool or prompt works without syntax errors before a full benchmark:
```bash
python dev_bench.py --canary --run test-canary
```

### 3. Extended Milestone Verification (8 Problems, ~3–4m across 4 workers)
Run full 8-problem milestone suite to verify broader generalization:
```bash
python dev_bench.py --extended --run exp1-<feature>-extended --notes "Extended suite verification"
```

### 4. Check Grading Rule Compliance
Ensure only allowed files inside `student/` were modified and tools meet requirements:
```bash
python -m testagent.submission student
```

---

## 📋 Benchmark Problem Suites

### Core 4-Problem Suite (Default, ~1.5–2m across 4 workers)
Balanced, statistically rigorous testbed with **28 realistic bugs, 24 subtle hard mutants, zero reasoning traps**:

| Problem ID | Problem Domain & Focus | Bugs | Hard Mutants | Sol. Lines | Primary Challenge |
|---|---|:---:|:---:|:---:|---|
| **`lcb-3610`** | Sliding window / heap frequency | **7** | 1 | 15 | Window sizes ($k=1, k=n$) and frequency collision ordering. |
| **`lcb-3612`** | Monotonicity / binary search | **7** | **9** | 14 | Strictly increasing subarray detection, boundary interval checks. |
| **`lcb-3686`** | Prefix arrays / beautiful splits | **8** | **11** | 17 | Partitioning logic, prefix match boundaries, off-by-one indices. |
| **`lcb-3594`** | Hash map / array arithmetic | **6** | 3 | 21 | Zero sums, negative outliers, identical duplicate values. |
| **Totals** | **4 Distinct Algorithmic Domains** | **28 bugs** | **24 hard mutants** | — | **Granular bug detection and hard mutant score evaluation.** |

### Extended 8-Problem Suite (`--extended`, ~3–4m across 4 workers)
Broader validation testbed with **56 realistic bugs, 72 subtle mutants**:
Includes the 4 core problems plus `lcb-3566` (strings), `lcb-3654` (DP), `lcb-3607` (greedy/primes), and `lcb-3690` (binary search flips).

---

## 🔬 Experiments & Run History

*(New runs executed via python dev_bench.py will append here automatically).

### Experiment: `exp0-baseline` (whitebox)
- **Timestamp:** 2026-10-24 19:42:09
- **Notes / Hypothesis:** Starter kit baseline (4-problem core dev suite)
- **Cost / Tokens:** $0.0463 | 445,222 tokens
- **Total Function Calls Used:** 134

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **81.5% (23/28)** | Primary Goal |
| **Hard-Mutant Score** | **64.6% (14/24)** | High-Yield Mutants |
| **Path Coverage** | 95.8% | Branch/Path Exhaustion |
| **Branch Coverage** | 100.0% | Structural Coverage |
| **Oracle Precision** | 94.9% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 21 | 0 | 5/6 | 1/3 | 21 | 100.0% |
| `lcb-3610` | 25 | 1 | 5/7 | 1/1 | 26 | 100.0% |
| `lcb-3612` | 48 | 6 | 5/7 | 8/9 | 50 | 100.0% |
| `lcb-3686` | 37 | 0 | 8/8 | 4/11 | 37 | 100.0% |

---

### Experiment: `exp1-runner` (whitebox)
- **Timestamp:** 2026-10-24 20:56:15
- **Notes / Hypothesis:** Phase 1: run_tests whitebox-only flag with docstring guard
- **Cost / Tokens:** $0.0525 | 506,940 tokens
- **Total Function Calls Used:** 127

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **81.5% (23/28)** | Primary Goal |
| **Hard-Mutant Score** | **67.4% (15/24)** | High-Yield Mutants |
| **Path Coverage** | 92.0% | Branch/Path Exhaustion |
| **Branch Coverage** | 97.5% | Structural Coverage |
| **Oracle Precision** | 95.2% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 18 | 0 | 5/6 | 1/3 | 18 | 90.0% |
| `lcb-3610` | 31 | 1 | 4/7 | 1/1 | 32 | 100.0% |
| `lcb-3612` | 63 | 5 | 6/7 | 9/9 | 50 | 100.0% |
| `lcb-3686` | 26 | 1 | 8/8 | 4/11 | 27 | 100.0% |

---

### Experiment: `exp2-check` (whitebox)
- **Timestamp:** 2026-10-24 21:51:43
- **Notes / Hypothesis:** Phase 2: check_tests evaluator parity validator
- **Cost / Tokens:** $0.0397 | 389,305 tokens
- **Total Function Calls Used:** 114

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **82.1% (23/28)** | Primary Goal |
| **Hard-Mutant Score** | **64.6% (14/24)** | High-Yield Mutants |
| **Path Coverage** | 94.6% | Branch/Path Exhaustion |
| **Branch Coverage** | 100.0% | Structural Coverage |
| **Oracle Precision** | 94.7% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 26 | 0 | 6/6 | 1/3 | 26 | 100.0% |
| `lcb-3610` | 27 | 1 | 4/7 | 1/1 | 28 | 100.0% |
| `lcb-3612` | 36 | 5 | 5/7 | 8/9 | 41 | 100.0% |
| `lcb-3686` | 19 | 0 | 8/8 | 4/11 | 19 | 100.0% |

---

### Experiment: `exp3-oracles` (whitebox)
- **Timestamp:** 2026-10-24 22:45:12
- **Notes / Hypothesis:** Phase 3: fix_oracles in-place alignment
- **Cost / Tokens:** $0.0458 | 448,723 tokens
- **Total Function Calls Used:** 124

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **82.1% (23/28)** | Primary Goal |
| **Hard-Mutant Score** | **64.6% (14/24)** | High-Yield Mutants |
| **Path Coverage** | 97.4% | Branch/Path Exhaustion |
| **Branch Coverage** | 100.0% | Structural Coverage |
| **Oracle Precision** | 95.2% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 26 | 0 | 6/6 | 1/3 | 26 | 100.0% |
| `lcb-3610` | 25 | 1 | 3/7 | 1/1 | 26 | 100.0% |
| `lcb-3612` | 35 | 5 | 6/7 | 8/9 | 40 | 100.0% |
| `lcb-3686` | 32 | 0 | 8/8 | 4/11 | 32 | 100.0% |

> **Note / Footnote:** No significant metric improvement was expected on this 4-problem dev benchmark suite because whitebox tests for these 4 problems already had zero wrong oracles (the 6 remaining wrong oracles in the table are inherited from the pre-seeded blackbox tests). However, `fix_oracles` is expected to make a measurable difference on the full 61-problem benchmark suite, specifically on the key problems where wrong oracles are prevalent (which accounted for 31+ discarded whitebox tests in the baseline run).

---
### Experiment: `exp4-bva-pipeline` (whitebox)
- **Timestamp:** 2026-10-24 23:28:00
- **Notes / Hypothesis:** Phase 4: bva_report comprehensive boundary analysis and full pipeline
- **Cost / Tokens:** $0.0356 | 350,181 tokens
- **Total Function Calls Used:** 126

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **89.3% (25/28)** | Primary Goal |
| **Hard-Mutant Score** | **67.4% (15/24)** | High-Yield Mutants |
| **Path Coverage** | 97.4% | Branch/Path Exhaustion |
| **Branch Coverage** | 100.0% | Structural Coverage |
| **Oracle Precision** | 95.2% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 26 | 0 | 6/6 | 1/3 | 26 | 100.0% |
| `lcb-3610` | 29 | 1 | 6/7 | 1/1 | 30 | 100.0% |
| `lcb-3612` | 30 | 5 | 5/7 | 9/9 | 35 | 100.0% |
| `lcb-3686` | 35 | 0 | 8/8 | 4/11 | 35 | 100.0% |

---


### Experiment: `exp5-bva-loop` (whitebox)
- **Timestamp:** 2026-10-25 17:23:41
- **Notes / Hypothesis:** BVA mutant-site language and 2-iter loop BVA
- **Cost / Tokens:** $0.0503 | 494,552 tokens
- **Total Function Calls Used:** 149

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **78.6% (22/28)** | Primary Goal |
| **Hard-Mutant Score** | **59.1% (16/24)** | High-Yield Mutants |
| **Path Coverage** | 98.7% | Branch/Path Exhaustion |
| **Branch Coverage** | 100.0% | Structural Coverage |
| **Oracle Precision** | 96.0% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 39 | 0 | 6/6 | 3/3 | 39 | 100.0% |
| `lcb-3610` | 28 | 1 | 3/7 | 0/1 | 29 | 100.0% |
| `lcb-3612` | 33 | 5 | 5/7 | 9/9 | 38 | 100.0% |
| `lcb-3686` | 43 | 0 | 8/8 | 4/11 | 43 | 100.0% |

---

### Experiment: `exp6-mcdc` (whitebox)
- **Timestamp:** 2026-10-25 17:43:09
- **Notes / Hypothesis:** Standalone mcdc_report tool and whitebox pipeline integration
- **Cost / Tokens:** $0.0465 | 450,046 tokens
- **Total Function Calls Used:** 151

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **89.3% (25/28)** | Primary Goal |
| **Hard-Mutant Score** | **84.1% (17/24)** | High-Yield Mutants |
| **Path Coverage** | 93.2% | Branch/Path Exhaustion |
| **Branch Coverage** | 97.5% | Structural Coverage |
| **Oracle Precision** | 94.0% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 38 | 3 | 6/6 | 3/3 | 41 | 90.0% |
| `lcb-3610` | 34 | 1 | 5/7 | 1/1 | 35 | 100.0% |
| `lcb-3612` | 32 | 5 | 6/7 | 9/9 | 37 | 100.0% |
| `lcb-3686` | 38 | 0 | 8/8 | 4/11 | 38 | 100.0% |

---

### Experiment: `exp7-final-extended` (whitebox)
- **Timestamp:** 2026-10-25 18:15:40
- **Notes / Hypothesis:** Extended 8-problem suite after BVA and MCDC enhancements
- **Cost / Tokens:** $0.1085 | 1,056,120 tokens
- **Total Function Calls Used:** 339

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **74.3% (41/56)** | Primary Goal |
| **Hard-Mutant Score** | **81.5% (54/72)** | High-Yield Mutants |
| **Path Coverage** | 97.6% | Branch/Path Exhaustion |
| **Branch Coverage** | 98.8% | Structural Coverage |
| **Oracle Precision** | 87.0% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3566` | 16 | 20 | 5/5 | 0/0 | 36 | 100.0% |
| `lcb-3594` | 27 | 7 | 5/6 | 3/3 | 34 | 90.0% |
| `lcb-3607` | 36 | 9 | 5/7 | 9/9 | 49 | 100.0% |
| `lcb-3610` | 34 | 3 | 4/7 | 1/1 | 37 | 100.0% |
| `lcb-3612` | 34 | 5 | 4/7 | 9/9 | 39 | 100.0% |
| `lcb-3654` | 44 | 3 | 5/8 | 7/15 | 47 | 100.0% |
| `lcb-3686` | 47 | 0 | 8/8 | 4/11 | 47 | 100.0% |
| `lcb-3690` | 142 | 10 | 5/8 | 21/24 | 50 | 100.0% |

---

### Experiment: `exp8-post-fixes` (whitebox)
- **Timestamp:** 2026-10-25 19:03:41
- **Notes / Hypothesis:** Post-eafbcde fixes: oracle ordering, nested loop exits, seed tolerance
- **Cost / Tokens:** $0.0534 | 521,317 tokens
- **Total Function Calls Used:** 149

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **78.6% (22/28)** | Primary Goal |
| **Hard-Mutant Score** | **84.1% (17/24)** | High-Yield Mutants |
| **Path Coverage** | 96.0% | Branch/Path Exhaustion |
| **Branch Coverage** | 97.5% | Structural Coverage |
| **Oracle Precision** | 89.7% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 47 | 10 | 6/6 | 3/3 | 50 | 90.0% |
| `lcb-3610` | 26 | 1 | 5/7 | 1/1 | 27 | 100.0% |
| `lcb-3612` | 30 | 5 | 3/7 | 9/9 | 35 | 100.0% |
| `lcb-3686` | 37 | 0 | 8/8 | 4/11 | 37 | 100.0% |

---

### Experiment: `test-2prob-guards` (whitebox)
- **Timestamp:** 2026-10-25 19:27:59
- **Notes / Hypothesis:** Verify append guard and instant submit on lcb-3594 and lcb-3612
- **Cost / Tokens:** $0.0279 | 267,852 tokens
- **Total Function Calls Used:** 95

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **85.7% (11/13)** | Primary Goal |
| **Hard-Mutant Score** | **100.0% (12/12)** | High-Yield Mutants |
| **Path Coverage** | 95.0% | Branch/Path Exhaustion |
| **Branch Coverage** | 100.0% | Structural Coverage |
| **Oracle Precision** | 94.0% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3594` | 44 | 1 | 6/6 | 3/3 | 45 | 100.0% |
| `lcb-3612` | 50 | 5 | 5/7 | 9/9 | 50 | 100.0% |

---

### Experiment: `verify-merge-canary` (whitebox)
- **Timestamp:** 2026-10-25 20:54:11
- **Notes / Hypothesis:** Development benchmark run
- **Cost / Tokens:** $0.0154 | 152,431 tokens
- **Total Function Calls Used:** 32

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **100.0% (5/5)** | Primary Goal |
| **Hard-Mutant Score** | **0.0% (0/0)** | High-Yield Mutants |
| **Path Coverage** | 100.0% | Branch/Path Exhaustion |
| **Branch Coverage** | 100.0% | Structural Coverage |
| **Oracle Precision** | 37.5% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3566` | 12 | 20 | 5/5 | 0/0 | 32 | 100.0% |

---

### Experiment: `exp-bb-baseline` (blackbox)
- **Timestamp:** 2026-10-25 22:17:36
- **Notes / Hypothesis:** Pre-improvement baseline blackbox seeds
- **Cost / Tokens:** $0.0000 | 0 tokens
- **Total Function Calls Used:** 50

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **23.8% (5/19)** | Primary Goal |
| **Hard-Mutant Score** | **38.9% (7/10)** | High-Yield Mutants |
| **Path Coverage** | 64.6% | Branch/Path Exhaustion |
| **Branch Coverage** | 66.7% | Structural Coverage |
| **Oracle Precision** | 48.0% | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3566` | 0 | 20 | 0/5 | 0/0 | 20 | 0.0% |
| `lcb-3610` | 12 | 1 | 2/7 | 0/1 | 13 | 100.0% |
| `lcb-3612` | 12 | 5 | 3/7 | 7/9 | 17 | 100.0% |

---

### Experiment: `exp-bb-test` (blackbox)
- **Timestamp:** 2026-10-25 22:54:35
- **Notes / Hypothesis:** Blackbox minimal oracle test (recovered & evaluated on lcb-3610 and lcb-3612)
- **Cost / Tokens:** $0.0080 | 75,080 tokens
- **Total Function Calls Used:** 26

| Metric | Result | Target / Baseline |
|---|---|---|
| **Bug Detection Rate** | **64.3% (9/14)** | Primary Goal (Baseline: 35.7% (5/14)) |
| **Hard-Mutant Score** | **80.0% (8/10)** | High-Yield Mutants (Baseline: 70.0% (7/10)) |
| **Path Coverage** | 100.0% | Branch/Path Exhaustion |
| **Branch Coverage** | 100.0% | Structural Coverage |
| **Oracle Precision** | 88.5% (23/26) | Test Correctness |

#### Per-Problem Breakdown
| Problem | Valid Tests | Wrong Oracle | Bugs Killed | Hard Mutants | Calls Used | Branch Cov |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `lcb-3610` | 12 | 2 | 4/7 | 0/1 | 14 | 100.0% |
| `lcb-3612` | 11 | 1 | 5/7 | 8/9 | 12 | 100.0% |

---

