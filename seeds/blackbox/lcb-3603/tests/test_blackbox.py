from solution import Solution


class TestSolution:
    def test_single_node(self):
        """Test with a single node tree."""
        sol = Solution()
        parent = [-1]
        s = "a"
        result = sol.findAnswer(parent, s)
        # dfs(0): no children, add 'a', dfsStr = "a", which is a palindrome
        assert result == [True]

    def test_two_nodes_line(self):
        """Test with 0 -> 1."""
        sol = Solution()
        parent = [-1, 0]
        s = "ab"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) adds 'b', then adds 'a' -> "ba", not a palindrome
        # dfs(1): adds 'b' -> "b", which is a palindrome
        assert result == [False, True]

    def test_two_nodes_same_chars(self):
        """Test with 0 -> 1 and same characters."""
        sol = Solution()
        parent = [-1, 0]
        s = "aa"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) adds 'a', then adds 'a' -> "aa", palindrome
        # dfs(1): adds 'a' -> "a", palindrome
        assert result == [True, True]

    def test_three_nodes_line(self):
        """Test with 0 -> 1 -> 2."""
        sol = Solution()
        parent = [-1, 0, 1]
        s = "abc"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) -> dfs(2) adds 'c', then adds 'b', then adds 'a' -> "cba", not palindrome
        # dfs(1): dfs(2) adds 'c', then adds 'b' -> "cb", not palindrome
        # dfs(2): adds 'c' -> "c", palindrome
        assert result == [False, False, True]

    def test_three_nodes_line_palindrome(self):
        """Test with 0 -> 1 -> 2 and palindrome string."""
        sol = Solution()
        parent = [-1, 0, 1]
        s = "aba"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) -> dfs(2) adds 'a', then adds 'b', then adds 'a' -> "aba", palindrome
        # dfs(1): dfs(2) adds 'a', then adds 'b' -> "ab", not palindrome
        # dfs(2): adds 'a' -> "a", palindrome
        assert result == [True, False, True]

    def test_three_nodes_star(self):
        """Test with 0 -> 1, 0 -> 2."""
        sol = Solution()
        parent = [-1, 0, 0]
        s = "aaa"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) adds 'a', add 'a', dfs(2) adds 'a', add 'a' -> "aaaa", palindrome
        # dfs(1): adds 'a' -> "a", palindrome
        # dfs(2): adds 'a' -> "a", palindrome
        assert result == [True, True, True]

    def test_three_nodes_star_not_palindrome(self):
        """Test with 0 -> 1, 0 -> 2 and non-palindrome string."""
        sol = Solution()
        parent = [-1, 0, 0]
        s = "aba"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) adds 'a', add 'a', dfs(2) adds 'b', add 'a' -> "aaba", not palindrome
        # dfs(1): adds 'a' -> "a", palindrome
        # dfs(2): adds 'b' -> "b", palindrome
        assert result == [False, True, True]

    def test_four_nodes_star(self):
        """Test with 0 -> 1, 2, 3."""
        sol = Solution()
        parent = [-1, 0, 0, 0]
        s = "aaaa"
        result = sol.findAnswer(parent, s)
        # All single characters are palindromes, and combining them with same char works
        assert result == [True, True, True, True]

    def test_four_nodes_star_not_palindrome(self):
        """Test with 0 -> 1, 2, 3 and non-palindrome string."""
        sol = Solution()
        parent = [-1, 0, 0, 0]
        s = "abca"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) adds 'a', add 'b', dfs(2) adds 'c', add 'b', dfs(3) adds 'a', add 'a' -> "abcbaa", not palindrome
        # dfs(1): adds 'a' -> "a", palindrome
        # dfs(2): adds 'c' -> "c", palindrome
        # dfs(3): adds 'a' -> "a", palindrome
        assert result == [False, True, True, True]

    def test_four_nodes_line_palindrome(self):
        """Test with 0 -> 1 -> 2 -> 3 and palindrome string."""
        sol = Solution()
        parent = [-1, 0, 1, 2]
        s = "abba"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) -> dfs(2) -> dfs(3) adds 'a', add 'b', add 'b', add 'a' -> "abba", palindrome
        # dfs(1): dfs(2) -> dfs(3) adds 'a', add 'b' -> "ab", not palindrome
        # dfs(2): dfs(3) adds 'a', add 'b' -> "ab", not palindrome
        # dfs(3): adds 'a' -> "a", palindrome
        assert result == [True, False, False, True]

    def test_large_tree_all_same(self):
        """Test with larger tree where all characters are the same."""
        sol = Solution()
        parent = [-1] + list(range(1, 10))  # 0 -> 1 -> 2 -> ... -> 9
        s = "a" * 10
        result = sol.findAnswer(parent, s)
        # All strings will be "aaaa..." which are all palindromes
        assert all(result)

    def test_complex_tree(self):
        """Test with a more complex tree structure."""
        sol = Solution()
        # 0 -> 1, 0 -> 2, 1 -> 3, 1 -> 4
        parent = [-1, 0, 0, 1, 1]
        s = "abcde"
        result = sol.findAnswer(parent, s)
        # dfs(0): dfs(1) -> dfs(3) adds 'c', add 'd', dfs(4) adds 'e', add 'd' -> "cde d", add 'a' -> "cde da"
        # Let me trace more carefully:
        # dfs(3): add 'c' -> "c"
        # dfs(1): add 'd' -> "cd"
        # dfs(4): add 'e' -> "cde"
        # dfs(0): add 'a' -> "cdea"
        # "cdea" is not a palindrome
        # dfs(2): add 'b' -> "b", palindrome
        # dfs(3): add 'c' -> "c", palindrome
        # dfs(4): add 'd' -> "d", palindrome
        assert result == [False, False, True, True, True]
