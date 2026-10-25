from solution import Solution


class TestConstructTransformedArray:
    def test_simple_positive_movement_no_wrap(self):
        """Test positive movement without wrapping around array boundaries."""
        solution = Solution()
        nums = [1, 2, 3]
        # i=0: move 1 right from 0 -> index 1, result[0] = nums[1] = 2
        # i=1: move 2 right from 1 -> index (1+2)%3 = 0, result[1] = nums[0] = 1
        # i=2: move 3 right from 2 -> index (2+3)%3 = 2, result[2] = nums[2] = 3
        result = solution.constructTransformedArray(nums)
        assert result == [2, 1, 3]

    def test_positive_movement_with_wrap(self):
        """Test positive movement that wraps around to beginning."""
        solution = Solution()
        nums = [1, 2, 3]
        # i=0: move 1 right from 0 -> index 1, result[0] = nums[1] = 2
        # i=1: move 2 right from 1 -> index (1+2)%3 = 0, result[1] = nums[0] = 1
        # i=2: move 3 right from 2 -> index (2+3)%3 = 2, result[2] = nums[2] = 3
        result = solution.constructTransformedArray(nums)
        assert result == [2, 1, 3]

    def test_negative_movement_with_wrap(self):
        """Test negative movement that wraps around to end."""
        solution = Solution()
        nums = [1, -1, 2]
        # i=0: move 1 right from 0 -> index 1, result[0] = nums[1] = -1
        # i=1: move 1 left from 1 -> index (1-1)%3 = 0, result[1] = nums[0] = 1
        # i=2: move 2 right from 2 -> index (2+2)%3 = 1, result[2] = nums[1] = -1
        result = solution.constructTransformedArray(nums)
        assert result == [-1, 1, -1]

    def test_zero_values(self):
        """Test that zero values result in 0 in the output."""
        solution = Solution()
        nums = [0, 1, 2]
        # i=0: nums[0]=0, result[0] = 0
        # i=1: move 1 right from 1 -> index 2, result[1] = nums[2] = 2
        # i=2: move 2 right from 2 -> index (2+2)%3 = 1, result[2] = nums[1] = 1
        result = solution.constructTransformedArray(nums)
        assert result == [0, 2, 1]

    def test_all_zeros(self):
        """Test array with all zero values."""
        solution = Solution()
        nums = [0, 0, 0]
        # All zeros stay at their positions
        result = solution.constructTransformedArray(nums)
        assert result == [0, 0, 0]

    def test_single_element_positive(self):
        """Test single element array with positive value."""
        solution = Solution()
        nums = [1]
        # i=0: move 1 right from 0 -> index (0+1)%1 = 0, result[0] = nums[0] = 1
        result = solution.constructTransformedArray(nums)
        assert result == [1]

    def test_single_element_negative(self):
        """Test single element array with negative value."""
        solution = Solution()
        nums = [-1]
        # i=0: move 1 left from 0 -> index (0-1)%1 = 0, result[0] = nums[0] = -1
        result = solution.constructTransformedArray(nums)
        assert result == [-1]

    def test_single_element_zero(self):
        """Test single element array with zero value."""
        solution = Solution()
        nums = [0]
        # i=0: nums[0]=0, result[0] = 0
        result = solution.constructTransformedArray(nums)
        assert result == [0]

    def test_mixed_positive_negative(self):
        """Test array with mixed positive and negative values."""
        solution = Solution()
        nums = [1, -2, 3, -1]
        # i=0: move 1 right from 0 -> index 1, result[0] = nums[1] = -2
        # i=1: move 2 left from 1 -> index (1-2)%4 = -1%4 = 3, result[1] = nums[3] = -1
        # i=2: move 3 right from 2 -> index (2+3)%4 = 1, result[2] = nums[1] = -2
        # i=3: move 1 left from 3 -> index (3-1)%4 = 2, result[3] = nums[2] = 3
        result = solution.constructTransformedArray(nums)
        assert result == [-2, -1, -2, 3]

    def test_wrap_multiple_times(self):
        """Test movement that wraps around multiple times."""
        solution = Solution()
        nums = [4, 1, 2, 3]
        # i=0: move 4 right from 0 -> index (0+4)%4 = 0, result[0] = nums[0] = 4
        # i=1: move 1 right from 1 -> index 2, result[1] = nums[2] = 2
        # i=2: move 2 right from 2 -> index (2+2)%4 = 0, result[2] = nums[0] = 4
        # i=3: move 3 right from 3 -> index (3+3)%4 = 2, result[3] = nums[2] = 2
        result = solution.constructTransformedArray(nums)
        assert result == [4, 2, 4, 2]

    def test_negative_left_wrap(self):
        """Test negative movement wrapping from beginning to end."""
        solution = Solution()
        nums = [1, 2, -3]
        # i=0: move 1 right from 0 -> index 1, result[0] = nums[1] = 2
        # i=1: move 2 right from 1 -> index (1+2)%3 = 0, result[1] = nums[0] = 1
        # i=2: move 3 left from 2 -> index (2-3)%3 = -1%3 = 2, result[2] = nums[2] = -3
        result = solution.constructTransformedArray(nums)
        assert result == [2, 1, -3]

    def test_left_wrap_across_boundary(self):
        """Test negative movement wrapping from index 0 to end."""
        solution = Solution()
        nums = [2, 3, 4]
        # i=0: move 2 right from 0 -> index 2, result[0] = nums[2] = 4
        # i=1: move 3 right from 1 -> index (1+3)%3 = 1, result[1] = nums[1] = 3
        # i=2: move 4 right from 2 -> index (2+4)%3 = 0, result[2] = nums[0] = 2
        result = solution.constructTransformedArray(nums)
        assert result == [4, 3, 2]

    def test_left_wrap_from_middle(self):
        """Test negative movement wrapping from middle to end."""
        solution = Solution()
        nums = [1, 2, 3, 4]
        # i=0: move 1 right from 0 -> index 1, result[0] = nums[1] = 2
        # i=1: move 2 right from 1 -> index (1+2)%4 = 3, result[1] = nums[3] = 4
        # i=2: move 3 right from 2 -> index (2+3)%4 = 1, result[2] = nums[1] = 2
        # i=3: move 4 right from 3 -> index (3+4)%4 = 3, result[3] = nums[3] = 4
        result = solution.constructTransformedArray(nums)
        assert result == [2, 4, 2, 4]

    def test_boundary_length_one(self):
        """Test with minimum array length of 1."""
        solution = Solution()
        nums = [5]
        # i=0: move 5 right from 0 -> index (0+5)%1 = 0, result[0] = nums[0] = 5
        result = solution.constructTransformedArray(nums)
        assert result == [5]

    def test_boundary_value_positive_100(self):
        """Test with maximum positive value of 100."""
        solution = Solution()
        nums = [100]
        # i=0: move 100 right from 0 -> index (0+100)%1 = 0, result[0] = nums[0] = 100
        result = solution.constructTransformedArray(nums)
        assert result == [100]

    def test_boundary_value_negative_100(self):
        """Test with minimum negative value of -100."""
        solution = Solution()
        nums = [-100]
        # i=0: move 100 left from 0 -> index (0-100)%1 = 0, result[0] = nums[0] = -100
        result = solution.constructTransformedArray(nums)
        assert result == [-100]

    def test_wrap_from_end_to_start(self):
        """Test movement wrapping from last element to first."""
        solution = Solution()
        nums = [1, 2, 100]
        # i=0: move 1 right from 0 -> index 1, result[0] = nums[1] = 2
        # i=1: move 2 right from 1 -> index (1+2)%3 = 0, result[1] = nums[0] = 1
        # i=2: move 100 right from 2 -> index (2+100)%3 = 2, result[2] = nums[2] = 100
        result = solution.constructTransformedArray(nums)
        assert result == [2, 1, 100]

    def test_wrap_from_start_to_end(self):
        """Test movement wrapping from first element to last."""
        solution = Solution()
        nums = [3, 1, 2]
        # i=0: move 3 right from 0 -> index (0+3)%3 = 0, result[0] = nums[0] = 3
        # i=1: move 1 right from 1 -> index 2, result[1] = nums[2] = 2
        # i=2: move 2 right from 2 -> index (2+2)%3 = 1, result[2] = nums[1] = 1
        result = solution.constructTransformedArray(nums)
        assert result == [3, 2, 1]
