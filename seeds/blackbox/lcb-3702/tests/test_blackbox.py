from typing import List
from solution import Solution


class TestMaxLength:
    def test_all_ones_length_2(self):
        """All 1s, length 2: prod=1, lcm=1, gcd=1, lcm*gcd=1"""
        sol = Solution()
        assert sol.maxLength([1, 1]) == 2

    def test_all_ones_length_3(self):
        """All 1s, length 3: prod=1, lcm=1, gcd=1, lcm*gcd=1"""
        sol = Solution()
        assert sol.maxLength([1, 1, 1]) == 3

    def test_all_ones_length_5(self):
        """All 1s, length 5: should return 5"""
        sol = Solution()
        assert sol.maxLength([1, 1, 1, 1, 1]) == 5

    def test_all_same_length_2(self):
        """All same value length 2: always valid (lcm*gcd = prod)"""
        sol = Solution()
        assert sol.maxLength([2, 2]) == 2

    def test_all_same_length_3(self):
        """All same value length 3 (k>1): prod=27, lcm=2, gcd=2, lcm*gcd=4"""
        sol = Solution()
        assert sol.maxLength([3, 3, 3]) == 2

    def test_all_same_length_4(self):
        """All same value length 4 (k>1): prod=16, lcm=2, gcd=2, lcm*gcd=4"""
        sol = Solution()
        assert sol.maxLength([4, 4, 4, 4]) == 2

    def test_two_different_length_2(self):
        """Two different values length 2: always valid"""
        sol = Solution()
        assert sol.maxLength([2, 3]) == 2

    def test_two_different_length_3_with_1(self):
        """[1, 2, 3]: prod=6, gcd=1, lcm=6, lcm*gcd=6"""
        sol = Solution()
        assert sol.maxLength([1, 2, 3]) == 3

    def test_two_different_length_3_without_1(self):
        """[2, 3, 4]: prod=24, gcd=1, lcm=12, lcm*gcd=12"""
        sol = Solution()
        assert sol.maxLength([2, 3, 4]) == 2

    def test_mixed_with_two_non_ones(self):
        """[1, 2, 3, 1, 1]: has 3 ones, 2 non-ones, length 5"""
        sol = Solution()
        assert sol.maxLength([1, 2, 3, 1, 1]) == 5

    def test_mixed_with_three_non_ones(self):
        """[1, 2, 3, 4, 5]: only 1 one, 4 non-ones, max valid is 3"""
        sol = Solution()
        assert sol.maxLength([1, 2, 3, 4, 5]) == 3

    def test_alternating_1_and_2(self):
        """[1, 2, 1, 2, 1, 2]: 3 ones, 3 twos, need 4 ones for length 6"""
        sol = Solution()
        assert sol.maxLength([1, 2, 1, 2, 1, 2]) == 4

    def test_minimal_array_length_2(self):
        """Minimum array length per constraints"""
        sol = Solution()
        assert sol.maxLength([1, 2]) == 2

    def test_minimal_array_length_2_same(self):
        """Minimum array length with same values"""
        sol = Solution()
        assert sol.maxLength([5, 5]) == 2

    def test_maximal_array_length_100_all_ones(self):
        """Maximum array length with all 1s"""
        sol = Solution()
        assert sol.maxLength([1] * 100) == 100

    def test_maximal_array_length_100_all_same(self):
        """Maximum array length with all same values (k>1)"""
        sol = Solution()
        assert sol.maxLength([7] * 100) == 2

    def test_single_1_surrounded_by_non_ones(self):
        """[2, 2, 1, 2, 2]: only 1 one, max valid subarray has 2 non-ones"""
        sol = Solution()
        assert sol.maxLength([2, 2, 1, 2, 2]) == 3

    def test_boundary_value_1(self):
        """Test with boundary value 1"""
        sol = Solution()
        assert sol.maxLength([1, 10]) == 2

    def test_boundary_value_10(self):
        """Test with boundary value 10"""
        sol = Solution()
        assert sol.maxLength([10, 10]) == 2

    def test_three_ones_two_non_ones(self):
        """[1, 1, 1, 2, 3]: 3 ones, 2 non-ones, length 5"""
        sol = Solution()
        assert sol.maxLength([1, 1, 1, 2, 3]) == 5

    def test_two_ones_three_non_ones(self):
        """[1, 1, 2, 3, 4]: 2 ones, 3 non-ones, max valid is 4"""
        sol = Solution()
        assert sol.maxLength([1, 1, 2, 3, 4]) == 4

    def test_no_ones_at_all(self):
        """[2, 3, 4, 5, 6]: 0 ones, max valid is 2"""
        sol = Solution()
        assert sol.maxLength([2, 3, 4, 5, 6]) == 2

    def test_ones_at_end(self):
        """[2, 3, 1, 1]: 2 ones, 2 non-ones, length 4"""
        sol = Solution()
        assert sol.maxLength([2, 3, 1, 1]) == 4

    def test_ones_at_start(self):
        """[1, 1, 2, 3]: 2 ones, 2 non-ones, length 4"""
        sol = Solution()
        assert sol.maxLength([1, 1, 2, 3]) == 4

    def test_all_10s(self):
        """All 10s: prod=10^n, lcm=10, gcd=10, lcm*gcd=100"""
        sol = Solution()
        assert sol.maxLength([10, 10, 10]) == 2

    def test_all_1s_length_10(self):
        """All 1s length 10"""
        sol = Solution()
        assert sol.maxLength([1] * 10) == 10

    def test_mixed_1s_and_2s(self):
        """[1, 2, 1, 2, 1, 2, 1]: 4 ones, 3 twos, need 5 ones for length 7"""
        sol = Solution()
        assert sol.maxLength([1, 2, 1, 2, 1, 2, 1]) == 5

    def test_two_ones_max(self):
        """[2, 2, 2, 1, 1]: 2 ones, 4 non-ones, max valid is 4"""
        sol = Solution()
        assert sol.maxLength([2, 2, 2, 1, 1]) == 4

    def test_three_ones_max(self):
        """[2, 2, 1, 1, 1, 2]: 3 ones, 3 non-ones, need 4 ones for length 6"""
        sol = Solution()
        assert sol.maxLength([2, 2, 1, 1, 1, 2]) == 5
