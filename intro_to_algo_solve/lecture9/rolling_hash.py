# a implementation of rolling hashing
# rolling hash is a quick hashing of a list or a string object with a fixed window size
# a rolling hash has three functions
# 1. hash function -> hash a sequence
# 2. append function -> add a element to the already hashed sequence do hashing again
# 3. pop function -> remove a element in front of the sequence and do hashing again

import sys


class RollingHash:
    """A class of the rolling hash."""

    def __init__(self, prime: int, base: int = sys.maxunicode + 1) -> None:
        """Constructor for the rolling hash instance.

        :param prime: Prime number to do a modular hashing.
        :param base: Base of the character, defaults to sys.maxunicode + 1.
        """
        self.string = ""
        self.prime = prime
        self.base = base
        self.hash = 0  # hash value is initially 0
        # this value is used when doing pop and append
        # since the base**size mode prime could be a large number,
        # save it before to prevent long time calculation
        self.magic_num = 1
        # doing skip in a fast way a new value before modulating could be negative
        # but a computer calculates the modular of a negative as a negative,
        # which is not what we want
        # to compensate this, add this value
        self.compensate_num = base * prime
        # this value is a modulo inverse of the base respect to the prime
        # this value is needed when updating the magic_num when doing skip
        # because dividing the magic_num with base could be less than 1
        # by using the inverse modulo of base this can be prevented
        self.inverse_base_mod = pow(self.base, -1, self.prime) % self.prime

    def append(self, character: str) -> None:
        """Add a character to the back of the sequence and calculate the hash.
        The original expression is:
        - [(u mod p) * a + val] mod p
        but for quick calculation it is changed slightly.

        :param character: Character to append.
        """
        self.string += character
        self.hash = (self.hash * self.base + ord(character)) % self.prime
        self.magic_num = (self.magic_num * self.base) % self.prime

    def pop(self, character: str) -> None:
        """Remove a character in front of the sequence and calculate the hash.
        The original expression is:
        - [(u mod p) - val * (a ** (|u| - 1) mod p)] mod p

        :param character: Character to pop.
        """
        assert self.string[0] == character, f'The first character is not "{character}".'
        self.string = self.string[1:]

        self.magic_num = (self.magic_num * self.inverse_base_mod) % self.prime
        self.hash = (
            self.hash - (ord(character) * self.magic_num) + self.compensate_num
        ) % self.prime
