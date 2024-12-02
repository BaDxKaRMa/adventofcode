#!/usr/bin/env python3
## advent of code 2024
## https://adventofcode.com/2024
## day 02

from typing import List
from my_utils import setup_logging

logger = setup_logging(log_level="INFO")


def parse_input(lines: List[str]) -> List[List[int]]:
    """
    Parses the input lines into a list of lists of integers.

    Args:
        lines (list of str): The input lines from the file.

    Returns:
        list of list of int: Parsed levels from the reports.
    """
    data = [list(map(int, line.split())) for line in lines]
    logger.debug(f"Parsed input: {data}")
    return data


def is_safe(report: List[int]) -> bool:
    """
    Determines if a report is safe by checking if the levels are either strictly increasing or strictly decreasing,
    with differences between consecutive levels ranging from 1 to 3.

    Args:
        report (list of int): A list of levels in the report.

    Returns:
        bool: True if the report is safe, False otherwise.
    """
    increasing = all(
        report[i] < report[i + 1] and 1 <= report[i + 1] - report[i] <= 3
        for i in range(len(report) - 1)
    )
    decreasing = all(
        report[i] > report[i + 1] and 1 <= report[i] - report[i + 1] <= 3
        for i in range(len(report) - 1)
    )
    logger.debug(
        f"Report: {report}, increasing: {increasing}, decreasing: {decreasing}"
    )
    return increasing or decreasing


def is_safe_with_dampener(report: List[int]) -> bool:
    """
    Determines if a report is safe with the Problem Dampener by checking if the report
    itself is safe or if it becomes safe by removing one level.

    Args:
        report (list of int): A list of levels in the report.

    Returns:
        bool: True if the report is safe, False otherwise.
    """
    if is_safe(report):
        logger.debug(f"Report: {report} is safe without dampener")
        return True

    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1 :]
        if is_safe(modified_report):
            logger.debug(
                f"Report: {report} is safe with dampener by removing level {report[i]}"
            )
            return True
    logger.debug(f"Report: {report} is not safe with dampener")
    return False


def part1(data: List[List[int]]) -> int:
    """
    Counts the number of safe reports.

    Args:
        data (list of list of int): The parsed levels from the reports.

    Returns:
        int: The number of safe reports.
    """
    safe_reports = sum(1 for report in data if is_safe(report))
    logger.debug(f"Number of safe reports: {safe_reports}")
    return safe_reports


def part2(data: List[List[int]]) -> int:
    """
    Counts the number of safe reports with the Problem Dampener.

    Args:
        data (list of list of int): The parsed levels from the reports.

    Returns:
        int: The number of safe reports with the Problem Dampener.
    """
    safe_reports_with_dampener = sum(
        1 for report in data if is_safe_with_dampener(report)
    )
    logger.debug(
        f"Number of safe reports with the Problem Dampener: {safe_reports_with_dampener}"
    )
    return safe_reports_with_dampener
