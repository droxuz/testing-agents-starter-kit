from typing import List
from solution import Solution


class TestSubsequencePairCount:
    """Tests for subsequencePairCount function."""

    def test_single_element(self):
        """Single element - no pairs possible."""
        sol = Solution()
        assert sol.subsequencePairCount([1]) == 0

    def test_two_same_elements(self):
        """Two same elements - 2 ordered pairs with same GCD."""
        sol = Solution()
        # [1] at idx 0 and [1] at idx 1 are disjoint, both have GCD=1
        # Ordered pairs: ([1]_0, [1]_1) and ([1]_1, [1]_0)
        assert sol.subsequencePairCount([2, 2]) == 2

    def test_two_same_ones(self):
        """Two 1s - 2 ordered pairs with GCD=1."""
        sol = Solution()
        assert sol.subsequencePairCount([1, 1]) == 2

    def test_three_elements_distinct(self):
        """[1, 2, 3] - all subsequences have GCD=1, count disjoint pairs."""
        sol = Solution()
        # All 7 non-empty subsequences have GCD=1
        # For each subsequence of size k, 2^(3-k)-1 disjoint non-empty subsequences
        # Size 1: 3 * (2^2-1) = 3*3 = 9
        # Size 2: 3 * (2^1-1) = 3*1 = 3
        # Size 3: 1 * (2^0-1) = 1*0 = 0
        # Total = 12
        assert sol.subsequencePairCount([1, 2, 3]) == 12

    def test_three_same_ones(self):
        """[1, 1, 1] - all subsequences have GCD=1."""
        sol = Solution()
        # 7 non-empty subsequences, all GCD=1
        # Size 1: 3 * 3 = 9
        # Size 2: 3 * 1 = 3
        # Size 3: 1 * 0 = 0
        # Total = 12
        assert sol.subsequencePairCount([1, 1, 1]) == 12

    def test_all_same_elements(self):
        """[2, 2, 2] - all subsequences have GCD=2."""
        sol = Solution()
        assert sol.subsequencePairCount([2, 2, 2]) == 12

    def test_mixed_gcds(self):
        """[2, 4, 6] - mixed GCDs."""
        sol = Solution()
        # [2]: GCD=2, disjoint with GCD=2: [4,6] = 1
        # [4]: GCD=4, disjoint with GCD=4: none = 0
        # [6]: GCD=6, disjoint with GCD=6: none = 0
        # [2,4]: GCD=2, disjoint with GCD=2: none = 0
        # [2,6]: GCD=2, disjoint with GCD=2: none = 0
        # [4,6]: GCD=2, disjoint with GCD=2: [2] = 1
        # [2,4,6]: GCD=2, disjoint with GCD=2: none = 0
        # Total = 2
        assert sol.subsequencePairCount([2, 4, 6]) == 2

    def test_five_ones(self):
        """[1, 1, 1, 1, 1] - all 31 subsequences have GCD=1."""
        sol = Solution()
        # Size 1: 5 * 15 = 75
        # Size 2: 10 * 7 = 70
        # Size 3: 10 * 3 = 30
        # Size 4: 5 * 1 = 5
        # Size 5: 1 * 0 = 0
        # Total = 180
        assert sol.subsequencePairCount([1, 1, 1, 1, 1]) == 180

    def test_boundary_min_length(self):
        """Minimum constraint: length 1."""
        sol = Solution()
        assert sol.subsequencePairCount([1]) == 0

    def test_boundary_single_value(self):
        """Single value array."""
        sol = Solution()
        assert sol.subsequencePairCount([100]) == 0

    def test_common_factor_elements(self):
        """[3, 6, 9] - all divisible by 3."""
        sol = Solution()
        # [3]: GCD=3, disjoint with GCD=3: [6,9] = 1
        # [6]: GCD=6, disjoint with GCD=6: none = 0
        # [9]: GCD=9, disjoint with GCD=9: none = 0
        # [3,6]: GCD=3, disjoint with GCD=3: none = 0
        # [3,9]: GCD=3, disjoint with GCD=3: none = 0
        # [6,9]: GCD=3, disjoint with GCD=3: [3] = 1
        # [3,6,9]: GCD=3, disjoint with GCD=3: none = 0
        # Total = 2
        assert sol.subsequencePairCount([3, 6, 9]) == 2

    def test_two_different_elements(self):
        """Two different elements - no disjoint pairs with same GCD."""
        sol = Solution()
        assert sol.subsequencePairCount([1, 2]) == 0
