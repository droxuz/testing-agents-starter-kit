from solution import Solution


class TestNumberOfWays:
    def test_minimal_values(self):
        """Test with minimum boundary values."""
        sol = Solution()
        # n=1 performer, x=1 stage, y=1 score
        # 1^1 * 1^1 = 1
        assert sol.numberOfWays(1, 1, 1) == 1

    def test_one_performer_two_stages(self):
        """Test with one performer and two stages."""
        sol = Solution()
        # n=1, x=2, y=1
        # 2^1 * 1^2 = 2
        assert sol.numberOfWays(1, 2, 1) == 2

    def test_one_performer_two_scores(self):
        """Test with one performer and two score options."""
        sol = Solution()
        # n=1, x=1, y=2
        # 1^1 * 2^1 = 2
        assert sol.numberOfWays(1, 1, 2) == 2

    def test_two_performers_one_stage(self):
        """Test with two performers and one stage."""
        sol = Solution()
        # n=2, x=1, y=1
        # 1^2 * 1^1 = 1
        assert sol.numberOfWays(2, 1, 1) == 1

    def test_two_performers_two_stages_one_score(self):
        """Test with two performers, two stages, one score option."""
        sol = Solution()
        # n=2, x=2, y=1
        # 2^2 * 1^2 = 4
        assert sol.numberOfWays(2, 2, 1) == 4

    def test_two_performers_one_stage_two_scores(self):
        """Test with two performers, one stage, two score options."""
        sol = Solution()
        # n=2, x=1, y=2
        # 1^2 * 2^1 = 2
        assert sol.numberOfWays(2, 1, 2) == 2

    def test_two_performers_two_stages_two_scores(self):
        """Test with two performers, two stages, two score options."""
        sol = Solution()
        # n=2, x=2, y=2
        # 2^2 * 2^2 = 16
        assert sol.numberOfWays(2, 2, 2) == 16

    def test_three_performers_two_stages_two_scores(self):
        """Test with three performers, two stages, two scores."""
        sol = Solution()
        # n=3, x=2, y=2
        # 2^3 * 2^2 = 8 * 4 = 32
        assert sol.numberOfWays(3, 2, 2) == 32

    def test_three_performers_three_stages_three_scores(self):
        """Test with three performers, three stages, three scores."""
        sol = Solution()
        # n=3, x=3, y=3
        # 3^3 * 3^3 = 27 * 27 = 729
        assert sol.numberOfWays(3, 3, 3) == 729

    def test_large_values_modulo(self):
        """Test with larger values to verify modulo arithmetic."""
        sol = Solution()
        # n=10, x=10, y=10
        # 10^10 * 10^10 = 10^20, modulo 10^9+7
        expected = pow(10, 10, 10**9 + 7) * pow(10, 10, 10**9 + 7) % (10**9 + 7)
        assert sol.numberOfWays(10, 10, 10) == expected

    def test_large_n(self):
        """Test with large n value."""
        sol = Solution()
        # n=1000, x=1, y=1
        # 1^1000 * 1^1 = 1
        assert sol.numberOfWays(1000, 1, 1) == 1

    def test_large_x(self):
        """Test with large x value."""
        sol = Solution()
        # n=1, x=1000, y=1
        # 1000^1 * 1^1000 = 1000
        assert sol.numberOfWays(1, 1000, 1) == 1000

    def test_large_y(self):
        """Test with large y value."""
        sol = Solution()
        # n=1, x=1, y=1000
        # 1^1 * 1000^1 = 1000
        assert sol.numberOfWays(1, 1, 1000) == 1000

    def test_all_large(self):
        """Test with all large values."""
        sol = Solution()
        # n=1000, x=1000, y=1000
        # 1000^1000 * 1000^1000, modulo 10^9+7
        expected = pow(1000, 1000, 10**9 + 7) * pow(1000, 1000, 10**9 + 7) % (10**9 + 7)
        assert sol.numberOfWays(1000, 1000, 1000) == expected
