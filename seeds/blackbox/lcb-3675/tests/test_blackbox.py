from typing import List
from solution import Solution


class TestMaximizeSumOfWeights:
    """Tests for maximizeSumOfWeights function."""

    def test_two_nodes_one_edge(self):
        """Test with minimum nodes: 2 nodes, 1 edge, k=1."""
        solution = Solution()
        edges = [[0, 1, 10]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        assert result == 10

    def test_two_nodes_k_greater_than_one(self):
        """Test with 2 nodes, k=2 (can keep all edges)."""
        solution = Solution()
        edges = [[0, 1, 10]]
        k = 2
        result = solution.maximizeSumOfWeights(edges, k)
        assert result == 10

    def test_line_graph_three_nodes(self):
        """Test line graph: 0-1-2, edges (0,1)=10, (1,2)=5, k=1."""
        solution = Solution()
        edges = [[0, 1, 10], [1, 2, 5]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        # Best: keep (0,1) with weight 10, or keep (1,2) with weight 5
        # But we can only keep one edge per node with k=1
        # Keep (0,1): node 0 has degree 1, node 1 has degree 1, node 2 has degree 0
        # Keep (1,2): node 0 has degree 0, node 1 has degree 1, node 2 has degree 1
        # Both valid, max is 10
        assert result == 10

    def test_line_graph_with_k_2(self):
        """Test line graph with k=2."""
        solution = Solution()
        edges = [[0, 1, 10], [1, 2, 5]]
        k = 2
        result = solution.maximizeSumOfWeights(edges, k)
        # Can keep both edges
        assert result == 15

    def test_star_graph_center_weighty(self):
        """Test star graph with heavy edges from center."""
        solution = Solution()
        # Center node 0 connected to nodes 1, 2, 3 with weights 10, 5, 3
        edges = [[0, 1, 10], [0, 2, 5], [0, 3, 3]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        # Can only keep 1 edge from center (k=1), keep heaviest
        assert result == 10

    def test_star_graph_center_k_2(self):
        """Test star graph with k=2."""
        solution = Solution()
        edges = [[0, 1, 10], [0, 2, 5], [0, 3, 3]]
        k = 2
        result = solution.maximizeSumOfWeights(edges, k)
        # Can keep 2 edges from center
        assert result == 15

    def test_star_graph_center_k_3(self):
        """Test star graph with k=3 (can keep all)."""
        solution = Solution()
        edges = [[0, 1, 10], [0, 2, 5], [0, 3, 3]]
        k = 3
        result = solution.maximizeSumOfWeights(edges, k)
        # Can keep all edges
        assert result == 18

    def test_line_graph_alternating_weights(self):
        """Test line graph with alternating weights, k=1."""
        solution = Solution()
        # 0-1-2-3 with weights 10, 5, 3
        edges = [[0, 1, 10], [1, 2, 5], [2, 3, 3]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        # Best: keep (0,1) and (2,3), total = 13
        assert result == 13

    def test_heavy_edges_at_leaves(self):
        """Test with heavy edges at leaves, k=1."""
        solution = Solution()
        # 0-1-2-3 with weights 3, 5, 10
        edges = [[0, 1, 3], [1, 2, 5], [2, 3, 10]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        # Best: keep (1,2) and (2,3) - but node 2 would have degree 2
        # Actually: keep (2,3)=10, node 2 has degree 1, node 3 has degree 1
        # Or keep (0,1)=3 and (1,2)=5, node 1 has degree 2 - invalid
        # Best: keep (2,3)=10 only, or (1,2)=5 only, or (0,1)=3 only
        # Wait, let me think again...
        # If we keep (2,3): node 2 has degree 1, node 3 has degree 1, node 1 has degree 0, node 0 has degree 0
        # Total = 10
        # If we keep (1,2): node 1 has degree 1, node 2 has degree 1, node 0 has degree 0, node 3 has degree 0
        # Total = 5
        # If we keep (0,1): node 0 has degree 1, node 1 has degree 1, node 2 has degree 0, node 3 has degree 0
        # Total = 3
        # Best is 10
        assert result == 10

    def test_heavy_edges_at_leaves_k_2(self):
        """Test with heavy edges at leaves, k=2."""
        solution = Solution()
        edges = [[0, 1, 3], [1, 2, 5], [2, 3, 10]]
        k = 2
        result = solution.maximizeSumOfWeights(edges, k)
        # Can keep all edges
        assert result == 18

    def test_disconnected_heavy_edges(self):
        """Test where keeping non-adjacent edges is better."""
        solution = Solution()
        # 0-1-2-3-4 with weights 100, 1, 1, 100
        edges = [[0, 1, 100], [1, 2, 1], [2, 3, 1], [3, 4, 100]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        # Best: keep (0,1) and (3,4), total = 200
        # Node 1 has degree 1, node 2 has degree 0, node 3 has degree 1
        assert result == 200

    def test_large_k_all_edges_kept(self):
        """Test with k >= n-1, all edges should be kept."""
        solution = Solution()
        edges = [[0, 1, 10], [1, 2, 20], [2, 3, 30]]
        k = 3  # n=4, k=3 >= n-1=3
        result = solution.maximizeSumOfWeights(edges, k)
        assert result == 60

    def test_single_edge_weight_1(self):
        """Test with minimum weight edge."""
        solution = Solution()
        edges = [[0, 1, 1]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        assert result == 1

    def test_single_edge_weight_max(self):
        """Test with maximum weight edge."""
        solution = Solution()
        edges = [[0, 1, 1000000]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        assert result == 1000000

    def test_complex_tree(self):
        """Test with a more complex tree structure."""
        solution = Solution()
        # Tree: 0 is root, children 1, 2
        # Node 1 has children 3, 4
        # Node 2 has child 5
        # Edges: (0,1)=10, (0,2)=8, (1,3)=5, (1,4)=3, (2,5)=7
        edges = [[0, 1, 10], [0, 2, 8], [1, 3, 5], [1, 4, 3], [2, 5, 7]]
        k = 2
        result = solution.maximizeSumOfWeights(edges, k)
        # Node 0: can keep 2 edges, keep (0,1)=10 and (0,2)=8, total so far = 18
        # Node 1: can keep 2 edges, keep (1,3)=5 and (1,4)=3, total so far = 18 + 8 = 26
        # Node 2: can keep 2 edges, keep (2,5)=7, total so far = 26 + 7 = 33
        # All nodes have degree <= 2
        assert result == 33

    def test_complex_tree_k_1(self):
        """Test with k=1 on complex tree."""
        solution = Solution()
        edges = [[0, 1, 10], [0, 2, 8], [1, 3, 5], [1, 4, 3], [2, 5, 7]]
        k = 1
        result = solution.maximizeSumOfWeights(edges, k)
        # With k=1, each node can have at most 1 edge
        # This is tricky - we need to select a matching
        # Best: (0,1)=10, (2,5)=7, total = 17
        # Or: (0,2)=8, (1,3)=5, (1,4)=3 - but node 1 would have degree 2
        # Or: (0,1)=10, (1,3)=5 - but node 1 would have degree 2
        # Best seems to be 17
        assert result == 17

