import math
import random
from typing import List


# This code is not used
def is_prime_brute(num: int) -> bool:
    """Check whether a `num` is a primary number using brute force.
    Checking from 2 to square root of the number.

    :param num: Number to check whether it is a primary number.
    :return: Whether the number is a primary number
    """
    if num < 2:
        return False

    for n in range(2, int(num**0.5) + 1):
        if num % n == 0:
            return False
    return True


def get_primes_using_sieve(sieve_size: int) -> List[int]:
    """Get list of prime numbers less or equal to the number `sieve_size`.

    :param sieve_size: Sieve size to do Eratosthenes Sieve algorithm.
    :return: List of prime numbers.
    """
    sieve = [True] * (sieve_size + 1)
    sieve[0] = False
    sieve[1] = False

    for num in range(2, int(sieve_size**0.5) + 1):
        multiple = num * 2
        while multiple < sieve_size:
            sieve[multiple] = False
            multiple += num

    prime_numbers = []
    for idx, is_prime in enumerate(sieve):
        if is_prime:
            prime_numbers.append(idx)

    return prime_numbers


def rabin_miller_test(num: int, trials: int = 5) -> bool:
    """Do a Rabin Miller Primary Test on the `num`.

    :param num: A number to do a Rabin Miller Primary Test.
    :param trials: A number of trials to test.
    :return: Whether the number is a probable primary number.
    """
    if num % 2 == 0 or num < 2:
        return False
    if num == 3:
        return True

    s = num - 1
    power_of_two = 0
    while s % 2 == 0:
        s = s // 2
        power_of_two += 1
    for _ in range(trials):
        a = random.randrange(2, num - 1)
        x = pow(a, s, num)

        for _ in range(power_of_two):
            y = pow(x, 2, num)
            if y == 1 and x != 1 and x != num - 1:
                return False
            x = y
        if y != 1:
            return False
    return True


def is_prime(num: int, sieve_size: int = 100, trials: int = 5) -> bool:
    """Check whether a `num` is a primary number or not using the
        1. Small prime numbers from `get_primes_using_sieve` function.
        2. `rabin_miller_test` function.

    :param num: Number to check if it is a primary number.
    :param sieve_size: Sieve size to do Eratosthenes Sieve algorithm, defaults to 100.
    :param trials: A number of trials to test, defaults to 5.
    :return: Whether the number is a primary number.
    """
    small_primes = get_primes_using_sieve(sieve_size)

    if num < 2:
        return False
    for prime in small_primes:
        if num == prime:
            return True
        if num % prime == 0:
            return False
    return rabin_miller_test(num, trials)


def generate_large_prime(
    bit_size: int = 1024, sieve_size: int = 100, trials: int = 5
) -> int:
    """Generate a large primary number.

    :param bit_size: Bit size for the large integer, defaults to 1024.
    :param sieve_size: Sieve size to do Eratosthenes Sieve algorithm, defaults to 100.
    :param trials: A number of trials to test, defaults to 5.
    :return: A primary number.
    """
    while True:
        num = random.randrange(2 ** (bit_size - 1), 2 ** (bit_size))
        if is_prime(num, sieve_size, trials):
            return num
