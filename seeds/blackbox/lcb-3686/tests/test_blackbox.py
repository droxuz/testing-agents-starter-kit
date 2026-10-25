from solution import Solution


class TestBeautifulSplits:
    def test_min_length_all_same(self):
        """Minimum length array [1,1,1] - only one split, should be beautiful."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 1])
        assert result == 1

    def test_min_length_different(self):
        """Minimum length array [1,2,3] - only one split, not beautiful."""
        sol = Solution()
        result = sol.beautifulSplits([1, 2, 3])
        assert result == 0

    def test_min_length_first_match(self):
        """[1,1,2] - nums1 prefix of nums2."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 2])
        assert result == 1

    def test_min_length_second_match(self):
        """[1,2,2] - nums2 prefix of nums3."""
        sol = Solution()
        result = sol.beautifulSplits([1, 2, 2])
        assert result == 1

    def test_all_same_four(self):
        """[1,1,1,1] - all splits should be beautiful."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 1, 1])
        assert result == 3

    def test_alternating_pattern(self):
        """[1,2,1,2,1] - pattern from specification analysis."""
        sol = Solution()
        result = sol.beautifulSplits([1, 2, 1, 2, 1])
        assert result == 2

    def test_all_different(self):
        """[1,2,3,4,5] - no beautiful splits possible."""
        sol = Solution()
        result = sol.beautifulSplits([1, 2, 3, 4, 5])
        assert result == 0

    def test_two_elements_same(self):
        """[1,1] - not enough elements for 3 subarrays."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1])
        assert result == 0

    def test_three_elements_first_prefix(self):
        """[1,1,1] - first condition met."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 1])
        assert result == 1

    def test_three_elements_second_prefix(self):
        """[1,2,2] - second condition met."""
        sol = Solution()
        result = sol.beautifulSplits([1, 2, 2])
        assert result == 1

    def test_three_elements_neither_prefix(self):
        """[1,2,3] - neither condition met."""
        sol = Solution()
        result = sol.beautifulSplits([1, 2, 3])
        assert result == 0

    def test_four_elements_all_same(self):
        """[1,1,1,1] - all 3 splits beautiful."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 1, 1])
        assert result == 3

    def test_four_elements_two_same(self):
        """[1,1,1,2] - check various splits."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 1, 2])
        assert result == 2

    def test_four_elements_first_two_same(self):
        """[1,1,2,2] - check various splits."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 2, 2])
        assert result == 3

    def test_five_elements_alternating(self):
        """[1,2,1,2,1] - expected 2 beautiful splits."""
        sol = Solution()
        result = sol.beautifulSplits([1, 2, 1, 2, 1])
        assert result == 2

    def test_five_elements_all_same(self):
        """[1,1,1,1,1] - all splits should be beautiful."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 1, 1, 1])
        assert result == 6

    def test_zero_values(self):
        """Array with zeros - [0,0,0]."""
        sol = Solution()
        result = sol.beautifulSplits([0, 0, 0])
        assert result == 1

    def test_zero_and_nonzero(self):
        """[0,1,0] - no beautiful splits."""
        sol = Solution()
        result = sol.beautifulSplits([0, 1, 0])
        assert result == 0

    def test_prefix_both_conditions(self):
        """[1,1,1] - both conditions met, still counts as 1."""
        sol = Solution()
        result = sol.beautifulSplits([1, 1, 1])
        assert result == 1
