#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 15

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
        self.input_data = parse_input(self.read_input_file("input.txt"))
        self.example_data = parse_input(self.read_input_file("example_input.txt"))

    def test_part1_example(self):
        self.assertEqual(part1(self.example_data), 1320)

    def test_part2_example(self):
        self.assertEqual(part2(self.example_data), 145)

    def test_part1_solution(self):
        self.assertEqual(part1(self.input_data), 510273)

    def test_part2_solution(self):
        self.assertEqual(part2(self.input_data), 212449)


def parse_input(lines):
    return lines[0].split(",")


def hash_string(s):
    result = 0

    for char in s:
        result += ord(char)
        result *= 17
        result %= 256

    return result


def part1(data):
    return sum(map(hash_string, data))


def part2(data):
    boxes = [[] for _ in range(256)]
    focal_lengths = {}

    for instruction in data:
        if "-" in instruction:
            label = instruction[:-1]
            index = hash_string(label)
            if label in boxes[index]:
                boxes[index].remove(label)
        else:
            label, length = instruction.split("=")
            length = int(length)

            index = hash_string(label)
            if label not in boxes[index]:
                boxes[index].append(label)

            focal_lengths[label] = length

    total = 0

    for box_number, box in enumerate(boxes, 1):
        for lens_slot, label in enumerate(box, 1):
            total += box_number * lens_slot * focal_lengths[label]

    return total


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
