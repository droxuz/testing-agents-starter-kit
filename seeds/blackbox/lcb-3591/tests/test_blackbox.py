from typing import List
from solution import Solution


class TestShiftDistance:
    def test_basic_forward_shift(self):
        """Test forward shift where forward is cheaper"""
        sol = Solution()
        # s[0]='a', t[0]='c': forward 2 steps, backward 24 steps
        # forward: 2 * nextCost[0] = 2 * 1 = 2
        # backward: 24 * previousCost[0] = 24 * 100 = 2400
        # expected: 2
        result = sol.shiftDistance("a", "c", [1] + [0] * 25, [100] + [0] * 25)
        assert result == 2

    def test_basic_backward_shift(self):
        """Test backward shift where backward is cheaper"""
        sol = Solution()
        # s[0]='c', t[0]='a': forward 24 steps, backward 2 steps
        # forward: 24 * nextCost[2] = 24 * 100 = 2400
        # backward: 2 * previousCost[2] = 2 * 1 = 2
        # expected: 2
        cost = [0] * 26
        cost[2] = 100
        prev_cost = [0] * 26
        prev_cost[2] = 1
        result = sol.shiftDistance("c", "a", cost, prev_cost)
        assert result == 2

    def test_same_character(self):
        """Test when s and t have same character at each position"""
        sol = Solution()
        # No shift needed, cost is 0
        result = sol.shiftDistance("abc", "abc", [1] * 26, [1] * 26)
        assert result == 0

    def test_wraparound_z_to_a(self):
        """Test wraparound from z to a"""
        sol = Solution()
        # s[0]='z', t[0]='a': forward 1 step, backward 25 steps
        # forward: 1 * nextCost[25] = 1 * 1 = 1
        # backward: 25 * previousCost[25] = 25 * 100 = 2500
        # expected: 1
        cost = [0] * 26
        cost[25] = 1
        prev_cost = [0] * 26
        prev_cost[25] = 100
        result = sol.shiftDistance("z", "a", cost, prev_cost)
        assert result == 1

    def test_wraparound_a_to_z(self):
        """Test wraparound from a to z"""
        sol = Solution()
        # s[0]='a', t[0]='z': forward 25 steps, backward 1 step
        # forward: 25 * nextCost[0] = 25 * 100 = 2500
        # backward: 1 * previousCost[0] = 1 * 1 = 1
        # expected: 1
        cost = [0] * 26
        cost[0] = 100
        prev_cost = [0] * 26
        prev_cost[0] = 1
        result = sol.shiftDistance("a", "z", cost, prev_cost)
        assert result == 1

    def test_multiple_characters_forward(self):
        """Test multiple characters with forward shifts"""
        sol = Solution()
        # s[0]='a'->'c': 2 forward steps
        # s[1]='b'->'d': 2 forward steps
        # total: 2 * nextCost[0] + 2 * nextCost[1] = 2 * 1 + 2 * 2 = 6
        result = sol.shiftDistance("ab", "cd", [1, 2] + [0] * 24, [0] * 26)
        assert result == 6

    def test_mixed_forward_backward(self):
        """Test combination of forward and backward shifts"""
        sol = Solution()
        # s[0]='a'->'c': 2 forward steps = 2 * 1 = 2
        # s[1]='b'->'b': 0 steps = 0
        # s[2]='c'->'a': 2 backward steps = 2 * 1 = 2
        # total: 2 + 0 + 2 = 4
        result = sol.shiftDistance("abc", "cba", [1, 0, 1] + [0] * 23, [1, 0, 1] + [0] * 23)
        assert result == 4

    def test_large_costs(self):
        """Test with large cost values"""
        sol = Solution()
        # s[0]='a'->'z': forward 25 steps, backward 1 step
        # forward: 25 * 10^9
        # backward: 1 * 1 = 1
        # expected: 1 (backward is cheaper)
        cost = [10**9] + [0] * 25
        prev_cost = [1] + [0] * 25
        result = sol.shiftDistance("a", "z", cost, prev_cost)
        assert result == 1

    def test_all_same_forward(self):
        """Test all characters shift forward"""
        sol = Solution()
        # s[0]='a'->'d': 3 forward steps = 3 * 1 = 3
        result = sol.shiftDistance("a", "d", [1] + [0] * 25, [0] * 26)
        assert result == 3

    def test_all_same_backward(self):
        """Test all characters shift backward"""
        sol = Solution()
        # s[0]='d'->'a': 3 backward steps = 3 * 1 = 3
        result = sol.shiftDistance("d", "a", [0] * 26, [1] + [0] * 25)
        assert result == 3

    def test_equality_costs(self):
        """Test when forward and backward costs are equal"""
        sol = Solution()
        # s[0]='a'->'c': forward 2 steps, backward 24 steps
        # forward: 2 * 5 = 10
        # backward: 24 * 5 = 120
        # expected: 10 (forward is cheaper)
        cost = [5] + [0] * 25
        prev_cost = [5] + [0] * 25
        result = sol.shiftDistance("a", "c", cost, prev_cost)
        assert result == 10

    def test_single_char_string(self):
        """Test with single character strings"""
        sol = Solution()
        result = sol.shiftDistance("x", "y", [1] * 26, [1] * 26)
        # x->y: 1 forward step
        assert result == 1

    def test_longer_string(self):
        """Test with longer string"""
        sol = Solution()
        # s="abcde", t="bcdef"
        # a->b: 1 forward = 1
        # b->c: 1 forward = 1
        # c->d: 1 forward = 1
        # d->e: 1 forward = 1
        # e->f: 1 forward = 1
        # total: 5
        result = sol.shiftDistance("abcde", "bcdef", [1] * 26, [0] * 26)
        assert result == 5
