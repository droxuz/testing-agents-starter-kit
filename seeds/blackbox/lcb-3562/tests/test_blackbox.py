from typing import List
from solution import Solution


class TestMaximumWeight:
    def test_single_interval(self):
        """Test with a single interval."""
        solution = Solution()
        intervals = [[1, 2, 5]]
        result = solution.maximumWeight(intervals)
        assert result == [0], f"Expected [0], got {result}"

    def test_two_non_overlapping(self):
        """Test with two non-overlapping intervals."""
        solution = Solution()
        intervals = [[1, 2, 5], [3, 4, 10]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1], f"Expected [0, 1], got {result}"

    def test_two_overlapping(self):
        """Test with two overlapping intervals, pick higher weight."""
        solution = Solution()
        intervals = [[1, 5, 5], [2, 3, 10]]
        result = solution.maximumWeight(intervals)
        assert result == [1], f"Expected [1], got {result}"

    def test_boundary_overlap(self):
        """Test that intervals sharing boundary are considered overlapping."""
        solution = Solution()
        intervals = [[1, 2, 5], [2, 3, 10]]
        result = solution.maximumWeight(intervals)
        assert result == [1], f"Expected [1], got {result}"

    def test_four_non_overlapping(self):
        """Test with exactly 4 non-overlapping intervals."""
        solution = Solution()
        intervals = [[1, 2, 5], [3, 4, 10], [5, 6, 15], [7, 8, 20]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1, 2, 3], f"Expected [0, 1, 2, 3], got {result}"

    def test_choose_three_out_of_five(self):
        """Test choosing 3 out of 5 intervals with max total weight."""
        solution = Solution()
        intervals = [[1, 2, 100], [3, 4, 1], [5, 6, 1], [7, 8, 1], [9, 10, 1]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1, 2, 3], f"Expected [0, 1, 2, 3], got {result}"

    def test_all_overlap_pick_max_weight(self):
        """Test when all intervals overlap, pick the one with max weight."""
        solution = Solution()
        intervals = [[1, 5, 10], [2, 6, 20], [3, 7, 5]]
        result = solution.maximumWeight(intervals)
        assert result == [1], f"Expected [1], got {result}"

    def test_lexicographic_ordering(self):
        """Test lexicographic ordering when multiple solutions have same weight."""
        solution = Solution()
        # Two sets of 2 non-overlapping intervals with same total weight
        # [0,1] with weight 10 each = 20 total
        # [2,3] with weight 10 each = 20 total
        # But we want indices [0, 2] lexicographically vs [1, 3]
        # Actually, we should pick indices in increasing order
        intervals = [[1, 2, 10], [3, 4, 10], [5, 6, 10], [7, 8, 10]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1, 2, 3], f"Expected [0, 1, 2, 3], got {result}"

    def test_lexicographic_with_different_weights(self):
        """Test lexicographic ordering with different weights."""
        solution = Solution()
        # First interval has lower weight but we need to check lex order
        intervals = [[1, 2, 5], [3, 4, 10], [5, 6, 5], [7, 8, 10]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1, 2, 3], f"Expected [0, 1, 2, 3], got {result}"

    def test_point_intervals(self):
        """Test with point intervals where l_i = r_i."""
        solution = Solution()
        intervals = [[1, 1, 5], [2, 2, 10], [3, 3, 15]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1, 2], f"Expected [0, 1, 2], got {result}"

    def test_point_interval_overlap(self):
        """Test that point intervals at same point overlap."""
        solution = Solution()
        intervals = [[1, 1, 5], [1, 1, 10]]
        result = solution.maximumWeight(intervals)
        assert result == [1], f"Expected [1], got {result}"

    def test_large_weights(self):
        """Test with large weights."""
        solution = Solution()
        intervals = [[1, 2, 1000000000], [3, 4, 1000000000], [5, 6, 1000000000], [7, 8, 1000000000]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1, 2, 3], f"Expected [0, 1, 2, 3], got {result}"

    def test_large_coordinates(self):
        """Test with large coordinate values."""
        solution = Solution()
        intervals = [[1000000000, 1000000000, 5], [1000000001, 1000000001, 10]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1], f"Expected [0, 1], got {result}"

    def test_empty_selection_not_possible(self):
        """Test with intervals that all overlap and we pick one."""
        solution = Solution()
        intervals = [[1, 10, 100]]
        result = solution.maximumWeight(intervals)
        assert result == [0], f"Expected [0], got {result}"

    def test_three_intervals_two_non_overlapping(self):
        """Test with 3 intervals where only 2 can be non-overlapping."""
        solution = Solution()
        intervals = [[1, 5, 10], [2, 6, 5], [7, 8, 20]]
        result = solution.maximumWeight(intervals)
        # Index 0 and 2 are non-overlapping, total = 30
        # Index 1 and 2 are non-overlapping, total = 25
        # So we should pick [0, 2]
        assert result == [0, 2], f"Expected [0, 2], got {result}"

    def test_three_intervals_pick_best_pair(self):
        """Test choosing best pair from 3 intervals."""
        solution = Solution()
        intervals = [[1, 5, 30], [2, 6, 40], [7, 8, 10]]
        result = solution.maximumWeight(intervals)
        # [0, 2] = 40, [1, 2] = 50
        # Should pick [1, 2]
        assert result == [1, 2], f"Expected [1, 2], got {result}"

    def test_choose_only_one_of_three(self):
        """Test when only one interval can be chosen."""
        solution = Solution()
        intervals = [[1, 10, 100], [2, 8, 200], [3, 7, 300]]
        result = solution.maximumWeight(intervals)
        assert result == [2], f"Expected [2], got {result}"

    def test_two_sets_of_two(self):
        """Test choosing between two sets of two intervals."""
        solution = Solution()
        # Set 1: indices 0, 1 (non-overlapping), weights 10, 10 = 20
        # Set 2: indices 2, 3 (non-overlapping), weights 15, 15 = 30
        intervals = [[1, 2, 10], [3, 4, 10], [5, 6, 15], [7, 8, 15]]
        result = solution.maximumWeight(intervals)
        assert result == [0, 1, 2, 3], f"Expected [0, 1, 2, 3], got {result}"

    def test_partial_overlap(self):
        """Test with partial overlaps."""
        solution = Solution()
        intervals = [[1, 5, 10], [2, 4, 5], [6, 10, 20]]
        result = solution.maximumWeight(intervals)
        # 0 and 2 are non-overlapping, total = 30
        assert result == [0, 2], f"Expected [0, 2], got {result}"

    def test_five_intervals_pick_four(self):
        """Test choosing 4 out of 5 non-overlapping intervals."""
        solution = Solution()
        intervals = [[1, 2, 1], [3, 4, 2], [5, 6, 3], [7, 8, 4], [9, 10, 100]]
        result = solution.maximumWeight(intervals)
        # Pick 0,1,2,3 (total=10) vs 0,1,2,4 (total=106) vs 0,1,3,4 (total=107) vs 0,2,3,4 (total=109) vs 1,2,3,4 (total=109)
        # [0, 2, 3, 4] = 1+3+4+100 = 108
        # [1, 2, 3, 4] = 2+3+4+100 = 109
        # [0, 1, 3, 4] = 1+2+4+100 = 107
        # [0, 1, 2, 4] = 1+2+3+100 = 106
        # [0, 1, 2, 3] = 1+2+3+4 = 10
        # So [1, 2, 3, 4] should be picked
        assert result == [1, 2, 3, 4], f"Expected [1, 2, 3, 4], got {result}"

    def test_five_intervals_pick_four_lexicographic(self):
        """Test choosing 4 out of 5 with lexicographic ordering."""
        solution = Solution()
        intervals = [[1, 2, 100], [3, 4, 100], [5, 6, 100], [7, 8, 100], [9, 10, 100]]
        result = solution.maximumWeight(intervals)
        # All have same weight, pick lexicographically smallest indices
        assert result == [0, 1, 2, 3], f"Expected [0, 1, 2, 3], got {result}"

    def test_mixed_overlap_scenarios(self):
        """Test with complex overlap scenarios."""
        solution = Solution()
        intervals = [[1, 10, 100], [2, 5, 50], [6, 15, 50], [16, 20, 50]]
        result = solution.maximumWeight(intervals)
        # 0 overlaps with 1 and 2
        # 1 overlaps with 0
        # 2 overlaps with 0
        # 3 doesn't overlap with 0, 1, or 2
        # Best: 0 + 3 = 150, or 1 + 2 + 3 = 150
        # [0, 3] = [0, 3] lexicographically
        # [1, 2, 3] = [1, 2, 3]
        # [0, 3] < [1, 2, 3] lexicographically
        assert result == [0, 3], f"Expected [0, 3], got {result}"

    def test_two_identical_intervals(self):
        """Test with two intervals at same position."""
        solution = Solution()
        intervals = [[1, 5, 50], [1, 5, 100]]
        result = solution.maximumWeight(intervals)
        # Both overlap, pick higher weight
        assert result == [1], f"Expected [1], got {result}"

    def test_three_identical_intervals(self):
        """Test with three intervals at same position."""
        solution = Solution()
        intervals = [[1, 5, 50], [1, 5, 100], [1, 5, 200]]
        result = solution.maximumWeight(intervals)
        # All overlap, pick highest weight
        assert result == [2], f"Expected [2], got {result}"
