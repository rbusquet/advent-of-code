import re
from collections import Counter
from pathlib import Path
from typing import Iterator, NamedTuple, TextIO

expression = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


class VentLine(NamedTuple):
    x1: int
    y1: int
    x2: int
    y2: int

    def vertical(self) -> bool:
        return self.x1 == self.x2

    def horizontal(self) -> bool:
        return self.y1 == self.y2

    def slope(self) -> int:
        return int((self.y2 - self.y1) / (self.x2 - self.x1))

    def y_intercept(self) -> int:
        # y1 = slope * x1 + b => b = y1 - x1 * slope
        return self.y1 - self.slope() * self.x1

    def all_points(self) -> Iterator[tuple[int, int]]:
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
                yield x, self.slope() * x + self.y_intercept()


def get_coverage(file: TextIO, non_diagonal: bool = True) -> Iterator[tuple[int, int]]:
    for line in file:
        if match := expression.match(line):
            vent_line = VentLine(*map(int, match.groups()))
            if not non_diagonal or vent_line.horizontal() or vent_line.vertical():
                yield from vent_line.all_points()


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        coverage = Counter(get_coverage(file))

        # remove 1s
        coverage -= Counter(coverage.keys())
        return len(coverage)


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        coverage = Counter(get_coverage(file, non_diagonal=False))

        # remove 1s
        coverage -= Counter(coverage.keys())
        return len(coverage)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
