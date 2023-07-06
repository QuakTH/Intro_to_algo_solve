def get_digit_count(num: int) -> int:
    """Get the number of digits of `num`.

    :param num: Number to get the digit count.
    :return: Number of digit of the integer.
    """
    # when the number is zero return 1
    if not num:
        return 1
    # when the number is negative, turn it into a positive
    if num < 0:
        num = -num

    digit = 0
    while num:
        digit += 1
        num //= 10

    return digit


def apply_karatsuba(num1: int, num2: int) -> int:
    """Do a recursive application of the karatsuba method to two integers multiplication.

    :param num1: Integer to multiply.
    :param num2: Integer to multiply.
    :return: Karatsuba's method result result.
    """
    num_digit = max(get_digit_count(num1), get_digit_count(num2))

    if num_digit == 1:
        return num1 * num2

    half_digit = num_digit // 2
    if num_digit - half_digit > half_digit:
        half_digit = num_digit - half_digit

    base_power = 10**half_digit
    num1_high = num1 // base_power
    num1_low = num1 % base_power
    num2_high = num2 // base_power
    num2_low = num2 % base_power

    z0 = apply_karatsuba(num1_low, num2_low)
    z2 = apply_karatsuba(num1_high, num2_high)
    z1 = apply_karatsuba(num1_high + num1_low, num2_high + num2_low) - z0 - z2

    return z2 * (10 ** (half_digit * 2)) + z1 * base_power + z0


def multiply_two_numbers(num1: int, num2: int) -> int:
    """Calculate the multiplication result of two numbers (`num1`, `num2`).
    The two numbers must be a base 10 integers and must have the same digit count.

    :param num1: Integer to multiply.
    :param num2: Integer to multiply.
    :return: Multiplication result.
    """
    num1_digit = get_digit_count(num1)
    num2_digit = get_digit_count(num2)

    assert num1_digit == num2_digit, "The two numbers must have the same digit count."

    # Flag and sign for calculating Negative * Positive multiplication
    num1_negative = False
    num2_negative = False
    sign = 1

    if num1 < 0:
        num1_negative = True
        num1 = -num1
    if num2 < 0:
        num2_negative = True
        num2 = -num2
    if num1_negative is not num2_negative:
        sign = -1

    return sign * apply_karatsuba(num1, num2)
