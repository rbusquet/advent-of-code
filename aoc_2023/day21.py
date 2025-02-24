from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


Position = tuple[int, int]


@dataclass(order=True)
class Entry:
    cost: int
    position: Position = field(compare=False)


def neighborhood(x, y, grid, max_x, max_y):
    possible = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for xx, yy in possible:
        if grid[xx % (max_x + 1), yy % (max_y + 1)] != "#":
            yield xx, yy


def part_1(file: TextIO) -> int:
    """
    Starting from the top left calculate the shortest path to
    the bottom right corner.
    """
    grid = defaultdict[Position, str](lambda: ".")
    costs = defaultdict[Position, int](lambda: sys.maxsize)

    queue = PriorityQueue[Entry]()
    sx = sy = 0

    max_x = max_y = 0
    for i, line in enumerate(strip_lines(file)):
        for j, char in enumerate(line):
            grid[i, j] = char
            if char == "S":
                sx, sy = i, j
            max_x = max(max_x, i)
            max_y = max(max_y, j)

    costs[(sx, sy)] = 0
    queue.put(Entry(0, (sx, sy)))

    max_distance = 0

    while u := queue.get():
        for x, y in neighborhood(*u.position, grid, max_x=max_x, max_y=max_y):
            current_cost = costs[x, y]
            alternative_cost = costs[u.position] + 1
            max_distance = max(max_distance, alternative_cost)
            if max_distance > 64:
                break
            if alternative_cost < current_cost:
                costs[x, y] = alternative_cost
                queue.put(Entry(alternative_cost, (x, y)))
        else:
            continue
        break

    can_reach = 0
    for k, v in costs.items():
        if v % 2 == 0:
            can_reach += 1

    return can_reach


def part_2(file: TextIO) -> int:
    file.seek(0)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
