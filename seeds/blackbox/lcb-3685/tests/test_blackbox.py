from solution import Solution


class TestCountSubarrays:
    """Tests for countSubarrays function."""

    def test_basic_valid(self):
        """Single valid subarray [1, 4, 1]: 1+1=2, 4/2=2."""
        sol = Solution()
        assert sol.countSubarrays([1, 4, 1]) == 1

    def test_basic_invalid(self):
        """Single invalid subarray [1, 2, 1]: 1+1=2, 2/2=1."""
        sol = Solution()
        assert sol.countSubarrays([1, 2, 1]) == 0

    def test_multiple_valid(self):
        """Two valid subarrays in [1, 4, 1, 2, 4, 2]."""
        sol = Solution()
        assert sol.countSubarrays([1, 4, 1, 2, 4, 2]) == 2

    def test_all_zeros(self):
        """All zeros: [0, 0, 0] is valid (0+0=0, 0/2=0)."""
        sol = Solution()
        assert sol.countSubarrays([0, 0, 0]) == 1

    def test_all_zeros_multiple(self):
        """Multiple consecutive zeros."""
        sol = Solution()
        assert sol.countSubarrays([0, 0, 0, 0, 0]) == 2

    def test_negative_numbers_invalid(self):
        """Negative numbers: [-1, -2, -1] is invalid."""
        sol = Solution()
        assert sol.countSubarrays([-1, -2, -1]) == 0

    def test_negative_valid(self):
        """Valid with negatives: [-1, -4, -1] -> -1+(-1)=-2, -4/2=-2."""
        sol = Solution()
        assert sol.countSubarrays([-1, -4, -1]) == 1

    def test_minimum_length(self):
        """Minimum array length of 3 with valid subarray."""
        sol = Solution()
        assert sol.countSubarrays([1, 4, 1]) == 1

    def test_boundary_values(self):
        """Boundary values at limits."""
        sol = Solution()
        # [-100, 200, -100]: -100+(-100)=-200, 200/2=100, invalid
        assert sol.countSubarrays([-100, 200, -100]) == 0
        # [-100, -200, -100]: -100+(-100)=-200, -200/2=-100, invalid
        assert sol.countSubarrays([-100, -200, -100]) == 0

    def test_large_valid(self):
        """Valid with larger numbers."""
        sol = Solution()
        assert sol.countSubarrays([5, 20, 5]) == 1

    def test_no_valid_subarrays(self):
        """Array with no valid subarrays."""
        sol = Solution()
        assert sol.countSubarrays([1, 2, 3, 4, 5]) == 0

    def test_overlapping_valid(self):
        """Overlapping valid subarrays."""
        sol = Solution()
        # [1, 4, 1, 4, 1]: [1,4,1] valid, [4,1,4] invalid, [1,4,1] valid
        assert sol.countSubarrays([1, 4, 1, 4, 1]) == 2

    def test_mixed_positive_negative(self):
        """Mixed positive and negative with valid subarrays."""
        sol = Solution()
        # [1, 4, 1, -1, -4, -1]: [1,4,1] valid, [-1,-4,-1] valid
        assert sol.countSubarrays([1, 4, 1, -1, -4, -1]) == 2

    def test_all_same_numbers(self):
        """All same numbers: [2, 2, 2] -> 2+2=4, 2/2=1, invalid."""
        sol = Solution()
        assert sol.countSubarrays([2, 2, 2]) == 0

    def test_many_valid(self):
        """Many valid subarrays in longer array."""
        sol = Solution()
        # [1, 4, 1, 1, 4, 1, 1, 4, 1]: 3 valid subarrays
        assert sol.countSubarrays([1, 4, 1, 1, 4, 1, 1, 4, 1]) == 3

    def test_odd_second_number(self):
        """Odd second number: [1, 3, 1] -> 1+1=2, 3/2=1.5, invalid."""
        sol = Solution()
        assert sol.countSubarrays([1, 3, 1]) == 0

    def test_negative_odd_second(self):
        """Negative odd second number: [1, -3, 1] -> 1+1=2, -3/2=-1.5, invalid."""
        sol = Solution()
        assert sol.countSubarrays([1, -3, 1]) == 0
