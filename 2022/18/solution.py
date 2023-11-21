#!/usr/bin/env python3

from pathlib import Path
import numpy as np
from functools import lru_cache

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "day18.txt")

SAMPLE_INPUT = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


try:
    with INPUT_FILE.open() as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = SAMPLE_INPUT.splitlines()


def parse_lines(raw):
    min_coord = 1 << 60
    max_coord = -(1 << 60)
    parsed_lines = set()
    for line in raw:
        x, y, z = map(int, line.split(","))
        parsed_lines.add((x, y, z))
        for num in [x, y, z]:
            min_coord = min(min_coord, num)
            max_coord = max(max_coord, num)
    return parsed_lines, min_coord, max_coord


def part1(lines):
    exposed_sides = 0
    for x, y, z in lines:
        covered = 0

        pos = np.array((x, y, z))

        for coord in range(3):
            dpos = np.array([0, 0, 0])
            dpos[coord] = 1

            dneg = np.array([0, 0, 0])
            dneg[coord] = -1

            covered += tuple(pos + dpos) in lines
            covered += tuple(pos + dneg) in lines
        exposed_sides += 6 - covered
    return exposed_sides


@lru_cache(None)
def exposed(pos):
    # do a DFS
    stack = [pos]
    seen = set()

    if pos in lines:
        return False

    while len(stack) > 0:
        pop = stack.pop()

        if pop in lines:
            continue

        for coord in range(3):
            if not (min_coord <= pop[coord] <= max_coord):
                return True

        if pop in seen:
            continue
        seen.add(pop)

        for coord in range(3):
            dpos = np.array([0, 0, 0])
            dpos[coord] = 1
            dneg = np.array([0, 0, 0])
            dneg[coord] = -1

            stack.append(tuple(pop + dpos))
            stack.append(tuple(pop + dneg))

    return False


def part2(lines, min_coord, max_coord):
    part2_answer = 0
    cache = {}

    for x, y, z in lines:
        for num in [x, y, z]:
            min_coord = min(min_coord, num)
            max_coord = max(max_coord, num)

    for x, y, z in lines:
        covered = 0

        pos = np.array((x, y, z))

        for coord in range(3):
            dpos = np.array([0, 0, 0])
            dpos[coord] = 1

            dneg = np.array([0, 0, 0])
            dneg[coord] = -1

            for nbr in [tuple(pos + dpos), tuple(pos + dneg)]:
                if nbr in cache:
                    part2_answer += cache[nbr]
                else:
                    result = exposed(nbr)
                    cache[nbr] = result
                    part2_answer += result

    return part2_answer

parsed_lines, min_coord, max_coord = parse_lines(lines)
print(f"Part 1: {part1(parsed_lines)}")
print(f"Part 2: {part2(parsed_lines, min_coord, max_coord)}")
