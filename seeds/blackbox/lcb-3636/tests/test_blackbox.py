from solution import Solution


class TestIsBalanced:
    def test_min_length_balanced(self):
        """Minimum length string that is balanced: '11' (even sum=1, odd sum=1)"""
        sol = Solution()
        assert sol.isBalanced("11") is True

    def test_min_length_unbalanced(self):
        """Minimum length string that is unbalanced: '12' (even sum=1, odd sum=2)"""
        sol = Solution()
        assert sol.isBalanced("12") is False

    def test_length_3_balanced(self):
        """Length 3 balanced: '121' (even sum=1+1=2, odd sum=2)"""
        sol = Solution()
        assert sol.isBalanced("121") is True

    def test_length_3_unbalanced(self):
        """Length 3 unbalanced: '123' (even sum=1+3=4, odd sum=2)"""
        sol = Solution()
        assert sol.isBalanced("123") is False

    def test_length_4_balanced(self):
        """Length 4 balanced: '1221' (even sum=1+2=3, odd sum=2+1=3)"""
        sol = Solution()
        assert sol.isBalanced("1221") is True

    def test_length_4_unbalanced(self):
        """Length 4 unbalanced: '1212' (even sum=1+1=2, odd sum=2+2=4)"""
        sol = Solution()
        assert sol.isBalanced("1212") is False

    def test_all_same_digits_balanced(self):
        """All same digits should be balanced"""
        sol = Solution()
        assert sol.isBalanced("5555") is True

    def test_alternating_same_digits_balanced(self):
        """Alternating pattern with balanced sums"""
        sol = Solution()
        assert sol.isBalanced("121212") is False  # even=1+1+1=3, odd=2+2+2=6

    def test_all_zeros_balanced(self):
        """All zeros should be balanced"""
        sol = Solution()
        assert sol.isBalanced("0000") is True

    def test_length_99_balanced(self):
        """Length 99 balanced string"""
        sol = Solution()
        # Create a balanced string of length 99
        # Pattern: 1,2,1,2,... with even indices summing to odd indices sum
        # For length 99 (odd), indices 0-98, even indices: 0,2,4,...,98 (50 indices)
        # odd indices: 1,3,5,...,97 (49 indices)
        # If we use pattern 1,1,1,1... all same, even sum = 50, odd sum = 49 - not balanced
        # Try pattern 1,2,1,2... even sum = 50*1 = 50, odd sum = 49*2 = 98 - not balanced
        # Try pattern 2,1,2,1... even sum = 50*2 = 100, odd sum = 49*1 = 49 - not balanced
        # Need: 50*a = 49*b for some digits a, b
        # Let's use: 1,1,1,1... all 1s doesn't work
        # Let's construct manually: first 98 chars balanced, add one more
        # Actually let's just use a simple balanced pattern
        # "11" repeated 49 times + "1" = 99 chars, even sum = 50, odd sum = 49*1 = 49
        # Hmm, let me think again...
        # For even length n, even indices = n/2, odd indices = n/2
        # For odd length n, even indices = (n+1)/2, odd indices = (n-1)/2
        # Length 99: even indices = 50, odd indices = 49
        # To balance: sum_even = sum_odd
        # If all digits are same d: 50*d = 49*d, only works if d=0
        # Let's use "000...000" (all zeros)
        assert sol.isBalanced("0" * 99) is True

    def test_length_100_balanced(self):
        """Length 100 balanced string"""
        sol = Solution()
        # Length 100: even indices = 50, odd indices = 50
        # All same digits should work: 50*d = 50*d
        assert sol.isBalanced("5" * 100) is True

    def test_length_100_unbalanced(self):
        """Length 100 unbalanced string"""
        sol = Solution()
        # Mix digits to make it unbalanced
        assert sol.isBalanced("1" * 50 + "2" * 50) is False  # even sum = 50*1 = 50, odd sum = 50*2 = 100

    def test_single_digit_at_each_position(self):
        """Test with single digits at each position"""
        sol = Solution()
        # "13" - even sum = 1, odd sum = 3
        assert sol.isBalanced("13") is False
        # "31" - even sum = 3, odd sum = 1
        assert sol.isBalanced("31") is False

    def test_max_length_edge_case(self):
        """Test at maximum boundary length 100"""
        sol = Solution()
        # Create a balanced string where even and odd sums match
        # Pattern: 1,1,1,1... all ones
        assert sol.isBalanced("1" * 100) is True
