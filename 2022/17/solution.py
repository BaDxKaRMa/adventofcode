#!/usr/bin/env python3
from dataclasses import dataclass
import itertools
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "day17.txt")

SHAPES = {
    "HLINE": {(0, 0), (1, 0), (2, 0), (3, 0)},
    "PLUS": {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    "BACKWARDS_L": {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    "I": {(0, 0), (0, 1), (0, 2), (0, 3)},
    "SQUARE": {(0, 0), (1, 0), (0, 1), (1, 1)},
}

MOVE = {"<": (-1, 0), ">": (1, 0), "V": (0, -1)}


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"P({self.x},{self.y})"


class Shape:
    def __init__(self, points: set[Point], at_rest=False) -> None:
        self.points: set[Point] = points  # the points that make up the shape
        self.at_rest = at_rest

    @classmethod
    def create_shape_by_type(cls, shape_type: str, origin: Point):
        return cls({(Point(*coords) + origin) for coords in SHAPES[shape_type]})

    @classmethod
    def create_shape_from_points(cls, points: set[Point], at_rest=False):
        return cls(points, at_rest)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Shape):
            if self.points == __o.points:
                return True
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"Shape(at_rest={self.at_rest}, points={self.points}"


class Tower:
    WIDTH = 7
    LEFT_WALL_X = 0
    RIGHT_WALL_X = LEFT_WALL_X + 7 + 1
    OFFSET_X = 2 + 1
    OFFSET_Y = 3 + 1
    FLOOR_Y = 0

    FALLING = "@"
    AT_REST = "#"
    EMPTY = "."
    WALL = "|"
    FLOOR = "-"

    def __init__(self, jet_pattern: str) -> None:
        self._jet_pattern = itertools.cycle(enumerate(jet_pattern))
        self._shape_generator = itertools.cycle(enumerate(SHAPES))
        self.top = Tower.FLOOR_Y
        self._all_at_rest_shapes: set[Shape] = set()
        self._all_at_rest_points: set[Point] = set()

        self.repeat_identified = False
        self._cache: dict[tuple, tuple] = {}
        self._repeat: tuple = (0, 0)

    def _current_origin(self) -> Point:
        return Point(Tower.LEFT_WALL_X + Tower.OFFSET_X, self.top + Tower.OFFSET_Y)

    def _next_shape(self):
        return next(self._shape_generator)

    def _next_jet(self):
        return next(self._jet_pattern)

    def _check_cache(self, shape_index: int, jet_index: int, formation: str) -> tuple:
        key = (shape_index, jet_index, formation)
        shape_ct = len(self._all_at_rest_shapes)
        if key in self._cache:  # We've found a repeat!
            last_height, last_shape_count = self._cache[key]
            return (True, self.top, last_height, shape_ct, last_shape_count)
        else:
            self._cache[key] = (self.top, shape_ct)

        return (False, self.top, 0, shape_ct, 0)

    def drop_shape(self):
        shape_index, next_shape_type = self._next_shape()
        self.current_shape = Shape.create_shape_by_type(
            next_shape_type, self._current_origin()
        )

        while True:
            jet_index, jet = self._next_jet()
            self._move_shape(jet)
            if not self._move_shape("V"):
                self.top = max(
                    self.top, max(point.y for point in self.current_shape.points)
                )
                settled_shape = Shape.create_shape_from_points(
                    self.current_shape.points, True
                )
                self._settle_shape(settled_shape)
                if not self.repeat_identified:
                    cache_response = self._check_cache(
                        shape_index, jet_index, self.get_recent_formation()
                    )
                    if cache_response[0]:
                        self.repeat_identified = True
                        self._repeat = (
                            cache_response[1] - cache_response[2],
                            cache_response[3] - cache_response[4],
                        )

                break

    def calculate_height(self, shape_drops: int) -> tuple[int, int]:
        remaining_drops = shape_drops - len(self._all_at_rest_shapes)
        repeats_req = remaining_drops // self._repeat[1]
        remaining_drops %= self._repeat[1]

        height_delta = self._repeat[0] * repeats_req
        new_height = self.top + height_delta

        return new_height, remaining_drops

    def _settle_shape(self, shape: Shape):
        self._all_at_rest_shapes.add(shape)
        self._all_at_rest_points.update(shape.points)

    def _move_shape(self, direction) -> bool:
        if direction == "<":
            shape_left_x = min(point.x for point in self.current_shape.points)
            if shape_left_x == Tower.LEFT_WALL_X + 1:
                return False

        if direction == ">":
            shape_right_x = max(point.x for point in self.current_shape.points)
            if shape_right_x == Tower.RIGHT_WALL_X - 1:
                return False

        if direction == "V":
            shape_bottom = min(point.y for point in self.current_shape.points)
            if shape_bottom == Tower.FLOOR_Y + 1:
                return False

        candidate_points = {
            (point + Point(*MOVE[direction])) for point in self.current_shape.points
        }
        if self._all_at_rest_points & candidate_points:
            return False
        else:
            self.current_shape = Shape.create_shape_from_points(candidate_points)
        return True

    def get_recent_formation(self) -> str:
        rows = []
        min_y = max(0, self.top - 20)  # we want the last 20 lines
        for y in range(min_y, self.top + 1):
            line = ""
            for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                if Point(x, y) in self._all_at_rest_points:
                    line += Tower.AT_REST
                elif Point(x, y) in self.current_shape.points:
                    line += Tower.FALLING
                else:
                    line += Tower.EMPTY

            rows.append(line)

        return "\n".join(rows[::-1])

    def __str__(self) -> str:
        rows = []
        top_for_vis = max(self.top, max(point.y for point in self.current_shape.points))

        for y in range(Tower.FLOOR_Y, top_for_vis + 1):
            line = f"{y:3d} "
            if y == Tower.FLOOR_Y:
                line += "+" + (Tower.FLOOR * Tower.WIDTH) + "+"
            else:
                for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X + 1):
                    if x in (Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                        line += Tower.WALL
                    elif Point(x, y) in self._all_at_rest_points:
                        line += Tower.AT_REST
                    elif Point(x, y) in self.current_shape.points:
                        line += Tower.FALLING
                    else:
                        line += Tower.EMPTY

            rows.append(line)

        return f"{repr(self)}:\n" + "\n".join(rows[::-1])

    def __repr__(self) -> str:
        return f"Tower(height={self.top}, rested={len(self._all_at_rest_shapes)})"


def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()

    # Part 1
    tower = Tower(jet_pattern=data)
    for _ in range(2022):
        tower.drop_shape()

    print(f"Part 1: {repr(tower)}")

    # Part 2
    tower = Tower(jet_pattern=data)
    while not tower.repeat_identified:
        tower.drop_shape()
    height_at_repeat_start = tower.top
    print(f"\nPart 2: Repeat found at: {repr(tower)}")

    new_height, remaining_drops = tower.calculate_height(1000000000000)
    print(f"Part 2: Calculated new height from repeats: {new_height}")

    for _ in range(remaining_drops):
        tower.drop_shape()
    height_after_top_up = tower.top
    final_height = new_height + height_after_top_up - height_at_repeat_start

    print(f"Part 2: Final height after top-up: {final_height}")


if __name__ == "__main__":
    main()
