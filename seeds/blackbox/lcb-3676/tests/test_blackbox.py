import pytest
from solution import Solution


class TestSmallestNumber:
    """Tests for smallestNumber function."""
    
    def test_boundary_min(self):
        """Test minimum input value n=1."""
        sol = Solution()
        result = sol.smallestNumber(1)
        assert result == 1
    
    def test_boundary_2(self):
        """Test n=2, should return 3 (binary 11)."""
        sol = Solution()
        result = sol.smallestNumber(2)
        assert result == 3
    
    def test_boundary_3(self):
        """Test n=3, should return 3 (binary 11)."""
        sol = Solution()
        result = sol.smallestNumber(3)
        assert result == 3
    
    def test_boundary_7(self):
        """Test n=7, should return 7 (binary 111)."""
        sol = Solution()
        result = sol.smallestNumber(7)
        assert result == 7
    
    def test_boundary_8(self):
        """Test n=8, should return 15 (binary 1111)."""
        sol = Solution()
        result = sol.smallestNumber(8)
        assert result == 15
    
    def test_boundary_9(self):
        """Test n=9, should return 15 (binary 1111)."""
        sol = Solution()
        result = sol.smallestNumber(9)
        assert result == 15
    
    def test_boundary_15(self):
        """Test n=15, should return 15 (binary 1111)."""
        sol = Solution()
        result = sol.smallestNumber(15)
        assert result == 15
    
    def test_boundary_16(self):
        """Test n=16, should return 31 (binary 11111)."""
        sol = Solution()
        result = sol.smallestNumber(16)
        assert result == 31
    
    def test_boundary_31(self):
        """Test n=31, should return 31 (binary 11111)."""
        sol = Solution()
        result = sol.smallestNumber(31)
        assert result == 31
    
    def test_boundary_32(self):
        """Test n=32, should return 63 (binary 111111)."""
        sol = Solution()
        result = sol.smallestNumber(32)
        assert result == 63
    
    def test_boundary_63(self):
        """Test n=63, should return 63 (binary 111111)."""
        sol = Solution()
        result = sol.smallestNumber(63)
        assert result == 63
    
    def test_boundary_64(self):
        """Test n=64, should return 127 (binary 1111111)."""
        sol = Solution()
        result = sol.smallestNumber(64)
        assert result == 127
    
    def test_boundary_127(self):
        """Test n=127, should return 127 (binary 1111111)."""
        sol = Solution()
        result = sol.smallestNumber(127)
        assert result == 127
    
    def test_boundary_128(self):
        """Test n=128, should return 255 (binary 11111111)."""
        sol = Solution()
        result = sol.smallestNumber(128)
        assert result == 255
    
    def test_boundary_255(self):
        """Test n=255, should return 255 (binary 11111111)."""
        sol = Solution()
        result = sol.smallestNumber(255)
        assert result == 255
    
    def test_boundary_256(self):
        """Test n=256, should return 511 (binary 111111111)."""
        sol = Solution()
        result = sol.smallestNumber(256)
        assert result == 511
    
    def test_boundary_511(self):
        """Test n=511, should return 511 (binary 111111111)."""
        sol = Solution()
        result = sol.smallestNumber(511)
        assert result == 511
    
    def test_boundary_512(self):
        """Test n=512, should return 1023 (binary 1111111111)."""
        sol = Solution()
        result = sol.smallestNumber(512)
        assert result == 1023
    
    def test_boundary_1000(self):
        """Test maximum input value n=1000, should return 1023."""
        sol = Solution()
        result = sol.smallestNumber(1000)
        assert result == 1023
    
    def test_mid_range_10(self):
        """Test mid-range input n=10."""
        sol = Solution()
        result = sol.smallestNumber(10)
        assert result == 15
    
    def test_mid_range_50(self):
        """Test mid-range input n=50."""
        sol = Solution()
        result = sol.smallestNumber(50)
        assert result == 63
    
    def test_mid_range_100(self):
        """Test mid-range input n=100."""
        sol = Solution()
        result = sol.smallestNumber(100)
        assert result == 127
    
    def test_mid_range_200(self):
        """Test mid-range input n=200."""
        sol = Solution()
        result = sol.smallestNumber(200)
        assert result == 255
    
    def test_mid_range_500(self):
        """Test mid-range input n=500."""
        sol = Solution()
        result = sol.smallestNumber(500)
        assert result == 511
    
    def test_mid_range_999(self):
        """Test near-max input n=999."""
        sol = Solution()
        result = sol.smallestNumber(999)
        assert result == 1023
