from typing import List
from solution import Solution


class TestCheckValidCuts:
    def test_horizontal_cuts_possible(self):
        """Three rectangles stacked vertically - horizontal cuts should work."""
        solution = Solution()
        # Rectangles at y=0-1, y=2-3, y=4-5
        # Can cut at y=1.5 and y=3.5 to get 3 sections
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [0, 2, 1, 3], [0, 4, 1, 5]])
        assert result is True

    def test_vertical_cuts_possible(self):
        """Three rectangles side by side - vertical cuts should work."""
        solution = Solution()
        # Rectangles at x=0-1, x=2-3, x=4-5
        # Can cut at x=1.5 and x=3.5 to get 3 sections
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [2, 0, 3, 1], [4, 0, 5, 1]])
        assert result is True

    def test_all_same_y_range(self):
        """All rectangles have same y range - vertical cuts should work."""
        solution = Solution()
        # All three rectangles are in the same y-range but different x
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [2, 0, 3, 1], [4, 0, 5, 1]])
        assert result is True

    def test_all_same_x_range(self):
        """All rectangles have same x range - horizontal cuts should work."""
        solution = Solution()
        # All three rectangles are in the same x-range but different y
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [0, 2, 1, 3], [0, 4, 1, 5]])
        assert result is True

    def test_minimum_rectangles_vertical(self):
        """Minimum 3 rectangles arranged for vertical cuts."""
        solution = Solution()
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [2, 0, 3, 1], [4, 0, 5, 1]])
        assert result is True

    def test_minimum_rectangles_horizontal(self):
        """Minimum 3 rectangles arranged for horizontal cuts."""
        solution = Solution()
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [0, 2, 1, 3], [0, 4, 1, 5]])
        assert result is True

    def test_larger_grid(self):
        """Test with larger n value."""
        solution = Solution()
        result = solution.checkValidCuts(100, [[0, 0, 1, 1], [2, 0, 3, 1], [4, 0, 5, 1]])
        assert result is True

    def test_mixed_arrangement_horizontal_works(self):
        """Mixed arrangement where horizontal cuts work."""
        solution = Solution()
        # Rectangles at different y levels
        result = solution.checkValidCuts(10, [[0, 0, 2, 1], [2, 2, 4, 3], [4, 4, 6, 5]])
        assert result is True

    def test_mixed_arrangement_vertical_works(self):
        """Mixed arrangement where vertical cuts work."""
        solution = Solution()
        # Rectangles at different x levels
        result = solution.checkValidCuts(10, [[0, 0, 1, 2], [2, 0, 3, 2], [4, 0, 5, 2]])
        assert result is True

    def test_staggered_rectangles(self):
        """Three rectangles in a diagonal pattern."""
        solution = Solution()
        # Can use vertical cuts
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [2, 2, 3, 3], [4, 4, 5, 5]])
        assert result is True

    def test_large_n_with_small_rectangles(self):
        """Test with very large n."""
        solution = Solution()
        result = solution.checkValidCuts(1000000000, [[0, 0, 1, 1], [2, 0, 3, 1], [4, 0, 5, 1]])
        assert result is True

    def test_rectangles_at_grid_boundaries(self):
        """Test rectangles at grid boundaries."""
        solution = Solution()
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [1, 0, 2, 1], [2, 0, 3, 1]])
        assert result is True

    def test_only_horizontal_possible(self):
        """Only horizontal cuts work, vertical don't."""
        solution = Solution()
        # All rectangles have same x range but different y
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [0, 2, 1, 3], [0, 4, 1, 5]])
        assert result is True

    def test_only_vertical_possible(self):
        """Only vertical cuts work, horizontal don't."""
        solution = Solution()
        # All rectangles have same y range but different x
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [2, 0, 3, 1], [4, 0, 5, 1]])
        assert result is True

    def test_four_rectangles_stacked(self):
        """Four rectangles stacked vertically - horizontal cuts should work."""
        solution = Solution()
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [0, 2, 1, 3], [0, 4, 1, 5], [0, 6, 1, 7]])
        assert result is True

    def test_four_rectangles_side_by_side(self):
        """Four rectangles side by side - vertical cuts should work."""
        solution = Solution()
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [2, 0, 3, 1], [4, 0, 5, 1], [6, 0, 7, 1]])
        assert result is True

    def test_adjacent_rectangles_horizontal(self):
        """Rectangles adjacent horizontally."""
        solution = Solution()
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [1, 0, 2, 1], [2, 0, 3, 1]])
        assert result is True

    def test_adjacent_rectangles_vertical(self):
        """Rectangles adjacent vertically."""
        solution = Solution()
        result = solution.checkValidCuts(10, [[0, 0, 1, 1], [0, 1, 1, 2], [0, 2, 1, 3]])
        assert result is True
