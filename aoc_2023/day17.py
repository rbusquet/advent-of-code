import argparse
import itertools
import sys
from collections import defaultdict, namedtuple
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Generic, Iterator, TextIO, TypeVar


@dataclass
class Arguments:
    file: TextIO = sys.stdin


DIRECTIONS = dict(
    N=(-1, 0),
    S=(1, 0),
    E=(0, 1),
    W=(0, -1),
)

Step = namedtuple("Step", "x y steps direction")
T = TypeVar("T")


@dataclass(slots=True, order=True)
class Entry(Generic[T]):
    priority: float
    count: int
    task: T = field(compare=False)
    removed: bool = field(default=False, compare=False)


class Queue(Generic[T]):
    """
    From https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes  # noqa: E501
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


OPPOSITES = {"N": "S", "S": "N", "E": "W", "W": "E"}


def neighborhood(step: Step) -> Iterator[Step]:
    if step.direction is None:
        yield Step(0, 1, 1, "E")
        yield Step(1, 0, 1, "S")
        return

    for direction, (ii, jj) in DIRECTIONS.items():
        next_x, next_y = step.x + ii, step.y + jj
        if direction == OPPOSITES[step.direction]:
            continue
        if direction == step.direction:
            next_step = step.steps + 1
            if next_step >= 3:
                continue
            yield Step(next_x, next_y, next_step, direction)
        else:
            yield Step(next_x, next_y, 0, direction)


def neighborhood_part2(step: Step, end: tuple[int, int]) -> Iterator[Step]:
    if step.direction is None:
        yield Step(0, 1, 1, "E")
        yield Step(1, 0, 1, "S")
        return

    if step.steps < 3:
        dx, dy = DIRECTIONS[step.direction]
        yield Step(step.x + dx, step.y + dy, step.steps + 1, step.direction)
    else:
        for direction, (ii, jj) in DIRECTIONS.items():
            if direction == OPPOSITES[step.direction]:
                continue
            next_x, next_y = step.x + ii, step.y + jj
            if next_x > end[0] + 1 or next_y > end[1] + 1 or next_x < 0 or next_y < 0:
                continue
            if direction == step.direction:
                next_steps = step.steps + 1
                if next_steps >= 10:
                    continue
                yield Step(next_x, next_y, next_steps, direction)
            else:
                yield Step(next_x, next_y, 0, direction)


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def part_1(file: TextIO) -> int:
    """
    Starting from the top left calculate the shortest path to
    the bottom right corner.
    """
    grid = dict[tuple[int, int], int]()
    costs = defaultdict[Step, int](lambda: sys.maxsize)

    queue = Queue[Step]()
    start = Step(0, 0, 0, None)
    queue.add_task(start, 0)

    end = 0, 0
    for i, line in enumerate(strip_lines(file)):
        for j, char in enumerate(line):
            grid[i, j] = int(char)
            end = i, j

    costs[start] = 0

    while u := queue.pop_task():
        for n in neighborhood(u):
            x, y = n.x, n.y
            if (x, y) not in grid:
                continue
            if (x, y) == end:
                return costs[u] + grid[x, y]

            current_cost = costs[n]
            alternative_cost = costs[u] + grid[x, y]
            if alternative_cost < current_cost:
                costs[n] = alternative_cost
                queue.add_task(n, alternative_cost + heuristic((x, y), end))

    raise ValueError("No path found")


def part_2(file: TextIO) -> int:
    """
    Starting from the top left calculate the shortest path to
    the bottom right corner.
    """
    file.seek(0)
    grid = dict[tuple[int, int], int]()
    costs = defaultdict[Step, int](lambda: sys.maxsize)

    queue = Queue[Step]()
    start = Step(0, 0, 0, None)
    queue.add_task(start, 0)

    end = 0, 0
    for i, line in enumerate(strip_lines(file)):
        for j, char in enumerate(line):
            grid[i, j] = int(char)
            end = i, j

    costs[start] = 0

    while u := queue.pop_task():
        for n in neighborhood_part2(u, end):
            x, y = n.x, n.y
            if (x, y) not in grid:
                continue
            if (x, y) == end and n.steps >= 4:
                return costs[u] + grid[x, y]

            current_cost = costs[n]
            alternative_cost = costs[u] + grid[x, y]
            if alternative_cost < current_cost:
                costs[n] = alternative_cost
                queue.add_task(n, alternative_cost + heuristic((x, y), end))

    raise ValueError("No path found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
