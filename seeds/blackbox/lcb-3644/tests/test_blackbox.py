from typing import List
from solution import Solution


class TestMinimumSumSubarray:
    """Tests for minimumSumSubarray function."""

    def test_simple_positive_array(self):
        """Array with all positive numbers, find minimum positive sum."""
        sol = Solution()
        # Subarrays of size 1: [1]=1, [2]=2, [3]=3
        # Subarrays of size 2: [1,2]=3, [2,3]=5
        # Minimum positive sum is 1
        assert sol.minimumSumSubarray([1, 2, 3], 1, 2) == 1

    def test_all_negative(self):
        """All negative numbers, no positive sum possible."""
        sol = Solution()
        # All subarrays have negative sums
        assert sol.minimumSumSubarray([-1, -2, -3], 1, 2) == -1

    def test_mixed_with_minimum_positive(self):
        """Mixed positive and negative, find minimum positive sum."""
        sol = Solution()
        # Size 1: [1]=1, [-2]=-2, [3]=3
        # Size 2: [1,-2]=-1, [-2,3]=1
        # Minimum positive sum is 1
        assert sol.minimumSumSubarray([1, -2, 3], 1, 2) == 1

    def test_boundary_sizes(self):
        """Test with l and r at boundaries."""
        sol = Solution()
        # Size 2: [5,1]=6, [1,1]=2
        # Size 3: [5,1,1]=7
        # Minimum positive sum is 2
        assert sol.minimumSumSubarray([5, 1, 1], 2, 3) == 2

    def test_single_element(self):
        """Test with single element array."""
        sol = Solution()
        # Only one subarray of size 1: [5]=5
        assert sol.minimumSumSubarray([5], 1, 1) == 5

    def test_no_positive_sum_possible(self):
        """All subarrays have sum <= 0."""
        sol = Solution()
        # [-1,0,-1] size 1: -1, 0, -1 (none > 0)
        # [-1,0,-1] size 2: -1, -1 (none > 0)
        assert sol.minimumSumSubarray([-1, 0, -1], 1, 2) == -1

    def test_zeros_only(self):
        """Array with only zeros."""
        sol = Solution()
        # All subarrays sum to 0, which is not > 0
        assert sol.minimumSumSubarray([0, 0, 0], 1, 3) == -1

    def test_multiple_options(self):
        """Multiple subarrays with different positive sums."""
        sol = Solution()
        # Size 1: [3]=3, [-1]=-1, [-1]=-1, [3]=3
        # Size 2: [3,-1]=2, [-1,-1]=-2, [-1,3]=2
        # Size 3: [3,-1,-1]=1, [-1,-1,3]=1
        # Minimum positive sum is 1
        assert sol.minimumSumSubarray([3, -1, -1, 3], 1, 3) == 1

    def test_exact_size_l_equals_r(self):
        """Test when l equals r (exact size required)."""
        sol = Solution()
        # Only size 2 subarrays allowed
        # [1,2]=3, [2,3]=5
        # Minimum positive sum is 3
        assert sol.minimumSumSubarray([1, 2, 3], 2, 2) == 3

    def test_negative_and_positive_mixed(self):
        """Negative and positive mixed, find minimum positive sum."""
        sol = Solution()
        # Size 2: [-5,10]=5, [10,-5]=5
        # Minimum positive sum is 5
        assert sol.minimumSumSubarray([-5, 10, -5], 2, 2) == 5

    def test_minimum_sum_is_larger_than_single_elements(self):
        """Minimum positive sum comes from larger subarray."""
        sol = Solution()
        # Size 1: [1]=1, [2]=2, [3]=3
        # Size 2: [1,2]=3, [2,3]=5
        # Size 3: [1,2,3]=6
        # Minimum positive sum is 1 (from size 1)
        assert sol.minimumSumSubarray([1, 2, 3], 1, 3) == 1

    def test_minimum_sum_from_larger_subarray(self):
        """Minimum positive sum comes from larger subarray only."""
        sol = Solution()
        # Size 2: [-1,5]=4, [5,-1]=4
        # Minimum positive sum is 4
        assert sol.minimumSumSubarray([-1, 5, -1], 2, 2) == 4

    def test_boundary_length_one(self):
        """Test with minimum array length."""
        sol = Solution()
        # Single element [1], l=1, r=1
        assert sol.minimumSumSubarray([1], 1, 1) == 1

    def test_all_same_positive(self):
        """All elements are the same positive value."""
        sol = Solution()
        # Size 1: [2]=2, [2]=2, [2]=2
        # Size 2: [2,2]=4, [2,2]=4
        # Size 3: [2,2,2]=6
        # Minimum positive sum is 2
        assert sol.minimumSumSubarray([2, 2, 2], 1, 3) == 2

    def test_large_positive_with_small_negatives(self):
        """Large positive numbers with small negative numbers."""
        sol = Solution()
        # Size 1: [100]=100, [-1]=-1, [100]=100
        # Size 2: [100,-1]=99, [-1,100]=99
        # Minimum positive sum is 99
        assert sol.minimumSumSubarray([100, -1, 100], 1, 2) == 99
