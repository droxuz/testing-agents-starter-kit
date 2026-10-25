from typing import List
from solution import Solution


class TestCountValidSelections:
    def test_single_zero(self):
        """Single zero element - both directions valid"""
        sol = Solution()
        assert sol.countValidSelections([0]) == 2

    def test_all_zeros_length_2(self):
        """Two zeros - 4 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 0]) == 4

    def test_all_zeros_length_3(self):
        """Three zeros - 6 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 0, 0]) == 6

    def test_all_zeros_length_4(self):
        """Four zeros - 8 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 0, 0, 0]) == 8

    def test_zero_positive(self):
        """[0, 1] - only one valid selection (start at 0, go right)"""
        sol = Solution()
        assert sol.countValidSelections([0, 1]) == 1

    def test_positive_zero(self):
        """[1, 0] - only one valid selection (start at 1, go left)"""
        sol = Solution()
        assert sol.countValidSelections([1, 0]) == 1

    def test_zero_positive_zero(self):
        """[0, 1, 0] - 2 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 1, 0]) == 2

    def test_positive_zero_positive(self):
        """[1, 0, 1] - 2 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([1, 0, 1]) == 2

    def test_zero_positive_zero_positive(self):
        """[0, 1, 0, 1] - 2 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 1, 0, 1]) == 2

    def test_zero_zero_positive(self):
        """[0, 0, 1] - 2 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 0, 1]) == 2

    def test_positive_zero_zero(self):
        """[1, 0, 0] - 1 valid selection"""
        sol = Solution()
        assert sol.countValidSelections([1, 0, 0]) == 1

    def test_no_zeros(self):
        """No zeros - 0 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([1, 2, 3]) == 0

    def test_two_positive_adjacent(self):
        """[0, 1, 1] - 0 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 1, 1]) == 0

    def test_two_positive_adjacent_left(self):
        """[1, 1, 0] - 0 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([1, 1, 0]) == 0

    def test_alternating_zeros_and_positive(self):
        """[0, 1, 0, 1, 0] - 2 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 1, 0, 1, 0]) == 2

    def test_alternating_zeros_and_positive_longer(self):
        """[0, 1, 0, 1, 0, 1] - 2 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 1, 0, 1, 0, 1]) == 2

    def test_single_positive_only(self):
        """[1] - 0 valid selections (no zeros to start)"""
        sol = Solution()
        assert sol.countValidSelections([1]) == 0

    def test_large_positive_value(self):
        """[0, 5] - 0 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 5]) == 0

    def test_multiple_zeros_with_one_positive(self):
        """[0, 0, 1, 0, 0] - 4 valid selections"""
        sol = Solution()
        assert sol.countValidSelections([0, 0, 1, 0, 0]) == 4
