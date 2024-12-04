#!/usr/bin/env python3
## advent of code 2024
## https://adventofcode.com/2024
## day 04

from typing import List
from my_utils import setup_logging
import re

logger = setup_logging(log_level="INFO")


def parse_input(lines: List[str]) -> List[str]:
    return lines


def part1(data: List[str]) -> int:
    text = "\n".join(data)
    line_length = len(data[0])
    rotations = [0, line_length, line_length + 1, line_length - 1]

    xmas_pattern = "|".join(
        rf"(?=(X(?:.{{{r}}})M(?:.{{{r}}})A(?:.{{{r}}})S))|(?=(S(?:.{{{r}}})A(?:.{{{r}}})M(?:.{{{r}}})X))"
        for r in rotations
    )

    return sum(
        [
            len(re.findall(pattern, text, flags=re.DOTALL))
            for pattern in xmas_pattern.split("|")
        ]
    )


def part2(data: List[str]) -> int:
    text = "\n".join(data)
    line_length = len(data[0])

    x_mas_pattern = rf"(?=(M.S.{{{line_length - 1}}}A.{{{line_length - 1}}}M.S))|(?=(S.M.{{{line_length - 1}}}A.{{{line_length - 1}}}S.M))|(?=(S.S.{{{line_length - 1}}}A.{{{line_length - 1}}}M.M))|(?=(M.M.{{{line_length - 1}}}A.{{{line_length - 1}}}S.S))"

    return len(re.findall(x_mas_pattern, text, flags=re.DOTALL))
