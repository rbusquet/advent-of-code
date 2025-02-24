import itertools
from collections.abc import Iterator
from heapq import heappop, heappush
from pathlib import Path

N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)

Point = tuple[int, int]


class Queue[T]:
    """
    From https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """

    def __init__(self) -> None:
        self.pq = list[tuple[float, int, T]]()  # list of entries arranged in a heap
        self.entry_finder = dict[
            T, tuple[float, int, T]
        ]()  # mapping of tasks to entries
        self.REMOVED = "<removed-task>"  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task: T, priority: float = 0.0) -> None:
        "Add a new task or update the priority of an existing task"
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry  # type: ignore[assignment]
        heappush(self.pq, entry)  # type: ignore[misc]

    def remove_task(self, task: T) -> None:
        "Mark an existing task as REMOVED.  Raise KeyError if not found."
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED  # type: ignore[index]

    def pop_task(self) -> T | None:
        "Remove and return the lowest priority task. Return None if empty."
        while self.pq:
            *_, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task

        return None


def neighborhood(i: int, j: int) -> Iterator[Point]:
    for ii, jj in (N, S, E, W):
        yield i + ii, j + jj


def part_1() -> int:
    risk_map = dict[Point, int]()
    distances = dict[Point, float]()
    distances[0, 0] = 0
    paths = dict[Point, Point | None]()

    queue = Queue[Point]()
    with open(Path(__file__).parent / "input.txt") as file:
        for i, line in enumerate(file):
            for j, value in enumerate(line.strip()):
                risk_map[i, j] = int(value)
                if (i, j) != (0, 0):
                    distances[i, j] = float("inf")
                    paths[i, j] = None
                queue.add_task((i, j), distances[i, j])

    distances[0, 0] = 0.0
    while u := queue.pop_task():
        for n in neighborhood(*u):
            if n not in risk_map:
                continue
            alt = distances[u] + risk_map[n]
            if alt < distances[n]:
                distances[n] = alt
                paths[n] = u
                queue.add_task(n, alt)
    return int(distances[max(risk_map)])


def part_2() -> int:
    risk_map = dict[Point, int]()
    distances = dict[Point, float]()
    distances[0, 0] = 0
    paths = dict[Point, Point | None]()

    queue = Queue[Point]()
    with open(Path(__file__).parent / "input.txt") as file:
        for i, line in enumerate(file):
            for j, value in enumerate(line.strip()):
                risk_map[i, j] = int(value)
                if (i, j) != (0, 0):
                    distances[i, j] = float("inf")
                    paths[i, j] = None
                queue.add_task((i, j), distances[i, j])

        tile_i, tile_j = max(risk_map)
        tile_i += 1
        tile_j += 1

        for i in range(tile_i * 5):
            for j in range(tile_j * 5):
                if (i, j) in risk_map:
                    continue

                if (i - tile_i, j) in risk_map:
                    risk = risk_map[i - tile_i, j] + 1
                elif (i, j - tile_j) in risk_map:
                    risk = risk_map[i, j - tile_j] + 1
                if risk > 9:
                    risk = 1
                risk_map[i, j] = risk
                distances[i, j] = float("inf")
                paths[i, j] = None
                queue.add_task((i, j), distances[i, j])

    distances[0, 0] = 0.0
    find_paths(risk_map, distances, paths, queue)
    return int(distances[max(risk_map)])


def find_paths(
    risk_map: dict[Point, int],
    distances: dict[Point, float],
    paths: dict[Point, Point | None],
    queue: Queue[Point],
) -> None:
    while u := queue.pop_task():
        for n in neighborhood(*u):
            if n not in risk_map:
                continue
            alt = distances[u] + risk_map[n]
            if alt < distances[n]:
                distances[n] = alt
                paths[n] = u
                queue.add_task(n, alt)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
