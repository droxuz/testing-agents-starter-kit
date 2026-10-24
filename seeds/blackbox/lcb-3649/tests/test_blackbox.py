from typing import List
from solution import Solution


class TestFindMinimumTime:
    """Tests for findMinimumTime function."""

    def test_single_lock_small(self):
        """Single lock with small strength."""
        solution = Solution()
        result = solution.findMinimumTime([5], 1)
        assert result == 5  # ceil(5/1) = 5

    def test_single_lock_large(self):
        """Single lock with large strength at boundary."""
        solution = Solution()
        result = solution.findMinimumTime([1000000], 1)
        assert result == 1000000  # ceil(1000000/1) = 1000000

    def test_two_locks_smaller_first(self):
        """Two locks - breaking smaller first is optimal."""
        solution = Solution()
        result = solution.findMinimumTime([3, 5], 1)
        assert result == 6  # ceil(3/1)=3, then ceil(5/2)=3, total=6

    def test_two_locks_larger_first(self):
        """Two locks - same as above, order doesn't matter for result."""
        solution = Solution()
        result = solution.findMinimumTime([5, 3], 1)
        assert result == 6

    def test_two_locks_with_k_2(self):
        """Two locks with K=2."""
        solution = Solution()
        result = solution.findMinimumTime([1, 10], 2)
        assert result == 5  # ceil(1/1)=1, X=3, ceil(10/3)=4, total=5

    def test_three_locks_same_strength(self):
        """Three locks with same strength."""
        solution = Solution()
        result = solution.findMinimumTime([1, 1, 1], 1)
        assert result == 3  # ceil(1/1)=1, X=2, ceil(1/2)=1, X=3, ceil(1/3)=1, total=3

    def test_three_locks_increasing(self):
        """Three locks with increasing strength."""
        solution = Solution()
        result = solution.findMinimumTime([1, 2, 3], 1)
        assert result == 3  # ceil(1/1)=1, X=2, ceil(2/2)=1, X=3, ceil(3/3)=1, total=3

    def test_k_at_boundary_min(self):
        """K at minimum value."""
        solution = Solution()
        result = solution.findMinimumTime([10], 1)
        assert result == 10

    def test_k_at_boundary_max(self):
        """K at maximum value."""
        solution = Solution()
        result = solution.findMinimumTime([10], 10)
        assert result == 10

    def test_two_locks_k_10(self):
        """Two locks with K=10."""
        solution = Solution()
        result = solution.findMinimumTime([5, 10], 10)
        assert result == 6  # ceil(5/1)=5, X=11, ceil(10/11)=1, total=6

    def test_two_locks_k_10_reverse(self):
        """Two locks with K=10, reversed order."""
        solution = Solution()
        result = solution.findMinimumTime([10, 5], 10)
        assert result == 6

    def test_two_locks_k_10_boundary_strengths(self):
        """Two locks with K=10 and boundary strengths."""
        solution = Solution()
        result = solution.findMinimumTime([1, 1000000], 10)
        assert result == 90911  # ceil(1/1)=1, X=11, ceil(1000000/11)=90910, total=90911

    def test_n_at_boundary_min(self):
        """Minimum n value."""
        solution = Solution()
        result = solution.findMinimumTime([1], 1)
        assert result == 1

    def test_n_at_boundary_max(self):
        """Maximum n value."""
        solution = Solution()
        result = solution.findMinimumTime([1, 2, 3, 4, 5, 6, 7, 8], 1)
        assert result == 8

    def test_all_same_small(self):
        """All locks with small same strength."""
        solution = Solution()
        result = solution.findMinimumTime([1, 1, 1, 1], 1)
        assert result == 4  # Each takes 1 minute

    def test_large_k_with_small_locks(self):
        """Large K with small locks."""
        solution = Solution()
        result = solution.findMinimumTime([1, 1, 1], 10)
        assert result == 3  # Each takes 1 minute

    def test_two_locks_both_divisible(self):
        """Two locks where both divide evenly by X."""
        solution = Solution()
        result = solution.findMinimumTime([2, 4], 1)
        assert result == 4  # ceil(2/1)=2, X=2, ceil(4/2)=2, total=4

    def test_two_locks_first_not_divisible(self):
        """Two locks where first is not divisible by X."""
        solution = Solution()
        result = solution.findMinimumTime([3, 4], 1)
        assert result == 5  # ceil(3/1)=3, X=2, ceil(4/2)=2, total=5

    def test_two_locks_second_not_divisible(self):
        """Two locks where second is not divisible by X."""
        solution = Solution()
        result = solution.findMinimumTime([2, 5], 1)
        assert result == 5  # ceil(2/1)=2, X=2, ceil(5/2)=3, total=5

    def test_single_lock_k_max(self):
        """Single lock with K at max."""
        solution = Solution()
        result = solution.findMinimumTime([1000000], 10)
        assert result == 1000000  # Only one lock, K doesn't matter

    def test_two_locks_strong_second(self):
        """Two locks, second is much stronger."""
        solution = Solution()
        result = solution.findMinimumTime([1, 1000000], 1)
        assert result == 500001  # ceil(1/1)=1, X=2, ceil(1000000/2)=500000, total=500001

    def test_two_locks_weak_second(self):
        """Two locks, second is weaker - order matters."""
        solution = Solution()
        result = solution.findMinimumTime([1000000, 1], 1)
        assert result == 500001  # Sorted: [1, 1000000], same as above
