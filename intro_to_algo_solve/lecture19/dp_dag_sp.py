import math
from typing import Any

from intro_to_algo_solve.data_structures.graph import Graph
from intro_to_algo_solve.lecture14.dfs import depth_first_search


class ShortedPathResult:
    """Class containing dynamic programming shortest path searching of
    DAG(Directed Acyclic Graph)
    """

    def __init__(self) -> None:
        """Constructor for the `ShortedPathResult` instance."""
        self.shortest_path = (
            {}
        )  # Shortest path length when there is a start node `s` for each node.
        self.before_node = {}  # Before node of the node when the path is shortest.


def shortest_path_rec_mem(graph: Graph, s: Any) -> ShortedPathResult:
    """Find the shortest path of a DAG using recursion and memoization.

    :param graph: Graph to find the shortest path.
    :param s: Start node.
    :return: Search result.
    """

    def sp_recursion(
        graph: Graph, vertex: Any, search_result: ShortedPathResult
    ) -> int:
        """The function that actually does the search by recursion.

        :param graph: Graph to find the shortest path.
        :param vertex: vertex to search the shortest path.
        :param search_result: Search result.
        :return: Shortest path weight from the start node to the `vertex`.
        """
        if vertex in search_result.shortest_path:
            return search_result.shortest_path[vertex]

        search_result.shortest_path[vertex] = math.inf
        search_result.before_node[vertex] = None
        for from_node in graph.inbound_vertices(vertex):
            calc_dist = (
                sp_recursion(graph, from_node, search_result)
                + graph.edge_weight_infos[(from_node, vertex)]
            )
            if search_result.shortest_path[vertex] > calc_dist:
                search_result.shortest_path[vertex] = calc_dist
                search_result.before_node[vertex] = from_node
        return search_result.shortest_path[vertex]

    assert s in graph.vertices, "The start node is not in the graph vertices."
    assert graph.is_directed, "This search is for directed graphs."
    dps_result = depth_first_search(graph)
    assert dps_result.acyclic, "This search is not available for graph with cycles."

    search_result = ShortedPathResult()
    search_result.before_node[s] = None
    search_result.shortest_path[s] = 0

    for vertex in graph.vertices:
        sp_recursion(graph, vertex, search_result)

    return search_result


def shortest_path_bottom_up(graph: Graph, s: Any) -> ShortedPathResult:
    """Find the shortest path of a DAG using the bottom up method.

    :param graph: Graph to find the shortest path.
    :param s: Start node.
    :return: Search result.
    """
    assert s in graph.vertices, "The start node is not in the graph vertices."
    assert graph.is_directed, "This search is for directed graphs."
    dps_result = depth_first_search(graph)
    assert dps_result.acyclic, "This search is not available for graph with cycles."

    search_result = ShortedPathResult()
    for vertex in graph.vertices:
        search_result.shortest_path[vertex] = math.inf
        search_result.before_node[vertex] = None
    search_result.shortest_path[s] = 0

    for vertex in dps_result.topological_sorted:
        for neighbor in graph.neighbors[vertex]:
            calc_dist = (
                search_result.shortest_path[vertex]
                + graph.edge_weight_infos[(vertex, neighbor)]
            )
            if search_result.shortest_path[neighbor] > calc_dist:
                search_result.shortest_path[neighbor] = calc_dist
                search_result.before_node[neighbor] = vertex

    return search_result
