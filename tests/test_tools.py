"""Unit tests for whitebox tools: bva_report, mcdc_report, and check_tests."""

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BVA_REPORT = REPO_ROOT / "student" / "tools" / "whitebox" / "bva_report"
MCDC_REPORT = REPO_ROOT / "student" / "tools" / "whitebox" / "mcdc_report"
CHECK_TESTS = REPO_ROOT / "student" / "tools" / "shared" / "check_tests"
LIST_CONSTRAINTS = REPO_ROOT / "student" / "tools" / "blackbox" / "list_constraints"


def test_bva_report_help():
    res = subprocess.run([sys.executable, str(BVA_REPORT), "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "bva_report" in res.stdout
    assert len(res.stdout.strip().splitlines()) <= 5


def test_bva_report_mutant_sites_and_loop_targets():
    code = """class Solution:
    def example(self, nums: list[int], k: int) -> bool:
        for i in range(len(nums) - 1):
            if nums[i] < nums[i + 1]:
                return True
        for j in range(k):
            for m in range(2):
                if nums[j] == 0:
                    break
        return False
"""
    with tempfile.TemporaryDirectory() as td:
        sol = Path(td) / "solution.py"
        sol.write_text(code)
        res = subprocess.run([sys.executable, str(BVA_REPORT), str(sol)], capture_output=True, text=True)
        assert res.returncode == 0
        out = res.stdout

        # Section 1 mutant-site language
        assert 'MUTANT SITE: "nums[i] < nums[i + 1]" vs "nums[i] <= nums[i + 1]"' in out
        assert "EXACT-TIE:" in out
        assert "JUST-BELOW:" in out

        # Section 3 loop targets
        assert "TWO-ITER" in out
        # Line 3 (for i) has Return -> has EARLY-EXIT and FULL-SCAN
        assert "Line 3 [For]:" in out
        # Line 6 (for j) has an inner loop with break, but j itself has no break or return -> NO EARLY-EXIT
        assert "Line 6 [For]:" in out
        j_block = out[out.find("Line 6 [For]:"):out.find("Line 7 [For]:")]
        assert "TWO-ITER" in j_block
        assert "EARLY-EXIT" not in j_block
        assert "FULL-SCAN" not in j_block

        # Line 7 (for m) has direct break -> has EARLY-EXIT
        m_block = out[out.find("Line 7 [For]:"):]
        assert "TWO-ITER" in m_block
        assert "EARLY-EXIT" in m_block
        assert "FULL-SCAN" in m_block


def test_mcdc_report_help():
    res = subprocess.run([sys.executable, str(MCDC_REPORT), "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "mcdc_report" in res.stdout


def test_mcdc_report_clean_exit_when_no_boolops():
    code = """class Solution:
    def simple(self, x: int) -> int:
        if x > 0:
            return x
        return 0
"""
    with tempfile.TemporaryDirectory() as td:
        sol = Path(td) / "solution.py"
        sol.write_text(code)
        res = subprocess.run([sys.executable, str(MCDC_REPORT), str(sol)], capture_output=True, text=True)
        assert res.returncode == 0
        assert "No compound boolean conditions (and/or) found. No MC/DC tests needed." in res.stdout


def test_mcdc_report_pairwise_scenarios():
    code = """class Solution:
    def check(self, a: int, b: int, c: int) -> bool:
        if a > 0 and b > 0:
            return True
        if a == 0 or b == 0:
            return False
        return True
"""
    with tempfile.TemporaryDirectory() as td:
        sol = Path(td) / "solution.py"
        sol.write_text(code)
        res = subprocess.run([sys.executable, str(MCDC_REPORT), str(sol)], capture_output=True, text=True)
        assert res.returncode == 0
        out = res.stdout

        # And scenarios
        assert "Compound [And] (a > 0 and b > 0)" in out
        assert "ALL-PASS: [a > 0]=True  AND  [b > 0]=True  -> decision = True" in out
        assert "ONLY-C1-FAILS: [a > 0]=False  AND  [b > 0]=True  -> decision = False" in out
        assert "ONLY-C2-FAILS: [a > 0]=True  AND  [b > 0]=False  -> decision = False" in out

        # Or scenarios
        assert "Compound [Or] (a == 0 or b == 0)" in out
        assert "ALL-FAIL: [a == 0]=False  OR  [b == 0]=False  -> decision = False" in out
        assert "ONLY-C1-PASSES: [a == 0]=True  OR  [b == 0]=False  -> decision = True" in out
        assert "ONLY-C2-PASSES: [a == 0]=False  OR  [b == 0]=True  -> decision = True" in out


def test_check_tests_seed_duplicate_tolerance():
    with tempfile.TemporaryDirectory() as td:
        tests_dir = Path(td) / "tests"
        tests_dir.mkdir()
        # Seed file with identical duplicate tests
        (tests_dir / "test_blackbox.py").write_text("""from solution import Solution
def test_one():
    assert Solution().f(1) == 1
def test_one_dup():
    assert Solution().f(1) == 1
""")
        # Whitebox file with unique test
        (tests_dir / "test_whitebox.py").write_text("""from solution import Solution
def test_wb():
    assert Solution().f(2) == 2
""")
        # Solution
        (Path(td) / "solution.py").write_text("""class Solution:
    def f(self, x: int) -> int:
        return x
""")
        res = subprocess.run([sys.executable, str(CHECK_TESTS)], cwd=td, capture_output=True, text=True)
        assert res.returncode == 0
        assert "WARNING tests/test_blackbox.py" in res.stdout
        assert "OK. All checks passed." in res.stdout


def test_list_constraints_help():
    res = subprocess.run([sys.executable, str(LIST_CONSTRAINTS), "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "list_constraints" in res.stdout


def test_list_constraints_minimal_bounds():
    with tempfile.TemporaryDirectory() as td:
        spec = Path(td) / "SPEC.md"
        spec.write_text("Constraints:\n1 <= n <= 100\n0 <= nums[i] <= 10^5\n")
        res = subprocess.run([sys.executable, str(LIST_CONSTRAINTS)], cwd=td, capture_output=True, text=True)
        assert res.returncode == 0
        assert "n: [1, 100] minimal candidates: 1, 2" in res.stdout
        assert "nums[i]: [0, 100000] minimal candidates: 0, 1" in res.stdout


def test_check_tests_blackbox_budget_target_and_cap():
    with tempfile.TemporaryDirectory() as td:
        tests_dir = Path(td) / "tests"
        tests_dir.mkdir()
        (Path(td) / "solution.py").write_text("class Solution:\n    def f(self, x: int) -> int:\n        return x\n")

        # 12 calls (under target 14)
        tests_code_12 = "from solution import Solution\n" + "\n".join(
            f"def test_{i}():\n    assert Solution().f({i}) == {i}" for i in range(12)
        )
        (tests_dir / "test_blackbox.py").write_text(tests_code_12)
        res = subprocess.run([sys.executable, str(CHECK_TESTS)], cwd=td, capture_output=True, text=True)
        assert res.returncode == 0
        assert "Total: 12/14 target, max 25" in res.stdout
        assert "WARNING" not in res.stdout
        assert "OK. All checks passed." in res.stdout

        # 15 calls (exceed target 14, under cap 25 -> warning, exit code 0)
        tests_code_15 = "from solution import Solution\n" + "\n".join(
            f"def test_{i}():\n    assert Solution().f({i}) == {i}" for i in range(15)
        )
        (tests_dir / "test_blackbox.py").write_text(tests_code_15)
        res = subprocess.run([sys.executable, str(CHECK_TESTS)], cwd=td, capture_output=True, text=True)
        assert res.returncode == 0
        assert "WARNING: 15 calls exceed optimal 12-14 target!" in res.stdout
        assert "OK. All checks passed." in res.stdout

        # 26 calls (exceed cap 25 -> error, non-zero exit)
        tests_code_26 = "from solution import Solution\n" + "\n".join(
            f"def test_{i}():\n    assert Solution().f({i}) == {i}" for i in range(26)
        )
        (tests_dir / "test_blackbox.py").write_text(tests_code_26)
        res = subprocess.run([sys.executable, str(CHECK_TESTS)], cwd=td, capture_output=True, text=True)
        assert res.returncode != 0
        assert "ERROR: 26 calls exceed black-box limit of 25!" in res.stdout
        assert "FAILED: 1 issue(s) must be fixed before submission." in res.stdout


def test_submission_main():
    from testagent.submission import main as sub_main
    assert sub_main(["student"]) == 0


def test_list_constraints_missing_spec():
    with tempfile.TemporaryDirectory() as td:
        res = subprocess.run([sys.executable, str(LIST_CONSTRAINTS)], cwd=td, capture_output=True, text=True)
        assert res.returncode == 1
        assert "ERROR: SPEC.md not found." in res.stdout


def test_list_constraints_equal_bounds_and_negative():
    with tempfile.TemporaryDirectory() as td:
        spec = Path(td) / "SPEC.md"
        spec.write_text("Constraints:\n1 <= k <= 1\n-10^4 <= val <= -10^4\n")
        res = subprocess.run([sys.executable, str(LIST_CONSTRAINTS)], cwd=td, capture_output=True, text=True)
        assert res.returncode == 0
        assert "k: [1, 1] minimal candidates: 1\n" in res.stdout
        assert "val: [-10000, -10000] minimal candidates: -10000\n" in res.stdout

