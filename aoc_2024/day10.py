from collections import deque
from collections.abc import Iterator
from pathlib import Path

input = Path(__file__).parent / "input.txt"

Position = tuple[int, int]

N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)


def neighborhood(i: int, j: int) -> Iterator[Position]:
    for ii, jj in (N, S, E, W):
        yield i + ii, j + jj


def score(trailhead: Position, grid: list[str]) -> int:
    queue = deque([trailhead])
    height = len(grid)
    width = len(grid[0])

    tops = set[Position]()

    while queue:
        current = queue.pop()
        x, y = current
        current_height = int(grid[x][y])
        if current_height == 9:
            tops.add(current)
            continue
        for n in neighborhood(*current):
            ii, jj = n
            if ii < 0 or ii >= height:
                continue
            if jj < 0 or jj >= width:
                continue
            step = int(grid[ii][jj]) - current_height
            if step == 1:
                queue.append(n)

    return len(tops)


def rating(trailhead: Position, grid: list[str]) -> int:
    queue = deque([trailhead])
    height = len(grid)
    width = len(grid[0])

    tops = list[Position]()

    while queue:
        current = queue.pop()
        x, y = current
        current_height = int(grid[x][y])
        if current_height == 9:
            tops.append(current)
            continue
        for n in neighborhood(*current):
            ii, jj = n
            if ii < 0 or ii >= height:
                continue
            if jj < 0 or jj >= width:
                continue
            step = int(grid[ii][jj]) - current_height
            if step == 1:
                queue.append(n)

    return len(tops)


def part_1() -> int:
    grid = input.read_text().splitlines()

    trailheads = []

    for x, line in enumerate(grid):
        for y, height in enumerate(line):
            if height == "0":
                trailheads.append((x, y))

    return sum(score(t, grid) for t in trailheads)


def part_2() -> int:
    grid = input.read_text().splitlines()

    trailheads = []

    for x, line in enumerate(grid):
        for y, height in enumerate(line):
            if height == "0":
                trailheads.append((x, y))

    return sum(rating(t, grid) for t in trailheads)


print(part_1())
print(part_2())
