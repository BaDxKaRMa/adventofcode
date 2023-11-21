#!/usr/bin/env python3

SAMPLE_INPUT = [
    "$ cd /",
    "$ ls",
    "dir a",
    "14848514 b.txt",
    "8504156 c.dat",
    "dir d",
    "$ cd a",
    "$ ls",
    "dir e",
    "29116 f",
    "2557 g",
    "62596 h.lst",
    "$ cd e",
    "$ ls",
    "584 i",
    "$ cd ..",
    "$ cd ..",
    "$ cd d",
    "$ ls",
    "4060174 j",
    "8033020 d.log",
    "5626152 d.ext",
    "7214296 k",
]

try:
    with open("day7.txt") as f:
        input_string = f.read().splitlines()
except FileNotFoundError:
    input_string = SAMPLE_INPUT


def parse_input(lines) -> tuple[dict[str, int], set[str]]:
    files = {}
    folders = set()
    current = []
    for line in lines:
        if line.startswith("$"):
            if line.startswith("$ cd"):
                destination = line[5:]
                if destination == "..":
                    if len(current) > 0:
                        current.pop(-1)
                elif destination == "/":
                    current = []
                else:
                    current.extend(destination.split("/"))
        else:
            size, name = line.split(" ")
            if size == "dir":
                continue
            size = int(size)
            files["/".join(current + [name])] = size
        folders.add("/".join(current))
    return files, folders


def part1(input_files, input_folders) -> tuple[int, dict[str, int]]:
    answer = 0
    folder_collection = {}
    for folder in input_folders:
        folder_size = 0
        for file in input_files:
            if file.startswith(folder):
                folder_size += input_files[file]
        if folder_size <= 100000:
            answer += folder_size
        folder_collection[folder] = folder_size
    return answer, folder_collection


def part2(parsed_folders) -> int:
    return min(
        v
        for v in parsed_folders.values()
        if 70000000 - parsed_folders[""] + v >= 30000000
    )


def test_parse_input():
    assert parse_input(SAMPLE_INPUT) == (
        {
            "b.txt": 14848514,
            "c.dat": 8504156,
            "a/f": 29116,
            "a/g": 2557,
            "a/h.lst": 62596,
            "a/e/i": 584,
            "d/j": 4060174,
            "d/d.log": 8033020,
            "d/d.ext": 5626152,
            "d/k": 7214296,
        },
        {"", "a/e", "d", "a"},
    )


def test_part1():
    assert part1(*parse_input(SAMPLE_INPUT))[0] == 95437


def test_part2():
    assert part2(part1(*parse_input(SAMPLE_INPUT))[1]) == 24933642


file_sizes, tree = parse_input(input_string)
part1_answer, folder_sizes = part1(file_sizes, tree)

print(f"Part 1: {part1_answer}")
print(f"Part 2: {part2(folder_sizes)}")
