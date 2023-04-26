# A code for implementing the Binary Search Tree
# Binary Search Tree has these representation invariant:
# 1. A value of one node is
# 1-1. Bigger than the left node's value
# 1-2. Smaller than the right node's value


from typing import List, Optional


class Node:
    """Node of the BST."""

    def __init__(self, key: int, bst: "BST", parent: Optional["Node"] = None) -> None:
        """Constructor for each Node instance.

        :param key: Value of the node.
        :param bst: BST containing the Node.
        :param parent: Parent Node.
        """
        self.key = key
        self.bst = bst
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

        total_len = (
            len(short[-1])
            if short
            else max(
                map(
                    lambda x: len(str(x)),
                    (self.bst.find_min().key, self.bst.find_max().key),
                )
            )
        )

        for idx in range(len(short), len(long)):
            short.append(" " * total_len)

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

    def find(self, value: int) -> Optional["Node"]:
        """Find the node that contains the `value`.
        If there is no node with the `value`, returns None.

        :param value: Value to find.
        :return: A BST node. If exists.
        """
        if self.key == value:
            return self

        if self.key > value and self.left:
            return self.left.find(value)

        if self.key < value and self.right:
            return self.right.find(value)

        return None

    def find_min(self) -> "Node":
        """Find the BST node containing the minimum value.
        Which root node is the node that calls this method.

        :return: Node containing the minimum value.
        """
        current = self
        while current.left:
            current = current.left
        return current

    def find_max(self) -> "Node":
        """Find the BST node containing the maximum value.
        Which root node is the node that calls this method.

        :return: Node containing the maximum value.
        """
        current = self
        while current.right:
            current = current.right
        return current

    def next_larger(self) -> Optional["Node"]:
        """Find the node which have the next large value if exists.

        :return: Node containing the next large value than
                 the node that calls this method, if exists.
        """
        if self.right:
            return self.right.find_min()

        current = self
        while self.parent and self.parent.right is current:
            current = self.parent
        return current.parent

    def next_smaller(self) -> Optional["Node"]:
        """Find the node which have the next small value if exists.

        :return: Node containing the next small value than
                 the node that calls this method, if exists.
        """
        if self.left:
            return self.left.find_max()

        current = self
        while self.parent and self.parent.left is current:
            current = self.parent
        return current.parent

    def insert(self, value: int, bst: "BST") -> "Node":
        """Insert a new value. If there is a Node with the same value,
        skip the insertion.

        :param value: Value to insert.
        :param bst: BST containing the Node.
        :return: Inserted node.
        """
        key = self.key
        left_node = self.left
        right_node = self.right

        if key == value:
            return self

        if key > value:
            if left_node:
                return left_node.insert(value, bst)
            self.left = Node(value, bst, self)
            return self.left

        if right_node:
            return right_node.insert(value, bst)
        self.right = Node(value, bst, self)
        return self.right

    def delete(self) -> "Node":
        """Delete the current node which calls this method.
        And return the Deleted Node.

        :return: The deleted node.
        """
        if not self.left or not self.right:
            if self.parent:
                if self is self.parent.left:
                    self.parent.left = self.left or self.right
                    if self.parent.left:
                        self.parent.left.parent = self.parent
                else:
                    self.parent.right = self.left or self.right
                    if self.parent.right:
                        self.parent.right.parent = self.parent
            else:
                self.bst.root=self.left or self.right

                if self.left:
                    self.left.parent = self.parent
                if self.right:
                    self.right.parent = self.parent

            self.bst = None
            return self

        next_large = self.next_larger()
        self.key, next_large.key = next_large.key, self.key
        return next_large.delete()


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

    def insert(self, value: int) -> Node:
        """Insert a new value to the BST.

        :param value: Value to insert.
        :return: Inserted node.
        """
        if self.root is None:
            self.root = Node(value, self)
            return self.root
        return self.root.insert(value, self)

    def find(self, value: int) -> Optional[Node]:
        """Find a node containing the `value`

        :param value: Value to find.
        :return: A BST node. If exists.
        """
        if self.root:
            return self.root.find(value)

        return None

    def find_min(self) -> Optional[Node]:
        """Find the BST node containing the minimum value of the BST.

        :return: Node containing the minimum value.
        """
        if self.root:
            return self.root.find_min()
        return None

    def find_max(self) -> Optional[Node]:
        """Find the BST node containing the maximum value of the BST.

        :return: Node containing the maximum value.
        """
        if self.root:
            return self.root.find_max()
        return None

    def __str__(self) -> str:
        if self.root:
            return str(self.root)
        return "Empty Tree"
