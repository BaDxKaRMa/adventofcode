#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 03

import sys
import unittest
from collections import defaultdict
from typing import List, Set, Tuple

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


class TestParts(unittest.TestCase):
    def setUp(self):
        self.input_data = [
            "467..114..",
            "...*......",
            "..35..633.",
            "......#...",
            "617*......",
            ".....+.58.",
            "..592.....",
            "......755.",
            "...$.*....",
            ".664.598..",
        ]

    def test_part1(self):
        self.assertEqual(part1(self.input_data), 4361)

    def test_part2(self):
        self.assertEqual(part2(self.input_data), 467835)


def parse_input(lines):
    return lines


def part1(data: List[str]) -> int:
    # Define the set of symbols
    SYMBOLS: Set[str] = {"/", "+", "#", "$", "-", "&", "%", "=", "@", "*"}

    # Get the height and length of the schematic
    schema_height: int = len(data) - 1
    schema_length: int = len(data[0]) - 1

    # Define a helper function to get the symbols near a given cell
    def _get_nearest_symbols(self_x: int, self_y: int, self_l: int) -> Set[str]:
        # Calculate the boundaries of the area to check
        x_0: int = max(0, self_x - self_l)
        y_0: int = max(0, self_y - 1)
        x_1: int = min(schema_length, self_x + 1)
        y_1: int = min(schema_height, self_y + 1)

        # Return the set of characters in the area
        return set(
            data[y_0][x_0 : x_1 + 1]
            + data[self_y][x_0 : x_1 + 1]
            + data[y_1][x_0 : x_1 + 1]
        )

    # Initialize the sum of part numbers
    part_numbers_sum: int = 0

    # Iterate over each line in the data
    for y, line in enumerate(data):
        # Initialize an empty string to hold the current number
        number_chunk: str = ""

        # Iterate over each character in the line
        for x, char in enumerate(line):
            # If the character is a digit, add it to the current number
            if char.isdigit():
                number_chunk += char

                # If we're at the end of the line or the next character is not a digit
                if x == schema_length or not line[x + 1].isdigit():
                    # Get the symbols near the current cell
                    nearest_symbols: Set[str] = _get_nearest_symbols(
                        x, y, len(number_chunk)
                    )

                    # If any of the symbols are in the set of symbols
                    if SYMBOLS.intersection(nearest_symbols):
                        # Convert the current number to an integer and add it to the sum
                        part_number: int = int(number_chunk)
                        part_numbers_sum += part_number
                        logger.debug(f"Added part number {part_number} to the sum.")

                    # Reset the current number
                    number_chunk = ""
    logger.success(f"Part numbers sum: {part_numbers_sum}")
    return part_numbers_sum


def part2(data: List[str]) -> int:
    # Get the height and length of the schematic
    schema_height: int = len(data) - 1
    schema_length: int = len(data[0]) - 1

    # Define a helper function to find the positions of gears near a given cell
    def _find_gear_positions(
        self_x: int, self_y: int, self_l: int
    ) -> Set[Tuple[int, int]]:
        # Calculate the boundaries of the area to check
        x_0: int = max(0, self_x - self_l)
        y_0: int = max(0, self_y - 1)
        x_1: int = min(schema_length, self_x + 2)
        y_1: int = min(schema_height, self_y + 2)

        # Return the set of positions in the area that contain a gear
        return {
            (y, x)
            for y in range(y_0, y_1)
            for x in range(x_0, x_1)
            if data[y][x] == "*"
        }

    # Initialize a dictionary to map gear positions to part numbers
    gear_pos_num_map = defaultdict(list)

    # Iterate over each line in the data
    for y, line in enumerate(data):
        # Initialize an empty string to hold the current number
        number_chunk: str = ""

        # Iterate over each character in the line
        for x, char in enumerate(line):
            # If the character is a digit, add it to the current number
            if char.isdigit():
                number_chunk += char

                # If we're at the end of the line or the next character is not a digit
                if x == schema_length or not line[x + 1].isdigit():
                    # Find the positions of gears near the current cell
                    for position in _find_gear_positions(x, y, len(number_chunk)):
                        # Add the current number to the list of part numbers for each gear position
                        gear_pos_num_map[position].append(int(number_chunk))
                        logger.debug(
                            f"Added part number {number_chunk} to gear at {position}"
                        )

                    # Reset the current number
                    number_chunk = ""

    # Return the sum of the product of the two part numbers for each gear position that has exactly two part numbers
    answer = sum((v[0] * v[1] for v in gear_pos_num_map.values() if len(v) == 2))
    logger.success(f"Part numbers product sum: {answer}")
    return answer


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.\n")
    unittest.main()
