import itertools
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from pathlib import Path

expression = re.compile(r"(\w+) to (\w+) = (\d+)")


@dataclass(slots=True, order=True)
class Entry[T]:
    priority: int
    count: int
    item: T
    removed: bool = False


class Queue[T]:
    """
    From https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """

    def __init__(self) -> None:
        self.pq = list[Entry]()  # list of entries arranged in a heap
        self.entry_finder = dict[T, Entry]()  # mapping of items to entries
        self.counter = itertools.count()  # unique sequence count

    def add_item(self, item: T, priority: int = 0) -> None:
        "Add a new item or update the priority of an existing item"
        if item in self.entry_finder:
            self.remove_item(item)
        count = next(self.counter)
        entry = Entry(priority, count, item)
        self.entry_finder[item] = entry
        heappush(self.pq, entry)

    def remove_item(self, item: T) -> None:
        "Mark an existing item as REMOVED.  Raise KeyError if not found."
        entry = self.entry_finder.pop(item)
        entry.removed = True

    def pop_item(self) -> T | None:
        "Remove and return the lowest priority item. Return None if empty."
        while self.pq:
            entry = heappop(self.pq)
            if not entry.removed:
                del self.entry_finder[entry.item]
                return entry.item

        return None


Item = tuple[int, tuple[int, ...]]
Distance = list[tuple[int, int]]


def Dijkstra(V: int, distances: defaultdict[int, Distance]) -> defaultdict[Item, int]:
    cost = defaultdict[Item, int](lambda: sys.maxsize)
    queue = Queue[Item]()
    for node in range(0, V):
        item = node, (node,)
        cost[item] = 0
        queue.add_item(item, 0)

    while front := queue.pop_item():
        current, mask = front
        for child, weight in distances[current]:
            if child in mask:
                continue
            next_path = mask + (child,)
            child_item = child, next_path
            tentative_distance = cost[front] + weight
            if cost[child_item] > tentative_distance:
                queue.add_item(child_item, tentative_distance)
                cost[child, next_path] = tentative_distance
    return cost


def part_1() -> int:
    file = Path(__file__).parent / "input.txt"
    contents = file.read_text()
    counter = itertools.count()
    nodes = defaultdict[str, int](lambda: next(counter))

    distances = defaultdict[int, Distance](list)
    for line in contents.splitlines():
        if (match := expression.match(line)) is None:
            continue
        a, b, value = map(str, match.groups())
        da = nodes[a]
        db = nodes[b]
        distances[da].append((db, int(value)))
        distances[db].append((da, int(value)))

    cost = Dijkstra(len(nodes), distances)
    answer = sys.maxsize

    for n, path in cost.keys():
        if len(path) != len(nodes):
            continue
        answer = min(answer, cost[n, path])
        # print(path, "=>", cost[n, path])

    return answer


def part_2() -> int:
    file = Path(__file__).parent / "input.txt"
    contents = file.read_text()
    counter = itertools.count()
    nodes = defaultdict[str, int](lambda: next(counter))

    distances = defaultdict[int, Distance](list)
    for line in contents.splitlines():
        if (match := expression.match(line)) is None:
            continue
        a, b, value = map(str, match.groups())
        da = nodes[a]
        db = nodes[b]
        distances[da].append((db, int(value)))
        distances[db].append((da, int(value)))

    cost = Dijkstra(len(nodes), distances)
    answer = 0

    for n, path in cost.keys():
        if len(path) != len(nodes):
            continue
        answer = max(answer, cost[n, path])
        # print(path, "=>", cost[n, path])

    return answer


if __name__ == "__main__":
    print(part_1())
    print(part_2())
