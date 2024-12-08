from itertools import cycle
from pathlib import Path

from more_itertools import seekable

input = Path(__file__).parent / "input.txt"


def find_guard(grid: list[list[str]]) -> tuple[int, int]:
    for x, line in enumerate(grid):
        for y, col in enumerate(line):
            if col == "^":
                return x, y
    raise Exception("invalid input")


def next_step(x: int, y: int, direction: int) -> tuple[int, int]:
    match direction:
        case 0:
            x -= 1
        case 1:
            y += 1
        case 2:
            x += 1
        case 3:
            y -= 1
    return x, y


def part_1() -> set[tuple[int, int]]:
    grid = [list(line) for line in input.read_text().splitlines()]
    height = len(grid)
    width = len(grid[0])

    x, y = find_guard(grid)
    visited = set[tuple[int, int]]([(x, y)])
    directions = cycle(range(4))

    direction = next(directions)
    start = x, y, direction

    while True:
        # print("\n".join("".join(line) for line in grid))
        x, y = next_step(*start)
        if x < 0 or x >= height:
            break
        if y < 0 or y > width:
            break
        while grid[x][y] == "#":
            direction = next(directions)
            x, y = next_step(start[0], start[1], direction)
        # grid[x][y] = "X"
        start = x, y, direction
        visited.add((x, y))

    return visited


def part_2() -> int:
    grid = [list(line) for line in input.read_text().splitlines()]
    height = len(grid)
    width = len(grid[0])

    guard = find_guard(grid)
    result = 0

    path = part_1()

    for xx, yy in path:
        if guard == (xx, yy):
            continue
        x, y = guard
        directions = seekable(cycle(range(4)))
        direction = next(directions)
        visited = set([(x, y, direction)])

        start = x, y, direction
        while True:
            # print("\n".join("".join(line) for line in grid))
            x, y = next_step(*start)
            if x < 0 or x >= height:
                break
            if y < 0 or y >= width:
                break
            found_obsctruction = False
            while grid[x][y] == "#" or (x == xx and y == yy):
                found_obsctruction = True
                direction = next(directions)
                x, y = next_step(start[0], start[1], direction)
            grid[x][y] = "X"
            start = x, y, direction
            if found_obsctruction and start in visited:
                # found loop
                result += 1
                break

            visited.add(start)

    return result


# print(part_1())
print(part_2())
