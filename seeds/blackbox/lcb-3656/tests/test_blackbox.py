from solution import Solution


class TestMinimumOperations:
    def test_already_distinct(self):
        """Array with all distinct elements requires 0 operations."""
        sol = Solution()
        assert sol.minimumOperations([1, 2, 3, 4, 5]) == 0

    def test_single_element(self):
        """Single element is already distinct."""
        sol = Solution()
        assert sol.minimumOperations([42]) == 0

    def test_two_distinct_elements(self):
        """Two distinct elements require 0 operations."""
        sol = Solution()
        assert sol.minimumOperations([1, 2]) == 0

    def test_two_same_elements(self):
        """Two identical elements require 1 operation to remove both."""
        sol = Solution()
        assert sol.minimumOperations([1, 1]) == 1

    def test_three_distinct_elements(self):
        """Three distinct elements require 0 operations."""
        sol = Solution()
        assert sol.minimumOperations([1, 2, 3]) == 0

    def test_three_same_elements(self):
        """Three identical elements require 1 operation to remove all."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1]) == 1

    def test_remove_three_makes_distinct(self):
        """Array where removing 3 elements from start makes it distinct."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1, 2, 3]) == 1

    def test_remove_three_not_enough(self):
        """Array where removing 3 elements still has duplicates."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1, 1, 1]) == 2

    def test_remove_six_makes_distinct(self):
        """Array where removing 6 elements from start makes it distinct."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1, 1, 1, 1, 2, 3]) == 2

    def test_remove_six_not_enough(self):
        """Array where removing 6 elements still has duplicates."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1, 1, 1, 1, 1, 1]) == 3

    def test_remove_all_makes_distinct(self):
        """Empty array is distinct, requires operations to remove all."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1]) == 1

    def test_alternating_duplicates(self):
        """Array with alternating duplicates at different positions."""
        sol = Solution()
        assert sol.minimumOperations([1, 2, 1, 2, 3]) == 1

    def test_boundary_length_100_all_same(self):
        """100 identical elements - after 33 ops, 1 element left which is distinct."""
        sol = Solution()
        assert sol.minimumOperations([1] * 100) == 33

    def test_length_99_all_same(self):
        """99 identical elements - after 33 ops, 0 elements left."""
        sol = Solution()
        assert sol.minimumOperations([1] * 99) == 33

    def test_all_same_elements(self):
        """All elements are the same, need to remove all."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1, 1, 1]) == 2

    def test_mixed_duplicates(self):
        """Multiple types of duplicates at different positions."""
        sol = Solution()
        assert sol.minimumOperations([1, 2, 1, 2, 1, 2]) == 2

    def test_two_elements_same(self):
        """Two same elements."""
        sol = Solution()
        assert sol.minimumOperations([5, 5]) == 1

    def test_three_elements_two_same(self):
        """Three elements with two same."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 2]) == 1

    def test_three_elements_all_same(self):
        """Three elements all same."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1]) == 1

    def test_five_elements_all_same(self):
        """Five elements all same."""
        sol = Solution()
        assert sol.minimumOperations([1, 1, 1, 1, 1]) == 2

    def test_large_array_distinct_suffix(self):
        """Large array where a suffix is distinct."""
        sol = Solution()
        # First 6 elements have duplicates, last 3 are distinct
        assert sol.minimumOperations([1, 1, 2, 2, 3, 3, 4, 5, 6]) == 2
