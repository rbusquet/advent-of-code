import re
from collections import Counter
from pathlib import Path
from typing import NamedTuple, TextIO

expression = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


class VentLine(NamedTuple):
    x1: int
    y1: int
    x2: int
    y2: int

    def vertical(self):
        return self.x1 == self.x2

    def horizontal(self):
        return self.y1 == self.y2

    @property
    def slope(self):
        return (self.y2 - self.y1) / (self.x2 - self.x1)

    @property
    def y_intercept(self):
        # y1 = slope * x1 + b => b = y1 - x1 * slope
        return self.y1 - self.slope * self.x1

    def all_points(self):
        x1, x2 = sorted([self.x1, self.x2])
        y1, y2 = sorted([self.y1, self.y2])

        if x1 == x2:
            for y in range(y1, y2 + 1):
                yield x1, y
        elif y1 == y2:
            for x in range(x1, x2 + 1):
                yield x, y1
        else:
            for x in range(x1, x2 + 1):
                yield x, self.slope * x + self.y_intercept


def get_coverage(file: TextIO, non_diagonal: bool = True) -> tuple[int, int]:
    for line in file:
        if match := expression.match(line):
            vent_line = VentLine(*map(int, match.groups()))
            if not non_diagonal or vent_line.horizontal() or vent_line.vertical():
                yield from vent_line.all_points()


def print_coverage(coverage: Counter[tuple[int, int]]):
    for i in range(20):
        for j in range(20):
            print(coverage.get((i, j)) or ".", end="")
        print()


def part_1():
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        coverage = Counter(get_coverage(file))

        # print_coverage(coverage)
        # remove 1s
        coverage -= Counter(coverage.keys())
        return len(coverage)


def part_2():
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        coverage = Counter(get_coverage(file, non_diagonal=False))

        # print_coverage(coverage)
        # remove 1s
        coverage -= Counter(coverage.keys())
        return len(coverage)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
