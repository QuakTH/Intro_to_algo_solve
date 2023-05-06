# Implementation of the counting sort


import random
from typing import Any, List, Tuple

from intro_to_algo_solve.lecture7.node import Node


class CountingSort:
    """Class containing methods for counting sort."""

    def __init__(self, max_key: int) -> None:
        """Constructor for the CountingSort instance.

        :param max_key: Maximum value for the key.
        """
        self.nodes = []
        self.max_key = max_key
        self.bucket = [
            0 for _ in range(max_key + 1)
        ]  # Used for counting each key from 0..k
        self.cum_bucket = [
            0 for _ in range(max_key + 1)
        ]  # Used for counting elements below value of index from 0..k

    def insert_node(self, value: Any) -> None:
        """Insert a node with a `value` with random key inside the range of 0..k.

        :param value: Value to insert.
        """
        self.nodes.append(Node(random.randint(0, self.max_key), value))

    @property
    def items(self) -> List[Tuple[int, Any]]:
        """Return a (key, value) of the node list.

        :return: Node list represented by a (key, value) list.
        """
        return [(node.key, node.value) for node in self.nodes]

    def reset_buckets(self) -> None:
        """Reset `bucket` and `cum_bucket` to 0 filled arrays."""
        for idx in range(self.max_key + 1):
            self.bucket[idx] = 0
            self.cum_bucket[idx] = 0

    def sort(self) -> None:
        """Do a counting sort on `self.nodes`."""
        self.reset_buckets()
        for node in self.nodes:
            self.bucket[node.key] += 1

        self.cum_bucket[0] = self.bucket[0]
        for idx in range(1, len(self.cum_bucket)):
            self.cum_bucket[idx] = self.cum_bucket[idx - 1] + self.bucket[idx]

        sorted_nodes = [None for _ in range(len(self.nodes))]
        for node in reversed(self.nodes):
            key = node.key
            sorted_nodes[self.cum_bucket[key] - 1] = node
            self.cum_bucket[key] -= 1
        self.nodes = sorted_nodes
