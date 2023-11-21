#!/usr/bin/env python3
# advent of code 2021
# https://adventofcode.com/2021
# day 05


import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


def parse_input(lines) -> list:
    instructions = []
    for line in lines:
        left, right = line.split(" -> ")
        instructions.append((left.split(","), right.split(",")))
    return instructions


def part1(data):
    for x in data:
        p1, p2 = x
        x1, y1 = p1
        x2, y2 = p2
        print(f"{x1}, {y1}, {x2}, {y2}")
    return data


def part2(data):
    pass
