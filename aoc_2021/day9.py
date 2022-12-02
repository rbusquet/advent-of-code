import functools
from collections import defaultdict, deque
from heapq import nlargest
from pathlib import Path
from typing import Iterator, TextIO

N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)

Map = dict[tuple[int, int], int]
Point = tuple[int, int]


def neighborhood(i: int, j: int) -> Iterator[Point]:
    for ii, jj in (N, S, E, W):
        yield i + ii, j + jj


def is_low_point(i: int, j: int, height_map: Map) -> bool:
    return all(
        height_map[i, j] < height_map.get((ii, jj), 10) for ii, jj in neighborhood(i, j)
    )


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        height_map, low_points = generate_low_points(file)

        return sum(height_map[i, j] + 1 for (i, j) in low_points)


def generate_low_points(file: TextIO) -> tuple[Map, list[Point]]:
    height_map = defaultdict[tuple[int, int], int](lambda: 10)
    for i, line in enumerate(file):
        for j, height in enumerate(line.strip()):
            height_map[i, j] = int(height)
        print("".join(i if i == "9" else "." for i in line))
    low_points = []
    for i, j in height_map:
        if is_low_point(i, j, height_map):
            low_points.append((i, j))
    return height_map, low_points


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        height_map, low_points = generate_low_points(file)

        basins = list[int]()
        for i, j in low_points:
            queue = deque[Point]([(i, j)])

            visited = set[Point]()
            while queue:
                current = queue.pop()
                for n in neighborhood(*current):
                    ii, jj = n
                    if n not in visited and height_map[ii, jj] < 9:
                        queue.appendleft(n)
                visited.add(current)
            basins.append(len(visited))
        return functools.reduce(lambda a, b: a * b, nlargest(3, basins))


if __name__ == "__main__":
    print(part_1())
    print(part_2())
