from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


N, S, E, W = (
    (0, -1),
    (0, +1),
    (+1, 0),
    (-1, 0),
)


Position = tuple[int, int]


class Walker:
    PIPES = {
        "|": {N: N, S: S},
        "L": {S: E, W: N},
        "F": {N: E, W: S},
        "7": {E: S, N: W},
        "J": {E: N, S: W},
        "-": {E: E, W: W},
    }

    def __init__(
        self, initial_position: Position, initial_direction: Position, pipes: list[str]
    ) -> None:
        self.loop = [initial_position]
        self.initial_direction = initial_direction
        self.pipes = pipes

    @property
    def position(self) -> Position:
        return self.loop[-1]

    def walk(self, direction) -> Position:
        x, y = self.position[0] + direction[0], self.position[1] + direction[1]
        next_pipe = self.pipes[y][x]

        if next_pipe == "S":
            self.loop.append((x, y))
            return self.initial_direction

        if next_pipe not in self.PIPES:
            raise Exception()
        if direction not in self.PIPES[next_pipe]:
            raise Exception()
        self.loop.append((x, y))
        return self.PIPES[next_pipe][direction]

    def contained_area(self) -> int:
        x_values, y_values = zip(*self.loop)

        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)

        area = 0
        vertices = [
            (x, y) for (x, y) in self.loop if self.pipes[y][x] in ["L", "7", "J", "F"]
        ]
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if self._is_inside(x, y, vertices):
                    area += 1
        return area

    def _is_inside(self, x: int, y: int, vertices) -> bool:
        count = 0
        if (x, y) in self.loop:
            return False
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            if (y1 > y) != (y2 > y):
                if x1 + (y - y1) / (y2 - y1) * (x2 - x1) > x:
                    count += 1
        return count % 2 == 1


def part_1(file: TextIO) -> None:
    file.seek(0)

    pipes = []

    initial = (0, 0)
    for y, row in enumerate(strip_lines(file)):
        pipes.append(row)
        if "S" in row:
            initial = (row.index("S"), y)

    for direction in (N, S, E, W):
        walker = Walker(initial, direction, pipes)
        try:
            last_direction = direction
            direction = walker.walk(last_direction)
            next_x, next_y = walker.position
        except Exception:
            continue
        steps = 1

        while pipes[next_y][next_x] != "S":
            try:
                last_direction = direction
                direction = walker.walk(last_direction)
                steps += 1
                next_x, next_y = walker.position
            except Exception:
                break
        else:
            print(steps // 2)
            print(walker.contained_area())
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    part_1(args.file)
