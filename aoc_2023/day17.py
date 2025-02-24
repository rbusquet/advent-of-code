import argparse
import sys
from collections import defaultdict, namedtuple
from collections.abc import Iterator
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import TextIO


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

    queue = PriorityQueue[Entry]()
    start = Step(0, 0, 0, None)
    queue.put(Entry(0, start))

    end = 0, 0
    for i, line in enumerate(strip_lines(file)):
        for j, char in enumerate(line):
            grid[i, j] = int(char)
            end = i, j

    costs[start] = 0

    while u := queue.get().step:
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
                queue.put(Entry(alternative_cost + heuristic((x, y), end), n))

    raise ValueError("No path found")


@dataclass(order=True)
class Entry:
    cost: int
    step: Step | None = field(compare=False)


def part_2(file: TextIO) -> int:
    """
    Starting from the top left calculate the shortest path to
    the bottom right corner.
    """
    file.seek(0)
    grid = dict[tuple[int, int], int]()
    costs = defaultdict[Step, int](lambda: sys.maxsize)

    queue = PriorityQueue[Entry]()
    start = Step(0, 0, 0, None)
    queue.put(Entry(0, start))

    end = 0, 0
    for i, line in enumerate(strip_lines(file)):
        for j, char in enumerate(line):
            grid[i, j] = int(char)
            end = i, j

    costs[start] = 0

    while u := queue.get_nowait().step:
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
                queue.put_nowait(Entry(alternative_cost + heuristic((x, y), end), n))

    raise ValueError("No path found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
