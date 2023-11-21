#!/usr/bin/env python3

SAMPLE_INPUT = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]

try:
    with open("day6.txt") as f:
        INPUT = f.read()
except FileNotFoundError:
    INPUT = SAMPLE_INPUT


def decode(input_string, window) -> int:
    for i in range(len(input_string) - window - 1):
        if len(set(input_string[i : i + window])) == window:
            return i + window


def test_decode():
    decode(SAMPLE_INPUT[0], 4)
    assert decode(SAMPLE_INPUT[0], 4) == 7


if __name__ == "__main__":
    parts = {"part1": 4, "part2": 14}

    for part, size in parts.items():
        if INPUT is SAMPLE_INPUT:
            print(f"Test Cases for {part}:")
            for line in INPUT:
                print(f"{part}: {decode(line, size)}")
            print()
        else:
            print(f"Part {part}: {decode(INPUT, size)}")
