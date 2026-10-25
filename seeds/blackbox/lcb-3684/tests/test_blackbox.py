from solution import Solution


class TestSubstringMatching:
    """Tests for the hasMatch function with substring matching pattern."""

    def test_basic_match_with_star(self):
        """Pattern with star in middle matches substring."""
        solution = Solution()
        assert solution.hasMatch("abacaba", "a*c") is True

    def test_star_at_end_prefix_only(self):
        """Pattern with star at end matches prefix."""
        solution = Solution()
        assert solution.hasMatch("abc", "a*") is True

    def test_star_at_start_suffix_only(self):
        """Pattern with star at start matches suffix."""
        solution = Solution()
        assert solution.hasMatch("abc", "*c") is True

    def test_star_alone_anything_matches(self):
        """Single star matches any non-empty substring."""
        solution = Solution()
        assert solution.hasMatch("abc", "*") is True

    def test_no_match_different_chars(self):
        """Pattern with no matching characters returns False."""
        solution = Solution()
        assert solution.hasMatch("abc", "d*c") is False

    def test_exact_match_with_star(self):
        """Pattern matches exact string."""
        solution = Solution()
        assert solution.hasMatch("abc", "ab*c") is True

    def test_pattern_longer_than_string(self):
        """Pattern longer than string cannot match."""
        solution = Solution()
        assert solution.hasMatch("ab", "a*c") is False

    def test_pattern_shorter_than_string(self):
        """Pattern shorter than string can match."""
        solution = Solution()
        assert solution.hasMatch("abcde", "a*c") is True

    def test_complex_pattern_full_match(self):
        """Complex pattern matches full string."""
        solution = Solution()
        assert solution.hasMatch("abcde", "ab*de") is True

    def test_complex_pattern_no_match(self):
        """Complex pattern doesn't match."""
        solution = Solution()
        assert solution.hasMatch("abcde", "ab*xyz") is False

    def test_star_at_end_matches_prefix(self):
        """Star at end matches any prefix."""
        solution = Solution()
        assert solution.hasMatch("abc", "*bc") is True

    def test_star_at_start_matches_suffix(self):
        """Star at start matches any suffix."""
        solution = Solution()
        assert solution.hasMatch("abc", "a*") is True

    def test_empty_star_sequence(self):
        """Star matches empty sequence between chars."""
        solution = Solution()
        assert solution.hasMatch("abc", "a*c") is True

    def test_single_char_string(self):
        """Single character string matches."""
        solution = Solution()
        assert solution.hasMatch("a", "*") is True

    def test_single_char_string_with_prefix_star(self):
        """Single char with prefix star."""
        solution = Solution()
        assert solution.hasMatch("a", "a*") is True

    def test_single_char_string_with_suffix_star(self):
        """Single char with suffix star."""
        solution = Solution()
        assert solution.hasMatch("a", "*a") is True

    def test_star_between_same_chars(self):
        """Star between same characters."""
        solution = Solution()
        assert solution.hasMatch("aba", "a*a") is True

    def test_star_matches_multiple_positions(self):
        """Star can match at different positions."""
        solution = Solution()
        assert solution.hasMatch("abcdef", "a*c") is True

    def test_star_with_empty_prefix_and_suffix(self):
        """Star alone in pattern."""
        solution = Solution()
        assert solution.hasMatch("xyz", "*") is True

    def test_boundary_min_length_s(self):
        """Minimum length string s=1."""
        solution = Solution()
        assert solution.hasMatch("a", "*") is True

    def test_boundary_min_length_p(self):
        """Minimum length pattern p=2 (char + star)."""
        solution = Solution()
        assert solution.hasMatch("ab", "a*") is True

    def test_star_with_no_matching_suffix(self):
        """Star with no matching suffix."""
        solution = Solution()
        assert solution.hasMatch("abc", "d*e") is False

    def test_star_with_no_matching_prefix(self):
        """Star with no matching prefix."""
        solution = Solution()
        assert solution.hasMatch("abc", "*d") is False

    def test_star_matches_middle(self):
        """Star matches characters in middle."""
        solution = Solution()
        assert solution.hasMatch("abcd", "a*d") is True

    def test_star_matches_empty_between(self):
        """Star matches empty sequence."""
        solution = Solution()
        assert solution.hasMatch("abc", "a*c") is True

    def test_star_matches_all(self):
        """Star matches all characters."""
        solution = Solution()
        assert solution.hasMatch("abc", "*c") is True

    def test_star_matches_none(self):
        """Star matches nothing (empty string)."""
        solution = Solution()
        assert solution.hasMatch("abc", "*") is True
