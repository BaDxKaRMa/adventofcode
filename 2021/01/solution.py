#!/usr/bin/env python3
# advent of code 2021
# https://adventofcode.com/2021
# day 01

import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


def parse_input(lines):
    return [int(i) for i in lines]


def part1(data):
    answer = 0
    prev = data[0]
    for i in data[1:]:
        if i > prev:
            answer += 1
        prev = i
    return answer


def part2(data):
    windows = [sum(i) for i in zip(data, data[1:], data[2:])]
    pairs = zip(windows, windows[1:])
    answer = [b - a for a, b in pairs if b - a > 0]
    return len(answer)
