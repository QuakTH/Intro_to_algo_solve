from typing import List, Tuple


def check_if_1dim_peak(array: List[int], index: int) -> bool:
    """Check if the given index of a 1D array is a peak.

    :param array: Array containing integers.
    :param index: Index to check whether the element of the index is a peak.
    :return: Whether the element of the index is a peak.
    """
    element = array[index]

    if index == 0 and element >= array[index + 1]:
        return True
    elif index == len(array) - 1 and element >= array[index - 1]:
        return True
    elif element >= array[index + 1] and element >= array[index - 1]:
        return True

    return False


def check_if_2dim_peak(matrix: List[List[int]], row_idx: int, col_idx: int) -> bool:
    """Check if a given row and col index of a matrix is a peak.

    :param matrix: 2D matrix of integers.
    :param row_idx: Row index to check whether the element of the index is a peak.
    :param col_idx: Column index to check whether the element of the index is a peak.
    :return: Whether the element of the index is a peak.
    """
    element = matrix[row_idx][col_idx]
    total_rows = len(matrix)
    total_cols = len(matrix[0])

    indices_to_compare = (
        (row_idx, col_idx - 1),
        (row_idx, col_idx + 1),
        (row_idx - 1, col_idx),
        (row_idx + 1, col_idx),
    )

    for row, col in indices_to_compare:
        if row < 0 or row >= total_rows or col < 0 or col >= total_cols:
            continue
        if element < matrix[row][col]:
            return False

    return True


def one_dim_peak_find_linear(array: List[int]) -> int:
    """1D peak finding function using linear search algorithm.
    <1D peak finding>
    From a given array of integers find the index of a array which is:
        1. If it is the leftmost of an array,
           the element is greater or equal to the right indexed element.
        2. If it is the rightmost of an array,
           the element is greater or equal to the left indexed element.
        3. If it is between,
           the element is greater or equal to the left and right indexed elements.
    Remember that this function only looks for one peak not all of the peak.

    :param array: Array containing integers.
    :return: Index of the peak element.
    """
    if len(array) == 1:
        return array[0]

    for index, element in enumerate(array):
        if index == 0 and element >= array[index + 1]:
            return index
        elif index == len(array) - 1 and element >= array[index - 1]:
            return index
        elif element >= array[index + 1] and element >= array[index - 1]:
            return index


def one_dim_peak_find_binary(array: List[int], start_index: int, end_index: int) -> int:
    """1D peak finding function using binary search algorithm.
    1D peak finding algorithm is specified in the `one_dim_peak_find_linear` function
    Remember that this function only looks for one peak not all of the peak.

    :param array: Array containing integers.
    :param start_index: Start index to find the peak index.
    :param end_index: End index to find the peak index.
    :return: Index of the peak element.
    """
    if start_index == end_index:
        return start_index

    index_to_compare = (end_index + start_index) // 2
    left_index = max(0, index_to_compare - 1)
    right_index = min(len(array) - 1, index_to_compare + 1)

    if array[index_to_compare] < array[left_index]:
        return one_dim_peak_find_binary(array, start_index, left_index)
    if array[index_to_compare] < array[right_index]:
        return one_dim_peak_find_binary(array, right_index, end_index)

    return index_to_compare


def two_dim_peak_find_greedy(
    matrix: List[List[int]], row_idx: int, col_idx: int
) -> Tuple[int]:
    """2D peak finding function using greedy ascent.
    2D peak finding is almost the same as the 1D peak finding but it compares four ways of the given element:
        - (row - 1, col)
        - (row + 1, col)
        - (row, col - 1)
        - (row, col + 1)
    Returns the peak row and column index if it is a peak.

    :param matrix: 2D matrix of integers.
    :param row_idx: Row index to check whether the element is a peak.
    :param col_idx: Column index to check whether the element is a peak.
    :return: Row and column index tuple of a peak.
    """
    element = matrix[row_idx][col_idx]
    total_rows = len(matrix)
    total_cols = len(matrix[0])

    indices_to_compare = (
        (row_idx, col_idx - 1),
        (row_idx, col_idx + 1),
        (row_idx - 1, col_idx),
        (row_idx + 1, col_idx),
    )

    for row, col in indices_to_compare:
        if row < 0 or row >= total_rows or col < 0 or col >= total_cols:
            continue
        if element < matrix[row][col]:
            return two_dim_peak_find_greedy(matrix, row, col)
    return row_idx, col_idx


def two_dim_peak_find_divide_and_conquer(
    matrix: List[List[int]], row_start: int, row_end: int
) -> Tuple[int]:
    """2D peak finding function using divide and conquer.
    Returns the peak row and column index if it is a peak.

    :param matrix: 2D matrix of integers.
    :param row_start: Start of a range of rows to look for a peak.
    :param row_end: End of a range of rows to look for a peak.
    :return: Row and column index tuple of a peak.
    """

    def find_max_col_idx(row: List[int]) -> int:
        """Return a column index of a max element of `row`. (Not a peak. It is a max value.)

        :param row: Row of a integer matrix.
        :return: column index of a max value element of a row.
        """
        max_val = row[0]
        max_idx = 0

        for idx, element in enumerate(row[1:]):
            if element >= max_val:
                max_val = element
                max_idx = idx + 1

        return max_idx

    row_idx_to_search = (row_start + row_end) // 2
    upper_row_idx = max(0, row_idx_to_search - 1)
    lower_row_idx = min(len(matrix) - 1, row_idx_to_search + 1)

    max_col_idx = find_max_col_idx(matrix[row_idx_to_search])
    element = matrix[row_idx_to_search][max_col_idx]

    if element < matrix[upper_row_idx][max_col_idx]:
        return two_dim_peak_find_divide_and_conquer(matrix, row_start, upper_row_idx)
    if element < matrix[lower_row_idx][max_col_idx]:
        return two_dim_peak_find_divide_and_conquer(matrix, lower_row_idx, row_end)
    return row_idx_to_search, max_col_idx
