# Implementation of 3 fibonacci methods
# 1. Recursion
# 2. Recursion w. Memoization
# 3. Bottom up


def fib_recursion(index: int) -> int:
    """Calculate the `index`'th fibonacci number using the recursion method.

    :param index: Index of the fibonacci number that the user want to know.
    :return: Fibonacci result.
    """
    if index <= 2:
        return 1

    return fib_recursion(index - 1) + fib_recursion(index - 2)


def fib_recursion_mem(index: int) -> int:
    """Calculate the `index`'th fibonacci number using the recursion + memoization method.

    :param index: Index of the fibonacci number that the user want to know.
    :return: Fibonacci result.
    """
    # memory to remember the fibonacci results
    # 1 and 2 is set before.
    memory = {1: 1, 2: 1}

    def inner_recursion(index: int) -> int:
        """Inner function that actually does the recursion.
        Using the dictionary from the outside function.

        :param index: Index of the fibonacci number that the user want to know.
        :return: Fibonacci result.
        """
        if index in memory:
            return memory[index]
        memory[index] = inner_recursion(index - 1) + inner_recursion(index - 2)
        return memory[index]

    return inner_recursion(index)


def fib_bottom_up(index: int) -> int:
    """Calculate the `index`'th fibonacci number using the bottom-up method.

    :param index: Index of the fibonacci number that the user want to know.
    :return: Fibonacci result.
    """
    memory = {}

    for i in range(1, index + 1):
        if i <= 2:
            memory[i] = 1
        else:
            memory[i] = memory[i - 1] + memory[i - 2]

    return memory[index]
