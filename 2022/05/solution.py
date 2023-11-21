#!/usr/bin/env python3

from re import findall
from collections import defaultdict

SAMPLE_INPUT = [
    "    [D]    ",
    "[N] [C]    ",
    "[Z] [M] [P]",
    " 1   2   3 ",
    "",
    "move 1 from 2 to 1",
    "move 3 from 1 to 3",
    "move 2 from 2 to 1",
    "move 1 from 1 to 2",
]

stacks = defaultdict(list)


def run(lines, part):
    for line in lines:
        if "[" in line:
            for i in range(1, len(line) - 1, 4):
                if line[i] != " ":
                    stacks[(i - 1) // 4].append(line[i])
        elif line.startswith("move"):
            a, b, c = map(int, findall(r"\d+", line))
            if part == 1:
                stacks[c - 1] = stacks[b - 1][:a][::-1] + stacks[c - 1]
            elif part == 2:
                stacks[c - 1] = stacks[b - 1][:a] + stacks[c - 1]
            stacks[b - 1] = stacks[b - 1][a:]
    return stacks


def test_run():
    run(SAMPLE_INPUT, 1)
    assert "".join(stacks[i][0] for i in range(len(stacks))) == "DCN"


try:
    run(open("day5.txt"), 1)
except FileNotFoundError:
    run(SAMPLE_INPUT, 1)
print("Part 1:", "".join(stacks[i][0] for i in range(len(stacks))))

stacks = defaultdict(list)

try:
    run(open("day5.txt"), 2)
except FileNotFoundError:
    run(SAMPLE_INPUT, 2)
print("Part 2:", "".join(stacks[i][0] for i in range(len(stacks))))
