#!/usr/bin/env python3
# advent of code 2021
# https://adventofcode.com/2021
# day 03

import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


def parse_input(lines):
    return lines


def part1(data):
    gamma_rate_binary = ""
    epsilon_rate_binary = ""
    for i in range(len(data[0])):
        bits = [column[i] for column in data]
        most_common_bit = max(set(bits), key=bits.count)
        least_common_bit = min(set(bits), key=bits.count)
        gamma_rate_binary += most_common_bit
        epsilon_rate_binary += least_common_bit

    gamma_rate_decimal = int(gamma_rate_binary, 2)
    epsilon_rate_decimal = int(epsilon_rate_binary, 2)
    return gamma_rate_decimal * epsilon_rate_decimal


def find_rating(rating_type, data):
    numbers = data.copy()
    for i in range(len(data[0])):
        bits = [int(number[i]) for number in numbers]
        if rating_type == "oxygen":
            common_bit = (
                max(set(bits), key=bits.count) if bits.count(1) != bits.count(0) else 1
            )
        elif rating_type == "CO2":
            common_bit = (
                min(set(bits), key=bits.count) if bits.count(1) != bits.count(0) else 0
            )
        numbers = [number for number in numbers if int(number[i]) == common_bit]
        if len(numbers) == 1:
            return int(numbers[0], 2)


def part2(data):
    oxygen_generator_rating = find_rating("oxygen", data)
    CO2_scrubber_rating = find_rating("CO2", data)
    return oxygen_generator_rating * CO2_scrubber_rating
