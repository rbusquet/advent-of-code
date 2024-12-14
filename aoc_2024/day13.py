import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from pathlib import Path
from typing import Generic, TypeVar

import numpy as np

input = Path(__file__).parent / "input.txt"


Position = tuple[int, int]


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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


def count_button_press(cameFrom, current) -> int:
    presses = 0
    while current in cameFrom:
        current = cameFrom[current]
        presses += 1
    return presses


class Arcade:
    def __init__(self, a: str, b: str, goal: Position) -> None:
        self.a = lambda X, Y: eval(a)
        self.b = lambda X, Y: eval(b)
        self.goal = goal

    def h(self, position: Position) -> int:
        return manhattan_distance(position, self.goal)

    def calculate_cost(self) -> int | None:
        queue = Queue[Position]()
        queue.add_task((0, 0), self.h((0, 0)))

        cost = defaultdict[Position, int](lambda: sys.maxsize)
        cost[0, 0] = 0
        pressed = 0
        came_from = dict[Position, Position]()

        while current := queue.pop_task():
            if current == self.goal:
                return cost[current]
            if came_from:
                count = count_button_press(came_from, current)
                if count > 200:
                    return None

            press_a = self.a(*current)
            tentative_cost = cost[current] + 3
            if tentative_cost < cost[press_a]:
                came_from[press_a] = current
                cost[press_a] = tentative_cost
                queue.add_task(press_a, tentative_cost + self.h(press_a))
                pressed += 1

            press_b = self.b(*current)

            tentative_cost = cost[current] + 1
            if tentative_cost < cost[press_b]:
                came_from[press_a] = current
                cost[press_b] = tentative_cost
                queue.add_task(press_b, tentative_cost + self.h(press_b))
                pressed += 1
        return cost[self.goal]

    def calculate_cost_fast(self) -> int | None:
        x1, y1 = self.a(0, 0)
        x2, y2 = self.b(0, 0)
        b1, b2 = self.goal

        A = np.array([[x1, x2], [y1, y2]])
        B = np.array([[b1], [b2]])

        X = np.linalg.solve(A, B)
        a, b = np.rot90(X)[0]
        if almost_integer(a) and almost_integer(b):
            return a * 3 + b

        return None


def almost_integer(a: np.float64) -> bool:
    return np.isclose(np.rint(a) - a, 0, atol=0.01)


def read_prize(X, Y, offset=0):
    return (X + offset, Y + offset)


def part_1() -> int:
    data = input.read_text().splitlines()

    arcades = list[Arcade]()
    for i in range(0, len(data), 4):
        a, b, prize, *_ = data[i : i + 3]
        action_a = a.split(":")[1]
        action_b = b.split(":")[1]
        prize_position = eval(f"read_prize({prize.split(':')[1]})")
        arcades.append(Arcade(action_a, action_b, prize_position))
    return sum(cost for arcade in arcades if (cost := arcade.calculate_cost_fast()))


def part_2() -> int:
    data = input.read_text().splitlines()

    arcades = list[Arcade]()
    for i in range(0, len(data), 4):
        a, b, prize, *_ = data[i : i + 3]
        action_a = a.split(":")[1]
        action_b = b.split(":")[1]
        prize_position = eval(
            f"read_prize({prize.split(':')[1]}, offset=10000000000000)"
        )
        arcades.append(Arcade(action_a, action_b, prize_position))

    return sum(cost for arcade in arcades if (cost := arcade.calculate_cost_fast()))


print(part_1())
print("---------")
print(part_2())
