def sqrt_precision(num: int, step: int) -> float:
    """Calculate the square root of `num` using the Newton's method.
    `step` indicates how much precision steps is needed for this square root calculation.

    :param num: Integer to calculate square root.
    :param step: Precision step.
                 One precision step increase means 2 decimal precision increase.
    :return: Result of the square root precision process.
    """
    assert step > 0, "`step` must be a integer larger than 0."

    guess = 1
    for _ in range(step):
        guess = (guess + num / guess) / 2

    return guess
