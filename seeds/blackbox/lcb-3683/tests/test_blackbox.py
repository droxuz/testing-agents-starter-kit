from solution import Solution


class TestAnswerString:
    def test_single_friend_entire_word(self):
        """When numFriends=1, the only split is the entire word."""
        sol = Solution()
        assert sol.answerString("abc", 1) == "abc"

    def test_three_chars_two_friends(self):
        """For 'abc' with 2 friends, max substring length is 2.
        Substrings: 'a', 'b', 'c', 'ab', 'bc'. Lexicographically largest is 'c'."""
        sol = Solution()
        assert sol.answerString("abc", 2) == "c"

    def test_three_chars_three_friends(self):
        """For 'abc' with 3 friends, each char is separate.
        Max substring length is 1. Substrings: 'a', 'b', 'c'. Largest is 'c'."""
        sol = Solution()
        assert sol.answerString("abc", 3) == "c"

    def test_five_chars_two_friends(self):
        """For 'abcde' with 2 friends, max substring length is 4.
        'e' is lexicographically largest single char."""
        sol = Solution()
        assert sol.answerString("abcde", 2) == "e"

    def test_five_chars_three_friends(self):
        """For 'abcde' with 3 friends, max substring length is 3.
        'e' is still the largest."""
        sol = Solution()
        assert sol.answerString("abcde", 3) == "e"

    def test_cba_two_friends(self):
        """For 'cba' with 2 friends, max substring length is 2.
        Substrings: 'c', 'b', 'a', 'cb', 'ba'. 'cb' > 'ba' > 'c' > 'b' > 'a'."""
        sol = Solution()
        assert sol.answerString("cba", 2) == "cb"

    def test_ba_two_friends(self):
        """For 'ba' with 2 friends, max substring length is 1.
        Substrings: 'b', 'a'. Largest is 'b'."""
        sol = Solution()
        assert sol.answerString("ba", 2) == "b"

    def test_single_char_one_friend(self):
        """Single character with 1 friend."""
        sol = Solution()
        assert sol.answerString("a", 1) == "a"

    def test_all_same_chars(self):
        """For 'zzz' with 2 friends, max substring length is 2.
        Substrings: 'z', 'zz'. Largest is 'zz'."""
        sol = Solution()
        assert sol.answerString("zzz", 2) == "zz"

    def test_zyx_two_friends(self):
        """For 'zyx' with 2 friends, max substring length is 2.
        Substrings: 'z', 'y', 'x', 'zy', 'yx'. 'zy' is largest."""
        sol = Solution()
        assert sol.answerString("zyx", 2) == "zy"

    def test_word_length_equals_num_friends(self):
        """When word length equals numFriends, each character is separate."""
        sol = Solution()
        assert sol.answerString("abcd", 4) == "d"

    def test_hello_two_friends(self):
        """For 'hello' with 2 friends, max substring length is 4.
        'o' is lexicographically largest."""
        sol = Solution()
        assert sol.answerString("hello", 2) == "o"

    def test_abcd_two_friends(self):
        """For 'abcd' with 2 friends, max substring length is 3.
        Substrings: 'a', 'ab', 'abc', 'b', 'bc', 'bcd', 'c', 'cd', 'd'.
        'd' is largest."""
        sol = Solution()
        assert sol.answerString("abcd", 2) == "d"

    def test_abcd_three_friends(self):
        """For 'abcd' with 3 friends, max substring length is 2.
        Substrings: 'a', 'ab', 'b', 'bc', 'c', 'cd', 'd'.
        'd' is largest."""
        sol = Solution()
        assert sol.answerString("abcd", 3) == "d"
