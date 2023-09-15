from random import getrandbits, random
from typing import Iterable, TypeVar

T = TypeVar("T")


def generate_id(extra_string="") -> str:
    """
    Generate random ID. Never spits out the same output.

    Args:
        extra_string (str): extra string to make it more random.
    """
    return (f"%010x{extra_string}{random()}" % getrandbits(60))[:15]


def split_into_n_elements(data: Iterable[T], n_element: int = 5) -> list[list[T]]:
    """
    Split iterable into n_element lists.

    Args:
        data (Iterable[T]): Iterable to be slice.
        n_element (int): how many element will be in each list

    Returns:
        list[list[T]]: list of list with n_element
    """
    data_list = list(data)
    return [data_list[i : i + n_element] for i in range(0, len(data_list), n_element)]
