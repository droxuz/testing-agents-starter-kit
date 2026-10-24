from typing import List
from solution import Solution


class TestMinBitwiseArray:
    """Tests for minBitwiseArray function."""

    def test_single_prime_3(self):
        """Test with prime 3, which is 2^2-1."""
        sol = Solution()
        result = sol.minBitwiseArray([3])
        assert result == [2], f"Expected [2], got {result}"

    def test_single_prime_31(self):
        """Test with prime 31, which is 2^5-1."""
        sol = Solution()
        result = sol.minBitwiseArray([31])
        assert result == [30], f"Expected [30], got {result}"

    def test_single_prime_2(self):
        """Test with prime 2, which is the only even prime."""
        sol = Solution()
        result = sol.minBitwiseArray([2])
        assert result == [-1], f"Expected [-1], got {result}"

    def test_single_prime_5(self):
        """Test with prime 5."""
        sol = Solution()
        result = sol.minBitwiseArray([5])
        assert result == [4], f"Expected [4], got {result}"

    def test_single_prime_7(self):
        """Test with prime 7."""
        sol = Solution()
        result = sol.minBitwiseArray([7])
        assert result == [6], f"Expected [6], got {result}"

    def test_single_prime_11(self):
        """Test with prime 11."""
        sol = Solution()
        result = sol.minBitwiseArray([11])
        assert result == [10], f"Expected [10], got {result}"

    def test_single_prime_13(self):
        """Test with prime 13."""
        sol = Solution()
        result = sol.minBitwiseArray([13])
        assert result == [12], f"Expected [12], got {result}"

    def test_single_prime_17(self):
        """Test with prime 17."""
        sol = Solution()
        result = sol.minBitwiseArray([17])
        assert result == [16], f"Expected [16], got {result}"

    def test_single_prime_19(self):
        """Test with prime 19."""
        sol = Solution()
        result = sol.minBitwiseArray([19])
        assert result == [18], f"Expected [18], got {result}"

    def test_single_prime_23(self):
        """Test with prime 23."""
        sol = Solution()
        result = sol.minBitwiseArray([23])
        assert result == [22], f"Expected [22], got {result}"

    def test_single_prime_29(self):
        """Test with prime 29."""
        sol = Solution()
        result = sol.minBitwiseArray([29])
        assert result == [28], f"Expected [28], got {result}"

    def test_single_prime_47(self):
        """Test with prime 47."""
        sol = Solution()
        result = sol.minBitwiseArray([47])
        assert result == [46], f"Expected [46], got {result}"

    def test_single_prime_79(self):
        """Test with prime 79."""
        sol = Solution()
        result = sol.minBitwiseArray([79])
        assert result == [78], f"Expected [78], got {result}"

    def test_single_prime_97(self):
        """Test with prime 97."""
        sol = Solution()
        result = sol.minBitwiseArray([97])
        assert result == [96], f"Expected [96], got {result}"

    def test_multiple_elements_mixed(self):
        """Test with multiple primes."""
        sol = Solution()
        result = sol.minBitwiseArray([3, 5, 7, 11, 31])
        assert result == [2, 4, 6, 10, 30], f"Expected [2, 4, 6, 10, 30], got {result}"

    def test_all_valid_primes(self):
        """Test with all valid primes."""
        sol = Solution()
        result = sol.minBitwiseArray([3, 7, 31])
        assert result == [2, 6, 30], f"Expected [2, 6, 30], got {result}"

    def test_all_invalid_primes(self):
        """Test with only prime 2."""
        sol = Solution()
        result = sol.minBitwiseArray([2, 2, 2])
        assert result == [-1, -1, -1], f"Expected [-1, -1, -1], got {result}"

    def test_boundary_minimum_prime(self):
        """Test with minimum prime value 2."""
        sol = Solution()
        result = sol.minBitwiseArray([2])
        assert result == [-1], f"Expected [-1], got {result}"

    def test_boundary_maximum_prime(self):
        """Test with maximum prime value 997."""
        sol = Solution()
        result = sol.minBitwiseArray([997])
        assert result == [996], f"Expected [996], got {result}"

    def test_empty_array(self):
        """Test with empty array."""
        sol = Solution()
        result = sol.minBitwiseArray([])
        assert result == [], f"Expected [], got {result}"
