from typing import List
from solution import Solution


def test_all_positive():
    """All positive numbers - removing any element reduces the max sum"""
    sol = Solution()
    assert sol.maxSubarraySum([1, 2, 3]) == 6


def test_all_negative():
    """All negative numbers - must keep at least one element"""
    sol = Solution()
    assert sol.maxSubarraySum([-1, -2, -3]) == -1


def test_mixed_positive_negative():
    """Mixed array where removing a negative helps"""
    sol = Solution()
    assert sol.maxSubarraySum([1, -2, 3]) == 4


def test_single_element_positive():
    """Single positive element - cannot remove (array must remain non-empty)"""
    sol = Solution()
    assert sol.maxSubarraySum([5]) == 5


def test_single_element_negative():
    """Single negative element - cannot remove (array must remain non-empty)"""
    sol = Solution()
    assert sol.maxSubarraySum([-5]) == -5


def test_duplicate_elements():
    """All same elements - removing makes array empty, so keep original"""
    sol = Solution()
    assert sol.maxSubarraySum([1, 1, 1]) == 3


def test_remove_negative_improves():
    """Removing negative element improves max subarray"""
    sol = Solution()
    assert sol.maxSubarraySum([2, -1, 2]) == 4


def test_remove_negative_improves2():
    """Another case where removing negative helps"""
    sol = Solution()
    assert sol.maxSubarraySum([3, -5, 3]) == 6


def test_remove_negative_improves3():
    """Removing negative creates better subarray"""
    sol = Solution()
    assert sol.maxSubarraySum([1, -100, 1]) == 2


def test_zeros():
    """Array with zeros - removing zeros makes array empty"""
    sol = Solution()
    assert sol.maxSubarraySum([0, 0, 0]) == 0


def test_zeros_with_positive():
    """Zeros with positive - removing zeros keeps positives"""
    sol = Solution()
    assert sol.maxSubarraySum([0, 1, 0]) == 1


def test_alternating():
    """Alternating positive and negative"""
    sol = Solution()
    assert sol.maxSubarraySum([-1, 1, -1, 1]) == 2


def test_larger_negative_in_middle():
    """Large negative in middle"""
    sol = Solution()
    assert sol.maxSubarraySum([10, -20, 30]) == 40


def test_multiple_negatives():
    """Multiple negative elements"""
    sol = Solution()
    assert sol.maxSubarraySum([-2, -3, -1]) == -1


def test_positive_with_negative_suffix():
    """Positive array with negative suffix"""
    sol = Solution()
    assert sol.maxSubarraySum([1, 2, -5, 3, 4]) == 10


def test_negative_with_positive_suffix():
    """Negative array with positive suffix"""
    sol = Solution()
    assert sol.maxSubarraySum([-100, 100]) == 100


def test_small_values():
    """Small boundary values"""
    sol = Solution()
    assert sol.maxSubarraySum([1]) == 1
    assert sol.maxSubarraySum([-1]) == -1


def test_large_values():
    """Large boundary values"""
    sol = Solution()
    assert sol.maxSubarraySum([1000000]) == 1000000
    assert sol.maxSubarraySum([-1000000]) == -1000000


def test_two_elements_positive():
    """Two positive elements"""
    sol = Solution()
    assert sol.maxSubarraySum([1, 2]) == 3


def test_two_elements_negative():
    """Two negative elements"""
    sol = Solution()
    assert sol.maxSubarraySum([-1, -2]) == -1


def test_two_elements_mixed():
    """Two elements with mixed signs"""
    sol = Solution()
    assert sol.maxSubarraySum([-5, 10]) == 10


def test_three_elements_all_same():
    """Three same elements"""
    sol = Solution()
    assert sol.maxSubarraySum([5, 5, 5]) == 15
    assert sol.maxSubarraySum([-5, -5, -5]) == -5


def test_complex_case():
    """Complex case with multiple removal options"""
    sol = Solution()
    assert sol.maxSubarraySum([1, -2, 3, -4, 5]) == 6


def test_all_zeros():
    """All zeros"""
    sol = Solution()
    assert sol.maxSubarraySum([0, 0, 0]) == 0


def test_single_zero():
    """Single zero"""
    sol = Solution()
    assert sol.maxSubarraySum([0]) == 0


def test_two_zeros():
    """Two zeros"""
    sol = Solution()
    assert sol.maxSubarraySum([0, 0]) == 0


def test_negative_then_positive():
    """Negative then positive"""
    sol = Solution()
    assert sol.maxSubarraySum([-5, 10, -2]) == 10


def test_positive_then_negative():
    """Positive then negative"""
    sol = Solution()
    # Original: [10, -5, 2] max = 10
    # Remove 10: [-5, 2] max = 2
    # Remove -5: [10, 2] max = 12
    # Remove 2: [10, -5] max = 10
    assert sol.maxSubarraySum([10, -5, 2]) == 12


def test_mixed_with_large_gap():
    """Mixed with large gap"""
    sol = Solution()
    # Original: [100, -200, 100] max = 100
    # Remove 100: [-200, 100] max = 100
    # Remove -200: [100, 100] max = 200
    assert sol.maxSubarraySum([100, -200, 100]) == 200


def test_consecutive_positives():
    """Consecutive positives"""
    sol = Solution()
    assert sol.maxSubarraySum([1, 2, 3, 4]) == 10


def test_consecutive_negatives():
    """Consecutive negatives"""
    sol = Solution()
    assert sol.maxSubarraySum([-1, -2, -3, -4]) == -1


def test_alternating_signs():
    """Alternating signs"""
    sol = Solution()
    # Original: [1,-1,1,-1,1] max = 1
    # Remove 1: [-1,-1,-1] max = -1
    # Remove -1: [1,1,1] max = 3
    assert sol.maxSubarraySum([1, -1, 1, -1, 1]) == 3
