from typing import List
from solution import Solution


class TestMinArraySum:
    def test_basic_case(self):
        """Test basic case with simple numbers"""
        sol = Solution()
        # nums = [10, 20], k = 5, op1 = 1, op2 = 1
        # Best: divide 20 -> 10, subtract 10 -> 5, sum = 15
        assert sol.minArraySum([10, 20], 5, 1, 1) == 15

    def test_k_zero(self):
        """Test when k = 0 (subtraction doesn't help)"""
        sol = Solution()
        # nums = [10, 20], k = 0, op1 = 1, op2 = 1
        # Only division helps: 10 -> 5, 20 -> 10, sum = 15
        assert sol.minArraySum([10, 20], 0, 1, 1) == 15

    def test_op1_zero(self):
        """Test when op1 = 0 (no division allowed)"""
        sol = Solution()
        # nums = [10, 20], k = 5, op1 = 0, op2 = 1
        # Only subtraction: 10 -> 5, 20 -> 20, sum = 25
        assert sol.minArraySum([10, 20], 5, 0, 1) == 25

    def test_op2_zero(self):
        """Test when op2 = 0 (no subtraction allowed)"""
        sol = Solution()
        # nums = [10, 20], k = 5, op1 = 1, op2 = 0
        # Only division: 10 -> 5, 20 -> 10, sum = 15
        assert sol.minArraySum([10, 20], 5, 1, 0) == 15

    def test_single_element(self):
        """Test with single element"""
        sol = Solution()
        # nums = [10], k = 5, op1 = 1, op2 = 1
        # Best: divide 10 -> 5, subtract 5 -> 0, sum = 0
        assert sol.minArraySum([10], 5, 1, 1) == 0

    def test_elements_too_small_for_subtraction(self):
        """Test when elements are smaller than k"""
        sol = Solution()
        # nums = [3, 4], k = 5, op1 = 1, op2 = 1
        # Neither element can be subtracted
        # Only division: 3 -> 2, 4 -> 2, sum = 4
        assert sol.minArraySum([3, 4], 5, 1, 1) == 4

    def test_all_elements_same(self):
        """Test with all elements the same"""
        sol = Solution()
        # nums = [10, 10, 10], k = 5, op1 = 2, op2 = 2
        # Best: divide two elements, subtract from two elements
        # Divide: 10 -> 5, Subtract: 5 -> 0
        # Two elements become 0, one stays 10, sum = 10
        assert sol.minArraySum([10, 10, 10], 5, 2, 2) == 10

    def test_large_numbers(self):
        """Test with large numbers"""
        sol = Solution()
        # nums = [100000, 100000], k = 100000, op1 = 1, op2 = 1
        # Divide: 100000 -> 50000, Subtract: 100000 -> 0
        # Best: divide one, subtract one, sum = 50000
        assert sol.minArraySum([100000, 100000], 100000, 1, 1) == 50000

    def test_op1_op2_larger_than_elements(self):
        """Test when operations exceed number of elements"""
        sol = Solution()
        # nums = [10, 20], k = 5, op1 = 10, op2 = 10
        # Each element can be divided once and subtracted once
        # 10: divide -> 5, subtract -> 0
        # 20: divide -> 10, subtract -> 5
        # Sum = 0 + 5 = 5
        assert sol.minArraySum([10, 20], 5, 10, 10) == 5

    def test_zero_elements(self):
        """Test with zero elements"""
        sol = Solution()
        # nums = [0, 0], k = 5, op1 = 1, op2 = 1
        # Zeros can't be subtracted, division doesn't change them
        # Sum = 0
        assert sol.minArraySum([0, 0], 5, 1, 1) == 0

    def test_one_element_op1_only(self):
        """Test single element with only op1"""
        sol = Solution()
        # nums = [10], k = 5, op1 = 1, op2 = 0
        # Divide: 10 -> 5, sum = 5
        assert sol.minArraySum([10], 5, 1, 0) == 5

    def test_one_element_op2_only(self):
        """Test single element with only op2"""
        sol = Solution()
        # nums = [10], k = 5, op1 = 0, op2 = 1
        # Subtract: 10 -> 5, sum = 5
        assert sol.minArraySum([10], 5, 0, 1) == 5

    def test_both_operations_on_same_element(self):
        """Test when both operations are applied to same element"""
        sol = Solution()
        # nums = [10], k = 5, op1 = 1, op2 = 1
        # Divide first: 10 -> 5, then subtract: 5 -> 0
        # Or subtract first: 10 -> 5, then divide: 5 -> 3
        # Best: divide then subtract, sum = 0
        assert sol.minArraySum([10], 5, 1, 1) == 0

    def test_very_small_k(self):
        """Test with very small k"""
        sol = Solution()
        # nums = [10, 20], k = 1, op1 = 1, op2 = 1
        # Subtract 1 from one element, divide one
        # Subtract from 20: 19, divide 10: 5, sum = 24
        # Or subtract from 10: 9, divide 20: 10, sum = 19
        # Best: subtract from 10, divide 20, sum = 19
        assert sol.minArraySum([10, 20], 1, 1, 1) == 19

    def test_no_operations_available(self):
        """Test when no operations can be beneficial"""
        sol = Solution()
        # nums = [5, 5], k = 10, op1 = 0, op2 = 0
        # No operations, sum = 10
        assert sol.minArraySum([5, 5], 10, 0, 0) == 10
