import pytest
from typing import List
from solution import Solution


class TestMaxRemovals:
    def test_basic_example(self):
        """Test with example: source='abacb', pattern='ab', targetIndices=[0,2,4]"""
        solution = Solution()
        source = "abacb"
        pattern = "ab"
        targetIndices = [0, 2, 4]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 2  # Can remove indices 2 and 4

    def test_pattern_equals_source(self):
        """When pattern equals source, all indices are essential"""
        solution = Solution()
        source = "abc"
        pattern = "abc"
        targetIndices = [0, 1, 2]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 0

    def test_empty_target_indices(self):
        """No target indices means no removals"""
        solution = Solution()
        source = "abc"
        pattern = "a"
        targetIndices = []
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 0

    def test_all_removals_possible(self):
        """Pattern is single character, all other indices can be removed"""
        solution = Solution()
        source = "abc"
        pattern = "a"
        targetIndices = [1, 2]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 2

    def test_boundary_single_char(self):
        """Single character source and pattern"""
        solution = Solution()
        source = "a"
        pattern = "a"
        targetIndices = [0]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 0

    def test_boundary_single_char_pattern_diff(self):
        """Single character pattern that appears once"""
        solution = Solution()
        source = "abc"
        pattern = "b"
        targetIndices = [0, 2]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 1

    def test_repeated_pattern_chars(self):
        """Pattern with repeated characters"""
        solution = Solution()
        source = "aabbcc"
        pattern = "abc"
        targetIndices = [0, 1, 2, 3, 4, 5]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 3  # Essential: 0, 2, 4; can remove: 1, 3, 5

    def test_repeated_pattern_chars_mixed(self):
        """Pattern with repeated characters, selective removals"""
        solution = Solution()
        source = "aabbcc"
        pattern = "abc"
        targetIndices = [0, 3, 5]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 2  # Essential: 0, 2, 4; can remove: 3, 5

    def test_pattern_at_end(self):
        """Pattern character at the end of source"""
        solution = Solution()
        source = "abc"
        pattern = "c"
        targetIndices = [0, 1]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 0  # Index 2 is essential, but not in targetIndices

    def test_pattern_in_middle(self):
        """Pattern character in the middle of source"""
        solution = Solution()
        source = "abc"
        pattern = "b"
        targetIndices = [0, 2]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 1  # Index 1 is essential, can remove 0 and 2

    def test_long_source_short_pattern(self):
        """Long source with short pattern"""
        solution = Solution()
        source = "abcdefghij"
        pattern = "ac"
        targetIndices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 8  # Essential: 0, 2; can remove: 1, 3, 4, 5, 6, 7, 8, 9

    def test_pattern_with_duplicates_in_source(self):
        """Pattern character appears multiple times in source"""
        solution = Solution()
        source = "aaabbb"
        pattern = "ab"
        targetIndices = [0, 1, 2, 3, 4, 5]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 4  # Essential: 0, 3; can remove: 1, 2, 4, 5

    def test_target_indices_subset(self):
        """targetIndices is a subset of all indices"""
        solution = Solution()
        source = "abcd"
        pattern = "ac"
        targetIndices = [0, 2]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 0  # Both 0 and 2 are essential

    def test_pattern_first_char_only(self):
        """Pattern consists of only the first character of source"""
        solution = Solution()
        source = "abcde"
        pattern = "a"
        targetIndices = [1, 2, 3, 4]
        result = solution.maxRemovals(source, pattern, targetIndices)
        assert result == 4  # Only index 0 is essential
