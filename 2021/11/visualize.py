from __future__ import annotations

import time
from curses import A_BOLD, wrapper
from itertools import count, product
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from curses import _CursesWindow as Window

Point = tuple[int, int]


def neighborhood(point: Point) -> Iterator[Point]:
    x, y = point
    for i, j in product([-1, 0, 1], repeat=2):
        if i == j == 0:
            continue
        yield x + i, y + j


def main(stdscr: Window) -> None:  # noqa: C901

    universe = dict[Point, int]()
    with open(Path(__file__).parent / "input.txt") as file:
        for i, line in enumerate(file):
            for j, brightness in enumerate(line.strip()):
                universe[i, j] = int(brightness)
    flashes = 0
    for step in count():
        stdscr.clear()
        stdscr.addstr(0, 0, f"Flashes: {flashes}")
        stdscr.addstr(1, 0, f"Steps: {step}")
        for i in range(10):
            for j in range(10):
                if universe[i, j] > 9:
                    stdscr.addstr(i + 2, j * 2, "🀫", A_BOLD)
                elif universe[i, j] > 5:
                    stdscr.addstr(i + 2, j * 2, "🀆")
        stdscr.move(0, 20)

        # zero flashed
        for point in universe:
            if universe[point] > 9:
                flashes += 1
                universe[point] = 0
        for point in universe:
            universe[point] += 1

        flashed = set()
        while True:
            flashing = [
                point
                for point in universe
                if universe[point] > 9 and point not in flashed
            ]
            if not flashing:
                break

            for point in flashing:
                flashed.add(point)
                for n in neighborhood(point):
                    if n not in universe:
                        continue
                    universe[n] += 1

        stdscr.refresh()
        time.sleep(0.1)


wrapper(main)
