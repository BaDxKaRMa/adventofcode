#!/usr/bin/env python3
## advent of code 2024
## https://adventofcode.com/2024
## day 07

import itertools

from my_utils import setup_logging

logger = setup_logging(log_level="DEBUG")


def parse_input(lines):
    parsed_data = []
    for line in lines:
        test_value, numbers = line.split(":")
        test_value = int(test_value.strip())
        numbers = list(map(int, numbers.strip().split()))
        parsed_data.append((test_value, numbers))
    return parsed_data


def evaluate_expression(numbers, operators, use_concat=False):
    result = numbers[0]
    for i in range(len(operators)):
        if operators[i] == "+":
            result += numbers[i + 1]
        elif operators[i] == "*":
            result *= numbers[i + 1]
        elif use_concat and operators[i] == "||":
            result = int(str(result) + str(numbers[i + 1]))
    return result


def can_be_true(test_value, numbers, use_concat=False):
    if len(numbers) == 1:
        return numbers[0] == test_value

    operator_set = ["+", "*", "||"] if use_concat else ["+", "*"]
    for operators in itertools.product(operator_set, repeat=len(numbers) - 1):
        if evaluate_expression(numbers, operators, use_concat) == test_value:
            return True
    return False


def part1(data):
    total_calibration_result = 0
    for test_value, numbers in data:
        if can_be_true(test_value, numbers):
            total_calibration_result += test_value
    return total_calibration_result


def part2(data):
    total_calibration_result = 0
    for test_value, numbers in data:
        if can_be_true(test_value, numbers, use_concat=True):
            total_calibration_result += test_value
    return total_calibration_result
