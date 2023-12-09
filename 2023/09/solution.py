#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 09

import os
import sys
import unittest
from itertools import pairwise

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

    def test_part1_example(self):
        self.assertEqual(
            part1(parse_input(self.read_input_file("example_input.txt"))), 114
        )

    def test_part2_example(self):
        self.assertEqual(
            part2(parse_input(self.read_input_file("example_input.txt"))), 2
        )

    def test_part1_solution(self):
        self.assertEqual(part1(self.input_data), 2005352194)

    def test_part2_solution(self):
        self.assertEqual(part2(self.input_data), 1077)


def parse_input(lines):
    digits = [[int(digit) for digit in line.strip().split()] for line in lines]
    return digits


def extrapolate(sequence):
    extrapolated = sequence[-1]

    while not all(n == 0 for n in sequence):
        sequence = [b - a for a, b in pairwise(sequence)]
        extrapolated += sequence[-1]

    return extrapolated


def part1(data):
    return sum(extrapolate(d) for d in data)


def part2(data):
    return sum(extrapolate(d[::-1]) for d in data)


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
