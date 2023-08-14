# Module for representing the weighted graph

from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx


class WeightedGraph:
    """A class containing information of the vertices, edges, and weight of the edges"""

    def __init__(
        self, graph_info: Dict[Any, List[Tuple[Any, int]]], is_directed: bool = False
    ) -> None:
        """Constructor for the `WeightedGraph` instance.

        :param graph_info: Dictionary containing the graph information.
        Example of the dictionary is this:
        {
            <from node> : [(<to node>, <weight>), (<to node>, <weight>), ...]
        }
        :param is_directed: Whether the graph is a directed graph, defaults to False
        """
        self.vertices = list(graph_info.keys())
        self.adjacency_infos = {}
        self.edge_weight_infos = {}
        self.is_directed = is_directed

        self.generate_attributes(graph_info)
        self.check_directed_feat()

    def generate_attributes(self, graph_info: Dict[Any, List[Tuple[Any, int]]]) -> None:
        """Generate information of edges with associated weights using the `graph_info`.
        And the adjacent information of each vertices.

        :param graph_info: Dictionary containing the graph information.
        """
        for s_node, edge_infos in graph_info.items():
            self.adjacency_infos[s_node] = []
            for e_node, weight in edge_infos:
                self.edge_weight_infos[(s_node, e_node)] = weight
                self.adjacency_infos[s_node].append(e_node)

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
                ), "The graph info is incorrect."

                edges.remove(current)
                edges.remove(reversed)

    def visualize(self) -> None:
        """Visualize the graph using the networkx and matplotlib library."""
        graph = nx.DiGraph() if self.is_directed else nx.Graph()

        graph.add_nodes_from(self.vertices)

        for edge, weight in self.edge_weight_infos.items():
            reversed_edge = (edge[1], edge[0])
            if not self.is_directed and reversed_edge in graph.edges:
                continue
            graph.add_edge(*edge, weight=weight)

        positions = nx.spring_layout(graph)
        edge_labels = nx.get_edge_attributes(graph, "weight")
        if self.is_directed:
            bidir_edges = []
            oneway_edges = []

            for edge in graph.edges:
                if reversed(edge) in graph.edges:
                    bidir_edges.append(edge)
                else:
                    oneway_edges.append(edge)

            nx.draw(
                graph,
                positions,
                with_labels=True,
                font_weight="bold",
                arrows=True,
                arrowstyle="->",
                arrowsize=15,
                edgelist=oneway_edges,
            )
            nx.draw(
                graph,
                positions,
                with_labels=True,
                font_weight="bold",
                arrows=True,
                arrowstyle="->",
                arrowsize=15,
                edgelist=bidir_edges,
                connectionstyle="arc3, rad = 0.2",
            )
        else:
            nx.draw(
                graph,
                positions,
                with_labels=True,
                font_weight="bold",
            )
        nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels)
        plt.show()
