#!/usr/bin/env python3
from utils import _parse_into_list
from re import match, compile

SAMPLE_INPUT = [
    "2-4,6-8",
    "2-3,4-5",
    "5-7,7-9",
    "2-8,3-7",
    "6-6,4-6",
    "2-6,4-8",
]


def compare_ranges(lines):
    part1 = 0
    part2 = 0
    for line in lines:
        left_elf, right_elf = line.split(",")
        L1, L2 = left_elf.split("-")
        R1, R2 = right_elf.split("-")
        L1, L2, R1, R2 = [int(x) for x in [L1, L2, R1, R2]]
        if L1 <= R1 and R2 <= L2 or R1 <= L1 and L2 <= R2:
            part1 += 1
        if not (L2 < R1 or L1 > R2):
            part2 += 1
    return part1, part2


def test_compare_ranges():
    assert compare_ranges(SAMPLE_INPUT) == (2, 4)


try:
    with open("day4.txt") as f:
        INPUT = f.read().splitlines()
except FileNotFoundError:
    INPUT = SAMPLE_INPUT

part1, part2 = compare_ranges(INPUT)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
