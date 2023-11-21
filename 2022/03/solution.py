#!/usr/bin/env python3
import sys

SAMPLE_INPUT = [
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw",
]


def _parse_into_list(file) -> list:
    try:
        with open(file, "r") as f:
            input_file = f.read()
            input_file = input_file.splitlines()
            return input_file
    except FileNotFoundError:
        print("File not found")


def _score(item):
    if "a" <= item <= "z":
        return ord(item) - 96
    if "A" <= item <= "Z":
        return ord(item) - 38
    raise RuntimeError(f"not ok: {item}")


def part1(lines):
    """
    >>> part1(SAMPLE_INPUT)
    157
    """
    total = 0
    for line in lines:
        line = line.strip()
        for item in set(line[: len(line) // 2]).intersection(line[len(line) // 2 :]):
            total += _score(item)
    return total


def part2(lines):
    """
    >>> part2(SAMPLE_INPUT)
    70
    """
    total = 0
    for first, second, third in zip(*(map(str.strip, lines),) * 3):
        total += _score(set(first).intersection(second).intersection(third).pop())
    return total


parts = (part1, part2)

for i, part in enumerate(parts, 1):
    try:
        print(f"Part {i}: {part(_parse_into_list('day3.txt'))}")
    except TypeError:
        import doctest

        doctest.testmod()
