#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 07

import os
import sys
import unittest
from typing import Any, Dict, List, Tuple

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


class TestParts(unittest.TestCase):
    @staticmethod
    def read_input_file(filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(current_dir, filename)
        with open(input_file, "r") as file:
            lines = file.readlines()
        return lines

    def setUp(self):
        self.input_data = parse_input(self.read_input_file("example_input.txt"))

    def test_part1_example(self):
        self.assertEqual(part1(self.input_data), 6440)

    def test_part1_solution(self):
        self.assertEqual(
            part1(parse_input(self.read_input_file("input.txt"))), 249726565
        )

    def test_part2_example(self):
        self.assertEqual(part2(self.input_data), 5905)

    def test_part2_solution(self):
        self.assertEqual(
            part2(parse_input(self.read_input_file("input.txt"))), 251135960
        )


def score(hand: List[str], part: int = 1) -> int:
    if part == 2:
        # Replace 'J' with the most frequent card that is not 'J'
        most_frequent_card = max(
            set(hand), key=lambda card: (card != "J", hand.count(card))
        )
        hand = [card if card != "J" else most_frequent_card for card in hand]

    counts = [hand.count(card) for card in hand]

    if 5 in counts:  # 5 of a kind
        return 6
    if 4 in counts:  # 4 of a kind
        return 5
    if 3 in counts:  # 3 of a kind
        if 2 in counts:  # full house
            return 4
        return 3
    if counts.count(2) == 4:  # 2 pairs
        return 2
    if 2 in counts:  # 1 pair
        return 1
    return 0  # high card


def strength(hand: List[str], letter_map: Dict[str, str] = {}) -> Tuple[int, List[str]]:
    if "J" in letter_map and letter_map["J"] == ".":
        return (score(hand, part=2), [letter_map.get(card, card) for card in hand])
    else:
        return (score(hand), [letter_map.get(card, card) for card in hand])


def parse_input(lines):
    plays = []
    for line in lines:
        hand, bid = line.split()
        plays.append((hand, int(bid)))

    return plays


def part1(plays):
    letter_map = {"T": "A", "J": "B", "Q": "C", "K": "D", "A": "E"}
    total = 0
    plays.sort(key=lambda play: strength(play[0], letter_map))

    for rank, (hand, bid) in enumerate(plays, 1):
        total += rank * bid

    return total


def part2(plays):
    letter_map = {"T": "A", "J": ".", "Q": "C", "K": "D", "A": "E"}
    total = 0

    plays.sort(key=lambda play: strength(play[0], letter_map))

    for rank, (hand, bid) in enumerate(plays, 1):
        total += rank * bid

    return total


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
