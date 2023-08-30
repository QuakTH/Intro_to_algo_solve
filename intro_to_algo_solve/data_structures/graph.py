# Common graph data structure used for path finding algorithms.

import math
from typing import Any, Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    def __init__(
        self,
        adjacency_info: Dict[Any, List[Union[Tuple[Any, int], Any]]],
        is_directed: bool = False,
    ) -> None:
        """Constructor for the `Graph` instance.

        :param adjacency_info: Dictionary containing the adjacency information of a graph.
        There are two types of `adjacency_info`, one with weight and one without weight.
        - Example of `adjacency_info` w. weight:
          {
            <from node> : [(<to node>, <weight>), (<to node>, <weight>), ...],
            ...
          }
        - Example of `adjacency_info` wo. weight:
          {
            <from node> : [<to node>, <to node>, ...],
            ...
          }

        :param is_directed:Whether the graph is a directed graph, defaults to False.
        """
        self.vertices = list(adjacency_info)
        self.is_directed = is_directed

        self.neighbors = {}
        self.edge_weight_infos = {}
        self.is_weighted = self.check_adjacency_info(adjacency_info)

        self.generate_attributes(adjacency_info)
        self.check_directed_feat()

    def check_adjacency_info(
        self, adjacency_info: Dict[Any, List[Union[Tuple[Any, int], Any]]]
    ) -> bool:
        """Check whether the adjacency information is correct.
        And return whether the graph is weighted.

        :param adjacency_info: Dictionary containing the adjacency information of a graph.
        :return: whether the graph is a weighted graph
        """
        edge_info_set = set()
        for edge_infos in adjacency_info.values():
            edge_info_set.update(edge_infos)

        is_weighted = all(
            map(lambda neighbor: isinstance(neighbor, tuple), edge_info_set)
        )
        is_not_weighted = all(
            map(lambda neighbor: not isinstance(neighbor, tuple), edge_info_set)
        )

        assert (
            is_weighted or is_not_weighted
        ), "Check the adjacency information, it is not set correctly."

        return is_weighted

    def generate_attributes(
        self, adjacency_info: Dict[Any, List[Union[Tuple[Any, int], Any]]]
    ) -> None:
        """Generate information of the graph.
        When the graph is not a weighted graph the weight of each edge will be None.

        :param adjacency_info: Dictionary containing the adjacency information of a graph.
        """
        for from_node, edge_infos in adjacency_info.items():
            self.neighbors[from_node] = []

            if self.is_weighted:
                for to_node, weight in edge_infos:
                    self.edge_weight_infos[(from_node, to_node)] = weight
                    self.neighbors[from_node].append(to_node)
            else:
                for to_node in edge_infos:
                    self.edge_weight_infos[(from_node, to_node)] = None
                    self.neighbors[from_node].append(to_node)

    def check_directed_feat(self) -> None:
        """Check if the `adjacency_info` is correct if `is_directed` is false.(Undirected)"""
        edges = list(self.edge_weight_infos)

        if not self.is_directed:
            while edges:
                current = edges[0]
                reversed = (current[1], current[0])
                assert (
                    reversed in edges
                    and self.edge_weight_infos[current]
                    == self.edge_weight_infos[reversed]
                ), "The adjacency info is incorrect."

                edges.remove(current)
                edges.remove(reversed)

    def inbound_vertices(self, vertex: Any) -> List[Any]:
        """Return list of vertices which points to the `vertex`.
        If the graph is not a directed graph. the neighbors will be returned.

        :param vertex: Vertex to find the inbound vertices.
        :return: List of inbound vertices.
        """
        assert vertex in self.vertices, "The vertex is not in the graph's vertices."

        if not self.is_directed:
            return self.neighbors[vertex]

        inbound_vertices = []
        for v, n in self.neighbors.items():
            if vertex in n:
                inbound_vertices.append(v)

        return inbound_vertices

    def visualize(self) -> None:
        """Visualize the graph using the networkx and matplotlib library."""
        # graph = nx.DiGraph() if self.is_directed else nx.Graph()
        graph = nx.MultiDiGraph()

        graph.add_nodes_from(self.vertices)

        for edge, weight in self.edge_weight_infos.items():
            reversed_edge = (edge[1], edge[0])
            if not self.is_directed and reversed_edge in graph.edges:
                continue

            if weight:
                graph.add_edge(*edge, weight=weight)
            else:
                graph.add_edge(*edge)

        positions = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, positions)
        nx.draw_networkx_labels(graph, positions)

        layout_tracker = {}

        arrow_property = {"shrinkB": 10, "shrinkA": 0, "arrowstyle": "-"}
        if self.is_directed:
            arrow_property["arrowstyle"] = "->"

        for node1, node2, index in graph.edges:
            x1, y1 = positions[node1]
            x2, y2 = positions[node2]

            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            tracker_key = tuple(
                sorted(((x1, y1), (x2, y2)), key=lambda x: (x[0], x[1]))
            )
            factor = layout_tracker.get(tracker_key, 0)
            theta = math.atan((y2 - y1) / (x2 - x1))

            mid_x -= factor * math.sin(theta)
            mid_y += factor * math.cos(theta)

            next_factor = -factor if factor > 0 else -factor + 0.2
            layout_tracker[tracker_key] = next_factor

            if self.is_directed:
                arrow_property["connectionstyle"] = f"arc3, rad=-{factor / 2}"

            plt.annotate(
                "",
                (x1, y1),
                xytext=(mid_x, mid_y),
                arrowprops={
                    "arrowstyle": "-",
                    "connectionstyle": f"arc3, rad={factor / 2}",
                    "shrinkA": 0,
                    "shrinkB": 10,
                },
            )
            plt.annotate("", (x2, y2), xytext=(mid_x, mid_y), arrowprops=arrow_property)

            if self.is_weighted:
                plt.text(
                    mid_x,
                    mid_y,
                    graph[node1][node2][index]["weight"],
                    rotation=math.degrees(theta),
                    rotation_mode="anchor",
                    verticalalignment="center",
                    horizontalalignment="center",
                    backgroundcolor="white",
                )
        plt.show()
