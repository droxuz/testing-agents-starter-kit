from solution import Solution


class TestCanAliceWin:
    """Tests for the stone removal game."""

    def test_alice_cannot_make_first_move(self):
        """Alice loses when n < 10 (cannot remove 10 stones on first turn)."""
        sol = Solution()
        assert sol.canAliceWin(1) is False
        assert sol.canAliceWin(5) is False
        assert sol.canAliceWin(9) is False

    def test_alice_wins_on_first_move(self):
        """Alice wins when 10 <= n < 19 (Alice removes 10, Bob cannot remove 9)."""
        sol = Solution()
        assert sol.canAliceWin(10) is True
        assert sol.canAliceWin(15) is True
        assert sol.canAliceWin(18) is True

    def test_alice_loses_on_second_move(self):
        """Alice loses when 19 <= n < 27 (Alice removes 10, Bob removes 9, Alice cannot remove 8)."""
        sol = Solution()
        assert sol.canAliceWin(19) is False
        assert sol.canAliceWin(20) is False
        assert sol.canAliceWin(26) is False

    def test_alice_wins_on_second_move(self):
        """Alice wins when 27 <= n < 34 (Alice removes 10+8, Bob cannot remove 7)."""
        sol = Solution()
        assert sol.canAliceWin(27) is True
        assert sol.canAliceWin(30) is True
        assert sol.canAliceWin(33) is True

    def test_alice_loses_on_third_move(self):
        """Alice loses when 34 <= n < 40 (Alice removes 10+8+6, Bob removes 7, Alice cannot remove 4)."""
        sol = Solution()
        assert sol.canAliceWin(34) is False
        assert sol.canAliceWin(35) is False
        assert sol.canAliceWin(39) is False

    def test_alice_wins_on_third_move(self):
        """Alice wins when 40 <= n < 45 (Alice removes 10+8+6+4, Bob cannot remove 5)."""
        sol = Solution()
        assert sol.canAliceWin(40) is True
        assert sol.canAliceWin(42) is True
        assert sol.canAliceWin(44) is True

    def test_alice_loses_on_fourth_move(self):
        """Alice loses when 45 <= n < 49 (Alice removes 10+8+6+4+2, Bob removes 5, Alice cannot remove 3)."""
        sol = Solution()
        assert sol.canAliceWin(45) is False
        assert sol.canAliceWin(46) is False
        assert sol.canAliceWin(48) is False

    def test_alice_wins_on_fourth_move(self):
        """Alice wins when 49 <= n <= 50 (Alice removes 10+8+6+4+2, Bob cannot remove 5)."""
        sol = Solution()
        assert sol.canAliceWin(49) is True
        assert sol.canAliceWin(50) is True

    def test_boundary_values(self):
        """Test all boundary values."""
        sol = Solution()
        # n = 1 to 9: False
        for n in range(1, 10):
            assert sol.canAliceWin(n) is False
        # n = 10 to 18: True
        for n in range(10, 19):
            assert sol.canAliceWin(n) is True
        # n = 19 to 26: False
        for n in range(19, 27):
            assert sol.canAliceWin(n) is False
        # n = 27 to 33: True
        for n in range(27, 34):
            assert sol.canAliceWin(n) is True
        # n = 34 to 39: False
        for n in range(34, 40):
            assert sol.canAliceWin(n) is False
        # n = 40 to 44: True
        for n in range(40, 45):
            assert sol.canAliceWin(n) is True
        # n = 45 to 48: False
        for n in range(45, 49):
            assert sol.canAliceWin(n) is False
        # n = 49 to 50: True
        for n in range(49, 51):
            assert sol.canAliceWin(n) is True
