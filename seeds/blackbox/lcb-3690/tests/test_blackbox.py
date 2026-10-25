import pytest
from solution import Solution


class TestMinLength:
    def test_all_zeros_numops_0(self):
        sol = Solution()
        assert sol.minLength("00000", 0) == 5

    def test_all_zeros_numops_1(self):
        sol = Solution()
        assert sol.minLength("00000", 1) == 3

    def test_all_zeros_numops_2(self):
        sol = Solution()
        assert sol.minLength("00000", 2) == 2

    def test_all_zeros_numops_4(self):
        sol = Solution()
        assert sol.minLength("00000", 4) == 1

    def test_all_zeros_numops_5(self):
        sol = Solution()
        assert sol.minLength("00000", 5) == 1

    def test_all_ones_numops_0(self):
        sol = Solution()
        assert sol.minLength("11111", 0) == 5

    def test_alternating_numops_0(self):
        sol = Solution()
        assert sol.minLength("010101", 0) == 1

    def test_single_char_numops_0(self):
        sol = Solution()
        assert sol.minLength("0", 0) == 1

    def test_single_char_numops_1(self):
        sol = Solution()
        assert sol.minLength("0", 1) == 1

    def test_mixed_runs_numops_0(self):
        sol = Solution()
        assert sol.minLength("00011100", 0) == 3

    def test_mixed_runs_numops_1(self):
        sol = Solution()
        assert sol.minLength("00011100", 1) == 2

    def test_mixed_runs_numops_3(self):
        sol = Solution()
        assert sol.minLength("00011100", 3) == 1

    def test_all_zeros_numops_3(self):
        sol = Solution()
        assert sol.minLength("000000", 3) == 2

    def test_all_zeros_numops_4(self):
        sol = Solution()
        assert sol.minLength("000000", 4) == 2

    def test_all_zeros_numops_5(self):
        sol = Solution()
        assert sol.minLength("000000", 5) == 1

    def test_all_zeros_numops_6(self):
        sol = Solution()
        assert sol.minLength("000000", 6) == 1

    def test_mixed_runs_numops_2(self):
        sol = Solution()
        assert sol.minLength("00011100", 2) == 2

    def test_mixed_runs_numops_4(self):
        sol = Solution()
        assert sol.minLength("00011100", 4) == 1

    def test_all_zeros_numops_7(self):
        sol = Solution()
        assert sol.minLength("0000000", 7) == 1

    def test_all_zeros_numops_0(self):
        sol = Solution()
        assert sol.minLength("0000000", 0) == 7

    def test_all_zeros_numops_1(self):
        sol = Solution()
        assert sol.minLength("0000000", 1) == 4

    def test_all_zeros_numops_2(self):
        sol = Solution()
        assert sol.minLength("0000000", 2) == 3

    def test_all_zeros_numops_3(self):
        sol = Solution()
        assert sol.minLength("0000000", 3) == 2

    def test_all_zeros_numops_4(self):
        sol = Solution()
        assert sol.minLength("0000000", 4) == 2

    def test_all_zeros_numops_5(self):
        sol = Solution()
        assert sol.minLength("0000000", 5) == 2

    def test_all_zeros_numops_6(self):
        sol = Solution()
        assert sol.minLength("0000000", 6) == 2

    def test_all_zeros_numops_7(self):
        sol = Solution()
        assert sol.minLength("0000000", 7) == 1

    def test_all_zeros_numops_8(self):
        sol = Solution()
        assert sol.minLength("0000000", 8) == 1

    def test_all_ones_numops_2(self):
        sol = Solution()
        assert sol.minLength("111111", 2) == 2

    def test_all_ones_numops_5(self):
        sol = Solution()
        assert sol.minLength("111111", 5) == 1

    def test_all_ones_numops_6(self):
        sol = Solution()
        assert sol.minLength("111111", 6) == 1

    def test_all_ones_numops_7(self):
        sol = Solution()
        assert sol.minLength("1111111", 7) == 1

    def test_all_ones_numops_6(self):
        sol = Solution()
        assert sol.minLength("1111111", 6) == 1

    def test_mixed_runs_numops_5(self):
        sol = Solution()
        assert sol.minLength("00011100", 5) == 1
