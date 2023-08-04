from typing import Any, Dict, List

import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    """A class containing information of the vertices and edges of a graph."""

    def __init__(
        self, adjacency_info: Dict[Any, List[Any]], is_directed: bool = False
    ) -> None:
        """Constructor for the Graph instance.

        :param adjacency_info: Adjacency info using a Python dictionary.
                               Which keys are vertices and values are list of vertices
                               adjacent to a particular vertex
        :param is_directed: Whether the graph is a directed graph.
        """
        self.adjacency_info = adjacency_info
        self.is_directed = is_directed

        self.check_directed_feat()

    def check_directed_feat(self) -> None:
        """Check if the `adjacency_info` is correct if `is_directed` is false.(Undirected)"""
        if not self.is_directed:
            edges = []

            for vertex, neighbors in self.adjacency_info.items():
                for neighbor in neighbors:
                    edges.append((vertex, neighbor))

            while edges:
                start, end = edges[0]
                assert (end, start) in edges, "The adjacency info is incorrect."

                edges.remove((start, end))
                edges.remove((end, start))

    def visualize(self) -> None:
        """Visualize the graph using the networkx and matplotlib library."""
        graph = nx.DiGraph() if self.is_directed else nx.Graph()

        graph.add_nodes_from(self.adjacency_info.keys())

        edges = []
        for vertex, neighbors in self.adjacency_info.items():
            for neighbor in neighbors:
                edges.append((vertex, neighbor))

        if not self.is_directed:
            undirected_edges = []
            while edges:
                edge = edges[0]

                undirected_edges.append(edge)
                edges.remove(edge)
                edges.remove(tuple(reversed(edge)))
            edges = undirected_edges

        graph.add_edges_from(edges)

        if self.is_directed:
            nx.draw(
                graph,
                with_labels=True,
                font_weight="bold",
                arrows=True,
                arrowstyle="->",
                arrowsize=15,
            )
        else:
            nx.draw(graph, with_labels=True, font_weight="bold")
        plt.show()
