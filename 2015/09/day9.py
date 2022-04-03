import itertools
import re
import sys
import typing as t
from collections import defaultdict
from copy import deepcopy
from heapq import heappop, heappush
from pathlib import Path

expression = re.compile(r"(\w+) to (\w+) = (\d+)")

T = t.TypeVar("T")


class Queue(t.Generic[T]):
    """
    From https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """

    def __init__(self) -> None:
        self.pq = list[tuple[float, int, T]]()  # list of entries arranged in a heap
        self.entry_finder = dict[
            T, tuple[float, int, T]
        ]()  # mapping of items to entries
        self.REMOVED = "<removed-item>"  # placeholder for a removed item
        self.counter = itertools.count()  # unique sequence count

    def add_item(self, item: T, priority: float = 0.0) -> None:
        "Add a new item or update the priority of an existing item"
        if item in self.entry_finder:
            self.remove_item(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entry_finder[item] = entry  # type: ignore[assignment]
        heappush(self.pq, entry)  # type: ignore[misc]

    def remove_item(self, item: T) -> None:
        "Mark an existing item as REMOVED.  Raise KeyError if not found."
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED  # type: ignore[index]

    def pop_item(self) -> T | None:
        "Remove and return the lowest priority item. Return None if empty."
        while self.pq:
            *_, item = heappop(self.pq)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item

        return None


def Dijkstra(Graph, source):
    dist = defaultdict[str, int](lambda: sys.maxsize)
    dist[source] = 0
    queue = Queue[str]()
    prev = {}

    for v in Graph:
        if v != source:
            prev[v] = None
        queue.add_item(v, dist[v])

    while True:
        u = queue.pop_item()
        if u is None:
            break
        for v, edge in Graph[u]:
            alt = dist[u] + edge
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                queue.add_item(v, alt)
    return dist, prev


def part_1() -> int:
    file = Path(__file__).parent / "input.txt"
    contents = file.read_text()
    graph = defaultdict[str, list[str, float]](list)
    sources = list[str]()
    for line in contents.splitlines():
        if (match := expression.match(line)) is None:
            continue
        a, b, value = match.groups()
        graph[a].append((b, float(value)))
        sources.append(a)
    for source in sources:
        dist, prev = Dijkstra(deepcopy(graph), source)
        print(dist, prev)


def part_2() -> int:
    file = Path(__file__).parent / "input.txt"
    contents = file.read_text()
    for line in contents.splitlines():
        print(line)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
