import pytest
from solution import Solution


class TestHasIncreasingSubarrays:
    def test_both_subarrays_increasing(self):
        """Both adjacent subarrays of length k are strictly increasing"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 4, 5, 6], 2) == True

    def test_first_subarray_not_increasing(self):
        """First subarray is not strictly increasing"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 2, 3, 4], 2) == False

    def test_second_subarray_not_increasing(self):
        """Second subarray is not strictly increasing"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 4, 2, 3], 2) == False

    def test_neither_subarray_increasing(self):
        """Neither subarray is strictly increasing"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([2, 1, 3, 2, 4, 3], 2) == False

    def test_k_equals_1(self):
        """k=1: single elements are always strictly increasing (vacuously true)"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 4, 5], 1) == True

    def test_minimum_array_length(self):
        """Array with exactly 2*k elements - only one pair to check"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 4], 2) == True

    def test_no_increasing_subarrays_decreasing_array(self):
        """All elements decreasing - no increasing subarrays"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([6, 5, 4, 3, 2, 1], 2) == False

    def test_multiple_positions_one_works(self):
        """Multiple adjacent pairs, at least one works"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 1, 2, 3], 2) == True

    def test_negative_numbers_increasing(self):
        """Negative numbers that form increasing subarrays"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([-1, 0, 1, -2, -1, 0], 2) == False

    def test_negative_numbers_all_decreasing(self):
        """All negative numbers, decreasing"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([-6, -5, -4, -3, -2, -1], 2) == True

    def test_mixed_positive_negative(self):
        """Mixed positive and negative numbers"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([-1, 0, 1, 2, 3, 4], 2) == True

    def test_larger_k(self):
        """Larger k value"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 4, 5, 6, 7, 8], 3) == True

    def test_larger_k_no_increasing(self):
        """Larger k value with no increasing subarrays"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([3, 2, 1, 4, 3, 2], 2) == False

    def test_equal_elements(self):
        """Equal elements - not strictly increasing"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 1, 2, 2, 3, 3], 2) == False

    def test_longer_array_multiple_pairs(self):
        """Longer array with multiple possible adjacent pairs"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3) == True

    def test_exact_boundary_2k(self):
        """Array length exactly equals 2*k"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([1, 2, 3, 4, 5, 6], 3) == True

    def test_exact_boundary_no_increasing(self):
        """Array length exactly equals 2*k but no increasing subarrays"""
        solution = Solution()
        assert solution.hasIncreasingSubarrays([3, 2, 1, 4, 3, 2], 3) == False
