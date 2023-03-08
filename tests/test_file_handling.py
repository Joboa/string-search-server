"""Unit test for file_handling.py"""

import pytest

from file_handling import text_file_path, search_for_string, strings_list


@pytest.fixture(scope="module")
def get_file_path():
    config_file = "configs.ini"
    file_path = text_file_path(config_file)
    yield file_path


@pytest.fixture(scope="module")
def get_file_path_not_found():
    config_file = "text_configs.ini"
    file_path_not_found = text_file_path(config_file)
    yield file_path_not_found


@pytest.fixture(scope="module")
def incorrect_config_file():
    iconfig_file = "text_configs.ini"
    yield iconfig_file


@pytest.fixture(scope="module")
def get_catched_data():
    file_path = text_file_path("configs.ini")
    cached_data = strings_list(file_path)
    yield cached_data


def test_text_file_path(get_file_path):
    """Test file path exist.

    It reads a text file and returns the value of the first line
    that starts with the string "linuxpath"
    """
    assert get_file_path == text_file_path("configs.ini")


def test_text_file_path_not_found(
        get_file_path_not_found,
        incorrect_config_file):
    """Test file path not found.

    It returns the path to a text file if it exists, otherwise
    it returns a message that the file was not found
    """
    assert get_file_path_not_found == f"{incorrect_config_file} not found"


def test_search_for_string_without_cached_data(get_file_path):
    """Test search for string without cached data.

    It searches for a string in a file

    :param get_file_path: This is the path to the file that we
    want to search
    """
    query = "26;29;2;3;25;26;11;6;"
    assert search_for_string(get_file_path, query) == True
    assert search_for_string(get_file_path, "foo") == False


# def test_search_for_string_with_cached_data(get_catched_data, get_file_path):
#     """Test search for string with cached data.

#     It searches for a string in a file, and if the file is large,
#     it caches the file's contents in memory

#     :param get_catched_data: This is a fixture that returns a list of strings
#     :param get_file_path: This is a fixture that returns a path to a file
#     """
#     query = "21;0;1;28;0;8;4;0;"
#     assert search_for_string(
#         get_file_path, query,
#         cached_data=get_catched_data
#     ) == True
#     assert (
#         search_for_string(
#             get_file_path, "foo",
#             cached_data=get_catched_data) == False
#     )


# def test_search_for_string_not_found(get_file_path):
#     """Test search for string not found.

#     This function searches for a string in a file and returns the
#     line number where the string is found
#     """
#     query = 123
#     file_name = get_file_path
#     message = (
#         f"File, '{file_name}' is not a text file or is encoded "
#         "in an unsupported format."
#     )

#     assert (search_for_string(file_name, query) == message)


# def test_strings_list(get_file_path):
#     """Test strings list.

#     It takes a file path as an argument, reads the file, and
#     returns a list of strings

#     :param get_file_path: This is the path to the file that
#     you want to read
#     """
#     contents = strings_list(get_file_path)
#     assert contents[-1] == "9;0;6;6;0;9;5;0;"


# def test_strings_list_file_not_found():
#     """Test strings list file not found.

#     It tests that the function `strings_list` returns the string
#     `"unknown_text_file.txt not found"` when the file
#     `unknown_text_file.txt` is not found

#     :param get_file_path: This is a fixture that returns the path
#     to the file
#     """
#     file_name = "unknown_text_file.txt"
#     assert strings_list(file_name) == f"{file_name} not found"
