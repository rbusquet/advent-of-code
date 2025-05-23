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


def neighborhood(i: int, j: int) -> Iterator[Position]:
    for d in Direction:
        ii, jj = d.value
        yield (i + ii, j + jj)


class Maze:
    def __init__(
        self, start: Position, goal: Position, grid: dict[Position, str]
    ) -> None:
        self.start = start
        self.goal = goal
        self.grid = grid

    def best_path(self) -> tuple[int, set[Position]]:
        queue = deque[tuple[Position, tuple[Position, ...]]]()
        queue.append((self.start, (self.start,)))

        cost = defaultdict[Position, int](lambda: sys.maxsize)
        best = sys.maxsize
        cost[self.start] = 0
        tiles = set[Position]()

        while queue:
            current = queue.pop()
            position, path = current

            known_cost = cost[position]

            if position == self.goal:
                best = known_cost
                tiles = set(path)
                break

            for n in neighborhood(*position):
                step_cost = 1
                if n not in self.grid or self.grid[n] == "#":  # wall
                    continue

                tentative_cost = cost[position] + step_cost
                if cost[n] > tentative_cost:
                    cost[n] = tentative_cost
                    queue.appendleft((n, (*path, n)))

        return best, tiles


def run(count, size, end) -> None:
    grid = {}
    for i in range(size):
        for j in range(size):
            grid[i, j] = "."
    progress = iter(eval(line) for line in input.read_text().splitlines())
    i = 0
    for line in progress:
        if i >= count:
            break
        grid[line] = "#"
        i += 1

    maze = Maze((0, 0), end, grid)
    best, path = maze.best_path()
    print(f"part 1: {best}")

    for line in progress:
        position = line
        grid[position] = "#"
        if position in path:
            best, path = maze.best_path()
            if best == sys.maxsize:
                print(f"part 2: {position}")
                break


run(1024, 71, (70, 70))
