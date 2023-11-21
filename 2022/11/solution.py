#!/usr/bin/env python3
# Advent of Code 2022 - Day 11
from __future__ import annotations

import operator
import re
from collections import Counter
from copy import deepcopy
from math import lcm
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "day11.txt")


class Monkey:
    def __init__(
        self, monkey_id: int, items: list, worry_op: str, div: int, throw_to: list
    ) -> None:
        self.monkey_id = monkey_id
        self.start_items = items
        self._worry_op = worry_op
        self.divisor = div
        self._throw_to = throw_to
        self.inspect_count = 0

    def add_item(self, item: int):
        self.start_items.append(item)

    def inspect(self, relief=True, lcm=None) -> int:
        self.inspect_count += 1
        worry_op = self._worry_op.replace("old", str(self.start_items[0]))
        first, the_op, second = re.findall(r"(\w+) (.) (\w+)", worry_op)[0]
        ops_dict = {"+": operator.add, "*": operator.mul}
        self.start_items[0] = ops_dict[the_op](int(first), int(second))
        if relief:
            self.start_items[0] //= 3
        if lcm:
            self.start_items[0] %= lcm
        return (
            self._throw_to[0]
            if self.start_items[0] % self.divisor == 0
            else self._throw_to[1]
        )

    def throw_to(self, other: Monkey):
        other.add_item(self.start_items.pop(0))

    def __repr__(self) -> str:
        return (
            f"Monkey:(id={self.monkey_id}, items={self.start_items}, "
            + f"inspect_count={self.inspect_count})"
        )


def play(monkeys: dict[int, Monkey], rounds_to_play: int, relief=True, lcm=None) -> int:
    for _ in range(1, rounds_to_play + 1):
        for monkey in monkeys.values():
            while monkey.start_items:
                to_monkey = monkeys[monkey.inspect(relief=relief, lcm=lcm)]
                monkey.throw_to(to_monkey)

    monkey_inspect = Counter(
        {monkey.monkey_id: monkey.inspect_count for monkey in monkeys.values()}
    )
    two_most_common = monkey_inspect.most_common(2)
    return two_most_common[0][1] * two_most_common[1][1]


def parse_input(data: str) -> dict[int, Monkey]:
    monkeys = {}
    blocks = data.split("\n\n")
    for block in blocks:
        for line in block.splitlines():
            if line.startswith("Monkey"):
                monkey_id = int(re.findall(r"(\d+)", line)[0])
            if "items:" in line:
                items = list(map(int, re.findall(r"(\d+)", line)))
            if "Operation:" in line:
                worry_op = line.split("=")[-1].strip()
            if "Test:" in line:
                divisor = int(re.findall(r"\d+", line)[0])
            if "true:" in line:
                to_monkey_true = int(re.findall(r"\d+", line)[0])
            if "false:" in line:
                to_monkey_false = int(re.findall(r"\d+", line)[0])

        monkey = Monkey(
            monkey_id=monkey_id,
            items=items,
            worry_op=worry_op,
            div=divisor,
            throw_to=[to_monkey_true, to_monkey_false],
        )

        monkeys[monkey_id] = monkey

    return monkeys


def test_fake():
    pass


if __name__ == "__main__":
    with open(INPUT_FILE, mode="r") as f:
        data = f.read()

    monkeys = parse_input(data)

    monkey_business = play(deepcopy(monkeys), 20)
    print(f"Part 1: monkey business={monkey_business}")

    lcm = lcm(*[monkey.divisor for monkey in monkeys.values()])
    monkey_business = play(monkeys, 10000, relief=False, lcm=lcm)
    print(f"Part 2: monkey business={monkey_business}")
