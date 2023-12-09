#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 08

import os
import re
import sys
import unittest
from itertools import count
from math import lcm

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
        self.instructions, self.left, self.right, self.ws = parse_input(
            self.read_input_file("input.txt")
        )

    def test_part1_example(self):
        self.assertEqual(
            part1(self.instructions, self.left, self.right, self.ws), 17263
        )

    def test_part2_example(self):
        self.assertEqual(
            part2(self.instructions, self.left, self.right, self.ws), 14631604759649
        )


def parse_input(lines):
    lines = "\n".join(lines)
    ws = [re.findall(r"\w+", l) for l in lines.strip().split("\n")]
    instructions = ws[0][0]
    left = {start: l for start, l, _ in ws[2:]}
    right = {start: r for start, _, r in ws[2:]}
    logger.debug(f"{instructions=} {left=} {right=} {ws=}")
    return instructions, left, right, ws


def steps(here, instructions, left, right, part1):
    for i in count():
        if here not in left or here not in right:
            raise ValueError(f"Invalid location: {here}")
        here = left[here] if instructions[i % len(instructions)] == "L" else right[here]
        if (part1 and here == "ZZZ") or (not part1 and here[-1] == "Z"):
            return i + 1


def part1(instructions, left, right, _):
    return steps("AAA", instructions, left, right, True)


def part2(instructions, left, right, ws):
    starts = [start for start, _, _ in ws[2:] if start[-1] == "A"]
    return lcm(
        *(steps(start, instructions, left, right, False) or 0 for start in starts)
    )


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
