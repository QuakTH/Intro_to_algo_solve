from typing import Any, Dict, List

import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    """A class containing information of the vertices and edges of a graph."""

    def __init__(self, adjacency_info: Dict[Any, List[Any]]) -> None:
        """Constructor for the Graph instance.

        :param adjacency_info: Adjacency info using a Python dictionary.
                               Which keys are vertices and values are list of vertices
                               adjacent to a particular vertex
        """
        self.adjacency_info = adjacency_info

    def visualize(self) -> None:
        """Visualize the graph using the networkx and matplotlib library."""
        graph = nx.Graph()

        graph.add_nodes_from(self.adjacency_info.keys())

        edge_set = set()
        for vertex, neighbors in self.adjacency_info.items():
            for neighbor in neighbors:
                edge_set.add((vertex, neighbor))

        graph.add_edges_from(edge_set)

        nx.draw(graph, with_labels=True, font_weight="bold")
        plt.show()
