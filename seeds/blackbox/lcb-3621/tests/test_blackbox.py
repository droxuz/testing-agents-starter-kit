from typing import List
from solution import Solution


class TestMinOperations:
    def test_all_equal_to_k(self):
        """All elements already equal to k - 0 operations needed."""
        sol = Solution()
        assert sol.minOperations([5, 5, 5], 5) == 0

    def test_single_element_equal_to_k(self):
        """Single element already equal to k - 0 operations needed."""
        sol = Solution()
        assert sol.minOperations([5], 5) == 0

    def test_single_element_greater_than_k(self):
        """Single element greater than k - 1 operation needed."""
        sol = Solution()
        assert sol.minOperations([10], 5) == 1

    def test_single_element_less_than_k(self):
        """Single element less than k - impossible, return -1."""
        sol = Solution()
        assert sol.minOperations([3], 5) == -1

    def test_all_equal_greater_than_k(self):
        """All elements equal and greater than k - 1 operation needed."""
        sol = Solution()
        assert sol.minOperations([10, 10, 10], 5) == 1

    def test_two_unique_values_both_greater_than_k(self):
        """Two unique values both > k - 2 operations needed."""
        sol = Solution()
        assert sol.minOperations([6, 7, 6, 7], 5) == 2

    def test_three_unique_values_all_greater_than_k(self):
        """Three unique values all > k - 3 operations needed."""
        sol = Solution()
        assert sol.minOperations([6, 7, 8, 6, 7, 8], 5) == 3

    def test_mixed_values_some_equal_to_k(self):
        """Some elements equal to k, some greater - count unique > k."""
        sol = Solution()
        assert sol.minOperations([5, 6, 5, 7], 5) == 2

    def test_values_greater_than_k_with_duplicates(self):
        """Multiple duplicates of each value > k."""
        sol = Solution()
        assert sol.minOperations([10, 10, 10, 8, 8, 8], 5) == 2

    def test_impossible_min_less_than_k(self):
        """Minimum value less than k - impossible."""
        sol = Solution()
        assert sol.minOperations([3, 5, 7], 5) == -1

    def test_impossible_min_less_than_k_all_values(self):
        """All values less than k - impossible."""
        sol = Solution()
        assert sol.minOperations([1, 2, 3], 5) == -1

    def test_k_not_in_array_all_greater(self):
        """k not in array but all values > k - still possible."""
        sol = Solution()
        assert sol.minOperations([6, 7, 8], 5) == 3

    def test_k_not_in_array_mixed(self):
        """k not in array, some equal, some greater."""
        sol = Solution()
        assert sol.minOperations([5, 6, 7], 5) == 2

    def test_boundary_k_equals_min(self):
        """k equals minimum value in array."""
        sol = Solution()
        assert sol.minOperations([5, 5, 6, 7], 5) == 2

    def test_boundary_k_equals_max(self):
        """k equals maximum value in array."""
        sol = Solution()
        assert sol.minOperations([5, 6, 7], 7) == 0

    def test_all_same_value_greater_than_k(self):
        """All values same and greater than k."""
        sol = Solution()
        assert sol.minOperations([100, 100, 100], 1) == 1

    def test_two_different_values_one_equal_to_k(self):
        """Two different values, one equals k."""
        sol = Solution()
        assert sol.minOperations([5, 10], 5) == 1

    def test_three_different_values_first_equals_k(self):
        """Three different values, first equals k."""
        sol = Solution()
        assert sol.minOperations([5, 6, 10], 5) == 2

    def test_values_with_large_gap(self):
        """Values with large gaps between them."""
        sol = Solution()
        assert sol.minOperations([5, 50, 50], 5) == 1

    def test_min_constraint_boundary(self):
        """Test at minimum constraint boundary."""
        sol = Solution()
        assert sol.minOperations([1, 1, 1], 1) == 0
        assert sol.minOperations([1, 2, 1], 1) == 1

    def test_max_constraint_boundary(self):
        """Test at maximum constraint boundary."""
        sol = Solution()
        assert sol.minOperations([100, 100, 100], 100) == 0
        assert sol.minOperations([100, 50, 100], 100) == 0
        assert sol.minOperations([100, 100, 50], 100) == 0
        assert sol.minOperations([100, 100, 100], 50) == 1

    def test_impossible_at_min_boundary(self):
        """Impossible case at minimum boundary."""
        sol = Solution()
        assert sol.minOperations([1, 2, 3], 2) == -1

    def test_impossible_at_min_boundary_all_greater(self):
        """Impossible case where min equals k."""
        sol = Solution()
        assert sol.minOperations([2, 3, 4], 2) == 2

    def test_complex_mixed_values(self):
        """Complex case with mixed values."""
        sol = Solution()
        assert sol.minOperations([3, 5, 5, 7, 7, 7], 3) == 2

    def test_two_values_both_greater_than_k(self):
        """Two distinct values both greater than k."""
        sol = Solution()
        assert sol.minOperations([10, 20], 5) == 2

    def test_all_values_equal_to_k(self):
        """All values already equal to k."""
        sol = Solution()
        assert sol.minOperations([7, 7, 7, 7], 7) == 0

    def test_impossible_with_min_less_than_k(self):
        """Impossible when min is less than k."""
        sol = Solution()
        assert sol.minOperations([4, 8, 8], 6) == -1

    def test_impossible_with_all_less_than_k(self):
        """Impossible when all values are less than k."""
        sol = Solution()
        assert sol.minOperations([4, 5, 6], 7) == -1

    def test_impossible_with_min_less_than_k_all_same(self):
        """Impossible when all values are less than k."""
        sol = Solution()
        assert sol.minOperations([5, 5, 5], 6) == -1

    def test_three_unique_values_increasing(self):
        """Three unique values in increasing order."""
        sol = Solution()
        assert sol.minOperations([3, 6, 9], 3) == 2

    def test_three_unique_values_decreasing(self):
        """Three unique values in decreasing order."""
        sol = Solution()
        assert sol.minOperations([9, 6, 3], 3) == 2

    def test_impossible_with_min_less_than_k_random(self):
        """Random impossible case."""
        sol = Solution()
        assert sol.minOperations([2, 5, 8], 4) == -1
