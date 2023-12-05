#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 04

import os
import sys
import unittest

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
        self.assertEqual(part1(self.input_data), 13)

    def test_part2(self):
        self.assertEqual(part2(self.input_data), 30)


def parse_input(lines):
    cards = {}
    for i, line in enumerate(lines, start=1):
        _, cardNumbers = line.split(":")
        winningSet, cardSet = [
            set(numbers.split()) for numbers in cardNumbers.split(" | ")
        ]

        cards[i] = (winningSet, cardSet)
    return cards


def part1(data):
    total_score = 0

    for _, (winningSet, cardSet) in data.items():
        matches = winningSet.intersection(cardSet)
        cardScore = pow(2, len(matches) - 1) if matches else 0
        total_score += cardScore

    return total_score


def part2(data):
    multipliers = [1] * len(data)

    for index, (winningSet, cardSet) in data.items():
        matchCount = len(winningSet.intersection(cardSet))

        logger.debug(f"matches: {matchCount}")

        for x in range(index + 1, index + 1 + matchCount):
            if x < len(multipliers):
                multipliers[x] += multipliers[index]

    return sum(multipliers)


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
