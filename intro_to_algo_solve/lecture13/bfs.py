from typing import Any, Dict, Tuple
from intro_to_algo_solve.data_structures.graph import Graph


def breadth_first_search(
    graph: Graph, start_node: Any
) -> Tuple[Dict[Any, int], Dict[Any, Any]]:
    """Do a breadth-first-search for the `graph` starting from `start_node`.
    And return how many path does it takes to go to each vertex
    and each vertex's before vertex.

    :param graph: Graph to do bfs.
    :param start_node: Start node when doing bfs.
    :return: A tuple which first element is a dictionary of path count,
             and the second element is the dictionary of before node.
    """
    assert (
        start_node in graph.vertices
    ), "Start node not in graph's vertices."

    shortest_paths = {start_node: 0}
    before_node = {start_node: None}
    frontier = [start_node]

    while frontier:
        next_frontier = []
        for node in frontier:
            for neighbor in graph.neighbors[node]:
                if neighbor not in shortest_paths:
                    shortest_paths[neighbor] = shortest_paths[node] + 1
                    before_node[neighbor] = node
                    next_frontier.append(neighbor)
        frontier = next_frontier

    return shortest_paths, before_node
