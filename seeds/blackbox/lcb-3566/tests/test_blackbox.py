from typing import List
from solution import Solution


class TestStringSequence:
    def test_single_char_a(self):
        """Single character 'a' - just press key 1"""
        sol = Solution()
        result = sol.stringSequence("a")
        assert result == ["", "a"]

    def test_single_char_b(self):
        """Single character 'b' - press key 1 then key 2"""
        sol = Solution()
        result = sol.stringSequence("b")
        assert result == ["", "a", "b"]

    def test_single_char_z(self):
        """Single character 'z' - press key 1 then 25 key 2 presses"""
        sol = Solution()
        result = sol.stringSequence("z")
        assert result == ["", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    def test_two_same_chars_aa(self):
        """Two 'a' characters - press key 1 twice"""
        sol = Solution()
        result = sol.stringSequence("aa")
        assert result == ["", "a", "aa"]

    def test_two_diff_chars_ab(self):
        """Two different chars - key 1 then key 2"""
        sol = Solution()
        result = sol.stringSequence("ab")
        assert result == ["", "a", "b"]

    def test_two_diff_chars_ba(self):
        """ba - key 1, key 2, key 1"""
        sol = Solution()
        result = sol.stringSequence("ba")
        assert result == ["", "a", "b", "ba"]

    def test_three_chars_abc(self):
        """abc - key 1, key 2, key 2"""
        sol = Solution()
        result = sol.stringSequence("abc")
        assert result == ["", "a", "b", "c"]

    def test_three_chars_aba(self):
        """aba - key 1, key 2, key 1, key 2"""
        sol = Solution()
        result = sol.stringSequence("aba")
        assert result == ["", "a", "b", "ba", "aba"]

    def test_three_chars_bba(self):
        """bba - key 1, key 2, key 1, key 2"""
        sol = Solution()
        result = sol.stringSequence("bba")
        assert result == ["", "a", "b", "ba", "bba"]

    def test_empty_string(self):
        """Empty string - just empty"""
        sol = Solution()
        result = sol.stringSequence("")
        assert result == [""]

    def test_repeated_char_ccc(self):
        """ccc - key 1, key 2, key 2"""
        sol = Solution()
        result = sol.stringSequence("ccc")
        assert result == ["", "a", "b", "c"]

    def test_repeated_char_ccc_ccc(self):
        """ccccc - key 1, key 2, key 2, key 1, key 2, key 2"""
        sol = Solution()
        result = sol.stringSequence("ccccc")
        assert result == ["", "a", "b", "c", "cc", "ccc", "cccc", "ccccc"]

    def test_wrap_around_z(self):
        """z - wraps around from y to z"""
        sol = Solution()
        result = sol.stringSequence("z")
        assert len(result) == 26
        assert result[0] == ""
        assert result[25] == "z"

    def test_z_to_a(self):
        """za - key 1, key 2 x 25, key 1"""
        sol = Solution()
        result = sol.stringSequence("za")
        assert result[0] == ""
        assert result[1] == "a"
        assert result[25] == "z"
        assert result[26] == "za"

    def test_abcabc(self):
        """abcabc - key 1, key 2, key 2, key 1, key 2, key 2"""
        sol = Solution()
        result = sol.stringSequence("abcabc")
        assert result == ["", "a", "b", "c", "ab", "abc", "abca", "abcab", "abcabc"]

    def test_bbb(self):
        """bbb - key 1, key 2, key 2, key 1, key 2, key 2"""
        sol = Solution()
        result = sol.stringSequence("bbb")
        assert result == ["", "a", "b", "bb", "bbb"]

    def test_aabb(self):
        """aabb - key 1, key 1, key 2, key 2"""
        sol = Solution()
        result = sol.stringSequence("aabb")
        assert result == ["", "a", "aa", "aab", "aabb"]

    def test_bbbbbb(self):
        """6 b's"""
        sol = Solution()
        result = sol.stringSequence("bbbbbb")
        assert result == ["", "a", "b", "bb", "bbb", "bbbb", "bbbbb", "bbbbbb"]

    def test_abcde(self):
        """abcde - 4 key 2 presses after key 1"""
        sol = Solution()
        result = sol.stringSequence("abcde")
        assert result == ["", "a", "b", "c", "d", "e"]

    def test_longer_string(self):
        """Longer string with mixed chars"""
        sol = Solution()
        result = sol.stringSequence("ababab")
        assert result == ["", "a", "b", "ba", "ab", "aba", "abab", "ababa", "ababab"]
