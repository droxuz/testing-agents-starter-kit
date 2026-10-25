"""Unit tests for whitebox tools: bva_report, mcdc_report, and check_tests."""

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BVA_REPORT = REPO_ROOT / "student" / "tools" / "whitebox" / "bva_report"
MCDC_REPORT = REPO_ROOT / "student" / "tools" / "whitebox" / "mcdc_report"
CHECK_TESTS = REPO_ROOT / "student" / "tools" / "shared" / "check_tests"


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
