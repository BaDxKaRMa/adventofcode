#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 13

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
        self.assertEqual(part1(self.example_data), 405)

    def test_part2_example(self):
        self.assertEqual(part2(self.example_data), 400)

    def test_part1_solution(self):
        self.assertEqual(part1(self.input_data), 30158)

    def test_part2_solution(self):
        self.assertEqual(part2(self.input_data), 36474)


def parse_input(lines):
    grids = []
    lines = "\n".join(lines)
    for block in lines.split("\n\n"):
        grids.append(block.splitlines())
    return grids


def find_mirror(grid, part):
    for r in range(1, len(grid)):
        above = grid[:r][::-1]
        below = grid[r:]

        if part == 1:
            above = above[: len(below)]
            below = below[: len(above)]

            if above == below:
                return r
        elif part == 2:
            if (
                sum(
                    sum(0 if a == b else 1 for a, b in zip(x, y))
                    for x, y in zip(above, below)
                )
                == 1
            ):
                return r
        else:
            raise ValueError("Invalid mode. There are only 2 parts.")

    return 0


def part1(data):
    total = 0
    for grid in data:
        row = find_mirror(grid, 1)
        total += row * 100

        col = find_mirror(list(zip(*grid)), 1)
        total += col
    return total


def part2(data):
    total = 0
    for grid in data:
        row = find_mirror(grid, 2)
        total += row * 100

        col = find_mirror(list(zip(*grid)), 2)
        total += col
    return total


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
