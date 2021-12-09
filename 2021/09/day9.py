from pathlib import Path
from typing import TextIO

N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)

Map = dict[tuple[int, int], int]
Point = tuple[int, int]


def is_low_point(i: int, j: int, height_map: Map) -> bool:
    neighbors = []
    for ii, jj in (N, S, E, W):
        if (i + ii, j + jj) in height_map:
            neighbors.append(height_map[i + ii, j + jj])
    return all(height_map[i, j] < n for n in neighbors)


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        height_map, low_points = generate_low_points(file)

        return sum(height_map[i, j] + 1 for (i, j) in low_points)


def generate_low_points(file: TextIO) -> tuple[Map, list[Point]]:
    height_map = dict[tuple[int, int], int]()
    for i, line in enumerate(file):
        for j, height in enumerate(line.strip()):
            height_map[i, j] = int(height)
    low_points = []
    for i, j in height_map:
        if is_low_point(i, j, height_map):
            low_points.append((i, j))
    return height_map, low_points


def part_2() -> int:  # type: ignore[return]
    with open(Path(__file__).parent / "input.txt") as file:
        height_map, low_points = generate_low_points(file)
        pass


if __name__ == "__main__":
    print(part_1())
    print(part_2())
