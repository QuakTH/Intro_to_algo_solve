from typing import Any


class Node:
    """A Node for Counting and Radix sort."""

    def __init__(self, key: int, value: Any) -> None:
        """Constructor for the Node.

        :param key: Key of the node. (Used for sorting)
        :param value: Value which the node holds. Could be any value.
        """
        assert isinstance(key, int), 'A `key` must be a Integer type.'

        self.key = key
        self.value = value
