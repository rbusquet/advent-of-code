from itertools import count, product
from pathlib import Path
from typing import Iterator

Point = tuple[int, int]


def neighborhood(point: Point) -> Iterator[Point]:
    x, y = point
    for i, j in product([-1, 0, 1], repeat=2):
        if i == j == 0:
            continue
        yield x + i, y + j


def flash(point: Point, universe: dict[Point, int], flashed: set[Point]) -> None:
    for n in neighborhood(point):
        if n not in universe:
            continue
        universe[n] += 1
        if universe[n] > 9 and n not in flashed:
            flashed.add(n)
            flash(n, universe, flashed)


def part_1_and_2() -> tuple[int, int]:
    universe = dict[Point, int]()
    with open(Path(__file__).parent / "input.txt") as file:
        for i, line in enumerate(file):
            for j, brightness in enumerate(line.strip()):
                universe[i, j] = int(brightness)

    flashes_after_100 = 0
    for step in count():
        flashed = propagate_energy(universe)

        if step <= 99:
            flashes_after_100 += len(flashed)
        if len(flashed) == 100:
            break
        # zero flashed
        for point in universe:
            if universe[point] > 9:
                universe[point] = 0
    return flashes_after_100, step


def propagate_energy(universe: dict[Point, int]) -> set[Point]:
    for point in universe:
        universe[point] += 1
    flashed = set[Point]()
    while True:
        flashing = [
            point for point in universe if universe[point] > 9 and point not in flashed
        ]
        if not flashing:
            break

        for point in flashing:
            flashed.add(point)
            for n in neighborhood(point):
                if n not in universe:
                    continue
                universe[n] += 1
    return flashed


if __name__ == "__main__":
    print(part_1_and_2())
