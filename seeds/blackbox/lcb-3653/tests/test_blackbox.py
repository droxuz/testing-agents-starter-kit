from typing import List
from solution import Solution


class TestMaxSubarraySum:
    """Tests for maximum subarray sum with length divisible by k."""

    def test_all_positive_k_equals_length(self):
        """When k equals array length, only entire array is valid."""
        sol = Solution()
        # [1, 2, 3, 4] with k=4: only entire array valid, sum=10
        assert sol.maxSubarraySum([1, 2, 3, 4], 4) == 10

    def test_all_positive_k_divides_length(self):
        """When k divides length, entire array may be optimal."""
        sol = Solution()
        # [1, 2, 3, 4] with k=2: length 2 or 4 valid
        # Length 2: [1,2]=3, [2,3]=5, [3,4]=7
        # Length 4: [1,2,3,4]=10
        assert sol.maxSubarraySum([1, 2, 3, 4], 2) == 10

    def test_k_equals_one_standard_max_subarray(self):
        """k=1 means any subarray is valid, standard max subarray problem."""
        sol = Solution()
        # [1, -2, 3, -4, 5, -6]: max single element is 5
        assert sol.maxSubarraySum([1, -2, 3, -4, 5, -6], 1) == 5

    def test_all_negative_k_equals_length(self):
        """All negative numbers, only entire array valid."""
        sol = Solution()
        # [-1, -2, -3] with k=3: only entire array valid, sum=-6
        assert sol.maxSubarraySum([-1, -2, -3], 3) == -6

    def test_all_negative_k_one(self):
        """All negative, k=1: pick the least negative element."""
        sol = Solution()
        # [-1, -2, -3] with k=1: max is -1
        assert sol.maxSubarraySum([-1, -2, -3], 1) == -1

    def test_all_negative_k_two(self):
        """All negative, k=2: pick best length-2 subarray."""
        sol = Solution()
        # [-1, -2, -3] with k=2: [-1,-2]=-3, [-2,-3]=-5, max=-3
        assert sol.maxSubarraySum([-1, -2, -3], 2) == -3

    def test_mixed_positive_negative(self):
        """Mixed values with various k."""
        sol = Solution()
        # [1, -2, 3, -4, 5, -6] with k=2
        # Length 2: [1,-2]=-1, [-2,3]=1, [3,-4]=-1, [-4,5]=1, [5,-6]=-1
        assert sol.maxSubarraySum([1, -2, 3, -4, 5, -6], 2) == 1

    def test_mixed_with_optimal_chunk(self):
        """Find optimal subarray of length divisible by k."""
        sol = Solution()
        # [5, -1, 5, -1, 5] with k=3
        # Length 3: [5,-1,5]=9, [-1,5,-1]=3, [5,-1,5]=9
        assert sol.maxSubarraySum([5, -1, 5, -1, 5], 3) == 9

    def test_mixed_with_zero_sum(self):
        """Subarray can have zero sum."""
        sol = Solution()
        # [-10, 5, -10, 5, -10] with k=3
        # Length 3: [-10,5,-10]=-15, [5,-10,5]=0, [-10,5,-10]=-15
        assert sol.maxSubarraySum([-10, 5, -10, 5, -10], 3) == 0

    def test_all_zeros(self):
        """Array of all zeros."""
        sol = Solution()
        assert sol.maxSubarraySum([0, 0, 0, 0], 2) == 0

    def test_single_element_positive(self):
        """Single positive element."""
        sol = Solution()
        assert sol.maxSubarraySum([42], 1) == 42

    def test_single_element_negative(self):
        """Single negative element."""
        sol = Solution()
        assert sol.maxSubarraySum([-42], 1) == -42

    def test_large_positive_values(self):
        """Large positive values."""
        sol = Solution()
        # [10**9, 10**9, 10**9] with k=2
        # Length 2: [10**9, 10**9]=2*10**9, [10**9, 10**9]=2*10**9
        assert sol.maxSubarraySum([10**9, 10**9, 10**9], 2) == 2 * 10**9

    def test_large_negative_values(self):
        """Large negative values."""
        sol = Solution()
        # [-10**9, -10**9, -10**9] with k=2
        # Length 2: [-10**9, -10**9]=-2*10**9, [-10**9, -10**9]=-2*10**9
        assert sol.maxSubarraySum([-10**9, -10**9, -10**9], 2) == -2 * 10**9

    def test_alternating_positive_negative(self):
        """Alternating pattern."""
        sol = Solution()
        # [10, -5, 10, -5, 10] with k=3
        # Length 3: [10,-5,10]=15, [-5,10,-5]=0, [10,-5,10]=15
        assert sol.maxSubarraySum([10, -5, 10, -5, 10], 3) == 15

    def test_shorter_than_k_not_possible(self):
        """k equals length, only one subarray."""
        sol = Solution()
        # [1, 2, 3] with k=3: only [1,2,3]=6
        assert sol.maxSubarraySum([1, 2, 3], 3) == 6

    def test_k_equals_length_with_mixed(self):
        """Mixed values, k equals length."""
        sol = Solution()
        # [-10, 5, -10, 5, -10] with k=5: only entire array
        assert sol.maxSubarraySum([-10, 5, -10, 5, -10], 5) == -10

    def test_two_elements_k_two(self):
        """Two elements with k=2."""
        sol = Solution()
        # [3, 4] with k=2: only [3,4]=7
        assert sol.maxSubarraySum([3, 4], 2) == 7

    def test_two_elements_k_one(self):
        """Two elements with k=1: pick max element."""
        sol = Solution()
        # [3, 4] with k=1: max is 4
        assert sol.maxSubarraySum([3, 4], 1) == 4

    def test_three_elements_k_three(self):
        """Three elements with k=3."""
        sol = Solution()
        # [1, -1, 1] with k=3: only [1,-1,1]=1
        assert sol.maxSubarraySum([1, -1, 1], 3) == 1

    def test_three_elements_k_one(self):
        """Three elements with k=1."""
        sol = Solution()
        # [1, -1, 1] with k=1: max is 1
        assert sol.maxSubarraySum([1, -1, 1], 1) == 1

    def test_three_elements_k_two(self):
        """Three elements with k=2: only length 2 subarrays."""
        sol = Solution()
        # [1, -1, 1] with k=2: [1,-1]=0, [-1,1]=0
        assert sol.maxSubarraySum([1, -1, 1], 2) == 0

    def test_prefix_negative_suffix_positive(self):
        """Prefix is negative, suffix is positive."""
        sol = Solution()
        # [-100, 1, 1, 1, 1] with k=4
        # Length 4: [-100,1,1,1]=-97, [1,1,1,1]=4
        assert sol.maxSubarraySum([-100, 1, 1, 1, 1], 4) == 4

    def test_prefix_positive_suffix_negative(self):
        """Prefix is positive, suffix is negative."""
        sol = Solution()
        # [100, -1, -1, -1, -1] with k=4
        # Length 4: [100,-1,-1,-1]=97, [-1,-1,-1,-1]=-4
        assert sol.maxSubarraySum([100, -1, -1, -1, -1], 4) == 97

    def test_all_same_positive(self):
        """All same positive values."""
        sol = Solution()
        # [5, 5, 5, 5, 5] with k=3
        # Length 3: [5,5,5]=15, [5,5,5]=15, [5,5,5]=15
        assert sol.maxSubarraySum([5, 5, 5, 5, 5], 3) == 15

    def test_all_same_negative(self):
        """All same negative values."""
        sol = Solution()
        # [-5, -5, -5, -5, -5] with k=3
        # Length 3: [-5,-5,-5]=-15
        assert sol.maxSubarraySum([-5, -5, -5, -5, -5], 3) == -15

    def test_exact_division(self):
        """Array length exactly divisible by k."""
        sol = Solution()
        # [1, 2, 3, 4, 5, 6] with k=3
        # Length 3: [1,2,3]=6, [2,3,4]=9, [3,4,5]=12, [4,5,6]=15
        assert sol.maxSubarraySum([1, 2, 3, 4, 5, 6], 3) == 15

    def test_not_exact_division(self):
        """Array length not divisible by k."""
        sol = Solution()
        # [1, 2, 3, 4, 5] with k=3
        # Length 3: [1,2,3]=6, [2,3,4]=9, [3,4,5]=12
        assert sol.maxSubarraySum([1, 2, 3, 4, 5], 3) == 12
