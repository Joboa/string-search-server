"""Search algorithms."""

import math


def linear_search(arr, target):
    """Linear search algorithm.

    This algorithm performs a linear search in an array,
    and if the target value is found, it returns "True,"
    otherwise it returns "False."

    :param arr: The array to search through
    :param target: The value you're looking for
    :return: True or False
    """
    if target in arr:
        return True
    return False


def binary_search(list, target):
    """Binary search algorithm.

    This algorithm searches for a target value in a sorted l
    ist by repeatedly dividing  the list in half until the target
    is found or it is determined that the target is not in the list.

    :param list: the list of numbers you want to search through
    :param target: the value we're looking for
    :return: The index of the target value
    """
    first = 0
    last = len(list) - 1

    while first <= last:
        midpoint = (first + last) // 2
        if list[midpoint] == target:
            return True
        elif list[midpoint] < target:
            first = midpoint + 1
        elif list[midpoint] > target:
            last = midpoint - 1
    return False


def jump_search(arr, target):
    """Jump search algorithm.

    This algorithm uses a technique called jump search to search for a
    target value in a sorted array by dividing the array into blocks
    and performing a linear search within the block that potentially
    contains the target value.

    :param arr: The array to search through
    :param target: The value we're searching for
    :return: True or False
    """
    n = len(arr)
    prev, step = 0, int(math.sqrt(n))
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return False
    while arr[prev] < target:
        prev += 1
        if prev == min(step, n):
            return False
    if arr[prev] == target:
        return True
    return False
