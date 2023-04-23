import math
import os
import string
from pathlib import Path
from typing import Dict, Union

Pathlike = Union[str, Path]
translate_table = str.maketrans(
    string.punctuation + string.ascii_uppercase,
    " " * len(string.punctuation) + string.ascii_lowercase,
)


def get_word_count_dict(file: Pathlike) -> Dict[str, int]:
    """Read a document and remove punctuation and change Upper case letters to lower case.
    And create a word count dictionary from the document.

    :param file: Document file path.
    :return: Word count dictionary containing keys as a word and values as a number of appearance of the word.
    """
    with open(file, encoding="utf8") as f:
        document = f.read()
    word_list = document.translate(translate_table).split()

    wc_dict = {}
    for word in word_list:
        if word in wc_dict:
            wc_dict[word] += 1
        else:
            wc_dict[word] = 1

    return wc_dict


def get_doc_dist(wc_dict1: Dict[str, int], wc_dict2: Dict[str, int]) -> float:
    """Return a angle distance of two documents using the word count dictionary.

    :param wc_dict1: Word count dictionary from the first document.
    :param wc_dict2: Word count dictionary from the second document.
    :return: Angle distance in radians.
    """

    def get_inner_product(wc_dict1: Dict[str, int], wc_dict2: Dict[str, int]) -> float:
        """Calculate inner product of two documents using the word count dictionary.
        If there is a common word with a count in each word count dictionary the multiplication of the count
        will be added to the inner product

        :param wc_dict1: Word count dictionary from the first document.
        :param wc_dict2: Word count dictionary from the second document.
        :return: Inner product of two documents.
        """
        inner_product = 0
        for word, count in wc_dict1.items():
            inner_product += count * wc_dict2.get(word, 0)
        return inner_product

    doc1_length = math.sqrt(get_inner_product(wc_dict1, wc_dict1))
    doc2_length = math.sqrt(get_inner_product(wc_dict2, wc_dict2))
    inner_product = get_inner_product(wc_dict1, wc_dict2)

    # Clip the values between [-1.0, 1.0] when the calculated values
    # is little bigger or smaller than the values. This is due to floating point precision.
    calculated_value = max(-1.0, min(inner_product / (doc1_length * doc2_length), 1.0))

    return math.acos(calculated_value)


def calculate_doc_dist(file1: Pathlike, file2: Pathlike) -> float:
    """Return a angle distance of two documents.
    If two documents are identical the angle will be 0 degrees.
    If two documents don't have any common words the angle will be 90 degrees.

    :param file1: Path to file1.
    :param file2: Path to file2.
    :return: Vector angle of two files. (By radian)
    """
    assert os.path.exists(file1), f"{file1} doesn't exists."
    assert os.path.exists(file2), f"{file2} doesn't exists."

    wc_dict1 = get_word_count_dict(file1)
    wc_dict2 = get_word_count_dict(file2)
    return get_doc_dist(wc_dict1, wc_dict2)
