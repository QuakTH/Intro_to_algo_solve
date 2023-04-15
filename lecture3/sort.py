from typing import List


def check_if_sorted(array: List[int]) -> bool:
    """Check if a array of integer is sorted. (From smaller to larger)

    :param array: Array of integers.
    :return: Whether the array is sorted.
    """
    for idx, value in enumerate(array[:-1]):
        if value > array[idx + 1]:
            return False
    return True


def get_insert_idx(
    array: List[int], insert_element: int, end_idx: int, start_idx: int = 0
) -> int:
    """Return a index of an array which the `insert_element` be inserted to.

    :param array: Array of integers.
    :param insert_element: Element to be inserted.
    :param end_idx: Search end index.
    :param start_idx: Search start index, defaults to 0.
    :return: A index to be inserted.
    """
    if start_idx == end_idx:
        if insert_element >= array[start_idx]:
            return start_idx + 1
        return start_idx

    target_index = (start_idx + end_idx) // 2
    left_index = max(start_idx, target_index - 1)
    right_index = min(end_idx, target_index + 1)

    if array[target_index] > insert_element:
        return get_insert_idx(array, insert_element, left_index)
    if array[target_index] < insert_element:
        return get_insert_idx(array, insert_element, end_idx, right_index)
    return target_index


def insert_element(
    array: List[int], element: int, end_idx: int, insert_idx: int
) -> None:
    """Insert the `element` to the given `insert_idx`.
    Before inserting shift the elements from `insert_idx` to `end_idx` - 1 to the left.

    :param array: Array of integers.
    :param element: Element to insert.
    :param end_idx: End index for shifting limit. (not a end index of the array)
    :param insert_idx: Insert index where the element should be inserted.
    """
    if end_idx == insert_idx:
        return

    for idx in range(end_idx - 1, insert_idx - 1, -1):
        array[idx + 1] = array[idx]
    array[insert_idx] = element


def insertion_sort(array: List[int]) -> None:
    """Do a insertion sort.
    Simple explanation:
    For a given array A[1..n]
        for j <- 2..n
            insert A[j] to already sorted array A[1..j-1]
    Remember that this function does the insertion sort inplace.

    :param array: Array to do insertion sort.
    """
    for key_idx in range(1, len(array)):
        element = array[key_idx]

        if element >= array[key_idx - 1]:
            continue

        insert_idx = get_insert_idx(array, element, key_idx - 1)
        insert_element(array, element, key_idx, insert_idx)


def merge_sort(array: List[int], start_idx: int, end_idx: int) -> List[int]:
    """Do a merge sort.
    Simple explanation:
    For a given array A[1..n]
    - If n = 1 Do nothing.
    - Otherwise recursively sort A[1..n/2] and A[n/2+1..n].
    - And merge these two arrays.

    :param array: Array of integers.
    :param start_idx: Start index to sort.
    :param end_idx: End index to sort.
    :return: Sorted array.
    """
    if start_idx == end_idx:
        return array[start_idx : end_idx + 1]

    sorted_array = []

    middle_index = (start_idx + end_idx) // 2
    right_index = min(len(array) - 1, middle_index + 1)

    left_sorted = merge_sort(array, start_idx, middle_index)
    right_sorted = merge_sort(array, right_index, end_idx)

    right_array_index = 0
    for value in left_sorted:
        while (
            right_array_index < len(right_sorted)
            and value >= right_sorted[right_array_index]
        ):
            sorted_array.append(right_sorted[right_array_index])
            right_array_index += 1
        sorted_array.append(value)

    return sorted_array
