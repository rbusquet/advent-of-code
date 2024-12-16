import enum
import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from pathlib import Path
from typing import Iterator

input = Path(__file__).parent / "input.txt"


Position = tuple[int, int]


@dataclass(slots=True, order=True)
class Entry[T]:
    priority: float
    count: int
    task: T
    removed: bool = False


class Queue[T]:
    """
    From https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """

    def __init__(self) -> None:
        self.pq = list[Entry[T]]()  # list of entries arranged in a heap
        self.entry_finder = dict[T, Entry[T]]()  # mapping of tasks to entries
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task: T, priority: float = 0.0) -> None:
        "Add a new task or update the priority of an existing task"
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = Entry(priority, count, task)
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task: T) -> None:
        "Mark an existing task as REMOVED.  Raise KeyError if not found."
        entry = self.entry_finder.pop(task)
        entry.removed = True

    def pop_task(self) -> T | None:
        "Remove and return the lowest priority task. Return None if empty."
        while self.pq:
            entry = heappop(self.pq)
            # if task is not self.REMOVED:
            if not entry.removed:
                del self.entry_finder[entry.task]
                return entry.task

        return None


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

    def calculate_points(self) -> int | None:
        queue = Queue[tuple[Position, Direction]]()
        queue.add_task((self.start, Direction.E))

        cost = defaultdict[Position, int](lambda: sys.maxsize)
        cost[self.start] = 0
        came_from = dict[tuple[Position, Direction], tuple[Position, Direction]]()

        while current := queue.pop_task():
            position, direction = current

            if position == self.goal:
                break

            for n, d in neighborhood(*position):
                step_cost = 1
                if n not in self.grid or self.grid[n] == "#":  # wall
                    continue
                elif d == direction.opposite():
                    # do not move backwards
                    continue
                elif d != direction:
                    step_cost += 1_000

                tentative_cost = cost[position] + step_cost

                if tentative_cost < cost[n]:
                    came_from[(n, d)] = current
                    cost[n] = tentative_cost
                    queue.add_task((n, d), tentative_cost)

        return cost[self.goal]

    def best_seats(self) -> int | None:
        queue = Queue[tuple[Position, Direction, int, tuple[Position, ...]]]()
        queue.add_task((self.start, Direction.E, 0, (self.start,)), 0)

        cost = defaultdict[tuple[Position, Direction], int](lambda: sys.maxsize)
        best = sys.maxsize
        cost[self.start, Direction.E] = 0
        tiles = set[Position]()

        while current := queue.pop_task():
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
                queue.add_task((n, d, tentative_cost, (*path, n)), tentative_cost)

        return len(tiles)


def part_1() -> int:
    grid = {}
    for x, line in enumerate(input.read_text().splitlines()):
        for y, tile in enumerate(line):
            grid[x, y] = tile
            if tile == "S":
                start = x, y
            if tile == "E":
                goal = x, y

    maze = Maze(start, goal, grid)
    return maze.calculate_points() or 0


def part_2() -> int:
    grid = {}
    for x, line in enumerate(input.read_text().splitlines()):
        for y, tile in enumerate(line):
            grid[x, y] = tile
            if tile == "S":
                start = x, y
            if tile == "E":
                goal = x, y

    maze = Maze(start, goal, grid)
    return maze.best_seats() or 0


print(part_1())
print(part_2())
