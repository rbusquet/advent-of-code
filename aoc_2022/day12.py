import argparse
import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
from email.policy import default
from heapq import heappop, heappush
from typing import Generic, Iterator, TextIO, TypeVar


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)

Point = tuple[int, int]


T = TypeVar("T")


@dataclass(slots=True, order=True)
class Entry(Generic[T]):
    priority: float
    count: int
    task: T
    removed: bool = False


class Queue(Generic[T]):
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


def neighborhood(i: int, j: int) -> Iterator[Point]:
    for ii, jj in (N, S, E, W):
        yield i + ii, j + jj


def part_1(file: TextIO) -> int:
    """
    Starting from S, calculate a dijkstra distance to E.
    """
    heights = dict[Point, int]()
    distances = defaultdict[Point, int](lambda: sys.maxsize)
    paths = dict[Point, Point | None]()

    queue = Queue[Point]()
    start = end = 0, 0
    for i, line in enumerate(file):
        if not line.strip():
            break
        for j, value in enumerate(line.strip()):
            match value:
                case "S":
                    heights[i, j] = ord("a")
                    start = i, j
                case "E":
                    heights[i, j] = ord("z")
                    end = i, j
                case _:
                    heights[i, j] = ord(value)

    distances[start] = 0
    queue.add_task(start, 0)
    distances[start] = 0
    while u := queue.pop_task():
        for n in neighborhood(*u):
            if n not in heights:
                continue
            step = heights[n]
            # can't move if step is heigher than current + 1
            if step > heights[u] + 1:
                continue
            alt = distances[u] + 1
            if alt < distances[n]:
                distances[n] = alt
                paths[n] = u
                queue.add_task(n, alt)
    return distances[end]


def part_2(file: TextIO) -> int:
    """
    start from the end, return the minimum of the distances
    from E to any `a`.
    """
    heights = dict[Point, int]()
    distances = defaultdict[Point, int](lambda: sys.maxsize)
    paths = dict[Point, Point | None]()

    queue = Queue[Point]()
    all_starts = list[Point]()
    end = 0, 0
    for i, line in enumerate(file):
        if not line.strip():
            break
        for j, value in enumerate(line.strip()):
            match value:
                case "S" | "a":
                    heights[i, j] = ord("a")
                    all_starts.append((i, j))
                case "E":
                    heights[i, j] = ord("z")
                    end = i, j
                case _:
                    heights[i, j] = ord(value)

    distances[end] = 0
    queue.add_task(end, 0)
    distances[end] = 0
    while u := queue.pop_task():
        for n in neighborhood(*u):
            if n not in heights:
                continue
            step = heights[n]

            # now I'm starting from the end and going down.
            # I only got at the current point from a point 1 down or high above
            if step < heights[u] - 1:
                continue
            alt = distances[u] + 1
            if alt < distances[n]:
                distances[n] = alt
                paths[n] = u
                queue.add_task(n, alt)
    return min(distances[start] for start in all_starts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)

    print(part_1(args.infile))
    args.infile.seek(0)

    print(part_2(args.infile))
