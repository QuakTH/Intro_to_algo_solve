# This code is a algorithm for a max heap
# A max heap's key element is greater or equal to the elements of the child nodes
# A max heap can be expressed as a array which have this characteristic :
# 1. A root of the heap is the index 0 of the heap array
# 2. A value of index i is greater or equal to the value at the child nodes at index:
#    2 * i - 1 (left child) and 2 * i + 1 (right child)

import math
from typing import Dict, List
from lecture3.sort import check_if_sorted


# This is not used
def to_dict_array(heap_array: List[int]) -> Dict[int, int]:
    """A dictionary is more faster when doing pop. (When doing heap sort)
    This will create a dictionary which key is a index of the `heap_array`
    and the value is the value of the index of the `heap_array`.

    :param heap_array: Original heap array which is the List of integers.
    :return: Dictionary version of the array.
    """
    return {idx: value for idx, value in enumerate(heap_array)}


def visualize_heap(heap_array: List[int]) -> None:
    """Visualize the heap_array.

    :param heap_array: A heap expressed by a array of integer.
    """

    max_num_len = len(str(max(heap_array)))

    max_element_count = 2 ** int(math.log2(len(heap_array)))
    total_width = max_element_count * (max_num_len + 2) + 3

    printed_col_count = 0
    for idx, element in enumerate(heap_array):
        row = int(math.log2(idx + 1))
        col_width = total_width // (2 ** (row))

        print(str(element).center(col_width), end="")
        printed_col_count += 1

        if printed_col_count == (2**row):
            print()
            printed_col_count = 0


def check_if_max_heap(heap_array: List[int]) -> bool:
    """Check if a given `heap_array` is a max heap.

    :param heap_array: Heap array to check whether the array is a max heap.
    :return: Whether the array is a max heap.
    """
    for idx, value in enumerate(heap_array):
        real_idx = idx + 1
        if real_idx * 2 > len(heap_array):
            break

        left_index = real_idx * 2 - 1
        right_index = min(real_idx * 2, len(heap_array) - 1)

        if value < heap_array[left_index] or value < heap_array[right_index]:
            return False
    return True


def max_heapify(heap_array: List[int], key_index: int) -> None:
    """From a given `heap_array` check if the element of `key_index` has a max heap feature.
    And if the element does not have the max heap feature:
        1. Swap with the biggest element in the child.
        2. Go down to the child index which the element has swapped and do `max_heapify` recursively.
    Until the function reaches the leaf node.

    :param heap_array: Array of integers to express a max heap.
    :param key_index: Index to do `max_heapify`.
    """
    real_idx = key_index + 1
    if real_idx * 2 > len(heap_array):
        return

    left_index = real_idx * 2 - 1
    right_index = min(real_idx * 2, len(heap_array) - 1)

    largest_val = heap_array[key_index]
    swap_index = key_index
    if heap_array[left_index] > largest_val:
        largest_val = heap_array[left_index]
        swap_index = left_index
    if heap_array[right_index] > largest_val:
        swap_index = right_index

    if swap_index == key_index:
        return

    heap_array[key_index], heap_array[swap_index] = (
        heap_array[swap_index],
        heap_array[key_index],
    )

    max_heapify(heap_array, swap_index)


def build_max_heap(heap_array: List[int]) -> None:
    """Generate a max heap from the `heap_array`.
    `heap_array` might not have the max heap characteristic.

    :param heap_array: Array of integers to express a heap.
    """
    for idx in range(len(heap_array) // 2, -1, -1):
        max_heapify(heap_array, idx)


def heap_sort(array: List[int]) -> List[int]:
    """Sort the array by using the `build_max_heap`, `max_heapify` function.
    Basically, do a heap sort.

    :param array: A List of Integers.
    :return: Sorted Array.
    """
    sorted_array = []

    build_max_heap(array)

    while array:
        array[0], array[-1] = array[-1], array[0]
        sorted_array.insert(0, array.pop())
        max_heapify(array, 0)

    return sorted_array
