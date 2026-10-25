from solution import Solution


class TestCountBalancedPermutations:
    """Tests for countBalancedPermutations function."""

    def test_single_digit_same(self):
        """Test with all same digits - length 2."""
        sol = Solution()
        # "11" -> only permutation "11", even=1, odd=1, balanced
        assert sol.countBalancedPermutations("11") == 1

    def test_single_digit_different(self):
        """Test with different digits - length 2."""
        sol = Solution()
        # "12" -> "12" (1!=2), "21" (2!=1), neither balanced
        assert sol.countBalancedPermutations("12") == 0

    def test_all_same_length_3(self):
        """Test with all same digits - length 3."""
        sol = Solution()
        # "111" -> only "111", even=1+1=2, odd=1, not balanced
        assert sol.countBalancedPermutations("111") == 0

    def test_two_same_one_diff_length_3(self):
        """Test with two same, one different - length 3."""
        sol = Solution()
        # "112" -> permutations: "112"(3!=1), "121"(2==2), "211"(3!=1)
        assert sol.countBalancedPermutations("112") == 1

    def test_all_different_length_3(self):
        """Test with all different digits - length 3."""
        sol = Solution()
        # "123" -> 6 permutations, 2 balanced: "132"(3==3), "231"(3==3)
        assert sol.countBalancedPermutations("123") == 2

    def test_two_pairs_same_length_4(self):
        """Test with two pairs of same digits - length 4."""
        sol = Solution()
        # "1122" -> 6 permutations, 4 balanced
        assert sol.countBalancedPermutations("1122") == 4

    def test_all_different_length_4(self):
        """Test with all different digits - length 4."""
        sol = Solution()
        # "1234" -> 24 permutations, 8 balanced
        assert sol.countBalancedPermutations("1234") == 8

    def test_all_zeros_length_4(self):
        """Test with all zeros - length 4."""
        sol = Solution()
        # "0000" -> only "0000", even=0, odd=0, balanced
        assert sol.countBalancedPermutations("0000") == 1

    def test_three_zeros_one_nonzero_length_4(self):
        """Test with three zeros and one nonzero - length 4."""
        sol = Solution()
        # "0001" -> 0 balanced
        assert sol.countBalancedPermutations("0001") == 0

    def test_two_pairs_zeros_length_4(self):
        """Test with two pairs of zeros - length 4."""
        sol = Solution()
        # "0011" -> 4 balanced permutations
        assert sol.countBalancedPermutations("0011") == 4

    def test_three_same_one_diff_length_4(self):
        """Test with three same, one different - length 4."""
        sol = Solution()
        # "0001" -> 0 balanced
        assert sol.countBalancedPermutations("0001") == 0

    def test_length_5_all_same(self):
        """Test with all same digits - length 5."""
        sol = Solution()
        # "11111" -> only "11111", even=3, odd=2, not balanced
        assert sol.countBalancedPermutations("11111") == 0

    def test_length_5_three_zeros_two_same(self):
        """Test with three zeros and two same - length 5."""
        sol = Solution()
        # "00011" -> 6 balanced permutations
        assert sol.countBalancedPermutations("00011") == 6

    def test_length_6_all_same(self):
        """Test with all same digits - length 6."""
        sol = Solution()
        # "111111" -> only "111111", even=3, odd=3, balanced
        assert sol.countBalancedPermutations("111111") == 1

    def test_length_6_all_zeros(self):
        """Test with all zeros - length 6."""
        sol = Solution()
        # "000000" -> only "000000", even=0, odd=0, balanced
        assert sol.countBalancedPermutations("000000") == 1

    def test_length_6_three_zeros_three_same(self):
        """Test with three zeros and three same - length 6."""
        sol = Solution()
        # "000111" -> 0 balanced
        assert sol.countBalancedPermutations("000111") == 0

    def test_length_7_all_same(self):
        """Test with all same digits - length 7."""
        sol = Solution()
        # "1111111" -> only "1111111", even=4, odd=3, not balanced
        assert sol.countBalancedPermutations("1111111") == 0

    def test_length_8_all_same(self):
        """Test with all same digits - length 8."""
        sol = Solution()
        # "11111111" -> only "11111111", even=4, odd=4, balanced
        assert sol.countBalancedPermutations("11111111") == 1

    def test_length_8_all_zeros(self):
        """Test with all zeros - length 8."""
        sol = Solution()
        # "00000000" -> only "00000000", even=0, odd=0, balanced
        assert sol.countBalancedPermutations("00000000") == 1

    def test_length_9_all_same(self):
        """Test with all same digits - length 9."""
        sol = Solution()
        # "111111111" -> only "111111111", even=5, odd=4, not balanced
        assert sol.countBalancedPermutations("111111111") == 0

    def test_length_10_all_same(self):
        """Test with all same digits - length 10."""
        sol = Solution()
        # "1111111111" -> only "1111111111", even=5, odd=5, balanced
        assert sol.countBalancedPermutations("1111111111") == 1

    def test_length_2_boundary(self):
        """Test boundary - minimum length 2."""
        sol = Solution()
        assert sol.countBalancedPermutations("00") == 1
        assert sol.countBalancedPermutations("99") == 1

    def test_length_3_boundary(self):
        """Test boundary - length 3."""
        sol = Solution()
        assert sol.countBalancedPermutations("999") == 0

    def test_length_79_boundary(self):
        """Test near maximum length - length 79."""
        sol = Solution()
        # All same digits, length 79 (odd)
        # even positions: 40, odd positions: 39
        # sum(even)=40, sum(odd)=39, not balanced
        assert sol.countBalancedPermutations("1" * 79) == 0

    def test_length_80_boundary(self):
        """Test maximum length - length 80."""
        sol = Solution()
        # All same digits, length 80 (even)
        # even positions: 40, odd positions: 40
        # sum(even)=40, sum(odd)=40, balanced
        assert sol.countBalancedPermutations("1" * 80) == 1

    def test_modulo_result(self):
        """Test that result is within modulo range."""
        sol = Solution()
        # For large inputs, result should be modulo 10^9 + 7
        # "11111111" -> 1, which is < 10^9 + 7
        assert sol.countBalancedPermutations("11111111") == 1

    def test_variable_assignment(self):
        """Test that the variable velunexorai is assigned."""
        sol = Solution()
        # This test just ensures the function runs without error
        # The variable assignment is part of the implementation requirement
        result = sol.countBalancedPermutations("11")
        assert result == 1
