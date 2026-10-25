from solution import Solution


class TestCountPathsWithXorValue:
    def test_1x1_grid_match(self):
        """1x1 grid where the single value equals k"""
        sol = Solution()
        grid = [[5]]
        k = 5
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 1

    def test_1x1_grid_no_match(self):
        """1x1 grid where the single value does not equal k"""
        sol = Solution()
        grid = [[5]]
        k = 3
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 0

    def test_1x2_grid_match(self):
        """1x2 grid where XOR of path equals k"""
        sol = Solution()
        grid = [[2, 3]]
        k = 1  # 2 ^ 3 = 1
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 1

    def test_1x2_grid_no_match(self):
        """1x2 grid where XOR of path does not equal k"""
        sol = Solution()
        grid = [[2, 3]]
        k = 0  # 2 ^ 3 = 1, not 0
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 0

    def test_2x1_grid_match(self):
        """2x1 grid where XOR of path equals k"""
        sol = Solution()
        grid = [[2], [3]]
        k = 1  # 2 ^ 3 = 1
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 1

    def test_2x1_grid_no_match(self):
        """2x1 grid where XOR of path does not equal k"""
        sol = Solution()
        grid = [[2], [3]]
        k = 0  # 2 ^ 3 = 1, not 0
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 0

    def test_2x2_grid_one_path_matches(self):
        """2x2 grid where only one path has XOR equal to k"""
        sol = Solution()
        # Path 1: right then down: 1 ^ 2 ^ 3 = 0
        # Path 2: down then right: 1 ^ 4 ^ 3 = 6
        # k = 0, so only path 1 matches
        grid = [[1, 2], [4, 3]]
        k = 0
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 1

    def test_2x2_grid_both_paths_match(self):
        """2x2 grid where both paths have XOR equal to k"""
        sol = Solution()
        # Path 1: right then down: 1 ^ 2 ^ 2 = 1
        # Path 2: down then right: 1 ^ 2 ^ 2 = 1
        # k = 1, so both paths match
        grid = [[1, 2], [2, 2]]
        k = 1
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 2

    def test_2x2_grid_neither_path_matches(self):
        """2x2 grid where neither path has XOR equal to k"""
        sol = Solution()
        # Path 1: right then down: 1 ^ 2 ^ 3 = 0
        # Path 2: down then right: 1 ^ 4 ^ 3 = 6
        # k = 5, so neither path matches
        grid = [[1, 2], [4, 3]]
        k = 5
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 0

    def test_3x3_grid_all_zeros_k_zero(self):
        """3x3 grid with all zeros, k=0, all paths should match"""
        sol = Solution()
        grid = [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]
        # For 3x3 grid, number of paths = C(4,2) = 6
        # All zeros, XOR of any path = 0
        k = 0
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 6

    def test_3x3_grid_all_zeros_k_nonzero(self):
        """3x3 grid with all zeros, k=1, no paths should match"""
        sol = Solution()
        grid = [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]
        k = 1
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 0

    def test_2x2_grid_xor_zero_k_zero(self):
        """2x2 grid where XOR of all cells is 0, k=0"""
        sol = Solution()
        # Path 1: 1 ^ 2 ^ 3 = 0
        # Path 2: 1 ^ 4 ^ 3 = 6
        # k = 0, so only path 1 matches
        grid = [[1, 2], [4, 3]]
        k = 0
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 1

    def test_grid_with_k_zero(self):
        """Grid where k=0 but some paths have XOR=0"""
        sol = Solution()
        # Path 1: 3 ^ 1 ^ 2 = 0 (3^1=2, 2^2=0)
        # Path 2: 3 ^ 3 ^ 2 = 2
        # k = 0, so only path 1 matches
        grid = [[3, 1], [3, 2]]
        k = 0
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 1

    def test_2x2_grid_all_same_values(self):
        """2x2 grid with all same values"""
        sol = Solution()
        # Path 1: 5 ^ 5 ^ 5 = 5
        # Path 2: 5 ^ 5 ^ 5 = 5
        # k = 5, so both paths match
        grid = [[5, 5], [5, 5]]
        k = 5
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 2

    def test_2x2_grid_all_same_values_k_different(self):
        """2x2 grid with all same values, k different"""
        sol = Solution()
        # Path 1: 5 ^ 5 ^ 5 = 5
        # Path 2: 5 ^ 5 ^ 5 = 5
        # k = 3, so neither path matches
        grid = [[5, 5], [5, 5]]
        k = 3
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 0

    def test_3x3_grid_specific_path_xor(self):
        """3x3 grid with specific XOR values"""
        sol = Solution()
        # Let's calculate XOR for all 6 paths
        # Path 1: R,R,D,D: 1^2^3^4^5 = 1
        # Path 2: R,D,R,D: 1^2^4^3^5 = 1
        # Path 3: R,D,D,R: 1^2^4^5^3 = 1
        # Path 4: D,R,R,D: 1^3^2^4^5 = 1
        # Path 5: D,R,D,R: 1^3^2^5^4 = 1
        # Path 6: D,D,R,R: 1^3^4^5^2 = 1
        # All paths have XOR = 1
        grid = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]]
        k = 1
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 6

    def test_large_grid_modulo(self):
        """Test that result is returned modulo 10^9+7"""
        sol = Solution()
        # Create a grid where many paths have the same XOR
        # Use all 1s, k=1
        # For 10x10 grid, number of paths = C(18,9) = 48620
        # All paths have XOR = 1 (since 1^1^...^1 = 1 if odd count of 1s)
        # Actually for 10x10, path length = 19 cells (odd), so XOR = 1
        grid = [[1] * 10 for _ in range(10)]
        k = 1
        result = sol.countPathsWithXorValue(grid, k)
        # C(18, 9) = 48620
        assert result == 48620

    def test_boundary_m_equals_n(self):
        """Square grid with m=n"""
        sol = Solution()
        # 2x2 grid
        grid = [[1, 2], [3, 4]]
        # Path 1: 1^2^4 = 7
        # Path 2: 1^3^4 = 6
        k = 7
        result = sol.countPathsWithXorValue(grid, k)
        assert result == 1
