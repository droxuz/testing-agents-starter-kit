from typing import List
from solution import Solution


class TestMaxDistinctElements:
    """Tests for maxDistinctElements function."""

    def test_all_same_elements(self):
        """All elements are the same, k allows creating distinct values."""
        solution = Solution()
        # [1, 1, 1] with k=1: can make them 1, 2, 3 -> 3 distinct
        assert solution.maxDistinctElements([1, 1, 1], 1) == 3

    def test_all_same_elements_k_zero(self):
        """All elements same, k=0 means no changes possible."""
        solution = Solution()
        # [1, 1, 1] with k=0: all stay 1 -> 1 distinct
        assert solution.maxDistinctElements([1, 1, 1], 0) == 1

    def test_already_distinct(self):
        """All elements already distinct, no duplicates to resolve."""
        solution = Solution()
        # [1, 2, 3] with k=0: already 3 distinct
        assert solution.maxDistinctElements([1, 2, 3], 0) == 3

    def test_already_distinct_k_positive(self):
        """Already distinct with k>0, still same count."""
        solution = Solution()
        # [1, 2, 3] with k=1: still 3 distinct (can keep as is)
        assert solution.maxDistinctElements([1, 2, 3], 1) == 3

    def test_two_duplicates(self):
        """Two elements same, one different."""
        solution = Solution()
        # [1, 1, 2] with k=1: can make them 1, 2, 3 -> 3 distinct
        assert solution.maxDistinctElements([1, 1, 2], 1) == 3

    def test_two_duplicates_k_zero(self):
        """Two elements same, k=0 means no changes."""
        solution = Solution()
        # [1, 1, 2] with k=0: can only be 1, 1, 2 -> 2 distinct
        assert solution.maxDistinctElements([1, 1, 2], 0) == 2

    def test_large_k(self):
        """Large k allows more flexibility."""
        solution = Solution()
        # [1, 1, 1] with k=100: can make them -99, 0, 99 -> 3 distinct
        assert solution.maxDistinctElements([1, 1, 1], 100) == 3

    def test_single_element(self):
        """Single element array."""
        solution = Solution()
        # [5] with any k: 1 distinct
        assert solution.maxDistinctElements([5], 0) == 1
        assert solution.maxDistinctElements([5], 100) == 1

    def test_two_same_elements(self):
        """Exactly two same elements."""
        solution = Solution()
        # [5, 5] with k=1: can make 5, 6 -> 2 distinct
        assert solution.maxDistinctElements([5, 5], 1) == 2

    def test_two_same_elements_k_zero(self):
        """Two same elements with k=0."""
        solution = Solution()
        # [5, 5] with k=0: can only be 5, 5 -> 1 distinct
        assert solution.maxDistinctElements([5, 5], 0) == 1

    def test_three_distinct_with_duplicates(self):
        """Mixed case with some duplicates."""
        solution = Solution()
        # [1, 2, 2, 3] with k=1: can make 1, 2, 3, 4 -> 4 distinct
        assert solution.maxDistinctElements([1, 2, 2, 3], 1) == 4

    def test_large_array_all_same(self):
        """Large array with all same elements."""
        solution = Solution()
        # [1, 1, 1, 1, 1] with k=1: can make 1, 2, 3, 4, 5 -> 5 distinct
        assert solution.maxDistinctElements([1, 1, 1, 1, 1], 1) == 5

    def test_negative_values(self):
        """Test with negative numbers in array."""
        solution = Solution()
        # [-1, -1, -1] with k=1: can make -1, 0, 1 -> 3 distinct
        assert solution.maxDistinctElements([-1, -1, -1], 1) == 3

    def test_large_values(self):
        """Test with large values."""
        solution = Solution()
        # [1000000000, 1000000000, 1000000000] with k=1000000000
        # Can make them 0, 1000000000, 2000000000 -> 3 distinct
        assert solution.maxDistinctElements([10**9, 10**9, 10**9], 10**9) == 3
