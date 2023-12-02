#!/usr/bin/env python3
# advent of code 2023
# https://adventofcode.com/2023
# day 02

import sys
import unittest

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="DEBUG")


class TestParts(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(
            part1(
                parse_input(
                    [
                        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
                        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
                        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
                    ]
                )
            ),
            8,
        )

    def test_part2(self):
        self.assertEqual(
            part2(
                parse_input(
                    [
                        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
                        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
                        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
                    ]
                )
            ),
            2286,
        )


def parse_input(lines):
    parsed_games = {}

    for game in lines:
        game_name, game_data = game.split(": ")
        pulls = game_data.split("; ")
        parsed_pulls = []

        for pull in pulls:
            cubes = pull.split(", ")
            parsed_cubes = {}

            for cube in cubes:
                count, color = cube.split(" ")
                parsed_cubes[color] = int(count)

            parsed_pulls.append(parsed_cubes)

        parsed_games[game_name] = parsed_pulls
        logger.debug(f"{game_name} - {parsed_pulls}")
    logger.debug(f"parsed_games: {parsed_games}")
    return parsed_games


def part1(data):
    valid_games = []
    valid_counts = {"red": 12, "green": 13, "blue": 14}
    logger.info(f"Valid Counts set to: {valid_counts}")

    for game_name, pulls in data.items():
        valid = True
        for pull in pulls:
            for color, count in pull.items():
                if count > valid_counts[color]:
                    valid = False
                    logger.error(f"{game_name} is invalid")
        if valid:
            valid_games.append(game_name)
            logger.success(f"{game_name} is valid")

    sum_of_games = 0
    for game in valid_games:
        sum_of_games += int(game.split(" ")[1])
        logger.debug(f"Adding game {game.split(' ')[1]} to sum_of_games")

    logger.info(f"Sum of games: {sum_of_games}")

    return sum_of_games


def part2(data):
    max_counts = {"red": 0, "green": 0, "blue": 0}
    max_per_game = {}

    for game_name, pulls in data.items():
        max_counts = {"red": 0, "green": 0, "blue": 0}
        logger.debug(f"Processing {game_name}")
        for pull in pulls:
            for color, count in pull.items():
                if count > max_counts[color]:
                    max_counts[color] = count
        max_per_game[game_name] = max_counts
        logger.debug(f"{game_name} - {max_counts}")

    sum_of_games = 0
    for game_name, max_counts in max_per_game.items():
        sum_of_games += max_counts["red"] * max_counts["green"] * max_counts["blue"]
        logger.debug(f"Adding game {game_name} to total: {sum_of_games}")

    return sum_of_games


if __name__ == "__main__":
    unittest.main()
