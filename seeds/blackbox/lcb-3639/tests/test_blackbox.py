from solution import Solution


class TestIsZeroArray:
    def test_basic_can_reduce_to_zero(self):
        """All elements can be reduced to zero - each element value <= coverage."""
        solution = Solution()
        nums = [1, 2, 3]
        queries = [[0, 2], [0, 2]]  # Each index covered 2 times
        # nums[0]=1 <= 2, nums[1]=2 <= 2, nums[2]=3 > 2 -> False
        assert solution.isZeroArray(nums, queries) == False

    def test_basic_can_reduce_to_zero_all(self):
        """All elements can be reduced to zero."""
        solution = Solution()
        nums = [1, 1, 1]
        queries = [[0, 2], [0, 2]]  # Each index covered 2 times
        # nums[0]=1 <= 2, nums[1]=1 <= 2, nums[2]=1 <= 2 -> True
        assert solution.isZeroArray(nums, queries) == True

    def test_zeros_array_always_true(self):
        """All zeros in nums should always return True."""
        solution = Solution()
        nums = [0, 0, 0]
        queries = [[0, 2]]
        assert solution.isZeroArray(nums, queries) == True

    def test_single_element_can_reduce(self):
        """Single element that can be reduced to zero."""
        solution = Solution()
        nums = [1]
        queries = [[0, 0]]
        assert solution.isZeroArray(nums, queries) == True

    def test_single_element_cannot_reduce(self):
        """Single element that cannot be reduced to zero."""
        solution = Solution()
        nums = [2]
        queries = [[0, 0]]
        assert solution.isZeroArray(nums, queries) == False

    def test_single_element_no_queries(self):
        """Single element with no queries cannot be reduced."""
        solution = Solution()
        nums = [1]
        queries = []
        assert solution.isZeroArray(nums, queries) == False

    def test_non_overlapping_queries(self):
        """Queries that don't overlap."""
        solution = Solution()
        nums = [1, 1, 1]
        queries = [[0, 0], [2, 2]]  # Middle element not covered
        # nums[1]=1 but coverage=0 -> False
        assert solution.isZeroArray(nums, queries) == False

    def test_all_elements_zero_coverage(self):
        """All elements have zero value, no queries needed."""
        solution = Solution()
        nums = [0, 0, 0]
        queries = [[0, 0], [2, 2]]
        assert solution.isZeroArray(nums, queries) == True

    def test_partial_coverage_sufficient(self):
        """Some elements need coverage, some don't."""
        solution = Solution()
        nums = [1, 0, 1]
        queries = [[0, 2], [0, 2]]  # Each covered 2 times
        # nums[0]=1 <= 2, nums[1]=0 <= 2, nums[2]=1 <= 2 -> True
        assert solution.isZeroArray(nums, queries) == True

    def test_boundary_max_value(self):
        """Test with maximum possible values."""
        solution = Solution()
        nums = [100000]
        queries = [[0, 0]] * 100000  # 100000 queries covering index 0
        assert solution.isZeroArray(nums, queries) == True

    def test_boundary_value_exceeds_coverage(self):
        """Test where value exceeds coverage."""
        solution = Solution()
        nums = [100000]
        queries = [[0, 0]] * 99999  # 99999 queries covering index 0
        assert solution.isZeroArray(nums, queries) == False

    def test_empty_nums_single_query(self):
        """Single element array."""
        solution = Solution()
        nums = [5]
        queries = [[0, 0]]
        assert solution.isZeroArray(nums, queries) == False

    def test_exact_coverage_needed(self):
        """Test exact coverage equals value."""
        solution = Solution()
        nums = [2, 2, 2]
        queries = [[0, 2], [0, 2]]  # Each covered 2 times
        # nums[i]=2, coverage=2 -> True
        assert solution.isZeroArray(nums, queries) == True

    def test_one_element_exceeds_coverage(self):
        """One element exceeds its coverage."""
        solution = Solution()
        nums = [3, 1, 1]
        queries = [[0, 2]]  # Each covered 1 time
        # nums[0]=3 > 1 -> False
        assert solution.isZeroArray(nums, queries) == False

    def test_disjoint_queries_full_coverage(self):
        """Disjoint queries covering all elements exactly."""
        solution = Solution()
        nums = [1, 1, 1, 1]
        queries = [[0, 0], [1, 1], [2, 2], [3, 3]]
        # Each covered 1 time, each needs 1 -> True
        assert solution.isZeroArray(nums, queries) == True

    def test_nested_queries(self):
        """Nested query ranges."""
        solution = Solution()
        nums = [1, 2, 1]
        queries = [[0, 2], [0, 2], [1, 1]]  # Index 1 covered 3 times
        # nums[0]=1 <= 2, nums[1]=2 <= 3, nums[2]=1 <= 2 -> True
        assert solution.isZeroArray(nums, queries) == True

    def test_query_not_covering_middle(self):
        """Query doesn't cover middle element."""
        solution = Solution()
        nums = [1, 1, 1]
        queries = [[0, 0], [2, 2]]
        # nums[1]=1 but coverage=0 -> False
        assert solution.isZeroArray(nums, queries) == False

    def test_all_queries_same_range(self):
        """All queries cover the same range."""
        solution = Solution()
        nums = [1, 1, 1]
        queries = [[0, 2]] * 3  # Each covered 3 times
        # nums[i]=1 <= 3 -> True
        assert solution.isZeroArray(nums, queries) == True
