from typing import List
from solution import Solution


class TestLongestSubsequence:
    """Tests for longestSubsequence function."""
    
    def test_min_length_array(self):
        """Test with minimum length array (2 elements)."""
        sol = Solution()
        # [1, 2] -> difference is 1, non-increasing
        assert sol.longestSubsequence([1, 2]) == 2
    
    def test_min_length_array_reverse(self):
        """Test with minimum length array in reverse order."""
        sol = Solution()
        # [2, 1] -> difference is 1, non-increasing
        assert sol.longestSubsequence([2, 1]) == 2
    
    def test_all_same_elements(self):
        """Test with all elements being the same."""
        sol = Solution()
        # [5, 5, 5, 5] -> all differences are 0, non-increasing
        assert sol.longestSubsequence([5, 5, 5, 5]) == 4
    
    def test_strictly_increasing(self):
        """Test with strictly increasing array."""
        sol = Solution()
        # [1, 2, 3, 4, 5] -> differences are 1, 1, 1, 1 (all equal, non-increasing)
        assert sol.longestSubsequence([1, 2, 3, 4, 5]) == 5
    
    def test_strictly_decreasing(self):
        """Test with strictly decreasing array."""
        sol = Solution()
        # [5, 4, 3, 2, 1] -> differences are 1, 1, 1, 1 (all equal, non-increasing)
        assert sol.longestSubsequence([5, 4, 3, 2, 1]) == 5
    
    def test_decreasing_differences(self):
        """Test with decreasing differences between consecutive elements."""
        sol = Solution()
        # [1, 10, 2, 9, 3, 8] -> differences: 9, 8, 7, 6, 5 (strictly decreasing)
        assert sol.longestSubsequence([1, 10, 2, 9, 3, 8]) == 6
    
    def test_alternating_pattern(self):
        """Test with alternating pattern."""
        sol = Solution()
        # [1, 5, 2, 6, 3, 7] -> best is [1, 5, 2] with diffs 4, 3 or [1, 5, 6] with diffs 4, 1
        assert sol.longestSubsequence([1, 5, 2, 6, 3, 7]) == 3
    
    def test_alternating_pattern2(self):
        """Test with another alternating pattern."""
        sol = Solution()
        # [1, 10, 20, 30] -> [1, 20, 30] has diffs 19, 10
        assert sol.longestSubsequence([1, 10, 20, 30]) == 3
    
    def test_alternating_pattern3(self):
        """Test with another alternating pattern."""
        sol = Solution()
        # [1, 5, 10, 15, 20] -> [1, 10, 15, 20] has diffs 9, 5, 5
        assert sol.longestSubsequence([1, 5, 10, 15, 20]) == 4
    
    def test_two_elements_same(self):
        """Test with two identical elements."""
        sol = Solution()
        # [3, 3] -> difference is 0
        assert sol.longestSubsequence([3, 3]) == 2
    
    def test_two_elements_different(self):
        """Test with two different elements."""
        sol = Solution()
        # [1, 100] -> difference is 99
        assert sol.longestSubsequence([1, 100]) == 2
    
    def test_single_element_subsequence_possible(self):
        """Test where single element subsequence is the answer."""
        sol = Solution()
        # [1, 100, 2] -> [1, 100] has diff 99, [100, 2] has diff 98, can't combine
        # Actually [1, 100, 2] has diffs 99, 98 which is non-increasing
        assert sol.longestSubsequence([1, 100, 2]) == 3
    
    def test_boundary_values_min(self):
        """Test with minimum boundary values."""
        sol = Solution()
        # [1, 1] -> both at minimum value
        assert sol.longestSubsequence([1, 1]) == 2
    
    def test_boundary_values_max(self):
        """Test with maximum boundary values."""
        sol = Solution()
        # [300, 300] -> both at maximum value
        assert sol.longestSubsequence([300, 300]) == 2
    
    def test_boundary_values_min_diff(self):
        """Test with minimum possible difference."""
        sol = Solution()
        # [1, 2] -> difference is 1 (minimum non-zero)
        assert sol.longestSubsequence([1, 2]) == 2
    
    def test_boundary_values_max_diff(self):
        """Test with maximum possible difference."""
        sol = Solution()
        # [1, 300] -> difference is 299 (maximum)
        assert sol.longestSubsequence([1, 300]) == 2
    
    def test_large_array_constant(self):
        """Test with large array of constant values."""
        sol = Solution()
        # Array of 10000 ones
        assert sol.longestSubsequence([1] * 10000) == 10000
    
    def test_large_array_increasing(self):
        """Test with large array with increasing values."""
        sol = Solution()
        # [1, 2, 3, ..., 100] -> all differences are 1
        assert sol.longestSubsequence(list(range(1, 101))) == 100
    
    def test_alternating_large(self):
        """Test with large alternating pattern."""
        sol = Solution()
        # [1, 100, 2, 99, 3, 98] -> differences: 99, 98, 97, 96, 95
        assert sol.longestSubsequence([1, 100, 2, 99, 3, 98]) == 6
    
    def test_random_like_pattern(self):
        """Test with a pattern similar to random."""
        sol = Solution()
        # [1, 50, 25, 75, 12, 88] -> need to find best subsequence
        # [1, 50, 25] has diffs 49, 25 (valid)
        # [1, 50, 75] has diffs 49, 25 (valid)
        # [1, 50, 75, 12] has diffs 49, 25, 63 (invalid, 25 < 63)
        # Best might be [1, 50, 25, 12] with diffs 49, 25, 13 (valid)
        # Or [1, 50, 75, 88] with diffs 49, 25, 13 (valid)
        assert sol.longestSubsequence([1, 50, 25, 75, 12, 88]) >= 4
    
    def test_plateau_then_decrease(self):
        """Test with plateau followed by decrease."""
        sol = Solution()
        # [5, 5, 5, 2, 1] -> [5, 5, 5, 2, 1] has diffs 0, 0, 3, 1 (invalid: 0 < 3)
        # [5, 5, 5] has diffs 0, 0 (valid)
        # [5, 2, 1] has diffs 3, 1 (valid)
        # Best is [5, 5, 5] or [5, 2, 1], both length 3
        assert sol.longestSubsequence([5, 5, 5, 2, 1]) == 3
    
    def test_increase_then_decrease(self):
        """Test with increase followed by decrease."""
        sol = Solution()
        # [1, 5, 3, 2] -> [1, 5, 3] has diffs 4, 2 (valid), length 3
        assert sol.longestSubsequence([1, 5, 3, 2]) == 3
    
    def test_decrease_then_increase(self):
        """Test with decrease followed by increase."""
        sol = Solution()
        # [5, 3, 1, 2] -> [5, 3, 1] has diffs 2, 2 (valid), length 3
        assert sol.longestSubsequence([5, 3, 1, 2]) == 3

    def test_five_elements_increasing(self):
        """Test with 5 elements in increasing order."""
        sol = Solution()
        # [1, 2, 3, 4, 5] -> all differences are 1
        assert sol.longestSubsequence([1, 2, 3, 4, 5]) == 5
    
    def test_five_elements_decreasing(self):
        """Test with 5 elements in decreasing order."""
        sol = Solution()
        # [5, 4, 3, 2, 1] -> all differences are 1
        assert sol.longestSubsequence([5, 4, 3, 2, 1]) == 5
    
    def test_five_elements_alternating(self):
        """Test with 5 elements in alternating pattern."""
        sol = Solution()
        # [1, 5, 2, 6, 3] -> best is [1, 5, 2] or [1, 5, 6] or [1, 2, 6] or [1, 2, 3]
        # [1, 5, 2] has diffs 4, 3 (valid)
        assert sol.longestSubsequence([1, 5, 2, 6, 3]) == 3
    
    def test_four_elements_plateau(self):
        """Test with plateau pattern."""
        sol = Solution()
        # [5, 5, 5, 5] -> all differences are 0
        assert sol.longestSubsequence([5, 5, 5, 5]) == 4
    
    def test_four_elements_stairs(self):
        """Test with stairs pattern."""
        sol = Solution()
        # [1, 3, 5, 7] -> all differences are 2
        assert sol.longestSubsequence([1, 3, 5, 7]) == 4
    
    def test_three_elements_increasing(self):
        """Test with 3 elements increasing."""
        sol = Solution()
        # [1, 2, 3] -> diffs 1, 1
        assert sol.longestSubsequence([1, 2, 3]) == 3
    
    def test_three_elements_decreasing(self):
        """Test with 3 elements decreasing."""
        sol = Solution()
        # [3, 2, 1] -> diffs 1, 1
        assert sol.longestSubsequence([3, 2, 1]) == 3
    
    def test_three_elements_varying(self):
        """Test with 3 elements with varying differences."""
        sol = Solution()
        # [1, 10, 5] -> diffs 9, 5 (non-increasing)
        assert sol.longestSubsequence([1, 10, 5]) == 3

    def test_varying_diffs_increasing(self):
        """Test where we can't combine all elements due to increasing diffs."""
        sol = Solution()
        # [1, 50, 100] -> [1, 50] has diff 49, [50, 100] has diff 50
        # [1, 50, 100] has diffs 49, 50 which is NOT non-increasing
        # So answer is 2
        assert sol.longestSubsequence([1, 50, 100]) == 2
    
    def test_varying_diffs_decreasing(self):
        """Test where we can combine all elements due to decreasing diffs."""
        sol = Solution()
        # [1, 100, 50] -> [1, 100] has diff 99, [100, 50] has diff 50
        # [1, 100, 50] has diffs 99, 50 which IS non-increasing
        # So answer is 3
        assert sol.longestSubsequence([1, 100, 50]) == 3
    
    def test_identical_elements_multiple(self):
        """Test with multiple identical elements."""
        sol = Solution()
        # [5, 5, 5, 5, 5] -> all diffs are 0
        assert sol.longestSubsequence([5, 5, 5, 5, 5]) == 5
