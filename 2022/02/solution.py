#!/usr/bin/env python3


SAMPLE_INPUT = ["A Y", "B X", "C Z"]

try:
    with open("day2.txt", "r") as f:
        input_file = f.read().splitlines()
except FileNotFoundError:
    input_file = SAMPLE_INPUT

# Unicode hacks lul
# 65-90 = A-Z


def part1(lines):
    """
    >>> part1(SAMPLE_INPUT)
    15
    """
    return sum(
        ((p2 - p1 + 1) % 3) * 3 + p2
        for (p1, p2) in ((ord(line[0]) - 64, ord(line[2]) - 87) for line in lines)
    )


def part2(lines):
    """
    >>> part2(SAMPLE_INPUT)
    12
    """
    return sum(
        win * 3 + (p1 + win - 2) % 3 + 1
        for (p1, win) in ((ord(line[0]) - 64, ord(line[2]) - 88) for line in lines)
    )


parts = (part1, part2)

for i, part in enumerate(parts, 1):
    print(f"Part {i}: {part(input_file)}")
