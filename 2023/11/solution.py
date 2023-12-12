#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 11

import os
import sys
import unittest

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


class TestParts(unittest.TestCase):
    @staticmethod
    def read_input_file(filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(current_dir, filename)
        with open(input_file, "r") as file:
            lines = [line.strip() for line in file]
        return lines

    def setUp(self):
        self.input_data = parse_input(self.read_input_file("input.txt"))
        self.example_data = parse_input(self.read_input_file("example_input.txt"))

    def test_part1_example(self):
        self.assertEqual(part1(parse_input(self.example_data)), 374)

    def test_part2_example(self):
        self.assertEqual(part2(parse_input(self.example_data)), 82000210)

    def test_part1_solution(self):
        self.assertEqual(part1(self.input_data), 9591768)

    def test_part2_solution(self):
        self.assertEqual(part2(self.input_data), 746962097860)


def parse_input(lines):
    return lines


def space(data, scale):
    # find empty rows and columns
    empty_row_indices = [
        row_index for row_index, row in enumerate(data) if all(ch == "." for ch in row)
    ]
    empty_col_indices = [
        col_index
        for col_index, col in enumerate(zip(*data))
        if all(ch == "." for ch in col)
    ]

    occupied_points = [
        (row_index, col_index)
        for row_index, row in enumerate(data)
        for col_index, ch in enumerate(row)
        if ch == "#"
    ]

    total = 0

    for i, (row1, col1) in enumerate(occupied_points):
        for row2, col2 in occupied_points[:i]:
            logger.debug(f"({row1}, {col1}) ({row2}, {col2})")
            # using min and max in case the points are not in order
            for row in range(min(row1, row2), max(row1, row2)):
                total += scale if row in empty_row_indices else 1
            for col in range(min(col1, col2), max(col1, col2)):
                total += scale if col in empty_col_indices else 1
    return total


def part1(data):
    return space(data, scale=2)


def part2(data):
    return space(data, scale=1000000)


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
