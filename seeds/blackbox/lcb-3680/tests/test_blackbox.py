from solution import Solution
from typing import List


class TestCountComponents:
    """Tests for countComponents function."""
    
    def test_single_element(self):
        """Single element should return 1 component."""
        sol = Solution()
        result = sol.countComponents([1], 10)
        assert result == 1
    
    def test_all_disconnected_small_threshold(self):
        """When threshold is small, elements may be disconnected."""
        sol = Solution()
        # lcm(2,3)=6 > 1, so no connections
        result = sol.countComponents([2, 3], 1)
        assert result == 2
    
    def test_all_connected(self):
        """When all pairs have lcm <= threshold, all connected."""
        sol = Solution()
        # lcm(1,2)=2, lcm(1,3)=3, lcm(2,3)=6, all <= 6
        result = sol.countComponents([1, 2, 3], 6)
        assert result == 1
    
    def test_mixed_connections(self):
        """Some connected, some not."""
        sol = Solution()
        # lcm(2,4)=4<=5, lcm(2,6)=6>5, lcm(4,6)=12>5
        # 2 and 4 connected, 6 isolated = 2 components
        result = sol.countComponents([2, 4, 6], 5)
        assert result == 2
    
    def test_element_greater_than_threshold(self):
        """Elements > threshold cannot connect to anything."""
        sol = Solution()
        # lcm(1, 100)=100 > 50, so 100 is isolated
        result = sol.countComponents([1, 100], 50)
        assert result == 2
    
    def test_threshold_equals_lcm(self):
        """Boundary case where lcm equals threshold."""
        sol = Solution()
        # lcm(10, 100) = 100 <= 100
        result = sol.countComponents([10, 100], 100)
        assert result == 1
    
    def test_threshold_less_than_lcm(self):
        """Boundary case where lcm exceeds threshold."""
        sol = Solution()
        # lcm(10, 100) = 100 > 99
        result = sol.countComponents([10, 100], 99)
        assert result == 2
    
    def test_all_elements_one(self):
        """All elements are 1."""
        sol = Solution()
        # lcm(1,1)=1 <= any threshold >= 1
        result = sol.countComponents([1, 1, 1], 1)
        assert result == 1
    
    def test_three_elements_partial_connection(self):
        """Three elements with partial connections."""
        sol = Solution()
        # lcm(2,4)=4<=6, lcm(2,6)=6<=6, lcm(4,6)=12>6
        # 2-4 connected, 2-6 connected, so 2,4,6 all connected via 2
        result = sol.countComponents([2, 4, 6], 6)
        assert result == 1
    
    def test_larger_numbers(self):
        """Test with larger numbers."""
        sol = Solution()
        # lcm(5, 10) = 10 <= 15, lcm(5, 20) = 20 > 15, lcm(10, 20) = 20 > 15
        # 5-10 connected, 20 isolated = 2 components
        result = sol.countComponents([5, 10, 20], 15)
        assert result == 2
    
    def test_minimum_threshold(self):
        """Test with minimum threshold value."""
        sol = Solution()
        result = sol.countComponents([1, 2], 1)
        assert result == 2
    
    def test_maximum_threshold_boundary(self):
        """Test near maximum threshold."""
        sol = Solution()
        # lcm(1, 200000) = 200000 <= 200000
        result = sol.countComponents([1, 200000], 200000)
        assert result == 1
    
    def test_large_element_isolated(self):
        """Large element that cannot connect."""
        sol = Solution()
        # lcm(1, 1000000000) = 1000000000 > 100000
        result = sol.countComponents([1, 1000000000], 100000)
        assert result == 2
    
    def test_five_elements_chain(self):
        """Five elements forming a chain."""
        sol = Solution()
        # All pairs should have lcm <= 30
        # lcm(2,4)=4, lcm(2,6)=6, lcm(2,8)=8, lcm(2,10)=10, lcm(4,6)=12, lcm(4,8)=8, lcm(4,10)=20, lcm(6,8)=24, lcm(6,10)=30, lcm(8,10)=40>30
        # 8 and 10 not directly connected, but 8-2-10 connects them
        # All connected via node 2
        result = sol.countComponents([2, 4, 6, 8, 10], 30)
        assert result == 1
    
    def test_all_connected_large_threshold(self):
        """All elements connect when threshold is very large."""
        sol = Solution()
        # All pairs have lcm <= 200000
        result = sol.countComponents([2, 3, 5], 200000)
        assert result == 1
    
    def test_two_elements_connected(self):
        """Two elements that are connected."""
        sol = Solution()
        # lcm(2, 4) = 4 <= 5
        result = sol.countComponents([2, 4], 5)
        assert result == 1
    
    def test_two_elements_not_connected(self):
        """Two elements that are not connected."""
        sol = Solution()
        # lcm(2, 3) = 6 > 5
        result = sol.countComponents([2, 3], 5)
        assert result == 2
