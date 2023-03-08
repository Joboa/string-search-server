"""Unit test for search_algorithms.py"""

import pytest

from file_handling import strings_list, text_file_path
from search_algorithms import linear_search, binary_search, jump_search


@pytest.fixture(scope="module")
def get_file_path():
    config_file = "configs.ini"
    file_path = text_file_path(config_file)
    yield file_path


def test_linear_search(get_file_path):
    """Test linear search algorithm.

    It takes a list of strings and a query string, and returns
    True if the query string is in the list, and False if it is not

    :param get_file_path: This is the path to the file that contains
    the strings
    """
    arr = strings_list(get_file_path)

    query_1 = "foo"
    query_2 = "2;3;12;29;13;3;19;22;"

    ls_1 = linear_search(arr, query_1)
    ls_2 = linear_search(arr, query_2)
    assert ls_1 == False
    assert ls_2 == True


def test_jump_search(get_file_path):
    """Test jump search algorithm.

    It takes a list of strings and a query string, and returns
    True if the query string is in the list, and False if it is not

    :param get_file_path: This is the path to the file that contains
    the strings
    """
    arr = strings_list(get_file_path)

    query_1 = "foo"
    query_2 = "2;3;12;29;13;3;19;22;"
    query_3 = "00"
    query_4 = arr[-1]

    js_1 = jump_search(arr, query_1)
    js_2 = jump_search(arr, query_2)
    js_3 = jump_search(arr, query_3)
    js_4 = jump_search(arr, query_4)

    assert js_1 == False
    assert js_2 == True
    assert js_3 == False
    assert js_4 == True


def test_binary_search(get_file_path):
    """Test binary search algorithm.

    It takes a list of strings and a query string, and returns True if
    the query string is in the list, and False if it is not

    :param get_file_path: This is the path to the file that contains
    the strings
    """
    arr = strings_list(get_file_path)

    query_1 = "foo"
    query_2 = "2;3;12;29;13;3;19;22;"

    bs_1 = binary_search(arr, query_1)
    bs_2 = binary_search(arr, query_2)
    assert bs_1 == False
    assert bs_2 == True
