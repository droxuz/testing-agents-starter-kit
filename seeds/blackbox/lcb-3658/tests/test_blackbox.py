from typing import List
from solution import Solution


class TestMinDifference:
    """Tests for minDifference function."""

    def test_no_missing_elements(self):
        """Test with no missing elements."""
        sol = Solution()
        # [1, 3, 5] -> max(|3-1|, |5-3|) = max(2, 2) = 2
        assert sol.minDifference([1, 3, 5]) == 2

    def test_all_missing_length_2(self):
        """Test with all missing elements, length 2."""
        sol = Solution()
        # [-1, -1] -> choose x=1, y=1 -> [1, 1] -> max diff = 0
        assert sol.minDifference([-1, -1]) == 0

    def test_single_missing_middle(self):
        """Test with single missing element in middle."""
        sol = Solution()
        # [1, -1, 5] -> best is [1, 3, 5] -> max(|3-1|, |5-3|) = 2
        assert sol.minDifference([1, -1, 5]) == 2

    def test_single_missing_at_end(self):
        """Test with single missing element at end."""
        sol = Solution()
        # [1, 3, -1] -> best is [1, 3, 5] -> max(|3-1|, |5-3|) = 2
        assert sol.minDifference([1, 3, -1]) == 2

    def test_single_missing_at_start(self):
        """Test with single missing element at start."""
        sol = Solution()
        # [-1, 3, 5] -> best is [1, 3, 5] -> max(|3-1|, |5-3|) = 2
        assert sol.minDifference([-1, 3, 5]) == 2

    def test_two_adjacent_missing(self):
        """Test with two adjacent missing elements."""
        sol = Solution()
        # [1, -1, -1, 5] -> best is [1, 3, 3, 5] -> max diff = 2
        assert sol.minDifference([1, -1, -1, 5]) == 2

    def test_two_non_adjacent_missing(self):
        """Test with two non-adjacent missing elements."""
        sol = Solution()
        # [1, -1, 5, -1, 10] -> best is [1, 3, 5, 7, 10] -> max diff = 3
        assert sol.minDifference([1, -1, 5, -1, 10]) == 3

    def test_all_missing_length_3(self):
        """Test with all missing elements, length 3."""
        sol = Solution()
        # [-1, -1, -1] -> choose x=1, y=1 -> [1, 1, 1] -> max diff = 0
        assert sol.minDifference([-1, -1, -1]) == 0

    def test_length_2_one_missing(self):
        """Test with length 2, one missing."""
        sol = Solution()
        # [1, -1] -> best is [1, 3] -> max diff = 2
        assert sol.minDifference([1, -1]) == 2

    def test_length_2_both_missing(self):
        """Test with length 2, both missing."""
        sol = Solution()
        # [-1, -1] -> best is [1, 1] -> max diff = 0
        assert sol.minDifference([-1, -1]) == 0

    def test_large_values(self):
        """Test with large values."""
        sol = Solution()
        # [1, -1, 1000000000] -> best is [1, 500000000, 1000000000] -> max diff = 499999999
        assert sol.minDifference([1, -1, 1000000000]) == 499999999

    def test_three_missing_consecutive(self):
        """Test with three consecutive missing elements."""
        sol = Solution()
        # [1, -1, -1, -1, 10] -> best arrangement gives max diff = 4
        assert sol.minDifference([1, -1, -1, -1, 10]) == 4

    def test_already_optimal_array(self):
        """Test with already optimal array."""
        sol = Solution()
        # [1, 2, 3, 4] -> all diffs are 1 -> max = 1
        assert sol.minDifference([1, 2, 3, 4]) == 1

    def test_alternating_values(self):
        """Test with alternating values."""
        sol = Solution()
        # [1, 3, 5, 7] -> all diffs are 2 -> max = 2
        assert sol.minDifference([1, 3, 5, 7]) == 2

    def test_all_same_values(self):
        """Test with all same values."""
        sol = Solution()
        # [5, 5, 5, 5] -> all diffs are 0 -> max = 0
        assert sol.minDifference([5, 5, 5, 5]) == 0

    def test_missing_with_same_neighbors(self):
        """Test with missing element between same values."""
        sol = Solution()
        # [5, -1, 5] -> best is [5, 5, 5] -> max diff = 0
        assert sol.minDifference([5, -1, 5]) == 0

    def test_missing_with_different_neighbors(self):
        """Test with missing element between different values."""
        sol = Solution()
        # [1, -1, 10] -> best is [1, 5, 10] -> max diff = 5
        assert sol.minDifference([1, -1, 10]) == 5
