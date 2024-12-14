from __future__ import annotations

import curses
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path

input = Path(__file__).parent / "input.txt"


@dataclass
class Robot:
    speed: tuple[int, int]
    start: tuple[int, int]

    @classmethod
    def from_line(cls, line: str) -> Robot:
        start, speed = line.split(" ")
        return cls(
            speed=eval(speed.split("=")[1]),
            start=eval(start.split("=")[1]),
        )

    def position(self, time: int) -> tuple[int, int]:
        x = self.start[0] + time * self.speed[0]
        y = self.start[1] + time * self.speed[1]
        return (x, y)


def part_1() -> int:
    robots = defaultdict[tuple[int, int], list[Robot]](list)
    for line in input.read_text().splitlines():
        robot = Robot.from_line(line)
        robots[robot.start].append(robot)

    width = 101
    height = 103

    mid_x = width // 2
    mid_y = height // 2

    quadrants = [0, 0, 0, 0]
    for i in range(height):
        for j in range(width):
            print(len(robots[j, i]) or ".", end="")
        print()
    final = defaultdict[tuple[int, int], list[Robot]](list)

    for position in robots:
        for robot in robots[position]:
            position = robot.position(100)
            x = position[0] % width
            y = position[1] % height
            final[x, y].append(robot)

            if x < mid_x and y < mid_y:
                quadrants[0] += 1
            if x < mid_x and y > mid_y:
                quadrants[1] += 1
            if x > mid_x and y > mid_y:
                quadrants[2] += 1
            if x > mid_x and y < mid_y:
                quadrants[3] += 1
    print("-----------")
    for i in range(height):
        for j in range(width):
            if i == mid_x - 2:
                print(" ", end="")
            elif j == mid_y + 2:
                print(" ", end="")
            else:
                print(len(final[j, i]) or ".", end="")
        print()
    print(quadrants)
    return reduce(mul, quadrants, 1)


def part_2(stdscr: curses.window) -> int:
    stdscr.clear()
    robots = list[Robot]()
    for line in input.read_text().splitlines():
        robot = Robot.from_line(line)
        robots.append(robot)

    width = 101
    height = 103
    seconds = 7916

    pad = curses.newpad(110, 110)
    while True:
        pad.addstr(0, 0, f"Time elapsed: {seconds}")
        robots_by_position = defaultdict[tuple[int, int], int](int)
        for robot in robots:
            x, y = robot.position(seconds)
            x %= width
            y %= height
            robots_by_position[x, y] += 1

        for i in range(height):
            for j in range(width):
                pad.addstr(j + 1, i, str(robots_by_position[i, j] or "."))
        rows, cols = stdscr.getmaxyx()
        pad.refresh(0, 0, 0, 0, rows - 1, cols - 1)
        if seconds == 7916:
            pad.refresh(0, 0, 0, 0, rows - 1, cols - 1)
            if pad.getkey() == "c":
                return 0

        else:
            seconds += 1


print(part_1())
curses.wrapper(part_2)
