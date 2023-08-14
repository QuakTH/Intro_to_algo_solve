import math
from typing import Any, Dict, Optional, Tuple, Union

from intro_to_algo_solve.lecture16.dijkstra import relax
from intro_to_algo_solve.lecture16.weighted_graph import WeightedGraph


def do_bellman_ford(
    graph: WeightedGraph, start_node: Any
) -> Tuple[Dict[Any, Union[int, float]], Dict[Any, Optional[Any]]]:
    assert start_node in graph.vertices, "The start node is not in the graph."

    min_weight_infos = {vertex: math.inf for vertex in graph.vertices}
    min_weight_infos[start_node] = 0

    before_node_infos = {vertex: None for vertex in graph.vertices}

    vertices_count = len(graph.vertices)
    for _ in range(vertices_count - 1):
        for from_node, to_node in graph.edge_weight_infos:
            relax(
                from_node,
                to_node,
                min_weight_infos,
                graph.edge_weight_infos,
                before_node_infos,
            )

    for (from_node, to_node), weight in graph.edge_weight_infos.items():
        assert (
            min_weight_infos[to_node] <= min_weight_infos[from_node] + weight
        ), "There is a negative weight cycle in the graph."

    return min_weight_infos, before_node_infos
