# Implementation of Hash table.
# Used the Universal Hashing for hashing keys


import random
from typing import Any, Optional

from intro_to_algo_solve.lecture8.prime_generator import generate_large_prime


class Node:
    """A Node for the hash table.
    Because the hash table have a linked list for the same hashed key element,
    There is a before, next attributes.
    """

    def __init__(self, value: Any) -> None:
        """Constructor for the Node instance.

        :param value: Value to save.
        """
        self.value = value
        self.before = None
        self.next = None

    def get_last_node(self) -> "Node":
        """Get the last node of the linked list.

        :return: Node which is the tail of the linked list.
        """
        if self.next:
            return self.next.get_last_node()
        return self

    def find_node_with_key(self, key: int) -> Optional["Node"]:
        """Find a node with a key value of `key` if it exists.

        :param key: A key value which a node inside the linked list may have.
        :return: A node with the `key` value if it exists.
        """
        if self.key == key:
            return self
        if self.next:
            return self.next.find_node_with_key(key)
        return None

    @property
    def key(self) -> int:
        """Return a key value for the node instance.

        :return: Key value, a memory address for the instance.
        """
        return id(self)


class HashTable:
    """A hash table class"""

    def __init__(self, table_length: int) -> None:
        """Constructor for the HashTable instance.

        :param table_length: Max length for the hash table. Which is a list type.
        """
        self.table_length = table_length
        self.table = [None for _ in range(self.table_length)]
        self.big_prime_num = generate_large_prime()
        self.a, self.b = (random.randrange(0, self.big_prime_num) for _ in range(2))

        while self.a == 0 and self.b == 0:
            self.a, self.b = (random.randrange(0, self.big_prime_num) for _ in range(2))

        assert (
            self.big_prime_num > self.table_length
        ), "A big prime number must be larger than the table length."

    def hash_key(self, key: int) -> int:
        """Hash the key using the Universal Hashing.

        :param key: Key to hash.
        :return: A hashed key.
        """

        return ((self.a * key + self.b) % self.big_prime_num) % self.table_length

    def insert(self, value: Any) -> None:
        """Insert a value by creating a Node and insert it to the hash table.

        :param value: A value to insert.
        """
        node = Node(value)
        hashed_key = self.hash_key(node.key)

        head = self.table[hashed_key]
        if not head:
            self.table[hashed_key] = node
        else:
            last_node = head.get_last_node()
            last_node.next = node
            node.before = last_node

    def find(self, key: int) -> Optional[Node]:
        """Find the node with the `key` value if it exists inside the hash table.

        :param key: Key value of the node.
        :return: A node instance if it exists.
        """
        hashed_key = self.hash_key(key)

        head = self.table[hashed_key]
        if not head:
            return None

        return head.find_node_with_key(key)

    def delete(self, key: int) -> Optional[Node]:
        """Delete the Node with the key value of `key` if it exists.

        :param key: Key value to delete.
        :return: A node that gets deleted if it exists.
        """
        node = self.find(key)

        if not node:
            return None

        if node.before:
            node.before.next = node.next
        if node.next:
            node.next.before = node.before

        if not node.before:
            if not node.next:
                self.table[self.hash_key(key)] = None
            else:
                self.table[self.hash_key(key)] = node.next

        node.next = None
        node.before = None

        return node

    def print_hash_table(self) -> None:
        """Print the hash table with this format:
        - [hashed key] -> (key, value) - (key, value) - ...
        """

        for idx, head in enumerate(self.table):
            if head:
                node_string = f"({head.key}, {head.value})"

                next = head.next
                while next:
                    node_string += f" - ({next.key}, {next.value})"
                    next = next.next
                print(f"[{idx}] -> {node_string}")
            else:
                print(f"[{idx}] -> Empty")
