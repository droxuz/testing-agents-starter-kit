from solution import Solution


class TestSumOfGoodSubsequences:
    def test_single_element(self):
        """Single element array - only size 1 subsequence is good"""
        solution = Solution()
        # [5] -> only [5] is good, sum = 5
        assert solution.sumOfGoodSubsequences([5]) == 5

    def test_two_consecutive(self):
        """Two consecutive elements - both size 1 and size 2 subsequences are good"""
        solution = Solution()
        # [1, 2]: size 1: [1]=1, [2]=2 (sum=3); size 2: [1,2]=3
        # Total = 3 + 3 = 6
        assert solution.sumOfGoodSubsequences([1, 2]) == 6

    def test_two_reverse_consecutive(self):
        """Two reverse consecutive elements"""
        solution = Solution()
        # [2, 1]: size 1: [2]=2, [1]=1 (sum=3); size 2: [2,1]=3
        # Total = 3 + 3 = 6
        assert solution.sumOfGoodSubsequences([2, 1]) == 6

    def test_three_consecutive(self):
        """Three consecutive elements"""
        solution = Solution()
        # [1, 2, 3]:
        # Size 1: [1]=1, [2]=2, [3]=3 (sum=6)
        # Size 2: [1,2]=3, [2,3]=5 (sum=8)
        # Size 3: [1,2,3]=6
        # Total = 6 + 8 + 6 = 20
        assert solution.sumOfGoodSubsequences([1, 2, 3]) == 20

    def test_three_with_repeated(self):
        """Three elements with repeated values - only size 1 subsequences are good"""
        solution = Solution()
        # [1, 1, 1]: only size 1 subsequences are good (|1-1|=0, not 1)
        # Total = 1 + 1 + 1 = 3
        assert solution.sumOfGoodSubsequences([1, 1, 1]) == 3

    def test_alternating(self):
        """Alternating elements like 1, 2, 1, 2"""
        solution = Solution()
        # [1, 2, 1, 2]:
        # Size 1: [1], [2], [1], [2] = 1+2+1+2 = 6
        # Size 2: [1,2](0,1)=3, [1,2](0,3)=3, [2,1](1,2)=3, [1,2](2,3)=3 = 12
        # Size 3: [1,2,1](0,1,2)=4, [2,1,2](1,2,3)=5 = 9
        # Size 4: [1,2,1,2](0,1,2,3)=6
        # Total = 6 + 12 + 9 + 6 = 33
        assert solution.sumOfGoodSubsequences([1, 2, 1, 2]) == 33

    def test_with_zero(self):
        """Test with zero value"""
        solution = Solution()
        # [0]: only [0] is good, sum = 0
        assert solution.sumOfGoodSubsequences([0]) == 0

    def test_non_consecutive_values(self):
        """Values that are not consecutive - only size 1 subsequences are good"""
        solution = Solution()
        # [1, 3, 2]:
        # Size 1: [1]=1, [3]=3, [2]=2 (sum=6)
        # Size 2: [1,3] NO (|1-3|=2), [1,2]=3 (good), [3,2]=5 (good)
        # Size 3: [1,3,2] NO (|1-3|=2)
        # Total = 6 + 3 + 5 = 14
        assert solution.sumOfGoodSubsequences([1, 3, 2]) == 14

    def test_with_repeated_and_consecutive(self):
        """Mixed repeated and consecutive values"""
        solution = Solution()
        # [1, 1, 2]:
        # Size 1: [1], [1], [2] = 4
        # Size 2: [1,1] NO, [1,2](0,2)=3 (good), [1,2](1,2)=3 (good)
        # Size 3: [1,1,2] NO
        # Total = 4 + 3 + 3 = 10
        assert solution.sumOfGoodSubsequences([1, 1, 2]) == 10

    def test_alternating_10_11(self):
        """Alternating 10, 11, 10, 11"""
        solution = Solution()
        # [10, 11, 10, 11]:
        # Size 1: 10+11+10+11 = 42
        # Size 2: [10,11](0,1)=21, [10,11](0,3)=21, [11,10](1,2)=21, [10,11](2,3)=21 = 84
        # Size 3: [10,11,10](0,1,2)=31, [11,10,11](1,2,3)=32 = 63
        # Size 4: [10,11,10,11]=42
        # Total = 42 + 84 + 63 + 42 = 231
        assert solution.sumOfGoodSubsequences([10, 11, 10, 11]) == 231

    def test_empty_subsequences_not_possible(self):
        """Minimum array length is 1"""
        solution = Solution()
        # Single element [0]
        assert solution.sumOfGoodSubsequences([0]) == 0

    def test_large_values(self):
        """Test with large values that don't affect the logic"""
        solution = Solution()
        # [100, 101]: same logic as [1, 2]
        # Size 1: 100+101 = 201
        # Size 2: 100+101 = 201
        # Total = 402
        assert solution.sumOfGoodSubsequences([100, 101]) == 402

    def test_all_same_values(self):
        """All values are the same - only size 1 subsequences are good"""
        solution = Solution()
        # [5, 5, 5, 5]: only size 1 subsequences are good
        # Total = 5 + 5 + 5 + 5 = 20
        assert solution.sumOfGoodSubsequences([5, 5, 5, 5]) == 20

    def test_with_negative_difference(self):
        """Test that absolute difference is considered"""
        solution = Solution()
        # [2, 1]: |2-1|=1, good
        # Size 1: 2+1=3
        # Size 2: 2+1=3
        # Total = 6
        assert solution.sumOfGoodSubsequences([2, 1]) == 6

    def test_modulo_result(self):
        """Test that results are within expected bounds (no modulo needed for small inputs)"""
        solution = Solution()
        # Verify basic calculation
        assert solution.sumOfGoodSubsequences([1, 2]) == 6
        assert solution.sumOfGoodSubsequences([1, 2, 3]) == 20
