import enum
import sys
from collections import defaultdict, deque
from collections.abc import Iterator
from pathlib import Path

input = Path(__file__).parent / "input.txt"


Position = tuple[int, int]


class Direction(enum.Enum):
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)

    def opposite(self) -> "Direction":
        return {
            Direction.N: Direction.S,
            Direction.E: Direction.W,
            Direction.S: Direction.N,
            Direction.W: Direction.E,
        }[self]

    def __str__(self) -> str:
        return {
            Direction.N: "^",
            Direction.E: ">",
            Direction.S: "v",
            Direction.W: "<",
        }[self]


def neighborhood(i: int, j: int) -> Iterator[tuple[Position, Direction]]:
    for d in Direction:
        ii, jj = d.value
        yield (i + ii, j + jj), d


class Maze:
    def __init__(
        self, start: Position, goal: Position, grid: dict[Position, str]
    ) -> None:
        self.start = start
        self.goal = goal
        self.grid = grid

    def best_seats(self) -> tuple[int, int]:
        queue = deque[tuple[Position, Direction, int, tuple[Position, ...]]]()
        queue.append((self.start, Direction.E, 0, (self.start,)))

        cost = defaultdict[tuple[Position, Direction], int](lambda: sys.maxsize)
        best = sys.maxsize
        cost[self.start, Direction.E] = 0
        tiles = set[Position]()

        while queue:
            current = queue.pop()
            position, direction, current_cost, path = current

            known_cost = cost[position, direction]
            if known_cost < current_cost:
                # been here with a better cost
                continue

            if current_cost > best:
                # bail out
                continue

            cost[position, direction] = current_cost

            if position == self.goal:
                if current_cost < best:
                    best = current_cost
                    tiles = set(path)
                else:
                    tiles |= set(path)

            for n, d in neighborhood(*position):
                step_cost = 1
                if n not in self.grid or self.grid[n] == "#":  # wall
                    continue
                elif d == direction.opposite():
                    # do not move backwards
                    continue
                elif d != direction:
                    step_cost += 1_000

                tentative_cost = cost[position, direction] + step_cost
                queue.appendleft((n, d, tentative_cost, (*path, n)))

        return best, len(tiles)


def run() -> tuple[int, int]:
    grid = {}
    for x, line in enumerate(input.read_text().splitlines()):
        for y, tile in enumerate(line):
            grid[x, y] = tile
            if tile == "S":
                start = x, y
            if tile == "E":
                goal = x, y

    maze = Maze(start, goal, grid)
    return maze.best_seats()


print(run())
