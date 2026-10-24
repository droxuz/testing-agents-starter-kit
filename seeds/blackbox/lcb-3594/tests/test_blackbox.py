from typing import List
from solution import Solution


class TestGetLargestOutlier:
    """Tests for getLargestOutlier function."""

    def test_minimal_valid_case(self):
        """Test [2, 2, 3] where special=[2], sum=2, outlier=3."""
        sol = Solution()
        result = sol.getLargestOutlier([2, 2, 3])
        assert result == 3

    def test_minimal_valid_case_reverse(self):
        """Test [2, 3, 2] where special=[2], sum=2, outlier=3."""
        sol = Solution()
        result = sol.getLargestOutlier([2, 3, 2])
        assert result == 3

    def test_negative_numbers(self):
        """Test with negative numbers."""
        sol = Solution()
        # [0, -1, -1]: special=[-1], sum=-1, one of [0,-1] is -1, other is 0. Outlier=0.
        result = sol.getLargestOutlier([0, -1, -1])
        assert result == 0

    def test_all_same(self):
        """Test with all same numbers."""
        sol = Solution()
        # [5, 5, 5]: special=[5], sum=5, one of [5,5] is 5, other is 5. Outlier=5.
        result = sol.getLargestOutlier([5, 5, 5])
        assert result == 5

    def test_four_elements(self):
        """Test with 4 elements."""
        sol = Solution()
        # [1, 2, 3, 4]: outliers are 2 and 4. Largest is 4.
        result = sol.getLargestOutlier([1, 2, 3, 4])
        assert result == 4

    def test_four_elements_variant(self):
        """Test another 4 element case."""
        sol = Solution()
        result = sol.getLargestOutlier([3, 1, 4, 2])
        assert result == 4

    def test_larger_array(self):
        """Test with larger array."""
        sol = Solution()
        # [1, 1, 2, 4]: outlier is 4.
        result = sol.getLargestOutlier([1, 1, 2, 4])
        assert result == 4

    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative numbers."""
        sol = Solution()
        # [-5, -5, 10]: special=[-5], sum=-5, one of [-5,10] is -5, other is 10. Outlier=10.
        result = sol.getLargestOutlier([-5, -5, 10])
        assert result == 10

    def test_zero_inclusion(self):
        """Test with zero in the array."""
        sol = Solution()
        result = sol.getLargestOutlier([0, 0, 0])
        assert result == 0

    def test_zero_as_sum(self):
        """Test where sum is zero."""
        sol = Solution()
        # [0, 0, 1]: special=[0], sum=0, one of [0,1] is 0, other is 1. Outlier=1.
        result = sol.getLargestOutlier([0, 0, 1])
        assert result == 1

    def test_multiple_outliers(self):
        """Test case with multiple valid outlier values."""
        sol = Solution()
        # [1, 2, 3, 5]: outliers are 1 and 5. Largest is 5.
        result = sol.getLargestOutlier([1, 2, 3, 5])
        assert result == 5

    def test_boundary_values(self):
        """Test with boundary values."""
        sol = Solution()
        # [-1000, -1000, -1000]: special=[-1000], sum=-1000, outlier=-1000.
        result = sol.getLargestOutlier([-1000, -1000, -1000])
        assert result == -1000

    def test_boundary_positive(self):
        """Test with boundary positive values."""
        sol = Solution()
        result = sol.getLargestOutlier([1000, 1000, 1000])
        assert result == 1000

    def test_two_outliers_same_value(self):
        """Test when both potential outliers have same value."""
        sol = Solution()
        # [2, 2, 4]: outlier is 4.
        result = sol.getLargestOutlier([2, 2, 4])
        assert result == 4

    def test_three_elements_different(self):
        """Test three elements where outlier is different."""
        sol = Solution()
        # [1, 1, 2]: special=[1], sum=1, one of [1,2] is 1, other is 2. Outlier=2.
        result = sol.getLargestOutlier([1, 1, 2])
        assert result == 2

    def test_three_elements_sum_case(self):
        """Test where the sum element is the outlier."""
        sol = Solution()
        # [1, 2, 2]: outlier is 1.
        result = sol.getLargestOutlier([1, 2, 2])
        assert result == 1

    def test_large_array(self):
        """Test with larger array to ensure algorithm scales."""
        sol = Solution()
        # [1, 2, 3, 4, 5, 10]: outlier is 5.
        result = sol.getLargestOutlier([1, 2, 3, 4, 5, 10])
        assert result == 5

    def test_basic_three_elements(self):
        """Test with minimal array of 3 elements."""
        sol = Solution()
        # [2, 2, 3]: special=[2], sum=2, outlier=3.
        result = sol.getLargestOutlier([2, 2, 3])
        assert result == 3
