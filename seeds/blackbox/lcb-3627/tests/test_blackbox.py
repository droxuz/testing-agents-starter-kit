from typing import List
from solution import Solution


class TestMinTimeToReach:
    """Tests for minTimeToReach function."""

    def test_basic_2x2_all_zeros(self):
        """2x2 grid with all move times 0 - should take 2 steps."""
        solution = Solution()
        moveTime = [[0, 0],
                    [0, 0]]
        assert solution.minTimeToReach(moveTime) == 2

    def test_2x2_with_blocking(self):
        """2x2 grid with high blocking values requires waiting."""
        solution = Solution()
        moveTime = [[0, 100],
                    [100, 0]]
        # Path: (0,0) -> (0,1) at time 101 -> (1,1) at time 102
        # Or: (0,0) -> (1,0) at time 101 -> (1,1) at time 102
        assert solution.minTimeToReach(moveTime) == 102

    def test_2x2_mixed_values(self):
        """2x2 grid with mixed values."""
        solution = Solution()
        moveTime = [[0, 1],
                    [1, 0]]
        # Path: (0,0) -> (0,1) at time 2 -> (1,1) at time 3
        # Or: (0,0) -> (1,0) at time 2 -> (1,1) at time 3
        assert solution.minTimeToReach(moveTime) == 3

    def test_3x3_all_zeros(self):
        """3x3 grid with all zeros - shortest path is 4 steps."""
        solution = Solution()
        moveTime = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]
        assert solution.minTimeToReach(moveTime) == 4

    def test_3x3_with_blocking_middle(self):
        """3x3 grid with blocking in middle - forces longer path."""
        solution = Solution()
        moveTime = [[0, 0, 0],
                    [0, 100, 0],
                    [0, 0, 0]]
        # Must go around the 100: (0,0)->(0,1)->(0,2)->(1,2)->(2,2) = 4 steps
        # Or: (0,0)->(1,0)->(2,0)->(2,1)->(2,2) = 4 steps
        assert solution.minTimeToReach(moveTime) == 4

    def test_3x3_blocking_corners(self):
        """3x3 grid with blocking at corners."""
        solution = Solution()
        moveTime = [[0, 0, 100],
                    [0, 0, 0],
                    [100, 0, 0]]
        # Path: (0,0)->(0,1)->(1,1)->(1,2)->(2,2) = 4 steps
        assert solution.minTimeToReach(moveTime) == 4

    def test_2x3_grid(self):
        """2x3 grid with all zeros."""
        solution = Solution()
        moveTime = [[0, 0, 0],
                    [0, 0, 0]]
        # Path: 4 steps minimum (right, right, down or down, right, right)
        assert solution.minTimeToReach(moveTime) == 4

    def test_3x2_grid(self):
        """3x2 grid with all zeros."""
        solution = Solution()
        moveTime = [[0, 0],
                    [0, 0],
                    [0, 0]]
        # Path: 4 steps minimum
        assert solution.minTimeToReach(moveTime) == 4

    def test_minimum_time_zero(self):
        """Start at (0,0) and target is also (0,0) - but n,m >= 2."""
        solution = Solution()
        moveTime = [[0, 0],
                    [0, 0]]
        # Actually we need to reach (1,1) not (0,0)
        # But this tests the base case of moveTime[0][0] = 0
        assert solution.minTimeToReach(moveTime) == 2

    def test_large_move_time_values(self):
        """Test with very large move time values."""
        solution = Solution()
        moveTime = [[0, 1000000000],
                    [1000000000, 0]]
        assert solution.minTimeToReach(moveTime) == 1000000002

    def test_one_step_path(self):
        """Test with 2x2 where we can reach in minimum 2 steps."""
        solution = Solution()
        moveTime = [[0, 0],
                    [0, 0]]
        assert solution.minTimeToReach(moveTime) == 2

    def test_waiting_required(self):
        """Test where waiting is required before moving."""
        solution = Solution()
        moveTime = [[0, 5],
                    [5, 0]]
        # (0,0) -> (0,1): arrive at max(0,5)+1 = 6
        # (0,1) -> (1,1): arrive at max(6,0)+1 = 7
        # (0,0) -> (1,0): arrive at max(0,5)+1 = 6
        # (1,0) -> (1,1): arrive at max(6,0)+1 = 7
        assert solution.minTimeToReach(moveTime) == 7

    def test_4x4_grid(self):
        """Test with larger 4x4 grid."""
        solution = Solution()
        moveTime = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
        # Shortest path from (0,0) to (3,3) is 6 steps
        assert solution.minTimeToReach(moveTime) == 6

    def test_boundary_n_2_m_2(self):
        """Test minimum size grid 2x2."""
        solution = Solution()
        moveTime = [[0, 0],
                    [0, 0]]
        assert solution.minTimeToReach(moveTime) == 2

    def test_boundary_n_50_m_50(self):
        """Test maximum size grid 50x50 with all zeros."""
        solution = Solution()
        moveTime = [[0] * 50 for _ in range(50)]
        # Shortest path is 49 + 49 = 98 steps
        assert solution.minTimeToReach(moveTime) == 98

    def test_diagonal_movement(self):
        """Test where diagonal-like movement is forced."""
        solution = Solution()
        moveTime = [[0, 100, 0],
                    [100, 0, 100],
                    [0, 100, 0]]
        # Path: (0,0)->(0,1)->(0,2)->(1,2)->(2,2) = 4 steps
        assert solution.minTimeToReach(moveTime) == 4

    def test_start_blocking(self):
        """Test where start position has high blocking."""
        solution = Solution()
        moveTime = [[100, 0],
                    [0, 0]]
        # Start at (0,0) at t=0, but moveTime[0][0]=100
        # Actually we start at (0,0) at t=0 regardless, so this shouldn't block
        # (0,0)->(0,1): arrive at max(0,0)+1 = 1
        # (0,1)->(1,1): arrive at max(1,0)+1 = 2
        assert solution.minTimeToReach(moveTime) == 2

    def test_longer_path_faster(self):
        """Test where longer path in steps is faster due to lower moveTime."""
        solution = Solution()
        moveTime = [[0, 0, 0],
                    [0, 1000, 0],
                    [0, 0, 0]]
        # Path through (0,1)->(0,2)->(1,2)->(2,2): 3 steps, no waiting
        # Path through (0,1)->(1,1)->(1,2)->(2,2): 3 steps, wait at (1,1)
        # Both paths have same length, but going through (1,1) would be slower
        # Actually: (0,0)->(0,1)->(0,2)->(1,2)->(2,2) = 4 steps, no waiting
        # (0,0)->(0,1)->(1,1)->(1,2)->(2,2) = 4 steps, wait at (1,1)
        # Both should take 4 steps
        assert solution.minTimeToReach(moveTime) == 4

    def test_alternate_shorter_path(self):
        """Test where alternate path is shorter."""
        solution = Solution()
        moveTime = [[0, 0, 0],
                    [100, 0, 100],
                    [0, 0, 0]]
        # Path through (1,1): (0,0)->(0,1)->(1,1)->(1,2)->(2,2) = 4 steps
        # Path around: (0,0)->(0,1)->(0,2)->(1,2)->(2,2) = 4 steps
        # Both same length
        assert solution.minTimeToReach(moveTime) == 4

    def test_2x2_with_start_blocking(self):
        """Test where moveTime[0][0] is high (shouldn't matter since we start there)."""
        solution = Solution()
        moveTime = [[100, 0],
                    [0, 0]]
        # We start at (0,0) at t=0 regardless of moveTime[0][0]
        # (0,0)->(0,1): arrive at max(0,0)+1 = 1
        # (0,1)->(1,1): arrive at max(1,0)+1 = 2
        assert solution.minTimeToReach(moveTime) == 2
