#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 14

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
        self.assertEqual(part1(self.example_data), 104)

    def test_part2_example(self):
        self.assertEqual(part2(self.example_data), 64)

    def test_part1_solution(self):
        self.assertEqual(part1(self.input_data), 102117)

    def test_part2_solution(self):
        self.assertEqual(part2(self.input_data), 106689)


def parse_input(lines):
    return lines


def part1(data):
    grid1 = list(map("".join, zip(*data)))
    grid1 = [
        "#".join(
            ["".join(sorted(list(group), reverse=True)) for group in row.split("#")]
        )
        for row in grid1
    ]
    grid1 = list(map("".join, zip(*grid1)))
    return sum(row.count("O") * (len(data) - r) for r, row in enumerate(data))


def cycle():
    global grid
    for _ in range(4):
        grid = tuple(map("".join, zip(*grid)))
        grid = tuple(
            "#".join(
                [
                    "".join(sorted(tuple(group), reverse=True))
                    for group in row.split("#")
                ]
            )
            for row in grid
        )
        grid = tuple(row[::-1] for row in grid)


def part2(data):
    global grid
    grid = tuple(data)

    seen = {grid}
    array = [grid]

    iter = 0

    while True:
        iter += 1
        cycle()
        if grid in seen:
            break
        seen.add(grid)
        array.append(grid)

    first = array.index(grid)

    grid = array[(1000000000 - first) % (iter - first) + first]

    return sum(row.count("O") * (len(grid) - r) for r, row in enumerate(grid))


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
