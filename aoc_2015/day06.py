from collections import defaultdict
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    grid = defaultdict[tuple[int, int], int](int)

    for line in input.read_text().splitlines():
        match line.split():
            case ["turn", "on", start_str, "through", end_str]:
                start = eval(start_str)
                end = eval(end_str)
                for x in range(start[0], end[0] + 1):
                    for y in range(start[1], end[1] + 1):
                        grid[x, y] = 1
            case ["turn", "off", start_str, "through", end_str]:
                start = eval(start_str)
                end = eval(end_str)
                for x in range(start[0], end[0] + 1):
                    for y in range(start[1], end[1] + 1):
                        grid[x, y] = 0
            case ["toggle", start_str, "through", end_str]:
                start = eval(start_str)
                end = eval(end_str)
                for x in range(start[0], end[0] + 1):
                    for y in range(start[1], end[1] + 1):
                        grid[x, y] = not grid[x, y]
    return sum(grid.values())


def part_2() -> int:
    grid = defaultdict[tuple[int, int], int](int)

    for line in input.read_text().splitlines():
        match line.split():
            case ["turn", "on", start_str, "through", end_str]:
                start = eval(start_str)
                end = eval(end_str)
                for x in range(start[0], end[0] + 1):
                    for y in range(start[1], end[1] + 1):
                        grid[x, y] += 1
            case ["turn", "off", start_str, "through", end_str]:
                start = eval(start_str)
                end = eval(end_str)
                for x in range(start[0], end[0] + 1):
                    for y in range(start[1], end[1] + 1):
                        grid[x, y] = max(grid[x, y] - 1, 0)
            case ["toggle", start_str, "through", end_str]:
                start = eval(start_str)
                end = eval(end_str)
                for x in range(start[0], end[0] + 1):
                    for y in range(start[1], end[1] + 1):
                        grid[x, y] += 2
    return sum(grid.values())


print(part_1())
print(part_2())
