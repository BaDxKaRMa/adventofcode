#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 12

import os
import sys
import unittest
from functools import lru_cache
from typing import Tuple

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
        self.assertEqual(part1(*self.example_data), 21)

    def test_part2_example(self):
        self.assertEqual(part2(*self.example_data), 525152)

    def test_part1_solution(self):
        self.assertEqual(part1(*self.input_data), 7204)

    def test_part2_solution(self):
        self.assertEqual(part2(*self.input_data), 1672318386674)


def parse_input(lines):
    records = []
    damaged_springs = []
    for line in lines:
        record, damaged_spring = line.split(" ")
        records.append(record)
        damaged_springs.append([int(spring) for spring in damaged_spring.split(",")])
        logger.debug(f"Record: {records[-1]}, Damaged Springs: {damaged_springs[-1]}")
    return records, damaged_springs


@lru_cache
def recursive_arrangements(pixels: str, groups: Tuple[int]):
    if len(pixels) == 0:
        return 1 if len(groups) == 0 else 0
    if pixels.startswith("."):
        return recursive_arrangements(pixels.strip("."), groups)
    if pixels.startswith("?"):
        return recursive_arrangements(
            pixels.replace("?", ".", 1), groups
        ) + recursive_arrangements(pixels.replace("?", "#", 1), groups)
    if pixels.startswith("#"):
        if len(groups) == 0:
            return 0
        if len(pixels) < groups[0]:
            return 0
        if any(c == "." for c in pixels[0 : groups[0]]):
            return 0
        if len(groups) > 1:
            if len(pixels) < groups[0] + 1 or pixels[groups[0]] == "#":
                return 0
            return recursive_arrangements(pixels[groups[0] + 1 :], tuple(groups[1:]))
        else:
            return recursive_arrangements(pixels[groups[0] :], tuple(groups[1:]))
    raise Exception("no other branches possible")


def part1(records, damaged_springs):
    total = 0
    for record, counts in zip(records, damaged_springs):
        counts = tuple(counts)
        total += recursive_arrangements(record, counts)
    return total


def part2(records, damaged_springs):
    total = 0
    for record, counts in zip(records, damaged_springs):
        counts = tuple(counts)
        record = "?".join([record] * 5)
        counts = counts * 5
        total += recursive_arrangements(record, counts)
    return total


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
