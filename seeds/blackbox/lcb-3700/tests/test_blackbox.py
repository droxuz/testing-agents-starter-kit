from typing import List
from solution import Solution


class TestSubsequencesWithMiddleMode:
    """Tests for subsequencesWithMiddleMode function."""
    
    def test_basic_example_with_three_of_middle_element(self):
        """Test case where middle element appears 3 times with 2 other elements."""
        solution = Solution()
        # nums = [1, 1, 1, 2, 3]
        # freq[1]=3, freq[2]=1, freq[3]=1, n=5
        # For x=1: 3 * C(2,2) * C(2,2) = 3 * 1 * 1 = 3
        # For x=2,3: 0 (not enough freq or remaining)
        # Expected: 3
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 2, 3])
        assert result == 3
    
    def test_all_same_elements(self):
        """Test case where all elements are the same."""
        solution = Solution()
        # nums = [1, 1, 1, 1, 1]
        # freq[1]=5, n=5
        # For x=1: 5 * C(4,2) * C(0,2) = 5 * 6 * 0 = 0
        # Expected: 0
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 1, 1])
        assert result == 0
    
    def test_all_different_elements(self):
        """Test case where all elements are different."""
        solution = Solution()
        # nums = [1, 2, 3, 4, 5]
        # All freq=1, n=5
        # For all x: 0 (freq < 3)
        # Expected: 0
        result = solution.subsequencesWithMiddleMode([1, 2, 3, 4, 5])
        assert result == 0
    
    def test_two_different_frequencies(self):
        """Test case with two elements having frequency >= 3."""
        solution = Solution()
        # nums = [1, 1, 1, 2, 2, 2]
        # freq[1]=3, freq[2]=3, n=6
        # For x=1: 3 * C(2,2) * C(3,2) = 3 * 1 * 3 = 9
        # For x=2: 3 * C(2,2) * C(3,2) = 3 * 1 * 3 = 9
        # Expected: 18
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 2, 2, 2])
        assert result == 18
    
    def test_three_of_one_two_of_another(self):
        """Test case with freq[1]=3, freq[2]=2."""
        solution = Solution()
        # nums = [1, 1, 1, 2, 2]
        # freq[1]=3, freq[2]=2, n=5
        # For x=1: 3 * C(2,2) * C(2,2) = 3 * 1 * 1 = 3
        # For x=2: 2 * C(1,2) * C(3,2) = 2 * 0 * 3 = 0
        # Expected: 3
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 2, 2])
        assert result == 3
    
    def test_four_of_one_two_of_another(self):
        """Test case with freq[1]=4, freq[2]=2."""
        solution = Solution()
        # nums = [1, 1, 1, 1, 2, 2]
        # freq[1]=4, freq[2]=2, n=6
        # For x=1: 4 * C(3,2) * C(2,2) = 4 * 3 * 1 = 12
        # For x=2: 2 * C(1,2) * C(4,2) = 2 * 0 * 6 = 0
        # Expected: 12
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 1, 2, 2])
        assert result == 12
    
    def test_five_of_one_two_of_another(self):
        """Test case with freq[1]=5, freq[2]=2."""
        solution = Solution()
        # nums = [1, 1, 1, 1, 1, 2, 2]
        # freq[1]=5, freq[2]=2, n=7
        # For x=1: 5 * C(4,2) * C(2,2) = 5 * 6 * 1 = 30
        # For x=2: 2 * C(1,2) * C(5,2) = 2 * 0 * 10 = 0
        # Expected: 30
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 1, 1, 2, 2])
        assert result == 30
    
    def test_negative_numbers(self):
        """Test case with negative numbers."""
        solution = Solution()
        # nums = [-1, -1, -1, 0, 1]
        # freq[-1]=3, freq[0]=1, freq[1]=1, n=5
        # For x=-1: 3 * C(2,2) * C(2,2) = 3 * 1 * 1 = 3
        # Expected: 3
        result = solution.subsequencesWithMiddleMode([-1, -1, -1, 0, 1])
        assert result == 3
    
    def test_large_array_with_multiple_frequencies(self):
        """Test case with larger array and multiple frequencies."""
        solution = Solution()
        # nums = [1, 1, 1, 1, 2, 2, 2, 3, 4]
        # freq[1]=4, freq[2]=3, freq[3]=1, freq[4]=1, n=9
        # For x=1: 4 * C(3,2) * C(5,2) = 4 * 3 * 10 = 120
        # For x=2: 3 * C(2,2) * C(6,2) = 3 * 1 * 15 = 45
        # For x=3,4: 0
        # Expected: 165
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 1, 2, 2, 2, 3, 4])
        assert result == 165
    
    def test_boundary_minimum_length(self):
        """Test case with minimum array length (5)."""
        solution = Solution()
        # nums = [1, 1, 1, 2, 3]
        # Expected: 3 (same as test_basic_example_with_three_of_middle_element)
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 2, 3])
        assert result == 3
    
    def test_boundary_with_four_of_middle(self):
        """Test case where middle element appears 4 times."""
        solution = Solution()
        # nums = [1, 1, 1, 1, 2, 3, 4]
        # freq[1]=4, freq[2]=1, freq[3]=1, freq[4]=1, n=7
        # For x=1: 4 * C(3,2) * C(3,2) = 4 * 3 * 3 = 36
        # Expected: 36
        result = solution.subsequencesWithMiddleMode([1, 1, 1, 1, 2, 3, 4])
        assert result == 36
    
    def test_modulo_result(self):
        """Test case that might produce large result requiring modulo."""
        solution = Solution()
        # Create array with many 1's and some other elements
        # nums = [1] * 100 + [2, 3, 4, 5]
        # freq[1]=100, freq[2]=1, freq[3]=1, freq[4]=1, freq[5]=1, n=104
        # For x=1: 100 * C(99,2) * C(4,2) = 100 * 4851 * 6 = 2,910,600
        # Expected: 2910600
        result = solution.subsequencesWithMiddleMode([1] * 100 + [2, 3, 4, 5])
        assert result == 2910600
