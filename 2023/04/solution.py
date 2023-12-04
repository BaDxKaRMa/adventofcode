#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 04

import sys
import unittest
from loguru import logger


logger.remove()
logger.add(sys.stderr, level="INFO")


class TestParts(unittest.TestCase):
    def setUp(self):
        self.input_data = parse_input(
            [
                "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
                "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
                "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
                "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
                "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
                "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
            ]
        )

    def test_part1(self):
        pass
        self.assertEqual(part1(self.input_data), 13)

    def test_part2(self):
        pass
        self.assertEqual(part2(self.input_data), 30)


def parse_input(lines):
    cards = {}
    for i, line in enumerate(lines, start=1):
        winningSet = set()
        cardSet = set()

        _, cardNumbers = line.split(":")
        cardNumbers = cardNumbers.split(" | ")
        winningSet = set(cardNumbers[0].split())
        cardSet = set(cardNumbers[1].split())

        cards[i] = (winningSet, cardSet)
    return cards


def part1(data):
    sum = 0

    for _, (winningSet, cardSet) in data.items():
        matches = winningSet.intersection(cardSet)

        if len(matches) > 0:
            cardScore = 1
            for _ in range(len(matches) - 1):
                cardScore *= 2
        else:
            cardScore = 0

        sum += cardScore
    return sum


def part2(data):
    multipliers = {i: 1 for i in data.keys()}

    for index, (winningSet, cardSet) in data.items():
        matchCount = len(winningSet.intersection(cardSet))

        logger.debug(f"matches: {matchCount}")

        for x in range(index + 1, index + 1 + matchCount):
            if x in multipliers:
                multipliers[x] += 1 * multipliers[index]

    return sum(multipliers.values())


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
