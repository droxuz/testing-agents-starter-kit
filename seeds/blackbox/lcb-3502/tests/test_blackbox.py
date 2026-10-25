from solution import Solution


class TestNumberOfSubstrings:
    def test_k_equals_1_all_substrings_qualify(self):
        """When k=1, every substring has at least one character appearing >= 1 time."""
        sol = Solution()
        # s="abc", substrings: a, b, c, ab, bc, abc = 6 total
        assert sol.numberOfSubstrings("abc", 1) == 6

    def test_single_character_k_1(self):
        """Single character with k=1."""
        sol = Solution()
        # s="a", substring: "a" = 1
        assert sol.numberOfSubstrings("a", 1) == 1

    def test_single_character_k_2(self):
        """Single character with k=2, no substring qualifies."""
        sol = Solution()
        # s="a", substring: "a" has 'a' appearing 1 time < 2
        assert sol.numberOfSubstrings("a", 2) == 0

    def test_two_same_chars_k_2(self):
        """Two identical characters with k=2."""
        sol = Solution()
        # s="aa", substrings: "a", "a", "aa"
        # "aa" has 'a' appearing 2 times >= 2
        assert sol.numberOfSubstrings("aa", 2) == 1

    def test_two_different_chars_k_2(self):
        """Two different characters with k=2."""
        sol = Solution()
        # s="ab", substrings: "a", "b", "ab"
        # None have any char appearing >= 2 times
        assert sol.numberOfSubstrings("ab", 2) == 0

    def test_aab_k_2(self):
        """String with one char appearing twice."""
        sol = Solution()
        # s="aab", substrings: a, a, b, aa, ab, aab
        # "aa": 'a' appears 2 times ✓
        # "aab": 'a' appears 2 times ✓
        assert sol.numberOfSubstrings("aab", 2) == 2

    def test_aaa_k_2(self):
        """All same characters with k=2."""
        sol = Solution()
        # s="aaa", substrings: a, a, a, aa, aa, aaa
        # Length 2: 2 substrings with 'a' appearing 2 times
        # Length 3: 1 substring with 'a' appearing 3 times
        assert sol.numberOfSubstrings("aaa", 2) == 3

    def test_abc_k_2(self):
        """All different characters with k=2."""
        sol = Solution()
        # s="abc", substrings: a, b, c, ab, bc, abc
        # None have any char appearing >= 2 times
        assert sol.numberOfSubstrings("abc", 2) == 0

    def test_aaa_k_3(self):
        """All same characters with k=3."""
        sol = Solution()
        # s="aaa", only "aaa" has 'a' appearing 3 times
        assert sol.numberOfSubstrings("aaa", 3) == 1

    def test_aabbcc_k_2(self):
        """String with multiple character pairs."""
        sol = Solution()
        # Length 2: "aa", "bb", "cc" = 3
        # Length 3: "aab", "abb", "bbc", "bcc" = 4
        # Length 4: "aabb", "abbc", "bbcc" = 3
        # Length 5: "aabbc", "abbcc" = 2
        # Length 6: "aabbcc" = 1
        # Total: 13
        assert sol.numberOfSubstrings("aabbcc", 2) == 13

    def test_abcabc_k_2(self):
        """Repeated pattern with k=2."""
        sol = Solution()
        # Length 3: "abca" (a:2), "bcab" (b:2, a:2), "cabc" (c:2, a:2, b:2) = 3
        # Length 4: "abcab" (a:2, b:2), "bcabc" (b:2, c:2, a:2) = 2
        # Length 5: "abcabc" (a:2, b:2, c:2) = 1
        # Total: 6
        assert sol.numberOfSubstrings("abcabc", 2) == 6

    def test_k_equals_length(self):
        """k equals string length."""
        sol = Solution()
        # s="abc", k=3, only "abc" has all 3 chars but none appear >= 3 times
        assert sol.numberOfSubstrings("abc", 3) == 0
        # s="aaa", k=3, only "aaa" has 'a' appearing 3 times
        assert sol.numberOfSubstrings("aaa", 3) == 1

    def test_longer_string_all_same_k_2(self):
        """Longer string with all same characters, k=2."""
        sol = Solution()
        # s="aaaa", substrings: 4 length-1, 3 length-2, 2 length-3, 1 length-4
        # Length 2+: all qualify
        # 3 + 2 + 1 = 6
        assert sol.numberOfSubstrings("aaaa", 2) == 6

    def test_k_equals_1_single_char(self):
        """k=1 with single character."""
        sol = Solution()
        assert sol.numberOfSubstrings("z", 1) == 1

    def test_boundary_k_equals_1(self):
        """k=1 minimum boundary."""
        sol = Solution()
        # For k=1, all substrings qualify
        # s="abcde" has 5+4+3+2+1 = 15 substrings
        assert sol.numberOfSubstrings("abcde", 1) == 15
