from typing import List
from solution import Solution


class TestMaxFrequency:
    def test_basic_case(self):
        """Basic case where we can make some elements equal."""
        solution = Solution()
        # nums = [1, 2, 4], k = 1, numOperations = 2
        # Sorted: [1, 2, 4]
        # Window [1, 2] with target 2: cost = 1, budget = 2*1 = 2, works, freq = 2
        # Window [2, 4] with target 4: cost = 2, budget = 2, works, freq = 2
        # Window [1, 2, 4] with target 4: cost = 5, budget = 2, doesn't work
        assert solution.maxFrequency([1, 2, 4], 1, 2) == 2

    def test_all_can_be_made_equal(self):
        """Case where all elements can be made equal."""
        solution = Solution()
        # nums = [1, 2, 3], k = 10, numOperations = 3
        # Window [1, 2, 3] with target 3: cost = 3, budget = 30, works, freq = 3
        assert solution.maxFrequency([1, 2, 3], 10, 3) == 3

    def test_no_operations(self):
        """Case with numOperations = 0, no changes allowed."""
        solution = Solution()
        # No operations, max frequency is just the max frequency in original array
        assert solution.maxFrequency([1, 2, 3], 1, 0) == 1
        assert solution.maxFrequency([1, 1, 2], 1, 0) == 2
        assert solution.maxFrequency([1, 1, 1], 1, 0) == 3

    def test_k_is_zero(self):
        """Case where k = 0, can't change any values."""
        solution = Solution()
        # Can't change values, so max frequency is just the max frequency in original
        assert solution.maxFrequency([1, 2, 2, 3], 0, 5) == 2
        assert solution.maxFrequency([1, 1, 1], 0, 10) == 3

    def test_single_element(self):
        """Edge case with single element."""
        solution = Solution()
        assert solution.maxFrequency([5], 10, 0) == 1
        assert solution.maxFrequency([5], 10, 1) == 1

    def test_two_elements_same(self):
        """Two same elements."""
        solution = Solution()
        assert solution.maxFrequency([3, 3], 1, 0) == 2
        assert solution.maxFrequency([3, 3], 1, 1) == 2

    def test_two_elements_different(self):
        """Two different elements, can make them equal."""
        solution = Solution()
        # [1, 2], k=1, numOperations=1: can add 1 to first element to make [2, 2]
        assert solution.maxFrequency([1, 2], 1, 1) == 2
        # [1, 2], k=1, numOperations=0: can't change, freq = 1
        assert solution.maxFrequency([1, 2], 1, 0) == 1

    def test_large_gap_requires_more_operations(self):
        """Case where elements are far apart."""
        solution = Solution()
        # [1, 100], k=1, numOperations=1: can only add at most 1 to first
        # Window [1, 100] with target 100: cost = 99, budget = 1, doesn't work
        # Window [1] with target 1: cost = 0, budget = 1, works, freq = 1
        assert solution.maxFrequency([1, 100], 1, 1) == 1
        # With more operations, we can make them equal
        assert solution.maxFrequency([1, 100], 1, 99) == 2

    def test_negative_values_in_range(self):
        """Test with values that can benefit from negative additions."""
        solution = Solution()
        # [5, 5, 6], k=1, numOperations=1
        # Already have two 5s, can make third 5 equal to 5 (add 0)
        assert solution.maxFrequency([5, 5, 6], 1, 1) == 3

    def test_already_sorted(self):
        """Test with already sorted array."""
        solution = Solution()
        # [1, 2, 3, 4], k=1, numOperations=2
        # Window [1, 2, 3] with target 3: cost = 2+1+0 = 3, budget = 2, doesn't work
        # Window [2, 3] with target 3: cost = 1, budget = 2, works, freq = 2
        # Window [3, 4] with target 4: cost = 1, budget = 2, works, freq = 2
        assert solution.maxFrequency([1, 2, 3, 4], 1, 2) == 2

    def test_reversed_order(self):
        """Test with reversed (descending) array."""
        solution = Solution()
        # [4, 3, 2, 1], k=1, numOperations=2
        # Sorted internally: [1, 2, 3, 4]
        # Same as above, answer should be 2
        assert solution.maxFrequency([4, 3, 2, 1], 1, 2) == 2

    def test_many_operations_can_make_all_equal(self):
        """Case with many operations allowing all elements to be equal."""
        solution = Solution()
        # [1, 2, 3, 4, 5], k=10, numOperations=5
        # Window [1, 2, 3, 4, 5] with target 5: cost = 4+3+2+1+0 = 10, budget = 50
        # 10 <= 50, works, freq = 5
        assert solution.maxFrequency([1, 2, 3, 4, 5], 10, 5) == 5

    def test_boundary_k_zero_with_operations(self):
        """k=0 but with operations - operations don't help if k=0."""
        solution = Solution()
        # [1, 2, 3], k=0, numOperations=10
        # Can't change any values, max freq is 1
        assert solution.maxFrequency([1, 2, 3], 0, 10) == 1

    def test_boundary_numOperations_zero(self):
        """numOperations=0 boundary."""
        solution = Solution()
        assert solution.maxFrequency([1, 2, 3], 5, 0) == 1
        assert solution.maxFrequency([1, 1, 1], 5, 0) == 3

    def test_boundary_k_zero_and_numOperations_zero(self):
        """Both k and numOperations at boundaries."""
        solution = Solution()
        assert solution.maxFrequency([1, 2, 3], 0, 0) == 1
        assert solution.maxFrequency([1, 1, 1], 0, 0) == 3

    def test_large_array_all_same(self):
        """Large array with all same elements."""
        solution = Solution()
        # Array of 100000 ones, k=1, numOperations=100000
        # Already all same, freq = 100000
        assert solution.maxFrequency([1] * 100, 1, 100) == 100

    def test_large_array_different(self):
        """Large array with different elements."""
        solution = Solution()
        # [1, 2, 3, ..., 100], k=1000, numOperations=100
        # Can make all equal to 100
        # Cost = sum(100-i for i in 1..100) = 4950
        # Budget = 100 * 1000 = 100000
        # 4950 <= 100000, works, freq = 100
        assert solution.maxFrequency(list(range(1, 101)), 1000, 100) == 100

    def test_exact_budget_boundary(self):
        """Test where cost exactly equals budget."""
        solution = Solution()
        # [1, 2], k=1, numOperations=1
        # Window [1, 2] with target 2: cost = 1, budget = 1
        # 1 <= 1, works, freq = 2
        assert solution.maxFrequency([1, 2], 1, 1) == 2

    def test_one_extra_operation(self):
        """Test with one extra operation beyond minimum."""
        solution = Solution()
        # [1, 2], k=1, numOperations=2
        # Window [1, 2] with target 2: cost = 1, budget = 2
        # 1 <= 2, works, freq = 2
        assert solution.maxFrequency([1, 2], 1, 2) == 2

    def test_all_elements_same_initially(self):
        """All elements are already the same."""
        solution = Solution()
        assert solution.maxFrequency([5, 5, 5, 5], 1, 0) == 4
        assert solution.maxFrequency([5, 5, 5, 5], 1, 1) == 4

    def test_three_elements_two_same(self):
        """Three elements with two already equal."""
        solution = Solution()
        # [1, 1, 2], k=1, numOperations=1
        # Window [1, 1, 2] with target 2: cost = 0+0+0 = 0, budget = 1
        # Wait, that's not right. Window [1, 1, 2] means making all equal to 2
        # Cost = (2-1) + (2-1) + (2-2) = 1 + 1 + 0 = 2
        # Budget = 1*1 = 1
        # 2 > 1, doesn't work
        # Window [1, 1] with target 1: cost = 0, budget = 1, works, freq = 2
        # Window [1, 2] with target 2: cost = 1, budget = 1, works, freq = 2
        assert solution.maxFrequency([1, 1, 2], 1, 1) == 2

    def test_three_elements_two_same_with_more_operations(self):
        """Three elements with two already equal, enough operations to make all equal."""
        solution = Solution()
        # [1, 1, 2], k=1, numOperations=2
        # Window [1, 1, 2] with target 2: cost = 2, budget = 2
        # 2 <= 2, works, freq = 3
        assert solution.maxFrequency([1, 1, 2], 1, 2) == 3

    def test_unsorted_array(self):
        """Unsorted array - function should sort internally."""
        solution = Solution()
        # [4, 1, 3, 2], k=1, numOperations=2
        # Sorted: [1, 2, 3, 4]
        # Same as test_already_sorted
        assert solution.maxFrequency([4, 1, 3, 2], 1, 2) == 2

    def test_numOperations_equals_length(self):
        """numOperations equals array length."""
        solution = Solution()
        # [1, 2, 3], k=100, numOperations=3
        # Window [1, 2, 3] with target 3: cost = 3, budget = 300
        # 3 <= 300, works, freq = 3
        assert solution.maxFrequency([1, 2, 3], 100, 3) == 3

    def test_minimum_constraints(self):
        """Test with minimum constraint values."""
        solution = Solution()
        # nums.length = 1, nums[i] = 1, k = 0, numOperations = 0
        assert solution.maxFrequency([1], 0, 0) == 1

    def test_maximum_frequency_with_large_k(self):
        """Large k allows making elements equal easily."""
        solution = Solution()
        # [1, 100000], k=100000, numOperations=1
        # Window [1, 100000] with target 100000: cost = 99999, budget = 100000
        # 99999 <= 100000, works, freq = 2
        assert solution.maxFrequency([1, 100000], 100000, 1) == 2
