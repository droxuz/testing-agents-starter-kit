import pytest
from typing import List
from solution import Solution


class TestNumberOfSubsequences:
    def test_empty_array(self):
        """Empty array - no subsequences possible"""
        sol = Solution()
        result = sol.numberOfSubsequences([])
        assert result == 0

    def test_array_too_short(self):
        """Array with length less than 7 - no valid subsequence possible"""
        sol = Solution()
        result = sol.numberOfSubsequences([1, 2, 3, 4, 5])
        assert result == 0

    def test_minimum_length_no_valid(self):
        """Minimum length array with no valid special subsequence"""
        sol = Solution()
        # Only valid indices are (0,2,4,6): 1*5=5, 3*7=21, not equal
        result = sol.numberOfSubsequences([1, 2, 3, 4, 5, 6, 7])
        assert result == 0

    def test_minimum_length_all_same(self):
        """Minimum length array with all same values - 1 valid subsequence"""
        sol = Solution()
        # Only valid indices are (0,2,4,6): 1*1=1, 1*1=1, equal
        result = sol.numberOfSubsequences([1, 1, 1, 1, 1, 1, 1])
        assert result == 1

    def test_length_8_all_same(self):
        """Length 8 array with all same values - 5 valid subsequences"""
        sol = Solution()
        # Valid index combinations: (0,2,4,6), (0,2,4,7), (0,2,5,6), (0,2,5,7), (0,2,6,7)
        # All satisfy 1*1=1*1
        result = sol.numberOfSubsequences([1, 1, 1, 1, 1, 1, 1, 1])
        assert result == 5

    def test_length_9_all_same(self):
        """Length 9 array with all same values - 15 valid subsequences"""
        sol = Solution()
        # Valid index combinations: C(6,4) = 15
        result = sol.numberOfSubsequences([1, 1, 1, 1, 1, 1, 1, 1, 1])
        assert result == 15

    def test_single_valid_subsequence(self):
        """Array with exactly one valid special subsequence"""
        sol = Solution()
        # Only (0,2,4,6) works: 1*1=1, 1*1=1
        result = sol.numberOfSubsequences([1, 2, 1, 2, 1, 2, 1])
        assert result == 1

    def test_two_valid_subsequences(self):
        """Array with exactly two valid special subsequences"""
        sol = Solution()
        # (0,2,4,6): 2*2=4, 2*2=4 ✓
        # (1,3,5,7): 1*1=1, 1*1=1 ✓
        result = sol.numberOfSubsequences([2, 1, 2, 1, 2, 1, 2, 1])
        assert result == 2

    def test_no_valid_subsequences_large(self):
        """Larger array with no valid special subsequences"""
        sol = Solution()
        # Check various combinations, none should satisfy the condition
        result = sol.numberOfSubsequences([1, 2, 3, 4, 5, 6, 7, 8])
        assert result == 0

    def test_large_array_all_same(self):
        """Large array with all same values - many valid subsequences"""
        sol = Solution()
        # C(10-3, 4) = C(7, 4) = 35
        result = sol.numberOfSubsequences([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        assert result == 35

    def test_boundary_minimum_value(self):
        """Test with minimum value 1"""
        sol = Solution()
        result = sol.numberOfSubsequences([1, 1, 1, 1, 1, 1, 1])
        assert result == 1

    def test_boundary_maximum_value(self):
        """Test with maximum value 1000"""
        sol = Solution()
        result = sol.numberOfSubsequences([1000, 1000, 1000, 1000, 1000, 1000, 1000])
        assert result == 1

    def test_alternating_pattern(self):
        """Test with alternating pattern"""
        sol = Solution()
        # (0,2,4,6): 1*1=1, 1*1=1 ✓
        # (0,2,4,7): 1*1=1, 1*1=1 ✓
        # (0,2,5,6): 1*1=1, 1*1=1 ✓
        # (0,2,5,7): 1*1=1, 1*1=1 ✓
        # (0,2,6,7): 1*1=1, 1*1=1 ✓
        # (0,3,5,7): 1*1=1, 1*1=1 ✓
        # (1,3,5,7): 1*1=1, 1*1=1 ✓
        result = sol.numberOfSubsequences([1, 2, 1, 2, 1, 2, 1, 2])
        assert result == 7
