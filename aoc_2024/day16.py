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


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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

    def recover_path(
        self,
        came_from: dict[tuple[Position, Direction], tuple[Position, Direction]],
        goal: Position,
        direction: Direction,
    ) -> list[tuple[Position, Direction]]:
        path = []
        current = (goal, direction)
        while current in came_from:
            path.append(current)
            current = came_from[current]
        return path

    def h(self, position: Position) -> int:
        return manhattan_distance(position, self.goal)

    def calculate_points(self) -> int | None:
        queue = Queue[tuple[Position, Direction]]()
        queue.add_task((self.start, Direction.E), self.h(self.start))

        cost = defaultdict[Position, int](lambda: sys.maxsize)
        cost[self.start] = 0
        came_from = dict[tuple[Position, Direction], tuple[Position, Direction]]()

        while current := queue.pop_task():
            position, direction = current

            if position == self.goal:
                # path = self.recover_path(came_from, self.goal, direction)
                # in_path.update(p[0] for p in path)
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
                    queue.add_task((n, d), tentative_cost + self.h(n))

        return cost[self.goal]


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
    return 0


print(part_1())
print(part_2())
