#!/usr/bin/env python3
## advent of code 2024
## https://adventofcode.com/2024
## day 08

from my_utils import setup_logging, Point
from itertools import permutations
from collections import defaultdict

logger = setup_logging(log_level="DEBUG")


def parse_input(lines):
    board = {}
    antennae = defaultdict(set)
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            p = Point(x, y)
            board[p] = c
            if c != ".":
                antennae[c].add(p)
    return board, antennae


def solve(board, antennae, part2=False):
    part_1_antinodes = set()
    part_2_antinodes = set()

    for freq, locs in antennae.items():
        for a, b in permutations(locs, 2):
            for i in range(len(board)):
                antinode = b + (b - a) * i
                part_2_antinodes.add(antinode)
                if i == 1:
                    part_1_antinodes.add(antinode)

    if part2:
        return len(part_2_antinodes & set(board))
    else:
        return len(part_1_antinodes & set(board))


def part1(board, antennae):
    return solve(board, antennae)


def part2(board, antennae):
    return solve(board, antennae, part2=True)
