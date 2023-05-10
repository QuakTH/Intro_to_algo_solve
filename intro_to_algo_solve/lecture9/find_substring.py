# find whether a certain substring exists inside list of strings
# And return the strings which have the string

from typing import List

from intro_to_algo_solve.lecture8.hash_table import generate_large_prime
from intro_to_algo_solve.lecture9.rolling_hash import RollingHash


def search(texts: List[str], text_to_search: str) -> List[str]:
    """Filter texts inside the `texts` variable which have the `text_to_search`.

    :param texts: List of texts to search.
    :param text_to_search: Sub text that needs to be found.
    :return: A filtered texts which have `text_to_search`.
    """
    prime_number = generate_large_prime(bit_size=64)

    text_to_search_rh = RollingHash(prime_number)
    for char in text_to_search:
        text_to_search_rh.append(char)

    filtered_texts = []
    text_rh = RollingHash(prime_number)
    for text in texts:
        if len(text) < len(text_to_search):
            continue

        text_rh.string = ""
        text_rh.hash = 0
        text_rh.magic_num = 1

        for idx, char in enumerate(text):
            if idx < len(text_to_search):
                text_rh.append(char)
            elif (
                text_rh.hash == text_to_search_rh.hash
                and text_rh.string == text_to_search_rh.string
            ):
                filtered_texts.append(text)
                break
            else:
                text_rh.append(char)
                text_rh.pop(text_rh.string[0])
        else:
            if (
                text_rh.hash == text_to_search_rh.hash
                and text_rh.string == text_to_search_rh.string
            ):
                filtered_texts.append(text)

    return filtered_texts
