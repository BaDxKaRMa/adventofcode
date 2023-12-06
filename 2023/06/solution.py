#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 06

import os
import sys
import unittest
from math import prod
from typing import List, Tuple

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


class TestParts(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(current_dir, "example_input.txt")
        with open(input_file, "r") as file:
            lines = file.readlines()
        self.input_data = parse_input(lines)

    def test_part1(self):
        self.assertEqual(part1(self.input_data), 288)

    def test_part2(self):
        self.assertEqual(part2(self.input_data), 71503)


def parse_input(lines: List[str]) -> List[Tuple[int, int]]:
    times_line, distances_line = lines[:2]
    times = [int(time) for time in times_line.replace("Time:", "").split()]
    distances = [
        int(distance) for distance in distances_line.replace("Distance:", "").split()
    ]
    races = list(zip(times, distances))
    return races


def is_winner(hold: int, time: int, dist: int) -> bool:
    return hold * (time - hold) > dist


def binary_search_left(time: int, dist: int) -> int:
    low, high = 0, time
    while low < high:
        mid = low + (high - low >> 1)
        if is_winner(mid, time, dist):
            high = mid
        else:
            low = mid + 1
    return low


def binary_search_right(time: int, dist: int) -> int:
    low, high = 0, time
    while low <= high:
        mid = low + (high - low >> 1)
        if is_winner(mid, time, dist):
            low = mid + 1
        else:
            high = mid - 1
    return high


def num_winners(time: int, dist: int) -> int:
    return binary_search_right(time, dist) - binary_search_left(time, dist) + 1


def part1(races: List[Tuple[int, int]]) -> int:
    return prod(num_winners(t, d) for t, d in races)


def part2(races: List[Tuple[int, int]]) -> int:
    t, d = (int("".join(str(x) for x in race)) for race in zip(*races))
    return num_winners(t, d)


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
