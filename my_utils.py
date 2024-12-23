#!/usr/bin/env python3
import argparse
import sys
import re
import math
import hashlib
import operator
import copy
from collections import Counter
from functools import total_ordering, reduce

try:
    from loguru import logger
except ImportError:
    print("Please install the 'loguru' package by running 'pip install loguru'")
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    """
    Parses debug and test arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Parse command line arguments.")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug logging",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        default=False,
        help="Run tests",
    )
    return parser.parse_args()


def setup_logging(log_level: str = "INFO") -> logger:
    """
    Setup loguru logging.

    Args:
        log_level (str): The log level to be set. Default = "INFO"

    Returns:
        logger: Loguru logger object.
    """
    # Define valid log levels
    valid_log_levels = [
        "TRACE",
        "DEBUG",
        "INFO",
        "SUCCESS",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]

    # Validate the log level
    if log_level.upper() not in valid_log_levels:
        raise ValueError(
            f"Invalid log level: {log_level}. Valid log levels are: {', '.join(valid_log_levels)}"
        )

    # Remove all built-in handlers
    logger.remove()
    # Set custom loguru format
    fmt = (
        "<level>{time:YYYY-MM-DD hh:mm:ss A}</level> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{"
        "function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> "
    )
    # Set the log level
    logger.add(sys.stderr, format=fmt, level=log_level.upper())

    # Test logging
    logger.debug("Logging setup complete with level: {}", log_level.upper())

    return logger


LETTERS = [x for x in "abcdefghijklmnopqrstuvwxyz"]
VOWELS = {"a", "e", "i", "o", "u"}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)


def parse_line(regex, line):
    """Returns capture groups in regex for line. Int-ifies numbers."""
    ret = []
    for match in re.match(regex, line).groups():
        try:
            ret.append(int(match))
        except ValueError:
            ret.append(match)
        except TypeError:
            # None match
            pass

    return ret


def parse_nums(line, negatives=True):
    """
    Returns a list of numbers in `line`.

    Pass negatives=False to parse 1-2 as [1, 2].
    """
    num_re = r"-?\d+" if negatives else r"\d+"
    return [int(n) for n in re.findall(num_re, line)]


def new_table(width, height, val=None):
    """Returns a `width` by `height` table populated with `val`."""
    return [[val for _ in range(width)] for _ in range(height)]


def transposed(matrix):
    """Returns the transpose of the given matrix."""
    return [list(r) for r in zip(*matrix)]


def rotated(matrix):
    """Returns the given matrix rotated 90 degrees clockwise."""
    return [list(r) for r in zip(*matrix[::-1])]


def firsts(matrix):
    """Like matrix[0], but for the first column."""
    return rotated(matrix)[0]


def lasts(matrix):
    """Like matrix[-1], but for the last column."""
    return rotated(matrix)[-1]


def mul(lst):
    """Like sum(), but for multiplication."""
    return reduce(operator.mul, lst, 1)  # NOQA


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


def parts(l, n):
    """Splits l into n equal parts. Excess (if it exists) returned as the n+1-th."""
    m = len(l) // n
    for i in range(0, n):
        yield l[i * m : (i + 1) * m]

    if len(l) % n != 0:
        yield l[m * n :]


def all_unique(lst):
    """Returns True if all items in `lst` are unique."""
    return len(lst) == len(set(lst))


def topsort(graph, tiebreak=None):
    """
    Given a graph where graph[x] is an iterable of edges of directed
    edges originating from x, returns a topologically sorted list of
    nodes in the graph.

    If `tiebreak` is given, this lambda is passed to sorted() when
    choosing what node to visit next.
    """
    if tiebreak is None:
        tiebreak = lambda x: x

    visited = set()
    stack = []

    def _topsort(node):
        visited.add(node)

        # Reversed because the DFS causes equal level nodes to be popped backwards.
        for n in sorted(graph[node], key=tiebreak, reverse=True):
            if n not in visited:
                _topsort(n)

        stack.append(node)

    for n in sorted(graph, key=tiebreak, reverse=True):
        if not n in visited:
            _topsort(n)

    return stack[::-1]


def gcd(a, b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)


def egcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def modinv(a, n):
    g, x, _ = egcd(a, n)
    if g == 1:
        return x % n
    else:
        raise ValueError("%d is not invertible mod %d" % (a, n))


def crt(rems, mods):
    """
    Solve a system of modular equivalences via the Chinese Remainder Theorem.
    Does not require pairwise coprime moduli.

    Returns (n, m), where n is the solution and m is the modulo.

    Arguments
      rems: the remainders of the problem
      mods: the modulos of the problem

    """

    # copy inputs
    orems, omods = rems, mods
    rems = list(rems)
    mods = list(mods)

    newrems = []
    newmods = []

    for i in range(len(mods)):
        for j in range(i + 1, len(mods)):
            g = gcd(mods[i], mods[j])
            if g == 1:
                continue
            if rems[i] % g != rems[j] % g:
                raise ValueError(
                    "inconsistent remainders at positions %d and %d (mod %d)"
                    % (i, j, g)
                )
            mods[j] //= g

            while 1:
                # transfer any remaining gcds to mods[j]
                g = gcd(mods[i], mods[j])
                if g == 1:
                    break
                mods[i] //= g
                mods[j] *= g

        if mods[i] == 1:
            continue

        newrems.append(rems[i] % mods[i])
        newmods.append(mods[i])

    rems, mods = newrems, newmods

    # standard CRT
    s = 0
    n = 1
    for k in mods:
        n *= k

    for i in range(len(mods)):
        ni = n // mods[i]
        s += rems[i] * modinv(ni, mods[i]) * ni
    return s % n, n


def min_max_xy(points):
    """
    For a list of points, returns min_x, max_x, min_y, max_y.
    This works on tuples (x, y) and Point(x, y).
    """
    if len(points) == 0:
        return None, None, None, None
    if type(points[0]) == tuple:
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
    else:
        min_x = min(p.x for p in points)
        max_x = max(p.x for p in points)
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)

    return min_x, max_x, min_y, max_y


def print_grid(grid, f=None, quiet=False):
    """
    Outputs `grid` to stdout. This works whether `grid` is a 2D array,
    or a sparse matrix (dictionary) with keys either (x, y) or Point(x, y).

    This function also returns a tuple (a, b), where a is the serialized
    representation of the grid, in case what gets printed out to stdout
    needs to be consumed afterwards, and b is a Counter over the values
    in `grid`.

    Arguments:
        f: a function to transform the values of grid to something printable.
        quiet: don't output to stdout.

    Returns:
        List[String]: Serialized, printable version of the grid.
        Counter: The values contained in the grid.
    """
    if f is None:
        f = lambda x: str(x)  # NOQA

    counts = Counter()
    serialized = []

    if type(grid) is dict:
        positions = list(grid.keys())
        min_x, max_x, min_y, max_y = min_max_xy(positions)
        if type(positions[0]) is tuple:
            for y in range(min_y, max_y + 1):
                row = "".join(f(grid.get((x, y), " ")) for x in range(min_x, max_x + 1))
                if not quiet:
                    print(row)
                serialized.append(row)
                for c in row:
                    counts[c] += 1

        else:
            # (x, y) => point
            for y in range(min_y, max_y + 1):
                row = "".join(
                    f(grid.get(Point(x, y), " ")) for x in range(min_x, max_x + 1)
                )
                if not quiet:
                    print(row)
                serialized.append(row)
                for c in row:
                    counts[c] += 1
    else:
        min_x = 0
        min_y = 0
        for y in range(len(grid)):
            row = "".join(f(grid[y][x]) for x in range(len(grid[0])))
            if not quiet:
                print(row)
            serialized.append(row)
            for x, c in enumerate(row):
                counts[c] += 1
                max_x = x
            max_y = y

    if not quiet:
        print("height={} ({} -> {})".format(max_y - min_y + 1, min_y, max_y))
        print("width={} ({} -> {})".format(max_x - min_x + 1, min_x, max_x))
        print("Statistics:")
        for item, num in counts.most_common():
            print("{}: {}".format(item, num))

    return serialized, counts


def resolve_mapping(candidates):
    """
    Given a dictionary `candidates` mapping keys to candidate values, returns
    a dictionary where each `key` maps to a unique `value`. Hangs if intractable.

    Example:

    candidates = {
        'a': [0, 1, 2],
        'b': [0, 1],
        'c': [0],
    }

    resolve_mapping(candidates) -> {'c': 0, 'b': 1, 'a': 2}
    """
    resolved = {}

    # Ensure the mapping is key -> set(values).
    candidates_map = {}
    for k, v in candidates.items():
        candidates_map[k] = set(v)

    while len(resolved) < len(candidates_map):
        for candidate in candidates_map:
            if len(candidates_map[candidate]) == 1 and candidate not in resolved:
                r = candidates_map[candidate].pop()
                for c in candidates_map:
                    candidates_map[c].discard(r)

                resolved[candidate] = r
                break

    return resolved


def memoize(f):
    """Simple dictionary-based memoization decorator"""
    cache = {}

    def _mem_fn(*args):
        hargs = ",".join(str(x) for x in args)
        if hargs not in cache:
            cache[hargs] = f(*args)
        return cache[hargs]

    _mem_fn.cache = cache
    return _mem_fn


@memoize
def _eratosthenes(n):
    """http://stackoverflow.com/a/3941967/239076"""
    # Initialize list of primes
    _primes = [True] * n

    # Set 0 and 1 to non-prime
    _primes[0] = _primes[1] = False

    for i, is_prime in enumerate(_primes):
        if is_prime:
            yield i

            # Mark factors as non-prime
            for j in range(i * i, n, i):  # NOQA
                _primes[j] = False


