from typing import List


def visualize_heap(heap_array: List[int]) -> None:
    """Visualize the heap_array.

    :param heap_array: A heap expressed by a array of integer.
    """
    floors = []
    max_num_len = len(str(max(heap_array)))
    current_len = len(heap_array)

    power = 0
    while current_len > 0:
        floors.append(
            [
                str(num)
                for num in heap_array[
                    2**power - 1 : min(2**power + current_len, 2 ** (power + 1) - 1)
                ]
            ]
        )
        current_len -= 2**power
        power += 1

    max_element_count = 2 ** (len(floors) - 1)
    total_width = max_element_count * (max_num_len + 1) + 3

    for idx, floor in enumerate(floors):
        col_width = int(total_width / (2 ** (idx - 1)))

        for element in floor:
            print(element.center(col_width), end="")
        print()

