from solution import Solution


class TestMaxRectangleArea:
    def test_no_rectangle_single_point(self):
        """Single point cannot form a rectangle"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0]]) == -1

    def test_no_rectangle_two_points(self):
        """Two points cannot form a rectangle"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [1, 1]]) == -1

    def test_no_rectangle_three_points(self):
        """Three points cannot form a rectangle"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [1, 0], [0, 1]]) == -1

    def test_minimal_rectangle_area_1(self):
        """Minimal 1x1 rectangle with no interior points"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [1, 0], [0, 1], [1, 1]]) == 1

    def test_larger_rectangle_area_4(self):
        """2x2 rectangle with no interior points"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2]]) == 4

    def test_point_inside_makes_invalid(self):
        """Rectangle with point inside is invalid"""
        solution = Solution()
        # Point [1,1] is inside the 2x2 rectangle
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2], [1, 1]]) == -1

    def test_point_on_border_makes_invalid(self):
        """Rectangle with point on border is invalid"""
        solution = Solution()
        # Point [1,0] is on the bottom edge
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2], [1, 0]]) == -1

    def test_point_on_top_border_makes_invalid(self):
        """Rectangle with point on top border is invalid"""
        solution = Solution()
        # Point [1,2] is on the top edge
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2], [1, 2]]) == -1

    def test_point_on_left_border_makes_invalid(self):
        """Rectangle with point on left border is invalid"""
        solution = Solution()
        # Point [0,1] is on the left edge
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2], [0, 1]]) == -1

    def test_point_on_right_border_makes_invalid(self):
        """Rectangle with point on right border is invalid"""
        solution = Solution()
        # Point [2,1] is on the right edge
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2], [2, 1]]) == -1

    def test_multiple_rectangles_max_area_1(self):
        """Two 1x1 rectangles, max area is 1"""
        solution = Solution()
        # Two separate 1x1 rectangles
        assert solution.maxRectangleArea([[0, 0], [1, 0], [0, 1], [1, 1], [2, 0], [3, 0], [2, 1], [3, 1]]) == 1

    def test_multiple_rectangles_max_area_4(self):
        """Two 2x2 rectangles, max area is 4"""
        solution = Solution()
        # Two separate 2x2 rectangles
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2], [1, 0], [3, 0], [1, 2], [3, 2]]) == 4

    def test_points_same_x_vertical_line(self):
        """Points on same vertical line cannot form rectangle"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [0, 1], [0, 2], [0, 3]]) == -1

    def test_points_same_y_horizontal_line(self):
        """Points on same horizontal line cannot form rectangle"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [1, 0], [2, 0], [3, 0]]) == -1

    def test_diagonal_points_no_rectangle(self):
        """Diagonal points cannot form axis-parallel rectangle"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [1, 1], [2, 2], [3, 3]]) == -1

    def test_rectangle_with_interior_point_on_edge(self):
        """Point on interior edge makes rectangle invalid"""
        solution = Solution()
        # Points at x=1, y=1 are on interior edges
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2], [1, 0], [1, 2], [0, 1], [2, 1]]) == -1

    def test_larger_rectangle_area_9(self):
        """3x3 rectangle with no interior points"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [3, 0], [0, 3], [3, 3]]) == 9

    def test_larger_rectangle_area_16(self):
        """4x4 rectangle with no interior points"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [4, 0], [0, 4], [4, 4]]) == 16

    def test_max_of_multiple_sizes(self):
        """Should return maximum of multiple valid rectangles"""
        solution = Solution()
        # One 2x2 rectangle and one 1x1 rectangle
        assert solution.maxRectangleArea([[0, 0], [2, 0], [0, 2], [2, 2], [3, 0], [4, 0], [3, 1], [4, 1]]) == 4

    def test_coordinates_at_boundary_zero(self):
        """Rectangle starting at origin"""
        solution = Solution()
        assert solution.maxRectangleArea([[0, 0], [1, 0], [0, 1], [1, 1]]) == 1

    def test_coordinates_at_boundary_100(self):
        """Rectangle at coordinates near 100"""
        solution = Solution()
        assert solution.maxRectangleArea([[99, 99], [100, 99], [99, 100], [100, 100]]) == 1

    def test_no_rectangle_four_points_not_rectangle(self):
        """Four points that don't form a rectangle"""
        solution = Solution()
        # Three points on one line, one off
        assert solution.maxRectangleArea([[0, 0], [1, 0], [2, 0], [0, 1]]) == -1

    def test_no_rectangle_only_two_x_coordinates(self):
        """Only two x coordinates but not forming rectangle"""
        solution = Solution()
        # Not enough y coordinates
        assert solution.maxRectangleArea([[0, 0], [1, 0], [0, 1], [1, 1], [0, 2]]) == -1

    def test_two_valid_rectangles_adjacent(self):
        """Two adjacent 1x1 rectangles"""
        solution = Solution()
        # [[0,0],[1,0],[0,1],[1,1]] and [[1,0],[2,0],[1,1],[2,1]]
        # They share an edge, but we can still find max area of 1
        assert solution.maxRectangleArea([[0, 0], [1, 0], [0, 1], [1, 1], [2, 0], [2, 1]]) == 1