@memoize
def primes(n):
    """Return a list of primes from [2, n)"""
    return list(_eratosthenes(n))


@memoize
def factors(n):
    """Returns the factors of n."""
    return sorted(
        x
        for tup in ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
        for x in tup
    )


def md5(msg):
    m = hashlib.md5()
    m.update(msg)
    return m.hexdigest()


def sha256(msg):
    s = hashlib.sha256()
    s.update(msg)
    return s.hexdigest()


def HASH(code):
    val = 0
    for c in code:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def knot_hash(msg):
    lengths = [ord(x) for x in msg] + [17, 31, 73, 47, 23]
    sparse = range(0, 256)
    pos = 0
    skip = 0

    for _ in range(64):
        for l in lengths:
            for i in range(l // 2):
                x = (pos + i) % len(sparse)
                y = (pos + l - i - 1) % len(sparse)
                sparse[x], sparse[y] = sparse[y], sparse[x]

            pos = pos + l + skip % len(sparse)
            skip += 1

    hash_val = 0

    for i in range(16):
        res = 0
        for j in range(0, 16):
            res ^= sparse[(i * 16) + j]

        hash_val += res << ((16 - i - 1) * 8)

    return "%032x" % hash_val


HEX_DIRS = {
    "N": (1, -1, 0),
    "NE": (1, 0, -1),
    "SE": (0, 1, -1),
    "S": (-1, 1, 0),
    "SW": (-1, 0, 1),
    "NW": (0, -1, 1),
}


def hex_distance(x, y, z):
    """Returns a given hex point's distance from the origin."""
    return (abs(x) + abs(y) + abs(z)) // 2


def polygon_perimeter(points):
    """Given a set of bounding box points, returns the perimeter of the polygon."""
    return sum(a.dist_manhattan(b) for a, b in zip(points, points[1:] + [points[0]]))


def polygon_area(points):
    """Given a set of integer bounding box points, returns the total area of the polygon."""
    # Use shoelace formula to compute internal area.
    area = 0

    for a, b in zip(points, points[1:] + [points[0]]):
        area += (b.x + a.x) * (b.y - a.y)

    area = int(abs(area / 2.0))

    # Calculate perimeter.
    perimeter = polygon_perimeter(points)

    # Account for outer perimeter strip in final area computation.
    return area + (perimeter // 2) + 1


@total_ordering
class Point:
    """Simple 2-dimensional point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)

    def __div__(self, n):
        return Point(self.x / n, self.y / n)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq__(self, other):
        if type(other) != Point:
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.length < other.length

    def __invert__(self):
        return Point(-self.y, -self.x)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def dist_manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def dist_chess(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def dist_chebyshev(self, other):
        return self.dist_chess(other)

    def angle(self, to=None):
        if to is None:
            return math.atan2(self.y, self.x)
        return math.atan2(self.y - to.y, self.x - to.x)

    def rotate(self, turns):
        """Returns the rotation of the Point around (0, 0) `turn` times clockwise."""
        turns = turns % 4

        if turns == 1:
            return Point(self.y, -self.x)
        elif turns == 2:
            return Point(-self.x, -self.y)
        elif turns == 3:
            return Point(-self.y, self.x)
        else:
            return self

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def chess(self):
        return max(abs(self.x), abs(self.y))

    @property
    def chebyshev(self):
        return self.chess

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def neighbours_4(self):
        return [self + p for p in DIRS_4]

    def neighbors_4(self):
        return self.neighbours_4()

    def neighbours(self):
        return self.neighbours_4()

    def neighbors(self):
        return self.neighbours()

    def neighbours_8(self):
        return [self + p for p in DIRS_8]

    def neighbors_8(self):
        return self.neighbours_8()


N = Point(0, 1)
NE = Point(1, 1)
E = Point(1, 0)
SE = Point(1, -1)
S = Point(0, -1)
SW = Point(-1, -1)
W = Point(-1, 0)
NW = Point(-1, 1)

DIRS_4 = DIRS = [
    Point(0, 1),  # north
    Point(1, 0),  # east
    Point(0, -1),  # south
    Point(-1, 0),  # west
]

DIRS_8 = [
    Point(0, 1),  # N
    Point(1, 1),  # NE
    Point(1, 0),  # E
    Point(1, -1),  # SE
    Point(0, -1),  # S
    Point(-1, -1),  # SW
    Point(-1, 0),  # W
    Point(-1, 1),  # NW
]


class UnionFind:
    """
    If this comes in handy, thank you mcpower!
    https://www.reddit.com/r/adventofcode/comments/a9c61w/2018_day_25_solutions/eci5kaf/
    """

    # n: int
    # parents: List[Optional[int]]
    # ranks: List[int]
    # num_sets: int

    def __init__(self, n: int) -> None:
        self.n = n
        self.parents = [None] * n
        self.ranks = [1] * n
        self.num_sets = n

    def find(self, i: int) -> int:
        p = self.parents[i]
        if p is None:
            return i
        p = self.find(p)
        self.parents[i] = p
        return p

    def in_same_set(self, i: int, j: int) -> bool:
        return self.find(i) == self.find(j)

    def merge(self, i: int, j: int) -> None:
        i = self.find(i)
        j = self.find(j)

        if i == j:
            return

        i_rank = self.ranks[i]
        j_rank = self.ranks[j]

        if i_rank < j_rank:
            self.parents[i] = j
        elif i_rank > j_rank:
            self.parents[j] = i
        else:
            self.parents[j] = i
            self.ranks[i] += 1
        self.num_sets -= 1


class Point:
    """Simple 2-dimensional point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)

    def __div__(self, n):
        return Point(self.x / n, self.y / n)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq__(self, other):
        if type(other) != Point:
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.length < other.length

    def __invert__(self):
        return Point(-self.y, -self.x)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def dist_manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def dist_chess(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def dist_chebyshev(self, other):
        return self.dist_chess(other)

    def angle(self, to=None):
        if to is None:
            return math.atan2(self.y, self.x)
        return math.atan2(self.y - to.y, self.x - to.x)

    def rotate(self, turns):
        """Returns the rotation of the Point around (0, 0) `turn` times clockwise."""
        turns = turns % 4

        if turns == 1:
            return Point(self.y, -self.x)
        elif turns == 2:
            return Point(-self.x, -self.y)
        elif turns == 3:
            return Point(-self.y, self.x)
        else:
            return self

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def chess(self):
        return max(abs(self.x), abs(self.y))

    @property
    def chebyshev(self):
        return self.chess

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def neighbours_4(self):
        return [self + p for p in DIRS_4]

    def neighbors_4(self):
        return self.neighbours_4()

    def neighbours(self):
        return self.neighbours_4()

    def neighbors(self):
        return self.neighbours()

    def neighbours_8(self):
        return [self + p for p in DIRS_8]

    def neighbors_8(self):
        return self.neighbours_8()


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logging("DEBUG" if args.debug else "INFO")
    if args.test:
        logger.info("Running tests...")
