from solution import Solution


class TestPossibleStringCount:
    """Tests for possibleStringCount function."""
    
    def test_single_character(self):
        """Single character - only one original possible."""
        sol = Solution()
        assert sol.possibleStringCount("a") == 1
    
    def test_double_same_character(self):
        """Two same characters - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aa") == 2
    
    def test_triple_same_character(self):
        """Three same characters - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aaa") == 2
    
    def test_single_different_characters(self):
        """All different characters - only one original possible."""
        sol = Solution()
        assert sol.possibleStringCount("abc") == 1
    
    def test_two_runs_first_repeated(self):
        """Two runs, first has repeat - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aab") == 2
    
    def test_two_runs_second_repeated(self):
        """Two runs, second has repeat - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("abb") == 2
    
    def test_two_runs_both_repeated(self):
        """Two runs, both have repeats - three originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aabb") == 3
    
    def test_three_runs_all_different(self):
        """Three runs, all single characters - one original possible."""
        sol = Solution()
        assert sol.possibleStringCount("abcd") == 1
    
    def test_three_runs_first_repeated(self):
        """Three runs, first has repeat - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aabbcc") == 3
    
    def test_three_runs_first_and_second_repeated(self):
        """Three runs, first and second have repeats - three originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aaabbbccc") == 4
    
    def test_all_same_characters_long(self):
        """All same characters, long run - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aaaa") == 2
    
    def test_alternating_characters(self):
        """Alternating characters - one original possible."""
        sol = Solution()
        assert sol.possibleStringCount("abab") == 1
    
    def test_two_runs_first_repeated_long(self):
        """Two runs, first has long repeat - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aaab") == 2
    
    def test_two_runs_second_repeated_long(self):
        """Two runs, second has long repeat - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("abbb") == 2
    
    def test_boundary_min_length(self):
        """Minimum length input - one original possible."""
        sol = Solution()
        assert sol.possibleStringCount("z") == 1
    
    def test_boundary_max_length(self):
        """Maximum length input with all same chars - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("a" * 100) == 2
    
    def test_boundary_max_length_alternating(self):
        """Maximum length input with alternating chars - one original possible."""
        sol = Solution()
        assert sol.possibleStringCount("ab" * 50) == 1
    
    def test_three_runs_all_repeated(self):
        """Three runs, all have repeats - four originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aabbccdd") == 4
    
    def test_two_runs_first_repeated_long_second_short(self):
        """Two runs, first has long repeat, second is single - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("aaaaab") == 2
    
    def test_two_runs_first_short_second_repeated_long(self):
        """Two runs, first is single, second has long repeat - two originals possible."""
        sol = Solution()
        assert sol.possibleStringCount("abbbbb") == 2
