from typing import List
from solution import Solution


class TestMaximumCoins:
    def test_single_segment_k_fits(self):
        """Single segment, k fits entirely within it."""
        solution = Solution()
        coins = [[1, 5, 10]]
        k = 3
        # Window [1,3] or [3,5] gives 3 bags * 10 = 30 coins
        assert solution.maximumCoins(coins, k) == 30

    def test_single_segment_k_larger(self):
        """Single segment, k is larger than segment length."""
        solution = Solution()
        coins = [[1, 3, 10]]
        k = 5
        # Window [1,5] overlaps with [1,3] for 3 bags = 30 coins
        assert solution.maximumCoins(coins, k) == 30

    def test_multiple_segments_optimal_at_boundary(self):
        """Multiple segments, optimal window spans across a gap."""
        solution = Solution()
        coins = [[1, 2, 10], [4, 5, 20]]
        k = 3
        # Window [3,5] or [4,6] gets 2 bags from second segment = 40 coins
        assert solution.maximumCoins(coins, k) == 40

    def test_k_equals_one(self):
        """k = 1, should return max coins per bag."""
        solution = Solution()
        coins = [[1, 5, 10]]
        k = 1
        # Any single bag has 10 coins
        assert solution.maximumCoins(coins, k) == 10

    def test_k_equals_segment_length(self):
        """k equals the length of a segment."""
        solution = Solution()
        coins = [[1, 3, 10]]
        k = 3
        # Window [1,3] gets all 3 bags = 30 coins
        assert solution.maximumCoins(coins, k) == 30

    def test_large_k_spanning_multiple_segments(self):
        """Large k that spans multiple segments."""
        solution = Solution()
        coins = [[1, 2, 100], [5, 6, 200]]
        k = 10
        # Window [1,10] gets both segments: 2*100 + 2*200 = 600
        assert solution.maximumCoins(coins, k) == 600

    def test_wide_gaps_between_segments(self):
        """Segments with wide gaps, k fits in one segment."""
        solution = Solution()
        coins = [[1, 1, 10], [10, 10, 20]]
        k = 5
        # Best is window [6,10] or [10,14] getting 1 bag from second segment = 20
        assert solution.maximumCoins(coins, k) == 20

    def test_all_segments_same_value(self):
        """All segments have same coin value per bag."""
        solution = Solution()
        coins = [[1, 2, 10], [4, 5, 10]]
        k = 3
        # Any window of 3 bags in coin-containing areas = 30 coins
        assert solution.maximumCoins(coins, k) == 30

    def test_first_segment_higher_value(self):
        """First segment has higher value than subsequent segments."""
        solution = Solution()
        coins = [[1, 2, 100], [4, 5, 10]]
        k = 3
        # Window [1,3] gets 2 bags from first segment = 200 coins
        assert solution.maximumCoins(coins, k) == 200

    def test_k_equals_two(self):
        """k = 2 with multiple segments."""
        solution = Solution()
        coins = [[1, 2, 10], [4, 5, 20]]
        k = 2
        # Window [4,5] gets 2 bags from second segment = 40 coins
        assert solution.maximumCoins(coins, k) == 40

    def test_single_bag_segments(self):
        """All segments are single bags."""
        solution = Solution()
        coins = [[1, 1, 5], [3, 3, 10], [5, 5, 3]]
        k = 2
        # Window [2,3] or [3,4] gets 1 bag from second segment = 10 coins
        assert solution.maximumCoins(coins, k) == 10

    def test_three_segments(self):
        """Three non-overlapping segments."""
        solution = Solution()
        coins = [[1, 2, 10], [5, 6, 15], [9, 10, 5]]
        k = 3
        # Window [5,7] or [6,8] gets 2 bags from middle segment = 30 coins
        assert solution.maximumCoins(coins, k) == 30

    def test_k_larger_than_all_segments(self):
        """k is larger than any single segment but smaller than total span."""
        solution = Solution()
        coins = [[1, 2, 10], [4, 5, 20]]
        k = 4
        # Window [1,4] or [2,5] gets 2+1=3 bags or 1+2=3 bags = 50 coins
        assert solution.maximumCoins(coins, k) == 50

    def test_k_larger_than_total_span(self):
        """k is larger than total span of all coin-containing bags."""
        solution = Solution()
        coins = [[1, 2, 10], [4, 5, 20]]
        k = 10
        # Window [1,10] gets all 4 bags = 70 coins
        assert solution.maximumCoins(coins, k) == 70
