import pytest
from solution import Solution

class TestSmallestNumber:
    def test_n_1_t_1(self):
        solution = Solution()
        assert solution.smallestNumber(1, 1) == 1

    def test_n_1_t_2(self):
        solution = Solution()
        assert solution.smallestNumber(1, 2) == 2

    def test_n_1_t_3(self):
        solution = Solution()
        assert solution.smallestNumber(1, 3) == 3

    def test_n_1_t_10(self):
        solution = Solution()
        assert solution.smallestNumber(1, 10) == 10

    def test_n_10_t_1(self):
        solution = Solution()
        assert solution.smallestNumber(10, 1) == 10

    def test_n_10_t_10(self):
        solution = Solution()
        assert solution.smallestNumber(10, 10) == 10

    def test_n_25_t_3(self):
        solution = Solution()
        assert solution.smallestNumber(25, 3) == 26

    def test_n_25_t_5(self):
        solution = Solution()
        assert solution.smallestNumber(25, 5) == 25

    def test_n_25_t_10(self):
        solution = Solution()
        assert solution.smallestNumber(25, 10) == 25

    def test_n_25_t_7(self):
        solution = Solution()
        assert solution.smallestNumber(25, 7) == 27

    def test_n_25_t_8(self):
        solution = Solution()
        assert solution.smallestNumber(25, 8) == 28

    def test_n_25_t_9(self):
        solution = Solution()
        assert solution.smallestNumber(25, 9) == 29

    def test_n_4_t_3(self):
        solution = Solution()
        assert solution.smallestNumber(4, 3) == 6

    def test_n_5_t_4(self):
        solution = Solution()
        assert solution.smallestNumber(5, 4) == 8

    def test_n_6_t_5(self):
        solution = Solution()
        assert solution.smallestNumber(6, 5) == 10

    def test_n_7_t_6(self):
        solution = Solution()
        assert solution.smallestNumber(7, 6) == 10

    def test_n_8_t_7(self):
        solution = Solution()
        assert solution.smallestNumber(8, 7) == 10

    def test_n_9_t_8(self):
        solution = Solution()
        assert solution.smallestNumber(9, 8) == 10

    def test_n_99_t_3(self):
        solution = Solution()
        assert solution.smallestNumber(99, 3) == 99

    def test_n_99_t_10(self):
        solution = Solution()
        assert solution.smallestNumber(99, 10) == 100

    def test_n_100_t_1(self):
        solution = Solution()
        assert solution.smallestNumber(100, 1) == 100

    def test_n_1_t_4(self):
        solution = Solution()
        assert solution.smallestNumber(1, 4) == 4

    def test_n_1_t_5(self):
        solution = Solution()
        assert solution.smallestNumber(1, 5) == 5

    def test_n_1_t_6(self):
        solution = Solution()
        assert solution.smallestNumber(1, 6) == 6

    def test_n_1_t_7(self):
        solution = Solution()
        assert solution.smallestNumber(1, 7) == 7

    def test_n_1_t_8(self):
        solution = Solution()
        assert solution.smallestNumber(1, 8) == 8

    def test_n_1_t_9(self):
        solution = Solution()
        assert solution.smallestNumber(1, 9) == 9

    def test_n_99_t_2(self):
        solution = Solution()
        assert solution.smallestNumber(99, 2) == 100

    def test_n_99_t_4(self):
        solution = Solution()
        assert solution.smallestNumber(99, 4) == 100

    def test_n_99_t_5(self):
        solution = Solution()
        assert solution.smallestNumber(99, 5) == 100

    def test_n_99_t_6(self):
        solution = Solution()
        assert solution.smallestNumber(99, 6) == 100

    def test_n_99_t_7(self):
        solution = Solution()
        assert solution.smallestNumber(99, 7) == 100

    def test_n_99_t_8(self):
        solution = Solution()
        assert solution.smallestNumber(99, 8) == 100

    def test_n_99_t_9(self):
        solution = Solution()
        assert solution.smallestNumber(99, 9) == 99

    def test_n_99_t_1(self):
        solution = Solution()
        assert solution.smallestNumber(99, 1) == 99
