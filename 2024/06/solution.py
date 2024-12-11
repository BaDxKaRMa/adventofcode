#!/usr/bin/env python3
## advent of code 2024
## https://adventofcode.com/2024
## day 06

from typing import List, Tuple, Dict, Set
from my_utils import setup_logging

logger = setup_logging(log_level="DEBUG")


def parse_input(lines: List[str]) -> Dict[complex, str]:
    return {i + j * 1j: c for i, r in enumerate(lines) for j, c in enumerate(r.strip())}


def walk(grid: Dict[complex, str], start: complex) -> Tuple[Set[complex], bool]:
    position, direction, seen = start, -1, set()
    logger.debug(
        f"Starting walk at position {position} with initial direction {direction}"
    )
    while position in grid and (position, direction) not in seen:
        seen |= {(position, direction)}
        logger.debug(f"Visiting position {position} with direction {direction}")
        if grid.get(position + direction) == "#":
            direction *= -1j  # Change direction on obstacle
            logger.debug(
                f"Encountered obstacle at {position + direction}, changing direction to {direction}"
            )
        else:
            position += direction  # Move to the next position
            logger.debug(f"Moving to position {position}")
    return {p for p, _ in seen}, (position, direction) in seen


def part1(data: Dict[complex, str]) -> int:
    start = min([p for p in data if data[p] == "^"])
    path = walk(data, start)[0]
    return len(path)


def part2(data: Dict[complex, str]) -> int:
    start = min(p for p in data if data[p] == "^")
    path = walk(data, start)[0]
    return sum(walk(data | {o: "#"}, start)[1] for o in path)
