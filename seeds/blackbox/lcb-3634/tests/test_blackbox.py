import pytest
from solution import Solution


class TestCalculateScore:
    """Tests for calculateScore function."""

    def test_single_character(self):
        """Single character - no pairs possible."""
        sol = Solution()
        assert sol.calculateScore("a") == 0

    def test_two_mirror_characters(self):
        """Two mirror characters 'a' and 'z' form one pair."""
        sol = Solution()
        assert sol.calculateScore("az") == 1

    def test_two_non_mirror_characters(self):
        """Two characters that are not mirrors."""
        sol = Solution()
        assert sol.calculateScore("ab") == 0

    def test_reverse_order_mirror(self):
        """Mirror characters in reverse order 'z' then 'a'."""
        sol = Solution()
        assert sol.calculateScore("za") == 1

    def test_no_pairs_at_all(self):
        """String with no mirror pairs."""
        sol = Solution()
        assert sol.calculateScore("abc") == 0

    def test_multiple_pairs_separate(self):
        """Multiple separate mirror pairs."""
        sol = Solution()
        assert sol.calculateScore("azaz") == 2

    def test_multiple_pairs_interleaved(self):
        """Multiple mirror pairs with interleaving."""
        sol = Solution()
        assert sol.calculateScore("azazaz") == 3

    def test_three_same_character(self):
        """Three same characters - no mirrors."""
        sol = Solution()
        assert sol.calculateScore("aaa") == 0

    def test_three_mirror_pairs(self):
        """Three mirror pairs."""
        sol = Solution()
        assert sol.calculateScore("azazaz") == 3

    def test_b_and_y_mirror(self):
        """Test 'b' and 'y' mirror pair."""
        sol = Solution()
        assert sol.calculateScore("by") == 1

    def test_y_and_b_mirror(self):
        """Test 'y' and 'b' mirror pair."""
        sol = Solution()
        assert sol.calculateScore("yb") == 1

    def test_c_and_x_mirror(self):
        """Test 'c' and 'x' mirror pair."""
        sol = Solution()
        assert sol.calculateScore("cx") == 1

    def test_overlapping_pairs(self):
        """Overlapping potential pairs - 'azbza'."""
        sol = Solution()
        # i=0: 'a', skip
        # i=1: 'z', mirror 'a' at j=0, mark (0,1), score += 1
        # i=2: 'b', mirror 'y', none before
        # i=3: 'z', mirror 'a' - j=2='b' no, j=1='z' marked, j=0='a' marked, skip
        # i=4: 'a', mirror 'z' at j=3, mark (3,4), score += 1
        assert sol.calculateScore("azbza") == 2

    def test_longer_string_multiple_pairs(self):
        """Longer string with multiple mirror pairs."""
        sol = Solution()
        assert sol.calculateScore("azazazaz") == 4

    def test_mixed_characters(self):
        """Mixed characters with some mirrors."""
        sol = Solution()
        # "axza" - 'a' at 0, 'x' at 1 (mirror 'c'), 'z' at 2 (mirror 'a' at 0), 'a' at 3 (mirror 'z' at 2)
        # i=0: 'a', skip
        # i=1: 'x', mirror 'c', none before
        # i=2: 'z', mirror 'a' at j=0, mark (0,2), score += 2
        # i=3: 'a', mirror 'z' at j=2 marked, j=1='x' no, j=0='a' marked, skip
        assert sol.calculateScore("axza") == 2

    def test_boundary_single_letter(self):
        """Minimum length boundary."""
        sol = Solution()
        assert sol.calculateScore("a") == 0
