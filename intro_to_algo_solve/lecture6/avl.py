# A code for implementing the AVL tree
# A AVL tree is same as the BST tree but with one more representation invariant
# The difference of hight of the left and right child
# of the node should be less or equal to 1

from typing import Optional

from intro_to_algo_solve.lecture5 import bst


def update_height(node: "Node") -> None:
    """Update the hight of the Node.
    Height's meaning is the max depths to the leaf node from the current node.

    :param node: Node to update the height.
    """
    left_height = node.left.height if node.left else -1
    right_height = node.right.height if node.right else -1

    node.height = max(left_height, right_height) + 1


def left_rotate(avl: "AVL", node: "Node") -> None:
    """Do a left rotation of nodes with respect to `node`.

    :param avl: AVL tree containing the node.
    :param node: Node to do rotation.
    """
    right_child = node.right
    parent = node.parent

    right_child.parent = parent
    if not parent:
        avl.root = right_child
    else:
        if parent.left is node:
            parent.left = right_child
        else:
            parent.right = right_child
    node.right = right_child.left
    if node.right:
        node.right.parent = node
    right_child.left = node
    node.parent = right_child

    update_height(node)
    update_height(right_child)


def right_rotate(avl: "AVL", node: "Node") -> None:
    """Do a right rotation of nodes with respect to `node`.

    :param avl: AVL tree containing the node.
    :param node: Node to do rotation.
    """
    left_child = node.left
    parent = node.parent

    left_child.parent = parent
    if not parent:
        avl.root = left_child
    else:
        if parent.left is node:
            parent.left = left_child
        else:
            parent.right = left_child
    node.left = left_child.right
    if node.left:
        node.left.parent = node
    left_child.right = node
    node.parent = left_child

    update_height(node)
    update_height(left_child)


def rebalance(avl: "AVL", node: "Node") -> None:
    """Re-balance the tree to follow the AVL RI rule.

    :param avl: AVL tree containing the node.
    :param node: Node to start re-balancing.
    """
    while node:
        update_height(node)

        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1

        if left_height - right_height >= 2:
            left_left_height = node.left.left.height if node.left.left else -1
            left_right_height = node.left.right.height if node.left.right else -1

            if left_left_height >= left_right_height:
                right_rotate(avl, node)
            else:
                left_rotate(avl, node.left)
                right_rotate(avl, node)
        elif right_height - left_height >= 2:
            right_left_height = node.right.left.height if node.right.left else -1
            right_right_height = node.right.right.height if node.right.right else -1

            if right_right_height >= right_left_height:
                left_rotate(avl, node)
            else:
                right_rotate(avl, node.right)
                left_rotate(avl, node)
        node = node.parent


class Node(bst.Node):
    """Node of the AVL."""

    def __init__(self, key: int, avl: "AVL", parent: Optional["Node"] = None) -> None:
        """Constructor for each Node instance of the AVL.

        :param key: Value of the node.
        :param avl: BST containing the Node.
        :param parent: Parent Node. defaults to None.
        """
        super().__init__(key, avl, parent)
        self.height = -1

    def delete(self) -> "Node":
        """Delete the current node which calls this method.
        And return the Deleted Node.

        :return: The deleted node.
        """
        node = super().delete()

        rebalance(node.tree, node)

        return node


class AVL(bst.BST):
    """AVL tree class."""

    def __init__(self) -> None:
        super().__init__()

    def insert(self, value: int) -> Node:
        """Insert a new value to the AVL tree.

        :param value: Value to insert.
        :return: Inserted node.
        """
        if self.root is None:
            node = Node(value, self)
            self.root = node
        else:
            node = self.root.insert(value, self)

        rebalance(self, node)
        return node
