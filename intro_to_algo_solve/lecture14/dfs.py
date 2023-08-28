from typing import Any, Optional

from intro_to_algo_solve.data_structures.graph import Graph


class DFSInfo:
    """Class containing information of Depth-First Search information."""

    def __init__(self) -> None:
        """Constructor for the DFSInfo instance."""
        self.before_node = {}
        self.start_steps = {}
        self.end_steps = {}
        self.edge_types = {}
        self.order = []
        self.topological_sorted = None
        self.acyclic = False
        self.step = 1


def dfs_step_in(
    graph: Graph,
    current_vertex: Any,
    dfs_info: DFSInfo,
    before_vertex: Optional[Any] = None,
):
    """Do a depth first search to the neighbors of `current_vertex`.

    :param graph: `Graph` instance containing vertices and edges information.
    :param current_vertex: Current vertex visited by the function.
    :param dfs_info: `DFSInfo` instance containing the depth first search result.
    :param before_vertex: Before vertex of the `current_vertex`, defaults to None.
    """
    dfs_info.before_node[current_vertex] = before_vertex
    dfs_info.step += 1
    dfs_info.start_steps[current_vertex] = dfs_info.step
    if before_vertex:
        dfs_info.edge_types[(before_vertex, current_vertex)] = "Tree"

    if current_vertex in graph.vertices:
        for neighbor in graph.neighbors[current_vertex]:
            if neighbor not in dfs_info.before_node:
                dfs_step_in(graph, neighbor, dfs_info, current_vertex)
            elif neighbor not in dfs_info.end_steps:
                dfs_info.edge_types[(current_vertex, neighbor)] = "Backward"
            elif dfs_info.start_steps[current_vertex] < dfs_info.start_steps[neighbor]:
                dfs_info.edge_types[(current_vertex, neighbor)] = "Forward"
            else:
                dfs_info.edge_types[(current_vertex, neighbor)] = "Cross"

    dfs_info.step += 1
    dfs_info.end_steps[current_vertex] = dfs_info.step
    dfs_info.order.append(current_vertex)


def depth_first_search(graph: Graph) -> DFSInfo:
    """Do a depth first search on the `graph`.
    And return the `DFSInfo` instance containing the search result.

    :param graph: `Graph` instance containing vertices and edges information.
    :return: `DFSInfo` instance containing the depth first search result.
    """
    dfs_info = DFSInfo()

    for vertex in graph.vertices:
        if vertex not in dfs_info.before_node:
            dfs_step_in(graph, vertex, dfs_info)

    # Do a topological sort if the graph is not acyclic
    for edge_type in dfs_info.edge_types.values():
        if edge_type == "Backward":
            dfs_info.acyclic = True
            break

    if not dfs_info.acyclic:
        dfs_info.topological_sorted = dfs_info.order[::-1]

    return dfs_info
