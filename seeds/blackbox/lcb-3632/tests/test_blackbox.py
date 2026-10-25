from typing import List
from solution import Solution


class TestButtonWithLongestTime:
    def test_basic_three_events(self):
        """Test with 3 events where button 3 has longest time."""
        solution = Solution()
        events = [[1, 2], [2, 5], [3, 10]]
        # Button 1: 2, Button 2: 5-2=3, Button 3: 10-5=5
        # Longest is 5, return 3
        assert solution.buttonWithLongestTime(events) == 3

    def test_first_button_longest(self):
        """Test where the first button has the longest time."""
        solution = Solution()
        events = [[1, 10], [2, 15], [3, 20]]
        # Button 1: 10, Button 2: 5, Button 3: 5
        # Longest is 10, return 1
        assert solution.buttonWithLongestTime(events) == 1

    def test_tie_returns_smallest_index(self):
        """Test where multiple buttons have same longest time, return smallest index."""
        solution = Solution()
        events = [[1, 10], [2, 15], [3, 25]]
        # Button 1: 10, Button 2: 5, Button 3: 10
        # Both 1 and 3 have 10, return smallest index 1
        assert solution.buttonWithLongestTime(events) == 1

    def test_single_event(self):
        """Test with only one event."""
        solution = Solution()
        events = [[1, 5]]
        # Button 1: 5
        assert solution.buttonWithLongestTime(events) == 1

    def test_two_events_tie(self):
        """Test with 2 events where both have same time."""
        solution = Solution()
        events = [[1, 5], [2, 10]]
        # Button 1: 5, Button 2: 5
        # Both have 5, return smallest index 1
        assert solution.buttonWithLongestTime(events) == 1

    def test_longest_time_in_middle(self):
        """Test where the longest time is in the middle."""
        solution = Solution()
        events = [[1, 10], [2, 15], [3, 30], [4, 35]]
        # Button 1: 10, Button 2: 5, Button 3: 15, Button 4: 5
        # Longest is 15, return 3
        assert solution.buttonWithLongestTime(events) == 3

    def test_same_button_multiple_presses(self):
        """Test where the same button is pressed multiple times."""
        solution = Solution()
        events = [[1, 10], [2, 15], [1, 20], [3, 25]]
        # Button 1: 10, Button 2: 5, Button 1: 5, Button 3: 5
        # Longest is 10, return 1
        assert solution.buttonWithLongestTime(events) == 1

    def test_all_same_time(self):
        """Test where all buttons have the same push time."""
        solution = Solution()
        events = [[1, 5], [2, 10], [3, 15]]
        # Button 1: 5, Button 2: 5, Button 3: 5
        # All have 5, return smallest index 1
        assert solution.buttonWithLongestTime(events) == 1

    def test_larger_events(self):
        """Test with a larger number of events."""
        solution = Solution()
        events = [[1, 100], [2, 150], [3, 200], [4, 250], [5, 300]]
        # Button 1: 100, Button 2: 50, Button 3: 50, Button 4: 50, Button 5: 50
        # Longest is 100, return 1
        assert solution.buttonWithLongestTime(events) == 1

    def test_second_button_longest(self):
        """Test where the second button has the longest time."""
        solution = Solution()
        events = [[1, 10], [2, 100], [3, 110]]
        # Button 1: 10, Button 2: 90, Button 3: 10
        # Longest is 90, return 2
        assert solution.buttonWithLongestTime(events) == 2
