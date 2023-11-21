#!/usr/bin/env python3

SAMPLE_INPUT = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

with open("day14.txt") as f:
    lines = f.read().splitlines()

sand_source = 500, 0

filled = set()

for line in lines:
    coords = []

    for str_coord in line.split(" -> "):
        x, y = map(int, str_coord.split(","))
        coords.append((x, y))

    for i in range(1, len(coords)):
        cx, cy = coords[i]  # cur
        px, py = coords[i - 1]

        if cy != py:
            assert cx == px
            for y in range(min(cy, py), max(cy, py) + 1):
                filled.add((cx, y))

        if cx != px:
            assert cy == py
            for x in range(min(cx, px), max(cx, px) + 1):
                filled.add((x, cy))


max_y = max([coord[1] for coord in filled])


def simulate_sand():
    global filled
    s_x, s_y = sand_source
    while s_y <= max_y:
        if (s_x, s_y + 1) not in filled:
            s_y += 1
            continue

        if (s_x - 1, s_y + 1) not in filled:
            s_x -= 1
            s_y += 1
            continue

        if (s_x + 1, s_y + 1) not in filled:
            s_x += 1
            s_y += 1
            continue

        filled.add((s_x, s_y))
        return True
    return False


# just redoing because I'm lazy
def simulate_sand_part2():
    global filled2
    filled2 = set()
    ss_x, ss_y = 500, 0

    if (ss_x, ss_y) in filled2:
        return (ss_x, ss_y)

    while ss_y <= max_y:
        if (ss_x, ss_y + 1) not in filled2:
            ss_y += 1
            continue

        if (ss_x - 1, ss_y + 1) not in filled2:
            ss_x -= 1
            ss_y += 1
            continue

        if (ss_x + 1, ss_y + 1) not in filled2:
            ss_x += 1
            ss_y += 1
            continue

        # Everything filled, come to rest
        break

    return (ss_x, ss_y)


part1 = 0
while True:
    res = simulate_sand()
    if not res:
        break
    part1 += 1

print(f"Part 1: {part1}")


part2 = 0

while True:
    x, y = simulate_sand_part2()
    filled2.add((x, y))
    part2 += 1

    if (x, y) == sand_source:
        break

print(f"Part 2: {part2}")
