# Implementation of the Hash table.
# Most of the process is inherited from the lecture8 hash table code.
# Some features have changed:
# 1. The table will increase or decrease when doing insert or delete.
# 2. The Node will be assigned to the table with the unique index. (No linked list)

import random
from typing import Any

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
        self.a2, self.b2 = (random.randrange(0, self.big_prime_num) for _ in range(2))

        while self.a2 == 0 and self.b2 == 0:
            self.a2, self.b2 = (
                random.randrange(0, self.big_prime_num) for _ in range(2)
            )

        assert (
            self.big_prime_num2 > self.table_length
        ), "A big prime number must be larger than the table length."
