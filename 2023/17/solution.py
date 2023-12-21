#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 17

import os
import sys
import unittest
from heapq import heappop, heappush

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
        self.assertEqual(part1(self.example_data), 102)

    def test_part2_example(self):
        self.assertEqual(part2(self.example_data), 94)

    def test_part1_solution(self):
        self.assertEqual(part1(self.input_data), 1023)

    def test_part2_solution(self):
        self.assertEqual(part2(self.input_data), 1165)


def parse_input(lines):
    return [list(map(int, line.strip())) for line in lines]


def part1(data):
    seen = set()
    priority_queue = [(0, 0, 0, 0, 0, 0)]
    heatloss = 0
    while priority_queue:
        heatloss, r, c, dr, dc, n = heappop(priority_queue)

        if r == len(data) - 1 and c == len(data[0]) - 1:
            break

        if (r, c, dr, dc, n) in seen:
            continue

        seen.add((r, c, dr, dc, n))

        if n < 3 and (dr, dc) != (0, 0):
            nr = r + dr
            nc = c + dc
            if 0 <= nr < len(data) and 0 <= nc < len(data[0]):
                heappush(priority_queue, (heatloss + data[nr][nc], nr, nc, dr, dc, n + 1))  # type: ignore

        for ndr, ndc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (ndr, ndc) != (dr, dc) and (ndr, ndc) != (-dr, -dc):
                nr = r + ndr
                nc = c + ndc
                if 0 <= nr < len(data) and 0 <= nc < len(data[0]):
                    heappush(priority_queue, (heatloss + data[nr][nc], nr, nc, ndr, ndc, 1))  # type: ignore

    return heatloss


def part2(data):
    seen = set()
    priority_queue = [(0, 0, 0, 0, 0, 0)]
    heatloss = 0

    while priority_queue:
        heatloss, r, c, dr, dc, n = heappop(priority_queue)

        if r == len(data) - 1 and c == len(data[0]) - 1 and n >= 4:
            break

        if (r, c, dr, dc, n) in seen:
            continue

        seen.add((r, c, dr, dc, n))

        if n < 10 and (dr, dc) != (0, 0):
            nr = r + dr
            nc = c + dc
            if 0 <= nr < len(data) and 0 <= nc < len(data[0]):
                heappush(priority_queue, (heatloss + data[nr][nc], nr, nc, dr, dc, n + 1))  # type: ignore

        if n >= 4 or (dr, dc) == (0, 0):
            for ndr, ndc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if (ndr, ndc) != (dr, dc) and (ndr, ndc) != (-dr, -dc):
                    nr = r + ndr
                    nc = c + ndc
                    if 0 <= nr < len(data) and 0 <= nc < len(data[0]):
                        heappush(priority_queue, (heatloss + data[nr][nc], nr, nc, ndr, ndc, 1))  # type: ignore
    return heatloss


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
