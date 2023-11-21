#!/usr/bin/env python3
from functools import cmp_to_key
from loguru import logger


SAMPLE_INPUT = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

# comparing two lists today


try:
    with open("day13.txt") as f:
        data = f.read().strip().split("\n\n")
        logger.info("Using input file")
        logger.debug(f"Input: {data} len: {len(data)}")
except FileNotFoundError:
    data = [list(map(eval, line.split())) for line in SAMPLE_INPUT.split("\n\n")]
    logger.info("Using sample input")
    logger.debug(f"Input: {data} len: {len(data)}")


def compare(a, b):
    if isinstance(a, list) and isinstance(b, int):
        logger.debug(f"Convert {b} to list")
        b = [b]

    if isinstance(a, int) and isinstance(b, list):
        logger.debug(f"Convert {a} to list")
        a = [a]

    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return 1
        if a == b:
            return 0
        return -1

    if isinstance(a, list) and isinstance(b, list):
        i = 0
        while i < len(a) and i < len(b):
            x = compare(a[i], b[i])
            if x == 1:
                return 1
            if x == -1:
                return -1

            i += 1

        if i == len(a):
            if len(a) == len(b):
                return 0
            return 1

        return -1


part1 = 0

for i, block in enumerate(data):
    a, b = map(eval, block.split("\n"))
    logger.debug(f"Checking {a} and {b}")
    if compare(a, b) == 1:
        part1 += i + 1
        logger.debug(f"Adding {i + 1} to answer because {a} > {b}")

logger.info(f"Part 1: {part1}")


# part 2

with open("./day13.txt") as f:
    parts = f.read().strip().replace("\n\n", "\n").split("\n")

lists = list(map(eval, parts))
lists.append([[2]])
lists.append([[6]])
lists = sorted(lists, key=cmp_to_key(compare), reverse=True)


for i, li in enumerate(lists):
    if li == [[2]]:
        a = i + 1
        logger.debug(f"Found 2 at {a}")
    if li == [[6]]:
        b = i + 1
        logger.debug(f"Found 6 at {b}")

logger.info(f"Part 2: {a * b}")
