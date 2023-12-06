#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 05

import os
import sys
import unittest
from typing import List, Set

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


# Represents one specific map
class Interval:
    def __init__(self, start=0, length=0, offset=0, line=""):
        if len(line) > 0:
            dest, start, length = [int(x) for x in line.split(" ")]
            offset = dest - start
        self.start = start
        self.end = start + length - 1
        self.offset = offset

    def contains(self, point: int):
        """Will this interval map this point"""
        return self.start <= point <= self.end

    def map(self, point: int):
        """Map the point"""
        return point + self.offset

    def outputs(self, mapped_point: int):
        """Could this point be the output of a map"""
        return self.start + self.offset <= mapped_point <= self.end + self.offset

    def undo_map(self, mapped_point: int):
        """Undo the map"""
        return mapped_point - self.offset


# Represents one layer of Intervals
class IntervalList:
    def __init__(self, intervals: List[Interval]):
        self.intervals = intervals

    def process(self, point: int):
        """Find the appropriate map for a point, and map it"""
        for interval in self.intervals:
            if interval.contains(point):
                return interval.map(point)
        return point

    def undo_process(self, outputs: Set[int]):
        """For a set of mapped points, find the points that could have mapped to them"""
        potential_inputs = set()
        for interval in self.intervals:
            for output in outputs:
                if interval.outputs(output):
                    potential_inputs.add(interval.undo_map(output))
        outputs.update(potential_inputs)

    def filter(self, points: Set[int]):
        """For a set of points, find the ones that are included in the intervals"""
        results = set()
        for point in points:
            if any(interval.contains(point) for interval in self.intervals):
                results.add(point)
        return results

    def boundaries(self, candidate_points: Set[int]):
        """For all the intervals in this layer, their boundaries should be considered candidate points"""
        for interval in self.intervals:
            candidate_points.add(interval.start)
            candidate_points.add(interval.end)


class TestParts(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(current_dir, "example_input.txt")
        with open(input_file, "r") as file:
            lines = file.read().splitlines()
        self.seeds, self.seed_intervals, self.interval_lists = parse_input(lines)

    def test_part1(self):
        self.assertEqual(part1(self.seeds, None, self.interval_lists), 35)

    def test_part2(self):
        self.assertEqual(part2(None, self.seed_intervals, self.interval_lists), 46)


def parse_input(lines):
    # Add a blank line to the end
    lines.append("")
    # Put it back together as a string (I know...)
    input = "\n".join(lines)
    lines = iter(input.split("\n"))

    # Parse the line of seeds
    seed_input, _ = next(lines).split(": ")[1], next(lines)
    seeds = [int(seed) for seed in seed_input.split(" ")]
    # Added the intervals for part 2
    seed_intervals = [Interval(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    seed_intervals = IntervalList(seed_intervals)

    # Will contain the seven layers of maps
    interval_lists: List[IntervalList] = []

    for x in range(7):
        # Skip the blank line and header lines
        _, line = next(lines), next(lines)

        intervals = []
        while len(line) != 0:
            intervals.append(Interval(line=line))
            line = next(lines)

        # One layer of maps
        interval_list = IntervalList(intervals)
        interval_lists.append(interval_list)

    return seeds, seed_intervals, interval_lists


def part1(seeds: List[int], _, interval_lists: List[IntervalList]) -> float:
    # Initialize min_seed to infinity for comparison purposes
    min_seed = float("inf")

    # Iterate over each seed in the provided list
    for seed in seeds:
        # Process the current seed through each IntervalList (layer of processing)
        for intervalList in interval_lists:
            seed = intervalList.process(seed)

        # If the processed seed is less than the current min_seed, update min_seed
        min_seed = seed if seed < min_seed else min_seed

    # Return the minimum seed value after all processing
    return min_seed


def part2(_, seed_intervals: IntervalList, interval_lists: List[IntervalList]) -> float:
    # Initialize a set to store the candidate seed values
    candidate_points = set()
    # Iterate over each IntervalList in the provided list in reverse order
    for intervalList in interval_lists[::-1]:
        # Undo the processing for candidate_points from lower maps
        intervalList.undo_process(candidate_points)
        # This map layer contributes its boundaries as candidates
        intervalList.boundaries(candidate_points)

    # Remove candidates that are not valid
    candidate_points = seed_intervals.filter(candidate_points)

    # Test the candidates and find the optimal one
    return part1(list(candidate_points), _, interval_lists)


if __name__ == "__main__":
    logger.warning("Only running tests, you should run using Advent-CLI.")
    unittest.main()
