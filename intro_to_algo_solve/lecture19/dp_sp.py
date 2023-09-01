import math
from typing import Any

from intro_to_algo_solve.data_structures.graph import Graph
from intro_to_algo_solve.lecture19.dp_dag_sp import ShortedPathResult


def dynamic_shortest_path(graph: Graph, s: Any) -> ShortedPathResult:
    """Find the shortest path of a graph even there is a cycle in the graph.

    :param graph: Graph to find the shortest path.
    :param s: Start node.
    :return: Search result.
    """

    def sp_recursion(
        graph: Graph, step: int, vertex: Any, search_result: ShortedPathResult
    ) -> int:
        """The function that actually does the search by recursion.

        :param graph: Graph to find the shortest path.
        :param step: Current step of the search.
        :param vertex: vertex to search the shortest path.
        :param search_result: Search result.
        :return: Shortest path weight from the start node to the `vertex`. In respect to `step`.
        """
        if (step, vertex) in search_result.shortest_path:
            return search_result.shortest_path[(step, vertex)]

        search_result.shortest_path[(step, vertex)] = math.inf
        search_result.before_node[(step, vertex)] = None
        for from_node in graph.inbound_vertices(vertex):
            calc_dist = (
                sp_recursion(graph, step - 1, from_node, search_result)
                + graph.edge_weight_infos[(from_node, vertex)]
            )
            if search_result.shortest_path[(step, vertex)] > calc_dist:
                search_result.shortest_path[(step, vertex)] = calc_dist
                search_result.before_node[(step, vertex)] = from_node
        return search_result.shortest_path[(step, vertex)]

    assert s in graph.vertices, "The start node is not in the graph vertices."
    assert graph.is_directed, "This search is for directed graphs."

    search_result = ShortedPathResult()
    num_vertices = len(graph.vertices)
    for step in range(num_vertices):
        search_result.shortest_path[(step, s)] = 0
        search_result.before_node[(step, s)] = None

    for vertex in graph.vertices:
        if vertex != s:
            search_result.shortest_path[(0, vertex)] = math.inf

    for vertex in graph.vertices:
        sp_recursion(graph, num_vertices - 1, vertex, search_result)

    final_shortest_path = {}
    final_before_node = {}
    for vertex in graph.vertices:
        final_shortest_path[vertex] = search_result.shortest_path[
            (num_vertices - 1, vertex)
        ]
        final_before_node[vertex] = search_result.before_node[
            (num_vertices - 1, vertex)
        ]
    search_result.shortest_path = final_shortest_path
    search_result.before_node = final_before_node

    return search_result
