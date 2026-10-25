import pytest
from solution import Solution


class TestCountGoodArrays:
    """Tests for countGoodArrays function."""
    
    def test_basic_case_n3_m2_k1(self):
        """n=3, m=2, k=1: 4 arrays [1,1,2], [1,2,2], [2,1,1], [2,2,1]"""
        sol = Solution()
        assert sol.countGoodArrays(3, 2, 1) == 4
    
    def test_all_equal_k_n_minus_1(self):
        """n=3, m=2, k=2: 2 arrays [1,1,1], [2,2,2]"""
        sol = Solution()
        assert sol.countGoodArrays(3, 2, 2) == 2
    
    def test_no_equal_k_0(self):
        """n=3, m=2, k=0: 2 arrays [1,2,1], [2,1,2]"""
        sol = Solution()
        assert sol.countGoodArrays(3, 2, 0) == 2
    
    def test_n4_m3_k2(self):
        """n=4, m=3, k=2: C(3,2)*3*2^1 = 3*3*2 = 18"""
        sol = Solution()
        assert sol.countGoodArrays(4, 3, 2) == 18
    
    def test_n4_m3_k1(self):
        """n=4, m=3, k=1: C(3,1)*3*2^2 = 3*3*4 = 36"""
        sol = Solution()
        assert sol.countGoodArrays(4, 3, 1) == 36
    
    def test_n4_m3_k3(self):
        """n=4, m=3, k=3: C(3,3)*3*2^0 = 1*3*1 = 3"""
        sol = Solution()
        assert sol.countGoodArrays(4, 3, 3) == 3
    
    def test_n4_m3_k0(self):
        """n=4, m=3, k=0: C(3,0)*3*2^3 = 1*3*8 = 24"""
        sol = Solution()
        assert sol.countGoodArrays(4, 3, 0) == 24
    
    def test_single_element_n1_m5_k0(self):
        """n=1, m=5, k=0: C(0,0)*5*4^0 = 1*5*1 = 5"""
        sol = Solution()
        assert sol.countGoodArrays(1, 5, 0) == 5
    
    def test_single_element_k1_impossible(self):
        """n=1, m=5, k=1: C(0,1) = 0, impossible"""
        sol = Solution()
        assert sol.countGoodArrays(1, 5, 1) == 0
    
    def test_m1_all_equal(self):
        """n=5, m=1, k=4: Only [1,1,1,1,1], answer = 1"""
        sol = Solution()
        assert sol.countGoodArrays(5, 1, 4) == 1
    
    def test_m1_not_all_equal_impossible(self):
        """n=5, m=1, k=3: Impossible with m=1, answer = 0"""
        sol = Solution()
        assert sol.countGoodArrays(5, 1, 3) == 0
    
    def test_n2_m10_k0(self):
        """n=2, m=10, k=0: C(1,0)*10*9^1 = 1*10*9 = 90"""
        sol = Solution()
        assert sol.countGoodArrays(2, 10, 0) == 90
    
    def test_n2_m10_k1(self):
        """n=2, m=10, k=1: C(1,1)*10*9^0 = 1*10*1 = 10"""
        sol = Solution()
        assert sol.countGoodArrays(2, 10, 1) == 10
    
    def test_n10_m10_k5(self):
        """n=10, m=10, k=5: C(9,5)*10*9^4 = 126*10*6561 = 8266860"""
        sol = Solution()
        assert sol.countGoodArrays(10, 10, 5) == 8266860
    
    def test_n100_m100_k50_large_values(self):
        """n=100, m=100, k=50: Large values with modulo"""
        sol = Solution()
        result = sol.countGoodArrays(100, 100, 50)
        assert 0 <= result < 10**9 + 7
    
    def test_n100000_m100000_k50000_boundary(self):
        """Boundary test with large n, m, k"""
        sol = Solution()
        result = sol.countGoodArrays(100000, 100000, 50000)
        assert 0 <= result < 10**9 + 7
    
    def test_minimal_n_m_k(self):
        """Minimal values: n=1, m=1, k=0"""
        sol = Solution()
        assert sol.countGoodArrays(1, 1, 0) == 1
    
    def test_n3_m100_k2(self):
        """n=3, m=100, k=2: C(2,2)*100*99^0 = 1*100*1 = 100"""
        sol = Solution()
        assert sol.countGoodArrays(3, 100, 2) == 100
    
    def test_n3_m100_k1(self):
        """n=3, m=100, k=1: C(2,1)*100*99^1 = 2*100*99 = 19800"""
        sol = Solution()
        assert sol.countGoodArrays(3, 100, 1) == 19800
    
    def test_n3_m100_k0(self):
        """n=3, m=100, k=0: C(2,0)*100*99^2 = 1*100*9801 = 980100"""
        sol = Solution()
        assert sol.countGoodArrays(3, 100, 0) == 980100
