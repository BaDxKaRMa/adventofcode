#!/usr/bin/env python3
# advent of code 2021
# https://adventofcode.com/2021
# day 02

import sys
from loguru import logger


logger.remove()
logger.add(sys.stderr, level="INFO")


def parse_input(lines):
    return [(d, int(v)) for d, v in [line.split() for line in lines]]


def dive(pos, direction, value):
    if direction == "down":
        pos += value
        return pos
    elif direction == "up":
        pos -= value
        return pos


def turn(pos, direction, value):
    if direction == "forward":
        pos += value
        return pos


def part1(data):
    horizontal = 0
    depth = 0
    for d, v in data:
        if d == "forward":
            horizontal = turn(horizontal, d, v)
        elif d == "down" or d == "up":
            depth = dive(depth, d, v)
    answer = horizontal * depth
    return answer


def part2(data):
    horizontal = 0
    depth = 0
    aim = 0
    for d, v in data:
        if d == "down":
            aim += v
        elif d == "up":
            aim -= v
        elif d == "forward":
            horizontal += v
            depth += aim * v
    answer = horizontal * depth
    return answer
