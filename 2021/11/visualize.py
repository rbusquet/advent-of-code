from __future__ import annotations

import curses
import sys
import time
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

    curses.use_default_colors()
    curses.curs_set(0)

    stdscr.nodelay(True)

    for i in range(1, 12):
        curses.init_pair(i, curses.COLORS - 2 * 13 + 2 * i, -1)

    with open(Path(__file__).parent / "input.txt") as file:
        for i, line in enumerate(file):
            for j, brightness in enumerate(line.strip()):
                universe[i, j] = int(brightness)
    flashes = 0
    match sys.argv:
        case [_, m]:
            multiplier = float(f"0.{m}")
        case _:
            multiplier = 0.1
    for step in count():
        match stdscr.getch():
            case 113:
                return

        stdscr.addstr(0, 0, f"Flashes: {flashes}")
        stdscr.addstr(1, 0, f"Steps: {step}")
        stdscr.addstr(13, 0, 'Press "q" to quit', curses.A_RIGHT)
        for i in range(11):
            stdscr.addstr(12, i, "██", curses.color_pair(i + 1))
        for i in range(10):
            for j in range(10):
                if universe[i, j] == 0:
                    continue
                if universe[i, j] > 9:
                    stdscr.addstr(i + 2, j * 2, "██", curses.color_pair(11))
                else:
                    stdscr.addstr(
                        i + 2, j * 2, "██", curses.color_pair(universe[i, j] + 1)
                    )

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

        time.sleep(multiplier)


curses.wrapper(main)
