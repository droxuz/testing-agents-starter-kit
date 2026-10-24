from solution import Solution


class TestMaxRemoval:
    def test_single_element_one_query(self):
        """Single element array, one query covering it."""
        sol = Solution()
        assert sol.maxRemoval([1], [[0, 0]]) == 0

    def test_multiple_queries_same_range(self):
        """Multiple identical queries, only need one."""
        sol = Solution()
        assert sol.maxRemoval([1], [[0, 0], [0, 0]]) == 1

    def test_single_query_covers_all(self):
        """Single query covering all indices."""
        sol = Solution()
        assert sol.maxRemoval([1, 1], [[0, 1]]) == 0

    def test_separate_queries_for_each_index(self):
        """Separate queries for each index."""
        sol = Solution()
        assert sol.maxRemoval([1, 1], [[0, 0], [1, 1]]) == 0

    def test_impossible_single_index(self):
        """Single index needs more queries than available."""
        sol = Solution()
        assert sol.maxRemoval([2], [[0, 0]]) == -1

    def test_impossible_multiple_indices(self):
        """Multiple indices, impossible to satisfy."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 0]]) == -1

    def test_multiple_redundant_queries(self):
        """Multiple identical queries, only need one."""
        sol = Solution()
        assert sol.maxRemoval([1, 1], [[0, 1], [0, 1], [0, 1]]) == 2

    def test_different_ranges_cover_all(self):
        """Queries with different ranges, need all."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 0], [1, 1], [2, 2]]) == 0

    def test_overlapping_ranges_one_sufficient(self):
        """Overlapping ranges, one query is sufficient."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 2], [0, 1], [1, 2]]) == 2

    def test_needs_multiple_queries_for_one_index(self):
        """One index needs multiple queries."""
        sol = Solution()
        assert sol.maxRemoval([2, 2, 2], [[0, 2], [0, 2]]) == 0

    def test_zero_elements(self):
        """Array with all zeros, no queries needed."""
        sol = Solution()
        assert sol.maxRemoval([0, 0, 0], [[0, 2]]) == 1

    def test_partial_coverage_needed(self):
        """Some indices need coverage, some don't."""
        sol = Solution()
        assert sol.maxRemoval([0, 1, 0], [[0, 2]]) == 0

    def test_overlapping_ranges_need_both(self):
        """Overlapping ranges, need both queries."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 1], [1, 2]]) == 0

    def test_redundant_query_in_middle(self):
        """Three queries, one is redundant."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 2], [0, 1], [1, 2]]) == 2

    def test_large_nums_single_query(self):
        """Large nums value, single query not enough."""
        sol = Solution()
        assert sol.maxRemoval([5], [[0, 0]]) == -1

    def test_large_nums_multiple_queries(self):
        """Large nums value, enough queries available."""
        sol = Solution()
        assert sol.maxRemoval([3], [[0, 0], [0, 0], [0, 0]]) == 0

    def test_queries_different_ranges(self):
        """Queries with different ranges covering multiple indices."""
        sol = Solution()
        assert sol.maxRemoval([1, 2, 1], [[0, 1], [1, 2], [0, 2]]) == 1

    def test_all_queries_needed(self):
        """All queries are needed to satisfy requirements."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 0], [1, 1], [2, 2]]) == 0

    def test_empty_queries_not_possible(self):
        """No queries provided."""
        sol = Solution()
        assert sol.maxRemoval([1], []) == -1

    def test_single_query_not_covering_all(self):
        """Single query doesn't cover all needed indices."""
        sol = Solution()
        assert sol.maxRemoval([1, 1], [[0, 0]]) == -1

    def test_single_query_covering_all(self):
        """Single query covers all needed indices."""
        sol = Solution()
        assert sol.maxRemoval([1, 1], [[0, 1]]) == 0

    def test_two_queries_partial_coverage(self):
        """Two queries, partial coverage needed."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 1], [1, 2]]) == 0

    def test_three_queries_one_sufficient(self):
        """Three queries, one is sufficient."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 2], [0, 2], [0, 2]]) == 2

    def test_three_queries_different_ranges(self):
        """Three queries with different ranges."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 0], [1, 1], [2, 2]]) == 0

    def test_two_identical_queries(self):
        """Two identical queries covering all."""
        sol = Solution()
        assert sol.maxRemoval([1, 1], [[0, 1], [0, 1]]) == 1

    def test_three_identical_queries(self):
        """Three identical queries covering all."""
        sol = Solution()
        assert sol.maxRemoval([1, 1], [[0, 1], [0, 1], [0, 1]]) == 2

    def test_single_index_needs_two_queries(self):
        """Single index needs two queries."""
        sol = Solution()
        assert sol.maxRemoval([2], [[0, 0], [0, 0]]) == 0

    def test_single_index_needs_three_queries(self):
        """Single index needs three queries."""
        sol = Solution()
        assert sol.maxRemoval([3], [[0, 0], [0, 0], [0, 0]]) == 0

    def test_mixed_zero_and_nonzero(self):
        """Mixed zero and nonzero values."""
        sol = Solution()
        assert sol.maxRemoval([0, 1, 0, 1, 0], [[0, 4]]) == 0

    def test_single_index_needs_one_query(self):
        """Single index needs one query."""
        sol = Solution()
        assert sol.maxRemoval([1], [[0, 0]]) == 0

    def test_single_index_needs_zero_queries(self):
        """Single index needs zero queries."""
        sol = Solution()
        assert sol.maxRemoval([0], [[0, 0]]) == 1

    def test_all_zero_array(self):
        """All zero array, can remove all queries."""
        sol = Solution()
        assert sol.maxRemoval([0, 0, 0], [[0, 2], [0, 2]]) == 2

    def test_single_query_range(self):
        """Single query covering a range."""
        sol = Solution()
        assert sol.maxRemoval([1, 1, 1], [[0, 2]]) == 0
