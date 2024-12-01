## advent of code 2024
## https://adventofcode.com/2024
## day 01

from my_utils import setup_logging
from collections import Counter

logger = setup_logging(log_level="INFO")


def parse_input(lines):
    """
    Parses the input lines into two separate lists for left and right values.

    Args:
        lines (list of str): The input lines from the file.

    Returns:
        tuple: Two lists containing the left and right values respectively.
    """
    left_list = []
    right_list = []

    for line in lines:
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)

    logger.debug(
        f"Parsed input into left_list: {left_list} and right_list: {right_list}"
    )
    return left_list, right_list


def part1(left_list, right_list):
    """
    Calculates the total distance by pairing and comparing the sorted lists.

    Args:
        left_list (list of int): The list of left values.
        right_list (list of int): The list of right values.

    Returns:
        int: The total distance.
    """
    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    logger.debug(f"Sorted left_list: {left_sorted}")
    logger.debug(f"Sorted right_list: {right_sorted}")

    # Calculate the total distance
    total_distance = 0
    for left, right in zip(left_sorted, right_sorted):
        distance = abs(left - right)
        total_distance += distance
        logger.debug(f"Pair ({left}, {right}) - Distance: {distance}")

    logger.debug(f"Total distance: {total_distance}")
    return total_distance


def part2(left_list, right_list):
    """
    Calculates the total similarity score by counting the occurrences of each number
    in the right list and multiplying it by the corresponding number in the left list.

    Args:
        left_list (list of int): The list of left values.
        right_list (list of int): The list of right values.

    Returns:
        int: The total similarity score.
    """
    right_count = Counter(right_list)
    logger.debug(f"Right list counts: {right_count}")

    total_similarity_score = 0
    for num in left_list:
        score = num * right_count.get(num, 0)
        total_similarity_score += score
        logger.debug(
            f"Number {num} - Count in right_list: {right_count.get(num, 0)} - Score: {score}"
        )

    logger.debug(f"Total similarity score: {total_similarity_score}")
    return total_similarity_score
