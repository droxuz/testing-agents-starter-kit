from typing import List
from solution import Solution


class TestMaxCollectedFruits:
    def test_2x2_all_different(self):
        """2x2 grid where all rooms have different fruit counts."""
        sol = Solution()
        fruits = [[1, 2], [3, 4]]
        # Child 1: (0,0) -> (1,1) collects 1 + 4 = 5
        # Child 2: (0,1) -> (1,0) -> (1,1) collects 2 + 3 (1,1 already collected) = 5
        # Child 3: (1,0) -> (0,1) -> (1,1) collects 0 (all already collected)
        # Union: all 4 rooms, total = 1+2+3+4 = 10
        result = sol.maxCollectedFruits(fruits)
        assert result == 10

    def test_2x2_all_zeros(self):
        """2x2 grid with all zeros."""
        sol = Solution()
        fruits = [[0, 0], [0, 0]]
        result = sol.maxCollectedFruits(fruits)
        assert result == 0

    def test_2x2_max_fruits_at_start(self):
        """2x2 grid with max fruits at start positions."""
        sol = Solution()
        fruits = [[100, 1], [1, 1]]
        # Child 1 collects (0,0)=100 and (1,1)=1
        # Child 2 collects (0,1)=1 and (1,0)=1
        # Child 3 collects nothing
        # Union: all 4 rooms, total = 100+1+1+1 = 103
        result = sol.maxCollectedFruits(fruits)
        assert result == 103

    def test_3x3_diagonal_only(self):
        """3x3 grid where optimal is just the diagonal (Child 1's path)."""
        sol = Solution()
        fruits = [[100, 1, 1], [1, 1, 1], [1, 1, 100]]
        # Child 1: (0,0) -> (1,1) -> (2,2) collects 100 + 1 + 100 = 201
        # Child 2: (0,2) -> (1,2) -> (2,2) collects 1 + 1 (2,2 already collected) = 2
        # Child 3: (2,0) -> (2,1) -> (2,2) collects 1 + 1 (2,2 already collected) = 2
        # Union: {(0,0), (1,1), (2,2), (0,2), (1,2), (2,0), (2,1)}
        # Total: 100+1+1+1+1+1+100 = 205
        result = sol.maxCollectedFruits(fruits)
        assert result == 205

    def test_3x3_max_coverage(self):
        """3x3 grid where we can cover many rooms."""
        sol = Solution()
        fruits = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # Child 1: (0,0) -> (1,1) -> (2,2) collects 1 + 5 + 9 = 15
        # Child 2: (0,2) -> (1,2) -> (2,2) collects 3 + 6 (2,2 already collected) = 9
        # Child 3: (2,0) -> (2,1) -> (2,2) collects 7 + 8 (2,2 already collected) = 15
        # Union: {(0,0), (1,1), (2,2), (0,2), (1,2), (2,0), (2,1)}
        # Total: 1+5+9+3+6+7+8 = 39
        result = sol.maxCollectedFruits(fruits)
        assert result == 39

    def test_3x3_corner_heavy(self):
        """3x3 grid with heavy corners."""
        sol = Solution()
        fruits = [[10, 1, 1], [1, 1, 1], [1, 1, 10]]
        # Child 1: (0,0) -> (1,1) -> (2,2) collects 10 + 1 + 10 = 21
        # Child 2: (0,2) -> (1,2) -> (2,2) collects 1 + 1 = 2
        # Child 3: (2,0) -> (2,1) -> (2,2) collects 1 + 1 = 2
        # Union: {(0,0), (1,1), (2,2), (0,2), (1,2), (2,0), (2,1)}
        # Total: 10+1+10+1+1+1+1 = 25
        result = sol.maxCollectedFruits(fruits)
        assert result == 25

    def test_3x3_child2_child3_overlap(self):
        """3x3 grid where Child 2 and Child 3 can overlap optimally."""
        sol = Solution()
        fruits = [[1, 100, 1], [1, 1, 1], [1, 1, 100]]
        # Child 1: (0,0) -> (1,1) -> (2,2) collects 1 + 1 + 100 = 102
        # Child 2: (0,2) -> (1,2) -> (2,2) collects 1 + 1 = 2
        # Child 3: (2,0) -> (2,1) -> (2,2) collects 1 + 1 = 2
        # Union: {(0,0), (1,1), (2,2), (0,2), (1,2), (2,0), (2,1)}
        # Total: 1+1+100+1+1+1+1 = 106
        result = sol.maxCollectedFruits(fruits)
        assert result == 106

    def test_boundary_n_2_min(self):
        """Boundary case: minimum n=2."""
        sol = Solution()
        fruits = [[0, 0], [0, 0]]
        result = sol.maxCollectedFruits(fruits)
        assert result == 0

    def test_boundary_n_2_max(self):
        """Boundary case: minimum n=2 with max values."""
        sol = Solution()
        fruits = [[1000, 1000], [1000, 1000]]
        result = sol.maxCollectedFruits(fruits)
        # All 4 rooms can be collected
        assert result == 4000

    def test_boundary_fruit_0(self):
        """Boundary case: fruit value of 0."""
        sol = Solution()
        fruits = [[0, 0], [0, 0]]
        result = sol.maxCollectedFruits(fruits)
        assert result == 0

    def test_boundary_fruit_1000(self):
        """Boundary case: fruit value of 1000."""
        sol = Solution()
        fruits = [[1000, 0], [0, 1000]]
        result = sol.maxCollectedFruits(fruits)
        # All 4 rooms can be collected
        assert result == 2000
