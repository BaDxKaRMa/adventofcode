from loguru import logger
from string import ascii_lowercase
from heapq import heappop, heappush

SAMPLE_INPUT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


try:
    with open("day12.txt") as f:
        lines = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    lines = SAMPLE_INPUT.splitlines()


grid = [list(line) for line in lines]
row_count = len(grid)
col_count = len(grid[0])
logger.debug(f"Built grid with {row_count} rows and {col_count} columns")

for i in range(row_count):
    for j in range(col_count):
        char = grid[i][j]
        if char == "S":
            start = i, j
            logger.debug(f"Found start at {start}")
        if char == "E":
            end = i, j
            logger.debug(f"Found end at {end}")


def height(character):
    logger.debug(f"Searching height of {character}")
    if character in ascii_lowercase:
        return ascii_lowercase.index(character)
    if character == "S":
        return 0
    if character == "E":
        return 25


def neighbors(i, j):
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for di, dj in directions:
        ii = i + di
        jj = j + dj

        if not (0 <= ii < row_count and 0 <= jj < col_count):
            continue

        if height(grid[ii][jj]) <= height(grid[i][j]) + 1:
            logger.debug(f"Found neighbor {grid[ii][jj]} at {ii}, {jj}")
            yield ii, jj


visited = [[False] * col_count for _ in range(row_count)]
heap = [(0, start[0], start[1])]
logger.debug(f"Starting heap: {heap}")

while True:
    steps, i, j = heappop(heap)

    if visited[i][j]:
        continue
    visited[i][j] = True
    logger.debug(f"Visiting {grid[i][j]} at {i}, {j}")

    if (i, j) == end:
        logger.success(f"Total steps: {steps}")
        print(steps)
        break

    for ii, jj in neighbors(i, j):
        heappush(heap, (steps + 1, ii, jj))


# do again but from end to start for part 2
def neighbors2(i, j):
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for di, dj in directions:
        ii = i + di
        jj = j + dj

        if not (0 <= ii < row_count and 0 <= jj < col_count):
            continue

        if height(grid[ii][jj]) >= height(grid[i][j]) - 1:
            yield ii, jj


# Dijkstra's
visited = [[False] * col_count for _ in range(row_count)]
heap = [(0, end[0], end[1])]

while True:
    steps, i, j = heappop(heap)

    if visited[i][j]:
        continue
    visited[i][j] = True

    if height(grid[i][j]) == 0:
        print(steps)
        break

    for ii, jj in neighbors2(i, j):
        heappush(heap, (steps + 1, ii, jj))
