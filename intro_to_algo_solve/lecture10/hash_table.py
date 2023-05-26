# Implementation of the Hash table.
# Most of the process is inherited from the lecture8 hash table code.
# Some features have changed:
# 1. The table will increase or decrease when doing insert or delete.
# 2. The Node will be assigned to the table with the unique index. (No linked list)

import random
from typing import Any, Optional

from intro_to_algo_solve.lecture8 import hash_table
from intro_to_algo_solve.lecture8.prime_generator import generate_large_prime


class Node:
    """A Node for the hash table.
    Doesn't use the linked list version.
    Also, only accept keys which is a string.
    """

    def __init__(self, key: str, value: Any) -> None:
        """Constructor for the Node instance.

        :param key: Key for the node.
        :param value: Value to save.
        """
        self.key = key
        self.value = value
        self.deleted = False  # Delete flag


class HashTable(hash_table.HashTable):
    """A hash table class."""

    def __init__(self) -> None:
        """Constructor for the HashTable instance.
        The initial table length in now fixed to 2.
        It will increase when <number of inserted element> == <table length>.
        """
        super().__init__(2)
        self.big_prime_num2 = generate_large_prime()
        self.inserted_element = 0  # keep track of the current inserted element
        self.a2, self.b2 = (random.randrange(0, self.big_prime_num2) for _ in range(2))

        while self.a2 == 0 and self.b2 == 0:
            self.a2, self.b2 = (
                random.randrange(0, self.big_prime_num2) for _ in range(2)
            )

        assert (
            self.big_prime_num2 > self.table_length
        ), "A big prime number must be larger than the table length."

    def hash_key(self, key: str, multiplier: int) -> int:
        """Hash the key using the Universal Hashing.
        Do a double hashing probing strategy.

        :param key: Key to hash.
        :param multiplier: Value to multiply to second hashed value.
        :return: A hashed key.
        """
        hashed_key = hash(key)
        h1 = ((self.a * hashed_key + self.b) % self.big_prime_num) % self.table_length
        h2 = (
            (self.a2 * hashed_key + self.b2) % self.big_prime_num2
        ) % self.table_length

        # if h2 is zero, meaning if h2 is a multiple of table length
        # reset h2 to 1
        h2 = 1 if h2 % 2 == 0 else h2

        return (h1 + multiplier * h2) % self.table_length

    def search(self, key: str) -> Optional[Node]:
        """Search for the node with the `key` as a key.
        If not found, return None.

        :param key: Key of a node to search.
        :return: The node itself or None if not found.
        """
        for multiplier in range(self.table_length):
            hashed_val = self.hash_key(key, multiplier)
            val_at_idx = self.table[hashed_val]

            if val_at_idx is None or val_at_idx.key != key:
                continue

            # if the found node was deleted break the loop
            if val_at_idx.deleted:
                break

            return val_at_idx
        return None

    def create_new_table(self, reduce=False) -> None:
        """Do a table doubling if reduce is False, else do table halfing.

        :param reduce: Whether to do table doubling or halfing, defaults to False.
        """
        assert (
            self.big_prime_num > self.table_length * 2
            and self.big_prime_num2 > self.table_length * 2
        ), "A big prime number must be larger than the new table length."

        old_table = self.table
        self.table = (
            [None for _ in range(self.table_length // 2)]
            if reduce
            else [None for _ in range(self.table_length * 2)]
        )
        self.table_length = len(self.table)

        for element in old_table:
            if element is None or element.deleted:
                continue

            for multiplier in range(self.table_length):
                hashed_val = self.hash_key(element.key, multiplier)
                val_at_idx = self.table[hashed_val]

                if val_at_idx is None:
                    self.table[hashed_val] = element
                    break

    def insert(self, key: str, value: Any) -> None:
        """Insert a `value` with a specific `key`.
        Do a table doubling when currently inserted elements num + 1 == table length.
        If there is a node with the same key, change the value to `value`.

        :param key: Key for the value.
        :param value: Value to insert.
        """
        # if there is a node with the same key change the value
        search_result = self.search(key)
        if search_result:
            search_result.value = value
            return

        for multiplier in range(self.table_length):
            hashed_val = self.hash_key(key, multiplier)
            val_at_idx = self.table[hashed_val]

            if val_at_idx is None:
                self.table[hashed_val] = Node(key, value)
                break

            if val_at_idx.deleted:
                val_at_idx.key = key
                val_at_idx.value = value
                val_at_idx.deleted = False
                break
        else:
            raise Exception("Table full")

        self.inserted_element += 1

        if self.inserted_element == self.table_length:
            self.create_new_table()

    def delete(self, key: str) -> None:
        """Delete the node with the key if it exists.
        Do a table halfing if the current inserted element number
        is less or equal to the table length / 4.

        :param key: Key to delete.
        """
        search_result = self.search(key)

        if not search_result:
            print(f"There is no key found : {key}")
            return

        search_result.deleted = True
        self.inserted_element -= 1

        if self.inserted_element <= self.table_length / 4 and self.table_length > 2:
            self.create_new_table(True)

    def print_hash_table(self) -> None:
        """Print the hash table with this format.
        [index] -> (key, value)
        """
        for idx, element in enumerate(self.table):
            item_string = (
                f"({element.key}, {element.value})"
                if (element and not element.deleted)
                else "Empty"
            )

            print(f"[{idx}] -> {item_string}")
