#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 01

import sys
import unittest

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


class TestParts(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(
            part1(["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]), 142
        )

    def test_part2(self):
        self.assertEqual(
            part2(
                [
                    "two1nine",
                    "eightwothree",
                    "abcone2threexyz",
                    "xtwone3four",
                    "4nineeightseven2",
                    "zoneight234",
                    "7pqrstsixteen",
                ]
            ),
            281,
        )


def parse_input(lines):
    return lines


def part1(data):
    """
    Part 1: On each line, combine the first digit then the last digit found.
    Then sum those values and return it. Each line will be a mix of letters
    and numbers. Only use the numbers.
    """
    list_of_digits = []
    logger.debug(f"Loaded {len(data)} lines of input")

    for line in data:
        digits = [char for char in line if char.isdigit()]
        if digits:
            first_digit = digits[0]
            last_digit = digits[-1]
            logger.debug(f"First digit: {first_digit}, Last digit: {last_digit}")
            # combine first and last into a double digit number
            list_of_digits.append(int(first_digit + last_digit))
            logger.debug(f"Combined digits: {digits}")

        else:
            logger.debug("No digits found in this line.")

    logger.debug(f"List of digits in lines: {list_of_digits}")
    return sum(list_of_digits)


def part2(data):
    """
    Part 2: Your calculation isn't quite right. It looks like some of the
    digits are actually spelled out with letters: one, two, three, four, five,
    six, seven, eight, and nine also count as valid "digits".
    """
    valid_digits = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    val = 0
    sumvals = 0

    for line in data:
        line = line.strip()
        first = last = None
        str = ""
        for char in line:
            if char >= "0" and char <= "9":
                if not first:
                    first = char
                last = char
                str = ""
                continue
            str += char
            for sp, sp_c in valid_digits.items():
                if len(str) >= len(sp) and str[len(str) - len(sp) :] == sp:
                    if not first:
                        first = sp_c
                    last = sp_c
        val = int(first + last)
        logger.debug(f"In line {line}, val is {val}")
        sumvals += val

    return sumvals


if __name__ == "__main__":
    unittest.main()
