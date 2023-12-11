#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 10

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
        self.input_data, self.start = parse_input(self.read_input_file("input.txt"))

    def test_part1_example(self):
        self.input_data, self.start = parse_input(
            self.read_input_file("example_input.txt")
        )
        self.assertEqual(part1(self.input_data, self.start), 8)

    def test_part2_example(self):
        self.input_data, self.start = parse_input(
            self.read_input_file("example_input.txt")
        )
        self.assertEqual(part2(self.input_data, self.start), 1)

    def test_part1_solution(self):
        self.assertEqual(part1(self.input_data, self.start), 6725)

    def test_part2_solution(self):
        self.assertEqual(part2(self.input_data, self.start), 383)


_dirs = "WNES"

_nghbrs = [
    ((-1, 0), "-LFS"),  # W
    ((0, -1), "|7FS"),  # N
    ((1, 0), "-J7S"),  # E
    ((0, 1), "|LJS"),  # S
]

_exits = {"|": "NS", "-": "EW", "L": "NE", "J": "NW", "7": "SW", "F": "SE", "S": "WNES"}


def _get_exits(c, tiles):
    w, h = len(tiles[0]), len(tiles)
    maybe_dirs = _exits[tiles[c[1]][c[0]]]
    for d, pipes in (_nghbrs[i] for i in map(_dirs.index, maybe_dirs)):
        x, y = tuple(map(sum, zip(c, d)))
        if x in range(0, w) and y in range(0, h) and tiles[y][x] in pipes:
            yield (x, y)


def parse_input(lines):
    data = []
    start = None
    for y, l in enumerate(lines):
        data.append(l.strip())
        if "S" in l:
            start = (l.index("S"), y)
    return data, start


def find_exit(data, start, is_part1):
    q = [(c, start, 1, (c[0] - start[0]) * start[1]) for c in _get_exits(start, data)]
    while q:
        c, prev, l, area = q.pop()
        if data[c[1]][c[0]] == "S":
            if is_part1:
                return l // 2
            else:
                return abs(area) - (l // 2) + 1
        q.extend(
            (next, c, l + 1, area + (next[0] - c[0]) * c[1])
            for next in _get_exits(c, data)
            if next != prev  # type: ignore
        )


def part1(data, start):
    return find_exit(data, start, is_part1=True)


def part2(data, start):
    return find_exit(data, start, is_part1=False)


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
