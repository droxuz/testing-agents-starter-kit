from typing import List
from solution import Solution


class TestMinOperations:
    def test_already_non_decreasing(self):
        """Test array that is already non-decreasing"""
        solution = Solution()
        assert solution.minOperations([1, 2, 3]) == 0

    def test_single_element(self):
        """Test single element array"""
        solution = Solution()
        assert solution.minOperations([5]) == 0

    def test_all_same(self):
        """Test array with all same elements"""
        solution = Solution()
        assert solution.minOperations([5, 5, 5]) == 0

    def test_all_ones(self):
        """Test array with all ones"""
        solution = Solution()
        assert solution.minOperations([1, 1, 1]) == 0

    def test_decreasing_array(self):
        """Test strictly decreasing array"""
        solution = Solution()
        # [3, 2, 1]: 3 -> 1 (2 ops), 2 -> 1 (1 op), 1 stays
        assert solution.minOperations([3, 2, 1]) == 3

    def test_simple_reduction(self):
        """Test simple case where one element needs reduction"""
        solution = Solution()
        # [5, 2]: 5 -> 1 (2 ops), but we need 5 <= 2, so 5 -> 1, then 1 <= 2, done
        assert solution.minOperations([5, 2]) == 2

    def test_power_of_two(self):
        """Test with power of 2"""
        solution = Solution()
        # [8, 4]: 8 -> 4 (1 op), 4 -> 2 (2 ops), 2 -> 1 (3 ops)
        # Actually: 8 -> 4 (1 op), now 4 >= 4, move on. Then 4 -> 2 (2 ops), 2 >= 1, done.
        assert solution.minOperations([8, 4]) == 1

    def test_power_of_two_decreasing(self):
        """Test power of 2 in decreasing order"""
        solution = Solution()
        # [8, 1]: 8 -> 4 (1 op), 4 -> 2 (2 ops), 2 -> 1 (3 ops)
        assert solution.minOperations([8, 1]) == 3

    def test_three_elements_needs_reduction(self):
        """Test three elements where middle needs reduction"""
        solution = Solution()
        # [6, 4, 1]: 6 -> 3 (1 op), 3 -> 1 (2 ops), 4 -> 2 (3 ops), 2 -> 1 (4 ops)
        assert solution.minOperations([6, 4, 1]) == 4

    def test_with_prime_numbers(self):
        """Test with prime numbers"""
        solution = Solution()
        # [7, 2]: 7 -> 1 (1 op), 1 <= 2
        assert solution.minOperations([7, 2]) == 1

    def test_with_composite_numbers(self):
        """Test with composite numbers"""
        solution = Solution()
        # [6, 3]: 6 -> 3 (1 op), 3 >= 3, done
        assert solution.minOperations([6, 3]) == 1

    def test_with_multiple_operations_needed(self):
        """Test case requiring multiple operations on same element"""
        solution = Solution()
        # [16, 2]: 16 -> 8 (1 op), 8 -> 4 (2 ops), 4 -> 2 (3 ops)
        assert solution.minOperations([16, 2]) == 3

    def test_with_larger_numbers(self):
        """Test with larger numbers within constraints"""
        solution = Solution()
        # [100, 50]: 100 -> 50 (1 op)
        assert solution.minOperations([100, 50]) == 1

    def test_with_larger_numbers_decreasing(self):
        """Test with larger numbers in decreasing order"""
        solution = Solution()
        # [100, 1]: 100 -> 50 (1 op), 50 -> 25 (2 ops), 25 -> 5 (3 ops), 5 -> 1 (4 ops)
        assert solution.minOperations([100, 1]) == 4

    def test_with_mixed_operations(self):
        """Test with mixed operations needed"""
        solution = Solution()
        # [10, 5, 2]: 10 -> 5 (1 op), 5 -> 1 (2 ops), 2 stays
        assert solution.minOperations([10, 5, 2]) == 2

    def test_boundary_value_one(self):
        """Test with boundary value 1"""
        solution = Solution()
        # [1, 10]: already non-decreasing
        assert solution.minOperations([1, 10]) == 0

    def test_boundary_value_max(self):
        """Test with boundary value 10^6"""
        solution = Solution()
        # [1000000, 1]: need to reduce 1000000 to 1
        # 1000000 = 2^6 * 5^6, smallest prime is 2
        # Each division by 2 reduces the number
        # 1000000 -> 500000 -> 250000 -> 125000 -> 62500 -> 31250 -> 15625 (6 ops)
        # 15625 -> 3125 -> 625 -> 125 -> 25 -> 5 -> 1 (6 more ops)
        # Total: 12 ops
        assert solution.minOperations([1000000, 1]) == 12

    def test_two_elements_equal(self):
        """Test two equal elements"""
        solution = Solution()
        assert solution.minOperations([7, 7]) == 0

    def test_two_elements_first_larger(self):
        """Test two elements where first is larger"""
        solution = Solution()
        # [9, 3]: 9 -> 3 (1 op)
        assert solution.minOperations([9, 3]) == 1

    def test_two_elements_second_larger(self):
        """Test two elements where second is larger"""
        solution = Solution()
        # [3, 9]: already non-decreasing
        assert solution.minOperations([3, 9]) == 0
