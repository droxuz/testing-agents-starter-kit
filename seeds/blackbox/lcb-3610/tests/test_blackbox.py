from solution import Solution


class TestFindXSum:
    def test_basic_example_1(self):
        """Test with equal frequencies, x=1, should pick largest element"""
        sol = Solution()
        # nums = [1, 2, 3], k = 2, x = 1
        # Subarray [1, 2]: freq {1:1, 2:1}, top 1 is 2 (larger value), sum = 2
        # Subarray [2, 3]: freq {2:1, 3:1}, top 1 is 3 (larger value), sum = 3
        result = sol.findXSum([1, 2, 3], 2, 1)
        assert result == [2, 3]

    def test_basic_example_2(self):
        """Test with equal frequencies, x=2, should include all elements"""
        sol = Solution()
        # nums = [1, 2, 3], k = 2, x = 2
        # Subarray [1, 2]: freq {1:1, 2:1}, top 2 are both, sum = 3
        # Subarray [2, 3]: freq {2:1, 3:1}, top 2 are both, sum = 5
        result = sol.findXSum([1, 2, 3], 2, 2)
        assert result == [3, 5]

    def test_with_duplicates(self):
        """Test with duplicate elements"""
        sol = Solution()
        # nums = [1, 1, 2, 2], k = 2, x = 1
        # Subarray [1, 1]: freq {1:2}, top 1 is 1, sum = 2
        # Subarray [1, 2]: freq {1:1, 2:1}, top 1 is 2 (larger), sum = 2
        # Subarray [2, 2]: freq {2:2}, top 1 is 2, sum = 4
        result = sol.findXSum([1, 1, 2, 2], 2, 1)
        assert result == [2, 2, 4]

    def test_x_equals_k(self):
        """Test when x equals k, include all distinct elements"""
        sol = Solution()
        # nums = [1, 2, 3, 4], k = 4, x = 4
        # Only one subarray: [1, 2, 3, 4], all 4 distinct, sum = 10
        result = sol.findXSum([1, 2, 3, 4], 4, 4)
        assert result == [10]

    def test_x_equals_1(self):
        """Test when x equals 1, pick only the most frequent (largest value if tie)"""
        sol = Solution()
        # nums = [5, 1, 5, 1], k = 3, x = 1
        # Subarray [5, 1, 5]: freq {5:2, 1:1}, top 1 is 5, sum = 5
        # Subarray [1, 5, 1]: freq {1:2, 5:1}, top 1 is 1, sum = 1
        result = sol.findXSum([5, 1, 5, 1], 3, 1)
        assert result == [5, 1]

    def test_all_same_elements(self):
        """Test when all elements are the same"""
        sol = Solution()
        # nums = [7, 7, 7], k = 2, x = 1
        # Subarray [7, 7]: freq {7:2}, top 1 is 7, sum = 14
        # Subarray [7, 7]: freq {7:2}, top 1 is 7, sum = 14
        result = sol.findXSum([7, 7, 7], 2, 1)
        assert result == [14, 14]

    def test_less_than_x_distinct(self):
        """Test when there are fewer than x distinct elements"""
        sol = Solution()
        # nums = [1, 1, 1], k = 3, x = 5
        # Only one subarray: [1, 1, 1], only 1 distinct element (< 5), sum = 3
        result = sol.findXSum([1, 1, 1], 3, 5)
        assert result == [3]

    def test_frequency_tie_breaker(self):
        """Test that larger value wins when frequencies are equal"""
        sol = Solution()
        # nums = [10, 20, 30], k = 2, x = 1
        # Subarray [10, 20]: freq {10:1, 20:1}, top 1 is 20, sum = 20
        # Subarray [20, 30]: freq {20:1, 30:1}, top 1 is 30, sum = 30
        result = sol.findXSum([10, 20, 30], 2, 1)
        assert result == [20, 30]

    def test_single_element_subarray(self):
        """Test with k=1"""
        sol = Solution()
        # nums = [5, 10, 3], k = 1, x = 1
        # Each subarray has only 1 element, sum is that element
        result = sol.findXSum([5, 10, 3], 1, 1)
        assert result == [5, 10, 3]

    def test_n_equals_k(self):
        """Test when n equals k (only one subarray)"""
        sol = Solution()
        # nums = [1, 2, 3], k = 3, x = 2
        # One subarray: [1, 2, 3], freq all 1, top 2 by value: 3 and 2, sum = 5
        result = sol.findXSum([1, 2, 3], 3, 2)
        assert result == [5]

    def test_multiple_frequencies(self):
        """Test with varying frequencies"""
        sol = Solution()
        # nums = [1, 1, 1, 2, 2, 3], k = 3, x = 2
        # Subarray [1, 1, 1]: freq {1:3}, top 2 is 1, sum = 3
        # Subarray [1, 1, 2]: freq {1:2, 2:1}, top 2 are 1 and 2, sum = 4
        # Subarray [1, 2, 2]: freq {1:1, 2:2}, top 2 are 2 and 1, sum = 5
        # Subarray [2, 2, 3]: freq {2:2, 3:1}, top 2 are 2 and 3, sum = 7
        result = sol.findXSum([1, 1, 1, 2, 2, 3], 3, 2)
        assert result == [3, 4, 5, 7]

    def test_boundary_small_array(self):
        """Test with minimum size arrays"""
        sol = Solution()
        # nums = [1], k = 1, x = 1
        result = sol.findXSum([1], 1, 1)
        assert result == [1]

    def test_boundary_x_k(self):
        """Test x=k boundary"""
        sol = Solution()
        # nums = [1, 2, 3], k = 3, x = 3
        # One subarray, all 3 distinct, sum = 6
        result = sol.findXSum([1, 2, 3], 3, 3)
        assert result == [6]
