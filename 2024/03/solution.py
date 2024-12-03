#!/usr/bin/env python3
## advent of code 2024
## https://adventofcode.com/2024
## day 03

from typing import List
from my_utils import setup_logging
import re

logger = setup_logging(log_level="INFO")


def parse_input(lines: List[str]) -> List[str]:
    return lines


def part1(data: List[str]) -> int:
    """
    Scans the corrupted memory for valid 'mul(X,Y)' instructions and sums their results.

    Args:
        data (List[str]): The parsed lines from the memory.

    Returns:
        int: The sum of all valid 'mul(X,Y)' results.
    """
    pattern = r"mul\((\d+),(\d+)\)"
    total_sum = 0

    for line in data:
        matches = re.findall(pattern, line)
        for match in matches:
            x, y = map(int, match)
            result = x * y
            logger.debug(f"Found mul({x},{y}) = {result}")
            total_sum += result

    logger.debug(f"Total sum of all valid 'mul(X,Y)' results: {total_sum}")
    return total_sum


def part2(data: List[str]) -> int:
    """
    Handles 'do()' and 'don't()' instructions to enable or disable 'mul(X,Y)' instructions and sums their results.

    Args:
        data (List[str]): The parsed lines from the memory.

    Returns:
        int: The sum of all enabled 'mul(X,Y)' results.
    """
    pattern_mul = r"mul\((\d+),(\d+)\)"
    pattern_do = r"do\(\)"
    pattern_dont = r"don't\(\)"
    total_sum = 0
    enabled = True

    for line in data:
        index = 0
        while index < len(line):
            match_mul = re.search(pattern_mul, line[index:])
            match_do = re.search(pattern_do, line[index:])
            match_dont = re.search(pattern_dont, line[index:])

            # Determine the next instruction to process
            next_instruction = None
            if match_mul:
                next_instruction = ("mul", match_mul)
            if match_do and (
                not next_instruction or match_do.start() < next_instruction[1].start()
            ):
                next_instruction = ("do", match_do)
            if match_dont and (
                not next_instruction or match_dont.start() < next_instruction[1].start()
            ):
                next_instruction = ("dont", match_dont)

            if not next_instruction:
                break

            instruction, match = next_instruction
            index += match.end()

            if instruction == "mul":
                if enabled:
                    x, y = map(int, match.groups())
                    result = x * y
                    logger.debug(f"Found enabled mul({x},{y}) = {result}")
                    total_sum += result
            elif instruction == "do":
                enabled = True
            elif instruction == "dont":
                enabled = False

    logger.debug(f"Total sum of all enabled 'mul(X,Y)' results: {total_sum}")
    return total_sum
