"""File handling script."""

import re

from search_algorithms import binary_search, jump_search, linear_search


def text_file_path(config_file):
    """Return the text file path in the config file.

    It opens the config file, reads the contents, searches for the
    linuxpath string, and returns the file path if found

    :param config_file: the path to the config file
    :return: The file path
    """
    try:
        with open(config_file, "r") as f:
            config_content = f.read()
            # Searching for the string "windows path" and returning the next line.
            match = re.search(r"windows_path([^\n]+)", config_content)
            if match:
                # Getting the file path from the config file.
                file_path = match.group(1)
                return file_path.replace(" ", "").replace("=", "")
    except FileNotFoundError:
        return f"{config_file} not found"


def search_for_string(file_name, search_string, cached_data=None):
    """Search for a string given a search string and a list.

    It opens the file, reads the contents, and checks if the search
    string is in the file

    :param file_name: the name of the file you want to search
    :param search_string: the string you want to search for
    """
    if cached_data is None:
        # read from file
        try:
            search_list = strings_list(file_name)
            return binary_search(search_list, search_string)
            # return jump_search(search_list, search_string)
            # return linear_search(search_list, search_string)
        except TypeError:
            return f"File, '{file_name}' is not a text file or is encoded"\
                + " in an unsupported format."
    else:
        # search in cached data
        return binary_search(cached_data, search_string)


def strings_list(file_name):
    """Generate a list of strings.

    It opens the file, reads the lines, strips the newline characters,
    sorts the list, and returns the list

    :param file_name: The name of the file that contains the list of
    strings to search for
    :return: A list of strings.
    """
    try:
        with open(file_name, "r") as f:
            search_list = f.readlines()
            search_list = [
                search_string.strip()
                for search_string in search_list
            ]
            search_list.sort()
            return search_list
    except FileNotFoundError:
        return f"{file_name} not found"
