# A code for implementing the Binary Search Tree
# Binary Search Tree has these representation invariant:
# 1. A value of one node is
# 1-1. Bigger than the left node's value
# 1-2. Smaller than the right node's value


from typing import List, Optional


class Node:
    """Node of the BST."""

    def __init__(self, key: int, parent: Optional["Node"] = None) -> None:
        """Constructor for each Node instance.

        :param key: Value of the node.
        :param parent: Parent Node.
        """
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None

    def string_rep(self) -> List[str]:
        """Get the List of string representation of each node.

        :return: List of string representation of each node.
        """
        left_string_rep = self.left.string_rep() if self.left else []
        right_string_rep = self.right.string_rep() if self.right else []

        short, long = (
            (left_string_rep, right_string_rep)
            if len(left_string_rep) <= len(right_string_rep)
            else (
                right_string_rep,
                left_string_rep,
            )
        )

        for idx in range(len(short), len(long)):
            short.append(" " * len(long[idx]))

        string_rep = []
        for left_str, right_str in zip(left_string_rep, right_string_rep):
            string_rep.append(left_str + "  " + right_str)

        if string_rep:
            string_rep.insert(0, str(self.key).center(len(string_rep[0])))
        else:
            string_rep.append(str(self.key))

        return string_rep

    def __str__(self):
        return "\n".join(self.string_rep())

    def insert(self, value: int) -> None:
        """Insert a new value. If there is a Node with the same value, skip the insertion.

        :param value: Value to insert.
        """
        key = self.key
        left_node = self.left
        right_node = self.right

        if key == value:
            return

        if key > value:
            if left_node:
                left_node.insert(value)
            else:
                self.left = Node(value, self)
        else:
            if right_node:
                right_node.insert(value)
            else:
                self.right = Node(value, self)


class BST:
    """Binary Search Tree which contains Nodes."""

    def __init__(self) -> None:
        self.root = None

    def check_ri(self, node: Optional[Node] = None) -> None:
        """Check if the BST satisfies the BST representation invariant.

        :param node: Node to check whether it satisfies the representation invariant.
        """
        if node is None and self.root is not None:
            node = self.root

        if node is None:
            return

        key = node.key
        left_key = node.left.key if node.left else key - 1
        right_key = node.right.key if node.right else key + 1
        assert (
            key > left_key and key < right_key
        ), f"The BST doesn't satisfy the BST ri. key = {key}, left key = {left_key}, right key = {right_key}."

        if node.left is not None:
            self.check_ri(node.left)
        if node.right is not None:
            self.check_ri(node.right)

    def insert(self, value: int) -> None:
        """Insert a new value to the BST.

        :param value: Value to insert.
        """
        if self.root is None:
            self.root = Node(value)
        else:
            self.root.insert(value)

    def __str__(self) -> str:
        if self.root:
            return str(self.root)
        return "Empty Tree"
