#!/usr/bin/env python3
# Day 9 Advent of Code 2022
# https://adventofcode.com/2022/day/9

import os
from utils import parse_args, setup_logging

SAMPLE_INPUT = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

offset = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}


def load_input():
    if os.path.exists("day9.txt"):
        with open(os.path.join(os.path.dirname(__file__), "day9.txt")) as f:
            input_data = f.read().splitlines()
            logger.debug(f"Loaded day9.txt: {input_data}")
    else:
        input_data = SAMPLE_INPUT.splitlines()
        logger.debug(f"Loaded sample input: {input_data}")
    return input_data


def parse_instructions(input_data):
    parsed_instructions = []
    for line in input_data:
        direction, distance = line.split()
        parsed_instructions.append((direction, int(distance)))
    return parsed_instructions


def part1():
    head_x, head_y = 0, 0
    tail_x, tail_y = 0, 0
    tail_tracker = {(0, 0)}
    for direction, distance in instructions:
        logger.debug(f"Direction: {direction}, Distance: {distance}")
        for _ in range(distance):
            head_x += offset[direction][0]
            head_y += offset[direction][1]
            logger.debug(f"Moving head to {head_x}, {head_y}")
            while max(abs(tail_x - head_x), abs(tail_y - head_y)) > 1:
                if abs(tail_x - head_x) > 0:
                    tail_x += 1 if tail_x < head_x else -1
                    logger.debug(f"Moving tail to {tail_x}, {tail_y}")
                if abs(tail_y - head_y) > 0:
                    tail_y += 1 if tail_y < head_y else -1
                    logger.debug(f"Moving tail to {tail_x}, {tail_y}")
                tail_tracker.add((tail_x, tail_y))
                logger.debug(f"Added {tail_x}, {tail_y} to tail tracker")
    return len(tail_tracker)


def part2():
    rope = [(0, 0)] * 10
    second_tracker = set()
    for direction, distance in instructions:
        logger.debug(f"Direction: {direction}, Distance: {distance}")
        for _ in range(distance):
            head2_x, head2_y = rope[0]
            rope[0] = head2_x + offset[direction][0], head2_y + offset[direction][1]
            logger.debug(f"Moving head to {head2_x}, {head2_y}")
            for i in range(1, len(rope)):
                px, py = rope[i - 1]
                cx, cy = rope[i]
                while max(abs(cx - px), abs(cy - py)) > 1:
                    if abs(cx - px) > 0:
                        cx += 1 if cx < px else -1
                        logger.debug(f"Moving tail to {cx}, {cy}")
                    if abs(cy - py) > 0:
                        cy += 1 if cy < py else -1
                        logger.debug(f"Moving tail to {cx}, {cy}")
                    rope[i] = cx, cy
                second_tracker.add(rope[-1])
                logger.debug(f"Added {cx}, {cy} to second tracker")
    return len(second_tracker)


def test():
    pass


if __name__ == "__main__":
    # Parse the arguments
    args = parse_args()
    # setup logger
    logger = setup_logging(args.debug)

    # Start here
    data = load_input()
    instructions = parse_instructions(data)
    logger.debug(f"Instructions: {instructions}")
    logger.success(f"Part 1: {part1()}")
    logger.success(f"Part 2: {part2()}")
