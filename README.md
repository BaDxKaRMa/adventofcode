# 🎄 advent-cli

This repo uses the Advent-CLI python tool (found in pypi). advent-cli is a command-line tool for interacting with Advent of Code, specifically geared toward writing solutions in Python. It can be used to view puzzle prompts, download input, submit solutions, and view personal or private stats and leaderboards.

![](https://user-images.githubusercontent.com/27470183/145635955-5ea316a2-d028-4954-a144-d87846ed05d9.gif)

## Installation

Install from [PyPI](https://pypi.org/project/advent-cli/):

```
pip install advent-cli
```

Or grab the latest version from [GitHub](https://github.com/fergusch/advent-cli):

```
pip install git+https://github.com/fergusch/advent-cli.git@develop
```

## Setup

Before you do anything, you'll need to provide advent-cli with a session cookie so it can authenticate as you. To do this, log in to the [Advent of Code website](https://adventofcode.com/) and grab the cookie named `session` from your browser's inspect element tool. Store it in an environment variable on your machine named `ADVENT_SESSION_COOKIE`. A fresh session cookie is good for about a month, after which you'll need to repeat these steps.

A full list of configuration options can be found [here](#configuration).

## Usage

advent-cli can be invoked using the `advent` command, or `python -m advent_cli`.

## Configuration

The following environment variables can be set to change the default config:

| Variable                   | Function                                                                                 |
| -------------------------- | ---------------------------------------------------------------------------------------- |
| `ADVENT_SESSION_COOKIE`    | Advent of Code session cookie for authentication. **(required)**                         |
| `ADVENT_PRIV_BOARDS`       | Comma-separated list of private leaderboard IDs.                                         |
| `ADVENT_DISABLE_TERMCOLOR` | Set to `1` to permanently disable coloring terminal output.                              |
| `ADVENT_MARKDOWN_EM`       | Method for converting `<em>` tags inside code blocks. See below for context and options. |

# Stats

<!--- advent_readme_stars table --->
## 2022 Results

| Day | Part 1 | Part 2 |
| :---: | :---: | :---: |
| [Day 1](https://adventofcode.com/2022/day/1) | ⭐ | ⭐ |
| [Day 2](https://adventofcode.com/2022/day/2) | ⭐ | ⭐ |
| [Day 3](https://adventofcode.com/2022/day/3) | ⭐ | ⭐ |
| [Day 4](https://adventofcode.com/2022/day/4) | ⭐ | ⭐ |
| [Day 5](https://adventofcode.com/2022/day/5) | ⭐ | ⭐ |
| [Day 6](https://adventofcode.com/2022/day/6) | ⭐ | ⭐ |
| [Day 7](https://adventofcode.com/2022/day/7) | ⭐ | ⭐ |
| [Day 8](https://adventofcode.com/2022/day/8) | ⭐ | ⭐ |
| [Day 9](https://adventofcode.com/2022/day/9) | ⭐ | ⭐ |
| [Day 10](https://adventofcode.com/2022/day/10) | ⭐ | ⭐ |
| [Day 11](https://adventofcode.com/2022/day/11) | ⭐ | ⭐ |
| [Day 12](https://adventofcode.com/2022/day/12) | ⭐ | ⭐ |
| [Day 13](https://adventofcode.com/2022/day/13) | ⭐ | ⭐ |
| [Day 14](https://adventofcode.com/2022/day/14) | ⭐ | ⭐ |
| [Day 15](https://adventofcode.com/2022/day/15) | ⭐ | ⭐ |
| [Day 16](https://adventofcode.com/2022/day/16) | ⭐ | ⭐ |
| [Day 17](https://adventofcode.com/2022/day/17) | ⭐ | ⭐ |
| [Day 18](https://adventofcode.com/2022/day/18) | ⭐ | ⭐ |
<!--- advent_readme_stars table --->
