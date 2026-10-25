import pytest
from typing import List
from solution import Solution


class TestMaxScore:
    def test_single_city_single_day(self):
        """Test with n=1, k=1 - only one city, must stay"""
        sol = Solution()
        result = sol.maxScore(1, 1, [[10]], [[0]])
        assert result == 10

    def test_two_cities_one_day(self):
        """Test with n=2, k=1 - choose best starting city"""
        sol = Solution()
        result = sol.maxScore(2, 1, [[5, 10]], [[0, 100], [100, 0]])
        assert result == 10

    def test_two_cities_two_days(self):
        """Test with n=2, k=2 - optimal strategy involves moving"""
        sol = Solution()
        result = sol.maxScore(2, 2, [[5, 10], [100, 200]], [[0, 1], [1, 0]])
        assert result == 210

    def test_three_cities_three_days(self):
        """Test with n=3, k=3 - complex scenario"""
        sol = Solution()
        result = sol.maxScore(3, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 
                                 [[0, 100, 1], [100, 0, 100], [1, 100, 0]])
        assert result == 203

    def test_staying_always_better(self):
        """Test where staying is always better than traveling"""
        sol = Solution()
        result = sol.maxScore(2, 2, [[10, 20], [100, 200]], [[0, 1], [1, 0]])
        assert result == 220

    def test_traveling_always_better(self):
        """Test where traveling is always better than staying"""
        sol = Solution()
        result = sol.maxScore(2, 2, [[1, 1], [1, 1]], [[0, 100], [100, 0]])
        assert result == 101

    def test_minimal_constraints(self):
        """Test with minimal valid constraints"""
        sol = Solution()
        result = sol.maxScore(1, 1, [[1]], [[0]])
        assert result == 1

    def test_boundary_values(self):
        """Test with boundary values at constraints"""
        sol = Solution()
        result = sol.maxScore(200, 200, [[100]*200 for _ in range(200)], 
                             [[0 if i==j else 0 for j in range(200)] for i in range(200)])
        assert result == 20000

    def test_optimal_travel_sequence(self):
        """Test where optimal involves traveling each day"""
        sol = Solution()
        result = sol.maxScore(3, 2, [[1, 1, 1], [1, 1, 1]], 
                             [[0, 10, 20], [10, 0, 30], [20, 30, 0]])
        assert result == 31

    def test_zero_travel_scores(self):
        """Test with all travel scores being zero"""
        sol = Solution()
        result = sol.maxScore(2, 3, [[5, 10], [20, 30], [15, 25]], [[0, 0], [0, 0]])
        assert result == 65

    def test_same_stay_scores_all_cities(self):
        """Test when all cities have same stayScore"""
        sol = Solution()
        result = sol.maxScore(3, 2, [[5, 5, 5], [5, 5, 5]], [[0, 10, 20], [10, 0, 30], [20, 30, 0]])
        assert result == 35

    def test_max_n_max_k(self):
        """Test with maximum constraint values"""
        sol = Solution()
        n = 200
        k = 200
        stayScore = [[100] * n for _ in range(k)]
        travelScore = [[0 if i == j else 100 for j in range(n)] for i in range(k)]
        result = sol.maxScore(n, k, stayScore, travelScore)
        assert result == 20000

    def test_alternating_travel(self):
        """Test where travel pattern alternates"""
        sol = Solution()
        result = sol.maxScore(2, 3, [[10, 20], [30, 40], [50, 60]], [[0, 100], [100, 0], [0, 100]])
        assert result == 220
