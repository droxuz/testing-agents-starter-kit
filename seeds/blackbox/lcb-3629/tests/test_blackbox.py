import pytest
from solution import Solution


class TestLengthAfterTransformations:
    """Tests for lengthAfterTransformations function."""

    def test_empty_string_edge_case(self):
        """Test with empty string - should return 0."""
        solution = Solution()
        assert solution.lengthAfterTransformations("", 1) == 0

    def test_t_equals_zero_single_char(self):
        """Test with t=0 - no transformations, return original length."""
        solution = Solution()
        assert solution.lengthAfterTransformations("abc", 0) == 3

    def test_t_equals_zero_multi_char(self):
        """Test with t=0 for longer string."""
        solution = Solution()
        assert solution.lengthAfterTransformations("abcdefgh", 0) == 8

    def test_single_z_t_one(self):
        """Test 'z' transforms to 'ab' with t=1."""
        solution = Solution()
        assert solution.lengthAfterTransformations("z", 1) == 2

    def test_single_z_t_zero(self):
        """Test 'z' with t=0 stays as 'z'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("z", 0) == 1

    def test_single_a_t_one(self):
        """Test 'a' transforms to 'b' with t=1."""
        solution = Solution()
        assert solution.lengthAfterTransformations("a", 1) == 1

    def test_single_a_t_twenty_five(self):
        """Test 'a' reaches 'z' at t=25."""
        solution = Solution()
        assert solution.lengthAfterTransformations("a", 25) == 1

    def test_single_a_t_twenty_six(self):
        """Test 'a' transforms to 'ab' at t=26."""
        solution = Solution()
        assert solution.lengthAfterTransformations("a", 26) == 2

    def test_single_a_t_large(self):
        """Test 'a' with large t stays at length 2."""
        solution = Solution()
        assert solution.lengthAfterTransformations("a", 100000) == 2

    def test_single_a_t_very_large(self):
        """Test 'a' with very large t stays at length 2."""
        solution = Solution()
        assert solution.lengthAfterTransformations("a", 1000000000) == 2

    def test_single_z_t_large(self):
        """Test 'z' with large t stays at length 2."""
        solution = Solution()
        assert solution.lengthAfterTransformations("z", 100000) == 2

    def test_string_ab_t_one(self):
        """Test 'ab' with t=1: 'a'->'b', 'b'->'c'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("ab", 1) == 2

    def test_string_ab_t_twenty_five(self):
        """Test 'ab' with t=25: 'a'->'z', 'b'->'c'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("ab", 25) == 2

    def test_string_ab_t_twenty_six(self):
        """Test 'ab' with t=26: 'a'->'ab', 'b'->'c'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("ab", 26) == 3

    def test_string_ab_t_twenty_seven(self):
        """Test 'ab' with t=27: 'a'->'bc', 'b'->'cd'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("ab", 27) == 4

    def test_string_abc_t_twenty_five(self):
        """Test 'abc' with t=25: 'a'->'z', 'b'->'c', 'c'->'d'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("abc", 25) == 3

    def test_string_abc_t_twenty_six(self):
        """Test 'abc' with t=26: 'a'->'ab', 'b'->'cd', 'c'->'de'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("abc", 26) == 6

    def test_string_abc_t_twenty_seven(self):
        """Test 'abc' with t=27: all become length 2 strings."""
        solution = Solution()
        assert solution.lengthAfterTransformations("abc", 27) == 6

    def test_string_zz_t_one(self):
        """Test 'zz' with t=1: both become 'ab'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("zz", 1) == 4

    def test_string_zz_t_zero(self):
        """Test 'zz' with t=0."""
        solution = Solution()
        assert solution.lengthAfterTransformations("zz", 0) == 2

    def test_string_zy_t_one(self):
        """Test 'zy' with t=1: 'z'->'ab', 'y'->'z'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("zy", 1) == 3

    def test_string_zy_t_twenty_five(self):
        """Test 'zy' with t=25: 'z'->'ab', 'y'->'z'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("zy", 25) == 3

    def test_string_zy_t_twenty_six(self):
        """Test 'zy' with t=26: 'z'->'bc', 'y'->'ab'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("zy", 26) == 4

    def test_string_all_zs_t_one(self):
        """Test string of all 'z's with t=1."""
        solution = Solution()
        assert solution.lengthAfterTransformations("zzzz", 1) == 8

    def test_string_all_as_t_twenty_five(self):
        """Test string of all 'a's with t=25: all become 'z'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("aaaa", 25) == 4

    def test_string_all_as_t_twenty_six(self):
        """Test string of all 'a's with t=26: all become 'ab'."""
        solution = Solution()
        assert solution.lengthAfterTransformations("aaaa", 26) == 8

    def test_string_mixed_t_twenty_six(self):
        """Test mixed string with t=26."""
        solution = Solution()
        # 'a' -> 'ab' (2), 'b' -> 'cd' (2), 'z' -> 'bc' (2)
        assert solution.lengthAfterTransformations("abz", 26) == 6

    def test_modulo_result_large_t(self):
        """Test that result is modulo 10^9 + 7."""
        solution = Solution()
        # With t=10^5 and 'a', result should be 2 (already small)
        assert solution.lengthAfterTransformations("a", 100000) == 2

    def test_boundary_char_y_t_one(self):
        """Test 'y' transforms to 'z' with t=1."""
        solution = Solution()
        assert solution.lengthAfterTransformations("y", 1) == 1

    def test_boundary_char_y_t_two(self):
        """Test 'y' transforms to 'ab' with t=2."""
        solution = Solution()
        assert solution.lengthAfterTransformations("y", 2) == 2

    def test_boundary_char_x_t_one(self):
        """Test 'x' transforms to 'y' with t=1."""
        solution = Solution()
        assert solution.lengthAfterTransformations("x", 1) == 1

    def test_boundary_char_x_t_two(self):
        """Test 'x' transforms to 'z' with t=2."""
        solution = Solution()
        assert solution.lengthAfterTransformations("x", 2) == 1

    def test_boundary_char_x_t_three(self):
        """Test 'x' transforms to 'ab' with t=3."""
        solution = Solution()
        assert solution.lengthAfterTransformations("x", 3) == 2

    def test_single_char_max_length(self):
        """Test single character constraint."""
        solution = Solution()
        assert solution.lengthAfterTransformations("m", 1) == 1

    def test_single_char_max_length_t_large(self):
        """Test single character with large t."""
        solution = Solution()
        assert solution.lengthAfterTransformations("m", 100000) == 2
