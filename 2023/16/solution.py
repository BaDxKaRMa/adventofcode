#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 16

import os
import sys
import unittest
from collections import deque

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
        self.assertEqual(part1(self.example_data), 46)

    def test_part2_example(self):
        self.assertEqual(part2(self.example_data), 51)

    def test_part1_solution(self):
        self.assertEqual(part1(self.input_data), 6361)

    def test_part2_solution(self):
        self.assertEqual(part2(self.input_data), 6701)


def parse_input(lines):
    return lines


def part1(data):
    # r, c, dr, dc
    a = [(0, -1, 0, 1)]
    seen = set()
    q = deque(a)

    while q:
        r, c, dr, dc = q.popleft()

        r += dr
        c += dc

        if r < 0 or r >= len(data) or c < 0 or c >= len(data[0]):
            continue

        ch = data[r][c]

        if ch == "." or (ch == "-" and dc != 0) or (ch == "|" and dr != 0):
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))  # type: ignore
        elif ch == "/":
            dr, dc = -dc, -dr
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))  # type: ignore
        elif ch == "\\":
            dr, dc = dc, dr
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))  # type: ignore
        else:
            for dr, dc in [(1, 0), (-1, 0)] if ch == "|" else [(0, 1), (0, -1)]:
                if (r, c, dr, dc) not in seen:
                    seen.add((r, c, dr, dc))
                    q.append((r, c, dr, dc))  # type: ignore

    coords = {(r, c) for (r, c, _, _) in seen}

    return len(coords)


def part2(data):
    def calc(r, c, dr, dc):
        # r, c, dr, dc
        a = [(r, c, dr, dc)]
        seen = set()
        q = deque(a)

        while q:
            r, c, dr, dc = q.popleft()

            r += dr
            c += dc

            if r < 0 or r >= len(data) or c < 0 or c >= len(data[0]):
                continue

            ch = data[r][c]

            if ch == "." or (ch == "-" and dc != 0) or (ch == "|" and dr != 0):
                if (r, c, dr, dc) not in seen:
                    seen.add((r, c, dr, dc))
                    q.append((r, c, dr, dc))
            elif ch == "/":
                dr, dc = -dc, -dr
                if (r, c, dr, dc) not in seen:
                    seen.add((r, c, dr, dc))
                    q.append((r, c, dr, dc))
            elif ch == "\\":
                dr, dc = dc, dr
                if (r, c, dr, dc) not in seen:
                    seen.add((r, c, dr, dc))
                    q.append((r, c, dr, dc))
            else:
                for dr, dc in [(1, 0), (-1, 0)] if ch == "|" else [(0, 1), (0, -1)]:
                    if (r, c, dr, dc) not in seen:
                        seen.add((r, c, dr, dc))
                        q.append((r, c, dr, dc))

        coords = {(r, c) for (r, c, _, _) in seen}

        return len(coords)

    max_val = 0

    for r in range(len(data)):
        max_val = max(max_val, calc(r, -1, 0, 1))
        max_val = max(max_val, calc(r, len(data[0]), 0, -1))

    for c in range(len(data)):
        max_val = max(max_val, calc(-1, c, 1, 0))
        max_val = max(max_val, calc(len(data), c, -1, 0))
    return max_val


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
