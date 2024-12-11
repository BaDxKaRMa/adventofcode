#!/usr/bin/env python3
## advent of code 2024
## https://adventofcode.com/2024
## day 05

from typing import List, Tuple, Dict, Set
from my_utils import setup_logging

logger = setup_logging(log_level="DEBUG")


def parse_input(lines: List[str]) -> Tuple[Dict[int, Set[int]], List[List[int]]]:
    rules: Dict[int, Set[int]] = {}
    updates: List[List[int]] = []
    parsing_rules = True

    for line in lines:
        line = line.strip()
        if not line:
            parsing_rules = False
            continue

        if parsing_rules:
            a, b = [int(x) for x in line.split("|")]
            if a not in rules:
                rules[a] = set()
            rules[a].add(b)
        else:
            updates.append([int(x) for x in line.split(",")])

    logger.debug(f"Parsed rules: {rules}")
    logger.debug(f"Parsed updates: {updates}")
    return rules, updates


def process(nums: List[int], rules: Dict[int, Set[int]]) -> int:
    read: Set[int] = set()
    for num in nums:
        if num in rules and len(rules[num].intersection(read)) > 0:
            logger.debug(f"Invalid sequence found in {nums}")
            return 0
        read.add(num)
    return nums[len(nums) // 2]


def find_invalid(nums: List[int], index: int, rules: Dict[int, Set[int]]) -> int:
    value = nums[index]
    if value not in rules:
        return -1
    for j in range(index):
        if nums[j] in rules[value]:
            return j
    return -1


def my_sort(nums: List[int], rules: Dict[int, Set[int]], step: int = 0) -> List[int]:
    invalid_index = -1
    for i in range(len(nums)):
        invalid_index = find_invalid(nums, i, rules)
        if invalid_index != -1:
            nums = (
                nums[:invalid_index] + [nums[i]] + nums[invalid_index:i] + nums[i + 1 :]
            )
            logger.debug(f"Step {step}: Reordered nums to {nums}")
            break
    if invalid_index == -1:
        return nums
    return my_sort(nums, rules, step + 1)


def part1(rules: Dict[int, Set[int]], updates: List[List[int]]) -> int:
    total_sum = 0
    for update in updates:
        total_sum += process(update, rules)
    return total_sum


def part2(rules: Dict[int, Set[int]], updates: List[List[int]]) -> int:
    total_sum = 0
    for update in updates:
        points = process(update, rules)
        if points != 0:
            logger.debug(f"Valid sequence found in {update}")
            continue
        update = my_sort(update, rules)
        total_sum += process(update, rules)
    return total_sum
