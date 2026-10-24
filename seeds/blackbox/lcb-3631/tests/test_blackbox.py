import pytest
from solution import Solution


class TestCountKReducibleNumbers:
    """Tests for countKReducibleNumbers function."""
    
    def test_k1_n8(self):
        """k=1, n=8 (binary "1000"). Only powers of 2: 1, 2, 4."""
        sol = Solution()
        result = sol.countKReducibleNumbers("1000", 1)
        assert result == 3  # 1, 2, 4
    
    def test_k2_n8(self):
        """k=2, n=8. Numbers with 1 or 2 set bits: 1,2,3,4,5,6."""
        sol = Solution()
        result = sol.countKReducibleNumbers("1000", 2)
        assert result == 6  # 1, 2, 3, 4, 5, 6
    
    def test_k3_n8(self):
        """k=3, n=8. All numbers 1-7 have at most 3 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("1000", 3)
        assert result == 7  # 1, 2, 3, 4, 5, 6, 7
    
    def test_k1_n7(self):
        """k=1, n=7 (binary "111"). Powers of 2: 1, 2, 4."""
        sol = Solution()
        result = sol.countKReducibleNumbers("111", 1)
        assert result == 3
    
    def test_k2_n7(self):
        """k=2, n=7. Numbers 1-6 with at most 2 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("111", 2)
        assert result == 6
    
    def test_k1_n4(self):
        """k=1, n=4 (binary "100"). Powers of 2: 1, 2."""
        sol = Solution()
        result = sol.countKReducibleNumbers("100", 1)
        assert result == 2
    
    def test_k1_n2(self):
        """k=1, n=2 (binary "10"). Only 1."""
        sol = Solution()
        result = sol.countKReducibleNumbers("10", 1)
        assert result == 1
    
    def test_k1_n1(self):
        """k=1, n=1 (binary "1"). No positive integers less than 1."""
        sol = Solution()
        result = sol.countKReducibleNumbers("1", 1)
        assert result == 0
    
    def test_k5_n8(self):
        """k=5, n=8. Same as k=3 since max bits is 3."""
        sol = Solution()
        result = sol.countKReducibleNumbers("1000", 5)
        assert result == 7
    
    def test_k3_n16(self):
        """k=3, n=16 (binary "10000"). Numbers 1-15 with at most 3 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("10000", 3)
        # Numbers with 1 bit: 1, 2, 4, 8 (4)
        # Numbers with 2 bits: 3, 5, 6, 9, 10, 12 (6)
        # Numbers with 3 bits: 7, 11, 13, 14 (4)
        assert result == 14
    
    def test_k2_n16(self):
        """k=2, n=16. Numbers 1-15 with at most 2 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("10000", 2)
        # Numbers with 1 bit: 1, 2, 4, 8 (4)
        # Numbers with 2 bits: 3, 5, 6, 9, 10, 12 (6)
        assert result == 10
    
    def test_k4_n16(self):
        """k=4, n=16. Numbers 1-15 with at most 4 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("10000", 4)
        # All numbers 1-15 have at most 4 bits (15 has 4 bits)
        assert result == 15
    
    def test_k1_n32(self):
        """k=1, n=32. Powers of 2: 1, 2, 4, 8, 16."""
        sol = Solution()
        result = sol.countKReducibleNumbers("100000", 1)
        assert result == 5
    
    def test_k5_n32(self):
        """k=5, n=32. All numbers 1-31 with at most 5 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("100000", 5)
        assert result == 31
    
    def test_large_n_k1(self):
        """Large n with k=1. Count powers of 2 less than n."""
        sol = Solution()
        # n = 2^10 = 1024, powers of 2 less than 1024: 1, 2, 4, ..., 512 (10 numbers)
        result = sol.countKReducibleNumbers("1" + "0" * 10, 1)
        assert result == 10
    
    def test_large_n_k5(self):
        """Large n with k=5. All numbers 1 to n-1."""
        sol = Solution()
        # n = 2^10 = 1024, all numbers 1-1023
        result = sol.countKReducibleNumbers("1" + "0" * 10, 5)
        assert result == 1023
    
    def test_k3_n15(self):
        """k=3, n=15 (binary "1111"). Numbers 1-14 with at most 3 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("1111", 3)
        # 14 has 3 bits, so all numbers 1-14 qualify
        assert result == 14
    
    def test_k2_n15(self):
        """k=2, n=15. Numbers 1-14 with at most 2 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("1111", 2)
        # Numbers with 1 bit: 1, 2, 4, 8 (4)
        # Numbers with 2 bits: 3, 5, 6, 9, 10, 12 (6)
        assert result == 10

    def test_k1_n3(self):
        """k=1, n=3 (binary "11"). Powers of 2: 1, 2."""
        sol = Solution()
        result = sol.countKReducibleNumbers("11", 1)
        assert result == 2
    
    def test_k2_n3(self):
        """k=2, n=3. Numbers 1-2 with at most 2 bits."""
        sol = Solution()
        result = sol.countKReducibleNumbers("11", 2)
        assert result == 2
    
    def test_k1_n5(self):
        """k=1, n=5 (binary "101"). Powers of 2: 1, 2, 4."""
        sol = Solution()
        result = sol.countKReducibleNumbers("101", 1)
        assert result == 3
    
    def test_k3_n5(self):
        """k=3, n=5. Numbers 1-4 with at most 3 bits (all qualify)."""
        sol = Solution()
        result = sol.countKReducibleNumbers("101", 3)
        assert result == 4
