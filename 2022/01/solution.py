#!/usr/bin/env python3

SAMPLE_INPUT = [
    "1000",
    "2000",
    "3000",
    "",
    "4000",
    "",
    "5000",
    "6000",
    "",
    "7000",
    "8000",
    "9000",
    "",
    "10000",
]

try:
    with open("day1.txt", "r") as f:
        input_file = f.read().splitlines()
except FileNotFoundError:
    input_file = SAMPLE_INPUT


def _parse(lines):
    sums = []
    elf = 0
    for line in lines:
        line = line.strip()
        if line:
            elf += int(line)
        else:
            sums.append(elf)
            elf = 0
    sums.append(elf)
    return sums


def part1(lines):
    """
    >>> part1(SAMPLE_INPUT)
    24000
    """
    return max(_parse(lines))


def part2(lines):
    """
    >>> part2(SAMPLE_INPUT)
    45000
    """
    return sum(sorted(_parse(lines))[-3:])


parts = (part1, part2)

for i, part in enumerate(parts, 1):
    print(f"Part {i}: {part(input_file)}")
