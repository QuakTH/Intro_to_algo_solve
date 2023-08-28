# Module for dijkstra algorithm


import math
from typing import Any, Dict, Optional, Set, Tuple, Union

from intro_to_algo_solve.data_structures.graph import Graph


def relax(
    from_node: Any,
    to_node: Any,
    min_weight_infos: Dict[Any, Union[int, float]],
    edge_weight_infos: Dict[Tuple[Any, Any], int],
    before_node_infos: Dict[Any, Any],
) -> None:
    """Update the `min_weight_infos` of `to_node` using the information from:
    1. Min dist information from `from_node`.
    2. Edge weight from `from_node` to `to_node`.
    If the original weight of the `to_node` is smaller than
    <weight of the `from_node`> + <edge weight of `from_node` to `to_node`>
    no update is made. else, there will be an update.

    Note that the `min_weight_infos` is a dictionary containing weights of nodes
    with respect to a start node.
    Meaning with different start nodes there will be different `min_weight_infos`.

    :param from_node: Node that has already found the minimum weight from the start node.
    :param to_node: Node that needs the minimum weight updated.
    :param min_weight_infos: Dictionary containing minimum weight from the start node.
    :param edge_weight_infos: Weight information of edges.
    :param before_node_infos: Dictionary containing before node
                              When the weight is currently minimum.
    """
    edge = (from_node, to_node)
    weight_added = min_weight_infos[from_node] + edge_weight_infos[edge]
    if min_weight_infos[to_node] > weight_added:
        min_weight_infos[to_node] = weight_added
        before_node_infos[to_node] = from_node


def get_from_node(
    min_weight_infos: Dict[Any, Union[int, float]], vertices_done: Set[Any]
) -> Any:
    """Return the from_node which will be used as a start point to do a `relax` process.
    When this function is called first, the start vertex will always be returned.

    :param min_weight_infos: Dictionary containing the minimum weight
                             information from the start vertex.
    :param vertices_done: Set containing vertices which has already been relaxed.
    :return: Vertex to be used as a from_node
    """
    priority_queue = sorted(min_weight_infos.items(), key=lambda item: item[1])
    filtered_queue = [
        vertex_weight[0]
        for vertex_weight in priority_queue
        if vertex_weight[0] not in vertices_done
    ]
    return filtered_queue[0]


def do_dijkstra(
    graph: Graph, start_node: Any
) -> Tuple[Dict[Any, Union[int, float]], Dict[Any, Optional[Any]]]:
    """Do a Dijkstra path finding on the weighted graph `graph`.
    Which start node is the `start_node`.

    :param graph: Graph to do dijkstra.
    :param start_node: Start node of the graph.
    :return: Tuple containing two elements which first value is the minimum sum of weights
             of edges from the `start_node` to each vertices. The second value contains the
             dictionary of before nodes of each end node when the sum of the weight is minimum.
    """
    assert start_node in graph.vertices, "The start node is not in the graph."
    assert all(
        weight >= 0 for weight in graph.edge_weight_infos.values()
    ), "Dijkstra can only be applied in with edges bigger than 0."

    min_weight_infos = {vertex: math.inf for vertex in graph.vertices}
    min_weight_infos[start_node] = 0

    before_node_infos = {vertex: None for vertex in graph.vertices}
    vertices_done = set()
    vertices_not_done = set(graph.vertices)

    while vertices_not_done:
        from_node = get_from_node(min_weight_infos, vertices_done)
        for neighbor in graph.neighbors[from_node]:
            relax(
                from_node,
                neighbor,
                min_weight_infos,
                graph.edge_weight_infos,
                before_node_infos,
            )
        vertices_done.add(from_node)
        vertices_not_done.remove(from_node)

    return min_weight_infos, before_node_infos
