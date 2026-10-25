from typing import List
from solution import Solution


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


class TestMaxScore:
    def test_single_element(self):
        """Single element array: score is element squared"""
        sol = Solution()
        assert sol.maxScore([5]) == 25

    def test_single_element_one(self):
        """Single element with value 1"""
        sol = Solution()
        assert sol.maxScore([1]) == 1

    def test_single_element_max(self):
        """Single element with maximum value 30"""
        sol = Solution()
        assert sol.maxScore([30]) == 900

    def test_two_elements_same(self):
        """Two identical elements"""
        sol = Solution()
        assert sol.maxScore([3, 3]) == 9

    def test_two_elements_different(self):
        """Two different elements, removing one gives better score"""
        sol = Solution()
        # LCM(2,4)=4, GCD(2,4)=2, score=8
        # Remove 2: [4] -> 16
        # Remove 4: [2] -> 4
        assert sol.maxScore([2, 4]) == 16

    def test_three_elements_all_same(self):
        """Three identical elements"""
        sol = Solution()
        assert sol.maxScore([5, 5, 5]) == 25

    def test_three_elements_mixed(self):
        """Three different elements"""
        sol = Solution()
        # LCM(2,3,4)=12, GCD(2,3,4)=1, score=12
        # Remove 2: [3,4] -> LCM=12, GCD=1, score=12
        # Remove 3: [2,4] -> LCM=4, GCD=2, score=8
        # Remove 4: [2,3] -> LCM=6, GCD=1, score=6
        assert sol.maxScore([2, 3, 4]) == 12

    def test_three_elements_improvement(self):
        """Three elements where removing one improves score"""
        sol = Solution()
        # [6,8,12]: LCM=24, GCD=2, score=48
        # Remove 6: [8,12] -> LCM=24, GCD=4, score=96
        assert sol.maxScore([6, 8, 12]) == 96

    def test_all_ones(self):
        """Array of all 1s"""
        sol = Solution()
        assert sol.maxScore([1, 1, 1]) == 1

    def test_all_thirties(self):
        """Array of all 30s"""
        sol = Solution()
        assert sol.maxScore([30, 30, 30]) == 900

    def test_two_elements_gcd_lcm(self):
        """Two elements where keeping both is optimal"""
        sol = Solution()
        # [4, 6]: LCM=12, GCD=2, score=24
        # Remove 4: [6] -> 36
        # Remove 6: [4] -> 16
        assert sol.maxScore([4, 6]) == 36

    def test_two_elements_keep_both(self):
        """Two elements where keeping both is optimal"""
        sol = Solution()
        # [3, 5]: LCM=15, GCD=1, score=15
        # Remove 3: [5] -> 25
        # Remove 5: [3] -> 9
        assert sol.maxScore([3, 5]) == 25

    def test_large_array_same_elements(self):
        """Large array with identical elements"""
        sol = Solution()
        assert sol.maxScore([7] * 10) == 49

    def test_mixed_array(self):
        """Mixed array with various elements"""
        sol = Solution()
        # [2, 6, 10]: LCM=30, GCD=2, score=60
        # Remove 2: [6,10] -> LCM=30, GCD=2, score=60
        # Remove 6: [2,10] -> LCM=10, GCD=2, score=20
        # Remove 10: [2,6] -> LCM=6, GCD=2, score=12
        assert sol.maxScore([2, 6, 10]) == 60

    def test_remove_improves_gcd(self):
        """Removing an element improves the GCD"""
        sol = Solution()
        # [2, 4, 6]: LCM=12, GCD=2, score=24
        # Remove 2: [4,6] -> LCM=12, GCD=2, score=24
        # Remove 4: [2,6] -> LCM=6, GCD=2, score=12
        # Remove 6: [2,4] -> LCM=4, GCD=2, score=8
        assert sol.maxScore([2, 4, 6]) == 24
