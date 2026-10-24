import pytest
from solution import Solution


class TestMinOperations:
    """Tests for minOperations function"""
    
    def test_equal_numbers_zero_cost(self):
        """When n equals m, no operations needed, cost is 0"""
        sol = Solution()
        assert sol.minOperations(4, 4) == 0
        assert sol.minOperations(10, 10) == 0
        assert sol.minOperations(100, 100) == 0
        assert sol.minOperations(9999, 9999) == 0
    
    def test_prime_target_impossible(self):
        """Cannot reach prime numbers, return -1"""
        sol = Solution()
        # Single digit primes
        assert sol.minOperations(1, 2) == -1
        assert sol.minOperations(1, 3) == -1
        assert sol.minOperations(1, 5) == -1
        assert sol.minOperations(1, 7) == -1
        # Multi-digit primes
        assert sol.minOperations(10, 11) == -1
        assert sol.minOperations(12, 13) == -1
        assert sol.minOperations(100, 101) == -1
        assert sol.minOperations(100, 103) == -1
        assert sol.minOperations(100, 107) == -1
    
    def test_single_digit_connected_components(self):
        """Single digit numbers form connected components based on non-prime paths"""
        sol = Solution()
        # 8 and 9 are connected (both not prime)
        assert sol.minOperations(8, 9) == 17
        assert sol.minOperations(9, 8) == 17
        # 1, 4, 6 are isolated from each other (blocked by primes)
        assert sol.minOperations(1, 4) == -1
        assert sol.minOperations(4, 1) == -1
        assert sol.minOperations(1, 6) == -1
        assert sol.minOperations(6, 1) == -1
        assert sol.minOperations(4, 6) == -1
        assert sol.minOperations(6, 4) == -1
    
    def test_multi_digit_direct_composite(self):
        """Direct path between composite multi-digit numbers"""
        sol = Solution()
        # 10 -> 12 (both composite)
        assert sol.minOperations(10, 12) == 22
        # 12 -> 10 (both composite)
        assert sol.minOperations(12, 10) == 22
        # 100 -> 102 (both composite)
        assert sol.minOperations(100, 102) == 202
        # 102 -> 100 (both composite)
        assert sol.minOperations(102, 100) == 202
        # 100 -> 104 (both composite)
        assert sol.minOperations(100, 104) == 204
        # 104 -> 100 (both composite)
        assert sol.minOperations(104, 100) == 204
    
    def test_multi_digit_path_through_composite(self):
        """Path through intermediate composite multi-digit numbers"""
        sol = Solution()
        # 10 -> 14: 10 -> 12 -> 14 (both 10, 12, 14 are composite)
        assert sol.minOperations(10, 14) == 36
        # 14 -> 10: 14 -> 12 -> 10
        assert sol.minOperations(14, 10) == 36
        # 100 -> 106: 100 -> 102 -> 104 -> 106 (all composite)
        assert sol.minOperations(100, 106) == 412
        # 106 -> 100: 106 -> 104 -> 102 -> 100
        assert sol.minOperations(106, 100) == 412
    
    def test_one_to_multi_digit(self):
        """From 1 to multi-digit composite numbers"""
        sol = Solution()
        # 1 -> 10 (direct, both not prime)
        assert sol.minOperations(1, 10) == 11
        # 10 -> 1 (direct)
        assert sol.minOperations(10, 1) == 11
        # 1 -> 100 (direct, both not prime)
        assert sol.minOperations(1, 100) == 101
        # 100 -> 1 (direct)
        assert sol.minOperations(100, 1) == 101
    
    def test_boundary_values(self):
        """Test boundary values from constraints"""
        sol = Solution()
        # Minimum values
        assert sol.minOperations(1, 1) == 0
        # Maximum values (9999 is not prime)
        assert sol.minOperations(9999, 9999) == 0
        assert sol.minOperations(9999, 9998) == 19997
        # 9998 -> 9999
        assert sol.minOperations(9998, 9999) == 19997
    
    def test_six_nine_connection(self):
        """6 and 9 are connected through multi-digit paths"""
        sol = Solution()
        # 6 -> 9: direct (both not prime)
        assert sol.minOperations(6, 9) == 15
        # 9 -> 6: direct
        assert sol.minOperations(9, 6) == 15
