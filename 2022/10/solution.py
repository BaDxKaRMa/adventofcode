#!/usr/bin/env python3
# Day 10 Advent of Code 2022
# https://adventofcode.com/2022/day/10

import os
from utils import parse_args, setup_logging

SAMPLE_INPUT = """\
noop
addx 3
addx -5
"""


def load_input():
    if os.path.exists("day10.txt"):
        with open(os.path.join(os.path.dirname(__file__), "day10.txt")) as f:
            input_data = f.read().splitlines()
            logger.debug(f"Loaded day10.txt: {input_data}")
    else:
        input_data = SAMPLE_INPUT.splitlines()
        logger.debug(f"Loaded sample input: {input_data}")
    return input_data


def parse_instructions(input_data):
    parsed_instructions = []
    for line in input_data:
        if line.startswith("noop"):
            parsed_instructions.append(("noop", None))
        elif line.startswith("addx"):
            parsed_instructions.append(("addx", int(line.split()[1])))
    return parsed_instructions


def test_parse_instructions():
    test_data = SAMPLE_INPUT.splitlines()
    assert parse_instructions(test_data) == [
        ("noop", None),
        ("addx", 3),
        ("addx", -5),
    ]


def run_instructions(parsed_instructions):
    x = 1
    for instruction, value in parsed_instructions:
        yield x
        if instruction == "addx":
            yield x
            x += value


def calculate_signal(register):
    signal_found = []
    for cycle, x in enumerate(register, 1):
        if cycle % 40 == 20:
            signal_found.append(cycle * x)
    return sum(signal_found)


def test_calculate_signal():
    test_data = SAMPLE_INPUT.splitlines()
    test_instructions = parse_instructions(test_data)
    test_after_run = run_instructions(test_instructions)
    assert calculate_signal(test_after_run) == 0


def build_crt(p2_instructions):
    rows = []
    row_string = ""
    for cycle, x in enumerate(run_instructions(p2_instructions)):
        row_string += ".#"[abs(cycle % 40 - x) < 2]
        if (cycle + 1) % 40 == 0:
            rows.append(row_string)
            row_string = ""
    return rows


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logging(args.debug)
    data = load_input()
    instructions = parse_instructions(data)
    after_run = run_instructions(instructions)
    logger.success(f"Part 1: {calculate_signal(after_run)}")
    crt = build_crt(instructions)
    logger.success("Part 2:")
    for row in crt:
        logger.success(row)
