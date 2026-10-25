import pytest
from solution import Solution


class TestCountWinningSequences:
    """Tests for countWinningSequences function."""

    def test_single_f(self):
        """Single round with Alice summoning Fire Dragon."""
        sol = Solution()
        # Bob can choose W (wins) or E (loses). Only W gives Bob a point.
        assert sol.countWinningSequences("F") == 1

    def test_single_w(self):
        """Single round with Alice summoning Water Serpent."""
        sol = Solution()
        # Bob can choose F (loses) or E (wins). Only E gives Bob a point.
        assert sol.countWinningSequences("W") == 1

    def test_single_e(self):
        """Single round with Alice summoning Earth Golem."""
        sol = Solution()
        # Bob can choose F (wins) or W (loses). Only F gives Bob a point.
        assert sol.countWinningSequences("E") == 1

    def test_two_ff(self):
        """Two rounds, Alice summons F, F."""
        sol = Solution()
        # Valid Bob sequences: (W,E), (W,F), (E,F), (E,W)
        # (W,E): Bob=1, Alice=1 (tie)
        # (W,F): Bob=1, Alice=1 (tie)
        # (E,F): Bob=2, Alice=0 (Bob wins)
        # (E,W): Bob=1, Alice=1 (tie)
        assert sol.countWinningSequences("FF") == 1

    def test_two_ww(self):
        """Two rounds, Alice summons W, W."""
        sol = Solution()
        # Valid Bob sequences: (F,E), (F,W), (E,F), (E,W)
        # All give Bob <= 1, Alice >= 1 (no wins for Bob)
        assert sol.countWinningSequences("WW") == 0

    def test_two_ee(self):
        """Two rounds, Alice summons E, E."""
        sol = Solution()
        # Valid Bob sequences: (F,W), (F,E), (W,F), (W,E)
        # All give Bob <= 1, Alice >= 1 (no wins for Bob)
        assert sol.countWinningSequences("EE") == 0

    def test_two_fe(self):
        """Two rounds, Alice summons F, E."""
        sol = Solution()
        # Valid Bob sequences: (W,W), (W,F), (E,F), (E,W)
        # (W,W): Bob=2, Alice=0 (Bob wins)
        # (W,F): Bob=1, Alice=1 (tie)
        # (E,F): Bob=1, Alice=1 (tie)
        # (E,W): Bob=0, Alice=2 (Bob loses)
        assert sol.countWinningSequences("FE") == 1

    def test_two_ef(self):
        """Two rounds, Alice summons E, F."""
        sol = Solution()
        # Valid Bob sequences: (F,W), (F,E), (W,E), (W,F)
        # (F,W): Bob=2, Alice=0 (Bob wins)
        # (F,E): Bob=1, Alice=1 (tie)
        # (W,E): Bob=1, Alice=1 (tie)
        # (W,F): Bob=0, Alice=2 (Bob loses)
        assert sol.countWinningSequences("EF") == 1

    def test_three_few(self):
        """Three rounds, Alice summons F, E, W."""
        sol = Solution()
        # Valid Bob sequences (no consecutive same moves):
        # (W,F,E): Bob=3, Alice=0 (Bob wins)
        # (E,F,E): Bob=2, Alice=1 (Bob wins)
        # All others give Bob <= Alice
        assert sol.countWinningSequences("FEW") == 2

    def test_three_fwe(self):
        """Three rounds, Alice summons F, W, E."""
        sol = Solution()
        # Valid Bob sequences:
        # (E,W,F): Bob=2, Alice=1 (Bob wins)
        # (E,F,E): Bob=2, Alice=1 (Bob wins)
        # (W,F,E): Bob=2, Alice=1 (Bob wins)
        # All others give Bob <= Alice
        assert sol.countWinningSequences("FWE") == 3

    def test_three_fff(self):
        """Three rounds, Alice summons F, F, F."""
        sol = Solution()
        # Valid Bob sequences:
        # (W,E,F): Bob=2, Alice=1 (Bob wins)
        # (W,F,E): Bob=2, Alice=1 (Bob wins)
        # (E,F,W): Bob=2, Alice=1 (Bob wins)
        # (E,W,F): Bob=2, Alice=1 (Bob wins)
        assert sol.countWinningSequences("FFF") == 4

    def test_three_www(self):
        """Three rounds, Alice summons W, W, W."""
        sol = Solution()
        # Valid Bob sequences:
        # (F,E,W): Bob=1, Alice=2 (Bob loses)
        # (F,W,E): Bob=1, Alice=2 (Bob loses)
        # (E,W,F): Bob=1, Alice=2 (Bob loses)
        # (E,F,W): Bob=1, Alice=2 (Bob loses)
        assert sol.countWinningSequences("WWW") == 0

    def test_three_eee(self):
        """Three rounds, Alice summons E, E, E."""
        sol = Solution()
        # Valid Bob sequences:
        # (F,W,E): Bob=1, Alice=2 (Bob loses)
        # (F,E,W): Bob=1, Alice=2 (Bob loses)
        # (W,E,F): Bob=1, Alice=2 (Bob loses)
        # (W,F,E): Bob=1, Alice=2 (Bob loses)
        assert sol.countWinningSequences("EEE") == 0

    def test_four_ffff(self):
        """Four rounds, Alice summons F, F, F, F."""
        sol = Solution()
        # Valid Bob sequences that give Bob > Alice:
        # (W,E,F,W): Bob=3, Alice=1 (Bob wins)
        # (W,F,E,W): Bob=3, Alice=1 (Bob wins)
        # (E,F,W,E): Bob=3, Alice=1 (Bob wins)
        # (E,W,F,E): Bob=3, Alice=1 (Bob wins)
        assert sol.countWinningSequences("FFFF") == 4

    def test_four_wwww(self):
        """Four rounds, Alice summons W, W, W, W."""
        sol = Solution()
        # All valid Bob sequences give Bob <= 2, Alice >= 2
        assert sol.countWinningSequences("WWWW") == 0

    def test_four_eeee(self):
        """Four rounds, Alice summons E, E, E, E."""
        sol = Solution()
        # All valid Bob sequences give Bob <= 2, Alice >= 2
        assert sol.countWinningSequences("EEEE") == 0

    def test_alternating_fw(self):
        """Alternating F, W, F, W..."""
        sol = Solution()
        # s = "FW"
        # Valid Bob sequences: (E,W), (E,F), (W,E), (W,F)
        # (E,W): Bob=2, Alice=0 (Bob wins)
        # (E,F): Bob=1, Alice=1 (tie)
        # (W,E): Bob=1, Alice=1 (tie)
        # (W,F): Bob=0, Alice=2 (Bob loses)
        assert sol.countWinningSequences("FW") == 1
